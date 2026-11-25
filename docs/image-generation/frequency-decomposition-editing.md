---
title: Frequency Decomposition Editing: Transform and Fidelity Contract
description: "Frequency decomposition is a declared transform, not a semantic edit map; record color domain, transform or filter, boundary and reconstruction policy, edit masks, and output review, and distinguish mathematically reconstructed signal from generated or visually plausible detail."
category: techniques
tags: [frequency, wavelets, laplacian, filtering, reconstruction, retouching, fidelity]
aliases: ["Frequency Separation", "Low and High Frequency Editing"]
---

# Frequency Decomposition Editing: Transform and Fidelity Contract

Low- and high-frequency labels describe the response of a selected transform
or filter. They do not identify “skin,” “detail,” “lighting,” or another
semantic region automatically. A frequency workflow is trustworthy only when
its color domain, transform, boundary behavior, edits, reconstruction, and
review are all declared.

## Declare the signal contract

For every job, record:

- source digest, dimensions, orientation, alpha/mask policy, color encoding,
  and whether operations occur in linear or display-referred values;
- transform/filter family, implementation/version, scale/level/radius,
  channels, dtype, and normalization;
- padding or boundary-extension mode, crop/alignment policy, and
  reconstruction routine;
- editable/protected regions and any generated component; and
- output transform, clipping/gamut behavior, numerical reconstruction check,
  and visual-review receipt.

Changing a blur radius, wavelet, padding mode, color encoding, or crop changes
the bands. Do not reuse a numeric radius or frequency-band label from another
resolution, lens, image domain, or transform as if it names the same content.

## Choose a transform for the stated property

Gaussian/laplacian pyramids, decimated wavelets, stationary wavelets, guided
filters, and learned frequency modules have different redundancy, alignment,
boundary, and reconstruction behavior. Select a method because its documented
property supports the task, then validate it on representative images.

[PyWavelets' stationary-wavelet documentation](https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html)
describes SWT as a translation-invariant, non-decimated modification of DWT;
it also records redundancy and signal-size constraints. The
[signal-extension documentation](https://pywavelets.readthedocs.io/en/latest/ref/signal-extension-modes.html)
shows why boundary mode belongs in the contract. Neither establishes that one
wavelet family is artifact-free or preferable for every retouching task.

## Preserve reconstruction evidence

For a linear transform paired with its matching inverse and unchanged
coefficients, calculate and retain a numerical round-trip residual under the
declared dtype and boundary policy. Once coefficients are edited, clipped,
masked, blended with another image, or passed through a nonlinear/generative
model, the result is a derived image and needs separate fidelity review.

Inspect seams, haloing, ringing, texture strength, gradients, color shifts,
text, product geometry, faces, and protected regions at delivery resolution.
If high-frequency content is synthesized after a low-frequency change, label
it as generated detail; do not represent it as recovered source texture.

## Editing and release boundary

Use masks and explicit change intent rather than treating a frequency band as
permission to modify every pixel in that band. A visually smooth result can
still remove factual marks or alter material/skin/product detail. Compare
against the source and an approved task baseline, and keep the transform
receipt with the output.

If the transform cannot reconstruct within the declared tolerance, the
boundary policy is ambiguous, or visual review finds a protected-detail
change, return a visible failure or review state. Do not silently reinject
another band, apply a new sharpening model, or claim exact reconstruction.

## Related pages

- [[color-space-and-gamma-reference]]
- [[tiled-inference]]
- [[paired-training-for-restoration]]
- [[skin-retouch-pipeline]]
