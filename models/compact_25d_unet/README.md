# In-House 2.5-D U-Net

This folder contains the model definition and the six original fold checkpoints
used to generate the 40 U-Net tumor masks in Tier B. It is one architecture
trained in six folds, not six different architectures. No checkpoint was retrained,
fine-tuned, or reserialized for this release. The 36 Tier-A release masks remain
the source expert masks, not predictions from this model.

## Contents

- `model.py`: the PyTorch `ConvBlock` and `SmallUNet` definitions, plus a loader.
- `checkpoints/fold_1_model.pth` through `fold_6_model.pth`: original checkpoints.
- `manifest.json`: checkpoint SHA-256 values, training/held-out case lists,
  architecture, input order, training settings, and deployment procedure.
- `requirements.txt`: the model-loading dependency, without training dependencies.

Each checkpoint contains `state_dict`, `fold`, `train_cases`, `input_channels`,
and `out_size`. The files include weights and batch-normalization buffers, but
not an optimizer state or a serialized custom Python model object.

## Architecture and Inputs

The two-level encoder uses 24, 48, and 96 feature channels. Each convolution block
contains two 3 x 3 convolutions with batch normalization and ReLU. Two 2 x 2
max-pooling operations reduce resolution; transposed convolutions and skip
concatenations restore it. The final 1 x 1 convolution produces one logit channel.
Apply a sigmoid to obtain probabilities; `model.py` returns logits, not probabilities.

The input tensor shape is `[batch, 7, 128, 128]`, with this channel order:

| Channel | Image slice |
|---|---|
| 0 | Reference MRI at z-1 |
| 1 | Reference MRI at z |
| 2 | Reference MRI at z+1 |
| 3 | First-postcontrast minus precontrast MRI at z-1 |
| 4 | First-postcontrast minus precontrast MRI at z |
| 5 | First-postcontrast minus precontrast MRI at z+1 |
| 6 | Binary anatomical ROI at z, including breast, skin and posterior muscle |

Inputs were prepared on the original MRI-reference grid and cropped to the
case's audited Duke tumor box. The precontrast image was aligned to the first
postcontrast image before subtraction. MRI and subtraction crops were normalized
separately: clip at the first/99th percentiles, subtract the crop median, and
divide by its interquartile range divided by 1.349. If that scale was at most
1e-6, the crop standard deviation plus 1e-6 was used. All input channels were
resized bilinearly to 128 x 128 with `align_corners=False`. Neighbor indices
outside the crop's slice range repeated the nearest edge slice.

The released 1-mm volumes are the final simulation data, not the original
training crops. Separate precontrast/first-postcontrast volumes and native-grid
tumor boxes are not bundled here. Preparing new model inputs therefore also
requires the original image/localization resources and the alignment described
in the paper; this folder is not an end-to-end DICOM prediction program.

## Load a Fold

Use a maintained PyTorch release, version 2.6 or later. This minimum excludes the
older checkpoint-loading vulnerability described in the
[official PyTorch advisory](https://github.com/pytorch/pytorch/security/advisories/GHSA-53q9-r3pm-6pq6).
Verify downloaded checkpoints against `manifest.json` or the release checksum
catalog before loading; load only trusted files.

Run from this folder in a Python environment with PyTorch installed:

```python
from model import load_fold_checkpoint

model = load_fold_checkpoint("checkpoints/fold_1_model.pth", device="cpu")
```

The loader uses `weights_only=True`, requires an exact state-dictionary match,
and sets evaluation mode. Importing the module or loading weights does not
perform inference. CPU is the default; CUDA is used only if explicitly requested.

## Fold Use and Output Processing

Each fold used 30 training cases and six held-out cases from the same 36-case
development set. To evaluate a Tier-A case without training overlap, use only
the checkpoint for which `manifest.json` lists that case as held out. Averaging
all six folds for those cases is not a held-out evaluation.

For the 40 deployment cases, each fold's sigmoid probabilities were resized to
the original crop size using bilinear interpolation, restricted to the binary
ROI, and averaged voxelwise. The average was thresholded at 0.5, the largest
3-D connected component was retained, and the crop was placed back on the full
MRI grid for review. The original component selection used SciPy's default
3-D connectivity (six face-connected neighbors). No model predictions were
regenerated while preparing this model release.

The checkpoints were hash-checked against the existing fold audit, loaded on CPU,
and checked for exact architecture/tensor compatibility. The author/institutional
license and publication decisions in [Sources and Terms](../../SOURCES_AND_TERMS.md)
also apply to this locally prepared model supplement. MAMA-MIA weights, the
complete training pipeline, and the broader data-processing code are not included.
