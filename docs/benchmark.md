# Parallel Benchmark System

End-to-end automated benchmark for path planning algorithms with Docker isolation, randomized scenarios, and statistical analysis.

## Architecture

```
parallel_runner.sh          ← Run this from project root (Ubuntu)
├── docker build             (one-time)
├── docker run [Worker 0]    ── docker_entrypoint.sh → run_battery.sh
├── docker run [Worker 1]    ── docker_entrypoint.sh → run_battery.sh
├── docker run [Worker 2]    ── docker_entrypoint.sh → run_battery.sh
│                                ├── generate_random_poses.py    (safe start/goal)
│                                ├── generate_pedestrian_config.py (N peds)
│                                └── benchmark_manager.py         (collect metrics)
└── analyze_results.py       (merge + stats + plots)
```

Each Docker container runs **one planner combination** in isolation with fixed CPU/RAM.

---

## Quick Start

### 1. Prerequisites

- Ubuntu 20.04+ with Docker installed
- Ryzen 7 5700 (16 threads) / 32GB RAM (or adjust config)

### 2. Run Full Benchmark (Parallel)

```bash
cd ros-path-planning-and-benchmark
chmod +x scripts/parallel_runner.sh
./scripts/parallel_runner.sh
```

This will:
1. Build the Docker image (~10 min first time)
2. Generate all planner combination jobs (6 global × 2 local × 2 scenarios = 24 base jobs)
3. Dispatch 3 workers in parallel (each gets 4 CPUs + 8GB RAM)
4. Aggregate results and generate plots

### 3. Smoke Test (Quick Validation)

Edit `scripts/parallel_runner.sh`:
```bash
MAX_WORKERS=1
NUM_RUNS=2
GLOBAL_PLANNERS=("astar")
LOCAL_PLANNERS=("dwa")
SCENARIOS=("static")
```

Then run to verify everything works in ~10 minutes.

### 4. Run Without Docker (Legacy Mode)

```bash
cd scripts
./run_battery.sh
```

Runs the full matrix sequentially on your host. Set `BENCHMARK_HEADLESS=1` to disable GUI.

### 5. Analyze Results Separately

```bash
# Merge CSVs + statistical tests
python scripts/analyze_results.py --results_dir ./results

# Also generate plots
python scripts/analyze_results.py --results_dir ./results --plot --plot_dir ./results/figures

# Single file
python scripts/analyze_results.py --summary_file ./results/battery_summary_20260310.csv --plot
```

---

## Configuration Reference

### `scripts/parallel_runner.sh` — Orchestrator

| Variable | Default | Description |
|---|---|---|
| `MAX_WORKERS` | 3 | Parallel Docker containers |
| `CPUS_PER_WORKER` | 4.0 | CPU threads per container |
| `RAM_PER_WORKER` | 8g | RAM limit per container |
| `NUM_RUNS` | 30 | Repetitions per planner combo |
| `SCENARIOS` | static, dynamic | Test scenarios |
| `GLOBAL_PLANNERS` | astar, hybrid_astar, dijkstra, lazy_theta_star, dstar_lite, rrt | Global planners |
| `LOCAL_PLANNERS` | dwa, apf | Local planners |
| `SWEEP_rrt` | 10.0:20.0:30.0 | RRT step size sweep (colon-separated) |

### `scripts/run_battery.sh` — Battery Runner

| Variable | Default | Description |
|---|---|---|
| `PED_COUNTS` | 3, 5, 10 | Pedestrian counts for dynamic scenario |
| `INFLATION_SWEEPS` | 0.3, 0.5, 0.7 | Costmap inflation factor sweep |
| `NUM_RUNS` | 30 | Runs per configuration |
| `MAX_TIMEOUT` | 180 | Max seconds per navigation attempt |

### `scripts/generate_random_poses.py` — Safe Pose Sampling

```bash
python generate_random_poses.py <map.yaml> [options]
```

| Argument | Default | Description |
|---|---|---|
| `--safety_radius` | 0.5 | Min distance from walls (meters) |
| `--min_dist` | 5.0 | Min distance between start and goal (meters) |
| `--seed` | random | Random seed for reproducibility |
| `--ped_config` | none | Path to pedestrian_config.yaml to exclude ped zones |
| `--ped_exclusion_radius` | 1.5 | Exclusion radius around each pedestrian (meters) |

**Safety guarantees:**
- 3-layer wall protection: occupancy threshold → binary erosion → connected component
- Pedestrian exclusion zones (1.5m radius)
- Start and goal in same navigable region
- Minimum 5m distance between start and goal
- Seed logged to stderr for reproducibility

### `scripts/generate_pedestrian_config.py` — Dynamic Pedestrian Config

```bash
python generate_pedestrian_config.py <map.yaml> --num_peds 5 --robot_x 1.0 --robot_y 2.0 --output ped_config.yaml
```

| Argument | Default | Description |
|---|---|---|
| `--num_peds` | 3 | Number of pedestrians |
| `--seed` | random | Random seed |
| `--robot_x/y` | none | Robot position to avoid |
| `--output` | stdout | Output YAML path |

**Safety:** All pedestrians spawn in free space, ≥2m from each other and robot.

### Headless Mode

Set `BENCHMARK_HEADLESS=1` to disable Gazebo GUI and RViz:
```bash
export BENCHMARK_HEADLESS=1
./scripts/run_battery.sh
```

This is set automatically inside Docker containers.

---

## Output Format

### CSV Columns

Each run produces one row in `battery_summary_*.csv`:

```
Scenario, GlobalPlanner, LocalPlanner, SweepParam, InflationFactor, PedCount,
Status, Time(s), Distance(m), Smoothness(rad), CPU(%), Memory(%), Memory(MiB), TotalRAM(GiB)
```

### Metrics Explained

| Metric | Description |
|---|---|
| `Time(s)` | Seconds from goal publication to arrival (or timeout) |
| `Distance(m)` | Total odometry-integrated path length |
| `Smoothness(rad)` | Sum of absolute angle changes Σ\|Δθ\| (lower = smoother) |
| `CPU(%)` | Average CPU usage of the `move_base` process |
| `Memory(MiB)` | Peak RSS memory of the `move_base` process |
| `Status` | SUCCESS or FAILURE (timeout / no path found) |

### Statistical Analysis Output

`analyze_results.py` produces:
- **Success rates** per planner with 95% Wilson confidence intervals
- **Descriptive statistics** (mean, std, min, max, quartiles) per metric
- **Bootstrap 95% CI** for metric means
- **Shapiro-Wilk** normality test per group
- **Kruskal-Wallis** omnibus test (H-test for overall difference)
- **Pairwise Mann-Whitney U** post-hoc tests (which planners differ)

### Generated Plots (`--plot`)

| Plot | File | Description |
|---|---|---|
| Boxplots | `boxplot_Times.png`, etc. | Distribution per planner per metric |
| Violin | `violin_time.png` | Time distribution shape |
| Success Rate | `success_rate.png` | Bar chart with 95% Wilson CI error bars |

All plots saved at 300 DPI, suitable for paper submission.

---

## Docker Details

### Image Build

```bash
docker build -t ros-benchmark -f docker/noetic/Dockerfile .
```

### Manual Single Container

```bash
docker run --rm \
  --cpus=4.0 --memory=8g \
  -e GLOBAL_PLANNER=astar \
  -e LOCAL_PLANNER=dwa \
  -e SCENARIO=static \
  -e NUM_RUNS=5 \
  -v $(pwd)/results:/project/src/plannie-main/results \
  ros-benchmark
```

### Multi-Instance Isolation

Each container gets:
- Unique `ROS_MASTER_PORT` (11311 + worker_id)
- Unique `GAZEBO_MASTER_PORT` (11345 + worker_id)
- Virtual framebuffer (`Xvfb :99`) for headless rendering
- `BENCHMARK_HEADLESS=1` (no GUI, no RViz)

---

## Scripts Reference

| Script | Purpose |
|---|---|
| `parallel_runner.sh` | **Main entry point**: Docker orchestrator |
| `run_battery.sh` | Test battery (Docker single-planner or legacy full matrix) |
| `generate_random_poses.py` | Safe start/goal sampling from occupancy grid |
| `generate_pedestrian_config.py` | Generate N-pedestrian YAML configs |
| `analyze_results.py` | Merge CSVs + statistical tests + plots |
| `killpro.sh` | Kill ROS/Gazebo processes between runs |
| `main.sh` | Launch ROS simulation stack |
| `build.sh` | Build the catkin workspace |

---

## Hardware Recommendations

| Setup | Workers | CPUs/Worker | RAM/Worker | Total |
|---|---|---|---|---|
| Ryzen 7 5700 / 32GB | 3 | 4 | 8g | 12 CPU + 24GB |
| Ryzen 9 / 64GB | 6 | 4 | 8g | 24 CPU + 48GB |
| Server (96 cores) | 20 | 4 | 8g | 80 CPU + 160GB |

Reserve 2+ cores and 4GB+ for the host OS.
