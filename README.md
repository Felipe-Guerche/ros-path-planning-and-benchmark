# ROS Motion Planning Benchmark Suite

This repository is an **integrated motion planning & benchmarking framework** for ROS Noetic. 

It bridges the gap between algorithmic implementation and performance verification by combining the extensive planner collection of [ros_motion_planning](https://github.com/ai-winter/ros_motion_planning) with the metric collection capabilities of [plannie](https://github.com/lidiaxp/plannie).

## 🚀 Key Features

*   **Diverse Algorithm Suite**: access to various Global Planners (A*, Hybrid A*, RRT, Lazy Theta*, etc.) and Local Planners (DWA, APF, MPC, etc.).
*   **Automated Benchmarking**: A system to run batch simulations (`scripts/run_battery.sh`), cycling through planner configurations and dynamic scenarios.
*   **Performance Metrics**: Automatically captures execution time, path length, CPU usage, and Memory consumption (MB & %) for every run.
*   **Dynamic Environments**: Support for warehouse environments with pedestrian simulation.

## 🏗️ Architecture & Credits

This project serves as an integration layer between two excellent open-source projects:

1.  **[ai-winter/ros_motion_planning](https://github.com/ai-winter/ros_motion_planning)**: Provided the foundational ROS navigation stack, the `sim_env` (Gazebo worlds), and the core C++ planner plugins.
2.  **[lidiaxp/plannie](https://github.com/lidiaxp/plannie)**: Provided the `benchmark_manager.py` logic for tracking system resources and recording trajectory data during execution. 

### 🔧 Modifications & Adaptation
While `plannie` was originally designed for **UAVs (Unmanned Aerial Vehicles)** and real-world flight missions, we have adapted its benchmarking logic for **UGVs (Unmanned Ground Vehicles)** / wheeled robots.

**Key Changes from Original Repositories**:
*   **Orchestration**: Created `scripts/run_battery.sh` to automate hundreds of sequential runs without human intervention.
*   **Process Monitoring**: Updated `benchmark_manager.py` to specifically track `move_base` process resources instead of system-wide averages, providing more granular CPU/Memory data.
*   **Metric Expansion**: Added support for **Megabytes (MB)** memory tracking (not just %) and Total System RAM context.
*   **World & Robots**: Standardized on a Warehouse environment with dynamic pedestrians, replacing the original drone scenarios.

## 📂 Project Structure
```text
.
├── scripts/
│   ├── run_battery.sh     # Main benchmark automation script
│   └── ...
├── src/
│   ├── plannie-main/      # Plannie Core Modules (Metric Collection)
│   └── ros_motion_planning/ # Simulation env & Planners
└── requirements.txt       # Python dependencies
```

## 📦 Installation

**System Requirements**:
*   Ubuntu 20.04 LTS
*   ROS Noetic

### 1. Install Dependencies
```bash
# Install core ROS Navigation stack
sudo apt install ros-noetic-desktop-full
sudo apt install ros-noetic-navigation ros-noetic-teb-local-planner

# Install analysis dependencies
pip3 install -r requirements.txt
```

### 2. Build the Workspace
Clone this repository into your catkin workspace `src` folder:
```bash
cd ~/catkin_ws/src
git clone <THIS_REPO_URL>
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

## 🛠️ Usage

### 🧪 Running the Benchmark Battery (Recommended)
To run a full scientific evaluation (cycling through planners and scenarios):

1.  **Configure the Test**:
    Edit `scripts/run_battery.sh` to select your desired planners:
    ```bash
    GLOBAL_PLANNERS=("astar" "rrt" "hybrid_astar")
    LOCAL_PLANNERS=("dwa" "apf")
    SCENARIOS=("static" "dynamic")
    NUM_RUNS="30"  # 30 runs for statistical relevance
    ```

2.  **Execute**:
    ```bash
    cd scripts
    chmod +x run_battery.sh killpro.sh
    ./run_battery.sh
    ```

    > **Note**: This will automatically launch Gazebo, run the navigation task, kill the processes, and repeat.

3.  **View Results**:
    Results are saved in `src/plannie-main/results/`.
    *   **Individual Runs**: `benchmark_<scenario>_<planners>_runX.txt` (detailed trajectory & resource log).
    *   **Summary**: `battery_summary_<timestamp>.csv` (Aggregated table with Success/Fail, Time, Distance, CPU, Memory).

### 🎮 Running a Single Simulation
If you just want to test one configuration manually:

```bash
cd scripts
./main.sh
```
*   Use **RViz** (2D Nav Goal) to send a goal manully.
*   *Note: Manual runs may not log metrics unless the benchmark node is explicitly launched.*

## ⚙️ Configuration

*   **Robot & World**: Modify `src/user_config/user_config.yaml` to change the robot model (e.g., `turtlebot3_waffle`) or the map (e.g., `warehouse`).
*   **Pedestrians**: To enable/disable dynamic obstacles, toggle the `pedestrians` plugin line in `user_config.yaml` (handled automatically by `run_battery.sh`).

## 📝 Citation
If you use this benchmark in your research, please cite the original authors who provided the foundation for this work:

1. **Plannie Benchmark**: [Rocha, L. et al. (ICUAS 2022)](https://ieeexplore.ieee.org/document/9836102)
2. **ROS Motion Planning**: [GitHub Repository](https://github.com/ai-winter/ros_motion_planning)

*The citation for this specific adaptation/paper will be added upon publication.*

## 📞 Contact
For questions regarding the adaptation for Ground Vehicles or the Metric extensions, please open an Issue in this repository.