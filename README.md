# An MRI-Derived Data Set of 100 Tumor-Bearing Breast Models with Frequency-Dependent Dielectric Maps

This distribution contains 100 bilateral breast models derived from
Duke breast magnetic resonance imaging (MRI). Each case includes aligned MRI, anatomical tissue masks,
detailed fat and fibroglandular tissue (FGT) labels, property coordinates, and
relative permittivity and conductivity maps at 0.915, 2.45, and 6 GHz.
The in-house 2.5-D U-Net definition and its six original fold checkpoints are
included in [the model folder](models/compact_25d_unet/README.md). The broader
processing/training pipeline, MAMA-MIA weights, and raw DICOM are not included.

**Status: locally prepared draft for author review, not a published release.**
The authors must confirm the release version, source terms, citation, and
remaining review items before making the data public. See
[Sources and Terms](SOURCES_AND_TERMS.md) and the review notes in the report.

## Start Here

1. Read the [Data Set Report](DATASET_REPORT.md) for its origin and generation story.
2. Read the [Usage Guide](USAGE_GUIDE.md) for extraction, visualization, and simulation use.
3. Use the [Data Dictionary](DATA_DICTIONARY.md) to interpret filenames and label values.
4. Select cases using [metadata/cases.csv](metadata/cases.csv).
5. Check the archive list in [metadata/archive_parts.csv](metadata/archive_parts.csv)
   and verify downloaded files against `SHA256SUMS.txt`.

## Contents

- 100 cases; 18 compressed NIfTI volumes per case, 1800 volumes in total.
- 36 cases with source expert tumor masks.
- 24 cases with accepted MAMA-MIA predictions and 40 cases with accepted
  in-house 2.5-D U-Net ensemble masks.
- 1 x 1 x 1 mm voxels, with case-specific array dimensions and physical coordinates.
- Dimensionless relative permittivity and conductivity in S/m.
- Stored property coordinates and literature-model parameters for calculating
  additional maps within the adopted 0.5-20 GHz band, as described in the guide.
- One 2.5-D U-Net architecture and six original fold checkpoints, with input,
  loading, and fold-use instructions. See the model manifest for checksums and splits.

## GitHub Layout

Place these Markdown documents and the `metadata` and `models` directories in the repository.
Distribute `GT100_data_part_*.zip` as **GitHub Release assets**, not ordinary Git
files. Some individual volumes exceed GitHub's regular-file limit. The supplied
ZIP parts are independent archives, each below 2 GiB; download the parts containing
the required cases, or all parts for the complete data set.

Extract every selected part into the same destination. They share a `cases`
directory and do not require concatenation. No case is divided between parts.
See [GitHub's large-file guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

An institutional repository or DOI-bearing data archive can also host the same
verified ZIP parts. No public URL, DOI, author list, or final data license has
been fabricated in this preparation.

## Scope

The dielectric values are assigned from published models. The provided maps are
inputs for research simulations, not patient-specific electrical measurements or
clinical treatment plans. Image conversion, constructed anatomy, and MRI-derived
tissue subdivision have the limitations described in the report.

For citations and upstream attribution, see [CITATION.md](CITATION.md).
