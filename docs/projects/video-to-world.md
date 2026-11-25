---
title: video_to_world
category: projects
date: 2026-03-23
tags: [project, video-to-world]
aliases: ["video_to_world"]
---

# video_to_world

**Development line:** `project:video-to-world` · thread `video-to-world`  
**Last event:** 2026-03-23 · 1 dated since 2026-03-23 · **Researched:** 2026-09-05 · confidence: medium

## What it is

video_to_world is local ECCV 2026 research code for people reconstructing a generated video sequence as an explorable 2DGS or 3DGS scene, not a video generator or hosted service.

- Depth Anything 3 estimates per-frame geometry and cameras.
- Non-rigid frame-to-model ICP and global optimization consolidate inconsistent views.
- Inverse-deformation-aware Gaussian-splat optimization produces the scene.

## Development line

- **2026-03-23 — Video-to-World project resources were linked publicly.** The project page and repository were recorded; first-party sources do not identify this as an upstream release date.

## What changed

2026-03-17: arXiv v1 and the repository’s initial commit made the paper and first code public. 2026-03-18: arXiv v2 became current; repository commits added the arXiv/BibTeX reference, setup updates, and an automatic-evaluation path fix. 2026-03-23: The project page and repository were recorded; first-party sources do not identify this as an upstream release date. 2026-03-26: The maintainer added the repository LICENSE file. 2026-04-27: The maintainer made a commit titled “Release sample data”; the current README provides paper-scene data, but the exact asset diff was not independently verified.

## How to use this

As of 2026-03-23, practitioners can use the linked project page and GitHub repository as the starting point for evaluating the Video-to-World project and its available implementation materials.

1. Clone the main branch, create a Python 3.10 Conda environment, retain numpy<2 and opencv-python<4.12, then pin Depth Anything 3 to the documented commit and apply the supplied trajectory-export patch.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
2. Provide an already generated MP4 with --config.input-video, or a folder of frames with --config.frames-dir; run_reconstruction.py performs preprocessing, alignment, inverse-deformation training, and Gaussian-splat training.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
3. Use the default fast preset for the shorter 3DGS-only path, or extensive when the full global-optimization, 2DGS, and 3DGS path is needed; renderer selection can be overridden explicitly.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
4. Use eval_gs to render novel views from the trained checkpoint; export a 3DGS checkpoint to PLY or open the local interactive viewer when the scene is ready.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
5. Check the preprocessing model before a run: the current default is depth-anything/DA3NESTED-GIANT-LARGE, not a model shipped by video_to_world itself.
  — <https://github.com/lukasHoel/video_to_world/blob/main/run_reconstruction.py>

## Best practices

- Pin the documented Depth Anything 3 source revision and apply the repository patch; the pipeline depends on its trajectory export, so substituting an arbitrary DA3 checkout is not equivalent.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
- Treat Stage 0 frame count and stride as a GPU-memory budget: its defaults are 100 frames and stride 8, and the authors explicitly advise fewer frames on smaller GPUs. Stage 1 has a separate 50-frame alignment default.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
- Record the exact main commit and resolved environment for every run. The repository has no GitHub release artifacts, so “current main” is not a versioned distribution.
  — <https://github.com/lukasHoel/video_to_world/releases>
- Screen source sequences for revisited areas that add, remove, or change objects: the paper says such video-model hallucinations can be consolidated into the final static geometry rather than repaired by alignment.
  — <https://arxiv.org/html/2603.16736v2>
- Do not infer commercial clearance from the repository alone: the current default DA3NESTED-GIANT-LARGE model card declares CC BY-NC 4.0 and non-commercial use only.
  — <https://huggingface.co/depth-anything/DA3NESTED-GIANT-LARGE>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No first-party source found with a publication, release, or commit date of 2026-03-23; that date is retained as the observed reference date rather than treated as an upstream launch.
- There is no GitHub release bundle or complete dependency lock, and the documented DA3 code revision does not pin an immutable model-weight revision.
- No local GPU run was performed. The A6000 timing and memory figures are a fixed paper benchmark, not a capacity guarantee for another clip or hardware.
- The published scope is generated video sequences. Performance on real, highly dynamic, or severely inconsistent video was not established here.
- The default DA3 weights are non-commercial; whether a commercially licensed substitute is compatible and preserves quality is unverified.

## Sources

| source | title | read |
|---|---|---|
| https://lukashoel.github.io/video_to_world/ | World Reconstruction From Inconsistent Views — official project page | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world | lukasHoel/video_to_world — official repository | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/blob/main/README.md | video_to_world README — installation, pipeline, presets, and data release | 2026-09-05 |
| https://arxiv.org/abs/2603.16736 | World Reconstruction From Inconsistent Views — arXiv abstract and version history | 2026-09-05 |
| https://arxiv.org/html/2603.16736v2 | World Reconstruction From Inconsistent Views — arXiv HTML v2 | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/commits/main/ | video_to_world — commit history | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/releases | video_to_world — GitHub releases | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/blob/main/run_reconstruction.py | video_to_world run_reconstruction.py — current pipeline defaults | 2026-09-05 |
| https://huggingface.co/depth-anything/DA3NESTED-GIANT-LARGE | Depth Anything 3 DA3NESTED-GIANT-LARGE — model card and license | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:video-to-world`, thread `video-to-world`, 1 dated events 2026-03-23 → 2026-03-23.
- **Practical note:** As of 2026-03-23, practitioners can use the linked project page and GitHub repository as the starting point for evaluating the Video-to-World project and its available implementation materials.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
