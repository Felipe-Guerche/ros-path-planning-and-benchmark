#!/usr/bin/env python3
"""
Generate Random Poses for Benchmark
- Reads .pgm occupancy grid and .yaml map config.
- Applies binary erosion for safety margin from walls.
- Optionally excludes pedestrian zones (1.5m radius).
- Verifies start/goal are in the SAME connected free region.
- Supports reproducible seeds.
- Outputs: x1 y1 x2 y2 (start goal) to stdout.
- Outputs: seed to stderr (for logging).
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
    """Load map config and occupancy grid image."""
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    image_filename = config['image']
    resolution = float(config['resolution'])
    origin = config['origin']
    ox, oy = origin[0], origin[1]
    free_thresh_prob = float(config.get('free_thresh', 0.196))

    pgm_path = os.path.join(os.path.dirname(yaml_path), image_filename)
    if not os.path.exists(pgm_path):
        print(f"Error: Map image not found: {pgm_path}", file=sys.stderr)
        sys.exit(1)

    img = Image.open(pgm_path).convert('L')
    img_data = np.array(img)
    return img_data, resolution, ox, oy, free_thresh_prob


def build_free_mask(img_data, resolution, free_thresh_prob, safety_radius_m,
                    ped_positions=None, ped_exclusion_radius=1.5, ox=0, oy=0):
    """Build a boolean free-space mask with safety erosion and pedestrian exclusion."""
    H, W = img_data.shape

    # Basic free-space from occupancy grid
    p_thresh = 255 - 255 * free_thresh_prob
    free_mask = img_data > p_thresh

    # Erode for robot safety margin
    pixels_to_erode = int(math.ceil(safety_radius_m / resolution))
    if pixels_to_erode > 0:
        free_mask = ndimage.binary_erosion(free_mask, iterations=pixels_to_erode)

    # Exclude pedestrian zones
    if ped_positions:
        ped_radius_px = int(math.ceil(ped_exclusion_radius / resolution))
        for px, py in ped_positions:
            # Convert world coords to pixel coords
            col = int(round((px - ox) / resolution))
            row = int(round(H - 1 - (py - oy) / resolution))
            # Mark circle around pedestrian as occupied
            rr, cc = np.ogrid[:H, :W]
            dist_sq = (rr - row) ** 2 + (cc - col) ** 2
            free_mask[dist_sq <= ped_radius_px ** 2] = False

    return free_mask


def get_connected_labels(free_mask):
    """Label connected components of free space."""
    labeled, num_features = ndimage.label(free_mask)
    return labeled, num_features


def px_to_real(row, col, H, resolution, ox, oy):
    """Convert pixel (row, col) to real-world (x, y) coordinates."""
    x = ox + col * resolution
    y = oy + (H - 1 - row) * resolution
    return x, y


def parse_pedestrian_positions(ped_config_path):
    """Extract pedestrian (x, y) positions from pedestrian_config.yaml."""
    if not os.path.exists(ped_config_path):
        print(f"Warning: Pedestrian config not found: {ped_config_path}", file=sys.stderr)
        return []

    with open(ped_config_path, 'r') as f:
        config = yaml.safe_load(f)

    positions = []
    if config and 'pedestrians' in config and 'ped_property' in config['pedestrians']:
        for ped in config['pedestrians']['ped_property']:
            pose_parts = str(ped['pose']).split()
            if len(pose_parts) >= 2:
                positions.append((float(pose_parts[0]), float(pose_parts[1])))
    return positions


def main():
    parser = argparse.ArgumentParser(description='Generate random safe poses from map')
    parser.add_argument('map_yaml', help='Path to map .yaml file')
    parser.add_argument('--safety_radius', type=float, default=0.5,
                        help='Safety radius from walls in meters (default: 0.5)')
    parser.add_argument('--min_dist', type=float, default=5.0,
                        help='Minimum distance between start and goal in meters (default: 5.0)')
    parser.add_argument('--seed', type=int, default=None,
                        help='Random seed for reproducibility (default: random)')
    parser.add_argument('--ped_config', type=str, default=None,
                        help='Path to pedestrian_config.yaml to exclude ped zones')
    parser.add_argument('--ped_exclusion_radius', type=float, default=1.5,
                        help='Exclusion radius around each pedestrian in meters (default: 1.5)')
    args = parser.parse_args()

    # Set seed
    if args.seed is None:
        args.seed = random.randint(0, 2**31 - 1)
    random.seed(args.seed)
    np.random.seed(args.seed)
    print(f"SEED={args.seed}", file=sys.stderr)

    # Load map
    if not os.path.exists(args.map_yaml):
        print(f"Error: Map yaml not found: {args.map_yaml}", file=sys.stderr)
        sys.exit(1)

    img_data, resolution, ox, oy, free_thresh_prob = load_map(args.map_yaml)
    H, W = img_data.shape

    # Parse pedestrian positions
    ped_positions = []
    if args.ped_config:
        ped_positions = parse_pedestrian_positions(args.ped_config)
        if ped_positions:
            print(f"Excluding {len(ped_positions)} pedestrian zones", file=sys.stderr)

    # Build free mask
    free_mask = build_free_mask(
        img_data, resolution, free_thresh_prob,
        args.safety_radius, ped_positions, args.ped_exclusion_radius, ox, oy
    )

    # Label connected components
    labeled, num_features = get_connected_labels(free_mask)

    # Get all free pixels with their component labels
    free_y, free_x = np.where(free_mask)
    if len(free_y) < 2:
        print("Error: Not enough free space found after erosion.", file=sys.stderr)
        sys.exit(1)

    free_labels = labeled[free_y, free_x]

    # Find the largest connected component
    unique_labels, counts = np.unique(free_labels, return_counts=True)
    largest_label = unique_labels[np.argmax(counts)]

    # Filter to largest component only (ensures navigability)
    mask_largest = free_labels == largest_label
    free_y = free_y[mask_largest]
    free_x = free_x[mask_largest]

    if len(free_y) < 2:
        print("Error: Largest connected region has < 2 points.", file=sys.stderr)
        sys.exit(1)

    print(f"Free pixels in largest region: {len(free_y)}", file=sys.stderr)

    # Sample valid pair
    max_attempts = 2000
    for _ in range(max_attempts):
        idx1, idx2 = random.sample(range(len(free_y)), 2)
        r1, c1 = free_y[idx1], free_x[idx1]
        r2, c2 = free_y[idx2], free_x[idx2]

        x1, y1 = px_to_real(r1, c1, H, resolution, ox, oy)
        x2, y2 = px_to_real(r2, c2, H, resolution, ox, oy)

        dist = math.hypot(x2 - x1, y2 - y1)
        if dist >= args.min_dist:
            print(f"{x1:.3f} {y1:.3f} {x2:.3f} {y2:.3f}")
            return

    # Fallback: find the most distant pair from a sample of candidates
    print("Warning: Could not find points satisfying min_dist, using most distant pair", file=sys.stderr)
    n_candidates = min(50, len(free_y))
    candidate_indices = random.sample(range(len(free_y)), n_candidates)
    best_dist = 0
    best_i, best_j = candidate_indices[0], candidate_indices[-1]
    for ci in candidate_indices:
        for cj in candidate_indices:
            if ci == cj:
                continue
            xci, yci = px_to_real(free_y[ci], free_x[ci], H, resolution, ox, oy)
            xcj, ycj = px_to_real(free_y[cj], free_x[cj], H, resolution, ox, oy)
            d = math.hypot(xcj - xci, ycj - yci)
            if d > best_dist:
                best_dist = d
                best_i, best_j = ci, cj
    x1, y1 = px_to_real(free_y[best_i], free_x[best_i], H, resolution, ox, oy)
    x2, y2 = px_to_real(free_y[best_j], free_x[best_j], H, resolution, ox, oy)
    print(f"{x1:.3f} {y1:.3f} {x2:.3f} {y2:.3f}")


if __name__ == '__main__':
    main()
