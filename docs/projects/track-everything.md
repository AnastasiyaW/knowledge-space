---
title: "Track Everything: track-everything-3d-tracker — Track Everything 3D Tracker"
category: "projects"
date: 2026-09-28
tags: ["project", "track-everything", "track-everything-3d-tracker"]
aliases: ["Track Everything: track-everything-3d-tracker"]
---

# Track Everything: track-everything-3d-tracker — Track Everything 3D Tracker

**Development line:** project:track-everything · thread track-everything-3d-tracker  
**Last event:** 2026-09-28 · 1 dated since 2026-09-28 · **Researched:** 2026-11-25 · confidence: high

## What it is

TrackEverything is a dense 3D point tracker from Carnegie Mellon University and Meta.

- Persistent 3D scene tracks: fuses surface observations in world coordinates so occluded points persist without redundant representation.
- Recurrent window architecture: refines motion estimates and chains predictions across sliding windows.
- Per-window classification: separates static from dynamic points to decode trajectories only for points in motion.

## Development line

- **2026-09-28 — TrackEverything 3D Tracker Announcement.** CMU and Meta announced a dense 3D tracker for long videos. It tracks visible points across 1000+ frames as persistent 3D trajectories in world coordinates. Features per-frame static/dynamic classification, multi-view trajectories, and duplicate removal via 3D scene representations.
  - The project page credits Carnegie Mellon University and Meta. It tracks points as soon as they appear, whereas prior methods mostly track points from the first frame. At each window boundary the 3D representation is voxelized to remove redundant points, so model cost scales with distinct scene content rather than video length. The model has 61M parameters and is trained on publicly available datasets only. TAPVid-3D results show it is the only dense method that runs on full-length sequences; Any4D + Pi3 runs out of memory there. The closed-source 1B-parameter D4RT reaches higher APD-P on 48-frame clips but has not been evaluated beyond 48 frames. Listed failure cases are fast, large-displacement motion and repetitive or low-texture backgrounds, where the lifted 3D correspondences become ambiguous. (undated) — <https://trackeverything.github.io/>
  - The code repository now exists, so the awaited code release has happened. Given RGB frames plus depth and camera poses, the tracker builds and maintains a de-duplicated 3D scene representation, refines trajectories in 3D across temporal windows, and classifies points as static or dynamic. If depth and poses are missing, they are estimated on the fly with feedforward 3D reconstruction models such as VGGT-Ω. The repo lists a hosted demo, a model, and a paper link, and shows 507 stars and 33 forks. (undated (page shows an Oct 2026 update)) — <https://github.com/ayushjain1144/trackeverything>

## What changed

TrackEverything is the first dense 3D point tracker that tracks all points across all frames of videos with 1000+ frames. It reports a gain of over 20% APD on TAPVid-3D over open-source dense 3D trackers and runs in under 40 GB of GPU memory. The code has since been released on GitHub, with a hosted demo, inference scripts, evaluation and training code, and an experimental multiview inference mode added in October 2026.

## How to use this

1. Try the model without installing anything by using the hosted demo linked from the project page and repository.
  — <https://github.com/ayushjain1144/trackeverything>
2. For local use, clone the repository and create a Python 3.10 conda environment. Install PyTorch 2.8.0 and torchvision 0.23.0 for CUDA 12.9, then torch_scatter and the listed dependencies. Add the repository's parent directory to PYTHONPATH. Inference needs nothing further.
  — <https://github.com/ayushjain1144/trackeverything>
3. Run demo.py to track a video and visualize the results (Rerun 3D viewer, 2D overlay MP4 videos, optional Weights & Biases logging). Use demo_hf.py for a Python API and lightweight CLI that extracts and saves track tensors without visualization dependencies.
  — <https://github.com/ayushjain1144/trackeverything>

## Best practices

- Supply depth and camera poses when available. Otherwise feedforward 3D reconstruction models such as VGGT-Ω estimate them on the fly.
  — <https://github.com/ayushjain1144/trackeverything>
- Expect degraded tracking under fast, large-displacement motion and on repetitive or low-texture backgrounds, and check results on such footage.
  — <https://trackeverything.github.io/>
- Only if training, build the deformable-attention CUDA extension. Set TORCH_CUDA_ARCH_LIST to your GPU architectures and CUDA_HOME to a toolkit matching the Torch build.
  — <https://github.com/ayushjain1144/trackeverything>

## Superseded by this

- The code for TrackEverything has not yet been released and is still awaited.
  — <https://github.com/ayushjain1144/trackeverything>

## Still unknown

- Exact public release date of the code; the repository page shows only an 'Oct 2026' update for multiview inference.
- The license terms were not visible in the retrieved repository text.
- Results on in-the-wild footage beyond the reported benchmarks and the listed failure cases.

## Sources

| source | title | read |
|---|---|---|
| https://trackeverything.github.io/ | TrackEverything: Long Horizon Dense Tracking via De-Duplicating 3D Scene Representations (project page) | 2026-10-01 |
| https://github.com/ayushjain1144/trackeverything | GitHub - ayushjain1144/trackeverything | 2026-10-01 |

## Agent brief {#agent-brief}

- **Subject:** project:track-everything, thread track-everything-3d-tracker, 1 dated events 2026-09-28 → 2026-09-28.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
