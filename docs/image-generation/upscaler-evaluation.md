---
title: Image Upscaler Evaluation: Fidelity-First Protocol
description: "Choose an upscaler by measured fidelity on the actual source class, not benchmark labels or a universal default; preserve source/output provenance, evaluate artifacts and factual detail, and keep generative outputs out of factual training targets."
category: tools
tags: [upscaling, super-resolution, image-restoration, evaluation, data-provenance, fidelity]
---

# Image Upscaler Evaluation: Fidelity-First Protocol

Upscaling creates a derived image. It can improve presentation or make a
training input usable, but it cannot recover unobserved factual detail. Choose
a model from evidence on the actual source class and intended use, rather than
from a fixed leaderboard, a hardware estimate, or a claim that one tool is
hallucination-free.

## Separate task classes

| Task class | Typical evidence | Release caution |
|---|---|---|
| Known downsampling | paired high/low-resolution references | paired metrics are meaningful only for the stated degradation |
| JPEG/noisy web imagery | source-disjoint real images plus reviewed outputs | learned restoration can alter texture, edges, and text |
| Generative super-resolution | perceptual review and disclosed generated detail | never treat invented detail as recovered source evidence |

[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) is an official project
for practical image/video restoration trained with synthetic degradation.
[SwinIR](https://github.com/JingyunLiang/SwinIR) documents restoration tasks
including classical, lightweight, and real-world super-resolution, denoising,
and JPEG artifact reduction. [HAT](https://arxiv.org/abs/2205.04437) is a
super-resolution research model. These names identify candidates; they do not
establish a universal ranking, safe default, license conclusion, or performance
number for your hardware and images.

## Evaluation dataset

Build the evaluation set before selecting a model:

- split by original asset/source, not by adjacent crops or derived copies;
- include the image classes the project will actually receive;
- keep paired references only where the known degradation is honest;
- reserve a source-disjoint holdout that no tuning decision sees; and
- record rights, original hash, crop/resize path, model revision, settings, and
  output hash for every derived image.

Do not use a model's own promotional gallery as a substitute for a held-out
test set.

## What to measure

For paired references, report metrics with their exact reference, crop, color
space, alignment, and aggregation rule. PSNR, SSIM, or perceptual metrics can
describe reconstruction error in that controlled setting; they do not prove
factual preservation for unpaired images.

For all source classes, review:

1. repeated or erased texture, ringing, aliasing, and compression artifacts;
2. text, logos, product geometry, facial features, and other factual detail;
3. crop and aspect-ratio changes; and
4. peak memory, wall time, retry behavior, and failures on the intended
   runtime.

Use a blinded visual review where the decision matters. Record disagreement
instead of resolving it by choosing the prettier result.

## Training-data boundary

For factual, catalog, or supervised targets, preserve the original source as
the authority. An upscaled derivative may be used only under a documented
policy that distinguishes:

- preprocessing for display or model input;
- validated paired reconstruction experiments; and
- generative or uncertain detail that must not become ground truth.

If an output changes a mark, text, edge, or material detail that matters to a
label, hold it for review or exclude it from that target. Saving as PNG does
not repair an earlier model alteration, and deterministic processing is not a
guarantee of factual recovery.

## Runtime integration

Verify every concrete integration at the installed version: model file digest,
loader, device/dtype, tile policy, alpha/bit-depth handling, input/output
colorspace, and failure path. A ComfyUI node, a Python script, and a standalone
binary are separate runtimes and require separate evidence.

Promote one candidate only after its source-class evaluation, provenance
records, and operational measurement meet the intended release contract.

## Related pages

- [[image-restoration-survey]]
- [[diffusion-lora-training]]
- [[flux-klein-9b-inference]]
