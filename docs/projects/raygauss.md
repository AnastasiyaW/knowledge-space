---
title: RayGauss
category: projects
date: 2024-11-17
tags: [project, raygauss]
aliases: ["RayGauss"]
---

# RayGauss

**Development line:** `project:raygauss` · thread `raygauss`  
**Last event:** 2024-11-17 · 2 dated since 2024-08-08 · **Researched:** 2026-09-04 · confidence: high

## What it is

RayGauss is novel view synthesis code and a method for researchers, built as a volumetric alternative to splatting.

- Scene training from multi-view images.
- Volumetric rendering with elliptical Gaussian basis functions, SH and SG features, and BVH/OptiX ray casting.
- PLY export for scene geometry.
- GUI viewer for inspecting trained scenes.

The original paper reports 25 FPS on Blender. It is suitable for reproducing the paper and experimenting on NVIDIA/OptiX, but is not a general production library.

## Development line

- **2024-08-08 — RayGauss public project page referenced.** Gaussian-parametric radiance field with differentiable volumetric ray casting, competing with splatting.
- **2024-11-17 — RayGauss source repository referenced.** On 2024-11-17, the public GitHub repository was linked, without verified claims about code version, contents, or release status.

## What changed

2024-08-08 — RayGauss is published: a Gaussian-parametric radiance field with differentiable volumetric ray casting, competing with splatting. 2024-11-17 — The public implementation repository is available with setup, training, evaluation, PLY export, and GUI. 2025-09-09 — The authors publish RayGaussX, speeding up RayGauss training and rendering on real scenes.

## How to use this

To reproduce or assess RayGauss as of 2024-11-17, start with the public project page and linked GitHub repository, then verify installation, version, and results claims.

1. Install the NVIDIA driver, CUDA, and OptiX 7.6, clone the repository, and create a conda environment from environment.yml; claimed training quality requires a GPU with 24 GB VRAM.
  — <https://github.com/hugobl1/ray_gauss>
2. Prepare the scene in COLMAP structure: images and sparse/0 with cameras.bin, images.bin, and points3D.bin; supported camera models are SIMPLE_PINHOLE and PINHOLE.
  — <https://github.com/hugobl1/ray_gauss>
3. Run single-scene training through main_train.py with a YAML configuration, then evaluate through main_test.py.
  — <https://github.com/hugobl1/ray_gauss>
4. Export the trained scene to PLY through convertpth_to_ply.py and view the result in main_gui.py.
  — <https://github.com/hugobl1/ray_gauss>

## Best practices

- On Windows, match cuda-toolkit and pytorch-cuda versions in environment.yml with installed CUDA; build python-optix from source instead of expecting a conda package.
  — <https://github.com/hugobl1/ray_gauss>
- For reproducible comparisons, place the dataset in dataset/ and run the provided nerf_synth.sh or mip_nerf360.sh script.
  — <https://github.com/hugobl1/ray_gauss>
- Do not assume the reported 25 FPS on Blender holds for real scenes: the authors' next paper notes that RayGauss computational cost prevents real-time rendering on real scenes.
  — <https://arxiv.org/abs/2509.07782>

## Superseded by this

- 2025-09-09 — For real-time tasks on real scenes, the assumption that base RayGauss is fast enough is superseded by RayGaussX; the base implementation remains separate code for the original method.

## Still unknown

- No independent dated primary source for 2024-11-17 adds facts specific to that date beyond describing the current repository state.
- No stable versioned release or supported API exists in available primary sources; verify compatibility on the specific CUDA, OptiX, and driver setup.
- event_findings: [{"event_date":"2024-08-08","finding":"The 2024-08-06 preprint clarifies the method: radiance and density are represented by Gaussian basis functions with spherical harmonics and spherical Gaussians, with slab-by-slab integration via GPU BVH; 25 FPS is reported on the Blender dataset.","source_url":"https://arxiv.org/abs/2408.03356","source_date":"2024-08-06"}]
- new_events: [{"date":"2025-09-09","finding":"The authors introduced RayGaussX: empty-space skipping, adaptive sampling, increased ray coherence, scale regularization, and a new densification criterion; the paper reports 5–12 times faster training, 50–80 times faster rendering, and up to 0.56 dB PSNR gain on real datasets.","source_url":"https://arxiv.org/abs/2509.07782","source_date":"2025-09-09"}]

## Sources

| source | title | read |
|---|---|---|
| https://raygauss.github.io/ | RayGauss: Volumetric Gaussian-Based Ray Casting for Photorealistic Novel View Synthesis | 2026-09-05 |
| https://arxiv.org/abs/2408.03356 | RayGauss: Volumetric Gaussian-Based Ray Casting for Photorealistic Novel View Synthesis | 2026-09-05 |
| https://github.com/hugobl1/ray_gauss | hugobl1/ray_gauss | 2026-09-05 |
| https://arxiv.org/abs/2509.07782 | RayGaussX: Accelerating Gaussian-Based Ray Marching for Real-Time and High-Quality Novel View Synthesis | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:raygauss`, thread `raygauss`, 2 dated events 2024-08-08 → 2024-11-17.
- **Practical note:** As of 2024-11-17, practitioners assessing or attempting to reproduce RayGauss should begin with the public project page and linked GitHub repository, then independently verify installation, version, and results claims.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.