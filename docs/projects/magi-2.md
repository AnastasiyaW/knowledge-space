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

- T2V: generates video and audio from text prompts.
- I2V: animates an input frame with audio.
- Joint audio-video generation: aligns sound and motion in a single model.
- Two-stage pipeline: outputs up to 1080p using preview and refiner stages.

6B active parameters per token, about 307 GB of weights, and eight Hopper GPUs.
This is an infrastructure-heavy open preview release rather than a lightweight API tool.

## Development line

- **2026-08-07 — Sand AI published MAGI-2 preview materials.** 114B parameters, about 6B active per token, and a unified MagiMoE audio-video architecture. Repository documentation limits the release to 10-second clips, a preview stage with a refiner up to 1080p, and T2V and I2V with audio.

## What changed

2026-08-07 — MAGI-2 Preview became available with weights and inference code. Primary Sand AI material from 2026-08-05 specifies the scale: 114B parameters, about 6B active per token, and a unified MagiMoE audio-video architecture. Current repository documentation defines the release scope: only 10-second clips, a preview stage and a refiner up to 1080p, and T2V and I2V with audio.

## How to use this

As of 2026-08-07, treat MAGI-2 as a public preview from Sand AI. Check the linked repository, model page, and API v2 documentation before evaluating or integrating it. Specific capabilities and access conditions still require direct verification.

1. Prepare a Linux environment with Python 3.12, current CUDA, ffmpeg, and eight NVIDIA Hopper GPUs as required by the inference code.
  — <https://github.com/SandAI-org/MAGI-2-preview>
2. Pull the Docker image or build from source; pin the image tag to a specific commit rather than moving latest for reproducibility.
  — <https://github.com/SandAI-org/MAGI-2-preview>
3. Download the full checkpoint set from sand-ai/MAGI-2-preview into the ckpt directory without renaming directories.
  — <https://huggingface.co/sand-ai/MAGI-2-preview>
4. Run T2V with a text prompt or I2V with a prompt and source frame; the result is a 10-second clip, and 1080p passes through preview and refiner stages.
  — <https://github.com/SandAI-org/MAGI-2-preview>

## Best practices

- Pin the Docker tag to a specific commit and record it with results: latest changes.
  — <https://github.com/SandAI-org/MAGI-2-preview>
- Keep the default staged offloading of preview and refiner for 1080p: both components together with activations do not fit even on an 80 GB GPU.
  — <https://github.com/SandAI-org/MAGI-2-preview>
- Use structured prompt expansion for the full 10-second scenario when a manual prompt does not sufficiently define action, framing, and audio.
  — <https://github.com/SandAI-org/MAGI-2-preview>

## Superseded by this

- 2026-08-05 — No dated subsequent release supersedes MAGI-2 Preview in verified primary sources; documentation marks the distilled variant as coming soon.
- 2026-08-07 — The assumption that MAGI-2 is a ready public API product is obsolete: the verifiable current implementation provides open weights and inference code with cluster requirements.

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
- **Practical note:** As of 2026-08-07, treat MAGI-2 as a public preview from Sand AI. Consult its linked repository, model page, and API v2 documentation before evaluating or integrating it; specific capabilities and access conditions still require direct verification.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.