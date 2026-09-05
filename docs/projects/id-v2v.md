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

ID-V2V is an open-source research pipeline built on Wan2.1 I2V-14B-720P and VACE for video editors. It turns a source video, a stylized first frame, optional keyframes, and a text prompt into a new video while preserving identity, facial expression, gaze, and human motion.

Abilities:
- Restyling: applies target style from keyframes to the source video.
- Relighting: preserves subject identity across changed lighting.
- Multiple characters: handles scenes containing more than one person.
- Extra keyframes: provides intermediate anchor frames to guide synthesis.
- Long video processing: splits long source video into overlapping clips.

Generation runs at 720p, the base weights and dependencies take around 96 GB, and the authors test on 8× A100 80GB. This is a heavy research artifact for local reproducible inference, not a finished service.

## Development line

- **2026-07-30 — ID-V2V public project resources were linked.** The official code specifies the input directory, a preprocess-to-generate workflow, 720p generation, clip processing for videos over 81 frames with overlapping boundaries, and recipes for restyling, relighting, and keyframes. A model card update from 2026-07-29 notes the base architecture is Wan 2.1 image-to-video with VACE control; the weights are released only for demonstration and inspiration.

## What changed

- 2026-07-24 — The arXiv paper "ID-V2V: Identity-Preserving Video Restylization" was published, describing decoupled keyframe-guided synthesis and source-grounded identity preservation through relighting.
- 2026-07-29 — Two fine-tuned, mutually incompatible checkpoints were published on Hugging Face: the recommended `idv2v.pth` with a single SAM3 foreground-on-gray condition, and `idv2v_with_normal_depth.pth` with additional normal and depth controls.
- 2026-07-30 — The release became practically reproducible. Official code specifies the input directory, a preprocess-to-generate workflow, 720p generation, clip processing for videos over 81 frames with overlapping boundaries, and recipes for restyling, relighting, and keyframes. A model card update from 2026-07-29 notes the base architecture is Wan 2.1 image-to-video with VACE control; the weights are released only for demonstration and inspiration.

## How to use this

As of 2026-07-30, practitioners should begin ID-V2V evaluation or reproduction from the linked official project page, source repository, and Hugging Face page, verifying exact capabilities and release status there before use.

1. Clone the repository, create a unified environment with `uv sync`, activate it, and log into Hugging Face: SAM3 requires gated model access.
  — <https://github.com/Eyeline-Labs/ID-V2V>
2. Download standard checkpoints and dependencies with `bash scripts/download_checkpoints.sh`; for the normal and depth variant, append `--with-depth`.
  — <https://github.com/Eyeline-Labs/ID-V2V>
3. Prepare a directory with `source.mp4`, `stylized_first_frame.png`, and `prompt.txt`; add `keyframes/<frame_number>.png` if needed.
  — <https://github.com/Eyeline-Labs/ID-V2V>
4. For the standard model, run preprocessing with a SAM3 text prompt, then run inference; relighting uses a separate path without preprocessing.
  — <https://github.com/Eyeline-Labs/ID-V2V>
5. For long source video, add keyframes and use the longer-video recipe: the pipeline joins clips across an overlapping boundary frame.
  — <https://github.com/Eyeline-Labs/ID-V2V>

## Best practices

- Match each checkpoint to its corresponding script: the shared architecture raises no error on a mismatched pair, but output silently degrades.
  — <https://huggingface.co/Eyeline-Labs/ID-V2V>
- Use more keyframes on long videos so drift between clips stays low.
  — <https://github.com/Eyeline-Labs/ID-V2V>
- Treat output as experimental: verify identity preservation, facial expressions, and lip-sync on your own footage before production use.
  — <https://huggingface.co/Eyeline-Labs/ID-V2V>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The schema provides no `event_findings` or `new_events` fields; verifiable details are merged into the `what_changed` chronology.
- Official materials describe reproducible inference, but list no confirmed production support, public hosted API, or minimum GPU specification.

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