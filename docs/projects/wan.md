---
title: WAN
category: projects
date: 2026-07-31
tags: [project, wan, wan-video-generation]
aliases: ["WAN", "Wan", "Wan2.2 dyno"]
---

# WAN

**Development line:** `project:wan` · thread `wan-video-generation`  
**Last event:** 2026-07-31 · 3 dated since 2025-09-23 · **Researched:** 2026-09-05 · confidence: medium

## What it is

WAN — a video-generation family for creators and developers: text-to-video, image-to-video, speech/reference-driven video, character animation and replacement. Wan2.2 remains an Apache-2.0 local model line; current hosted APIs expose newer 2.6/2.7 models. Local A14B inference needs at least 80 GB VRAM in the official example. Verdict: use current hosted WAN for production generation; use Wan2.2 when local, inspectable weights and community acceleration matter.

## Development line

- **2025-09-23 — Alibaba Wan 2.5 appeared as a text-to-video model on WaveSpeed.** On 2025-09-23, a WaveSpeed model route identified Alibaba Wan 2.5 as a text-to-video offering. This is a material ecosystem availability step because it gave practitioners a named hosted route for using that WAN version for video generation.
- **2025-10-01 — Wan 2.2 Lightning assets surfaced for four-step text-to-video workflows.** On 2025-10-01, the linked resources identified a Wan 2.2 Lightning four-step Dyno variant, a corresponding FP8 ComfyUI artifact, and a workflow page. This is a material practical step because it points to a faster, workflow-ready inference path for Wan 2.2 text-to-video generation.
- **2026-07-31 — WAN exposed a realtime playground route.** On 2026-07-31, the WAN Create site included a lab playground route labeled realtime. This is a material interface-development step because it indicates an interactive realtime entry point for WAN, distinct from a model-download or batch-workflow link.

## What changed

2025-09-23 — Wan 2.5 appeared as a hosted text/image-to-video API with synced audio, 480p–1080p output and 5/10-second jobs. 2025-10-01 — the community Wan2.2-Lightning path added a named 4-step Dyno checkpoint directory for the Wan2.2 T2V-A14B base; its repository lists the directory at 28.6 GB and the companion ComfyUI FP8 asset identifies the exact T2V model family. 2026-07-31 — a WAN Realtime playground route was available, but the accessible page exposes no model name, latency, pricing, or public usage contract. 2026-08-04 — a canary version of the same Realtime route was available; its accessible page likewise exposes no release details, so it is not evidence of a separate public model. 2025-07-28 — omitted earlier step: Wan2.2 released code and weights and gained ComfyUI and Diffusers integration. 2025-09-19 — omitted earlier step: Wan2.2-Animate-14B added character animation and replacement. 2026-09-02 — current hosted documentation lists Wan 2.6/2.7 video APIs; Wan2.7 supports 720p/1080p, 2–15-second, 30-fps text-to-video and image-to-video variants.

## How to use this

From 2025-10-01, practitioners could evaluate Wan 2.2 through the linked four-step Lightning/ComfyUI workflow path when low-step video inference mattered; from 2026-07-31, they should also evaluate the public WAN realtime playground separately from batch workflows. Treat the 2026-08-04 canary endpoint as unverified deployment infrastructure, not a public capability change.

1. For a current hosted text-to-video job, submit a prompt to the Wan API, select a supported size and duration, retain the returned task ID, then poll rather than resubmitting duplicate work.
  — <https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference>
2. For local Wan2.2, clone the official repository, install its requirements, download the matching checkpoint, then run generate.py with the intended task and resolution.
  — <https://github.com/Wan-Video/Wan2.2>
3. For accelerated local Wan2.2 T2V experimentation, download both the base A14B checkpoint and LightX2V assets, then pass the Lightning LoRA directory to the official generation command.
  — <https://huggingface.co/lightx2v/Wan2.2-Lightning>

## Best practices

- Pin a seed for reproducibility, but do not treat a fixed seed as a guarantee of identical video output.
  — <https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference>
- Treat model version, resolution, duration, audio, and region as explicit job parameters; they affect availability, cost, and output limits.
  — <https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference>
- Use a local Wan2.2 workflow only with hardware sized for it; the official A14B single-GPU 720p example states a minimum of 80 GB VRAM.
  — <https://github.com/Wan-Video/Wan2.2>
- Use Lightning-style acceleration as a community add-on to the matching base model, not as a replacement for the base checkpoint.
  — <https://huggingface.co/lightx2v/Wan2.2-Lightning>

## Superseded by this

- 2025-09-23: treating Wan 2.5 as the current WAN endpoint is obsolete; current Alibaba documentation lists Wan 2.6 and Wan 2.7 video model families.
- 2025-10-01: treating the Dyno 4-step Wan2.2 asset as the default WAN path is obsolete for hosted production; it remains a community local-inference option.
- 2026-07-31 and 2026-08-04: treating either Realtime playground URL as a documented product specification is unsupported; neither accessible route exposed a public contract.

## Still unknown

- The accessible Realtime and canary Realtime pages were shell pages with no extractable model, release date, latency, quota, or pricing information; their 2026-07-31 and 2026-08-04 events cannot be characterized beyond route availability.
- The dated WAN 2.5 event is supported here by a third-party API provider rather than an accessible first-party announcement; its exact original release scope remains unverified.
- WAN spans two operationally different subjects: open local Wan2.2 weights and later hosted Wan 2.5–2.7 APIs. They share a name but should not be treated as interchangeable deployment targets.

## Sources

| source | title | read |
|---|---|---|
| https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference | Wan - text-to-video API reference | 2026-09-05 |
| https://www.alibabacloud.com/help/tc/model-studio/video-generate-edit-model/ | Video generation and editing model list | 2026-09-05 |
| https://github.com/Wan-Video/Wan2.2 | Wan2.2 — official repository | 2026-09-05 |
| https://huggingface.co/lightx2v/Wan2.2-Lightning | lightx2v/Wan2.2-Lightning | 2026-09-05 |
| https://huggingface.co/lightx2v/Wan2.2-Lightning/tree/main/Wan2.2-T2V-A14B-4steps-250928-dyno | Wan2.2 Lightning Dyno 4-step directory | 2026-09-05 |
| https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/blob/main/T2V/Wan2_2-T2V-A14B-HIGH_4_steps-250928-dyno-lightx2v_fp8_e4m3fn_scaled_KJ.safetensors | Kijai Wan2.2 T2V-A14B Dyno 4-step FP8 asset | 2026-09-05 |
| https://wavespeed.ai/models/alibaba/wan-2.5/text-to-video | Wan 2.5 Text-to-Video API on WaveSpeed | 2026-09-05 |
| https://create.wan.video/lab/playground/realtime | Wan Realtime playground | 2026-09-05 |
| https://canary-create.wan.video/lab/playground/realtime | Wan Realtime playground canary route | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:wan`, thread `wan-video-generation`, 3 dated events 2025-09-23 → 2026-07-31.
- **Practical note:** From 2025-10-01, practitioners could evaluate Wan 2.2 through the linked four-step Lightning/ComfyUI workflow path when low-step video inference mattered; from 2026-07-31, they should also evaluate the public WAN realtime playground separately from batch workflows. Treat the 2026-08-04 canary endpoint as unverified deployment infrastructure, not a public capability change.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
