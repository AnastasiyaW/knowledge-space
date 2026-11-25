---
title: MAGI-2
category: projects
date: 2026-08-07
tags: [magi, magi-2, magi-2-preview, project]
aliases: ["MAGI-2"]
---

# MAGI-2

**Development line:** `project:magi-2` · thread `magi-2-preview`  
**Last event:** 2026-08-07 · 1 dated since 2026-08-07 · **Researched:** 2026-09-05 · confidence: high

## What it is

MAGI-2 Preview is a 114B-parameter unified audio-video MoE model for teams generating 10-second clips with synchronized audio locally from text or images.

- T2V creates video from text prompts with joint audio.
- I2V animates a starting frame into video with joint audio.
- Two-stage pipeline generates a preview and refines output up to 1080p.

The model uses 6B active parameters per token, roughly 307 GB of weights, and eight Hopper GPUs. This is an infrastructure-heavy open preview release, not a lightweight API tool.

## Development line

- **2026-08-07 — Sand AI published MAGI-2 preview materials.** The model uses 114B parameters with about 6B active per token on a unified MagiMoE audio-video architecture. Repository documentation limits the release to 10-second clips, a preview stage with a refiner up to 1080p, and T2V and I2V with synchronized sound.

## What changed

2026-08-07 — MAGI-2 Preview became available with weights and inference code. Primary material from Sand AI on 2026-08-05 specifies the scale: 114B parameters, about 6B active per token, and a unified MagiMoE audio-video architecture. Repository documentation limits the release to 10-second clips, a preview stage and refiner up to 1080p, and T2V and I2V with sound.

## How to use this

As of 2026-08-07, practitioners should treat MAGI-2 as a publicly previewed Sand AI project and consult its linked repository, model page, and API v2 documentation before evaluating or integrating it; specific capabilities and access conditions still require direct verification.

1. Prepare a Linux environment with Python 3.12, current CUDA, ffmpeg, and eight NVIDIA Hopper GPUs as required by the inference code.
  — <https://github.com/SandAI-org/MAGI-2-preview>
2. Pull the Docker image or build from source. Specify the image tag matching the commit rather than moving latest for reproducibility.
  — <https://github.com/SandAI-org/MAGI-2-preview>
3. Download the full checkpoint set from sand-ai/MAGI-2-preview into the ckpt folder without renaming directories.
  — <https://huggingface.co/sand-ai/MAGI-2-preview>
4. Run T2V with a text prompt or I2V with a prompt and first frame. The output is a 10-second clip, and 1080p passes through preview and refiner.
  — <https://github.com/SandAI-org/MAGI-2-preview>

## Best practices

- Pin the Docker tag to a specific commit and log it with results, because latest changes.
  — <https://github.com/SandAI-org/MAGI-2-preview>
- Keep the default staged offload for preview and refiner at 1080p, because both components and activations do not fit together even on an 80 GB GPU.
  — <https://github.com/SandAI-org/MAGI-2-preview>
- Use structured prompt expansion for the full 10-second scene when a manual prompt does not set action, framing, and audio.
  — <https://github.com/SandAI-org/MAGI-2-preview>

## Superseded by this

- 2026-08-05 — MAGI-2 Preview is not replaced by a separate publicly dated subsequent release in verified primary sources; documentation marks the distilled variant as coming soon.
- 2026-08-07 — The assumption that MAGI-2 is a ready public API product is obsolete: the verified implementation provides open weights and inference code with cluster requirements.

## Still unknown

- URL https://platform.sand.ai/docs/api-v2 returned no readable documentation during verification, so API features, pricing, limits, and current availability remain unconfirmed.
- Verified primary sources provide no separately dated event after 2026-08-07; changes in the current README cannot be reliably dated as a new release.

## Sources

| source | title | read |
|---|---|---|
| https://sand.ai/blog/magi-2-preview | MAGI-2 Preview: Scaling Video Generation Models Efficiently | 2026-09-05 |
| https://github.com/SandAI-org/MAGI-2-preview | SandAI-org/MAGI-2-preview | 2026-09-05 |
| https://huggingface.co/sand-ai/MAGI-2-preview | sand-ai/MAGI-2-preview | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:magi-2`, thread `magi-2-preview`, 1 dated events 2026-08-07 → 2026-08-07.
- **Practical note:** As of 2026-08-07, practitioners should treat MAGI-2 as a publicly previewed Sand AI project and consult its linked repository, model page, and API v2 documentation before evaluating or integrating it; specific capabilities and access conditions still require direct verification.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.