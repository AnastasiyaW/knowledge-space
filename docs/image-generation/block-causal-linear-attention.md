---
title: "Block Causal Linear Attention"
description: "Block causal linear attention is SANA-Video's trained long-video mechanism with a fixed-size cumulative attention state; it is not a generic plug-in for arbitrary image tiling or DiTs."
category: architectures
tags: [sana-video, causal, kv-cache, temporal, linear-attention, long-video, diffusion-transformer]
aliases: ["BCLA", "Causal Linear Attention", "SANA-Video Attention"]
---

# Block Causal Linear Attention

**Scope checked: 2026-09-04.** Block causal linear attention is the long-context mechanism described for SANA-Video. It turns a video into causally ordered blocks and carries a fixed-size cumulative linear-attention state from earlier blocks to later ones. It is a trained architecture component, not a post-processing recipe for arbitrary image tiles.

## What SANA-Video Actually Uses

SANA-Video extends the [[SANA]] linear-DiT family for video with temporal position handling and a causal Mix-FFN. For long-video generation, the paper reformulates causal linear attention so that a block needs cumulative attention-state and key summaries from earlier blocks rather than a growing per-token KV cache.

The constant-size cache is part of a larger coupled design:

- an ordered block-wise autoregressive diffusion objective;
- a causal linear-attention state accumulated across previous blocks;
- temporal positional handling inside the model;
- a causal Mix-FFN that also retains the previous block's last frame for temporal convolution;
- training and post-training procedures that teach the model to operate with that state.

The fixed cache size reduces the memory growth associated with a conventional long token cache. It does not by itself prove temporal quality, make a generic DiT causal, or remove the need for block-boundary evaluation.

## Do Not Generalize It to Image Tiling Without Evidence

The source material concerns long-video generation. It does not validate a raster-scanned image-tile workflow, seam-free high-resolution image synthesis, or a generic causal-state argument for arbitrary diffusion models.

An implementation that feeds cumulative state into an unmodified image model is a new research experiment. It needs its own training and compatibility evidence, positional scheme, block ordering, and visual validation; it must not be presented as SANA-Video behavior.

## Integration Contract

1. Choose an official SANA release and read the matching model/configuration documentation.
2. Use the implementation's declared model, VAE, attention kernel, block ordering, and checkpoint together.
3. Keep state isolation explicit: one generation stream must not reuse a cache from another prompt, seed, or video.
4. Retain model/config revisions, prompt, seed, block schedule, state-handling policy, output, and logs.
5. Test short clips before increasing duration, then inspect block boundaries, motion continuity, subject identity, and prompt adherence.

The SANA family evolves rapidly. Later releases introduce hybrid linear/softmax attention and attention-residual designs, so their performance or API must not be projected backwards onto the original block-causal mechanism.

## Acceptance Checks

| Question | Evidence |
|---|---|
| Is the intended architecture actually active? | matching official config, checkpoint, and runtime trace |
| Is the cache isolated and ordered correctly? | per-run state receipt and deterministic replay |
| Are transitions stable? | sequential review around every generated block boundary |
| Is the claimed efficiency real for this build? | measured memory and latency on the declared hardware and duration |
| Does it beat a simpler baseline? | same-prompt comparison against a non-causal or shorter-context baseline |

## References

- [SANA official repository](https://github.com/NVlabs/Sana)
- [SANA-Video paper](https://arxiv.org/abs/2509.24695)
- [SANA-Video documentation](https://nvlabs.github.io/Sana/docs/sana_video/)
- [SANA-Video 2.0 documentation](https://nvlabs.github.io/Sana/docs/sana_video2/)
