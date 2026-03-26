# Path Planning Algorithm Parameters

This document describes the important parameters of the path planning algorithms implemented in this project. It includes the algorithms tested in the benchmark suite: **A\***, **Hybrid A\***, **Dijkstra**, **Lazy Theta\***, **D\* Lite**, **RRT**, **APF** (Artificial Potential Field), and **DWA** (Dynamic Window Approach).

---

## Index

1. [A* (A-Star)](#1-a-a-star)
2. [Hybrid A*](#2-hybrid-a)
3. [Dijkstra](#3-dijkstra)
4. [Lazy Theta*](#4-lazy-theta)
5. [D* Lite](#5-d-lite)
6. [APF (Artificial Potential Field)](#6-apf-artificial-potential-field)
7. [DWA (Dynamic Window Approach)](#7-dwa-dynamic-window-approach)
8. [RRT (Rapidly-exploring Random Tree)](#8-rrt-rapidly-exploring-random-tree)
9. [General System Parameters](#9-general-system-parameters)

---

## 1. A* (A-Star)

### Description
The A* algorithm is a graph search algorithm that finds the shortest path between two points using a heuristic function. In this implementation, A* does not have specific configurable parameters but uses the general system parameters.

### Code Location
- **Implementation**: `src/core/path_planner/path_planner/src/graph_planner/astar_planner.cpp`
- **Header**: `src/core/path_planner/path_planner/include/path_planner/graph_planner/astar_planner.h`

### Parameters Used

A* uses only the general path planner parameters:

| Parameter | Location | Default Value | Description |
|-----------|-------------|--------------|-----------|
| `obstacle_inflation_factor` | `system_config.pb.txt` | `0.5` | Obstacle inflation factor used for collision checking |

### Remarks
- A* uses 8-direction movement (4 cardinal + 4 diagonal)
- The heuristic used is the Euclidean distance
- Can be configured to function as Dijkstra (`dijkstra=true`) or GBFS (`gbfs=true`)

---

## 2. Hybrid A*

### Description
Hybrid A* is an extension of A* that considers vehicle movement constraints (such as minimum turning radius), generating smooth trajectories using Dubins or Reeds-Shepp motion models.

### Parameter Location
- **Configuration File**: `src/core/system_config/system_config/system_config.pb.txt` (lines 12-30)
- **Protobuf Definition**: `src/core/system_config/system_config/path_planner_protos/graph_planner/hybrid_astar_planner.proto`
- **Implementation**: `src/core/path_planner/path_planner/src/graph_planner/hybrid_astar_planner/hybrid_astar_planner.cpp`

### Parameters

| Parameter | Type | Default Value | Unit | Description |
|-----------|------|--------------|---------|-----------|
| `motion_model` | `enum` | `DUBINS_UNSPECIFIED` | - | Motion model: `DUBINS_UNSPECIFIED` (0) or `REEDS_SHEPP` (1) |
| `goal_tolerance` | `double` | `0.125` | meters | Distance tolerance to the goal |
| `dim_3_size` | `int64` | `64` | - | Auxiliary dimensions for search (angular discretization) |
| `max_iterations` | `int64` | `1000000` | - | Maximum number of iterations during search expansion |
| `max_approach_iterations` | `int64` | `1000` | - | Maximum iterations during search near the goal |
| `traverse_unknown` | `bool` | `false` | - | Allow search in unknown space (useful during mapping) |
| `curve_sample_ratio` | `double` | `0.15` | - | Sampling ratio for curve generation |
| `minimum_turning_radius` | `double` | `0.4` | meters | Minimum turning radius of the vehicle |
| `non_straight_penalty` | `double` | `1.20` | - | Penalty for non-straight movements (must be ≥ 1) |
| `change_penalty` | `double` | `0.0` | - | Penalty for direction change (must be ≥ 0) |
| `reverse_penalty` | `double` | `2.1` | - | Penalty for reverse movement (must be ≥ 1) |
| `retrospective_penalty` | `double` | `0.025` | - | Penalty to prefer later maneuvers over earlier ones along the path |
| `lookup_table_dim` | `int64` | `20` | - | Dubins/Reeds-Shepp distance window size for cache [m] |
| `analytic_expansion_ratio` | `double` | `3.5` | - | Ratio to attempt analytic expansions during search for final approach |
| `analytic_expansion_max_length` | `double` | `3.0` | meters | Maximum length of analytic expansion to be considered valid |
| `lamda_h` | `double` | `2.5` | - | Heuristic weight (lambda) |
| `default_graph_size` | `int64` | `100000` | - | Default graph size |

### Configuration Example

```protobuf
graph_planner {
    hybrid_astar_planner {
        motion_model: DUBINS_UNSPECIFIED
        goal_tolerance: 0.125
        dim_3_size: 64
        max_iterations: 1000000
        max_approach_iterations: 1000
        traverse_unknown: false
        curve_sample_ratio: 0.15
        minimum_turning_radius: 0.4
        non_straight_penalty: 1.20
        change_penalty: 0.0
        reverse_penalty: 2.1
        retrospective_penalty: 0.025
        lookup_table_dim: 20
        analytic_expansion_ratio: 3.5
        analytic_expansion_max_length: 3.0
        lamda_h: 2.5
        default_graph_size: 100000
    }
}
```

### Tuning Tips
- **`minimum_turning_radius`**: Should match the physical characteristics of the robot.
- **`reverse_penalty`**: Higher values discourage reverse movement.
- **`max_iterations`**: Increasing can improve path quality but increases calculation time.
- **`dim_3_size`**: Controls angular discretization. Higher values = more precision but more computational cost.

---

## 3. Dijkstra

### Description
The Dijkstra algorithm is a variant of A* that does not use a heuristic (h=0), ensuring the lowest cost path is found, but generally exploring more nodes.

### Code Location
- **Implementation**: Uses the same `AStarPathPlanner` class with the `dijkstra=true` flag.
- **Code**: `src/core/path_planner/path_planner/src/graph_planner/astar_planner.cpp`

### Parameters Used

Dijkstra uses only the general path planner parameters (same as A*):

| Parameter | Location | Default Value | Description |
|-----------|-------------|--------------|-----------|
| `obstacle_inflation_factor` | `system_config.pb.txt` | `0.5` | Obstacle inflation factor used for collision checking |

### Remarks
- Dijkstra is implemented as a variant of A* (same class, different flag).
- It does not use a heuristic, so it always finds the optimal path but can be slower.
- Uses 8-direction movement (4 cardinal + 4 diagonal).

---

## 4. Lazy Theta*

### Description
Lazy Theta* is a variant of Theta* that checks collisions in a "lazy" manner, improving computational efficiency by only validating line-of-sight when necessary.

### Code Location
- **Implementation**: `src/core/path_planner/path_planner/src/graph_planner/lazy_theta_star_planner.cpp`
- **Header**: `src/core/path_planner/path_planner/include/path_planner/graph_planner/lazy_theta_star_planner.h`

### Parameters Used

Lazy Theta* uses only the general path planner parameters:

| Parameter | Location | Default Value | Description |
|-----------|-------------|--------------|-----------|
| `obstacle_inflation_factor` | `system_config.pb.txt` | `0.5` | Obstacle inflation factor used for collision checking |

### Remarks
- Inherits from `ThetaStarPathPlanner`.
- Does not have specific configurable parameters in the config file.
- Checks collisions lazily (only when needed), improving performance.

---

## 5. D* Lite

### Description
D* Lite is an incremental planning algorithm that can replan efficiently when the environment changes, making it useful for navigation in dynamic environments.

### Code Location
- **Implementation**: `src/core/path_planner/path_planner/src/graph_planner/dstar_lite_planner.cpp`
- **Header**: `src/core/path_planner/path_planner/include/path_planner/graph_planner/dstar_lite_planner.h`

### Parameters Used

D* Lite uses only the general path planner parameters:

| Parameter | Location | Default Value | Description |
|-----------|-------------|--------------|-----------|
| `obstacle_inflation_factor` | `system_config.pb.txt` | `0.5` | Obstacle inflation factor used for collision checking |

### Remarks
- Does not have specific configurable parameters.
- Maintains a local window of the costmap (fixed size: 70 cells = 3.5m / 0.05m resolution).
- Efficient for replanning when the environment changes.

---

## 6. APF (Artificial Potential Field)

### Description
The APF algorithm uses artificial potential fields to guide the robot towards the goal (attractive force) and away from obstacles (repulsive force).

### Parameter Location
- **Configuration File**: `src/core/system_config/system_config/system_config.pb.txt` (lines 150-157)
- **Protobuf Definition**: `src/core/system_config/system_config/controller_protos/apf_controller.proto`

### Parameters

| Parameter | Type | Default Value | Unit | Description |
|-----------|------|--------------|---------|-----------|
| `lookahead_time` | `double` | `1.0` | seconds | Lookahead time for trajectory prediction |
| `min_lookahead_dist` | `double` | `0.3` | meters | Minimum lookahead distance |
| `max_lookahead_dist` | `double` | `0.9` | meters | Maximum lookahead distance |
| `smooth_window` | `int64` | `5` | - | Time window for trajectory smoothing |
| `weight_attractive_force` | `double` | `1.0` | - | Attractive force scaling factor (attraction to goal) |
| `weight_repulsive_force` | `double` | `3.0` | - | **Repulsion Gain (krep)**: Global repulsive force scaling factor (obstacle repulsion) |

### Repulsion Gain (krep) Based on Distance

The **Repulsion Gain (krep)** in APF is calculated **dynamically based on the distance** to the obstacle and then multiplied by the global gain `weight_repulsive_force`.

**Distance-based krep formula:**
```cpp
k = (1.0 - 1.0 / dist) / (dist * dist)
```

Where:
- `dist`: Normalized distance to the obstacle (0 = at obstacle, 1 = far from obstacle)
- `k`: Dynamically calculated repulsive gain

**Final repulsive force:**
```cpp
rep_force = k * grad_dist
net_force = weight_attractive_force * attr_force + 
            weight_repulsive_force * rep_force
```

### Characteristics
- The gain `k` is **inversely proportional to the square of the distance**.
- When near an obstacle (`dist → 0`), `k → ∞` (very high repulsive force).
- When far from an obstacle (`dist → 1`), `k → 0` (low repulsive force).
- The `weight_repulsive_force` parameter (default: **3.0**) multiplies the entire repulsive force.

### Recommendations
- **Low `weight_repulsive_force` (1.0-2.0)**: Less cautious robot, may pass very close to obstacles.
- **Medium `weight_repulsive_force` (3.0-5.0)**: Balance between safety and efficiency.
- **High `weight_repulsive_force` (>5.0)**: Very cautious robot, may struggle to pass through narrow corridors.

### Configuration Example

```protobuf
apf_controller {
    lookahead_time: 1.0
    min_lookahead_dist: 0.3
    max_lookahead_dist: 0.9
    smooth_window: 5
    weight_attractive_force: 1.0
    weight_repulsive_force: 3.0
}
```

### Tuning Tips
- **`weight_repulsive_force`**: Increasing this value makes the robot more cautious with obstacles but can cause oscillations.
- **`weight_attractive_force`**: Controls the force of attraction to the goal.
- **`smooth_window`**: Higher values result in smoother trajectories but may increase latency.

---

## 7. DWA (Dynamic Window Approach)

### Description
DWA is a local planning algorithm that selects safe velocities within a dynamic window, considering the robot's acceleration limits.

### Parameter Location
- **Configuration File**: `src/core/controller/dwa_controller/cfg/DWAController.cfg`
- **Implementation**: `src/core/controller/dwa_controller/src/dwa.cpp`

### DWA Specific Parameters

| Parameter | Type | Default Value | Unit | Description |
|-----------|------|--------------|---------|-----------|
| `sim_time` | `double` | `1.7` | seconds | Simulation time to roll out trajectories |
| `sim_granularity` | `double` | `0.025` | meters | Granularity for collision checking along the trajectory |
| `angular_sim_granularity` | `double` | `0.1` | radians | Granularity for collision checking during rotations |
| `path_distance_bias` | `double` | `0.6` | - | Weight for path distance in the cost function |
| `goal_distance_bias` | `double` | `0.8` | - | Weight for goal distance in the cost function |
| `occdist_scale` | `double` | `0.01` | - | Weight for obstacle distance in the cost function |
| `twirling_scale` | `double` | `0.0` | - | Weight to penalize changes in robot heading |
| `stop_time_buffer` | `double` | `0.2` | seconds | Time the robot should stop before a collision for the trajectory to be valid |
| `oscillation_reset_dist` | `double` | `0.05` | meters | Distance the robot must travel before resetting oscillation flags |
| `oscillation_reset_angle` | `double` | `0.2` | radians | Angle the robot must turn before resetting oscillation flags |
| `forward_point_distance` | `double` | `0.325` | meters | Distance from the robot center to place an additional scoring point |
| `scaling_speed` | `double` | `0.25` | m/s | Speed value to start scaling the robot footprint |
| `max_scaling_factor` | `double` | `0.2` | - | Maximum factor to scale the robot footprint |
| `vx_samples` | `int` | `3` | - | Number of samples to explore the x-velocity space |
| `vy_samples` | `int` | `10` | - | Number of samples to explore the y-velocity space |
| `vth_samples` | `int` | `20` | - | Number of samples to explore the angular velocity space |
| `use_dwa` | `bool` | `True` | - | Use the dynamic window approach to restrict sampling velocities |

### Generic Local Planner Parameters

DWA also uses generic local planner parameters (defined via `add_generic_localplanner_params`):

- `max_vel_trans`, `min_vel_trans`: Maximum and minimum translational velocities.
- `max_vel_x`, `min_vel_x`: Maximum and minimum x-velocities.
- `max_vel_y`, `min_vel_y`: Maximum and minimum y-velocities.
- `max_vel_theta`, `min_vel_theta`: Maximum and minimum angular velocities.
- `acc_lim_x`, `acc_lim_y`, `acc_lim_theta`, `acc_lim_trans`: Acceleration limits.
- `xy_goal_tolerance`, `yaw_goal_tolerance`: Tolerances for reaching the goal.
- `prune_plan`: Whether to prune the plan.
- `trans_stopped_vel`, `theta_stopped_vel`: Velocities considered as stopped.

### Tuning Tips
- **`sim_time`**: Increasing allows looking further ahead but increases calculation time.
- **`path_distance_bias` vs `goal_distance_bias`**: Balance between following the global path and going straight to the goal.
- **`occdist_scale`**: Higher values make the robot more cautious with obstacles.
- **`vx_samples`, `vth_samples`**: More samples improve quality but increase calculation time.

---

## 8. RRT (Rapidly-exploring Random Tree)

### Description
RRT is a probabilistic planning algorithm that builds a random exploration tree in the configuration space.

### Parameter Location
- **Configuration File**: `src/core/system_config/system_config/system_config.pb.txt` (lines 33-38)
- **Protobuf Definition**: `src/core/system_config/system_config/path_planner_protos/sample_planner/sample_planner.proto`
- **Implementation**: `src/core/path_planner/path_planner/src/sample_planner/rrt_planner.cpp`

### Parameters

| Parameter | Type | Default Value | Unit | Description |
|-----------|------|--------------|---------|-----------|
| `sample_points` | `int64` | `1500` | - | Number of random points to sample |
| `sample_max_distance` | `double` | `30.0` | meters | Maximum distance between sample points |
| `optimization_radius` | `double` | `20.0` | meters | Optimization radius to improve the path |
| `optimization_sampe_probability` | `double` | `0.05` | - | **Goal Bias**: Probability of sampling the goal directly (0.0-1.0) |

### Goal Bias

**Goal Bias** in RRT is controlled by the `optimization_sampe_probability` parameter with a default value of **0.05 (5%)**.

**How it works:**
- At each iteration, the algorithm generates a random number between 0 and 1.
- If the number is **≤ 0.05** (5% of the time), the algorithm samples the goal directly.
- Otherwise (95% of the time), it samples a random point in the configuration space.

**Code Formula:**
```cpp
if (p(eng) > config_.sample_planner().optimization_sampe_probability()) {
    // Sample random point
} else {
    // Sample goal directly
}
```

### Recommendations
- **Low values (0.01-0.05)**: Broader exploration, may take longer to converge.
- **Medium values (0.1-0.2)**: Balance between exploration and convergence.
- **High values (>0.3)**: Faster convergence but may get stuck in local minima.

### Configuration Example

```protobuf
sample_planner {
    sample_points: 1500
    sample_max_distance: 30.0
    optimization_radius: 20.0
    optimization_sampe_probability: 0.05
}
```

### Additional Parameters Used

RRT also uses general path planner parameters:

| Parameter | Default Value | Description |
|-----------|--------------|-----------|
| `obstacle_inflation_factor` | `0.5` | Obstacle inflation factor for collision checking |

### Tuning Tips
- **`sample_points`**: Increasing improves the probability of finding a path but increases calculation time.
- **`sample_max_distance`**: Controls step sizes. Smaller values result in more detailed exploration.
- **`optimization_sampe_probability`**: Probability of sampling the goal directly. Values of 0.1-0.2 can speed up convergence.
- **`optimization_radius`**: Used by RRT variants (RRT*, Informed RRT) for path optimization.

---

## 9. General System Parameters

### Path Planner Parameters

Located in `src/core/system_config/system_config/system_config.pb.txt`:

| Parameter | Default Value | Description |
|-----------|--------------|-----------|
| `obstacle_inflation_factor` | `0.5` | Obstacle inflation factor (used by all planners) |
| `convert_offset` | `0.0` | Conversion offset |
| `default_tolerance` | `0.0` | Default tolerance |
| `expand_zone` | `true` | Expand zone |
| `show_safety_corridor` | `false` | Show safety corridor |
| `enable_resample` | `false` | Enable resampling |
| `resample_ratio` | `0.5` | Resampling ratio |
| `is_outline_map` | `true` | Whether it is an outline map |

### General Controller Parameters

Located in `src/core/system_config/system_config/system_config.pb.txt` (lines 78-90):

| Parameter | Default Value | Unit | Description |
|-----------|--------------|---------|-----------|
| `control_frequency` | `10.0` | Hz | Control frequency |
| `goal_dist_tolerance` | `0.3` | meters | Distance tolerance to the goal |
| `rotate_tolerance` | `0.5` | radians | Rotation tolerance |
| `max_linear_velocity` | `0.5` | m/s | Maximum linear velocity |
| `min_linear_velocity` | `0.0` | m/s | Minimum linear velocity |
| `max_linear_velocity_increment` | `0.5` | m/s | Maximum linear velocity increment |
| `max_angular_velocity` | `1.5` | rad/s | Maximum angular velocity |
| `min_angular_velocity` | `0.0` | rad/s | Minimum angular velocity |
| `max_angular_velocity_increment` | `1.5` | rad/s | Maximum angular velocity increment |

---

## How to Modify Parameters

### For APF, RRT, and Hybrid A*:
1. Edit the file: `src/core/system_config/system_config/system_config.pb.txt`
2. Locate the corresponding section:
   - `apf_controller` for APF
   - `sample_planner` for RRT
   - `graph_planner.hybrid_astar_planner` for Hybrid A*
3. Modify the desired values.
4. Recompile the project.

### For DWA:
1. Edit the file: `src/core/controller/dwa_controller/cfg/DWAController.cfg`
2. Modify the default values in the `gen.add(...)` lines.
3. Recompile the project.
4. **Alternatively**: Use `dynamic_reconfigure` during execution:
   ```bash
   rosrun rqt_reconfigure rqt_reconfigure
   ```

### For A*:
A* does not have specific parameters, but you can adjust:
- `obstacle_inflation_factor` in `system_config.pb.txt` to tune obstacle sensitivity.

---

## References

- **A***: Implementation based on heuristic search.
- **APF**: Artificial potential fields for navigation.
- **DWA**: Dynamic Window Approach for local planning.
- **RRT**: Rapidly-exploring Random Tree for probabilistic planning.

---

## Final Notes

- All default values are based on the current project configuration.
- Parameters may vary depending on the robot type and environment.
- It is recommended to test different configurations to optimize performance.
- Use visualization tools (RViz) to observe the effect of changes.

---

**Last updated**: Based on project source code analysis

