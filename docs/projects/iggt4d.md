---
title: IGGT4D
category: projects
date: 2026-07-22
tags: [iggt4d, project]
aliases: ["IGGT4D"]
---

# IGGT4D

**Development line:** `project:iggt4d` · thread `iggt4d`  
**Last event:** 2026-07-22 · 1 dated since 2026-07-22 · **Researched:** 2026-09-05 · confidence: medium

## What it is

IGGT4D processes video frames sequentially to predict camera, geometry, persistent object identities, and instance masks together.

- Streaming 4D reconstruction
- Pose estimation
- Object tracking
- Open-vocabulary segmentation

The 1B parameter checkpoint requires accepting access terms on Hugging Face; dataset, benchmark, training, and evaluation code are not released yet.
It works for inference experiments on custom image sequences, but not for reproducible training or benchmarking.

## Development line

- **2026-07-22 — IGGT4D GitHub Pages site was linked.** Causal streaming model that unifies scene geometry and persistent object identities.

## What changed

2026-07-22 — IGGT4D was presented as Streaming 4D Instance-Grounded Geometry Transformer: a causal streaming model that unifies scene geometry and persistent object identities.

## How to use this

From 2026-07-22, practitioners should treat the linked IGGT4D GitHub Pages site as a project reference point, while verifying its specific guidance or release status before relying on it.

1. Clone the official repository and create a Conda environment with Python 3.10.
  — <https://github.com/HorizonRobotics/IGGT4D>
2. Install PyTorch; the README gives the example of PyTorch 2.8.0 with CUDA 12.8, then install the package with `pip install -e .`.
  — <https://github.com/HorizonRobotics/IGGT4D>
3. Accept the checkpoint access terms on Hugging Face, download it, and save it as `checkpoints/model.safetensors`.
  — <https://huggingface.co/HorizonRobotics/IGGT4D>
4. Run `python streaming_infer.py` for the demo, or pass `--image-dir` and `--output-dir` for a custom sequence of RGB frames.
  — <https://github.com/HorizonRobotics/IGGT4D>
5. If needed, enable `--camera` for external camera parameters and save results via `--save-npy` or `--save-ply`.
  — <https://github.com/HorizonRobotics/IGGT4D>

## Best practices

- Keep streaming mode as the default for long sequences; `--mode full` is the offline full-attention variant.
  — <https://github.com/HorizonRobotics/IGGT4D>
- Do not plan training, evaluation, or comparison on the official benchmark before release: the repository lists them as pending artifacts.
  — <https://github.com/HorizonRobotics/IGGT4D>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- For the 2026-07-22 event, the primary arXiv source specifies the paper submission date as 2026-07-21 16:00:01 UTC; this confirms the title, ten authors, and the InsScene4D-147K scale, but gives no separate dated publication for 2026-07-22.
- The exact date when inference code and the checkpoint became available is not stated on the primary pages read; therefore we did not add it as a separate dated event.
- The public project page states that the dataset and benchmark will arrive later, and the repository also awaits training and evaluation code.

## Sources

| source | title | read |
|---|---|---|
| https://iggt4d.github.io/ | IGGT4D: Streaming 4D Instance-Grounded Geometry Transformer | 2026-09-05 |
| https://arxiv.org/abs/2607.19228 | IGGT4D: Streaming 4D Instance-Grounded Geometry Transformer | 2026-09-05 |
| https://github.com/HorizonRobotics/IGGT4D | HorizonRobotics/IGGT4D | 2026-09-05 |
| https://huggingface.co/HorizonRobotics/IGGT4D | HorizonRobotics/IGGT4D model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:iggt4d`, thread `iggt4d`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** From 2026-07-22, practitioners should treat the linked IGGT4D GitHub Pages site as a project reference point, while verifying its specific guidance or release status before relying on it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
