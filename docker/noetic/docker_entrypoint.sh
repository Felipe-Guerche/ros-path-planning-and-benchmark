#!/bin/bash
set -e

# =============================================================================
# Docker Entrypoint for Benchmark Workers
# Receives configuration via environment variables and runs one planner combo.
# =============================================================================

# Source ROS
source /opt/ros/noetic/setup.bash
source /project/devel/setup.bash 2>/dev/null || true

# ---- Environment Variables (set by parallel_runner.sh) ----
# WORKER_ID          - Unique worker identifier (e.g., 0, 1, 2)
# GLOBAL_PLANNER     - Global planner name (e.g., "astar")
# LOCAL_PLANNER      - Local planner name (e.g., "dwa")
# SCENARIO           - "static" or "dynamic"
# NUM_RUNS           - Number of repetitions (e.g., 30)
# SWEEP_VALUES       - Colon-separated sweep values (e.g., "10.0:20.0:30.0") or "default"
# ROS_MASTER_PORT    - Port for roscore (e.g., 11311)
# GAZEBO_MASTER_PORT - Port for gzserver (e.g., 11345)

WORKER_ID="${WORKER_ID:-0}"
GLOBAL_PLANNER="${GLOBAL_PLANNER:-astar}"
LOCAL_PLANNER="${LOCAL_PLANNER:-dwa}"
SCENARIO="${SCENARIO:-static}"
NUM_RUNS="${NUM_RUNS:-30}"
SWEEP_VALUES="${SWEEP_VALUES:-default}"
ROS_MASTER_PORT="${ROS_MASTER_PORT:-11311}"
GAZEBO_MASTER_PORT="${GAZEBO_MASTER_PORT:-11345}"

# Set ROS/Gazebo isolation ports
export ROS_MASTER_URI="http://localhost:${ROS_MASTER_PORT}"
export GAZEBO_MASTER_URI="http://localhost:${GAZEBO_MASTER_PORT}"

# Force headless mode inside Docker
export BENCHMARK_HEADLESS=1

echo "============================================="
echo "  Benchmark Worker #${WORKER_ID}"
echo "============================================="
echo "  Global Planner : ${GLOBAL_PLANNER}"
echo "  Local Planner  : ${LOCAL_PLANNER}"
echo "  Scenario       : ${SCENARIO}"
echo "  Runs           : ${NUM_RUNS}"
echo "  Sweep Values   : ${SWEEP_VALUES}"
echo "  ROS Master     : ${ROS_MASTER_URI}"
echo "  Gazebo Master  : ${GAZEBO_MASTER_URI}"
echo "============================================="

# Export single-planner mode env vars for benchmark_worker.sh
export SINGLE_GLOBAL_PLANNER="${GLOBAL_PLANNER}"
export SINGLE_LOCAL_PLANNER="${LOCAL_PLANNER}"
export SINGLE_SCENARIO="${SCENARIO}"
export SINGLE_NUM_RUNS="${NUM_RUNS}"
export SINGLE_SWEEP_VALUES="${SWEEP_VALUES}"

# Support Conan external dependencies for Pluginlib (libglog.so, etc)
echo "Looking for Conan dependencies in /root/.conan/data..."
CONAN_LIB_DIRS=$(find /root/.conan/data/ -type d -name "lib" 2>/dev/null || true)
CONAN_PATHS=""
for dir in $CONAN_LIB_DIRS; do
  CONAN_PATHS="${dir}:${CONAN_PATHS}"
done
export LD_LIBRARY_PATH="${CONAN_PATHS}${LD_LIBRARY_PATH}"

# Start virtual framebuffer for headless Gazebo
Xvfb :99 -screen 0 1024x768x16 &
export DISPLAY=:99
sleep 1

# Run the battery
cd /project/scripts
exec ./benchmark_worker.sh
