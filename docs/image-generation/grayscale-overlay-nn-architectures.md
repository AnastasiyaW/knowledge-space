---
title: Grayscale Overlay Prediction: Paired Retouching Contract
description: "Grayscale overlay prediction is a paired, pixel-aligned retouching task; preserve the blend contract and no-op baseline, bind every source/target pair and mask, and evaluate the composited image plus the map before releasing an automated adjustment."
category: reference
tags: [image-restoration, retouching, regression, paired-data, evaluation, provenance]
---

# Grayscale Overlay Prediction: Paired Retouching Contract

Grayscale overlay prediction estimates a single-channel adjustment map for a
declared compositing operation. It is a paired, pixel-aligned retouching task,
not a generic image-restoration benchmark. The map is meaningful only together
with the exact blend implementation, color handling, input image, and approved
editing scope.

## Define the blend contract first

Before choosing a network, make the target reproducible:

- input color space, bit depth, orientation, and alpha handling;
- overlay range and its neutral no-op value;
- blend function and implementation version, including linear/gamma handling;
- opacity, masks, protected regions, and clipping behavior; and
- source image, target map, approved composited target, and rights/consent
  record.

Changing any of these can change the expected map even if the visible retouch
looks similar. A target map without its compositing contract is not reusable
training data.

## Model candidates are hypotheses

[NAFNet](https://github.com/megvii-research/NAFNet) and
[Restormer](https://github.com/swz30/Restormer) are published image-restoration
implementations. They can be candidates for a paired regression baseline, but
their published architectures do not establish that one is best for a
single-channel retouch map, that a particular head modification is compatible,
or that a fixed loss/tiling recipe is safe for every overlay.

Start with the smallest versioned model that can produce the required channel
layout. Bind the training and inference code to:

1. a checkpoint/repository revision;
2. the output range and no-op initialization policy;
3. the full-resolution/tile behavior used at release; and
4. a baseline that emits the neutral map.

Treat unsupported head rewrites, custom hooks, and batch-normalization behavior
as experiments with their own evidence, not implicit architecture features.

## Build pairs that mean the same thing

Each example must pair the same scene geometry with the target adjustment:

- no crop, perspective, face alignment, or retouch operation may drift between
  input and target;
- masks should distinguish editable pixels from protected/unknown pixels;
- separate source assets by photographer, subject, shoot, and derivative chain
  before train/validation/test splitting; and
- retain the original, map, composited target, edit rationale, and reviewer
  decision together.

Augmentations are valid only when they preserve the image-to-map relationship
and the blend contract. A transformation that changes illumination,
composition, or geometry may create an apparently aligned pair with an invalid
target.

## Evaluate the map and the visible result

Use paired map error only after its scale and valid region are defined. It
cannot tell whether the adjustment looks correct after compositing. Review both
surfaces:

| Surface | Check |
|---|---|
| Predicted map | neutral regions remain neutral, gradients are stable, masks are honored, and edges do not leak |
| Composited image | intended correction appears, protected features remain unchanged, and no banding, seams, clipping, or color shift is introduced |
| Held-out sources | performance survives new subjects, lighting, materials, and crops |
| Runtime | resolution, memory, tile behavior, and fallback/failure path match the release environment |

For faces or products, a visually smooth result still requires review of
identity-relevant features, labels, texture, and factual detail. The network
proposes an adjustment; it does not authorize a finished retouch.

## Release gate

Release an automated overlay only when a reviewer can reproduce the input,
model, map, blend contract, composited output, and approval. If the model emits
a non-neutral change outside the allowed mask or evaluation cannot distinguish a
plausible map from an approved adjustment, hold it for manual correction.

## Sources and related pages

- [NAFNet official repository](https://github.com/megvii-research/NAFNet)
- [Restormer official repository](https://github.com/swz30/Restormer)
- [[paired-training-for-restoration]]
- [[image-restoration-survey]]
- [[low-vram-inference-strategies]]
