"""Simple runner script to demonstrate pipeline usage.

Usage:
    python run_tracking.py --input data/frames --output results
"""

import argparse
import os
from src import data, preprocessing, tracking, utils


def main(input_folder: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    seq = list(data.load_sequence(input_folder))
    pre = [preprocessing.normalize_contrast(preprocessing.gaussian_blur(f, sigma=1.0)) for f in seq]
    tracks = tracking.track_centroids(pre)
    # Save a simple visualization for the first frame
    if seq:
        first = seq[0]
        # take detected centroids for frame 0
        pts = []
        for tid, recs in tracks.items():
            for frame_idx, y, x in recs:
                if frame_idx == 0:
                    pts.append((y, x))
        plt = utils.overlay_points(first, pts)
        plt.savefig(os.path.join(output_folder, "frame0_overlay.png"))
    # dump tracks to csv
    import csv
    out_csv = os.path.join(output_folder, "tracks.csv")
    with open(out_csv, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["track_id", "frame", "y", "x"])
        for tid, recs in tracks.items():
            for frame_idx, y, x in recs:
                writer.writerow([tid, frame_idx, y, x])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    main(args.input, args.output)
