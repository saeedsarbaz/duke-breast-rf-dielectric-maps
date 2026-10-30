# Sources and Terms

## Draft Status

No final license for this derived distribution has been selected on behalf of
the authors. This local preparation is not an authorization to publish or a grant
of unrestricted reuse rights. Confirm attribution, redistribution terms, and
institutional requirements before public release. Processing source images does
not by itself remove source restrictions.

## Upstream Resources

| Resource | Role | Primary reference / terms |
|---|---|---|
| Duke Breast Cancer MRI / TCIA | Clinical MRI and tumor-localization source | [Collection and data-use terms](https://www.cancerimagingarchive.net/collection/duke-breast-cancer-mri/); DOI 10.7937/TCIA.e3sv-re93 |
| Lew et al., 2024 | 100-case breast/FGT/vessel annotation resource | [Scientific Reports article](https://doi.org/10.1038/s41598-024-54048-2); confirm the annotation-distribution terms separately from article copyright |
| MAMA-MIA | Source expert tumor masks and model provenance | [Official repository](https://github.com/LidiaGarrucho/MAMA-MIA), [CC BY-NC 4.0 license](https://github.com/LidiaGarrucho/MAMA-MIA/blob/main/LICENSE), DOI 10.7303/syn60868042 |
| UWCEM / Zastrow and Lazebnik studies | Fat/FGT reference-property intervals | [Instruction manual](https://uwcem.ece.wisc.edu/MRIdatabase/InstructionManual.pdf) |
| Gabriel compilation | Dry-skin and muscle reference curves | [Appendix C](https://niremf.ifac.cnr.it/docs/DIELECTRIC/AppendixC.html) |
| Lazebnik et al., cancer-surgery study | Tumor median reference curve | [Publication](https://doi.org/10.1088/0031-9155/52/20/002) |

The Duke collection lists CC BY-NC 4.0 for its image/data resources. MAMA-MIA's
official repository also identifies CC BY-NC 4.0. These are non-commercial
source terms; this preparation does not relabel the data as MIT, CC0, or
unrestricted CC BY. The authors must determine the appropriate final notice for
the combined derived distribution and retain all required source citations.

The scientific articles cited here are not redistributed as part of the package.
Raw DICOM, upstream source archives, MAMA-MIA weights, and third-party library
code are not included. The in-house U-Net definition and six original fold
checkpoints are included at the authors' request. The authors and institution
must confirm the terms for those files, including applicable source-data and
annotation obligations. No separate model/code license is invented here.
The converted MRI and derived masks/property maps still require the source-term
review described above.

## Before Publication

1. Confirm permission and attribution for converted MRI, annotations, and derived maps.
2. Resolve the release-review items in `DATASET_REPORT.md` and select the frozen version.
3. Finalize the author list, institutional contact, and citation.
4. Select a data license consistent with applicable upstream terms.
5. Create the actual repository/release or archival record and replace draft status.
6. Publish the verified data, documentation and requested model supplement together,
   without internal audit files or the broader processing/training pipeline.

These notes record preparation decisions and source statements; they are not a
legal opinion or an institutional ethics determination.
