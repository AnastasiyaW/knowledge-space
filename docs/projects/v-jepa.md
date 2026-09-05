---
title: V-JEPA
category: projects
date: 2026-03-20
tags: [project, v-jepa]
aliases: ["V-JEPA"]
---

# V-JEPA

**Development line:** `project:v-jepa` · thread `v-jepa`  
**Last event:** 2026-03-20 · 1 dated since 2026-03-20 · **Researched:** 2026-09-05 · confidence: high

## What it is

V-JEPA is a family of PyTorch models from Meta for video understanding and robotics developers.

- Feature extraction: pulls representations from video without manual annotations.
- Latent prediction: predicts actions and states in latent space.
- V-JEPA 2-AC: adds action-conditioned planning for manipulators.
- V-JEPA 2.1: targets spatially and temporally consistent dense features.

The 2.1 line provides ViT-B 80M, ViT-L 300M, ViT-g 1B, and ViT-G 2B parameters at 384 px.

Start with V-JEPA 2.1 for new segmentation, depth, tracking, and video features; 2-AC is needed only to reproduce the robotics research loop.

## Development line

- **2026-03-20 — V-JEPA was linked to the V-JEPA 2 repository.** Dense video and image encoders using Dense Predictive Loss, deep self-supervision, and multimodal tokenizers; the initial README announcement is dated 2026-03-16, and the paper was published on 2026-03-15.

## What changed

- 2026-03-20 — V-JEPA 2.1 became available in the V-JEPA repository: a family of dense video and image encoders using Dense Predictive Loss, deep self-supervision, and multimodal tokenizers. The initial README announcement is dated 2026-03-16, and the paper was published on 2026-03-15.
- 2025-06-11 — Meta introduced V-JEPA 2, a 1.2B-parameter video world model, and V-JEPA 2-AC: an action-conditioned variant fine-tuned on under 62 hours of unlabeled DROID video for zero-shot pick-and-place.
- 2026-03-15 — The V-JEPA 2.1 paper added four checkpoint sizes from 80M to 2B and reported dense task gains, including 0.307 RMSE on NYUv2 and 77.7% on Something-Something-V2.

## How to use this

As of 2026-03-20, treat facebookresearch/vjepa2 as the reference implementation for V-JEPA; available documentation gives no operational guidance beyond it.

1. Install PyTorch, timm, and einops; use a CUDA build of PyTorch for local runs.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
2. Load the preprocessor and the required 2.1 backbone via torch.hub; start with vjepa2_1_vit_base_384 for lower resource use, or gigantic for maximum quality.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
3. Pass video through the encoder and train a lightweight head or linear probe for downstream tasks; the provided demo shows video inference.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
4. Use V-JEPA 2-AC with image goals and model-predictive control for robotics experiments; this is a separate action-conditioned checkpoint, not the standard 2.1 encoder.
  — <https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/>

## Best practices

- Choose V-JEPA 2.1 for dense representations: the release changes the objective and tokenizer for spatial-temporal consistency rather than just scaling the model.
  — <https://arxiv.org/abs/2603.14482>
- Match checkpoint size to task and compute budget: 2.1 offers 80M, 300M, 1B, and 2B variants at 384 px.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
- Replace decord in advance on macOS: the base package lacks macOS support, and the authors pin no single recommended fork.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>

## Superseded by this

- 2026-03-15 — For new dense video and image representation tasks, V-JEPA 2 is no longer the preferred starting point: V-JEPA 2.1 replaces it specifically to improve dense and temporally consistent features.
- 2026-03-15 — Do not treat V-JEPA 2.1 as a new robotics action-conditioned checkpoint: V-JEPA 2-AC remains a separate post-training variant of V-JEPA 2.

## Still unknown

- The official repository does not publish GitHub Releases: the 2026-03-20 date confirms V-JEPA 2.1 presence in the repository, but the paper and README are dated 2026-03-15 and 2026-03-16.
- Official instructions document PyTorch Hub for V-JEPA 2.1, but the Transformers example in the README lists only V-JEPA 2 repositories; the README does not confirm 2.1 support through that path.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/facebookresearch/vjepa2 | facebookresearch/vjepa2 — official repository | 2026-09-05 |
| https://github.com/facebookresearch/vjepa2/blob/main/README.md | V-JEPA 2 repository README | 2026-09-05 |
| https://arxiv.org/abs/2603.14482 | V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning | 2026-09-05 |
| https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/ | Introducing the V-JEPA 2 world model and new benchmarks for physical reasoning | 2026-09-05 |
| https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/ | V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:v-jepa`, thread `v-jepa`, 1 dated events 2026-03-20 → 2026-03-20.
- **Practical note:** As of 2026-03-20, practitioners should treat the linked facebookresearch/vjepa2 repository as the recorded implementation reference for this V-JEPA line; the sealed evidence alone does not justify operational guidance beyond that.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
