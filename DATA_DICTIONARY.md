# Data Dictionary

FGT denotes fibroglandular tissue; ROI denotes region of interest.

## Files in Each Case

Paths below are relative to `cases/Breast_MRI_NNN/` after extraction.

| File | Meaning |
|---|---|
| `mri_reference.nii.gz` | MRI reference image aligned with the released masks; intensities have arbitrary MRI units |
| `t1_reference.nii.gz` | MRI used for intensity-based fat/FGT subdivision on the final grid |
| `simple_label_mask.nii.gz` | Five-tissue anatomical label map; background is zero |
| `detailed_label_map.nii.gz` | Fat/FGT subdivisions plus skin, muscle, and tumor; uses signed label values |
| `roi_mask.nii.gz` | Binary complete modeled material region, including posterior muscle |
| `fat_mask.nii.gz` | Binary fat mask |
| `fibro_mask.nii.gz` | Binary FGT mask; historical filename retained |
| `skin_mask.nii.gz` | Binary constructed skin mask |
| `muscle_mask.nii.gz` | Binary posterior-muscle mask |
| `tumor_mask.nii.gz` | Binary final tumor mask for the case |
| `t1_composition_rank_map.nii.gz` | Intensity-ordering coordinate used for tissue subdivision; not fat fraction |
| `pval_map.nii.gz` | Within-detailed-class property coordinate used for dielectric interpolation |
| `Breast_MRI_NNN_epsr_0.915GHz.nii.gz` | Relative permittivity at 0.915 GHz; dimensionless |
| `Breast_MRI_NNN_epsr_2.45GHz.nii.gz` | Relative permittivity at 2.45 GHz; dimensionless |
| `Breast_MRI_NNN_epsr_6GHz.nii.gz` | Relative permittivity at 6 GHz; dimensionless |
| `Breast_MRI_NNN_sigma_0.915GHz.nii.gz` | Conductivity at 0.915 GHz, in S/m |
| `Breast_MRI_NNN_sigma_2.45GHz.nii.gz` | Conductivity at 2.45 GHz, in S/m |
| `Breast_MRI_NNN_sigma_6GHz.nii.gz` | Conductivity at 6 GHz, in S/m |

All files of a case describe the same physical grid. Different cases have
different array dimensions, coverage, and origins. Preserve each file's affine
transform; an array axis is not automatically a particular anatomical direction.

## Anatomical Labels

| Value | Tissue |
|---|---|
| 0 | Background |
| 1 | Fat |
| 2 | FGT |
| 3 | Skin |
| 4 | Posterior muscle |
| 5 | Tumor |

## Detailed Labels

| Value | Class |
|---|---|
| -3 | Tumor |
| -2 | Skin |
| -1 | Posterior muscle |
| 0 | Background |
| 1 | FGT low |
| 2 | FGT median |
| 3 | FGT high |
| 5 | Fat low |
| 6 | Fat median |
| 7 | Fat high |

Detailed label 4 is not used. In particular, it is not a transition-tissue label.
Keep detailed labels signed; converting negative values to unsigned integers
without explicit remapping changes their meanings. The names low, median, and
high refer to ordered modeling classes, not histological tissue subtypes.

## Background and Coordinates

Zero property values outside `roi_mask.nii.gz` indicate unassigned space, not a
physical material with zero relative permittivity. Define the outside material
for the intended simulation. MRI intensities are not dielectric values.

Property coordinates range from 0 to 1 in the modeled fat/FGT subdivisions.
The detailed label selects the appropriate interval before the coordinate is
used. A coordinate by itself does not identify fat, FGT, or a physical composition.
Skin, muscle, and tumor use their fixed tissue curves rather than this interpolation.

## Metadata

- `cases.csv`: case identifier, provenance tier, tumor-mask source, array dimensions,
  and recorded MRI-input/support flags. Empty flags mean unavailable information.
- `files.csv`: portable relative path, compressed size, SHA-256, dimensions, type,
  spatial units, axis codes, coordinate-field codes, and archive membership.
- `archive_parts.csv`: archive filename, case/file counts, size, checksum, and case range.
- `dielectric_models.json`: curve coefficients, parameter units, interval mapping,
  and source references. It contains data, not executable generation code.
- `release_manifest.json`: scope, preparation date, verification results, and
  pending publication decisions. Packaging checks are distinct from scientific validation.

## Model Supplement

`models/compact_25d_unet/model.py` defines the seven-channel U-Net and a checkpoint
loader. The `checkpoints` directory holds the six original `fold_N_model.pth`
files. They contain state dictionaries and fold/input metadata, not the final
patient masks; those masks remain in the case archives. The model's
`manifest.json` records weights, checksums, training/held-out identifiers, input
order and processing settings. See its README for loading and fold-use details.
