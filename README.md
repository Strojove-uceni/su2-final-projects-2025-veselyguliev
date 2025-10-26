# Endocytosis Tracking

This repository is a starter project for tracking endocytic vesicles from microscopy time-lapse image sequences.

Purpose
- Provide a small, well-structured Python project to iterate on preprocessing, detection, and tracking methods.

Structure
- `src/` - core modules (data loading, preprocessing, tracking, models, utils)
- `notebooks/` - example notebook with usage
- `data/` - place raw frames or sample dataset here
- `tests/` - unit tests (not yet populated)

Quick start
1. Create a virtual environment and install dependencies from `requirements.txt`.
2. Put a sequence of frames (png/jpg/tif) into `data/frames/`.
3. Run `python run_tracking.py --input data/frames --output results`.

Next steps
- Add dataset loader and sample dataset
- Implement and evaluate detection models
- Improve tracking (Kalman, Hungarian assignment)
- Add visualization and metrics (MOTA/MOTP)
