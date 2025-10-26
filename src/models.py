"""Placeholder for models to detect vesicles or classify events.

Add ML/DL model training and inference utilities here.
"""

from typing import Any


def train_detector(X, y, **kwargs) -> Any:
    """Train a detector (placeholder).

    Returns a fitted model object.
    """
    raise NotImplementedError("Add implementation for detector training.")


def predict_detector(model: Any, frames):
    """Run detection on frames using a fitted model."""
    raise NotImplementedError("Add model inference implementation.")
