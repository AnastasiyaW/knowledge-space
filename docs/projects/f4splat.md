---
title: F⁴Splat
category: projects
tags: [f4splat, f4splat-development, project]
aliases: ["F⁴Splat"]
---

# F⁴Splat

**Development line:** `project:f4splat` · thread `f4splat-development`  
**Events:** 2 dated, 2026-03-30 → 2026-07-24 · **Researched:** 2026-09-04 · confidence: medium

## What it is

F⁴Splat is a 3DGS research framework for developers synthesizing novel views from sparse uncalibrated images. It is a code alternative to AnySplat for CUDA research, not a finished cloud service or universal 3D scanner.

- Camera and parameter prediction: predicts camera poses, Gaussian parameters, and densification score maps.
- Primitive allocation: distributes Gaussian primitives by scene complexity and cross-view overlaps.
- Budget scaling: changes the target Gaussian budget at inference without retraining.

The local demo takes 2–16 images; published weights cover ACID 2-view and RealEstate10K 2-/24-view.

## Development line

- **2026-03-30 — F⁴Splat project page published.** F⁴Splat appeared on its public project page on 2026-03-30. A reference to level-of-detail graphics framed the announcement in rendering development. The page gave no exact technical claims or release status.
- **2026-07-24 — F⁴Splat GitHub repository linked.** The development line linked the F⁴Splat GitHub repository on 2026-07-24 alongside the March announcement. This opened public access to source code. The post did not specify which code, version, or implementation changes appeared on that date.

## What changed

- **2026-03-30:** The project page described the method. Instead of uniform pixel- or voxel-to-Gaussian distribution, the model allocates primitives by predicted density.
- **2026-06-30:** The official commit "Release public code" added 181 files with demo, training, evaluation, and source code. The method became a reproducible local workflow.
- **2026-07-24:** The link pointed to the official repository, but the source recorded no separate technical change on that day. The nearest confirmed code release remains 30 June.
- **2026-09-03:** The arXiv paper updated to v3. The page provides no description of differences, so we cannot claim new features or altered results from this revision.

## How to use this

As of 2026-07-24, consult the F⁴Splat project page for context and the linked GitHub repository for source access. Treat precise capabilities and version status as unverified pending research.

1. Clone the repository, create a Python 3.11 environment, install PyTorch 2.8.0 for CUDA 12.8, and install project dependencies.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
2. Download the Hub checkpoint matching the target dataset and context view count: `acid-2view`, `re10k-2view`, or `re10k-24view`.
  — <https://huggingface.co/Knowing/F4Splat>
3. Run `python demo/app.py`, upload 2–16 images, and select a Gaussian budget to compare renders.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
4. For experiments, prepare the dataset in PyTorch chunk format with `index.json`, then run the supplied training or evaluation scripts with GPU ID and checkpoint path.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>

## Best practices

- Match the PyTorch wheel to the installed CUDA version first. If CUDA is not 12.8, install matching PyTorch before other dependencies.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
- Choose checkpoints by dataset and context view count. Do not treat published weights as a universal model for arbitrary scenes.
  — <https://huggingface.co/Knowing/F4Splat>
- Evaluate the Gaussian budget by actual primitive count. The demo renders interpolation-only video and marks results with true Gaussian counts in thousands.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
- Follow the license and access terms for RealEstate10K, DL3DV, and ACID when training.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>

## Superseded by this

- 2026-06-30: Treating F⁴Splat solely as a paper or project page is obsolete. Official source code is available with demo, training, and evaluation scripts.
- 2026-09-03: Cite arXiv v3 instead of v1/v2 for current research citations. This revision does not demonstrate runtime capability changes.

## Still unknown

- Primary source text was not readable, leaving any separate release claim for 2026-07-24 unextracted.
- The 2026-09-03 arXiv v3 preprint includes no change note, leaving differences from v1/v2 unconfirmed.
- Official materials provide no independent quality evaluation on user captures, runtime speed, or GPU memory usage.

## Sources

| source | title | read |
|---|---|---|
| https://mlvlab.github.io/F4Splat/ | F⁴Splat | 2026-09-04 |
| https://github.com/mlvlab/F4Splat | mlvlab/F4Splat | 2026-09-04 |
| https://github.com/mlvlab/F4Splat/commits/main | Commits · mlvlab/F4Splat | 2026-09-04 |
| https://github.com/mlvlab/F4Splat/commit/127ed096c1ab7c4aa65431dc659bc08592adbb22 | Release public code · mlvlab/F4Splat@127ed09 | 2026-09-04 |
| https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md | F4Splat README | 2026-09-04 |
| https://huggingface.co/Knowing/F4Splat | Knowing/F4Splat | 2026-09-04 |
| https://arxiv.org/abs/2603.21304 | F4Splat: Feed-Forward Predictive Densification for Feed-Forward 3D Gaussian Splatting | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:f4splat`, thread `f4splat-development`, 2 dated events 2026-03-30 → 2026-07-24.
- **Practical note:** As of 2026-07-24, consult the F⁴Splat project page for context and the linked GitHub repository for source access, while treating precise capabilities and version status as unverified pending research.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.