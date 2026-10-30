# Data Set Report

## Purpose and Coverage

The resource provides 100 bilateral, tumor-bearing breast models derived from
magnetic resonance imaging (MRI) for electromagnetic research. It brings MRI, tissue labels, and assigned dielectric
maps together on a common grid within each case, reducing the need to prepare
individual breast models again from the source MRI. The complete distribution
contains 1800 compressed NIfTI volumes. Exact file sizes, hashes, dimensions, and
archive membership are recorded in `metadata/files.csv` and
`metadata/release_manifest.json`.

| Item | Content |
|---|---|
| Cases | 100 Duke breast MRI cases |
| Tier A | 36 cases with source expert tumor masks |
| Tier B | 64 cases with generated tumor masks |
| Tier-B sources | 24 accepted MAMA-MIA predictions; 40 in-house U-Net ensemble masks |
| Anatomical tissues | Fat, FGT, skin, posterior muscle, tumor |
| Detailed subdivisions | Low, median, and high classes within fat and within FGT |
| Voxel spacing | 1 x 1 x 1 mm; array dimensions remain case-specific |
| Supplied frequencies | 0.915, 2.45, and 6 GHz |
| Additional-frequency representation | Detailed labels, property coordinates, and Cole-Cole parameters |
| Parameter evaluation band | 0.5-20 GHz |
| Format | Gzip-compressed NIfTI, with millimetre spatial units |
| Release contents | Data, documentation, in-house 2.5-D U-Net definition and six fold checkpoints |

## Generation Story

FGT denotes fibroglandular tissue throughout this report.

The starting population was the 100-case annotation subset supplied by Lew et al.
from the Duke Breast Cancer MRI collection. The released breast, FGT, and vessel
annotations supplied the source tissue masks; the Lew segmentation model was not
used to predict those masks. For the 36 cases shared with MAMA-MIA, source expert
tumor masks were retained after the project's spatial review. For the remaining
64 cases, MAMA-MIA predictions were checked against the Duke tumor boxes and MRI
overlays. Twenty-four predictions passed these checks. An in-house 2.5-D U-Net,
trained using the 36 expert-mask cases, supplied the replacement masks for the
other 40 cases; probabilities from its six training folds were averaged for
these cases. The tumor-mask source for every case is preserved in
`metadata/cases.csv`.

The model definition and original checkpoints are supplied in
`models/compact_25d_unet/`. Each checkpoint matches the recorded training-fold
hash and loads into the released architecture with an exact tensor match.
The fold manifest records the 30 training and six held-out cases for each fold.
No training, fine-tuning, or new patient predictions were performed for this
addition; the 1800 data volumes and their archives are unchanged.

DICOM acquisition geometry was used to establish physical alignment before
transferring MRI and masks to case-specific grids with 1-mm voxels. The source
breast and FGT regions were assembled with tumor labels, a nominal 1.5-mm skin
shell with posterior cut-face cleanup, and a constructed posterior-muscle region.
Bias-corrected T1-based intensity ordering was used to subdivide fat and FGT
separately into low, median, and high classes while retaining their anatomical
boundaries. Published frequency-dependent tissue curves and the stored
within-class coordinates supplied the relative permittivity and conductivity
values. The resulting maps were exported at the three supplied frequencies, with
the labels and coordinates retained for additional-frequency calculations.

## What Is Supplied

The anatomical label map describes the modeled tissue compartments. Its binary
masks provide each tissue and the complete material region separately. The
detailed map subdivides only fat and FGT; skin, posterior muscle, and tumor retain
their tissue classes. The property-coordinate volume specifies a voxel's relative
position within the dielectric interval assigned to its detailed class.

Skin uses the dry-skin curve, posterior muscle uses the muscle curve, and tumor
uses the 50th-percentile malignant-tissue curve. These respective
frequency-dependent curves are shared by all cases. Their assigned values
therefore change with frequency but are identical across cases at each frequency.
Fat and FGT retain spatially
varying assigned properties. There is no separate transition class between fat
and FGT in this version.

## Technical Packaging Checks

The preparation checks all 1800 core-volume headers for case-level shape and
affine agreement, millimetre units, 1-mm spacing, and matching qform/sform fields.
Every source file is compared with its previously recorded SHA-256 while being
copied into an archive. Every archive member is then read back and its SHA-256
is checked independently against that record; ZIP readback also checks CRC.
The source volumes are not resampled, renamed internally, or overwritten.

An additional content audit read all 1800 archived volumes. All 600 binary masks
matched the anatomical labels, the complete ROI matched their union, and every
detailed class remained within its parent tissue. The stored ordering and
property coordinates were finite and within [0, 1]. Tissue counts, physical
volumes, and fractions matched all 1100 case/tissue composition records used for
the manuscript. Means, standard deviations, minima, and maxima matched all 6600
case/frequency/property/tissue summary records; the archived whole-ROI means
also matched all 6600 baseline entries in the existing sensitivity records.

All 600 dielectric maps were independently checked using the supplied curve
parameters, detailed labels, and property coordinates. The largest absolute
differences from the double-precision calculation were approximately
3.815 x 10^-6 for relative permittivity and 2.3842 x 10^-7 S/m for conductivity,
consistent with float32 storage. The 11 coefficient sets matched the verified
parameter record. The 212 numeric cells in the current manuscript's reference
curve, tissue-composition, dielectric-summary, and anatomical-sensitivity tables
matched at their printed precision. Existing sensitivity results were summarized
again, but perturbation maps were not regenerated for this audit.

Tumor-box checks preserved the source distinction: all 24 accepted MAMA-MIA
masks overlapped their Duke boxes and had centroids inside, and all 40 U-Net
ensemble masks were fully inside their boxes. The 36 source expert masks were
retained without enforcing box containment. The case-level source labels and
MRI-input flags matched the final manuscript evidence records.

These checks establish file integrity and packaging consistency. They do not
constitute a new anatomical review or an independent assessment of dielectric
accuracy. The limited NIfTI text-header check is not a clinical de-identification
certification.

## Interpretation and Review Notes

- The 1-mm grid standardizes sampling; it does not increase acquired MRI resolution.
- Skin and posterior muscle are constructed modeling compartments, not independent
  expert tissue-thickness measurements.
- Generated Tier-B tumor masks have different provenance from the 36 expert masks.
  The release does not assign an unsupported expert-overlap accuracy to all 100 cases.
- The T1 ordering and property coordinates are modeling coordinates, not quantitative
  fat-fraction or patient-specific dielectric measurements.
- MRI inputs vary across cases. The six dynamic-reference fallback cases and cases
  with reduced positive/finite T1 support remain identifiable in the case metadata.
- Earlier project review identified unresolved source/preprocessing questions about
  normalized fallback intensities and the source FGT grid of Breast_MRI_246.
  This packaging preserves the existing data and does not claim those questions
  were resolved. The authors must adjudicate them before public release.
- Some cases used combined FGT/vessel annotations and others FGT-only annotations;
  this release retains that existing tissue-label policy.

## Publication Status

This is a local preparation of the current 100-case data snapshot. It is not a
newly corrected data set, a journal submission, or a public deposit. Author and
institutional sign-off, final source-term review, citation metadata, and a public
release destination remain to be confirmed. Apart from the requested model
definition and loader, the broader processing/training code is not included.
