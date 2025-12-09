#!/bin/bash

# Suppress Warnings
export ROS_PYTHON_WARNINGS="ignore"
export GAZEBO_ROS_CMD_WARNINGS="0"
export DISABLE_ROS1_EOL_WARNINGS="1" # Correct variable from error message

# Configuration
PLANNERS=("astar" "hybrid_astar" "dijkstra" "lazy_theta_star" "dstar_lite" "rrt")
GOAL_X="8.5"
GOAL_Y="-4.0"
CONFIG_FILE="../src/user_config/user_config.yaml"
SUMMARY_FILE="$(pwd)/../src/plannie-main/results/battery_summary_$(date +%Y%m%d_%H%M%S).csv"

echo "=========================================="
echo "      Benchmark Battery Suite"
echo "=========================================="
echo "Planners: ${PLANNERS[*]}"
echo "Goal: ($GOAL_X, $GOAL_Y)"
echo "Summary File: $SUMMARY_FILE"
echo "=========================================="

for planner in "${PLANNERS[@]}"; do
    echo ""
    echo ">>> Starting Benchmark for: $planner"
    
    # 1. Update Configuration
    echo "[1/5] Updating user_config.yaml..."
    # Use sed to replace the planner line: '    robot1_global_planner: "value"'
    # We match the indentation and key carefully
    sed -i "s/robot1_global_planner: \".*\"/robot1_global_planner: \"$planner\"/" "$CONFIG_FILE"
    
    # 2. Cleanup
    echo "[2/5] Cleaning process..."
    ./killpro.sh > /dev/null 2>&1
    sleep 5
    
    # 3. Start Simulation
    # Note: main.sh reads the config we just modified
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
             # Check if move_base action server is registered
            if rostopic list | grep -q "/move_base/status"; then
                READY=true
                break
            fi
        fi
        
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_WAIT))
        
        if [ $ELAPSED -gt $TIMEOUT ]; then
            echo "Timeout waiting for simulation (Planner: $planner)!"
            ./killpro.sh
            exit 1
        fi
        sleep 2
    done
    
    echo "System Ready. Resetting AMCL..."
    rostopic pub -1 /initialpose geometry_msgs/PoseWithCovarianceStamped "{header: {frame_id: 'map'}, pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}}" > /dev/null 2>&1
    sleep 5
    
    # 5. Run Benchmark
    echo "[5/5] Executing Benchmark Test..."
    roslaunch plannie benchmark.launch planner:=$planner goal_x:=$GOAL_X goal_y:=$GOAL_Y summary_file:=$SUMMARY_FILE
    
    echo ">>> Finished: $planner"
    echo "------------------------------------------"
    
    # Ensure cleanup before next loop
    ./killpro.sh > /dev/null 2>&1
    sleep 2
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
