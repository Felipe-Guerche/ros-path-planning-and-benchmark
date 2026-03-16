#!/bin/bash
# =============================================================================
#  Parallel Benchmark Runner (Orchestrator)
#  Builds the Docker image once and launches N containers in parallel.
# =============================================================================

set -e

# Change to the root workspace folder
cd "$(dirname "$0")/.."

# ===================== MODULAR CONFIGURATION =====================
DOCKER_IMAGE="ros-benchmark"
DOCKERFILE_PATH="./docker/noetic"

MAX_WORKERS=6              # Number of parallel containers
CPUS_PER_WORKER="2.0"      # CPU threads per container
RAM_PER_WORKER="4g"        # RAM per container

SCENARIOS=("static" "dynamic")
GLOBAL_PLANNERS=("astar" "hybrid_astar" "dijkstra" "lazy_theta_star" "dstar_lite" "rrt")
LOCAL_PLANNERS=("dwa" "apf")
NUM_RUNS=40                # Repetitions per job

# --- Parameter Sweeps ---
SWEEP_rrt="10.0:20.0:30.0"

# --- Port Allocation ---
BASE_ROS_PORT=11311
BASE_GAZEBO_PORT=11345

# --- Randomization & Reproducibility ---
MASTER_SEED="random"
FORCE_NEW_SEED=false
FORCE_RESUME_SEED=false

# Parse Arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --new-seed)
      FORCE_NEW_SEED=true
      shift
      ;;
    --resume)
      FORCE_RESUME_SEED=true
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: $0 [--new-seed] [--resume]"
      exit 1
      ;;
  esac
done

RESULTS_DIR="$(pwd)/results"
mkdir -p "$RESULTS_DIR"

# =================================================================
# Resolve Master Seed
# =================================================================
SEED_FILE="$RESULTS_DIR/.master_seed"

if [ -f "$SEED_FILE" ] && [ "$FORCE_NEW_SEED" = false ] && [ "$FORCE_RESUME_SEED" = false ]; then
    echo "============================================="
    echo "  Existing Seed Found: $(cat "$SEED_FILE")"
    echo "  What would you like to do?"
    echo "  1) Resume with existing seed (keep parity)"
    echo "  2) Generate a NEW random seed (fresh start)"
    echo "============================================="
    read -p "  Enter choice [1/2]: " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[1]$ ]]; then
        MASTER_SEED="random"
        rm -f "$SEED_FILE"
    else
        FORCE_RESUME_SEED=true
    fi
fi

if [ "$FORCE_NEW_SEED" = true ]; then
    rm -f "$SEED_FILE"
    MASTER_SEED="random"
fi

if [ "$MASTER_SEED" == "random" ] && [ "$FORCE_RESUME_SEED" = false ]; then
    if [ -f "$SEED_FILE" ]; then
        MASTER_SEED=$(cat "$SEED_FILE")
        echo "[State] Resuming with persisted random seed: $MASTER_SEED"
    else
        MASTER_SEED=$RANDOM
        echo "$MASTER_SEED" > "$SEED_FILE"
        echo "[State] Generated and persisted new random seed: $MASTER_SEED"
    fi
else
    # Either forced resume or explicit seed
    if [ -f "$SEED_FILE" ]; then
        MASTER_SEED=$(cat "$SEED_FILE")
        echo "[State] Resuming with persisted random seed: $MASTER_SEED"
    else
        # This case only hit if MASTER_SEED was hardcoded to something other than "random"
        echo "$MASTER_SEED" > "$SEED_FILE"
        echo "[State] Using explicit fixed seed: $MASTER_SEED"
    fi
fi

echo "============================================="
echo "  Parallel Benchmark Orchestrator"
echo "============================================="
echo "  Workers      : $MAX_WORKERS"
echo "  CPUs/Worker  : $CPUS_PER_WORKER"
echo "  RAM/Worker   : $RAM_PER_WORKER"
echo "  Runs/Job     : $NUM_RUNS"
echo "  Master Seed  : $MASTER_SEED"
echo "============================================="

RUNNING_PIDS=()

cleanup_on_exit() {
    echo ""
    echo "[State] Interrupt received. Killing background workers..."
    for pid in "${RUNNING_PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            docker ps --filter "name=benchmark_" -q | xargs -r docker rm -f || true
            kill "$pid" 2>/dev/null || true
        fi
    done
    exit 1
}
trap cleanup_on_exit SIGINT SIGTERM

# --- Step 1: Build Docker Image ---
echo "[1/3] Building Docker image '$DOCKER_IMAGE'..."
docker build -t "$DOCKER_IMAGE" -f "$DOCKERFILE_PATH/Dockerfile" .
echo "      Build complete."

# --- Step 2: Generate Job Queue ---
JOBS=()
for scenario in "${SCENARIOS[@]}"; do
    for global in "${GLOBAL_PLANNERS[@]}"; do
        for local in "${LOCAL_PLANNERS[@]}"; do
            sweep_var="SWEEP_${global}"
            sweep_vals="${!sweep_var:-default}"
            JOBS+=("${scenario}|${global}|${local}|${sweep_vals}")
        done
    done
done

TOTAL_JOBS=${#JOBS[@]}
echo "[2/3] Generated $TOTAL_JOBS jobs."

# --- Step 3: Dispatch Jobs ---
WORKER_ID=0
JOB_INDEX=0

dispatch_job() {
    local job="$1"
    local wid="$2"
    IFS='|' read -r scenario global local sweep_vals <<< "$job"

    local ros_port=$((BASE_ROS_PORT + wid))
    local gazebo_port=$((BASE_GAZEBO_PORT + wid))
    local sweep_tag=$(echo "$sweep_vals" | cut -c1-3 | tr -d ':')
    local job_tag="${scenario}_${global}_${local}_${sweep_tag}"
    local container_name="benchmark_${job_tag}"

    local summary_file="$RESULTS_DIR/battery_summary_${job_tag}.csv"
    RESUME_FROM_ROW=0
    if [ -f "$summary_file" ]; then
        local n_peds=1; [ "$scenario" == "dynamic" ] && n_peds=3
        local n_inflations=3
        local n_sweeps=$(echo "$sweep_vals" | tr ':' '\n' | wc -l)
        [ "$sweep_vals" == "default" ] && n_sweeps=1
        local expected=$(( (n_peds * n_sweeps * n_inflations * NUM_RUNS) + 1 ))
        local actual=$(wc -l < "$summary_file")

        if [ "$actual" -ge "$expected" ]; then
            echo "  [Skip] Job $job_tag is already complete."
            return 0
        else
            RESUME_FROM_ROW=$(( actual - 1 ))
            [ "$RESUME_FROM_ROW" -lt 0 ] && RESUME_FROM_ROW=0
            echo "  [Resume] Job $job_tag partial ($actual/$expected). Resuming from row $RESUME_FROM_ROW..."
        fi
    fi

    echo "  [Worker $wid] Starting: $scenario | $global + $local"
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
        -e RESUME_FROM_ROW="$RESUME_FROM_ROW" \
        -e ROS_MASTER_PORT="$ros_port" \
        -e GAZEBO_MASTER_PORT="$gazebo_port" \
        -v "$RESULTS_DIR:/project/src/plannie-main/results" \
        "$DOCKER_IMAGE" \
        > "$RESULTS_DIR/log_${container_name}.txt" 2>&1 &
    RUNNING_PIDS+=($!)
}

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
        [ ${#RUNNING_PIDS[@]} -ge $MAX_WORKERS ] && sleep 5
    done
}

for job in "${JOBS[@]}"; do
    wait_for_slot
    dispatch_job "$job" "$WORKER_ID"
    # Logic to only increment worker ID if a job was actually dispatched
    if [ ${#RUNNING_PIDS[@]} -gt 0 ]; then
         WORKER_ID=$(( (WORKER_ID + 1) % MAX_WORKERS ))
    fi
    JOB_INDEX=$((JOB_INDEX + 1))
    echo "      ($JOB_INDEX / $TOTAL_JOBS dispatched)"
done

echo "Waiting for all workers to finish..."
for pid in "${RUNNING_PIDS[@]}"; do
    wait "$pid" 2>/dev/null || true
done
echo "Benchmark completed."
