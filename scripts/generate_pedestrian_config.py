#!/usr/bin/env python3
"""
Generate Pedestrian Configuration for Benchmark
- Uses the same occupancy grid as generate_random_poses.py to find free space.
- Spawns N pedestrians in safe positions (not inside walls or obstacles).
- Generates 2 waypoints per pedestrian for cyclic SFM traversal.
- Ensures pedestrians don't spawn on top of each other (≥2m apart).
- Randomizes velocity within realistic walking range [0.8, 1.4] m/s.
- Outputs a valid pedestrian_config.yaml compatible with the existing pipeline.
"""

import os
import sys
import yaml
import random
import math
import argparse

try:
    import numpy as np
    from PIL import Image
    import scipy.ndimage as ndimage
except ImportError:
    print("Error: Required libraries (numpy, Pillow, scipy) not installed.", file=sys.stderr)
    sys.exit(1)


def load_map(yaml_path):
    """Load map config and occupancy grid."""
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    image_filename = config['image']
    resolution = float(config['resolution'])
    origin = config['origin']
    ox, oy = origin[0], origin[1]
    free_thresh_prob = float(config.get('free_thresh', 0.196))

    pgm_path = os.path.join(os.path.dirname(yaml_path), image_filename)
    img = Image.open(pgm_path).convert('L')
    img_data = np.array(img)
    return img_data, resolution, ox, oy, free_thresh_prob


def build_free_mask(img_data, resolution, free_thresh_prob, safety_radius_m=0.8):
    """Build free-space mask with erosion for pedestrian safety."""
    p_thresh = 255 - 255 * free_thresh_prob
    free_mask = img_data > p_thresh

    pixels_to_erode = int(math.ceil(safety_radius_m / resolution))
    if pixels_to_erode > 0:
        free_mask = ndimage.binary_erosion(free_mask, iterations=pixels_to_erode)
    return free_mask


def px_to_real(row, col, H, resolution, ox, oy):
    """Convert pixel to world coordinates."""
    x = ox + col * resolution
    y = oy + (H - 1 - row) * resolution
    return x, y


def sample_point(free_y, free_x, H, resolution, ox, oy, existing_points, min_dist=2.0, max_attempts=500):
    """Sample a free-space point that is ≥min_dist from all existing_points."""
    for _ in range(max_attempts):
        idx = random.randint(0, len(free_y) - 1)
        r, c = free_y[idx], free_x[idx]
        x, y = px_to_real(r, c, H, resolution, ox, oy)

        too_close = False
        for ex, ey in existing_points:
            if math.hypot(x - ex, y - ey) < min_dist:
                too_close = True
                break
        if not too_close:
            return x, y

    # Fallback: pick any point and log the violation so it is visible in container logs
    idx = random.randint(0, len(free_y) - 1)
    r, c = free_y[idx], free_x[idx]
    x, y = px_to_real(r, c, H, resolution, ox, oy)
    min_achieved = min(
        (math.hypot(x - ex, y - ey) for ex, ey in existing_points),
        default=float('inf')
    )
    print(
        f"[WARN] sample_point fallback: min_dist={min_dist}m not satisfied "
        f"(closest existing point: {min_achieved:.2f}m). Pedestrians may overlap.",
        file=sys.stderr
    )
    return x, y


def generate_config(num_peds, map_yaml, robot_pos=None, seed=None, output_path=None):
    """Generate a pedestrian_config.yaml with num_peds pedestrians."""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    img_data, resolution, ox, oy, free_thresh_prob = load_map(map_yaml)
    H, W = img_data.shape

    free_mask = build_free_mask(img_data, resolution, free_thresh_prob, safety_radius_m=0.8)
    free_y, free_x = np.where(free_mask)

    if len(free_y) < num_peds * 3:
        print(f"Error: Not enough free space for {num_peds} pedestrians.", file=sys.stderr)
        sys.exit(1)

    # Existing points to avoid: start with robot position if known
    existing = []
    if robot_pos:
        existing.append(robot_pos)

    pedestrians = []
    for i in range(num_peds):
        # Sample spawn position
        px, py = sample_point(free_y, free_x, H, resolution, ox, oy, existing, min_dist=2.0)
        existing.append((px, py))

        # Sample 2 waypoints for cyclic trajectory (≥3m from each other)
        wp1_x, wp1_y = px, py  # First waypoint = spawn
        wp2_x, wp2_y = sample_point(free_y, free_x, H, resolution, ox, oy,
                                     [(wp1_x, wp1_y)], min_dist=3.0)

        # Random velocity in realistic range
        velocity = round(random.uniform(0.8, 1.4), 1)

        ped = {
            'name': f'human_{i+1}',
            'pose': f'{px:.2f} {py:.2f} 1 0 0 0',
            'velocity': velocity,
            'radius': 0.4,
            'cycle': True,
            'ignore': {
                'model_1': 'ground_plane',
                'model_2': 'turtlebot3_waffle'
            },
            'trajectory': {
                'goal_point_1': f'{wp1_x:.2f} {wp1_y:.2f} 1 0 0 0',
                'goal_point_2': f'{wp2_x:.2f} {wp2_y:.2f} 1 0 0 0'
            }
        }
        pedestrians.append(ped)

    # Build full config (keeping same format as existing)
    config = {
        'social_force': {
            'animation_factor': 5.1,
            'people_distance': 6.0,
            'goal_weight': 2.0,
            'obstacle_weight': 20.0,
            'social_weight': 15,
            'group_gaze_weight': 3.0,
            'group_coh_weight': 2.0,
            'group_rep_weight': 1.0
        },
        'pedestrians': {
            'update_rate': 5,
            'ped_property': pedestrians
        }
    }

    yaml_str = yaml.dump(config, default_flow_style=False, sort_keys=False, allow_unicode=True)

    if output_path:
        with open(output_path, 'w') as f:
            f.write(yaml_str)
        print(f"Generated {num_peds} pedestrians -> {output_path}", file=sys.stderr)
    else:
        print(yaml_str)

    return config


def main():
    parser = argparse.ArgumentParser(description='Generate pedestrian config with N safe pedestrians')
    parser.add_argument('map_yaml', help='Path to map .yaml file')
    parser.add_argument('--num_peds', type=int, default=3, help='Number of pedestrians (default: 3)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    parser.add_argument('--robot_x', type=float, default=None, help='Robot X position to avoid')
    parser.add_argument('--robot_y', type=float, default=None, help='Robot Y position to avoid')
    parser.add_argument('--output', type=str, default=None,
                        help='Output path (default: stdout)')
    args = parser.parse_args()

    if args.seed is None:
        args.seed = random.randint(0, 2**31 - 1)

    robot_pos = None
    if args.robot_x is not None and args.robot_y is not None:
        robot_pos = (args.robot_x, args.robot_y)

    generate_config(
        num_peds=args.num_peds,
        map_yaml=args.map_yaml,
        robot_pos=robot_pos,
        seed=args.seed,
        output_path=args.output
    )


if __name__ == '__main__':
    main()
