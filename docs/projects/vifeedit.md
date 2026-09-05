---
title: ViFeEdit — Public project presence
category: projects
date: 2026-03-18
tags: [project, public-project-presence, vifeedit]
aliases: ["ViFeEdit"]
---

# ViFeEdit — Public project presence

**Development line:** `project:vifeedit` · thread `public-project-presence`  
**Last event:** 2026-03-18 · 1 dated since 2026-03-18 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ViFeEdit is a research codebase for adapting a text-to-video Diffusion Transformer to controllable video generation and editing without video training data. The repository targets the Wan model family.

- 3D attention reparameterization: separates spatial independence.
- Dual-path pipeline: uses separate timestep embeddings.
- 2D training: trains on 100–250 paired source and target images.

Practical training takes fewer than 20 epochs. This is a task-specific tuning workflow rather than a turnkey video editor.

## Development line

- **2026-03-18 — ViFeEdit public project resources were linked.** On 2026-03-18, the project linked a public GitHub repository and a Hugging Face page. The links identify project resources. They do not establish a release, version, capability change, or publication status.

## What changed

2026-03-16: the ViFeEdit preprint introduced video-free tuning for video Diffusion Transformers using only 2D image pairs.

2026-03-17: the authors released training and inference code.

2026-03-18: the project opened the repository. The repository defines the operational scope: 100–250 paired images per task, practical training within the first 20 epochs, and an inference pipeline with optional post-processing.

## How to use this

As of 2026-03-18, we use the GitHub repository as the primary code source. We treat the Hugging Face link as a related resource until its exact role is verified.

1. Clone the repository and install it in an isolated Python environment with `pip install -e .`. Reuse a DiffSynth Conda environment only if dependencies match.
  — <https://github.com/Lexie-YU/ViFeEdit>
2. Prepare paired source and target images with a `metadata_vife.csv`. Map each target prompt and target image to the source image used as the inference reference.
  — <https://github.com/Lexie-YU/ViFeEdit>
3. Set data and output paths in `train_vife.sh`, run the script, and pick a checkpoint from the first 20 epochs instead of running the configured 500 epochs.
  — <https://github.com/Lexie-YU/ViFeEdit>
4. Configure the inference example and run `python inference.py`. Run `postprocess.py` only when output alignment needs correction.
  — <https://github.com/Lexie-YU/ViFeEdit>

## Best practices

- Start with a narrow edit and 100–250 paired images. Keep source and target names consistent, because training uses the source image as the video reference later.
  — <https://github.com/Lexie-YU/ViFeEdit>
- Evaluate checkpoints within the first 20 epochs before extending a training run.
  — <https://github.com/Lexie-YU/ViFeEdit>
- Pin `transformers==4.55.0`. If editable install fails on `pkg_resources`, add the documented `--no-build-isolation` flag instead of swapping packages.
  — <https://github.com/Lexie-YU/ViFeEdit>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The hf.ru link errored during verification, so we do not treat it as an official weights release.
- The repository provides code, data formats, and inference scripts, but provides no downloadable ViFeEdit checkpoint or production deployment target.
- We found no first-party release note dated after 2026-03-18.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Lexie-YU/ViFeEdit | Lexie-YU/ViFeEdit — repository README | 2026-09-05 |
| https://arxiv.org/abs/2603.15478 | ViFeEdit: A Video-Free Tuner of Your Video Diffusion Transformer | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:vifeedit`, thread `public-project-presence`, 1 dated events 2026-03-18 → 2026-03-18.
- **Practical note:** As of 2026-03-18, we use the GitHub repository as the main source and treat the Hugging Face link as related until clarified.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
