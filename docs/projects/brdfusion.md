---
title: BRDFusion
category: projects
date: 2026-06-22
tags: [brdfusion, project]
aliases: ["BRDFusion"]
---

# BRDFusion

**Development line:** `project:brdfusion` · thread `brdfusion`  
**Last event:** 2026-06-22 · 1 dated since 2026-06-22 · **Researched:** 2026-09-05 · confidence: medium

## What it is

BRDFusion is an open research pipeline for turning urban video into a controllable 3D Gaussian/PBR scene, closer to UrbanIR plus diffusion refinement than to a general video generator.

- Geometry, materials, and HDR lighting: reconstructs them from video.
- Novel views and relighting: renders both through PBR.
- Rendered video: refines frames with DiffusionRenderer.
- Scene edits: supports night simulation, local lights, headlights, and dynamic-object edits.

Tested on Ubuntu 22.04 with an RTX A6000; Gen. Render can exceed 24 GB of VRAM.
We use it for reproducible research and driving-scene simulation on a Linux GPU stack, not as a lightweight single-model workflow.

## Development line

- **2026-06-22 — BRDFusion project resources were published.** On 2026-06-22, BRDFusion linked its project page, source repository, and checkpoint collection. This release makes the implementation and model artifacts public so researchers can locate and use them.

## What changed

- 2026-06-15 — arXiv v1 introduced BRDFusion’s hybrid physics-and-generation method for urban-scene inverse and forward rendering.
- 2026-06-22 — The project page, public code, and pretrained-checkpoint resources were linked as a usable research release.

## How to use this

From 2026-06-22, we can evaluate or reproduce the project starting from the linked BRDFusion project page, source repository, and checkpoint collection.

1. Check the documented Linux, compiler, CUDA, and GPU prerequisites before installing; the project uses separate `brdfusion` and `cosmos-predict1` environments.
  — <https://github.com/shigon255/BRDFusion>
2. Clone recursively, build both Conda environments, authenticate with Hugging Face for DiffusionRenderer weights, and supply the required SMPL asset.
  — <https://github.com/shigon255/BRDFusion>
3. Download a supplied preprocessed scene and matching one-camera checkpoint, unpack it under `ckpt/`, then run `bash scripts/stage_ckpt.sh`.
  — <https://github.com/shigon255/BRDFusion>
4. Run `tools/run_pipeline.py` with `--stage render` for PBR output; use the matching scene, camera, frame range, and render target for optional `--stage gen_render`.
  — <https://github.com/shigon255/BRDFusion>
5. For relighting or scene edits, set the documented environment variables or JSON specs and invoke `scripts/applications/render.sh` against a staged checkpoint.
  — <https://github.com/shigon255/BRDFusion>

## Best practices

- Start with the supplied data and pretrained checkpoints for inference or evaluation before attempting training or new Waymo-scene preprocessing.
  — <https://github.com/shigon255/BRDFusion>
- Download only the scene subset needed for an experiment; training, rendering, and metrics operate per scene.
  — <https://github.com/shigon255/BRDFusion>
- Keep dataset, scene or path, camera setting, frame range, and render target identical between render and Gen. Render.
  — <https://github.com/shigon255/BRDFusion>
- Use `--dry_run` to inspect selected commands and the pipeline manifest before expensive work; existing stage outputs are skipped unless `--rerun_existing` is supplied.
  — <https://github.com/shigon255/BRDFusion>
- Use `NO_PBR=1` and `PRINT_CMD=1` when checking geometry, camera paths, or generated commands before a full application render.
  — <https://github.com/shigon255/BRDFusion>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- We found no dated primary release note for a code or checkpoint change on 2026-06-22 itself; the date establishes the link event, but not a separate upstream version.
- The repository documents 35 commits without a dated commit history in available research access, so we cannot assign current README capabilities to a post-22-June development event.
- The source code is MIT-licensed, while the checkpoint card is labelled `License: other`; checkpoint and bundled third-party use terms need review before commercial deployment.
- We found no independent reproduction, runtime-performance measurement, or production deployment evidence.

## Sources

| source | title | read |
|---|---|---|
| https://shigon255.github.io/brdfusion-page/ | BRDFusion: Physics Meets Generation for Urban Scene Inverse Rendering — project page | 2026-09-05 |
| https://github.com/shigon255/BRDFusion | shigon255/BRDFusion — official source repository and usage guide | 2026-09-05 |
| https://huggingface.co/Shigon/BRDFusion_checkpoints | Shigon/BRDFusion_checkpoints — official pretrained checkpoints | 2026-09-05 |
| https://arxiv.org/abs/2606.17049 | BRDFusion: Physics Meets Generation for Urban Scene Inverse Rendering — arXiv v1, submitted 2026-06-15 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:brdfusion`, thread `brdfusion`, 1 dated events 2026-06-22 → 2026-06-22.
- **Practical note:** From 2026-06-22, use the linked BRDFusion project page, source repository, and checkpoint collection to evaluate or reproduce the project.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
