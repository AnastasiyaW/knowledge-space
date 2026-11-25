---
title: Color Checker and White Balance Correction
description: Color checker and white-balance correction requires a measured physical chart or a separately validated estimator; detector output and a generated checker are not colorimetric ground truth.
category: techniques
tags: [color-checker, white-balance, color-constancy, calibration, illumination, product-photography]
aliases: ["Color Constancy", "White Balance"]
---

# Color Checker and White Balance Correction

White balance and color correction solve related but different problems. White
balance estimates or neutralizes the illuminant; a color transform maps a
particular capture/rendering response to a defined reference. Neither becomes
reliable merely because a chart-shaped object was detected in an image.

## Decide what counts as a reference

Use one of these evidence paths and record which one was used:

1. **Measured physical chart.** Capture a known chart in the same lighting and
   optical path as the subject. Read its patches from an un-clipped, correctly
   exposed capture and compare them with the chart's reference values.
2. **Separately validated estimator.** A learned white-balance or illumination
   estimator may be useful when a physical chart is absent, but it needs
   validation on the target camera, render path, materials, and lighting. Its
   output is an estimate, not a measurement.

For jewelry and product work, retain the source capture, chart identity,
illuminant/setup, render transform, and validation samples. A pleasing result
is not enough evidence that metal or gemstone colors are accurate.

## Physical-chart workflow

1. Photograph the chart under the capture lighting without clipping highlights
   or changing the exposure/lighting between reference and product frames.
2. Locate the chart, order its patches, and reject frames with glare, blur,
   occlusion, extreme perspective, or uncertain patch correspondence.
3. Derive the transform in the declared working space and apply it only to
   captures governed by that calibration contract.
4. Validate on held-out neutral, skin, product, or material patches chosen for
   the actual deliverable. Inspect both numerical error and the rendered image.
5. Version the transform with the camera profile, lens/lighting setup, raw
   converter, and validation receipt. Recalibrate after a material setup or
   rendering-pipeline change.

The transformation should not silently combine white balance, camera profile,
tone mapping, and creative grading. Keep those operations explicit so a later
review can reproduce the result.

## Detection is only localization

[Colour Checker Detection](https://github.com/colour-science/colour-checker-detection)
implements segmentation, templated, and machine-learning approaches. Its
published YOLOv8 model is trained for ColorChecker Classic 24 and is not a
general detector for Nano or SG charts. The repository also documents
licensing differences for the inference path that uses the Ultralytics API.

Accordingly, pin the detector version, chart type, and inference dependency,
then verify its patch ordering and crop quality on the real capture set.
Detection can find a candidate chart; it does not validate chart condition,
lighting equivalence, exposure, or colorimetry.

## Learned and generative estimators

[Deep White Balance](https://github.com/mahmoudnafifi/Deep_White_Balance)
is a research implementation for learned white-balance correction of rendered
images. It can be evaluated as an estimator, but its training data and
rendering assumptions need to be compared with the local capture pipeline.

Generative Color Constancy (GCC) is a different research direction: its
[paper](https://arxiv.org/abs/2502.17435) uses deterministic inpainting to
place a virtual color checker that reflects an estimated scene illumination.
That is useful for studying illumination estimation, not for turning generated
patch values into a measured target. A generated checker must stay labeled as
a model estimate and must never replace a physical reference in a
colorimetric acceptance test.

## Minimal acceptance record

For every calibrated batch, retain:

- capture and chart identifiers, source digest, and declared color space;
- detector/estimator revision and all transform parameters;
- rejected frames with a reason;
- held-out validation images and the pass/fail criterion; and
- the reviewer or automated job that approved release.

This makes color correction auditable when a camera, lighting rig, model, or
raw-processing pipeline later changes.

## Related pages

- [[color-correction-by-numbers]]
- [[color-space-and-gamma-reference]]
- [[diffusion-inference-acceleration]]
