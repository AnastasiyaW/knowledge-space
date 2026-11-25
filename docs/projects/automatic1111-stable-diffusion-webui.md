---
title: stable-diffusion-webui — Release history
category: projects
date: 2024-03-02
tags: [automatic1111-stable-diffusion-webui, automatic1111_stable_diffusion_webui, automatic1111_webui_releases, project, release-history]
aliases: ["AUTOMATIC1111 Stable Diffusion WebUI", "AUTOMATIC1111 stable-diffusion-webui", "stable-diffusion-webui"]
---

# stable-diffusion-webui — Release history

**Development line:** `project:automatic1111-stable-diffusion-webui` · thread `release-history`  
**Last event:** 2024-03-02 · 2 dated since 2023-05-02 · **Researched:** 2026-11-21 · confidence: high

## What it is

AUTOMATIC1111 stable-diffusion-webui is an AGPL-3.0 Gradio web interface for running Stable Diffusion image generation on your own machine.

- Modes: text-to-image, image-to-image, inpainting, upscaling, and extension-based workflows.
- Users: individual artists and hobbyists who run checkpoints on a local GPU; many community extensions build on it.
- Key capability: runs local checkpoints, including SDXL (1.8.0 added SDXL-Inpaint) and Stable Diffusion 3 (1.10.0).
- Limits: NVIDIA GPU is the recommended target; the README recommends Python 3.10.6 and says newer Python versions do not support torch.

## Development line

- **2023-05-01 — stable-diffusion-webui v1.1.0 was released.** GitHub records the release at 2023-05-01 11:36 UTC. The earlier stub date of 2023-05-02 is a day off in UTC.
- **2024-03-02 — stable-diffusion-webui v1.8.0 was released.** GitHub records the release at 2024-03-02 04:08 UTC.

## What changed

- 2023-05-01 — v1.1.0: switched to torch 2.0.0 (except AMD GPUs), enabled TCMalloc on Linux by default, added X/Y/Z plot dropdowns and img2img resize tabs.
- 2023-12-16 — v1.7.0: reworked the settings tab, added IPEX support for Intel Arc GPUs, HyperTile, and SSD-1B support.
- 2024-03-02 — v1.8.0: Soft Inpainting, FP8 support, SDXL-Inpaint, Spandrel-based upscalers, Extra Networks tree view, official LCM sampler, NPU support; torch updated to 2.1.2.
- 2024-04-13 — v1.9.0: refiner switchover moved to model timesteps, scheduler selection added to the main UI, DoRA support.
- 2024-07-27 — v1.10.0: Stable Diffusion 3 support, several new schedulers, performance work (release candidate 1.10.0-RC on 2024-07-06).
- 2025-02-09 — v1.10.1: fixes image upscaling on CPU. As of 2026-11, GitHub still marks this as the latest release.

## How to use this

1. Install Python 3.10.6 (Windows) and git; the README says newer Python versions do not support torch.
  — <https://github.com/AUTOMATIC1111/stable-diffusion-webui>
2. Pin a tagged release, for example 1.10.1, rather than the moving main branch, and record the tag in your deployment notes.
  — <https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases>
3. Launch with `webui-user.bat` from Explorer as a non-administrator user on Windows, or `webui.sh` on Linux; set launch options in `webui-user.bat` or `webui-user.sh`.
  — <https://github.com/AUTOMATIC1111/stable-diffusion-webui>
4. Before upgrading an existing install, read the release notes for every tag between your version and the target; the 1.9.0 refiner change and the 1.8.0 torch update changed behavior, not only features.
  — <https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.8.0>

## Best practices

- Pin a release tag for shared or production installs. Release candidates (for example 1.10.0-RC) are marked as pre-releases on GitHub.
  — <https://api.github.com/repos/AUTOMATIC1111/stable-diffusion-webui/releases?per_page=100>
- Use Python 3.10.6 on Windows; the README states that newer Python versions do not support torch.
  — <https://github.com/AUTOMATIC1111/stable-diffusion-webui>

## Superseded by this

- 2023-05-01 — the v1.1.0 torch 2.0.0 default was superseded by the torch 2.1.2 update in v1.8.0 (2024-03-02).
- 2024-03-02 — the v1.8.0 release replaced earlier upscaler handling with Spandrel-based upscalers.
- 2024-04-13 — the v1.9.0 refiner switchover at model timesteps replaced the earlier refiner behavior.

## Still unknown

- Maintenance status: the repository page does not state whether the project is actively maintained. The last tagged release is from 2025-02-09 as of 2026-11; we did not verify main-branch activity.
- Model folder path: the README capture did not state the checkpoint folder location.
- Minimum VRAM for SD3 and the 1.10.x schedulers: not stated in the sources read.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/AUTOMATIC1111/stable-diffusion-webui | README and repository overview | 2026-11-21 |
| https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases | Releases list | 2026-11-21 |
| https://api.github.com/repos/AUTOMATIC1111/stable-diffusion-webui/releases?per_page=100 | GitHub REST API: release dates (published_at) | 2026-11-21 |
| https://api.github.com/repos/AUTOMATIC1111/stable-diffusion-webui/releases/tags/v1.1.0 | GitHub REST API: v1.1.0 published_at | 2026-11-21 |
| https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.1.0 | v1.1.0 release notes | 2026-11-21 |
| https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.8.0 | v1.8.0 release notes | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:automatic1111-stable-diffusion-webui`, thread `release-history`, 2 dated events 2023-05-01 → 2024-03-02; releases through v1.10.1 (2025-02-09) verified.
- **Practical note:** Pin a release tag, check Python 3.10.6 on Windows, and read release notes for every intermediate tag before upgrading.
- **Confidence:** high for release dates and release contents; unknown for current maintenance activity. Dated supersedes above are the authority for what is obsolete.
