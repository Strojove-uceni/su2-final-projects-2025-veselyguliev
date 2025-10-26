"""Simple object detection + tracking utilities.

This module provides a basic centroid-based tracker suitable as a starter.
"""

import numpy as np
from scipy import ndimage as ndi
from typing import List, Dict, Tuple


def detect_blobs(frame: np.ndarray, threshold: float = 0.2, min_size: int = 5) -> List[Tuple[float, float]]:
    """Very small detector: threshold + connected components -> centroids.

    Returns list of (y, x) centroids.
    """
    mask = frame > threshold
    labeled, n = ndi.label(mask)
    centers = []
    for lab in range(1, n + 1):
        coords = np.argwhere(labeled == lab)
        if coords.shape[0] < min_size:
            continue
        cy, cx = coords.mean(axis=0)
        centers.append((float(cy), float(cx)))
    return centers


def track_centroids(sequence: List[np.ndarray], max_distance: float = 10.0) -> Dict[int, List[Tuple[int, float, float]]]:
    """A naive frame-to-frame centroid tracker.

    Returns tracks dict: track_id -> list of (frame_index, y, x).
    """
    tracks: Dict[int, List[Tuple[int, float, float]]] = {}
    next_id = 1
    prev_centroids = []
    prev_ids = []

    for t, frame in enumerate(sequence):
        centroids = detect_blobs(frame)
        assigned = set()
        new_prev_centroids = []
        new_prev_ids = []

        # greedy nearest-neighbour assignment
        for cid, c in enumerate(centroids):
            best_id = None
            best_dist = max_distance + 1
            for pid, p in enumerate(prev_centroids):
                dist = np.hypot(c[0] - p[0], c[1] - p[1])
                if dist < best_dist and prev_ids[pid] not in assigned:
                    best_dist = dist
                    best_id = prev_ids[pid]
            if best_id is None:
                best_id = next_id
                next_id += 1
            assigned.add(best_id)
            tracks.setdefault(best_id, []).append((t, c[0], c[1]))
            new_prev_centroids.append(c)
            new_prev_ids.append(best_id)

        prev_centroids = new_prev_centroids
        prev_ids = new_prev_ids

    return tracks
