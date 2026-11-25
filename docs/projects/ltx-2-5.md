---
title: LTX-2.5 — LTX Video
category: projects
date: 2026-08-11
tags: [ltx-2-5, ltx-video, project]
aliases: ["LTX-2.5"]
---

# LTX-2.5 — LTX Video

**Development line:** `project:ltx-2-5` · thread `ltx-video`  
**Last event:** 2026-08-11 · 1 dated since 2026-08-11 · **Researched:** 2026-09-07 · confidence: medium

## What it is

LTX-2.5 is Lightricks' 22B audio-video model family for local ComfyUI and Python setups or hosted generation.

- Synchronized video and audio generation from text, image, video, and audio conditioning.
- Local tooling for video-to-video, LoRA/IC-LoRA, HDR, and fine-tuning paths.
- Hosted API access via `ltx-2-5-fast` and `ltx-2-5-pro` without retake, extend, or reframe.

The technical local guide requires an NVIDIA GPU with 32 GB+ VRAM, 32 GB RAM, 100 GB free storage, CUDA 12.7+, and Python 3.12+. The product page separately lists a 16 GB minimum. Use LTX-2.5 when synchronized sound, self-hosting, or local adaptation matter. Keep LTX-2.3 for a hosted workflow that needs retake, extend, or reframe.

## Development line

- **2026-08-11 — LTX-2.5 official model and application links were shared.** On 2026-08-11, a dated item in the LTX Video thread linked to the official LTX-2.5 model page and the LTX application. This marks a specific LTX-2.5 model and its official access path. The available evidence does not establish whether this was a launch, an update, or a change in availability.

## What changed

- 2026-08-10 — `ltx-2-5-fast` gained automatic duration for text-to-video and image-to-video before the named release.
- 2026-08-11 — LTX introduced hosted Fast and Pro variants for text-, image-, and audio-to-video; LTX-2 v1.2.0 added the local 2.5 runtime and training support.
- 2026-08-12 — ComfyUI added day-one LTX-2.5 templates and both local-weight and hosted Partner Node routes.
- 2026-08-16 — The older `ltx-2-fast` and `ltx-2-pro` API IDs were removed, making migration to 2.3 or 2.5 mandatory.
- 2026-08-18 — Audio-to-video gained Fast 4K and Pro 1080p resolution tiers.
- 2026-08-19 — Audio-to-video gained frame-rate, last-frame, and camera-motion controls.
- 2026-08-25 — LTX-2 v1.3.0 changed local DFR with tiled 4K, multi-GPU execution, keyframe-aware decoding, and new DFR flags.
- 2026-09-02 — `ltx-2-5-pro` expanded to 1440p/4K and 48 fps across text-, image-, and audio-to-video.

## How to use this

1. Choose the surface first. Use `ltx-2-5-fast` for speed and lower cost, or `ltx-2-5-pro` for higher fidelity in hosted text-to-video, image-to-video, or audio-to-video routes. Use a local path if you need self-hosting or adaptation.
  — <https://docs.ltx.io/models/ltx-2-5>
2. For a hosted image-to-video request, pass `duration: null` only when the end frame is not fixed. Automatic duration cannot be combined with `last_frame_uri`.
  — <https://docs.ltx.io/models/ltx-2-5>
3. For the visual local path, install `ComfyUI-LTXVideo`, select an LTX-2.5 template, download the listed matching files, add a prompt or references, and queue the job.
  — <https://docs.ltx.io/open-source-model/getting-started/quick-start>
4. For code or automation, clone LTX-2, run `uv sync`, obtain access to the model repository, download the split components, and provide each component path to `ltx-pipelines`.
  — <https://docs.ltx.io/open-source-model/integration-tools/pytorch-api>
5. For local generation, keep width and height divisible by 32. Use an `8n + 1` frame count, or omit the frame count to let the LTX-2.5 duration head choose it.
  — <https://docs.ltx.io/open-source-model/integration-tools/pytorch-api>

## Best practices

- Keep the checkpoint components matched, especially the LTX-specific fine-tuned Gemma 4 text encoder. Do not substitute Google's vanilla Gemma 4.
  — <https://github.com/Lightricks/LTX-2/blob/main/packages/ltx-trainer/docs/configuration-reference.md>
- Start the ComfyUI text-to-video template at 768x512, 97 frames, and 24 fps. Increase length or resolution only after hardware handles the baseline, and fix the seed when you need reproduction.
  — <https://docs.ltx.io/open-source-model/usage-guides/text-to-video>
- Write prompts as a chronological scene. Name the shot, scene, action, character, camera movement, and audio. Rewrite prompts from other video models rather than pasting their tags or shot-list syntax unchanged.
  — <https://docs.ltx.io/open-source-model/usage-guides/prompting-guide>
- For native multi-shot work, use a chronological paragraph. Explicitly name every cut, restate recurring identifiers and audio continuity, and prefer two to four shots per generation.
  — <https://docs.ltx.io/open-source-model/usage-guides/prompting-guide>
- Use the native two-stage pipeline for local production. Use the distilled pipeline for speed or batch runs.
  — <https://docs.ltx.io/open-source-model/integration-tools/pytorch-api>
- Provision local work against the technical baseline: 32 GB+ NVIDIA VRAM, 32 GB RAM, 100 GB storage, CUDA 12.7+, and Python 3.12+. Validate the actual workflow on target hardware.
  — <https://docs.ltx.io/open-source-model/getting-started/system-requirements>

## Superseded by this

- 2026-08-16 — The API model IDs `ltx-2-fast` and `ltx-2-pro` remain valid. Source: https://docs.ltx.io/api-changelog/2026/8/16
- 2026-08-18 — Audio-to-video on `ltx-2-5-fast` is limited to 1080p. Source: https://docs.ltx.io/api-changelog/2026/8/18
- 2026-08-19 — Audio-to-video cannot set frame rate, camera motion, or a last frame. Source: https://docs.ltx.io/api-changelog/2026/8/19
- 2026-09-02 — LTX-2.5 Pro is limited to 720p/1080p. Source: https://docs.ltx.io/api-changelog/2026/9/2
- 2026-08-25 — DFR uses `--checkpoint-path`, `--distilled-lora`, and `--temporal-upsample-rounds`. Source: https://github.com/Lightricks/LTX-2/blob/main/CHANGELOG.md

## Still unknown

- A second unresolved LTX-2.5 entry dated 2026-08-12 uses provisional key `ltx_2_5` and different Hugging Face URLs. It may cover a downstream artifact rather than this base release. Do not merge its history without a reviewed exact identity.
- Hosted API names `fast`/`pro` and local checkpoint names `dev`/`distilled` are separate documented surfaces. No first-party source found here declares a one-to-one mapping between them.
- First-party sources conflict on local VRAM: the product page says 16 GB minimum, while the technical system-requirements page says 32 GB+. No reconciliation was found; the latter is used for the practical baseline.
- The supplied hosted-app URL did not yield readable documentation in this research. Current UI controls, account flow, and pricing were not independently verified.
- The Simplified-Chinese search lane produced community pages but no verified, dated, reproducible LTX-2.5 practice source. No Chinese-language parameter claim is included.

## Sources

| source | title | read |
|---|---|---|
| https://ltx.io/model/ltx-2-5 | LTX-2.5: LTX's Latest AI Open-Source Foundation Model | LTX | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/10 | August 10, 2026 | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/11 | August 11, 2026 | LTX Documentation | 2026-09-07 |
| https://github.com/Lightricks/LTX-2/releases/tag/v1.2.0 | Release v1.2.0 · Lightricks/LTX-2 · GitHub | 2026-09-07 |
| https://blog.comfy.org/p/ltx-25-day-0-support-in-comfyui | LTX-2.5 Day-0 Support in ComfyUI | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/16 | August 16, 2026 | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/18 | August 18, 2026 | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/19 | August 19, 2026 | LTX Documentation | 2026-09-07 |
| https://github.com/Lightricks/LTX-2/blob/main/CHANGELOG.md | LTX-2/CHANGELOG.md at main · Lightricks/LTX-2 · GitHub | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/9/2 | September 2, 2026 | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/models/ltx-2-5 | LTX-2.5 | LTX Documentation | 2026-09-07 |
| https://huggingface.co/Lightricks/LTX-2.5 | Lightricks/LTX-2.5 · Hugging Face | 2026-09-07 |
| https://docs.ltx.io/open-source-model/getting-started/quick-start | Quick Start | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/usage-guides/text-to-video | Text-to-Video Workflow for Beginners | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/integration-tools/pytorch-api | PyTorch API | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/getting-started/system-requirements | System Requirements | LTX Documentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/usage-guides/prompting-guide | Prompting Guide | LTX Documentation | 2026-09-07 |
| https://github.com/Lightricks/LTX-2/blob/main/packages/ltx-trainer/docs/configuration-reference.md | LTX-2 trainer configuration reference · Lightricks/LTX-2 · GitHub | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:ltx-2-5`, thread `ltx-video`, 1 dated events 2026-08-11 → 2026-08-11.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
