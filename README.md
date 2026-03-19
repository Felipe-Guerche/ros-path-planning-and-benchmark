# ROS Motion Planning Benchmark Suite

This repository is an **integrated motion planning & benchmarking framework** for ROS Noetic. 

It bridges the gap between algorithmic implementation and performance verification by combining the extensive planner collection of [ros_motion_planning](https://github.com/ai-winter/ros_motion_planning) with the metric collection capabilities of [plannie](https://github.com/lidiaxp/plannie).

## 📊 Benchmark Results & Performance

The following results were obtained using the **Robust Research** pipeline with `MASTER_SEED=15257`. The analysis focuses on the **Nominal Case** (Inflation=0.5, PedCount=5) to ensure a balanced comparison across all planner architectures.

### 1. Overall Success Rate
A* combined with the Artificial Potential Field (APF) local planner demonstrated the highest overall success rate (74.3%), followed closely by Dijkstra-APF (70.1%).

![Success Rate](results/seed_15257/figures/tier1_article/success_rate.png)

*   **Grid-based Planners (A*, Dijkstra):** Showed superior reliability in nominal conditions, effectively navigating traditional static and moderately dynamic scenarios.
*   **Sampling-based Planners (RRT):** Exhibited lower success rates (~57%) but maintained a more consistent performance in extremely dense maps where grid search complexity peaks.
*   **Kinematic Planners (Hybrid A*):** Provided smooth, feasible paths (46-52% success) but faced challenges in high-frequency dynamic obstacle avoidance due to higher computational overhead.

### 2. Temporal Efficiency
Computation time varies significantly between deterministic and stochastic approaches.

![Computation Time](results/seed_15257/figures/tier1_article/Times.png)

*   **Observation:** While A* and Dijkstra are faster to reach a solution, RRT variants show a wider spread in computation time, reflecting their stochastic nature.
*   **Trade-off:** Planners that prioritize path smoothness (like Hybrid A*) generally require more computation time per cycle compared to raw grid search.

### 3. Metric Distribution (Memory & Distance)
| Metric | Leader | Observation |
| :--- | :--- | :--- |
| **Memory** | A*-DWA | Deterministic planners maintain a lower and more predictable memory footprint. |
| **Distance** | Dijkstra | Grid-based optimal search consistently produces shorter paths compared to RRT-based exploration. |

---
*For the complete statistical analysis, including parameter sensitivity (facet grids) and failure case logs, refer to the [results session folder](results/seed_15257/).*

## 🚀 Key Features

*   **Diverse Algorithm Suite**: access to various Global Planners (A*, Hybrid A*, RRT, Lazy Theta*, etc.) and Local Planners (DWA, APF, MPC, etc.).
*   **Automated Benchmarking**: A system to run batch simulations (`scripts/benchmark_worker.sh`), cycling through planner configurations and dynamic scenarios.
*   **Performance Metrics**: Automatically captures execution time, path length, CPU usage, and Memory consumption (MB & %) for every run.
*   **Scientific Reproducibility**: Seed-based reproducibility with per-run logging and configuration auto-backup.
*   **Automated Data Analysis**: Built-in statistical analysis (Kruskal-Wallis, Mann-Whitney U) and failure case reporting.
*   **Dynamic Environments**: Support for warehouse environments with pedestrian simulation.

## 🏗️ Architecture & Credits

This project serves as an integration layer between two excellent open-source projects:

1.  **[ai-winter/ros_motion_planning](https://github.com/ai-winter/ros_motion_planning)**: Provided the foundational ROS navigation stack, the `sim_env` (Gazebo worlds), and the core C++ planner plugins.
2.  **[lidiaxp/plannie](https://github.com/lidiaxp/plannie)**: Provided the `benchmark_manager.py` logic for tracking system resources and recording trajectory data during execution. 

### 🔧 Modifications & Adaptation
While `plannie` was originally designed for **UAVs (Unmanned Aerial Vehicles)** and real-world flight missions, we have adapted its benchmarking logic for **UGVs (Unmanned Ground Vehicles)** / wheeled robots.

**Key Changes from Original Repositories**:
*   **Orchestration**: Created `scripts/benchmark_worker.sh` to automate hundreds of sequential runs without human intervention.
*   **Process Monitoring**: Updated `benchmark_manager.py` to specifically track `move_base` process resources instead of system-wide averages, providing more granular CPU/Memory data.
*   **Metric Expansion**: Added support for **Megabytes (MB)** memory tracking (not just %) and Total System RAM context.
*   **World & Robots**: Standardized on a Warehouse environment with dynamic pedestrians, replacing the original drone scenarios.

## � Project Structure
```text
.
├── scripts/
│   ├── benchmark_worker.sh     # Main benchmark automation script
│   └── ...
├── src/
│   ├── plannie-main/      # Plannie Core Modules (Metric Collection)
│   └── ros_motion_planning/ # Simulation env & Planners
└── requirements.txt       # Python dependencies
```

## �📦 Installation

**System Requirements**:
*   Ubuntu 20.04 LTS
*   ROS Noetic

### 1. Automated Installation
Clone this repository and run the automated setup script. It will install all required `apt` and `pip` dependencies, set executable permissions, and build the Catkin workspace automatically.

```bash
git clone https://github.com/Felipe-Guerche/ros-path-planning-and-benchmark.git
cd ros-path-planning-and-benchmark
./setup.sh
```

## 🖥️ Testbed Hardware
The benchmark results presented in this work were collected on a high-performance workstation to ensure consistent simulation physics.
*   **CPU**: AMD Ryzen 7 5700X (8 Cores, 16 Threads) @ 3.4GHz
*   **GPU**: AMD Radeon RX 6950 XT
*   **RAM**: 32 GB DDR4
*   **OS**: Ubuntu 20.04 LTS (Kernel 5.15)

## 🛠️ Usage

### 🧪 Running the Benchmark Battery (Recommended)
To run a full scientific evaluation (cycling through planners and scenarios):

1.  **Configure the Test**:
    Edit `scripts/run_benchmark.sh` to select your desired planners:
    ```bash
    GLOBAL_PLANNERS=("astar" "rrt" "hybrid_astar")
    LOCAL_PLANNERS=("dwa" "apf")
    SCENARIOS=("static" "dynamic")
    NUM_RUNS="30"  # 30 runs for statistical relevance
    ```

2.  **Execute**:
    ```bash
    cd scripts
    ./run_benchmark.sh [options]
    ```
    
    **Available Options**:
    - `--new-seed`: Force the generation of a new random Master Seed.
    - `--resume`: Search for and resume the latest existing session for the current seed.

    > **Note**: This will automatically spin up Docker containers, launch Gazebo headless, run the navigation task, kill the processes, and aggregate the results.

3.  **View Results**:
    Results are saved in `results/run_<timestamp>_seed_<seed>/`.
    - **Backups**: Automatically saves copies of `user_config.yaml`, `system_config.pb.txt`, and `seed.md`.
    - **Individual Runs**: `benchmark_<scenario>_<planners>_runX.txt` (detailed trajectory & resource log).
    - **Summary**: `battery_summary_*.csv` (Aggregated table with Success/Fail, Time, Distance, CPU, Memory).
    - **Analysis**: `failure_report.txt` (List of problematic seeds per planner).
    - **Figures**: Publication-ready plots in the `figures/` subdirectory.

### 🎮 Running a Single Simulation
If you just want to test one configuration manually:

```bash
cd scripts
./launch_simulator.sh
```
*   Use **RViz** (2D Nav Goal) to send a goal manully.
*   *Note: Manual runs may not log metrics unless the benchmark node is explicitly launched.*

## ⚙️ Configuration

*   **Robot & World**: Modify `src/user_config/user_config.yaml` to change the robot model (e.g., `turtlebot3_waffle`) or the map (e.g., `warehouse`).
*   **Pedestrians**: To enable/disable dynamic obstacles, toggle the `pedestrians` plugin line in `user_config.yaml` (handled automatically by `benchmark_worker.sh`).

## 📝 Citation
If you use this benchmark in your research, please cite the original authors who provided the foundation for this work:

1. **Plannie Benchmark**: [Rocha, L. et al. (ICUAS 2022)](https://ieeexplore.ieee.org/document/9836102)
2. **ROS Motion Planning**: [GitHub Repository](https://github.com/ai-winter/ros_motion_planning)

*The citation for this specific adaptation/paper will be added upon publication.*

## �� Contact
For questions regarding the adaptation for Ground Vehicles or the Metric extensions, please open an Issue in this repository.