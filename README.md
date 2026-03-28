# ROS Motion Planning Benchmark Suite

This repository is an **integrated motion planning & benchmarking framework** for ROS Noetic. 

It bridges the gap between algorithmic implementation and performance verification by combining the extensive planner collection of [ros_motion_planning](https://github.com/ai-winter/ros_motion_planning) with the metric collection capabilities of [plannie](https://github.com/lidiaxp/plannie).

## 📊 Benchmark Results & Performance

The following results were obtained using the **Robust Research** pipeline with `MASTER_SEED=15257`. The analysis focuses on the **Baseline Case** (Inflation=0.5, PedCount=3) to provide a statistically significant comparison across 12 planner configurations.

### 1. Overall Success Rate
The following table summarizes the performance of the top planner combinations in the **Nominal Scenario** (Inflation=0.7, Dynamic Obstacles).

| Planner Suite | Success Rate | Time (s) | Distance (m) | Smoothness (rad) |
| :--- | :---: | :---: | :---: | :---: |
| **A* + APF** | **100.0%** | 34.6 | 15.9 | 3.9 |
| **Dijkstra + APF** | 97.5% | 33.7 | 15.8 | 4.1 |
| **RRT + APF** | 80.0% | 45.1 | 18.2 | 4.8 |
| **D* Lite + APF** | 77.5% | 31.1 | 15.5 | 4.2 |
| **Lazy Theta* + APF**| **75.0%** | 31.8 | 15.4 | 3.8 |
| **Hybrid A* + APF** | 56.3% | 40.2 | 16.3 | 4.5 |

![Success Rate](assets/benchmark/success_rate.png)

*   **Grid-based Dominance:** A* and Dijkstra remain the most reliable planners in dynamic warehouse environments.
-   **Statistical Rigor:** All metrics are derived from the aggregated **Seed 15257** master dataset (1,920 runs), providing high confidence intervals.
-   **Technical Transparency:** Data structures and implementation details are documented in [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md).

### 2. Temporal Efficiency & Smoothness
Computation time and path quality exhibit clear trade-offs between deterministic and sampling-based methods.

![Computation Time](assets/benchmark/Times.png)
![Smoothness](assets/benchmark/Smoothnessrad.png)

*   **Speed Leader:** **D* Lite** and **Lazy Theta*** achieved the fastest mean computation times, though at a significant cost to success rate in dynamic zones.
*   **Path Quality:** **A* + APF** maintains the most consistent balance between reachability and trajectory smoothness.

### 3. Resource Usage (Memory & CPU)
![Memory Usage](assets/benchmark/MemoryMiB.png)

| Metric | Leader | Empirical Observation |
| :--- | :--- | :--- |
| **CPU Usage** | A* + APF | Lowest CPU footprint (**~9.4%**) due to efficient grid search and reactive local avoidance. |
| **Memory** | Hybrid A* | Competitive memory footprint (**~41 MiB**) despite 3D $(x,y,\theta)$ search space. |
| **Reliability**| A* + APF | Only configuration maintaining significant success across the full spectrum of pedestrian densities ($N=3,5,10$). |

---
*For the complete statistical analysis and failure case logs, refer to [results/seed_15257/merges/final_summary_seed_15257.csv](results/seed_15257/merges/final_summary_seed_15257.csv).*

## 🚀 Key Features

*   **Diverse Algorithm Suite**: access to various Global Planners (A*, Hybrid A*, RRT, Lazy Theta*, etc.) and Local Planners (DWA, APF, MPC, etc.).
*   **Automated Benchmarking**: A system to run batch simulations (`scripts/benchmark_worker.sh`), cycling through planner configurations and dynamic scenarios.
*   **Performance Metrics**: Automatically captures execution time, path length, CPU usage, and Memory consumption (MB & %) for every run.
*   **Scientific Reproducibility**: Seed-based reproducibility with per-run logging and configuration auto-backup.
*   **Publication Pipeline**: Includes `scripts/prepare_paper_results.py` for automated **LaTeX Table** snippets and 300 DPI figure generation (Success Rate, Boxplots, Heatmaps).
*   **Automated Data Analysis**: Built-in statistical analysis (Kruskal-Wallis, Mann-Whitney U) and failure case reporting via `analyze_results.py`.
*   **Real-time Monitoring**: Track simulation progress and CSV health via `scripts/monitor.sh`.
*   **Safe Execution**: Automated process cleanup (`cleanup_processes.sh`) and headless rendering for resource-constrained environments.
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

## 📋 Project Structure
```text
.
├── scripts/
│   ├── benchmark_worker.sh     # Main benchmark automation script
│   └── ...
├── src/
│   ├── plannie-main/      # Plannie Core Modules (Metric Collection)
│   └── ros_motion_planning/ # Simulation env & Planners
|── results/               # Persistent storage for benchmark data
└── requirements.txt       # Python dependencies
```

## 📦 Installation

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

1.  **Execute the Orchestrator**:
    ```bash
    cd scripts
    ./run_benchmark.sh [options]
    ```
    
    **Available Options**:
    - `--new-seed`: Generate a new random Master Seed.
    - `--resume`: Auto-detect and resume the latest session for the current seed.
    - `--workers N`: Specify parallel containers (default: 6).

2.  **Monitor Progress**:
    While the benchmark is running, you can monitor the CSV growth in real-time:
    ```bash
    ./scripts/monitor.sh
    ```

3.  **View Results Analysis**:
    Results are saved in `results/run_<timestamp>_seed_<seed>/`. 
    The folder includes publication-ready plots in the `figures/` subdirectory.

### 🎮 Running a Single Simulation
If you just want to test one configuration manually:

```bash
cd scripts
./launch_simulator.sh
```
*   Use **RViz** (2D Nav Goal) to send a goal manually.
*   *Note: Manual runs may not log metrics unless the benchmark node is explicitly launched.*

## ⚙️ Configuration

*   **Robot & World**: Modify `src/user_config/user_config.yaml` to change the robot model (e.g., `turtlebot3_waffle`) or the map (e.g., `warehouse`).
*   **Pedestrians**: To enable/disable dynamic obstacles, toggle the `pedestrians` plugin line in `user_config.yaml` (handled automatically by `benchmark_worker.sh`).

## 📝 Citation
If you use this benchmark in your research, please cite the original authors who provided the foundation for this work:

1. **Plannie Benchmark**: [Rocha, L. et al. (ICUAS 2022)](https://ieeexplore.ieee.org/document/9836102)
2. **ROS Motion Planning**: [GitHub Repository](https://github.com/ai-winter/ros_motion_planning)

*The citation for this specific adaptation/paper will be added upon publication.*

## 📬 Contact
For questions regarding the adaptation for Ground Vehicles or the Metric extensions, please open an Issue in this repository.