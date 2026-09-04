---
title: CameraCtrl — CameraCtrl development
category: projects
tags: [cameractrl, cameractrl-development, project]
aliases: ["CameraCtrl"]
---

# CameraCtrl — CameraCtrl development

**Development line:** `project:cameractrl` · thread `cameractrl-development`  
**Events:** 2 dated, 2024-04-10 → 2024-05-29 · **Researched:** 2026-09-04 · confidence: medium

## What it is

CameraCtrl — an official research codebase for creators and researchers who need to prescribe camera motion while generating video with AnimateDiffV3 or Stable Video Diffusion. - conditions generation on camera pose and trajectory; - keeps the base video-diffusion model outside its plug-in camera-control module; - provides separate AnimateDiffV3 (`main`) and SVD image-to-video (`svd`) implementations. Limit: the reference commands launch eight processes, and the public SVD Space currently reports a dependency failure. Verdict: suitable for a pinned local research workflow, not a ready hosted tool.

## Development line

- **2024-04-10 — CameraCtrl project page and source repository were linked.** On 2024-04-10, the CameraCtrl line was represented by links to its project page and GitHub repository. This is a material public availability step for the project, while the supplied links alone do not establish a release version or the contents of the linked post.
- **2024-05-29 — A CameraCtrl-svd Hugging Face Space was linked.** On 2024-05-29, the CameraCtrl development line included a link to a Hugging Face Space named CameraCtrl-svd, alongside a reference to the earlier CameraCtrl post. This is a material distribution or demonstration step, but the dated links alone do not establish the Space's exact functionality, model version, or availability status on that date.

## What changed

2024-04-10 — CameraCtrl was available through its project page and public repository; its release notes date the AnimateDiffV3 code and checkpoint release to 2024-04-03. 2024-05-29 — the Stable Video Diffusion path appeared through the SVD-xt demo; maintainer notes date its code, pretrained models, and Gradio demo to 2024-05-24. This added a separate SVD image-to-video implementation. 2025-03-13 [found today] — CameraCtrl II was submitted, extending the research line toward iterative, coherent exploration of wider dynamic scenes. 2026-09-04 [found today] — the original repository still assigns AnimateDiffV3 to `main` and SVD to `svd`; the public CameraCtrl-svd Space displays a dependency import failure.

## How to use this

As of 2024-04-10, practitioners could locate CameraCtrl's public project and source links; as of 2024-05-29, they could additionally look for the linked CameraCtrl-svd Hugging Face Space as a possible evaluation route. The supplied link-only evidence does not justify operational claims beyond those locations.

1. Choose the backend first: use `main` for AnimateDiffV3, and check out `svd` only for Stable Video Diffusion image-to-video.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
2. For the AnimateDiffV3 path, create the documented Python 3.10/CUDA 11.7 environment and activate `cameractrl`.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
3. Download SD1.5, the AnimateDiffV3 adaptor and motion-module checkpoints, and the CameraCtrl checkpoint; merge the ADV3 adaptor into the SD1.5 UNet before inference.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
4. Prepare a trajectory text file and prompt JSON from the provided assets, then visualize the trajectory before sampling.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
5. Run the documented `inference.py` recipe, supplying the base-model, motion-module, CameraCtrl-checkpoint, prompt, trajectory, and output paths. The reference launch uses eight processes.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
6. For SVD, use the branch-specific environment, compatible SVD or SVD-xt checkpoint, condition images, prompt JSON, and trajectory; the documented frame counts are 14 for SVD and 25 for SVD-xt.
  — <https://github.com/hehao13/CameraCtrl/blob/svd/README.md>

## Best practices

- Keep `main` and `svd` separate: they target different backends, environments, and input modes, so do not mix their setup instructions or checkpoints.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
- Treat the camera trajectory as a first-class input: begin with the supplied pose files, visualize the path, and hold prompts and seeds fixed when comparing trajectories.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
- Use the matching asset set: main needs SD1.5 plus merged ADV3 and CameraCtrl weights, while `svd` needs SVD/SVD-xt plus its matching CameraCtrl checkpoint.
  — <https://github.com/hehao13/CameraCtrl/blob/svd/README.md>
- Reproduce with the project-pinned environment before upgrading libraries; the main environment pins Python 3.10, PyTorch 1.13.1, CUDA 11.7, diffusers 0.24.0, and xformers 0.0.16.
  — <https://github.com/hehao13/CameraCtrl/blob/main/environment.yaml>
- Use a local SVD run rather than depending on the public Space until it is repaired: the observed Space error is an import failure for `cached_download`.
  — <https://huggingface.co/spaces/hehao13/CameraCtrl-svd>

## Superseded by this

- 2024-04-10 main-only setup guidance — superseded for SVD users by the 2024-05-24 `svd` release; it is a separate image-to-video implementation, not a `main`-branch upgrade.
- 2024-05-29 hosted-demo workflow — superseded as of 2026-09-04 by the observed CameraCtrl-svd runtime failure; use the local `svd` code path if you need to reproduce it.

## Still unknown

- The CameraCtrl-svd error page was accessible through a crawl labelled two weeks old; a fresh interactive inference check was not available, so recheck its runtime before relying on that status operationally.
- CameraCtrl II is a later research project, but no official migration guide, compatible implementation release, or drop-in replacement claim was found; it is not treated as a replacement for the 2024 repository.
- The author page lists CameraCtrl II++, but this research did not verify a usable release or its compatibility with the original CameraCtrl workflow.
- No official single-GPU reference recipe was found; both documented inference examples use eight processes.

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
- **Practical note:** As of 2024-04-10, practitioners could locate CameraCtrl's public project and source links; as of 2024-05-29, they could additionally look for the linked CameraCtrl-svd Hugging Face Space as a possible evaluation route. The supplied link-only evidence does not justify operational claims beyond those locations.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
