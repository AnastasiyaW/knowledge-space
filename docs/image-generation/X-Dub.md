---
title: "X-Dub: Public Mask-Free Visual Dubbing"
description: "X-Dub is a public Wan2.2-TI2V-5B-based visual-dubbing release; validate single-person cropping, identity, temporal stability, audio rights, and model terms on every target video."
category: models
tags: [visual-dubbing, lip-sync, video-editing, wan2.2, audio-driven, generative-bootstrapping, synthetic-media]
aliases: ["X-Dub Wan-5B"]
---

# X-Dub: Public Mask-Free Visual Dubbing

**Scope checked: 2026-09-04.** X-Dub is the public implementation of a visual-dubbing method that synchronizes a video with replacement audio. The upstream method frames the task as mask-free editing trained through generative bootstrapping. It is intended to alter speech-related motion while retaining the rest of the video, but retention is an acceptance target—not a guarantee.

## Public Release Versus the Paper Model

The maintainers explicitly distinguish the published X-Dub (Wan-5B) release from the internal model evaluated in the paper. The public release uses a Wan2.2-TI2V-5B-based stack and multi-stage supervised fine-tuning; the internal model and its LoRA tuning are not released.

Do not transfer quantitative claims, quality expectations, or settings from the paper's internal model to the public checkpoint. The public repository itself records remaining temporal and subject-consistency limitations and says that a quantitative comparison is still pending.

## Current Runtime Boundary

The official repository packages an inference pipeline, a model bundle, audio components, and face-cropping support. Its current online crop path is for **single-person** videos. It crops the face, runs dubbing on the crop, then maps the result back to the original video.

That convenience path is not a multi-person tracker. Rapid head movement, occlusion, or unreliable crop tracking can yield jitter, identity drift, colour drift, or failed frames. Treat every output as a candidate clip requiring review.

## Safe Production Workflow

1. Confirm rights and consent for the source video, the replacement audio, and any depicted person or character.
2. Freeze the exact repository revision, weights, dependencies, input video, input audio, and inference settings.
3. Run a short representative segment before processing a full asset.
4. Review the output frame by frame around speech, cuts, occlusions, fast motion, and the crop boundary.
5. Compare identity, lighting, colour, background, and non-mouth motion against the source.
6. Retain source, output, configuration, logs, and a clear synthetic-media label where appropriate.

Never use a generated dubbing result as evidence that a real person said something. For public, commercial, or sensitive material, add a human approval gate and follow the applicable consent, disclosure, and platform rules.

## Validation Matrix

| Risk | Required evidence |
|---|---|
| Lip/audio alignment | review several speech segments with the intended audio |
| Identity and appearance | source/output comparison at delivery resolution |
| Temporal stability | sequential review across cuts, fast turns, and occlusions |
| Crop correctness | verify that the intended face alone was selected |
| Reproducibility | source and audio digests, model revision, settings, and output receipt |

## Licensing and Artifact Terms

The code repository, Wan backbone, checkpoint bundle, audio-model components, and any community integration can have separate terms. Review the current terms and redistribution conditions for every downloaded artifact; do not derive deployment permission from one repository label.

## References

- [X-Dub official repository](https://github.com/KlingAIResearch/X-Dub)
- [X-Dub project page](https://hjrphoebus.github.io/X-Dub/)
- [X-Dub paper](https://arxiv.org/abs/2512.25066)
- [X-Dub model collection](https://huggingface.co/KlingTeam/X-Dub)
