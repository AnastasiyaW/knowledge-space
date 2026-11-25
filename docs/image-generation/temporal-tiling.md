---
title: Temporal Tiling: Research Boundary and Evaluation Plan
description: "Temporal tiling is a model-specific research experiment for cross-tile consistency, not a direct reuse of video memory; bind the tile plan and runtime state, compare against an overlap baseline, and validate seams, composition, and cost on held-out images."
category: techniques
tags: [tiling, image-generation, research, global-context, evaluation]
aliases: ["Tiles-as-Frames", "Temporal Tile Processing"]
---

# Temporal Tiling: Research Boundary and Evaluation Plan

Temporal tiling is the hypothesis that a large image can be rendered as a
sequence of spatial tiles while carrying useful context from earlier tiles.
The word *temporal* is an analogy: tiles occupy different locations in one
image, not different frames of a video. Treat it as a model-specific research
experiment until a trained model and runtime explicitly support the state that
is being propagated.

## What a tiled system must preserve

Ordinary tiling can independently denoise regions and blend their overlaps.
That is often enough for memory control, but it can produce discontinuities in
gradients, geometry, lighting, or repeated objects. A temporal-tiling proposal
has to improve those defects without quietly changing the image contract.

Record these inputs for every experiment:

- the source image or prompt, rights boundary, seed, and checkpoint revision;
- the tile grid, overlap, order, coordinate convention, and resize policy;
- the exact runtime, latent representation, and any supported cache/state API;
- protected regions and the definition of an acceptable edit; and
- a plain overlap-only baseline generated from the same inputs.

Without that record, a smoother output cannot be attributed to tile context
rather than a changed prompt, sampler, crop, or checkpoint.

## Do not equate video state with image-tile state

[SANA-Video](https://github.com/NVlabs/Sana/blob/main/docs/sana_video.md)
uses block-wise autoregressive mechanisms for a video model. The
[SANA repository](https://github.com/NVlabs/Sana) documents linear attention,
image/video model families, and their own runtimes. That evidence does **not**
make its internal state a public drop-in interface for arbitrary image tiles.

In particular, do not:

- inject undocumented attention statistics with forward hooks;
- reuse a video cache after changing token positions, latent layout, or model
  revision;
- claim that a video causal mask proves spatial seam improvement; or
- copy a video configuration into an image pipeline without a model-specific
  implementation and test.

The same caution applies to any cross-attention, adapter, or hidden-state
handoff: it is valid only when the checkpoint was trained and evaluated with
that conditioning path.

## Candidate approaches and their evidence boundary

| Approach | What it can test | What it does not prove |
|---|---|---|
| Overlap and blending | memory-safe tiled inference baseline | global object consistency |
| Low-resolution global condition | whether a supported conditioning path helps structure | that every tile model can consume the condition |
| Trained spatial-context module | whether a named checkpoint learns cross-tile dependencies | transfer to another model, grid, or aspect ratio |
| Video-native causal state | long-sequence behavior in the compatible video runtime | correctness for a spatial image scan |

Start with the smallest supported path. If an image model exposes an official
global-condition or tiled-inference mode, bind the experiment to that model's
own documentation. If it does not, keep the proposal in research rather than
creating an unversioned hidden-state bridge.

## Evaluation plan

Use source-disjoint held-out images and include both smooth material and
composition-heavy scenes. Compare each candidate with the overlap-only
baseline under the same seed and model contract.

Evaluate three separate questions:

1. **Boundary continuity.** Inspect overlap crops, gradients, repeated
   textures, and color shifts at every tile edge.
2. **Global fidelity.** Inspect duplicated objects, changed counts, altered
   labels, product geometry, faces, and protected regions across the full
   image.
3. **Operational cost.** Measure peak memory, wall time, retry behavior, and
   cache reset behavior on the actual runtime and hardware.

Use metrics only where their reference and computation are defined. A seam
score may compare an output with a known target or a controlled overlap, but it
does not establish that generated text, identity, product attributes, or other
facts are correct. Keep visual review and factual preservation as explicit
release checks.

## Promotion gate

Call a temporal-tiling path implemented only when all of the following exist:

- a versioned model/runtime interface for the propagated condition or state;
- a reproducible configuration and source/output record;
- held-out evidence against the overlap baseline; and
- an owner-approved release policy for failures, protected regions, and
  factual-detail review.

Otherwise label it as an experiment. A plausible seamless image is not enough
evidence to turn an architecture analogy into a production capability.

## Sources and related pages

- [SANA repository](https://github.com/NVlabs/Sana)
- [SANA-Video documentation](https://github.com/NVlabs/Sana/blob/main/docs/sana_video.md)
- [[tiled-inference]]
- [[block-causal-linear-attention]]
- [[sana-denoiser-architecture]]
