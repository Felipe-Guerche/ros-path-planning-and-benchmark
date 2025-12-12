#!/bin/bash

# Suppress Warnings
export ROS_PYTHON_WARNINGS="ignore"
export GAZEBO_ROS_CMD_WARNINGS="0"
export DISABLE_ROS1_EOL_WARNINGS="1" # Correct variable from error message

# Configuration
# Uncomment the planners you want to run
GLOBAL_PLANNERS=("astar" "hybrid_astar" "dijkstra" "lazy_theta_star" "dstar_lite" "rrt")
LOCAL_PLANNERS=("dwa" "apf")

# Scenarios: "static" and/or "dynamic"
# Scenarios: "static" and/or "dynamic"
# SCENARIOS=("static" "dynamic")
SCENARIOS=("static" "dynamic")
GOAL_X="8.5"
GOAL_Y="-4.0"
START_TIME="30.0" # Simulation time to send goal (synchronization)
MAX_TIMEOUT="180.0" # Max duration before killing test (3 mins)
NUM_RUNS="30"        # Number of repetitions per configuration (Academic standard: ~20-30)
CONFIG_FILE="../src/user_config/user_config.yaml"
SUMMARY_FILE="$(pwd)/../src/plannie-main/results/battery_summary_$(date +%Y%m%d_%H%M%S).csv"

echo "=========================================="
echo "      Benchmark Battery Suite"
echo "=========================================="
echo "Global Planners: ${GLOBAL_PLANNERS[*]}"
echo "Local Planners: ${LOCAL_PLANNERS[*]}"
echo "Scenarios: ${SCENARIOS[*]}"
echo "Goal: ($GOAL_X, $GOAL_Y)"
echo "Runs per Config: $NUM_RUNS"
echo "Summary File: $SUMMARY_FILE"
echo "=========================================="

# Create summary header
if [ ! -f "$SUMMARY_FILE" ]; then
    echo "Scenario,GlobalPlanner,LocalPlanner,Status,Time(s),Distance(m),CPU(%),Memory(%),Memory(MiB),TotalRAM(GiB)" > "$SUMMARY_FILE"
fi

for scenario in "${SCENARIOS[@]}"; do
    for global in "${GLOBAL_PLANNERS[@]}"; do
        for local in "${LOCAL_PLANNERS[@]}"; do
            
            # Update Configuration ONLY ONCE per planner combination if desired, 
            # but doing it inside the loop is safer to ensure state reset.
            # Actually, let's configure once here to be efficient? 
            # No, user_config.yaml is modified by sed. Let's do it inside the loop to be safe 
            # or just here. Let's do it here to avoid 30x sed calls if not needed.
            
            # 1. Update Configuration (Global/Local)
            echo ""
            echo ">>> Configuring: Scenario=$scenario | Global=$global | Local=$local"
            sed -i "s/robot1_global_planner: \".*\"/robot1_global_planner: \"$global\"/" "$CONFIG_FILE"
            sed -i "s/robot1_local_planner: \".*\"/robot1_local_planner: \"$local\"/" "$CONFIG_FILE"
            
            if [ "$scenario" == "dynamic" ]; then
                # Enable pedestrians (uncomment)
                sed -i 's/.*pedestrians: "pedestrian_config.yaml"/  pedestrians: "pedestrian_config.yaml"/' "$CONFIG_FILE"
            else
                # Disable pedestrians (comment)
                sed -i 's/.*pedestrians: "pedestrian_config.yaml"/  # pedestrians: "pedestrian_config.yaml"/' "$CONFIG_FILE"
            fi

            # Loop for Repetitions
            for (( i=1; i<=NUM_RUNS; i++ )); do
                echo "------------------------------------------"
                echo "    Run $i / $NUM_RUNS"
                echo "------------------------------------------"
                
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
                        echo "Timeout waiting for simulation ! (Retry or exit logic needed)"
                        ./killpro.sh
                        exit 1
                    fi
                    sleep 2
                done
                
                echo "System Ready. Resetting AMCL..."
                rostopic pub -1 /initialpose geometry_msgs/PoseWithCovarianceStamped "{header: {frame_id: 'map'}, pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}}" > /dev/null 2>&1
                sleep 5
                
                # 5. Run Benchmark (Pass composite planner name for logging)
                echo "[4/4] Executing Benchmark Test..."
                roslaunch plannie benchmark.launch planner:="${scenario}_${global}_${local}_run${i}" goal_x:=$GOAL_X goal_y:=$GOAL_Y summary_file:=$SUMMARY_FILE target_startup_time:=$START_TIME max_timeout:=$MAX_TIMEOUT
                
                echo ">>> Finished Run $i: ${scenario}_${global}_${local}"
                
                # Cleanup
                ./killpro.sh > /dev/null 2>&1
                sleep 2
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
