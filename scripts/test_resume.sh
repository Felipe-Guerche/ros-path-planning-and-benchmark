#!/bin/bash

# =============================================================================
#  Parallel Benchmark Runner (Orchestrator)
#  Builds the Docker image once and launches N containers in parallel,
#  each running one planner combination with fixed CPU/RAM.
#
#  All values below are easily configurable.
# =============================================================================

set -e

# Change to the root workspace folder to ensure all paths resolve correctly
cd "$(dirname "$0")/.."

# ===================== MODULAR CONFIGURATION =====================

# Docker image name
DOCKER_IMAGE="ros-benchmark"
DOCKERFILE_PATH="./docker/noetic"

# --- Hardware Budget ---
# Adjust these to your machine. The script will launch MAX_WORKERS
# containers, each limited to CPUS_PER_WORKER cores and RAM_PER_WORKER memory.
MAX_WORKERS=4              # Number of parallel containers
CPUS_PER_WORKER="3.0"      # CPU threads per container (docker --cpus)
RAM_PER_WORKER="6g"        # RAM per container (docker --memory)

# --- Benchmark Matrix ---
# Each combination of (SCENARIO, GLOBAL, LOCAL) becomes a "job".
# Jobs are queued and dispatched to workers as they become available.
SCENARIOS=("static" "dynamic")
GLOBAL_PLANNERS=("astar")
LOCAL_PLANNERS=("dwa")
NUM_RUNS=2                # Repetitions per job

# --- Randomization & Reproducibility ---
# Set to a number (e.g., 42) to force the exact same obstacle and start/goal
# positions across all planners. Set to "random" for a new random sequence.
MASTER_SEED="random"

# --- Parameter Sweep ---
# Define sweep values per global planner. Use "default" for no sweep.
# Format: SWEEP_<PLANNER>="val1:val2:val3"
SWEEP_rrt="10.0:20.0:30.0"
# Add more as needed, e.g.:
# SWEEP_astar="euclidean:manhattan:octile"

# --- Port Allocation ---
# Each worker gets a unique pair of ports to isolate ROS/Gazebo masters.
BASE_ROS_PORT=11311
BASE_GAZEBO_PORT=11345

# --- Output ---
RESULTS_DIR="$(pwd)/results"
mkdir -p "$RESULTS_DIR"

# =================================================================

# =================================================================
# Resolve Master Seed (with Persistence for Pause & Resume)
# =================================================================
SEED_FILE="$RESULTS_DIR/.master_seed"

if [ "$MASTER_SEED" == "random" ]; then
    if [ -f "$SEED_FILE" ]; then
        # Load existing seed to maintain parity with cached jobs
        MASTER_SEED=$(cat "$SEED_FILE")
        echo "[State] Resuming with persisted random seed: $MASTER_SEED"
    else
        # Initialize new run and persist seed
        MASTER_SEED=$RANDOM
        echo "$MASTER_SEED" > "$SEED_FILE"
        echo "[State] Generated and persisted new random seed: $MASTER_SEED"
    fi
else
    # Enforce explicit seed and sync to state file
    echo "$MASTER_SEED" > "$SEED_FILE"
    echo "[State] Using explicit fixed seed: $MASTER_SEED"
fi

echo "============================================="
echo "  Parallel Benchmark Orchestrator"
echo "============================================="
echo "  Workers      : $MAX_WORKERS"
echo "  CPUs/Worker  : $CPUS_PER_WORKER"
echo "  RAM/Worker   : $RAM_PER_WORKER"
echo "  Runs/Job     : $NUM_RUNS"
echo "  Master Seed  : $MASTER_SEED"
echo "  Results Dir  : $RESULTS_DIR"
echo "============================================="

# Record the start time
START_TIME=$(date +%s)

# --- Step 1: Build Docker Image ---
echo ""
echo "[1/3] Building Docker image '$DOCKER_IMAGE'..."
docker build -t "$DOCKER_IMAGE" -f "$DOCKERFILE_PATH/Dockerfile" .
echo "      Build complete."

# --- Step 2: Generate Job Queue ---
# Each job is a string: "scenario|global|local|sweep_values"
JOBS=()
for scenario in "${SCENARIOS[@]}"; do
    for global in "${GLOBAL_PLANNERS[@]}"; do
        for local in "${LOCAL_PLANNERS[@]}"; do
            # Check if there's a sweep for this global planner
            sweep_var="SWEEP_${global}"
            sweep_vals="${!sweep_var:-default}"
            JOBS+=("${scenario}|${global}|${local}|${sweep_vals}")
        done
    done
done

TOTAL_JOBS=${#JOBS[@]}
echo ""
echo "[2/3] Generated $TOTAL_JOBS jobs. Dispatching to $MAX_WORKERS workers..."
echo ""

# --- Step 3: Dispatch Jobs ---
# Simple round-robin dispatcher with GNU parallel-style wait.
RUNNING_PIDS=()
WORKER_ID=0
JOB_INDEX=0

dispatch_job() {
    local job="$1"
    local wid="$2"

    IFS='|' read -r scenario global local sweep_vals <<< "$job"

    local ros_port=$((BASE_ROS_PORT + wid))
    local gazebo_port=$((BASE_GAZEBO_PORT + wid))

    # Create a deterministic tag for this job: scenario_global_local_sweep (first 3 chars)
    local sweep_tag=$(echo "$sweep_vals" | cut -c1-3 | tr -d ':')
    local job_tag="${scenario}_${global}_${local}_${sweep_tag}"
    local container_name="benchmark_${job_tag}"

    # --- Check if Job is already complete ---
    local summary_file="$RESULTS_DIR/battery_summary_${job_tag}.csv"
    if [ -f "$summary_file" ]; then
        # Calculate expected lines: (Peds * Sweeps * Inflations * Runs) + 1
        local n_peds=1; [ "$scenario" == "dynamic" ] && n_peds=3
        local n_inflations=3
        local n_sweeps=$(echo "$sweep_vals" | tr ':' '\n' | wc -l)
        [ "$sweep_vals" == "default" ] && n_sweeps=1
        
        local expected=$(( (n_peds * n_sweeps * n_inflations * NUM_RUNS) + 1 ))
        local actual=$(wc -l < "$summary_file")

        if [ "$actual" -ge "$expected" ]; then
            echo "  [Skip] Job $job_tag is already complete ($actual/$expected rows)."
            return 0
        else
            local completed_runs=$(( actual - 1 ))
            [ "$completed_runs" -lt 0 ] && completed_runs=0
            echo "  [Resume] Job $job_tag is partial ($actual/$expected rows). Resuming from row $((completed_runs + 1))..."
            RESUME_FROM_ROW="$completed_runs"
        fi
    else
        RESUME_FROM_ROW=0
    fi

    echo "  [Worker $wid] Starting: $scenario | $global + $local | sweep=$sweep_vals"

    docker run --rm \
        --name "$container_name" \
        --cpus="$CPUS_PER_WORKER" \
        --memory="$RAM_PER_WORKER" \
        -e WORKER_ID="$wid" \
        -e SINGLE_GLOBAL_PLANNER="$global" \
        -e SINGLE_LOCAL_PLANNER="$local" \
        -e SINGLE_SCENARIO="$scenario" \
        -e SINGLE_NUM_RUNS="$NUM_RUNS" \
        -e SINGLE_SWEEP_VALUES="$sweep_vals" \
        -e JOB_TAG="$job_tag" \
        -e MASTER_SEED="$MASTER_SEED" \
        -e RESUME_FROM_ROW="${RESUME_FROM_ROW:-0}" \
        -e ROS_MASTER_PORT="$ros_port" \
        -e GAZEBO_MASTER_PORT="$gazebo_port" \
        -v "$RESULTS_DIR:/project/src/plannie-main/results" \
        "$DOCKER_IMAGE" \
        > "$RESULTS_DIR/log_${container_name}.txt" 2>&1 &

    RUNNING_PIDS+=($!)
}

# Wait for a slot to open up
wait_for_slot() {
    while [ ${#RUNNING_PIDS[@]} -ge $MAX_WORKERS ]; do
        local new_pids=()
        for pid in "${RUNNING_PIDS[@]}"; do
            if kill -0 "$pid" 2>/dev/null; then
                new_pids+=("$pid")
            else
                wait "$pid" 2>/dev/null || true
            fi
        done
        RUNNING_PIDS=("${new_pids[@]}")
        if [ ${#RUNNING_PIDS[@]} -ge $MAX_WORKERS ]; then
            sleep 5
        fi
    done
}

# Dispatch all jobs
for job in "${JOBS[@]}"; do
    wait_for_slot
    prev_count=${#RUNNING_PIDS[@]}
    dispatch_job "$job" "$WORKER_ID"
    # Only advance WORKER_ID when a container was actually dispatched
    if [ ${#RUNNING_PIDS[@]} -gt $prev_count ]; then
        WORKER_ID=$(( (WORKER_ID + 1) % MAX_WORKERS ))
    fi
    JOB_INDEX=$((JOB_INDEX + 1))
    echo "      ($JOB_INDEX / $TOTAL_JOBS jobs dispatched)"
done

# Wait for all remaining workers
echo ""
echo "All jobs dispatched. Waiting for remaining workers to finish..."
for pid in "${RUNNING_PIDS[@]}"; do
    wait "$pid" 2>/dev/null || true
done

# --- Step 4: Aggregate Results ---
echo ""
echo "[3/3] Aggregating results..."

# Fix permissions for files created by docker (root) before analyzing locally
docker run --rm --entrypoint /bin/chown -v "$RESULTS_DIR:/results" ubuntu -R $(id -u):$(id -g) /results > /dev/null 2>&1 || true

python scripts/analyze_results.py --results_dir "$RESULTS_DIR" --plot --plot_dir "$RESULTS_DIR/figures"

echo ""
echo "============================================="
echo "  All benchmarks complete!"
echo "  Results: $RESULTS_DIR"

# Calculate total execution time
END_TIME=$(date +%s)
TOTAL_SECONDS=$((END_TIME - START_TIME))
HOURS=$((TOTAL_SECONDS / 3600))
MINUTES=$(( (TOTAL_SECONDS % 3600) / 60 ))
SECONDS=$((TOTAL_SECONDS % 60))

echo "  Total Time: ${HOURS}h ${MINUTES}m ${SECONDS}s"
echo "============================================="
