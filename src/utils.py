"""Utility helpers for visualization and IO."""

import matplotlib.pyplot as plt
import numpy as np


def overlay_points(image: np.ndarray, points, color="r"):
    """Show image with overlaid points (list of (y,x))."""
    plt.imshow(image, cmap="gray")
    ys = [p[0] for p in points]
    xs = [p[1] for p in points]
    plt.scatter(xs, ys, c=color, s=30, edgecolors="white")
    plt.axis("off")
    return plt
