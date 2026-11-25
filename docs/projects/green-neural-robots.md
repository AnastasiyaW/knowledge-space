---
title: "Green Neural Robots: animated-3d-avatars-head — Animated 3D Avatars Head"
category: "projects"
date: 2026-09-25
tags: ["animated-3d-avatars-head", "green-neural-robots", "project"]
aliases: ["Green Neural Robots: animated-3d-avatars-head"]
---

# Green Neural Robots: animated-3d-avatars-head — Animated 3D Avatars Head

AGORA animates 3D Gaussian head avatars in real time.

**Development line:** project:green-neural-robots · thread animated-3d-avatars-head  
**Last event:** 2026-09-25 · 2 dated since 2026-09-05 · **Researched:** 2026-11-25 · confidence: medium

## What it is

AGORA (Adversarial Generation Of Real-time Animatable 3D Gaussian Head Avatars) is a GAN-based method that generates animatable 3D Gaussian head avatars. The repository reports 250 FPS on GPU and about 9 FPS on CPU-only inference. The official implementation covers inference (generate an avatar from a random latent and drive it with a video), metrics, and a two-stage GAN training recipe.

## Development line

- **2026-09-05 — Fake driver in Chinese autonomous train for passenger reassurance.** A Chinese autonomous train operates with a fake driver who sits in the cabin without controls to calm passengers, highlighting that work will continue but will be boring for humans.
- **2026-09-25 — Release of animated 3D avatars code.** Summer release of code for animated 3D avatars heads on 3DGS from subscriber.
  - The repository (ramazan793/AGORA, tagged 'Real-time 3DGS avatars') is the official implementation of AGORA. Its README says the work was accepted to the ECCV 2026 Interactive Social Avatars Workshop and that the model renders at 250 FPS on GPU and about 9 FPS on CPU. The code covers inference, metrics (FID, FPS, ArcFace identity consistency, and AED / AED-jaw / APD / ASD re-estimated with SMIRK), and training (stage 1 at 256², stage 2 progressively grown to 512²). PTI / test-time inversion is excluded. The README says the agora_m distillation module on branch main_experimental was a preliminary experiment and is not part of the workshop paper. The page showed 20 stars and 13 commits when observed. (undated page; observed 2026-09-25) — <https://github.com/ramazan793/agora>

## What changed

The official implementation is now available in a public GitHub repository. It is described as accepted to the ECCV 2026 Interactive Social Avatars (ISA) Workshop. PTI / test-time inversion is not part of this release.

## How to use this

1. Clone the repository (git clone git@github.com:ramazan793/AGORA.git), then create a Python 3.10 environment with uv venv and install the pure-Python dependencies with uv sync --inexact.
  — <https://github.com/ramazan793/agora>
2. Build or install the CUDA-compiled extensions that uv does not resolve (gsplat, the diff_gaussian_rasterization forks, simple_knn, pytorch3d, nvdiffrast, among others) against your CUDA toolkit; the authors used CUDA 11.8. If you already have a compatible GGHead/EG3D environment, run scripts/setup_cuda_deps.sh with SRC pointing at its site-packages.
  — <https://github.com/ramazan793/agora>
3. Run scripts with uv run --no-sync. Use the repository's inference path to generate an avatar from a random latent and reenact it with a driving video.
  — <https://github.com/ramazan793/agora>

## Best practices

- Never run a bare uv sync after the CUDA extensions are installed. It prunes packages not declared in pyproject.toml and would delete the out-of-band compiled forks. Use uv sync --inexact or uv pip install when adding a dependency.
  — <https://github.com/ramazan793/agora>
- Keep NumPy at the pinned 1.24.3. The compiled extensions are built against NumPy 1.x and NumPy 2.x breaks them. The authors tested with Python 3.10.14 and PyTorch 2.4.1 (CUDA 11.8) on NVIDIA RTX 6000 Ada GPUs.
  — <https://github.com/ramazan793/agora>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact date of the code release is not stated on the linked page.
- No linked page supports the autonomous-train item, so it has no independent verification here.
- The full README (data and checkpoints, quickstart, troubleshooting) was truncated in the observed page.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/ramazan793/agora | GitHub - ramazan793/AGORA: Real-time 3DGS avatars | 2026-09-25 |

## Agent brief {#agent-brief}

- **Subject:** project:green-neural-robots, thread animated-3d-avatars-head, 2 dated events 2026-09-05 → 2026-09-25.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
