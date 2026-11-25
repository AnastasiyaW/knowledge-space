---
title: UPAL
category: projects
date: 2026-08-24
tags: [project, upal, upal-development]
aliases: ["UPAL"]
---

# UPAL

**Development line:** `project:upal` · thread `upal-development`  
**Last event:** 2026-08-24 · 1 dated since 2026-08-24 · **Researched:** 2026-09-05 · confidence: medium

## What it is

UPAL is a standalone PyTorch feature extractor for CV and SLAM practitioners. It combines point detection, line detection, and local descriptors in one network.

- sub-pixel keypoints and confidence scores;
- 128-dimensional L2-normalized descriptors;
- keypoint heatmaps and line-distance fields, with bundled `points_lsd` post-processing for segments.

## Development line

- **2026-08-24 — UPAL GitHub repository referenced.** The repository appeared publicly, but no first-party commit, tag, or release ties to this date, so it does not establish a new version.

## What changed

2026-08-20: arXiv v1 introduced UPAL as a shared-backbone point-line feature extractor with public code. It reported roughly 4× speedup and a 10× smaller memory footprint than ALIKED + DeepLSD. 2026-08-24: UPAL's repository appeared publicly, but no first-party commit, tag, or release ties to this date, so it does not establish a new version.

## How to use this

As of 2026-08-24, start from the UPAL GitHub repository for project research, because the evidence supports no narrower operational guidance.

1. Check out the repository, make a Python 3.10+ environment, and install the package with `pip install -e .`.
  — <https://github.com/francois141/upal>
2. Initialize recursive submodules and install `third_party/points_lsd`. For CUDA, install the matching PyTorch build before building that extension.
  — <https://github.com/francois141/upal>
3. Run `demo_inference.py`, `demo_match_points.py`, and `demo_match_lines.py` to test the supported inference, point-matching, and line-matching paths.
  — <https://github.com/francois141/upal>
4. To use UPAL in an application, load `weights/upal.tar`, pass a normalized `[0,1]` tensor shaped `B×1×H×W` or `B×3×H×W`, and read out keypoints, descriptors, heatmaps, and the line-distance field.
  — <https://github.com/francois141/upal>

## Best practices

- Install a CUDA-compatible PyTorch build before compiling `points_lsd`, because the line path depends on that native submodule.
  — <https://github.com/francois141/upal>
- Test all three bundled demos before integration, because inference, point matching, and line matching are separate supported paths.
  — <https://github.com/francois141/upal>
- Do not generalize the speed figure across deployments: the published 70 ms result used 500 sequential 800×800 images, batch size one, and an RTX 2080 Ti.
  — <https://arxiv.org/html/2608.19894v1>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- We found no primary-source commit, tag, or release dated 2026-08-24, so we cannot treat that date as a version release.
- The repository documents standalone inference and demos, not a supported production service, training workflow, or operating-system matrix.
- We found no verified community installation report, so target-runtime builds and performance remain untested.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/francois141/upal | GitHub - francois141/upal: Unified point and line detector | 2026-09-05 |
| https://arxiv.org/abs/2608.19894 | Unified and Efficient Point-Line Local Features | 2026-09-05 |
| https://arxiv.org/html/2608.19894v1 | Unified and Efficient Point-Line Local Features — arXiv HTML v1 | 2026-09-05 |
| https://www.x-techcon.com/article/178188.html | SLAM优化新方向：UPAL统一点线特征，提速4倍内存小10倍 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:upal`, thread `upal-development`, 1 dated events 2026-08-24 → 2026-08-24.
- **Practical note:** As of 2026-08-24, start from the UPAL GitHub repository for project research, because the evidence supports no narrower operational guidance.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.