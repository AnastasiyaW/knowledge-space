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

ViFeEdit adapts Wan and similar text-to-video Diffusion Transformers for video generation and editing without video training data.
- 3D attention reparameterization: separates spatial independence.
- Dual-path pipeline: routes separate timestep embeddings across paired 2D source and target images.

Training takes 100–250 paired images and fewer than 20 epochs in practice. We treat it as a task-specific tuning workflow rather than a turnkey video editor.

## Development line

- **2026-03-18 — ViFeEdit public project resources were linked.** On 2026-03-18, we linked the development line to a public GitHub repository and a Hugging Face link. The links identify the project resources. They do not establish a release, version, capability change, or publication status.

## What changed

2026-03-16: the ViFeEdit preprint introduced video-free tuning for video Diffusion Transformers using only 2D image pairs.  
2026-03-17: the authors released training and inference code.  
2026-03-18: the project became available through the linked repository. The repository adds the practical limits omitted by the event links: 100–250 paired images per task, training limited to the first 20 epochs, and an inference plus optional post-processing path.

## How to use this

As of 2026-03-18, we use the linked GitHub repository as the primary project source. We treat the Hugging Face link as a related resource until research confirms its role.

1. Clone the repository and install it in an isolated Python environment with `pip install -e .`. Reuse a DiffSynth Conda environment only if its dependencies are compatible.
  — <https://github.com/Lexie-YU/ViFeEdit>
2. Create paired source and target images plus a `metadata_vife.csv` that maps each target prompt and target image to the source image used as the inference-video reference.
  — <https://github.com/Lexie-YU/ViFeEdit>
3. Set data and output paths in `train_vife.sh`, run the script, and pick a checkpoint from the first 20 epochs instead of running the configured 500 epochs.
  — <https://github.com/Lexie-YU/ViFeEdit>
4. Configure the provided inference example and run `python inference.py`. Use `postprocess.py` only when additional output alignment is needed.
  — <https://github.com/Lexie-YU/ViFeEdit>

## Best practices

- Start with a narrowly defined edit and 100–250 paired images. Keep source and target pairing and metadata names consistent, because training uses the source image as the later source-video reference.
  — <https://github.com/Lexie-YU/ViFeEdit>
- Treat the first 20 epochs as the practical training window. Evaluate checkpoints there before extending a run.
  — <https://github.com/Lexie-YU/ViFeEdit>
- Pin or verify `transformers==4.55.0`. If editable installation fails on `pkg_resources`, use the repository’s documented `--no-build-isolation` flag rather than changing dependencies.
  — <https://github.com/Lexie-YU/ViFeEdit>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The linked hf.ru URL returned an error during verification, so we do not treat it as an official model-weight release.
- The repository documents code, data preparation, and inference, but does not identify a downloadable ViFeEdit checkpoint or a supported production deployment target.
- No post-2026-03-18 first-party release note exists in the sources used here.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Lexie-YU/ViFeEdit | Lexie-YU/ViFeEdit — repository README | 2026-09-05 |
| https://arxiv.org/abs/2603.15478 | ViFeEdit: A Video-Free Tuner of Your Video Diffusion Transformer | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:vifeedit`, thread `public-project-presence`, 1 dated events 2026-03-18 → 2026-03-18.
- **Practical note:** As of 2026-03-18, use the linked GitHub repository as the identified project source. Treat the Hugging Face link as a related resource until research establishes its exact role.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.