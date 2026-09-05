---
title: ID-V2V — Public project resources
category: projects
date: 2026-07-30
tags: [id-v2v, project, public-project-resources]
aliases: ["ID-V2V"]
---

# ID-V2V — Public project resources

**Development line:** `project:id-v2v` · thread `public-project-resources`  
**Last event:** 2026-07-30 · 1 dated since 2026-07-30 · **Researched:** 2026-09-05 · confidence: high

## What it is

ID-V2V is an open-source research pipeline built on Wan2.1 I2V-14B-720P and VACE for video editors. It transforms source video, a stylized first frame, optional keyframes, and a text prompt into a new video while preserving human appearance, expression, gaze, and motion.

- Restyling transfers new visual appearance to the footage.
- Relighting adjusts scene illumination while preserving identity.
- Multi-character handling processes several people in the same scene.
- Extra keyframes guide intermediate character generation.
- Long-video processing divides longer sequences across clips.

Generation runs in 720p, base weights and dependencies take about 96 GB, and the author testbed is 8× A100 80GB. This is a heavy research artifact for local reproducible inference, not a production service.

## Development line

- **2026-07-30 — ID-V2V public project resources were linked.** Official code defines the input directory, preprocess-to-generate workflow, and 720p generation. It processes clips longer than 81 frames using overlapping windows. It provides recipes for restyling, relighting, and keyframes. A model card update from 2026-07-29 notes the base architecture as Wan 2.1 image-to-video with VACE control. The weights are intended only for demonstration and inspiration.

## What changed

2026-07-24 — The arXiv paper "ID-V2V: Identity-Preserving Video Restylization" was published, describing the separation of keyframe-guided synthesis and source-grounded identity preservation through relighting. 2026-07-29 — Hugging Face published two fine-tuned, incompatible checkpoints: the recommended `idv2v.pth` with one SAM3 foreground-on-gray condition and `idv2v_with_normal_depth.pth` with additional normal and depth controls. 2026-07-30 — The release became practically reproducible: official code defines an input directory, preprocess-to-generate workflow, 720p generation, processing clips longer than 81 frames via overlapping clips, and recipes for restyling, relighting, and keyframes. A model card update from 2026-07-29 notes the base architecture as Wan 2.1 image-to-video with VACE control, with weights meant only for demonstration and inspiration.

## How to use this

As of 2026-07-30, practitioners should begin ID-V2V evaluation or reproduction from the linked official project page, source repository, and Hugging Face page, verifying exact capabilities and release status there before use.

1. Clone the repository, create a unified environment with `uv sync`, activate it, and log in to Hugging Face early because SAM3 requires gated access.
  — <https://github.com/Eyeline-Labs/ID-V2V>
2. Download standard checkpoints and dependencies with `bash scripts/download_checkpoints.sh`; add `--with-depth` for the normal and depth variant.
  — <https://github.com/Eyeline-Labs/ID-V2V>
3. Prepare a directory with `source.mp4`, `stylized_first_frame.png`, and `prompt.txt`; add `keyframes/<frame_number>.png` when needed.
  — <https://github.com/Eyeline-Labs/ID-V2V>
4. For the standard model, run preprocessing with the SAM3 text prompt, then run inference; relighting uses a separate path without preprocessing.
  — <https://github.com/Eyeline-Labs/ID-V2V>
5. For long source footage, add keyframes and use the longer-video recipe: the system joins clips across overlapping boundary frames.
  — <https://github.com/Eyeline-Labs/ID-V2V>

## Best practices

- Match each checkpoint to its variant script: matching architecture raises no error on an invalid pair, but output silently degrades.
  — <https://huggingface.co/Eyeline-Labs/ID-V2V>
- Use more keyframes on long videos so drift between clips stays low.
  — <https://github.com/Eyeline-Labs/ID-V2V>
- Treat results as experimental, verifying identity preservation, facial expressions, and lip-sync on your own footage before production use.
  — <https://huggingface.co/Eyeline-Labs/ID-V2V>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The provided schema omits `event_findings` and `new_events`; their verifiable details sit in `what_changed`.
- Official materials describe reproducible inference, but lack confirmed production support, a public hosted API, or minimum GPU requirements.

## Sources

| source | title | read |
|---|---|---|
| https://eyeline-labs.github.io/ID-V2V/ | ID-V2V: Identity-preserving Video Restylization | 2026-09-05 |
| https://github.com/Eyeline-Labs/ID-V2V | Eyeline-Labs/ID-V2V | 2026-09-05 |
| https://huggingface.co/Eyeline-Labs/ID-V2V | Eyeline-Labs/ID-V2V | 2026-09-05 |
| https://arxiv.org/abs/2607.22830 | ID-V2V: Identity-Preserving Video Restylization | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:id-v2v`, thread `public-project-resources`, 1 dated events 2026-07-30 → 2026-07-30.
- **Practical note:** As of 2026-07-30, practitioners should begin ID-V2V evaluation or reproduction from the linked official project page, source repository, and Hugging Face page, verifying exact capabilities and release status there before use.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.