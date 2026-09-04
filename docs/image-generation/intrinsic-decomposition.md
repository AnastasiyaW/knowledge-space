---
title: Intrinsic Decomposition: Assumption and Review Contract
description: "Intrinsic decomposition is an ambiguity-bound estimate of reflectance and illumination, not ground truth; bind the image-formation assumptions, model and version, color domain, residual policy, source evidence, and task-specific review before using its albedo or shading outputs for editing or relighting."
category: techniques
tags: [intrinsic-decomposition, albedo, illumination, reflectance, shading, relighting, evidence]
aliases: ["Albedo and Illumination Separation", "Intrinsic Image Decomposition"]
---

# Intrinsic Decomposition: Assumption and Review Contract

Intrinsic decomposition estimates components such as reflectance (often called
albedo) and shading from an image. It is not a measurement of the material or
lighting in a photographed scene. In a simplified diffuse model, an observed
image can be expressed as `I ≈ R ⊙ S + E`, where `R` is reflectance, `S` is
illumination-dependent shading, and `E` absorbs effects the model does not
represent. Real images include specularity, transparency, subsurface
scattering, sensor processing, clipping, and mixed light. A single RGB image
usually does not uniquely determine these components.

## Declare the decomposition contract

For every output, retain:

- source asset digest, crop/orientation, color encoding, alpha policy, and
  whether the model sees linear, scene-referred, or display-referred values;
- exact model release, weights, runtime, prompt/reference inputs, and the
  image-formation assumptions the method documents;
- named outputs, their units/normalization, residual or confidence handling,
  and which pixels have no reliable estimate;
- intended operation, such as a lighting-only preview or a constrained
  recolor, plus protected content; and
- comparison source, numerical/reconstruction check where meaningful, and
  delivery-resolution visual review.

An albedo-like output from one method cannot be substituted for another
method's albedo, normal, material, or relighting input without an
implementation-specific compatibility test.

## Treat estimates as model-scoped

The task spans different observations and assumptions. For example,
[Intrinsic Scene Decomposition From RGB-D Images](https://openaccess.thecvf.com/content_iccv_2015/html/Hachama_Intrinsic_Scene_Decomposition_ICCV_2015_paper.html)
uses depth and a stated illumination model, while
[Intrinsic Image Transformation via Scale Space Decomposition](https://openaccess.thecvf.com/content_cvpr_2018/html/Cheng_Intrinsic_Image_Transformation_CVPR_2018_paper.html)
frames single-image outputs as learned image-to-image estimates. Those papers
do not establish that a named output is physically correct for arbitrary RGB
photographs, skin, products, transparent objects, or a later model release.

Select a method only after testing the exact release on representative images
and the downstream operation. Record failure cases such as hard shadows,
specular highlights, clipped lights, saturated colors, mixed illumination,
thin structures, and camera-processing artifacts.

## Use a constrained edit workflow

1. Verify that the source, rights, crop, color domain, and protected regions
   are within the job scope.
2. Produce the stated estimate and keep the source-to-output association.
3. Inspect the residual and ambiguity-prone regions before treating a value as
   reflectance or shading.
4. Apply only the approved change to explicit masks. A low-frequency or
   albedo-like layer is not permission to change every material or face pixel.
5. Recompose only with the model's declared routine. If a generated image,
   clipping, blend, or nonlinear step is involved, label the result as derived
   rather than exact reconstruction.
6. Review source versus result at delivery resolution for color drift, halos,
   shadow/material swaps, detail removal, geometry changes, and protected
   content.

Albedo-domain color transfer can be a useful experiment when illumination
confounds a color edit. It still needs a source-aware comparison and does not
prove that the target color is physically correct. Preserve a residual only
when the selected method defines it and the output contract says how it is
combined.

## Failure and release boundary

Do not silently replace an uncertain estimate with a different model, add
generated texture, or present a relit result as recovered source data. Return
a visible review or failure state when assumptions are unknown, the runtime
cannot reproduce the declared output, the residual is unexplained, or review
finds a protected-content change.

## Related pages

- [[color-space-and-gamma-reference]]
- [[color-checker-and-white-balance]]
- [[frequency-decomposition-editing]]
- [[tiled-inference]]
