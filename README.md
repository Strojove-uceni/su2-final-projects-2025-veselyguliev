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


**Trainig:** `UnetPlusPlus_showcase.ipynb`

**Author:** Ruslan Guliev

### HRNet (High-Resolution Network)

HRNet maintains high-resolution representations throughout the network by connecting multi-resolution subnetworks in parallel. Unlike traditional approaches that recover high resolution from low resolution, HRNet preserves spatial precision, making it well-suited for detecting small biological structures.

HRNet proved to be a better alternative to U-Net++ in our experiments and was subsequently trained on larger datasets. The notebook includes loading of a pretrained model trained on 3000 synthetic samples + 2000 fine-tuning samples over 50 epochs.

| HOTA | DetA | AssA |
|------|------|------|
| 0.7272 | 0.7590 | 0.6967 |

This represents our best result achieved so far with a relatively small synthetic dataset of 5000 samples. The performance was additionally affected by the fine-tuning phase, which introduced some noise and error into the model. We belief that with bigger computation capacities the result could be even better.

**Inference:** `HRnet_showcase.ipynb`

**Repository:** [https://github.com/gulierus/SU2_HR-net_U-net.git](https://github.com/gulierus/SU2_HR-net_U-net.git)

**Author:** Ruslan Guliev

### SAM3 (Segment Anything Model 3)

SAM3 is a pretrained foundation model for image segmentation. We used SAM3 directly without additional training, only combining it with tracking methods to evaluate its out-of-the-box performance on CCP detection.

**HITL annotated data using SAM3:**  [https://github.com/veselm73/SU2/tree/main/annotation/sam_data/unet_train](https://github.com/veselm73/SU2/tree/main/annotation/sam_data/unet_train)

**Author:** Matyáš Veselý

### StarDist

StarDist is a deep learning method originally designed for star-convex object detection in microscopy images. It predicts object boundaries using radial distances from object centers, making it effective for detecting roughly circular structures. StarDist is particularly robust for overlapping objects.

**Trainig:** `SU2_StarDist_final.ipynb`

**Inference:** `SU2_StarDist_inference.ipynb`

**Repository:** [https://github.com/veselm73/SU2.git](https://github.com/veselm73/SU2.git)

**Author:** Matyáš Veselý


## Tracking Methods

### LapTrack (v0.17.0)

LapTrack is a tracking algorithm based on the Linear Assignment Problem (LAP) formulation. It solves the frame-to-frame linking problem by minimizing a global cost function that considers spatial distances between detections. LapTrack is well-suited for particle tracking scenarios where objects do not divide.

**Benchmark on GT data:** `tracking_benchmark_laptrack_gt_3.ipynb`

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

For **StarDist**, we employed a different approach using k-fold cross-validation on validation data with bonus data annotated by hand with SAM3 HITL workflow using label-studio. This strategy helps maximize the use of limited annotated data while providing robust performance estimates.

For detailed information see [veselm73/SU2](https://github.com/gulierus/SU2_HR-net_U-net.git).

## Results

Various detection-tracking combinations were evaluated. Specific numerical results will be presented during the project presentation. Through **non-standard approaches**, we achieved very good results for:

- **HRNet + LapTrack**
- **StarDist + LapTrack**

  
## BEST RESULT

  ### StarDist with K-Fold Cross-Validation

  Our best performing approach uses **StarDist** trained on K-fold cross-validation with SAM3 Human-in-the-Loop annotated data.

  #### Detection Performance

  | Metric | Value | Evaluation Method |
  |--------|-------|-------------------|
  | **DetA (OOF)** | **0.8129 ± 0.0224** | Out-of-fold |
  | Best Single Fold | 0.8286 | Fold 5 |
  | Worst Single Fold | 0.7691 | Fold 2 |

  *All metrics computed with fixed threshold (prob=0.5, nms=0.3) and 5px matching distance.*

  **Best tracker configuration has been found on GT data.


## References

1. **LapTrack:** Fukai, Y. T., Kawaguchi, K. (2022). LapTrack: Linear assignment particle tracking with tunable metrics. *Bioinformatics*. [https://github.com/yfukai/laptrack](https://github.com/yfukai/laptrack)

2. **btrack:** Ulicna, K., Vallardi, G., Charras, G., Lowe, A. R. (2021). Automated deep lineage tree analysis using a Bayesian single cell tracking approach. *Frontiers in Computer Science*. [https://github.com/quantumjot/btrack](https://github.com/quantumjot/btrack)

3. **SAM 3:** Carion, N., et al. (2025). SAM 3: Segment Anything with Concepts. *Meta AI*. [https://github.com/facebookresearch/sam3](https://github.com/facebookresearch/sam3)

4. **HRNet:** Wang, J., et al. (2020). Deep High-Resolution Representation Learning for Visual Recognition. *IEEE TPAMI*. [https://github.com/HRNet](https://github.com/HRNet)

5. **StarDist:** Schmidt, U., Weigert, M., Broaddus, C., Myers, G. (2018). Cell Detection with Star-Convex Polygons. *MICCAI*. [https://github.com/stardist/stardist](https://github.com/stardist/stardist)

6. **UTIA Validation Data:** Institute of Information Theory and Automation, Czech Academy of Sciences. [https://su2.utia.cas.cz](https://su2.utia.cas.cz)

7. **Label Studio:** Tkachenko, M., et al. (2020). Label Studio: Data labeling software. *Heartex*. [https://github.com/HumanSignal/label-studio](https://github.com/HumanSignal/label-studio)
