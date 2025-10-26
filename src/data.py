"""Data loading helpers for image sequences."""

from skimage import io
import os
from typing import List, Iterator


def load_image(path: str):
    """Load a single image (grayscale) and return as ndarray."""
    img = io.imread(path, as_gray=True)
    return img


def list_frames(folder: str) -> List[str]:
    """Return a sorted list of image file paths from a folder."""
    exts = (".tif", ".tiff", ".png", ".jpg", ".jpeg")
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]
    files.sort()
    return files


def load_sequence(folder: str) -> Iterator:
    """Yield images from a folder in sorted order."""
    for p in list_frames(folder):
        yield load_image(p)
