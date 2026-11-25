---
title: Paired Restoration Training: Evidence and Conditioning Contract
description: "Paired restoration training learns a declared degraded-to-target mapping; it needs source-aligned and rights-cleared pairs, a model-compatible conditioning path, holdouts separated by source, and evaluation that distinguishes measured recovery from plausible invention."
category: techniques
tags: [image-to-image, paired-data, restoration, conditioning, provenance, evaluation]
aliases: ["Image-to-Image Conditioning", "Paired Image Training", "Degradation Pipeline"]
---

# Paired Restoration Training: Evidence and Conditioning Contract

Paired restoration training learns a declared mapping from a degraded input to
an approved target. It is not ordinary text-to-image training with cleaner
captions, and it must not present plausible generated texture as recovered
source evidence.

[Palette](https://arxiv.org/abs/2111.05826) is a conditional
image-to-image diffusion framework covering tasks such as colorization,
inpainting, uncropping, and JPEG restoration. That paper supports the general
need for an explicit image condition; it does not prescribe one channel layout,
initialization, loss, scheduler, or training recipe for every modern model.

## Define the pair

For every sample, retain:

- original/source authority and rights record;
- degraded input, target, and their hashes;
- alignment/crop/resize/color-space policy;
- declared degradation or approved retouch operation;
- editable versus protected/unknown regions; and
- reviewer decision and any uncertainty or exclusion reason.

Source and target must depict the same approved scene or a deliberately
specified edit. If the target contains manual beautification, generative fill,
or unknown historical changes, label that fact rather than treating it as a
clean ground truth.

## Conditioning must match the model

Image-conditioned systems may use channel concatenation, cross-attention, a
dedicated control branch, an image encoder, or another architecture-specific
mechanism. Use only the conditioning path documented and trained for the
pinned checkpoint. Changing input channel counts, injecting latents, or
copying a conditioning module from another framework creates a new model
configuration that requires its own initialization, training, and evaluation.

Record the full conditioning contract:

- base model/checkpoint and VAE/encoder revisions;
- runtime, scheduler/objective, and conditioning module implementation;
- input/target latent or pixel preprocessing; and
- behavior when the condition is missing, malformed, masked, or out of
  distribution.

Never silently drop an image condition and return an unconditional result as if
the restoration succeeded.

## Build honest degradation evidence

Synthetic degradation can create controlled paired examples, but it models only
the transforms that were declared. Keep synthetic and observed real-world
degradations distinguishable. Do not claim that noise, blur, compression, or
downscaling parameters reproduce an unknown camera or editing history without
evidence.

Split training, tuning, and holdout data by original asset, capture session,
subject/product, and derivative chain. Adjacent crops or multiple degraded
versions of the same original belong in the same split.

## Evaluate recovery separately from plausibility

| Evidence type | What it can support |
|---|---|
| Authorized aligned target | paired reconstruction metrics and visual error review under a defined color/crop policy |
| Source-disjoint real degraded image without target | reviewed usefulness and failure analysis, not a pixel-accuracy claim |
| Generative or uncertain target detail | a derived visual proposal, never recovered factual ground truth |

Review text, marks, product geometry, faces, protected regions, and material
detail separately from aggregate metrics. A high visual-quality score can
coexist with a factually altered output.

## Release gate

Promote a paired-restoration model only with reproducible pairs, a
model-compatible conditioning path, source-disjoint holdouts, source/output
provenance, and a policy for uncertain or changed factual detail. If the model
cannot distinguish recovery from invention for the intended use, release it
only as a reviewed enhancement proposal or keep it out of that workflow.

## Related pages

- [[image-restoration-survey]]
- [[synthetic-dataset-pipeline]]
- [[upscaler-evaluation]]
