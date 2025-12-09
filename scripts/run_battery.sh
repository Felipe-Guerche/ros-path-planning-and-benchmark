#!/bin/bash

# Suppress Warnings
export ROS_PYTHON_WARNINGS="ignore"
export GAZEBO_ROS_CMD_WARNINGS="0"
export DISABLE_ROS1_EOL_WARNINGS="1" # Correct variable from error message

# Configuration
GLOBAL_PLANNERS=("astar" "hybrid_astar" "dijkstra" "lazy_theta_star" "dstar_lite" "rrt")
LOCAL_PLANNERS=("dwa" "apf")
SCENARIOS=("static" "dynamic")
GOAL_X="8.5"
GOAL_Y="-4.0"
CONFIG_FILE="../src/user_config/user_config.yaml"
SUMMARY_FILE="$(pwd)/../src/plannie-main/results/battery_summary_$(date +%Y%m%d_%H%M%S).csv"

echo "=========================================="
echo "      Benchmark Battery Suite"
echo "=========================================="
echo "Global Planners: ${GLOBAL_PLANNERS[*]}"
echo "Local Planners: ${LOCAL_PLANNERS[*]}"
echo "Scenarios: ${SCENARIOS[*]}"
echo "Goal: ($GOAL_X, $GOAL_Y)"
echo "Summary File: $SUMMARY_FILE"
echo "=========================================="

# Create summary header
if [ ! -f "$SUMMARY_FILE" ]; then
    echo "Scenario,GlobalPlanner,LocalPlanner,Status,Time(s),Distance(m),CPU(%),Memory(%)" > "$SUMMARY_FILE"
fi

for scenario in "${SCENARIOS[@]}"; do
    for global in "${GLOBAL_PLANNERS[@]}"; do
        for local in "${LOCAL_PLANNERS[@]}"; do
            echo ""
            echo ">>> Starting Benchmark: Scenario=$scenario | Global=$global | Local=$local"
            
            # 1. Update Configuration
            echo "[1/5] Updating user_config.yaml..."
            sed -i "s/robot1_global_planner: \".*\"/robot1_global_planner: \"$global\"/" "$CONFIG_FILE"
            sed -i "s/robot1_local_planner: \".*\"/robot1_local_planner: \"$local\"/" "$CONFIG_FILE"
            
            if [ "$scenario" == "dynamic" ]; then
                # Enable pedestrians (uncomment)
                # Matches valid indentation, optional #, then pedestrians:... key
                sed -i 's/.*pedestrians: "pedestrian_config.yaml"/  pedestrians: "pedestrian_config.yaml"/' "$CONFIG_FILE"
            else
                # Disable pedestrians (comment)
                sed -i 's/.*pedestrians: "pedestrian_config.yaml"/  # pedestrians: "pedestrian_config.yaml"/' "$CONFIG_FILE"
            fi
            
            # 2. Cleanup
            echo "[2/5] Cleaning process..."
            ./killpro.sh > /dev/null 2>&1
            sleep 5
            
            # 3. Start Simulation
            echo "[3/5] Starting Simulation..."
            ./main.sh > /dev/null 2>&1 &
            SIM_PID=$!
            
            # 4. Wait for Readiness
            echo "[4/5] Waiting for System..."
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
            echo "[5/5] Executing Benchmark Test..."
            roslaunch plannie benchmark.launch planner:="${scenario}_${global}_${local}" goal_x:=$GOAL_X goal_y:=$GOAL_Y summary_file:=$SUMMARY_FILE
            
            echo ">>> Finished: ${scenario}_${global}_${local}"
            echo "------------------------------------------"
            
            # Cleanup
            ./killpro.sh > /dev/null 2>&1
            sleep 2
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
