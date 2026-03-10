import os
import sys
import yaml
import random
import math

try:
    import numpy as np
    from PIL import Image
    import scipy.ndimage as ndimage
except ImportError:
    print("Error: Required libraries (numpy, Pillow, scipy) are not installed.")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_random_poses.py <path_to_map_yaml> [safety_radius_m] [min_dist_m]")
        sys.exit(1)
        
    yaml_path = sys.argv[1]
    safety_radius_m = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    min_dist_m = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0

    if not os.path.exists(yaml_path):
        print(f"Error: Map yaml not found: {yaml_path}")
        sys.exit(1)

    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    image_filename = config['image']
    resolution = float(config['resolution'])
    origin = config['origin']
    ox, oy = origin[0], origin[1]
    free_thresh_prob = float(config.get('free_thresh', 0.196))

    pgm_path = os.path.join(os.path.dirname(yaml_path), image_filename)
    if not os.path.exists(pgm_path):
        print(f"Error: Map image not found: {pgm_path}")
        sys.exit(1)

    img = Image.open(pgm_path).convert('L')
    img_data = np.array(img)
    H, W = img_data.shape

    # Pixel value for free space: (255 - p) / 255.0 < free_thresh
    # => p > 255 - 255 * free_thresh
    p_thresh = 255 - 255 * free_thresh_prob
    free_mask = img_data > p_thresh

    # Erode the free space to keep robot away from walls
    pixels_to_erode = int(math.ceil(safety_radius_m / resolution))
    if pixels_to_erode > 0:
        free_mask = ndimage.binary_erosion(free_mask, iterations=pixels_to_erode)

    free_y, free_x = np.where(free_mask)
    if len(free_y) < 2:
        print("Error: Not enough free space found after erosion.")
        sys.exit(1)

    # Helper function to convert pixel (row, col) to real coordinates
    def px_to_real(row, col):
        # In ROS, row=H-1 (bottom) corresponds to Y=oy
        # row=0 (top) corresponds to Y=oy + (H-1)*res
        x = ox + col * resolution
        y = oy + (H - 1 - row) * resolution
        return x, y

    # Try to find a valid pair
    max_attempts = 1000
    for _ in range(max_attempts):
        idx1, idx2 = random.sample(range(len(free_y)), 2)
        r1, c1 = free_y[idx1], free_x[idx1]
        r2, c2 = free_y[idx2], free_x[idx2]

        x1, y1 = px_to_real(r1, c1)
        x2, y2 = px_to_real(r2, c2)

        dist = math.hypot(x2 - x1, y2 - y1)
        if dist >= min_dist_m:
            print(f"{x1:.3f} {y1:.3f} {x2:.3f} {y2:.3f}")
            return

    # If couldn't find points far enough, just return whatever
    print("Warning: Could not find points satisfying min_dist_m", file=sys.stderr)
    r1, c1 = free_y[0], free_x[0]
    r2, c2 = free_y[-1], free_x[-1]
    x1, y1 = px_to_real(r1, c1)
    x2, y2 = px_to_real(r2, c2)
    print(f"{x1:.3f} {y1:.3f} {x2:.3f} {y2:.3f}")

if __name__ == '__main__':
    main()
