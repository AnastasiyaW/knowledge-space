---
title: "Déjà View (DVLT): deja-view-dvlt-open-release — Deja View Dvlt Open Release"
category: "projects"
date: 2026-11-13
tags: ["deja-view-dvlt", "deja-view-dvlt-open-release", "project"]
aliases: ["Déjà View (DVLT): deja-view-dvlt-open-release"]
---

# Déjà View \(DVLT\): open release

**Development line:** project:deja-view-dvlt · thread deja-view-dvlt-open-release  
**Last event:** 2026-11-13 · 1 dated since 2026-11-13 · **Researched:** 2026-11-14 · confidence: high

## What it is

Déjà View \(DVLT\) is a multi-view 3D reconstruction model from NVIDIA Research, ETH Zurich and the University of Toronto. It takes unposed RGB images and predicts metric 3D scene geometry and camera poses directly. It competes with feed-forward baselines such as pi^3 and Depth Anything 3.

- Depth: dense per-pixel depth and confidence maps.
- Ray maps: the basis for metric 3D point clouds.
- Cameras: intrinsics and extrinsics for each view.

One weight-tied recurrent transformer block of approximately 117 million parameters, run for 8 to 16 refinement steps at inference.

The explicit recurrence works as an inductive bias for multi-view geometry. It matches much larger models with fewer parameters and a smaller memory footprint.

## Development line

- **2026-11-13 — NVIDIA Research releases open Déjà View \(DVLT\) 3D reconstruction model.** On 2026-11-13, NVIDIA Research, ETH Zurich and the University of Toronto released Déjà View \(DVLT\) as open source. It is one weight-tied recurrent transformer block of about 117M parameters. The step count K is tunable at inference. Code and weights \(nvidia/dvlt\) are on Hugging Face.
  - The NVIDIA project page lists the outputs: per-pixel depth, confidence masks, ray maps for dense point clouds, and per-view camera intrinsics and extrinsics, all from unposed RGB sets. It outperforms larger baselines with 1.9x to 2.3x less compute. (2026-11-13) — <https://research.nvidia.com/labs/dvl/projects/dvlt/>
  - The official repository nv-tlabs/dvlt has PyTorch inference pipelines and multi-view evaluation scripts for indoor and driving datasets. The recurrent step count K can be changed at inference through the config. (2026-11-13) — <https://github.com/nv-tlabs/dvlt>
  - The Hugging Face repository nvidia/dvlt hosts the 117M parameter weights under the NVIDIA Research License, for research and development. (2026-11-13) — <https://huggingface.co/nvidia/dvlt>
  - The paper reports that under matched compute, weight-tied recurrence is a stronger inductive bias for multi-view geometry than independent layers. On ScanNet\+\+ it is competitive with larger models, including pi^3 and Depth Anything 3. (2026-11-13) — <https://arxiv.org/abs/2605.30215>

## What changed

The approach moves away from many unique, heavily scaled feed-forward transformer layers. Instead, one transformer block is looped over DINOv2 visual features. The number of refinement iterations is a knob at inference, so no retraining is needed to change it. The release then added full open weights and evaluation code across standard indoor, outdoor and driving benchmarks.

## How to use this

1. Clone the official repository and install the PyTorch and DINOv2 dependencies.
  — <https://github.com/nv-tlabs/dvlt>
2. Download the pre-trained 117M checkpoint from the Hugging Face repository nvidia/dvlt.
  — <https://huggingface.co/nvidia/dvlt>
3. Run the multi-view inference script on unposed RGB images or video frames. Pick the step count K to fit your compute budget.
  — <https://github.com/nv-tlabs/dvlt>
4. Take the per-pixel depth maps, confidence masks, camera intrinsics/extrinsics and ray-derived 3D point clouds into 3D Gaussian splatting or mesh reconstruction.
  — <https://research.nvidia.com/labs/dvl/projects/dvlt/>

## Best practices

- Set K between 8 and 16 at inference to trade precision against latency, with the same checkpoint.
  — <https://research.nvidia.com/labs/dvl/projects/dvlt/>
- Drop low-confidence depth with the per-pixel confidence masks before multi-view fusion.
  — <https://arxiv.org/abs/2605.30215>
- Keep enough visual overlap between input views so the geometry stays consistent across recurrent passes.
  — <https://github.com/nv-tlabs/dvlt>

## Superseded by this

- The idea that multi-view 3D transformer reconstruction needs more than one billion parameters in deep independent feed-forward layers to reach state-of-the-art geometry.
  — <https://arxiv.org/abs/2605.30215>

## Still unknown

- Third-party community discussion, such as forum threads or CUDA acceleration ports, could not be tied to working links, so community views are left out.
- Commercial terms beyond research and evaluation under the NVIDIA Research License: ask NVIDIA.

## Sources

| source | title | read |
|---|---|---|
| https://research.nvidia.com/labs/dvl/projects/dvlt/ | Déjà View: Multi-View 3D Reconstruction via Looped Transformers | 2026-11-14 |
| https://github.com/nv-tlabs/dvlt | nv-tlabs/dvlt: Official implementation of Déjà View \(DVLT\) | 2026-11-14 |
| https://huggingface.co/nvidia/dvlt | nvidia/dvlt at Hugging Face | 2026-11-14 |
| https://arxiv.org/abs/2605.30215 | Déjà View: Multi-View 3D Reconstruction via Looped Transformers | 2026-11-14 |

## Agent brief {#agent-brief}

- **Subject:** project:deja-view-dvlt, thread deja-view-dvlt-open-release, 1 dated events 2026-11-13 → 2026-11-13.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
