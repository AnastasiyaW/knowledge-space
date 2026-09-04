---
title: LTX-2.3
category: projects
date: 2026-07-30
tags: [ltx-video, project]
aliases: ["LTX Video", "LTX-2.3"]
---

# LTX-2.3

**Development line:** `project:ltx-video` · thread `ltx-video`  
**Last event:** 2026-07-30 · 3 dated since 2026-03-05 · **Researched:** 2026-09-04 · confidence: medium

## What it is

LTX-2.3 is a 22B DiT-based audio-video foundation model for teams generating synchronized video and audio locally, in ComfyUI, or through the LTX API.

- Text-to-video and image-to-video generation.
- Audio-to-video, Retake, Extend, and Reframe through Pro.
- Dev, distilled, fp8, and latent-upscaler weight paths.

Parameter count is 22B; the current Hugging Face repository is 156 GB and the dev checkpoint alone is 46.1 GB. We keep it for existing integrations and 2.3-specific adapters; begin new multi-shot, footage-editing, or deep fine-tuning work on LTX-2.5.

## Development line

- **2026-03-05 — LTX-2.3 was presented with documentation and a text-to-video playground.** Fast handled text/image-to-video, while Pro added audio-to-video, Retake, and Extend; 22B dev/distilled weights and latent upscalers shipped.
- **2026-03-05 — LTX-2.3 model files and a ComfyUI text-to-video workflow were linked.** Fast handled text/image-to-video, while Pro added audio-to-video, Retake, and Extend; 22B dev/distilled weights and latent upscalers shipped.
- **2026-07-30 — An LTX-2.3 22B IC LoRA for relighting was published.** On 2026-07-30, a Hugging Face resource named LTX-2.3-22B-IC-LoRA-Relight was linked. This is a material extension of the LTX-2.3 line because it adds a specialized relighting capability through a LoRA resource.

## What changed

- 2026-03-05 — LTX-2.3 became the API default: Fast handled text/image-to-video, while Pro added audio-to-video, Retake, and Extend; 22B dev/distilled weights and latent upscalers shipped.
- 2026-04-23 — Asynchronous HDR conversion added SDR-to-EXR output.
- 2026-05-03 — Async V2 expanded to text-to-video, image-to-video, audio-to-video, Retake, and Extend.
- 2026-07-02 — LTX-2 was deprecated, with temporary automatic routing to LTX-2.3.
- 2026-07-07 — Asynchronous video reframe added generated fill for a new aspect ratio.
- 2026-07-30 — LTX-2.3-22B-IC-LoRA-Relight added controlled exterior-video relighting from a source clip plus a light-direction ball.
- 2026-08-02 — LTX-2.3 text-to-video and image-to-video gained a 720p tier.
- 2026-08-11 — LTX-2.5 added Fast up to 4K, Pro at 720p/1080p, camera motion, last-frame image-to-video, and automatic duration; it is now the recommended starting point.
- 2026-08-16 — LTX-2 API model IDs stopped working; remaining migration targets are LTX-2.3 and LTX-2.5.

## How to use this

We use LTX-2.3 through its documented text-to-video route or the linked ComfyUI workflow from 2026-03-05. We evaluate the dedicated 22B IC relighting LoRA from 2026-07-30 when relighting is required.

1. Keep LTX-2.3 for a working integration or a 2.3-specific adapter; select LTX-2.5 for a new project.
  — <https://ltx.io/model/ltx-2-3>
2. Create a Developer Console API key, then submit a text-to-video or image-to-video request.
  — <https://docs.ltx.video/quickstart>
3. Use `ltx-2-3-fast` for text/image previews; use `ltx-2-3-pro` when the workflow needs audio-to-video, Retake, Extend, or Reframe.
  — <https://docs.ltx.io/models/ltx-2-3>
4. For production, submit a V2 async job, retain its job ID, poll to completion, and download the result URL.
  — <https://docs.ltx.io/async-jobs>
5. For a local run, clone LTX-2, run `uv sync`, download LTX-2.3 plus Gemma 3 12B, then choose the distilled pipeline for speed or the two-stage HQ pipeline for quality.
  — <https://huggingface.co/Lightricks/LTX-2.3/blob/main/README.md>
6. In ComfyUI, update ComfyUI first, load the supplied text-to-video workflow, and place its fp8 checkpoint, LoRAs, and spatial upscaler in the named model folders.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_t2v.json>
7. For exterior-video relighting, use the official single-stage graph with the Relight IC-LoRA at weight 1.0 and a source clip carrying the light-direction ball.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight>

## Best practices

- Treat width and height divisible by 32 and frame count divisible by 8+1 as an input contract; otherwise pad with -1 and crop after generation.
  — <https://huggingface.co/Lightricks/LTX-2.3/blob/main/README.md>
- Write one focused, chronological shot with explicit action, camera, lighting, and audio; rewrite prompts from other video models instead of pasting their tags or shot lists unchanged.
  — <https://docs.ltx.io/api-documentation/implementation-guides/prompting-guide>
- Use Fast for iterative text/image generation and reserve Pro for the endpoint set that requires it.
  — <https://docs.ltx.io/models/ltx-2-3>
- Use asynchronous jobs for production workloads rather than holding a long-lived synchronous connection.
  — <https://docs.ltx.io/async-jobs>
- For Relight, stay with exterior footage, align the ball-bearing reference to the target clip, use the minimal direction prompt, and avoid the true two-stage path because Stage 2 drops the conditioning.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight>
- When migrating from LTX-2, retrain custom LoRAs for LTX-2.3’s latent space instead of assuming drop-in compatibility.
  — <https://ltx.io/model/ltx-2-3>

## Superseded by this

- 2026-03-05 — “Custom LTX-2 LoRAs work unchanged on LTX-2.3” is obsolete; retraining is required for the 2.3 latent space.
- 2026-08-11 — “LTX-2.3 is the recommended start for a new project” is superseded by LTX-2.5; LTX-2.3 remains supported for existing integrations.
- 2026-08-16 — “`ltx-2-fast` and `ltx-2-pro` remain valid API model IDs” is obsolete; those requests return errors.

## Still unknown

- The 2026-07-30 item is a first-party IC-LoRA adapter release, not a new LTX-2.3 base checkpoint; available sources do not define whether every adapter release belongs in the core-model history.
- The Relight model card does not display an independent publication date, so its timing is anchored to 2026-07-30 while its technical scope is first-party verified.
- The original Studio text-to-video URL now redirects to the Studio home; without a dated snapshot, its exact 2026-03-05 interface and availability cannot be reconstructed.

## Sources

| source | title | read |
|---|---|---|
| https://ltx.io/model/ltx-2-3 | LTX-2.3: Previous Generation AI Video Model | LTX | 2026-09-04 |
| https://docs.ltx.video/quickstart | Quick Start | LTX Documentation | 2026-09-04 |
| https://app.ltx.studio/ltx-2-playground/t2v | AI video production | LTX | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3/tree/main | Lightricks/LTX-2.3 at main | 2026-09-04 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_t2v.json | workflow_templates/templates/video_ltx2_3_t2v.json at main · Comfy-Org/workflow_templates · GitHub | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight | Lightricks/LTX-2.3-22b-IC-LoRA-Relight · Hugging Face | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3/commits/main | Commits · Lightricks/LTX-2.3 | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3/blob/main/README.md | README.md · Lightricks/LTX-2.3 at main | 2026-09-04 |
| https://docs.ltx.io/models/ltx-2-3 | LTX-2.3 | LTX Documentation | 2026-09-04 |
| https://docs.ltx.io/api-documentation/implementation-guides/prompting-guide | Prompting Guide | LTX Documentation | 2026-09-04 |
| https://docs.ltx.io/async-jobs | Async Jobs | LTX Documentation | 2026-09-04 |
| https://docs.ltx.io/api-changelog | API Changelog | LTX Documentation | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:ltx-video`, thread `ltx-video`, 3 dated events 2026-03-05 → 2026-07-30.
- **Practical note:** We use LTX-2.3 through its documented text-to-video route or the linked ComfyUI workflow from 2026-03-05. We evaluate the dedicated 22B IC relighting LoRA from 2026-07-30 when relighting is required.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
