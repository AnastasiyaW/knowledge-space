---
title: JoyAI-Video-Edit
category: projects
date: 2026-08-06
tags: [joyai-video-edit, joyai-video-edit-public-reference, joyai_video_edit, project]
aliases: ["JoyAI-Video-Edit"]
---

# JoyAI-Video-Edit

**Development line:** `project:joyai-video-edit` · thread `joyai-video-edit-public-reference`  
**Last event:** 2026-08-06 · 1 dated since 2026-08-06 · **Researched:** 2026-09-05 · confidence: high

## What it is

JoyAI-Video-Edit: an Apache-2.0, 16B autoregressive-diffusion video editor for causal, live video-to-video edits.

- Text, local, background, style, motion and reference-image edits.
- Live-camera or uploaded-video input over WebSocket.
- Claimed benchmark: 720p at about 30 FPS on one Nvidia B200; the consumer-GPU configuration is 840×480 at 24 FPS on RTX 5090.

## Development line

- **2026-08-06 — JoyAI-Video-Edit public project references recorded.** On 2026-08-06, public links appeared for a GitHub repository, a Hugging Face page, and a JoyAI Labs site. The references show active work, but omit a specific release version, capability, or launch status.

## What changed

- 2026-08-06 — Deployment code, checkpoints, and a technical report released; initial DiT checkpoint was `joyai_video_edit_dit_0804.pth`.
- 2026-08-14 — DiT checkpoint `joyai_video_edit_dit_0811.pth` replaced the initial checkpoint for serving and improved reference-image-guided editing.
- 2026-08-15 — A live Hugging Face demo became available on RTX PRO 6000 hardware.
- 2026-08-24 — Official consumer-GPU support added an RTX 5090 configuration at 840×480 and 24 FPS.

## How to use this

As of 2026-08-06, check the public code, model-distribution, and official-web references to verify the exact release state and usage guidance before adopting JoyAI-Video-Edit.

1. Clone the repository, create a Python 3.10 Conda environment, then install `deploy/requirements.txt`.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit>
2. Build the in-tree `joyomni_ops` CUDA extension; for Blackwell hardware use CUDA nvcc 12.8 or later.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>
3. Download `joyai_video_edit_dit_0811.pth`, the VAE files and the required MiMo-VL encoder into the documented checkpoints tree.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>
4. Set the GPU-specific environment variables and run `bash deploy/run_server.sh`; open port 8080 or forward it over SSH.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>

## Best practices

- Use the current `0811` DiT checkpoint; `0804` is retained only for reproducibility and is not the server default.
  — <https://huggingface.co/jdopensource/JoyAI-Video-Edit>
- Give each GPU model a separate `JOYOMNI_CACHE_ROOT` when sharing a checkout, and use the documented per-GPU resolution/FPS settings.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>
- Use SageAttention only on RTX 5090; leave it disabled on RTX PRO 6000 and B200. Enable low-VRAM mode on cards with 48 GB or less.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>

## Superseded by this

- 2026-08-14 — `joyai_video_edit_dit_0804.pth` is superseded for serving by `joyai_video_edit_dit_0811.pth`; retain the former only for reproducibility.

## Still unknown

- The original JoyAI Labs demo URL could not be retrieved in this research environment, so its current availability is unverified.
- The claimed throughput is first-party benchmark evidence, not an independently reproduced performance result.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/jd-opensource/JoyAI-Video-Edit | JoyAI-Video-Edit official repository | 2026-09-05 |
| https://huggingface.co/jdopensource/JoyAI-Video-Edit | jdopensource/JoyAI-Video-Edit model card | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md | JoyAI-Video-Edit Deployment Guide | 2026-09-05 |
| https://arxiv.org/abs/2608.03974 | JoyAI-Video-Edit: Real-Time Open-Ended Video Editing with Autoregressive Diffusion | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:joyai-video-edit`, thread `joyai-video-edit-public-reference`, 1 dated events 2026-08-06 → 2026-08-06.
- **Practical note:** As of 2026-08-06, practitioners should treat JoyAI-Video-Edit as having public code, model-distribution, and official-web references, then verify the exact release state and usage guidance at those sources before adopting it.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.