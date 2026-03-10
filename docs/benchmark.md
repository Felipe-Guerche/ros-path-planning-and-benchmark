# Parallel Benchmark System

This document describes the automated benchmark infrastructure for running path planning evaluations at scale using Docker containers with resource isolation.

## Overview

The benchmark system supports:
- **Randomized test scenarios**: spawn and goal positions are sampled from free space in the occupancy grid map, ensuring the robot never spawns inside obstacles.
- **Parameter sweeping**: automated variation of planner parameters (e.g., RRT `sample_max_distance`) across runs.
- **Parallel execution**: multiple Docker containers run simultaneously, each pinned to fixed CPU/RAM quotas for reproducibility.
- **Statistical analysis**: non-parametric tests (Shapiro-Wilk, Kruskal-Wallis, Mann-Whitney U) for rigorous comparison of planners.

## Architecture

```
parallel_runner.sh (orchestrator)
├── docker build (once)
├── docker run [Worker 0] ── run_battery.sh (astar+dwa, static)
├── docker run [Worker 1] ── run_battery.sh (rrt+dwa, static)
├── docker run [Worker 2] ── run_battery.sh (theta*+apf, dynamic)
│                               ├── generate_random_poses.py
│                               └── benchmark.launch
└── analyze_results.py (merge CSVs + statistical tests)
```

## Hardware Requirements

| Resource       | Total | OS Reserve | Available | Per Worker (3 workers) |
|----------------|-------|------------|-----------|------------------------|
| CPU Threads    | 16    | 2          | 14        | 4                      |
| RAM (GB)       | 32    | 4          | 28        | 8                      |

> All values are configurable in `scripts/parallel_runner.sh`.

## Quick Start

### 1. Build and Run (Parallel)

```bash
# From the project root:
chmod +x scripts/parallel_runner.sh
./scripts/parallel_runner.sh
```

### 2. Smoke Test (Recommended First)

Edit `scripts/parallel_runner.sh`:
```bash
MAX_WORKERS=2
NUM_RUNS=2
```

Then run to verify everything works before the full battery.

### 3. Analyze Results

```bash
python scripts/analyze_results.py --results_dir ./results
# or for a specific file:
python scripts/analyze_results.py --summary_file ./results/battery_summary_20260310.csv
```

## Configuration Reference

### `scripts/parallel_runner.sh`

| Variable           | Default | Description                                      |
|--------------------|---------|--------------------------------------------------|
| `MAX_WORKERS`      | 3       | Number of parallel Docker containers             |
| `CPUS_PER_WORKER`  | 4.0     | CPU threads allocated per container              |
| `RAM_PER_WORKER`   | 8g      | RAM limit per container                          |
| `NUM_RUNS`         | 30      | Repetitions per planner combination              |
| `SCENARIOS`        | static, dynamic | Test scenarios                           |
| `GLOBAL_PLANNERS`  | astar, hybrid_astar, dijkstra, lazy_theta_star, dstar_lite, rrt | Global planners |
| `LOCAL_PLANNERS`   | dwa, apf | Local planners                                  |
| `SWEEP_rrt`        | 10.0:20.0:30.0 | Parameter sweep values (colon-separated) |

### `scripts/generate_random_poses.py`

```bash
python generate_random_poses.py <path_to_map.yaml> [safety_radius_m] [min_distance_m]
```

| Argument          | Default | Description                                    |
|-------------------|---------|------------------------------------------------|
| `safety_radius_m` | 0.5     | Minimum distance from walls (erosion radius)   |
| `min_distance_m`  | 5.0     | Minimum euclidean distance between start & goal|

### Headless Mode

Set the environment variable `BENCHMARK_HEADLESS=1` to disable Gazebo GUI and RViz. This is done automatically inside Docker containers.

For native (non-Docker) usage:
```bash
export BENCHMARK_HEADLESS=1
./scripts/run_battery.sh
```

## Output

### CSV Format

Each run appends a row to `battery_summary_*.csv`:

```
Scenario,GlobalPlanner,LocalPlanner,SweepParam,StartX,StartY,GoalX,GoalY,Status,Time(s),Distance(m),CPU(%),Memory(%),Memory(MiB),TotalRAM(GiB)
```

### Statistical Analysis Output

`analyze_results.py` produces:
- Descriptive statistics per planner (mean, std, min, max, quartiles)
- Shapiro-Wilk normality test per group
- Kruskal-Wallis omnibus test (overall difference)
- Pairwise Mann-Whitney U post-hoc tests (which planners differ)

## Scripts Reference

| Script                       | Purpose                                          |
|------------------------------|--------------------------------------------------|
| `scripts/parallel_runner.sh` | Orchestrator: builds image, dispatches containers|
| `scripts/run_battery.sh`     | Battery runner (Docker single-planner or legacy)  |
| `scripts/generate_random_poses.py` | Samples valid free-space poses from `.pgm` |
| `scripts/analyze_results.py` | Merges CSVs + non-parametric statistical tests   |
| `scripts/killpro.sh`         | Kills ROS/Gazebo processes between runs          |
