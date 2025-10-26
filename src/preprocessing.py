"""Image preprocessing utilities."""

import numpy as np
from skimage import filters, exposure


def gaussian_blur(image: np.ndarray, sigma: float = 1.0):
    """Apply Gaussian blur to reduce noise."""
    return filters.gaussian(image, sigma=sigma)


def normalize_contrast(image: np.ndarray):
    """Simple contrast stretching to [0,1]."""
    p2, p98 = np.percentile(image, (2, 98))
    return exposure.rescale_intensity(image, in_range=(p2, p98))
