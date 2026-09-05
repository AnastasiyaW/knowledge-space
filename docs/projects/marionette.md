---
title: Marionette — Public project release
category: projects
date: 2026-08-18
tags: [alayalab/marionette, marionette, project, public-project-release]
aliases: ["Marionette"]
---

# Marionette — Public project release

**Development line:** `project:marionette` · thread `public-project-release`  
**Last event:** 2026-08-18 · 1 dated since 2026-08-18 · **Researched:** 2026-09-05 · confidence: high

## What it is

Marionette is an Alaya Lab pipeline for world-model researchers. ActionGPT and PoseGPT predict a 276-dimensional articulated state. A deterministic bridge renders geometry, and fine-tuned Wan2.2-Fun-5B-Control generates RGB video.

- Control: swaps an action token or trajectory root at state level.
- Runtime: requires two Python environments for stage 1 and stage 2.
- Scope: covers one monster type, scans of specific locations, and a non-commercial research license.

The released observation checkpoint is 10.0 GB, and the required third-party base model takes about 23 GB.

This is a reproducible research pipeline, not a general game engine or a ready-made video generation service.

## Development line

- **2026-08-18 — Marionette public project resources were linked.** On 2026-08-18, the project linked its project page, source repository, Hugging Face model page, and hosted world-model space. The release ties together documentation, code, model distribution, and a runnable demonstration.

## What changed

2026-08-13 — The project page, inference code, runtime assets, and controllability demos were published; the full three-stage pipeline became available for local runs. 2026-08-14 — The paper «Marionette: Predicting World States, Rendering Geometry, Painting Appearance» appeared on arXiv, documenting the architecture and claimed state-control results. 2026-08-18 — Project materials, repository code, Hugging Face weights, and the demo came together in one release; the model card specifies the exact base model name, checkpoint sizes, inference settings, and limits.

## How to use this

From 2026-08-18, practitioners should use the linked project page, repository, Hugging Face model page, and hosted space as the starting set for evaluating Marionette. Capabilities, licensing, and reproduction steps still require source research before adoption.

1. Clone the repository, download the Marionette weights and third-party base model, then run `bash run_demo.sh`.
  — <https://huggingface.co/AlayaLab/Marionette>
2. For a split run, create a render environment for stage 1 and a Wan environment for stage 2; run `run_stage1_render.sh`, then `run_stage2_wan.sh`.
  — <https://github.com/AlayaLab/Marionette>
3. Keep the observation checkpoint and its prompt paired; published settings are 704×1280, 40 steps, guidance 6.0, 81-frame chunks, 30 fps.
  — <https://huggingface.co/AlayaLab/Marionette>

## Best practices

- Do not combine stage 1 and stage 2 into one environment: the renderer needs Python 3.12 and EGL, while the diffusion stage requires torch, diffusers, and decord.
  — <https://github.com/AlayaLab/Marionette>
- Pin `TORCH_SEED` for dynamics stage reproducibility; compare runs on one machine by matching output artifacts rather than portable video hashes.
  — <https://github.com/AlayaLab/Marionette>
- Do not transfer action IDs between checkpoints: their meaning depends on the vocabulary of a specific training split.
  — <https://huggingface.co/AlayaLab/Marionette>
- Do not apply the model to new geometry without a fresh terrain scan, and do not treat it as a general character-motion model.
  — <https://huggingface.co/AlayaLab/Marionette>

## Superseded by this

- 2026-08-13 — The roadmap status «pretrained weights uploading» is obsolete: the AlayaLab/Marionette model card now lists published checkpoints and download instructions.

## Still unknown

- Hugging Face Space `hugging-apps/marionette-world-model` returned an internal error during verification, so its live behaviour and maintenance status are unverified.
- The supplied response schema has no `event_findings` or `new_events` fields. The event-specific addition for 2026-08-18 is therefore recorded in `what_changed`; separately dated 2026-08-13 and 2026-08-14 developments are also recorded there.

## Sources

| source | title | read |
|---|---|---|
| https://alayalab.github.io/Marionette/ | Marionette — Predicting World States, Rendering Geometry, Painting Appearance | 2026-09-05 |
| https://github.com/AlayaLab/Marionette | AlayaLab/Marionette repository | 2026-09-05 |
| https://huggingface.co/AlayaLab/Marionette | AlayaLab/Marionette — weights model card | 2026-09-05 |
| https://arxiv.org/abs/2608.14530 | Marionette: Predicting World States, Rendering Geometry, Painting Appearance | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:marionette`, thread `public-project-release`, 1 dated events 2026-08-18 → 2026-08-18.
- **Practical note:** From 2026-08-18, practitioners should use the linked project page, repository, Hugging Face model page, and hosted space as the starting set for evaluating Marionette; capabilities, licensing, and reproduction steps still require source research before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
