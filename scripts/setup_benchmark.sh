#!/bin/bash
set -e

echo "=========================================="
echo "    ROS Benchmark Setup & Dependency Installer "
echo "=========================================="

echo "[1/4] Installing System Dependencies (apt)..."
sudo apt-get update
sudo apt-get install -y \
    ros-noetic-desktop-full \
    ros-noetic-navigation \
    ros-noetic-teb-local-planner \
    python3-pip \
    python-is-python3

echo ""
echo "[2/4] Installing Python Dependencies (pip)..."
# Using pip3 directly as requested
pip3 install -r ../requirements.txt

# Additional pip dependencies explicit in the dockerfile but might be needed locally
pip3 install setuptools catkin-tools conan==1.59.0

echo ""
echo "[3/4] Setting Execution Permissions..."
chmod +x scripts/*.sh

echo ""
echo "[4/4] Building Catkin Workspace..."
cd ..
if [ ! -d "devel" ]; then
    echo "Initializing workspace and building..."
    catkin_make
else
    echo "Workspace already built. Skipping catkin_make."
    echo "If you need to rebuild, run 'catkin_make' from the repository root."
fi

echo "=========================================="
echo " Setup Complete! "
echo " You can now run the benchmark using: "
echo " cd scripts && ./run_benchmark.sh "
echo "=========================================="
