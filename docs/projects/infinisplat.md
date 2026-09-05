---
title: InfiniSplat
category: projects
date: 2026-08-07
tags: [infinisplat, infinisplat-public-availability, project]
aliases: ["InfiniSplat"]
---

# InfiniSplat

**Development line:** `project:infinisplat` · thread `infinisplat-public-availability`  
**Last event:** 2026-08-07 · 1 dated since 2026-08-07 · **Researched:** 2026-09-05 · confidence: high

## What it is

InfiniSplat turns one RGB image, or an aligned RGB-depth pair, into a 3D Gaussian scene for novel-view rendering. It offers RGB-only and depth-sensor-guided modes. The released workflow is single-image rather than multi-view reconstruction. We use it for fast spatial-photo output, not metric scene capture from arbitrary imagery.

## Development line

- **2026-08-07 — InfiniSplat public project resources were documented.** Checkpoint `infinisplat_rgb.ckpt` handles RGB-only input, and `infinisplat_lidar.ckpt` handles aligned RGB plus depth. The method uses geometry-guided supports and query-conditioned implicit Gaussian decoding.

## What changed

- 2026-08-03 — arXiv v1 introduced InfiniSplat: Implicit Gaussian Decoding for Large-Baseline Monocular View Synthesis.
- 2026-08-04 — arXiv v2 revised the paper.
- 2026-08-07 — Released code and demo exposed two complete checkpoints: `infinisplat_rgb.ckpt` for RGB-only input and `infinisplat_lidar.ckpt` for aligned RGB plus depth. The method uses geometry-guided supports and query-conditioned implicit Gaussian decoding.

## How to use this

From 2026-08-07, we use the linked InfiniSplat project page, repository, and Hugging Face Space to assess the project, inspect its implementation, and try its public interface before adoption.

1. Create the documented Python 3.10 environment, install the CUDA 12.8 PyTorch dependencies, then download the two checkpoints.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/INSTALL.md>
2. Run RGB-only inference on one image or a directory with `python -m src.demo.infer_batch_images --input PATH`.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/README.md>
3. For depth-guided reconstruction, supply spatially aligned RGB and depth files with matching stems and use `--mode lidar`.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>
4. Use the exported PLY as the baseline artifact. Optionally install gsplat for MP4 renders or splat-transform for interactive HTML.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>

## Best practices

- Provide camera intrinsics or focal length when known. Otherwise the runner falls back to a fixed 30 mm full-frame-equivalent focal length.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>
- Use depth aligned to the RGB image, expressed as depth rather than disparity. Valid decoded values must be finite and strictly between 1 and 100.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>
- Avoid `--overwrite` when outputs are already valid: the runner skips completed artifacts and only creates a missing requested artifact.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>

## Superseded by this

- 2026-08-04 — arXiv v2 supersedes the 2026-08-03 v1 preprint.
- 2026-08-07 — We treat InfiniSplat as a released two-mode inference workflow, not only a paper or preview.

## Still unknown

- No independently dated post-2026-08-07 InfiniSplat release was verified. The project page has an undated InfiniSplat V2 multi-view preview, so we do not treat it as a released successor.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2608.02437 | InfiniSplat: Implicit Gaussian Decoding for Large-Baseline Monocular View Synthesis | 2026-09-05 |
| https://zju3dv.github.io/InfiniSplat/ | InfiniSplat project page | 2026-09-05 |
| https://github.com/zju3dv/InfiniSplat/blob/main/README.md | InfiniSplat README | 2026-09-05 |
| https://github.com/zju3dv/InfiniSplat/blob/main/INSTALL.md | InfiniSplat installation guide | 2026-09-05 |
| https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md | InfiniSplat inference guide | 2026-09-05 |
| https://huggingface.co/spaces/PLUS-WAVE/InfiniSplat | PLUS-WAVE InfiniSplat hosted demo | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:infinisplat`, thread `infinisplat-public-availability`, 1 dated events 2026-08-07 → 2026-08-07.
- **Practical note:** From 2026-08-07, we use the linked InfiniSplat project page, repository, and Hugging Face Space to assess the project, inspect its implementation, and try its public interface before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.