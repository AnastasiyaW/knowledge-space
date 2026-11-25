---
title: Holi-Spatial
category: projects
date: 2026-03-10
tags: [holi-spatial, holi-spatial-development, project]
aliases: ["Holi-Spatial"]
---

# Holi-Spatial

**Development line:** `project:holi-spatial` · thread `holi-spatial-development`  
**Last event:** 2026-03-10 · 1 dated since 2026-03-10 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Holi-Spatial is a public data-preparation pipeline for research teams that need 3D Gaussian Splatting, masks, 3D boxes, and spatial QA from ScanNet, ScanNet++, or DL3DV scenes.

- Depth and point clouds: builds depth and point clouds with DA3, then runs PGSR/3DGS.
- Object annotation and QA: segments objects with SAM3 and a VLM, lifts masks to 3D, and generates QA.
- Multimodal dataset export: converts the output into an SFT dataset for LLaMA-Factory.

12K optimized 3DGS scenes and over 4M spatial annotations in the paper; the available HoliSpatial-2M-QA-Qwen3-VL-8B checkpoint is a BF16 model with 9B parameters and 17.6 GB.

This is an offline pipeline for curation and training with CUDA, external models, and your own scenes, not an interactive 3D service.

## Development line

- **2026-03-10 — Holi-Spatial project resources were shared.** On 2026-03-10, Holi-Spatial was linked to a public project page, source repository, and Hugging Face resource. This is a material public-development reference point, although the available evidence does not establish the precise release status or capabilities of the linked resource.

## What changed

- 2026-03-08 — arXiv v1 published: describes a three-stage automated pipeline and Holi-Spatial-4M.
- 2026-03-10 — Holi-Spatial received a public project page and repository for video spatial annotation, claiming 13K+ scenes, 1.3M+ QA, and 300K+ 3D boxes.
- 2026-03-19 — the official Hugging Face page marks the ScanNetPP dataset as updated.
- 2026-03-21 — the official Hugging Face page marks the ScanNet_v2 dataset as updated.
- 2026-03-22 — the official Hugging Face page marks HoliSpatial-QA-2M as updated.
- 2026-03-29 — the official Hugging Face page marks HoliSpatial-2M-QA-Qwen3-VL-8B as an updated 9B checkpoint.
- 2026-04-21 — the official Hugging Face page marks HoliSpatial-3D-Grounding as updated.

## How to use this

From 2026-03-10, practitioners should use the linked project page, repository, and Hugging Face resource as the starting point for evaluating Holi-Spatial, while independently verifying the exact artifact, version, and usage instructions.

1. Create a CUDA-enabled Python environment and install requirements with the two PGSR submodules.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
2. Prepare one scene in the expected ScanNet, ScanNet++, or DL3DV structure; add covisibility root for QA.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
3. Run DA3 on one scene through SCENE_DIR first; check depth_da3 and pointcloud_da3.ply.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
4. Train PGSR/3DGS, then generate mesh and mesh-guided masks.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
5. Start an OpenAI-compatible vLLM endpoint, run object/region annotation with SAM3, postprocess AABB, generate QA, and convert to LLaMA-Factory dataset.jsonl.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>

## Best practices

- Start with one scene and check intermediate artifacts: batch scripts treat a scene as complete if a final JSON or trained point cloud already exists.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
- Set up CUDA, Depth Anything 3, SAM3 assets, and an OpenAI-compatible vLLM endpoint explicitly instead of relying on implicit dependencies.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
- Keep VLM verification for borderline instances: confidence filtering increases precision but can discard valid complex objects.
  — <https://arxiv.org/abs/2603.07660>
- Do not transfer results unverified to video with motion blur, heavy occlusion, few viewpoints, or dynamic objects: the authors list these as pipeline limits.
  — <https://arxiv.org/abs/2603.07660>

## Superseded by this

- 2026-03-10 — The 'Data (coming soon)' and 'Benchmark (coming soon)' status on the project page no longer reflects availability: the repository reports a released data subset and checkpoint, and the Hugging Face organization now hosts four datasets and one model. This does not prove availability of the full Holi-Spatial-4M.

## Still unknown

- The March/April dates on the Hugging Face organization page are last-update dates rather than confirmed initial release dates: commit history pages were unavailable.
- The project page still lists data and benchmark as 'coming soon', while the README and Hugging Face show available artifacts. Whether this note refers to the full Holi-Spatial-4M or is simply outdated remains unclear.
- The checkpoint lacks a model card and a hosted inference provider; the exact prompt template, supported inputs, and recommended runtime remain unconfirmed.
- Neither the repository nor the model page lists an explicit license for code, datasets, or weights.

## Sources

| source | title | read |
|---|---|---|
| https://visionary-laboratory.github.io/holi-spatial/ | Holi-Spatial | Holistic Spatial Intelligence | 2026-09-06 |
| https://github.com/Visionary-Laboratory/Holi-Spatial | GitHub - Visionary-Laboratory/Holi-Spatial: Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence | 2026-09-06 |
| https://arxiv.org/abs/2603.07660 | Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence | 2026-09-06 |
| https://huggingface.co/Holi-Spatial | Holi-Spatial (Visionary Laboratory) | 2026-09-06 |
| https://huggingface.co/Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B | Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B | 2026-09-06 |
| https://huggingface.co/Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B/tree/main | Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B at main | 2026-09-06 |
| https://huggingface.co/datasets/Holi-Spatial/HoliSpatial-QA-2M | Holi-Spatial/HoliSpatial-QA-2M | 2026-09-06 |
| https://huggingface.co/datasets/Holi-Spatial/HoliSpatial-3D-Grounding | Holi-Spatial/HoliSpatial-3D-Grounding | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:holi-spatial`, thread `holi-spatial-development`, 1 dated events 2026-03-10 → 2026-03-10.
- **Practical note:** From 2026-03-10, practitioners should use the linked project page, repository, and Hugging Face resource as the starting point for evaluating Holi-Spatial, while independently verifying the exact artifact, version, and usage instructions.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.