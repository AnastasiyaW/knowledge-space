---
title: "Denoising Architectures: Degradation and Evidence Contract"
description: "A denoising architecture is selected against a declared degradation and fidelity target, not a leaderboard or family name; bind capture/noise assumptions, model and checkpoint, preprocessing/tiling/color path, authorized train/evaluation splits, task and preservation metrics, and visual review before accepting generated or restored detail."
category: reference
tags: [denoising, restoration, degradation, evaluation, fidelity, provenance]
aliases: ["Denoise Architectures 2026", "Image Denoising Architectures"]
---

# Denoising Architectures: Degradation and Evidence Contract

Architecture names do not identify the degradation to remove or the detail to
preserve. A denoiser may estimate sensor noise, compression artifacts, blur,
rain, a synthetic perturbation, or a mixture; each task needs a separate
input, fidelity, and evaluation contract.

The [NTIRE 2025 Image Denoising Challenge report](https://openaccess.thecvf.com/content/CVPR2025W/NTIRE/html/Sun_The_Tenth_NTIRE_2025_Image_Denoising_Challenge_Report_CVPRW_2025_paper.html)
reports methods and scores for its specified AWGN sigma-50 challenge. Its
findings are useful evidence for that benchmark. They do not rank
architectures universally across camera pipelines, noise mixtures, artistic
retouching, forensic recovery, runtime limits, or protected-detail
requirements.

## Declare the restoration target

For each model evaluation or deployment, record:

- source asset/capture provenance, orientation, color profile, dynamic range,
  compression history, alpha/mask policy, and declared degradation model;
- model/checkpoint, code/runtime/version, compatible input range, color
  domain, preprocessing, padding, crop/tiling/blend policy, and output
  transform;
- authorized paired or normal-reference data, annotation/ground-truth policy,
  group-disjoint splits, and any synthetic degradation generator;
- task metrics and preservation metrics, evaluated on a source-disjoint set;
  and
- visual review of noise removal, texture, text, edges, product geometry,
  faces, shadows, gradients, color, and protected regions at delivery size.

Changing the camera, codec, noise distribution, crop, working color space,
tile plan, or checkpoint creates a new configuration. A score from a
different degradation or source split is not evidence for it.

## Choose by measured failure behavior

Convolutional, transformer, state-space, Fourier, and diffusion-based
approaches make different locality, conditioning, and generation assumptions.
Use the documented release only where its assumptions match the declared task,
then compare it against a named baseline under identical inputs and export
path.

Measure latency and peak memory separately from recovery quality. If a method
generates plausible texture or detail that is not supported by the input,
label that output as derived/generated rather than recovered source signal.
For masked correction, record the mask and separately verify unchanged
regions; an apparent no-op outside a mask is not proven without comparison.

## Failure boundary

If degradation assumptions, model compatibility, ground-truth authority,
source-disjoint evaluation, or protected-detail review is absent, return a
visible review/failure state. Do not select a model because it tops another
leaderboard, silently switch to a generative prior, or represent plausible
detail as factual restoration.

## Related pages

- [[image-restoration-survey]]
- [[paired-training-for-restoration]]
- [[tiled-inference]]
- [[frequency-decomposition-editing]]
