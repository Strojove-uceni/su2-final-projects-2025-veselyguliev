# CCP Detection and Tracking Pipeline

**Authors:** Matyáš Veselý, Ruslan Guliev

Detection and tracking of Clathrin-Coated Pits (CCPs) in TIRF-SIM microscopy data using deep learning approaches and particle tracking algorithms.

## Task Description

Clathrin-Coated Pits (CCPs) are small membrane structures involved in receptor-mediated endocytosis. This project addresses the challenge of detecting and tracking these structures in time-lapse TIRF-SIM (Total Internal Reflection Fluorescence - Structured Illumination Microscopy) images. The task involves two main components: accurate spatial detection of CCPs in individual frames and temporal association of detections into coherent trajectories across the video sequence.

Performance is evaluated using the HOTA (Higher Order Tracking Accuracy) metric, which balances detection accuracy (DetA) and association accuracy (AssA).

## Detection Methods

### U-Net++

U-Net++ is an encoder-decoder architecture with nested skip connections that bridge the semantic gap between encoder and decoder feature maps. The dense skip pathways allow the network to capture fine-grained details essential for detecting small structures like CCPs. Our implementation uses attention gates to focus on relevant spatial regions.

During initial experiments with limited training data, U-Net++ was compared against HRNet. HRNet showed better performance, therefore we did not train U-Net++ on larger datasets. The notebook contains training code, parameter sweep functionality, and evaluation tools.

**Showcase:** `UnetPlusPlus_showcase.ipynb`

### HRNet (High-Resolution Network)

HRNet maintains high-resolution representations throughout the network by connecting multi-resolution subnetworks in parallel. Unlike traditional approaches that recover high resolution from low resolution, HRNet preserves spatial precision, making it well-suited for detecting small biological structures.

HRNet proved to be a better alternative to U-Net++ in our experiments and was subsequently trained on larger datasets. The notebook includes loading of a pretrained model trained on 3000 synthetic samples + 2000 fine-tuning samples over 50 epochs.

**Showcase:** `HRnet_showcase.ipynb`

**Repository:** [https://github.com/gulierus/SU2_HR-net_U-net.git](https://github.com/gulierus/SU2_HR-net_U-net.git)

### SAM3 (Segment Anything Model 3)

SAM3 is a pretrained foundation model for image segmentation. We used SAM3 directly without additional training, only combining it with tracking methods to evaluate its out-of-the-box performance on CCP detection.

### StarDist

StarDist is a deep learning method originally designed for star-convex object detection in microscopy images. It predicts object boundaries using radial distances from object centers, making it effective for detecting roughly circular structures. StarDist is particularly robust for overlapping objects.

**Repository:** [https://github.com/veselm73/SU2.git](https://github.com/veselm73/SU2.git)

## Tracking Methods

### LapTrack

LapTrack is a tracking algorithm based on the Linear Assignment Problem (LAP) formulation. It solves the frame-to-frame linking problem by minimizing a global cost function that considers spatial distances between detections. LapTrack is well-suited for particle tracking scenarios where objects do not divide.

For detailed parameter configuration, see the [LapTrack documentation](https://laptrack.readthedocs.io/) and our repositories.

### btrack (v0.6.5)

btrack is a Bayesian multi-object tracking library originally designed for cell tracking in microscopy. It uses a Kalman filter-based motion model for state prediction and a global optimization step to resolve track hypotheses. btrack can handle object appearance, disappearance, and division events.

For detailed parameter configuration, see the [btrack documentation](https://btrack.readthedocs.io/) and our repositories.

## Training Approaches

### Synthetic Data Training (HRNet)

**HRNet** was trained on synthetically generated data using an improved generator. The key improvements include:

**1. Probabilistic Mixing of Clusters and Grid**

The `cluster_sample_prob` parameter controls the sample ratio:
- `0.0` = grid-based only (uniformly distributed CCPs)
- `1.0` = clusters only
- `0.5` = 50% mix (recommended for training)

**2. Fixed Mask Generation**

The original method used `np.sum` for overlapping Gaussians, creating bright "blobs" at overlap regions. The model then learned to detect blob centers instead of individual CCPs. Using `np.maximum` preserves individual peaks even when overlapping.

**3. Clustering Parameters**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `use_clusters` | `False` | Enable cluster mode |
| `cluster_sample_prob` | `0.5` | Probability of clustered sample |
| `cluster_prob` | `0.6` | Probability of forming cluster vs. isolated CCP |
| `cluster_size_range` | `(2, 6)` | Range of CCPs per cluster |
| `cluster_spread` | `8.0` | σ of Gaussian position distribution in cluster (px) |

For detailed information about the improved generator, see the README in the [HRNet/U-Net++ repository](https://github.com/gulierus/SU2_HR-net_U-net.git).

### Pretrained Models (SAM3)

**SAM3** was used as a pretrained model without additional training on our data.

### K-Fold Cross-Validation with Manual Annotations (StarDist)

For **StarDist**, we employed a different approach using newly annotated real data with k-fold cross-validation. This strategy helps maximize the use of limited annotated data while providing robust performance estimates.

## Results

Various detection-tracking combinations were evaluated. Specific numerical results will be presented during the project presentation. Through **non-standard approaches**, we achieved relatively good results for:

- **HRNet + LapTrack**
- **StarDist + LapTrack**

## References

1. **LapTrack:** Fukai, Y. T., Kawaguchi, K. (2022). LapTrack: Linear assignment particle tracking with tunable metrics. *Bioinformatics*. [https://github.com/yfukai/laptrack](https://github.com/yfukai/laptrack)

2. **btrack:** Ulicna, K., Vallardi, G., Charras, G., Lowe, A. R. (2021). Automated deep lineage tree analysis using a Bayesian single cell tracking approach. *Frontiers in Computer Science*. [https://github.com/quantumjot/btrack](https://github.com/quantumjot/btrack)

3. **SAM 2:** Ravi, N., et al. (2024). SAM 2: Segment Anything in Images and Videos. *Meta AI*. [https://github.com/facebookresearch/sam2](https://github.com/facebookresearch/sam2)

4. **HRNet:** Wang, J., et al. (2020). Deep High-Resolution Representation Learning for Visual Recognition. *IEEE TPAMI*. [https://github.com/HRNet](https://github.com/HRNet)

5. **StarDist:** Schmidt, U., Weigert, M., Broaddus, C., Myers, G. (2018). Cell Detection with Star-Convex Polygons. *MICCAI*. [https://github.com/stardist/stardist](https://github.com/stardist/stardist)

6. **UTIA Validation Data:** Institute of Information Theory and Automation, Czech Academy of Sciences. [https://su2.utia.cas.cz](https://su2.utia.cas.cz)
