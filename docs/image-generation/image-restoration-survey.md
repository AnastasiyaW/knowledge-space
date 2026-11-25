---
title: Image Restoration: Task and Fidelity Guide
description: Image restoration must declare the degradation and fidelity target; choose a task-compatible deterministic or diffusion method, then validate measured recovery separately from plausible but invented detail.
category: techniques
tags: [image-restoration, denoising, deblurring, super-resolution, jpeg-artifacts, diffusion, fidelity, evaluation]
aliases: ["Image Restoration Survey", "Image Enhancement", "Denoising Survey"]
---

# Image Restoration: Task and Fidelity Guide

Image restoration needs a declared degradation and a declared fidelity target.
“Looks better” is not sufficient for product, documentary, scientific, or
forensic material: a generative method can produce plausible detail that was
not supported by the observed image.

## Start with the restoration contract

Define:

- degradation type and known acquisition history, such as noise, blur,
  compression, missing area, low light, or limited resolution;
- required output behavior: measurement-faithful recovery, perceptual cleanup,
  or clearly labeled creative reconstruction;
- available reference target or a source-specific validation method;
- protected content such as text, faces, product geometry, colors, and marks;
  and
- allowed model/data/license boundary.

Do not combine degradation classes under one generic “enhance” action unless
the model was trained and validated for that combined contract.

## Method families

### Task-specific deterministic models

Task-specific CNN and transformer approaches remain appropriate when the
degradation is known and pixel-faithful recovery matters. Examples include
[SwinIR](https://github.com/JingyunLiang/SwinIR),
[NAFNet](https://github.com/megvii-research/NAFNet), and
[Restormer](https://arxiv.org/abs/2111.09881). Their published results apply
to particular tasks, datasets, and checkpoints; select a compatible release
instead of treating any of them as a universal restoration model.

### Conditional diffusion restoration

[Palette](https://research.google/pubs/palette-image-to-image-diffusion-models/)
demonstrates conditional diffusion across image-to-image tasks including
colorization, inpainting, uncropping, and JPEG restoration. Diffusion methods
can model a broader output distribution, but that flexibility makes
unsupported detail a central acceptance risk.

[IR-SDE](https://arxiv.org/abs/2301.11699) is another research formulation
that uses a mean-reverting stochastic differential equation for restoration.
It does not establish a default schedule or a production configuration for a
different checkpoint.

### Editing and foundation-model workflows

General image-editing systems may be useful for a bounded, mask- and
instruction-controlled repair. They need source-preservation evaluation and
must be kept distinct from metric-oriented denoising or super-resolution. See
[[RealRestorer]] for one release-specific workflow rather than a ranking over
all restorers.

## Evaluation that catches invention

Use a validation set with known targets where possible, and report the metric
in its task context. Add visual review for:

- hallucinated text, geometry, texture, or small-object detail;
- color and tone drift, especially after compression or low-light correction;
- seams and discontinuities at masks, crops, or tiles;
- preservation of product, document, or medical/scientific evidence; and
- behavior on degraded inputs outside the training distribution.

Separate a metric result from a release decision. A high reconstruction metric
does not automatically prove factual preservation, and a visually attractive
diffusion output may be unacceptable when pixels are evidence.

## Release record

Store the input digest, degradation diagnosis, model/checkpoint, parameters,
reference target or validation fixture, output, acceptance result, and an
explicit label for any creative reconstruction. Re-run validation after a
model, runtime, or input-domain change.

## Related pages

- [[RealRestorer]]
- [[color-checker-and-white-balance]]
- [[tiled-inference]]
- [[diffusion-inference-acceleration]]
