---
title: RealFusion
category: projects
date: 2023-03-03
tags: [code_release, project, realfusion, realfusion-development]
aliases: ["RealFusion"]
---

# RealFusion

**Development line:** `project:realfusion` · thread `realfusion-development`  
**Last event:** 2023-03-03 · 1 dated since 2023-03-03 · **Researched:** 2026-09-04 · confidence: high

## What it is

RealFusion reconstructs a plausible 360-degree object from one masked image by combining single-image textual inversion, Stable Diffusion score distillation, and an Instant-NGP-style NeRF.

- token inversion: learns an image-specific token
- radiance field: optimizes against the input image and diffusion prior
- mesh export: exports a textured mesh optionally

Unseen geometry is inferred, not recovered; failed convergence and Janus-style duplicated faces remain documented failure modes.

Use it as a reproducibility baseline or a tunable research workflow, not as a current turnkey image-to-3D product.

## Development line

- **2023-03-03 — RealFusion code and project resources linked.** On 2023-03-03, the RealFusion development line recorded a code-release entry with links to the project's public page and GitHub repository. This establishes a dated public reference point, but no version, commit, or specific technical change is identified.

## What changed

2023-03-03 — RealFusion’s public project page and code release made the single-image textual-inversion-plus-NeRF workflow runnable outside the paper implementation. 2023-04-08 — The later reference pointed back to the 2023-03-03 release; no separate RealFusion code, model, or method update is evidenced by that link.

## How to use this

From 2023-03-03, practitioners could use the dated RealFusion project page and repository links as the starting point for locating its publicly referenced code-release resources.

1. Install the Python requirements, PyTorch separately, and the CUDA extensions; install nvdiffrast only when exporting a textured mesh.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
2. Prepare a square RGBA image containing the object and mask; use the supplied mask-extraction script when starting from an unmasked image.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
3. Run single-image textual inversion with Stable Diffusion v1.5 to create the learned object embedding.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
4. Run reconstruction with python main.py --O, the RGBA image, learned embedding, and matching Stable Diffusion checkpoint.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
5. Inspect novel views and tune camera pose, camera radii, losses, and random seeds for the specific image before accepting an output.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>

## Best practices

- Start with a clean masked object image; the documented input contract is a square RGBA image.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Use --O: the repository states that its CUDA raymarching path was developed and tested with that optimization bundle.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Match pose_angle to the camera viewpoint and set radius_rot slightly above the training radius maximum.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Run multiple seeds and select outputs after inspection; default parameters are explicitly not equally good for every example.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Treat backsides as plausible extrapolations, and reject transparent fields, floaters, incorrect geometry, or duplicated-face outputs rather than presenting them as recovered geometry.
  — <https://arxiv.org/abs/2302.10663>

## Superseded by this

- 2023-03-03 — The public repository’s refactored release superseded reliance on the paper’s original implementation details; its maintainer states that parts differ from the paper code.
- 2023-04-08 — Treating the later reference as a separate release is obsolete: it links to the earlier 2023-03-03 item rather than documenting a new release.

## Still unknown

- No dated first-party release, checkpoint, compatibility test, or successor-method announcement was found for the 2023-04-08 reference; it appears to be a retrospective pointer to the earlier item, not a distinct development step.
- The current repository documents a CUDA-dependent research workflow but does not provide evidence of compatibility with current PyTorch, CUDA, Diffusers, or Stable Diffusion ecosystem versions.

## Sources

| source | title | read |
|---|---|---|
| https://lukemelas.github.io/realfusion/ | RealFusion project page | 2026-09-05 |
| https://github.com/lukemelas/realfusion | lukemelas/realfusion | 2026-09-05 |
| https://github.com/lukemelas/realfusion/blob/main/README.md | RealFusion README | 2026-09-05 |
| https://arxiv.org/abs/2302.10663 | RealFusion: 360° Reconstruction of Any Object from a Single Image | 2026-09-05 |
| https://cvpr.thecvf.com/virtual/2023/poster/21294 | CVPR 2023 poster: RealFusion: 360° Reconstruction of Any Object From a Single Image | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:realfusion`, thread `realfusion-development`, 1 dated events 2023-03-03 → 2023-03-03.
- **Practical note:** From 2023-03-03, practitioners could use the dated RealFusion project page and repository links as the starting point for locating its publicly referenced code-release resources.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.