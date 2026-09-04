---
title: CameraCtrl
category: projects
date: 2024-05-29
tags: [cameractrl, cameractrl-development, project]
aliases: ["CameraCtrl"]
---

# CameraCtrl

**Development line:** `project:cameractrl` · thread `cameractrl-development`  
**Last event:** 2024-05-29 · 2 dated since 2024-04-10 · **Researched:** 2026-09-04 · confidence: medium

## What it is

CameraCtrl is a research codebase for video generation with prescribed camera motion in AnimateDiffV3 and Stable Video Diffusion.

- Camera pose conditioning: drives video generation along an exact camera trajectory.
- Modular design: keeps the base diffusion model separate from camera-control weights.
- Backend implementations: provides AnimateDiffV3 on `main` and SVD image-to-video on `svd`.

## Development line

- **2024-04-10 — CameraCtrl project page and source repository were linked.** On 2024-04-10, public links pointed to the CameraCtrl project page and GitHub repository. The links mark public availability, but do not state a release version or post contents.
- **2024-05-29 — A CameraCtrl-svd Hugging Face Space was linked.** On 2024-05-29, public tracking linked the CameraCtrl-svd Hugging Face Space and referenced the earlier CameraCtrl post. This showed a demo step, but the links alone do not confirm functionality, model version, or live status on that date.

## What changed

2024-04-10 — CameraCtrl appeared on its project page and public repository. Release notes date the AnimateDiffV3 code and checkpoint release to 2024-04-03.
2024-05-29 — The Stable Video Diffusion path appeared through the SVD-xt demo. Maintainer notes date the code, pretrained models, and Gradio demo to 2024-05-24. This added a separate SVD image-to-video implementation.
2025-03-13 [found today] — CameraCtrl II was submitted to extend research toward iterative exploration of dynamic scenes.
2026-09-04 [found today] — The original repository still assigns AnimateDiffV3 to `main` and SVD to `svd`. The public CameraCtrl-svd Space displays a dependency import failure.

## How to use this

We had public project and source links on 2024-04-10. The CameraCtrl-svd Hugging Face Space followed on 2024-05-29 for testing. The link-only evidence supports no operational claims beyond those locations.

1. Choose the backend first: use `main` for AnimateDiffV3, and check out `svd` only for Stable Video Diffusion image-to-video.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
2. For the AnimateDiffV3 path, create the documented Python 3.10/CUDA 11.7 environment and activate `cameractrl`.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
3. Download SD1.5, the AnimateDiffV3 adaptor, motion-module checkpoints, and the CameraCtrl checkpoint. Merge the ADV3 adaptor into the SD1.5 UNet before inference.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
4. Prepare a trajectory text file and prompt JSON from the provided assets, then visualize the trajectory before sampling.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
5. Run the documented `inference.py` recipe, supplying the base-model, motion-module, CameraCtrl-checkpoint, prompt, trajectory, and output paths. The reference launch uses eight processes.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
6. For SVD, use the `svd` environment, a compatible SVD or SVD-xt checkpoint, condition images, prompt JSON, and trajectory. Documented frame counts are 14 for SVD and 25 for SVD-xt.
  — <https://github.com/hehao13/CameraCtrl/blob/svd/README.md>

## Best practices

- Keep `main` and `svd` separate: they target different backends, environments, and input modes, so do not mix their setup instructions or checkpoints.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
- Treat the camera trajectory as a first-class input: begin with the supplied pose files, visualize the path, and hold prompts and seeds fixed when comparing trajectories.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
- Use the matching asset set: main needs SD1.5 plus merged ADV3 and CameraCtrl weights, while `svd` needs SVD/SVD-xt plus its matching CameraCtrl checkpoint.
  — <https://github.com/hehao13/CameraCtrl/blob/svd/README.md>
- Reproduce with the project-pinned environment before upgrading libraries. The main environment pins Python 3.10, PyTorch 1.13.1, CUDA 11.7, diffusers 0.24.0, and xformers 0.0.16.
  — <https://github.com/hehao13/CameraCtrl/blob/main/environment.yaml>
- Run SVD locally rather than depending on the public Space until it is repaired: the Space error is an import failure for `cached_download`.
  — <https://huggingface.co/spaces/hehao13/CameraCtrl-svd>

## Superseded by this

- 2024-04-10 main-only setup guidance — superseded for SVD users by the 2024-05-24 `svd` release. This is a separate image-to-video implementation, not an upgrade to `main`.
- 2024-05-29 hosted-demo workflow — superseded as of 2026-09-04 by the observed CameraCtrl-svd runtime failure. Run the local `svd` path to reproduce results.

## Still unknown

- The CameraCtrl-svd error page came from a crawl labelled two weeks old. A fresh interactive check was not available, so verify runtime status before relying on it.
- CameraCtrl II is a later research project without an official migration guide, compatible release, or drop-in claim. We do not treat it as a replacement for the 2024 repository.
- The author page lists CameraCtrl II++, but tests did not verify a usable release or compatibility with the original CameraCtrl workflow.
- No official single-GPU reference recipe exists. Both documented inference examples use eight processes.

## Sources

| source | title | read |
|---|---|---|
| https://hehao13.github.io/projects-CameraCtrl/ | CameraCtrl: Enabling Camera Control for Video Diffusion Models | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl | hehao13/CameraCtrl | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl/blob/main/README.md | CameraCtrl README — main branch | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl/blob/main/environment.yaml | CameraCtrl environment.yaml — main branch | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl/blob/svd/README.md | CameraCtrl README — svd branch | 2026-09-04 |
| https://huggingface.co/spaces/hehao13/CameraCtrl-svd | CameraCtrl Svd Xt — Hugging Face Space | 2026-09-04 |
| https://arxiv.org/abs/2404.02101 | CameraCtrl: Enabling Camera Control for Text-to-Video Generation | 2026-09-04 |
| https://arxiv.org/abs/2503.10592 | CameraCtrl II: Dynamic Scene Exploration via Camera-controlled Video Diffusion Models | 2026-09-04 |
| https://hehao13.github.io/ | Hao He — projects | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:cameractrl`, thread `cameractrl-development`, 2 dated events 2024-04-10 → 2024-05-29.
- **Practical note:** Public project and source links were live as of 2024-04-10. The CameraCtrl-svd Hugging Face Space was available as of 2024-05-29 for evaluation. The link-only evidence justifies no operational claims beyond those locations.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
