#!/bin/bash

# Suppress Warnings
export ROS_PYTHON_WARNINGS="ignore"
export GAZEBO_ROS_CMD_WARNINGS="0"
export DISABLE_ROS1_EOL_WARNINGS="1"

# =============================================================================
# Configuration
# =============================================================================
# If SINGLE_* env vars are set (Docker mode), use them.
# Otherwise, fall back to the full matrix (legacy mode).
# =============================================================================

if [ -n "$SINGLE_GLOBAL_PLANNER" ]; then
    # ---- Docker Single-Planner Mode ----
    GLOBAL_PLANNERS=("$SINGLE_GLOBAL_PLANNER")
    LOCAL_PLANNERS=("$SINGLE_LOCAL_PLANNER")
    SCENARIOS=("$SINGLE_SCENARIO")
    NUM_RUNS="${SINGLE_NUM_RUNS:-30}"

    # Parse colon-separated sweep values
    if [ "$SINGLE_SWEEP_VALUES" == "default" ] || [ -z "$SINGLE_SWEEP_VALUES" ]; then
        SWEEP_VALUES_ARRAY=("default")
    else
        IFS=':' read -ra SWEEP_VALUES_ARRAY <<< "$SINGLE_SWEEP_VALUES"
    fi
    echo "[Docker Mode] Single planner: ${GLOBAL_PLANNERS[0]}+${LOCAL_PLANNERS[0]} | Scenario: ${SCENARIOS[0]} | Runs: $NUM_RUNS"
else
    # ---- Legacy Full Matrix Mode ----
    GLOBAL_PLANNERS=("astar" "hybrid_astar" "dijkstra" "lazy_theta_star" "dstar_lite" "rrt")
    LOCAL_PLANNERS=("dwa" "apf")
    SCENARIOS=("static" "dynamic")
    NUM_RUNS="30"
    SWEEP_VALUES_ARRAY=("default")
fi

# Headless mode: disable GUI when BENCHMARK_HEADLESS is set
if [ "${BENCHMARK_HEADLESS}" == "1" ]; then
    export BENCHMARK_GUI=false
    echo "[Headless Mode] Gazebo GUI and RViz disabled."
fi

START_TIME="30.0"
MAX_TIMEOUT="180.0"
CONFIG_FILE="../src/user_config/user_config.yaml"
SUMMARY_FILE="$(pwd)/../src/plannie-main/results/battery_summary_$(date +%Y%m%d_%H%M%S).csv"

echo "=========================================="
echo "      Benchmark Battery Suite"
echo "=========================================="
echo "Global Planners: ${GLOBAL_PLANNERS[*]}"
echo "Local Planners: ${LOCAL_PLANNERS[*]}"
echo "Scenarios: ${SCENARIOS[*]}"
echo "Runs per Config: $NUM_RUNS"
echo "Sweep Values: ${SWEEP_VALUES_ARRAY[*]}"
echo "Summary File: $SUMMARY_FILE"
echo "=========================================="

# Create summary header
if [ ! -f "$SUMMARY_FILE" ]; then
    echo "Scenario,GlobalPlanner,LocalPlanner,SweepParam,StartX,StartY,GoalX,GoalY,Status,Time(s),Distance(m),CPU(%),Memory(%),Memory(MiB),TotalRAM(GiB)" > "$SUMMARY_FILE"
fi

for scenario in "${SCENARIOS[@]}"; do
    for global in "${GLOBAL_PLANNERS[@]}"; do
        for local in "${LOCAL_PLANNERS[@]}"; do
            
            # 1. Update Configuration (Global/Local)
            echo ""
            echo ">>> Configuring: Scenario=$scenario | Global=$global | Local=$local"
            sed -i "s/robot1_global_planner: \".*\"/robot1_global_planner: \"$global\"/" "$CONFIG_FILE"
            sed -i "s/robot1_local_planner: \".*\"/robot1_local_planner: \"$local\"/" "$CONFIG_FILE"
            
            if [ "$scenario" == "dynamic" ]; then
                sed -i 's/.*pedestrians: "pedestrian_config.yaml"/  pedestrians: "pedestrian_config.yaml"/' "$CONFIG_FILE"
            else
                sed -i 's/.*pedestrians: "pedestrian_config.yaml"/  # pedestrians: "pedestrian_config.yaml"/' "$CONFIG_FILE"
            fi

            # Define Parameter Sweep Options based on Planners
            if [ -n "$SINGLE_GLOBAL_PLANNER" ]; then
                # Docker mode: use env-provided sweep values
                PARAM_SWEEPS=("${SWEEP_VALUES_ARRAY[@]}")
            elif [ "$global" == "rrt" ]; then
                PARAM_SWEEPS=("10.0" "20.0" "30.0")
            else
                PARAM_SWEEPS=("default")
            fi

            for sweep_val in "${PARAM_SWEEPS[@]}"; do
                echo ">>> Using Parameter Sweep Value: $sweep_val"
                
                if [ "$global" == "rrt" ] && [ "$sweep_val" != "default" ]; then
                    sed -i "s/sample_max_distance: .*/sample_max_distance: $sweep_val/" ../src/core/system_config/system_config/system_config.pb.txt
                fi

                # Loop for Repetitions
                for (( i=1; i<=NUM_RUNS; i++ )); do
                    echo "------------------------------------------"
                    echo "    Run $i / $NUM_RUNS (Sweep: $sweep_val)"
                    echo "------------------------------------------"
                    
                    # Generate Random Start and Goal
                    MAP_FILE="../src/sim_env/maps/warehouse/warehouse.yaml"
                    POSES=$(python generate_random_poses.py "$MAP_FILE")
                    START_X=$(echo $POSES | awk '{print $1}')
                    START_Y=$(echo $POSES | awk '{print $2}')
                    GOAL_X=$(echo $POSES | awk '{print $3}')
                    GOAL_Y=$(echo $POSES | awk '{print $4}')
                    
                    echo ">>> Random Poses: Start($START_X, $START_Y) -> Goal($GOAL_X, $GOAL_Y)"
                    sed -i "s/robot1_x_pos: \".*\"/robot1_x_pos: \"$START_X\"/" "$CONFIG_FILE"
                    sed -i "s/robot1_y_pos: \".*\"/robot1_y_pos: \"$START_Y\"/" "$CONFIG_FILE"
                
                    # 2. Cleanup
                    echo "[1/4] Cleaning process..."
                    ./killpro.sh > /dev/null 2>&1
                    sleep 5
                    
                    # 3. Start Simulation
                    echo "[2/4] Starting Simulation..."
                    ./main.sh > /dev/null 2>&1 &
                    SIM_PID=$!
                    
                    # 4. Wait for Readiness
                    echo "[3/4] Waiting for System..."
                    source ../devel/setup.bash
                    TIMEOUT=300
                    START_WAIT=$(date +%s)
                    READY=false
                    
                    while true; do
                        if rostopic list > /dev/null 2>&1; then
                            if rostopic list | grep -q "/move_base/status"; then
                                READY=true
                                break
                            fi
                        fi
                        
                        CURRENT_TIME=$(date +%s)
                        ELAPSED=$((CURRENT_TIME - START_WAIT))
                        
                        if [ $ELAPSED -gt $TIMEOUT ]; then
                            echo "Timeout waiting for simulation! (Retry or exit logic needed)"
                            ./killpro.sh
                            exit 1
                        fi
                        sleep 2
                    done
                    
                    echo "System Ready. Resetting AMCL..."
                    rostopic pub -1 /initialpose geometry_msgs/PoseWithCovarianceStamped "{header: {frame_id: 'map'}, pose: {pose: {position: {x: $START_X, y: $START_Y, z: 0.0}, orientation: {w: 1.0}}}}" > /dev/null 2>&1
                    sleep 5
                    
                    # 5. Run Benchmark
                    echo "[4/4] Executing Benchmark Test..."
                    roslaunch plannie benchmark.launch planner:="${scenario}_${global}_${local}_${sweep_val}_run${i}" goal_x:=$GOAL_X goal_y:=$GOAL_Y summary_file:=$SUMMARY_FILE target_startup_time:=$START_TIME max_timeout:=$MAX_TIMEOUT
                    
                    echo ">>> Finished Run $i: ${scenario}_${global}_${local}_${sweep_val}"
                    
                    # Cleanup
                    ./killpro.sh > /dev/null 2>&1
                    sleep 2
                done
            done
        done
    done
done

echo "=========================================="
echo "      Battery Complete!"
echo "Summary saved to: $SUMMARY_FILE"
echo "=========================================="
# Print summary to console
if [ -f "$SUMMARY_FILE" ]; then
    echo "Results:"
    cat "$SUMMARY_FILE" | column -t -s,
fi
