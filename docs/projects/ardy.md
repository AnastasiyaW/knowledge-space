---
title: ARDY — Public availability
category: projects
date: 2026-07-15
tags: [ardy, project, public-availability]
aliases: ["ARDY"]
---

# ARDY — Public availability

**Development line:** `project:ardy` · thread `public-availability`  
**Last event:** 2026-07-15 · 1 dated since 2026-07-15 · **Researched:** 2026-09-05 · confidence: high

## What it is

ARDY is an autoregressive diffusion system for real-time humanoid motion: streaming text prompts, root paths and waypoints, full-body keyframes, and sparse joint constraints. It ships four 326M-parameter Core and Unitree G1 checkpoints; released models generate up to eight seconds of motion per output. Practical verdict: use it for Linux/NVIDIA-GPU prototypes and integration work, not as a drop-in DCC animation tool.

## Development line

- **2026-07-15 — ARDY public project resources were linked.** On 2026-07-15, ARDY was linked through its NVIDIA Research project page, source repository, Hugging Face collection, and interactive Hugging Face Space. This is a material public-availability milestone because it connects the project to its research, code, model, and hands-on entry points. The dated links alone do not establish the exact announcement wording, version, capabilities, or release status.

## What changed

2026-07-15 — ARDY’s project page, official code, checkpoint collection and interactive demo became available; the release covers Core and Unitree G1 rigs, rather than a single generic character model.

Event finding for 2026-07-15: the linked official repository specifies four checkpoints released 2026-07-10: 20-FPS Core models with 8- or 40-frame horizons and 25-FPS Unitree G1 models with 8- or 52-frame horizons. The NVIDIA model card dates the 40-frame Core checkpoint to 2026-07-10, gives it 326M parameters, and says it was trained on 630 hours of Bones Rigplay 1 motion capture.

New events: 2026-07-09 — the accompanying ARDY paper was posted to arXiv, describing the hybrid root-motion/body-latent representation and two-stage transformer denoiser. 2026-07-10 — NVIDIA released the four pretrained checkpoints under the NVIDIA Open Model Agreement.

## How to use this

As of 2026-07-15, practitioners should use the ARDY project page, source repository, Hugging Face collection, and interactive Space together as the starting points for evaluating or trying the project, while independently verifying the exact supported workflow and versions.

1. Create a Python 3.10+ environment on Linux, install a CUDA-matched PyTorch build, then install ARDY; the official setup was mainly tested on Ubuntu 22.04 with an RTX 4090, driver 575 and Python 3.11.
  — <https://github.com/nv-tlabs/ardy>
2. Obtain access to Meta-Llama-3-8B-Instruct and authenticate Hugging Face, because ARDY’s text encoder depends on that gated model.
  — <https://github.com/nv-tlabs/ardy>
3. Run `python scripts/run_demo.py`, open `http://localhost:2333`, load a checkpoint, then control motion with text, waypoints, velocity keys or kinematic constraints.
  — <https://github.com/nv-tlabs/ardy>
4. Choose a rig-specific checkpoint: Core for the 27-joint character rig, or G1 for Unitree G1; use the listed FPS and horizon instead of treating the variants as interchangeable.
  — <https://huggingface.co/nvidia/ARDY-Core-RP-20FPS-Horizon40>

## Best practices

- Install PyTorch before ARDY so the CUDA build matches the GPU and driver; use the TensorRT extra only where its driver and package-index requirements are met.
  — <https://github.com/nv-tlabs/ardy>
- Keep post-processing off initially: it can reduce foot skating and improve constraint following, but it is slower and disabled by default.
  — <https://github.com/nv-tlabs/ardy>
- Set history length according to the task: shorter history adapts faster to changed prompts or constraints; longer history improves semantic continuity and transitions.
  — <https://github.com/nv-tlabs/ardy>
- Validate a use-case-specific integration before deployment; the model card identifies Linux and NVIDIA Ampere, Hopper and Blackwell as supported environments.
  — <https://huggingface.co/nvidia/ARDY-Core-RP-20FPS-Horizon40>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The hosted Hugging Face Space could not be read during research, so its current availability and interface were not verified.
- No dated release note was found for the 2026-07-15 publication itself; the July 15 event is supported by the official project, repository and model pages, while checkpoint release dates are explicitly 2026-07-10.

## Sources

| source | title | read |
|---|---|---|
| https://research.nvidia.com/labs/sil/projects/ardy/ | ARDY: Interactive Human Motion Generation | 2026-09-05 |
| https://github.com/nv-tlabs/ardy | Official implementation of ARDY | 2026-09-05 |
| https://huggingface.co/collections/nvidia/ardy | ARDY — NVIDIA collection | 2026-09-05 |
| https://huggingface.co/nvidia/ARDY-Core-RP-20FPS-Horizon40 | ARDY-Core-RP-20FPS-Horizon40 model card | 2026-09-05 |
| https://arxiv.org/abs/2607.08741 | ARDY: Autoregressive Diffusion with Hybrid Representation for Interactive Human Motion Generation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ardy`, thread `public-availability`, 1 dated events 2026-07-15 → 2026-07-15.
- **Practical note:** As of 2026-07-15, practitioners should use the ARDY project page, source repository, Hugging Face collection, and interactive Space together as the starting points for evaluating or trying the project, while independently verifying the exact supported workflow and versions.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
