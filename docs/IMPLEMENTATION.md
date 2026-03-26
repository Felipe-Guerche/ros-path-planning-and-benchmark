# Implementation Details & Data Structures

This document provides technical transparency into the algorithms and infrastructure used in the benchmark, as requested during the peer-review process.

## 1. Path Planning Algorithms

### Hybrid A* (Robot-Centric)
*   **State Space**: 3D search space $(x, y, \theta)$ discretized into a grid.
*   **Motion Model**: Discretized steering angles to ensure kinematic feasibility for ackermann-like or differential drive constrained robots.
*   **Heuristics**:
    1.  **Non-holonomic Without Obstacles**: Pre-calculated Reeds-Shepp or Dubins curve lengths.
    2.  **Holonomic With Obstacles**: 2D Dijkstra/A* distance to the goal considering the static costmap.
*   **Data Structures**:
    *   **Open Set**: Priority Queue (Min-Heap) indexed by $f(n) = g(n) + h(n)$.
    *   **Closed Set**: 3D Hash Map or discretized bit-array for coordinate pruning.

### Lazy Theta*
*   **State Space**: 2D/3D Grid or Octree representation.
*   **Optimization**: Implements Any-Angle path planning. Unlike standard A*, it allows the parent of a node to be any of its predecessors if a direct Line-Of-Sight (LOS) exists.
*   **Lazy Evaluation**: Only performs expensive LOS checks (ray-casting) when a node is being expanded, significantly reducing computation time compared to standard Theta*.
*   **Fallback Logic**: In complex cluttered environments, if a direct path is blocked by dynamic obstacles during execution, the algorithm falls back to a parent-to-child grid traversal to ensure safety.

## 2. Benchmark Infrastructure

### Parallel Orchestration
*   **Mechanism**: Bash-based job dispatcher with semaphore logic.
*   **Isolation**: Each worker runs in a separate Docker container with dedicated CPU (`--cpus`) and Memory (`--memory`) limits.
*   **Port Mapping**: Unique ROS Master and Gazebo ports (starting at 11311 and 11345 respectively) are assigned per worker to prevent cross-container interference.

### Resource Monitoring
*   **CPU/Memory**: Collected via `ps` inside the worker container at 1Hz and averaged over the run duration.
*   **Stability**: Handled via a 2-tier timeout system (ROS-level `max_timeout` and Shell-level `timeout` command) to prevent zombie processes in case of simulation freezes.

## 3. Hardware / Simulation Fidelity
*   **Simulator**: Gazebo 11 with ODE physics engine.
*   **Frequency**: 50Hz control loop frequency.
*   **Data Integrity**: Used a fixed `MASTER_SEED` to ensure deterministic pedestrian behavior and obstacle placement across all planners.
