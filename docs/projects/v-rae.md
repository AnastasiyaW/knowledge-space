---
title: V-RAE
category: projects
date: 2026-08-24
tags: [project, v-rae, v-rae-development, v_rae]
aliases: ["V-RAE"]
---

# V-RAE

**Development line:** `project:v-rae` · thread `v-rae-development`  
**Last event:** 2026-08-24 · 1 dated since 2026-08-24 · **Researched:** 2026-09-05 · confidence: high

## What it is

V-RAE is a research codebase and checkpoint set for video reconstruction and generation. It pairs frozen DINOv3, SigLIP2, V-JEPA2.1, or EUPE encoders with temporal pooling and a video decoder.

- Video reconstruction from frozen representations.
- Class-conditional generation across video benchmarks.
- Future-frame prediction without updating encoder weights.

Best reported generation results are 117.86 gFVD on UCF101 and 19.16 on Kinetics-600. The code is research-oriented and requires Linux, NVIDIA CUDA, FFmpeg, Python 3.10+, and matching encoder weights.

## Development line

- **2026-08-24 — V-RAE project resources were linked.** On 2026-08-24, the project published entry links to its website, GitHub repository, and Hugging Face model page without separate release details or verified capabilities.

## What changed

- 2026-08-13 — The V-RAE paper was submitted to arXiv, defining the representation-autoencoder approach and tFVD temporal-coherence diagnostic.
- 2026-08-14 — The official implementation began with an initial GitHub release.
- 2026-08-19 — The repository added data manifests, visual results, and a fix for mismatched configurations.
- 2026-08-24 — Public entrypoints covered the project page, official implementation, and checkpoint repository; no first-party source proves a distinct code or model release on this date.
- 2026-08-26 — The repository updated GIF visual results.

## How to use this

As of 2026-08-24, treat the linked V-RAE website, GitHub repository, and Hugging Face model page as starting points to check project documentation, source, and model availability; exact versions and usage requirements still need research.

1. Clone the implementation, create a Python 3.10 environment, install FFmpeg and the pinned package dependencies.
  — <https://github.com/V-RAE/V-RAE>
2. Download the V-RAE checkpoint repository into `ckpts`, then download the frozen encoder weights that match the selected variant.
  — <https://huggingface.co/Guomh0707/V-RAE-Models>
3. Put input clips in `assets/sample1.mp4` through `assets/sample3.mp4`, then run `python sampling.py dino`, `siglip`, `vjepa`, or `eupe`; compare results under `outputs/<variant>/`.
  — <https://github.com/V-RAE/V-RAE>

## Best practices

- Match every V-RAE checkpoint to its corresponding frozen encoder weights; the checkpoints are custom PyTorch files intended for the official codebase.
  — <https://huggingface.co/Guomh0707/V-RAE-Models>
- Use Linux with an NVIDIA GPU, a CUDA-compatible driver, FFmpeg, and Python 3.10 or newer; verify CUDA and TorchCodec before inference.
  — <https://github.com/V-RAE/V-RAE>
- Treat the published numbers as task-specific research results: rFVD measures reconstruction, gFVD generation, and tFVD temporal coherence; do not compare them as a single universal quality score.
  — <https://github.com/V-RAE/V-RAE>

## Superseded by this

- 2026-08-19 — Initial repository configurations were superseded by the documented fix for mismatched configs.

## Still unknown

- No dated first-party release record exists for 2026-08-24 itself; the linked paper and initial repository release predate that date.
- The model hub omits a dated revision on the retrieved page, leaving the original checkpoint-publication date unverified.
- No hosted inference endpoint or production deployment guidance exists; the model card says no Inference Provider deploys it.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/V-RAE/V-RAE | V-RAE/V-RAE official implementation README | 2026-09-05 |
| https://huggingface.co/Guomh0707/V-RAE-Models | Guomh0707/V-RAE-Models model card | 2026-09-05 |
| https://arxiv.org/abs/2608.13556 | V-RAE: Rethinking Video Latent Spaces for Generation | 2026-09-05 |
| https://github.com/V-RAE/V-RAE/commits/main/ | V-RAE/V-RAE commit history | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:v-rae`, thread `v-rae-development`, 1 dated events 2026-08-24 → 2026-08-24.
- **Practical note:** As of 2026-08-24, practitioners should treat the linked V-RAE website, GitHub repository, and Hugging Face model page as the starting points for checking project documentation, source, and model availability; exact versions and usage requirements still need research.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
