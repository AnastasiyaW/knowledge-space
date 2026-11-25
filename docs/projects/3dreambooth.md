---
title: 3DreamBooth
category: projects
date: 2026-03-21
tags: [3dreambooth, 3dreambooth-development, project]
aliases: ["3DreamBooth"]
---

# 3DreamBooth

**Development line:** `project:3dreambooth` · thread `3dreambooth-development`  
**Last event:** 2026-03-21 · 1 dated since 2026-03-21 · **Researched:** 2026-09-07 · confidence: medium

## What it is

3DreamBooth is a research codebase for adapting HunyuanVideo-1.5 to a subject captured from multiple viewpoints.

- 3DreamBooth: one-frame, per-subject LoRA optimization for spatial identity.
- 3Dapter: a reference-image conditioning adapter jointly optimized with the subject LoRA.

The paper reports 720p, 81-frame, 50-step outputs; the public repository still marks evaluation code unavailable. Use it for controlled reproduction or supplied-checkpoint inference, not as a turnkey production package.

## Development line

- **2026-03-21 — 3DreamBooth project resources were publicly linked.** On 2026-03-21, an entry linked the 3DreamBooth project website and its GitHub source repository. We treat this as a public reference point for project history. We do not infer an unevidenced release, feature, or other change.

## What changed

- 2026-03-19 — arXiv v1 introduced 3DreamBooth, 3Dapter, and 3D-CustomBench.
- 2026-03-20 — The repository records its initial commit, removes the Code Coming Soon badge, and uploads source files.
- 2026-03-21 — The project page and repository were linked for the dated event. We have no independent verification of an official launch date.
- 2026-07-22 — Hugging Face listed the 3D-CustomBench dataset as updated.
- 2026-07-28 — Hugging Face listed the 3DreamBooth-CustomBench checkpoint collection as updated.

## How to use this

1. Clone the repository, create its Python 3.10 environment, and install the declared requirements.
  — <https://github.com/Ko-Lani/3DreamBooth>
2. Download HunyuanVideo-1.5, its text and vision dependencies, and the pretrained 3Dapter. Obtain access to gated FLUX.1-Redux-dev before launching a job.
  — <https://github.com/Ko-Lani/3DreamBooth>
3. For a ready-made trial, download one of the 30 joint CustomBench checkpoint pairs and use its exact identifier-plus-class trigger phrase.
  — <https://huggingface.co/lanikoworld/3DreamBooth-CustomBench>
4. For a custom subject, prepare ordered multi-view captures in images/ and a smaller set of background-removed, white-normalized square references in references/.
  — <https://github.com/Ko-Lani/3DreamBooth>
5. Run the supplied YAML configuration with --dry-run first, then use the 3dreambooth baseline or joint mode as appropriate.
  — <https://github.com/Ko-Lani/3DreamBooth/blob/main/docs/training-modes.md>
6. Keep generated video length at 4n + 1, such as 49, 81, or 129 frames. Do not treat a visual run as official metric reproduction while evaluation code is absent.
  — <https://github.com/Ko-Lani/3DreamBooth>

## Best practices

- Start with a supplied CustomBench checkpoint before attempting custom training. It isolates environment and prompt errors from subject-training errors.
  — <https://huggingface.co/lanikoworld/3DreamBooth-CustomBench>
- Use diverse, ordered views and references covering the full 360-degree extent of the object. Remove reference backgrounds before conditioning.
  — <https://arxiv.org/html/2603.18524>
- Keep the bracketed identifier-plus-class phrase identical across training and validation. The literal phrase is the LoRA span that activates identity.
  — <https://huggingface.co/lanikoworld/3DreamBooth-CustomBench>
- Validate YAML resolution with --dry-run before loading large checkpoints or starting distributed training.
  — <https://github.com/Ko-Lani/3DreamBooth/blob/main/docs/training-modes.md>
- Check FLUX access and Hunyuan-derived licensing terms before committing to a workflow or commercial use.
  — <https://github.com/Ko-Lani/3DreamBooth>

## Superseded by this

- 2026-03-20 — The initial Code Coming Soon state is obsolete: repository history records its removal and source-file uploads.

## Still unknown

- We found no immutable tag or GitHub Release for the exact code state on 2026-03-21, so we cannot pin that revision from inspected public pages.
- The July Hugging Face labels establish update dates, but not the exact file-level changes made on those dates.
- We performed no local installation, GPU-memory measurement, throughput test, or independent metric reproduction; official evaluation code remains unavailable.
- We found no first-party Simplified Chinese documentation or official Chinese community guidance; current practical guidance rests on English primary sources.

## Sources

| source | title | read |
|---|---|---|
| https://ko-lani.github.io/3DreamBooth/ | 3DreamBooth | 2026-09-07 |
| https://github.com/Ko-Lani/3DreamBooth | Ko-Lani/3DreamBooth | 2026-09-07 |
| https://arxiv.org/abs/2603.18524 | 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model | 2026-09-07 |
| https://arxiv.org/html/2603.18524 | 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model — HTML | 2026-09-07 |
| https://github.com/Ko-Lani/3DreamBooth/commits/main | Commits · Ko-Lani/3DreamBooth | 2026-09-07 |
| https://github.com/Ko-Lani/3DreamBooth/blob/main/docs/training-modes.md | Training and validation modes | 2026-09-07 |
| https://huggingface.co/lanikoworld/3DreamBooth-CustomBench | 3DreamBooth-CustomBench Checkpoints | 2026-09-07 |
| https://huggingface.co/datasets/lanikoworld/3D-CustomBench | 3D-CustomBench | 2026-09-07 |
| https://huggingface.co/papers/2603.18524 | Paper page — 3DreamBooth: High-Fidelity 3D Subject-Driven Video Generation Model | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:3dreambooth`, thread `3dreambooth-development`, 1 dated events 2026-03-21 → 2026-03-21.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.