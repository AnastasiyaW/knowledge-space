---
title: GUSH3R
category: projects
date: 2026-07-08
tags: [gush3r, gush3r-development, project]
aliases: ["GUSH3R"]
---

# GUSH3R

**Development line:** `project:gush3r` · thread `gush3r-development`  
**Last event:** 2026-07-08 · 1 dated since 2026-07-08 · **Researched:** 2026-09-05 · confidence: high

## What it is

GUSH3R is research code for novel-view rendering of people moving in a scene from monocular video, replacing a separate AnySplat background plus LHM human pipeline.

- Static scene Gaussians: reconstructs the background.
- Dynamic human Gaussians: reconstructs moving people.
- Shared metric-space render: unifies background and human geometry.
- Causal frame processing: processes frames causally and can use recurrent TTT3R updates.

The downloadable merged checkpoint is 4.87 GB, and inference additionally requires separately licensed SMPL/SMPL-X assets.

We can use it for research reproduction and controlled video experiments. It is not a robust production capture pipeline because errors in pose, camera, detection, and occluded identities propagate to the result.

## Development line

- **2026-07-08 — GUSH3R public project resources linked.** On 2026-07-08, the GUSH3R development line was associated with a public project page, a source-code repository, and a Hugging Face resource. These links open public access to the project without establishing further technical details.

## What changed

2026-07-08 — The first public research release of GUSH3R pairs code, a merged `gush3r.pth` inference checkpoint, and a project page. The associated arXiv v1, submitted on 2026-07-06, identifies the method as Gaussian-Unified Scene Human 3D Reconstruction. The release adds a single-pass, streaming 3D-Gaussian representation for static scenes and dynamic humans. It reports 1.70 FPS on its single-human benchmark and 1.45 FPS on its multi-human BEDLAM benchmark.

## How to use this

From 2026-07-08, we can assess GUSH3R through the linked project page, source repository, and Hugging Face resource. Their contents remain unresearched in this review.

1. Clone the repository, create the recommended Python 3.10 environment, install CUDA 12.1 PyTorch, requirements, PyTorch3D, and the Gaussian rasterizer.
  — <https://github.com/abkeito/GUSH3R>
2. Download `checkpoints/gush3r.pth` from the model repository, obtain licensed SMPL and SMPL-X assets, and run the supplied body-model helper.
  — <https://github.com/abkeito/GUSH3R>
3. Run `infer.py` on a monocular video; begin with `--max_frames 3`, then inspect `outputs/<name>/render.mp4`.
  — <https://github.com/abkeito/GUSH3R>

## Best practices

- Run the three-frame smoke test before a full sequence, and use `--subsample` to reduce sequence load during diagnosis.
  — <https://github.com/abkeito/GUSH3R>
- Review outputs manually when encountering identity association, severe person-to-person occlusion, motion blur, large pose changes, faces, hands, and clothing texture.
  — <https://arxiv.org/html/2607.05243v1>
- Control accumulated background complexity with `--bg_gaussian_max`, mask threshold, and voxel size rather than allowing unbounded scene growth.
  — <https://github.com/abkeito/GUSH3R>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No later official release, benchmark replication, hardware-specific inference requirement, or maintained production-support policy was found in the reviewed first-party materials.

## Sources

| source | title | read |
|---|---|---|
| https://abkeito.github.io/gush3r-page/ | GUSH3R: Everyone Everywhere All at Once as Gaussians | 2026-09-05 |
| https://github.com/abkeito/GUSH3R | abkeito/GUSH3R | 2026-09-05 |
| https://huggingface.co/abkeito/GUSH3R/tree/main | abkeito/GUSH3R model files | 2026-09-05 |
| https://arxiv.org/abs/2607.05243 | GUSH3R: Everyone Everywhere All at Once as Gaussians | 2026-09-05 |
| https://arxiv.org/html/2607.05243v1 | GUSH3R paper, HTML version | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:gush3r`, thread `gush3r-development`, 1 dated events 2026-07-08 → 2026-07-08.
- **Practical note:** From 2026-07-08, practitioners can use the linked project page, source repository, and Hugging Face resource as the dated public entry points for assessing GUSH3R; their contents remain unresearched in this review.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
