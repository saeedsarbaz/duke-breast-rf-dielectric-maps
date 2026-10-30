# Usage Guide

## 1. Obtain and Extract Cases

Download the required ZIP parts and `SHA256SUMS.txt` from the eventual data
release. Consult `metadata/archive_parts.csv` to find the part containing a case.
Each part is a complete, ordinary ZIP archive, not a segment of a split ZIP.
Extract selected parts into the same destination, or extract all parts to obtain
all 100 case folders. No case spans multiple archives.

Check each archive's SHA-256 with a checksum utility against `SHA256SUMS.txt`.
An archive test checks ZIP integrity but does not replace the SHA-256 comparison.
Keep a clean copy of the extracted data and save derived work elsewhere.

## 2. Inspect Anatomy in 3D Slicer

3D Slicer is a medical-image visualization and segmentation application that
can display the NIfTI images and tissue masks together.

1. Open 3D Slicer and choose **File > Add Data**.
2. Add `mri_reference.nii.gz` as a scalar volume.
3. Add `simple_label_mask.nii.gz`; enable **Show Options** and **LabelMap**, or
   select **Segmentation** in the Description column for direct NIfTI import.
4. Display the MRI as the background and the label map/segmentation as the overlay.
5. Inspect axial, sagittal, and coronal views. Use the anatomical-label table in
   `DATA_DICTIONARY.md` to name the tissues rather than relying on default colors.
6. Adjust opacity to compare tissue placement with MRI. Do not apply independent
   rotations, flips, or spacing changes to one file.

Individual binary masks can be loaded in the same way. For a first review, the
simple map and individual masks are the easiest choices. The detailed map uses
signed codes, including negative skin/muscle/tumor values; default color tables
may not supply the intended tissue names. Load the detailed map as a scalar
volume to inspect its signed values. Preserve the original values and use
the detailed-label dictionary when assigning names or display colors.

These are standard Slicer import instructions, not a bundled scene or an
interactive test of every case in a particular Slicer installation. See the
[Volumes documentation](https://slicer.readthedocs.io/en/latest/user_guide/modules/volumes.html)
and [Segmentation import documentation](https://slicer.readthedocs.io/en/latest/user_guide/modules/segmentations.html).

## 3. Inspect Dielectric Maps

Load a permittivity or conductivity NIfTI as a scalar volume and display it in
the same views as the MRI. Use the same display range when comparing frequencies.
Relative permittivity is dimensionless; conductivity is in S/m. The values inside
the material ROI are physical property assignments, not normalized MRI intensities.

A logarithmic display can make differences within fat more visible. This is a
display choice only: do not replace the stored values by their logarithms.
Mask background zero values before applying a logarithmic color scale.

## 4. Use in Electromagnetic Simulations

Select the supplied frequency appropriate to the intended study. Import the
permittivity and conductivity fields using the NIfTI physical coordinates and
millimetre-to-simulator unit conversion. Use `roi_mask.nii.gz` to distinguish
the modeled tissue region from unassigned background. Assign the surrounding
air or coupling medium explicitly; background zeros are not an air model.

The simple map supplies tissue identities when a simulator also needs thermal,
density, or other material parameters. Those parameters, applicator geometry,
excitation, meshes, boundary conditions, and perfusion are not supplied here.
The data set does not contain SAR solutions, temperature predictions, or
patient-specific treatment plans.

If another simulation grid is required, transfer categorical labels with
nearest-neighbor sampling. Treat continuous-property transfer as a separate
modeling decision and check the consequences at small structures and tissue
interfaces. Always keep images, labels, and properties in one physical frame.

## 5. Calculate Maps at Another Frequency

The distribution does not include the dielectric-map generation program. It supplies the detailed
labels, the voxelwise coordinate p, and the parameter tables needed to implement
the documented assignment at frequencies within 0.5-20 GHz. Prefer the supplied
maps when the required frequency is already available.

For frequency f in hertz, let omega = 2 pi f. Evaluate each tissue's complex
relative permittivity using the parameters in `metadata/dielectric_models.json`:

$$
\varepsilon_r^*(\omega)=\varepsilon_\infty+
\sum_n\frac{\Delta\varepsilon_n}{1+(j\omega\tau_n)^{1-\alpha_n}}
+\frac{\sigma_s}{j\omega\varepsilon_0}.
$$

Relative permittivity and conductivity follow from

$$
\varepsilon_r=\operatorname{Re}(\varepsilon_r^*),\qquad
\sigma=-\omega\varepsilon_0\operatorname{Im}(\varepsilon_r^*).
$$

Conductivity sigma and static conductivity sigma_s are in S/m; relaxation times
are in seconds. The JSON records epsilon_0 in F/m. The sign convention above
must be retained when converting the imaginary part into conductivity.

For a fat/FGT voxel, its detailed label l selects lower and upper curves. For
either property q, the assigned value is

$$q(\mathbf{x},f)=[1-p(\mathbf{x})]q_l^-(f)+p(\mathbf{x})q_l^+(f).$$

The JSON's `detailed_label_bounds` lists those endpoint curves. Evaluate skin,
muscle, and tumor from their respective fixed curves, using `fixed_label_curves`.
The baseline uses dry skin and the 50th-percentile malignant-tissue tumor curve.
Do not use p to introduce heterogeneity into those tissues. Keep the original
grid, assign background outside the ROI separately, and verify an implementation
against the provided 0.915-, 2.45-, and 6-GHz maps before generating other values.

## 6. Cite and Interpret the Data

Preserve case identifiers and cite both this work, once its citation is final,
and the upstream image/annotation resources. Tumor-mask provenance is recorded
per case: do not describe every mask as an expert annotation. Consult the report
for constructed-tissue, MRI-intensity, and pending review limitations, and the
terms document before reuse or redistribution.

## 7. Reuse the 2.5-D U-Net

The [model guide](models/compact_25d_unet/README.md) describes the included
architecture and six original fold checkpoints. It specifies channel order,
crop normalization, loading, fold membership, and probability postprocessing.
The model uses original-grid, Duke-box crops; the final 1-mm simulation volumes
are not the original training inputs. The model guide identifies the additional
source MRI/localization inputs required. The original checkpoints were verified
and copied without retraining or rerunning patient predictions.
