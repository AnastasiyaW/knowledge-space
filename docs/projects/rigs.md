---
title: RiGS — Repository reference
category: projects
date: 2026-07-25
tags: [project, repository-reference, rigs]
aliases: ["RiGS"]
---

# RiGS — Repository reference

**Development line:** `project:rigs` · thread `repository-reference`  
**Last event:** 2026-07-25 · 1 dated since 2026-07-25 · **Researched:** 2026-09-05 · confidence: high

## What it is

RiGS is the codebase for Rigid-aware 4D Gaussian Splatting.

- Scene decomposition into static, rigid, and transient Gaussian primitives
- Data preparation with ViPE and TAPIR/BootsTAPIR
- Training, evaluation, rendering, and visual inspection in a viewer

It requires Python 3.10 and a CUDA 12.x stack. This is a research repository without packaged releases.

## Development line

- **2026-07-25 — RiGS project repository was referenced.** On 2026-07-25, the RiGS development line linked to the project GitHub repository. We record the repository reference as a public development-history event without asserting features, release status, or repository contents.

## What changed

2026-07-25 — The RiGS implementation repository became available. First-party materials specify that the method runs on a single monocular video and uses static, rigid, and transient components for different motion time scales.

2026-05-22 — Earlier date added: the authors posted the RiGS paper on arXiv (v1), describing object-wise dynamic masks and scene-flow supervision.

## How to use this

From 2026-07-25, use the linked RiGS GitHub repository as the dated source reference for this project line, and verify its current contents separately.

1. Clone the repository with the ViPE submodule, create a Python 3.10 conda environment, install requirements and the local ViPE package, then download the TAPIR/BootsTAPIR checkpoint.
  — <https://github.com/ladvu/RiGS>
2. Prepare video and frames, extract depth, poses, intrinsics, optical flow, flow consistency, and static masks through ViPE, then build TAPIR tracks.
  — <https://github.com/ladvu/RiGS>
3. Run src/main.py with data paths and the experiment name. For checkpoint results, use --eval_step, --render_video, or run_viewer.py.
  — <https://github.com/ladvu/RiGS>

## Best practices

- Clone with --recursive, or initialize the submodule separately; monocular preprocessing will not run without it.
  — <https://github.com/ladvu/RiGS>
- Check PyTorch, CUDA toolkit, and driver versions against pinned requirements before training, because the repository targets CUDA 12.x.
  — <https://github.com/ladvu/RiGS>
- Inspect preprocessing visualizations and generate TAPIR tracks before reconstruction, because the pipeline requires both ViPE outputs and 2D tracks.
  — <https://github.com/ladvu/RiGS>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- GitHub does not publish releases, so the repository provides no versioned release history and no packaged installation path.
- First-party pages do not provide a creation date or commit record that ties code publication directly to 2026-07-25; that date remains the dated event for the repository link.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/ladvu/RiGS | ladvu/RiGS — official implementation and usage instructions | 2026-09-05 |
| https://arxiv.org/abs/2605.23672 | RiGS: Rigid-aware 4D Gaussian Splatting from a Single Monocular Video | 2026-09-05 |
| https://ladvu.github.io/RiGS/ | RiGS project page | 2026-09-05 |
| https://github.com/ladvu/RiGS/releases | RiGS releases | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:rigs`, thread `repository-reference`, 1 dated events 2026-07-25 → 2026-07-25.
- **Practical note:** From 2026-07-25, practitioners should use the linked RiGS GitHub repository as the dated source reference for this project line, while verifying its current contents separately.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.