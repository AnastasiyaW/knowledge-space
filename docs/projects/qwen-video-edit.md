---
title: Qwen-Video-Edit
category: projects
date: 2026-08-18
tags: [project, qwen-video-edit]
aliases: ["Qwen-Video-Edit"]
---

# Qwen-Video-Edit

**Development line:** `project:qwen-video-edit` · thread `qwen-video-edit`  
**Last event:** 2026-08-18 · 1 dated since 2026-08-18 · **Researched:** 2026-09-05 · confidence: high

## What it is

Qwen-Video-Edit provides code and checkpoints for instruction-based video editing without a video-pretrained transformer. Qwen-Image-Edit edits the latent representation of Wan 2.1 VAE, while Wan 2.2 can clean up the result.

- Frame consistency to keep edits stable across the video.
- Per-chunk instructions to assign an individual prompt to each segment of a long clip.
- CLI and ComfyUI workflows for local runs.

One checkpoint takes about 40 GB, base weights and enhancement require about 55 GB of storage, and the 720P checkpoint has less training than the others.
Start with 360P/step-30000 for a first run, and use 480P/global_local_81 for 81-frame chunks.

## Development line

- **2026-08-18 — Qwen-Video-Edit was publicly presented with project, code, and model links.** On 2026-08-18, the authors published the project page, GitHub repository, and Hugging Face resource so users can evaluate and run the models.

## What changed

- 2026-08-18 — The initial release published the code, report, project page, and a 360P checkpoint; the README dates the initial release to 2026-08-14.
- 2026-08-20 — The authors added 480P checkpoints across data subsets, an 81-frame variant, and 720P weights, alongside custom nodes for ComfyUI.

## How to use this

From 2026-08-18, evaluate Qwen-Video-Edit through the project page, repository, and Hugging Face resource, checking capabilities, installation, licensing, and model details before adoption.

1. Create a Python 3.10–3.12 environment with a CUDA build of PyTorch, install requirements.txt, and set DIFFSYNTH_MODEL_BASE_PATH.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
2. Download the recommended 360P/step-30000 checkpoint and base weights, or let the loader fetch them on first run.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
3. Run infer.py with the input video, prompts.txt, and matching checkpoint, num_frames, and video_max_pixels settings, where each line in prompts.txt maps to one segment.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
4. For ComfyUI, install the repository into custom_nodes, import the workflow, and set paths to the checkpoint and Wan 2.2.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>

## Best practices

- Run commands from the repository root so the bundled diffsynth and wan packages take precedence over external packages.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
- Match num_frames, video_max_pixels, latent_mode, and pe_mode to the checkpoint table, because mismatched values are unsupported.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
- Start with 360P/step-30000 as the safest lightweight default; 720P trained for only 3,500 steps, so drop back to 480P or 360P if outputs degrade.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
- Split long videos into chunks and assign an individual prompt to each; keep skip_enhance for debugging only.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>

## Superseded by this

- 2026-08-20 — The initial single 360P checkpoint is no longer the complete model inventory: releases now include 480P, 81-frame, and 720P variants alongside ComfyUI integration.

## Still unknown

- The target schema omits event_findings and new_events fields, so the dated clarification for 2026-08-18 and the separate 2026-08-20 event appear in what_changed and supersedes instead.
- Independent benchmarks have not verified visual quality, VRAM requirements, or reliability on arbitrary input video; current data comes solely from the project authors.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/yunpeng1998/Qwen-Video-Edit | Qwen-Video-Edit — GitHub repository and README | 2026-09-05 |
| https://yunpeng1998.github.io/Qwen-Video-Edit-Page/ | Qwen-Image Video-Edit — project page | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen-video-edit`, thread `qwen-video-edit`, 1 dated events 2026-08-18 → 2026-08-18.
- **Practical note:** From 2026-08-18, practitioners should use the linked project page, repository, and Hugging Face resource as the starting point for evaluating Qwen-Video-Edit, while verifying capabilities, installation, licensing, and model details from those sources before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
