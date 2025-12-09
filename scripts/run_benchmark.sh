#!/bin/bash

# Default Parameters
PLANNER="astar"
GOAL_X="8.5"
GOAL_Y="-4.0"

# Parse Arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --planner)
      PLANNER="$2"
      shift 2
      ;;
    --x)
      GOAL_X="$2"
      shift 2
      ;;
    --y)
      GOAL_Y="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: $0 [--planner NAME] [--x X_COORD] [--y Y_COORD]"
      exit 1
      ;;
  esac
done

echo "=========================================="
echo "Automated Benchmark Script"
echo "Planner: $PLANNER"
echo "Goal: ($GOAL_X, $GOAL_Y)"
echo "=========================================="

# 1. Cleanup
echo "[1/4] Cleaning up previous processes..."
./killpro.sh > /dev/null 2>&1
sleep 5

# 2. Start Simulation
echo "[2/4] Starting Simulation..."
./main.sh > /dev/null 2>&1 &
SIM_PID=$!
echo "Simulation started (PID: $SIM_PID)"

# 3. Wait for Readiness
echo "[3/4] Waiting for Move Base to be ready..."
source ../devel/setup.bash
TIMEOUT=300
START_WAIT=$(date +%s)
READY=false

while true; do
    # Check if we can contact master
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
        echo "Timeout waiting for simulation!"
        ./killpro.sh
        exit 1
    fi
    
    sleep 2
done

echo "System Ready! Resetting AMCL pose to (0,0)..."
rostopic pub -1 /initialpose geometry_msgs/PoseWithCovarianceStamped "{header: {frame_id: 'map'}, pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}}" > /dev/null 2>&1
sleep 5 # Give AMCL time to settle

# 4. Run Benchmark
echo "[4/4] Running Benchmark..."
source ../devel/setup.bash
roslaunch plannie benchmark.launch planner:=$PLANNER goal_x:=$GOAL_X goal_y:=$GOAL_Y

# Cleanup after finish
echo "Benchmark completed."
# Optional: Uncomment to kill simulation after run
# ./killpro.sh
