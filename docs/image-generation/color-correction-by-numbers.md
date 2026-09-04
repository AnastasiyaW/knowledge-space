---
title: Color Correction: Measurement-Bound Calibration Contract
description: "Color correction is valid only against a declared measurement target, illuminant, camera or profile, working space, and viewing transform; neutral samples and chart patches are evidence when their provenance is known, while scene averages and skin-color ratios are not universal ground truth."
category: techniques
tags: [color-correction, white-balance, color-checker, calibration, profiles, evaluation]
aliases: ["Color Correction by Numbers", "White Balance Measurement"]
---

# Color Correction: Measurement-Bound Calibration Contract

Numerical correction is defensible when numbers are tied to a declared
measurement target and color-management path. Pixel averages, a scene-wide
RGB ratio, or a presumed skin-color rule do not establish an illuminant,
reflectance, camera response, or intended creative grade.

## Start with a correction target

Choose one of these explicit purposes before changing pixels:

| Purpose | Required evidence |
|---|---|
| Capture calibration | a known target, capture conditions, input transform, and measured reference values for that target |
| Cross-camera matching | approved reference shots, both camera transforms, viewing conditions, and reviewer acceptance |
| Editorial grade | an authored target/look and approval policy, not a claim of physical neutrality |
| Automated proposal | a bounded estimate with confidence and review, not an automatic truth label |

[Calibrite's ColorChecker White Balance target](https://calibrite.com/us/product/colorchecker-white-balance/?noredirect=en-US)
is designed as a spectrally neutral reference for custom white balance. That
supports a measurement workflow when the actual target is visible and
traceable; it does not make an arbitrary wall, clipped highlight, or image
average a universal neutral reference.

## Bind the measurement

For each correction, retain:

- target type, revision, ownership, position in the scene, and target-region
  mask;
- illuminant/capture conditions, camera settings, raw decoder or input
  profile, and any in-camera processing;
- source encoding, linearization policy, working space, transform versions,
  and output/view transform;
- measured patch or neutral values with their sampling method; and
- proposed transform, clipping/gamut behavior, reviewer decision, and output
  digest.

Known chart values depend on the chart, illuminant, measurement geometry, and
encoding. Do not hard-code one table of RGB values across raw, scene-linear,
display-referred, or differently profiled images.

## Use a managed transform path

The [ICC profile guide](https://www.color.org/getting-started/) explains that
device profiles connect through a defined Profile Connection Space. An RGB
triplet names device channels until its encoding and profile are known.
[OpenColorIO](https://opencolorio.readthedocs.io/en/latest/guides/authoring/authoring.html)
likewise treats colorspaces and display views as explicit configuration
objects. Apply a correction in a declared path and validate that path rather
than assuming a blend mode or channel curve isolates luminance in every
encoding.

An implementation may estimate gains, a matrix, or another transform, but it
must expose its assumptions. If metadata, target visibility, or input
interpretation is missing, return a reviewable estimate or an explicit
cannot-calibrate state instead of inventing a numerical reference.

## Evaluate color and content together

Use held-out captures made under the intended capture and delivery conditions.
Compare target patches or approved reference regions after the same output
transform used for delivery, and inspect:

- neutral or target-region error under the declared measurement method;
- highlight and shadow clipping, gamut mapping, and gradient continuity;
- product/material identity, text, masks, and protected regions; and
- appearance on the validated viewing configuration.

Choose task-appropriate metrics and thresholds during validation; a single
RGB delta, channel hierarchy, or skin-tone ratio is not a release criterion
for all subjects, illuminants, or render intents.

## Human and safety boundary

Do not infer ethnicity, health, attractiveness, or a canonical human
appearance from color values. Human skin is not a calibration chart. When a
person is in scope, use consent, an approved visual reference, and review
criteria that do not convert color measurements into sensitive-trait labels.

## Related pages

- [[color-checker-and-white-balance]]
- [[color-space-and-gamma-reference]]
- [[color-theory-for-ml]]
- [[intrinsic-decomposition]]
