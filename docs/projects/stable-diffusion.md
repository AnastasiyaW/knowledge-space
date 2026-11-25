---
title: Stable Diffusion
category: projects
date: 2022-07-26
tags: [dataset, project, stable-diffusion, stable-diffusion-development, stable_diffusion, stable_diffusion_v2_2_2_xl_beta]
aliases: ["Stable Diffusion", "Stable Diffusion 3"]
---

# Stable Diffusion

**Development line:** `project:stable-diffusion` · thread `stable-diffusion-development`  
**Last event:** 2022-07-26 · 1 dated since 2022-07-26 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Stable Diffusion is a family of generative image models for artists and developers who need a choice between self-hosting and an API instead of a closed service like Midjourney.

- text-to-image and image-to-image
- ControlNet for control via Canny, depth or blur
- Large, Turbo, Medium and Flash variants

The SD 3.5 API outputs 1 MP images, default 1024×1024; image-to-image input accepts up to 10 MiB.

For new integrations, use SD 3.5 rather than earlier SD3 or SDXL beta identifiers.

## Development line

- **2022-07-26 — Stable Diffusion beta-access signup milestone.** On 2022-07-26, the Stable Diffusion record linked to Stability AI's beta-signup form. This supports retaining a beta-access milestone, but it does not establish a released model version, eligibility, or feature set.

## What changed

2022-07-26 — beta registration meant limited testing rather than public weight release; research access opened 2022-08-10, public release followed on 2022-08-22.

2023-03-09 — the NeuralPic link specifies no dataset, model or Stable Diffusion release; product change unconfirmed.

2023-03-25 — the `stable_diffusion_v2_2_2_xl_beta` entry has no URL, so the date and change cannot be verified. On 2023-04-13 the official API added the `stable-diffusion-xl-beta-v2-2-2` engine for SDXL beta and DreamStudio.

2024-03-07 — the link points only to an X profile, leaving the specific post unverifiable. The official status of SD3 in this window was early preview and waitlist with variants from 800M to 8B parameters.

2024-03-13 — the specific X post is unavailable to check; no confirmed model or API change comes from it.

On 2024-06-12 SD3 Medium was released for REST API and weight download; on 2024-10-22 SD 3.5 Large and Large Turbo appeared, and on 2024-10-29 SD 3.5 Medium followed.

From 2025-04-17 SD3 API identifiers redirect automatically to SD 3.5 equivalents. In the active Core Models list from 2026-05-20, SD 3.5 Medium, Large and Large Turbo remain.

## How to use this

For the 2022-07-26 historical record, treat beta signup—not a confirmed public release—as the operational access route; confirm current availability and terms separately.

1. Choose a path: API for managed integration or local hosting for infrastructure control. For 1 MP quality take Large, for speed pick Large Turbo or Flash, and for lower resource cost pick Medium.  
  — <https://platform.stability.ai/docs/api-reference>
2. For the API, create an account and key, then pass the key only in the Authorization header.  
  — <https://platform.stability.ai/docs>
3. Send a multipart POST to `/v2beta/stable-image/generate/sd3` with `prompt`, `model` and `output_format`; for image-to-image pass the source image, `strength` and `mode=image-to-image`.  
  — <https://platform.stability.ai/docs/api-reference>
4. For local runs, accept the weight license, install `diffusers`, `transformers` and `accelerate`, load `StableDiffusion3Pipeline`, and save output images.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
5. To anchor composition to reference images, attach SD3.5 Large ControlNet with a Canny, depth or blur condition image.  
  — <https://github.com/Stability-AI/sd3.5>

## Best practices

- Do not store or commit API keys: pass the key in the Authorization header and rotate it if leaked.  
  — <https://platform.stability.ai/docs>
- Set an explicit seed for repeatable comparisons: it controls generation randomness.  
  — <https://platform.stability.ai/docs/api-reference>
- For SD 3.5 Medium, keep prompts within 256 T5 tokens: longer requests risk edge artifacts. Use Skip Layer Guidance for structure and anatomy.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- When VRAM is tight, use official 4-bit quantization and CPU offload instead of arbitrary weight swaps.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- Check the license before commercial self-hosting: the Community License covers entities under $1M annual revenue, above which an Enterprise License is required.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- Add custom content-safety guardrails in production: training filters do not prevent harmful outputs.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>

## Superseded by this

- 2022-07-26: joining the beta waitlist was superseded by the 2022-08-22 Stable Diffusion public release.
- 2023-04-13: engine limits and the name `stable-diffusion-xl-beta-v2-2-2` apply to historical SDXL beta, not current API routes.
- 2024-02—03: waiting for SD3 early preview was superseded by SD3 and SD 3.5 releases.
- 2025-04-17: API instructions targeting `sd3-large`, `sd3-large-turbo` and `sd3-medium` are obsolete because requests redirect to SD 3.5.

## Still unknown

- Content of the 2022-07-26 beta registration form is unavailable; its role as preliminary access rests on later official announcements.
- The NeuralPic link from 2023-03-09 does not connect the event to a specific Stable Diffusion dataset, checkpoint or release.
- The 2023-03-25 record lacks a URL: the name resembles the later SDXL beta API engine, but does not prove it appeared on that date.
- X links from 2024-03-07 and 2024-03-13 returned no content, leaving model, license, or management changes unverified.
- Tags `dataset`, `stable_diffusion` and `stable_diffusion_v2_2_2_xl_beta` may conflate an unconfirmed dataset link, an unofficial beta lead, and official model releases.

## Sources

| source | title | read |
|---|---|---|
| https://stability.ai/beta-signup-form | Stability AI beta signup form — недоступна при чтении | 2026-09-04 |
| https://twitter.com/EMostaque | Emad Mostaque on X — недоступен при чтении | 2026-09-04 |
| https://twitter.com/EMostaque/status/1767662732797411433 | Emad Mostaque, post 1767662732797411433 — недоступен при чтении | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-launch-announcement | Stable Diffusion launch announcement | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-public-release | Stable Diffusion Public Release | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-xl-beta-available-for-api-customers-and-dreamstudio-users | Stable Diffusion XL Beta Available for API Customers and DreamStudio Users | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-3 | Stable Diffusion 3 | 2026-09-04 |
| https://platform.stability.ai/docs/release-notes | Stability AI Developer Platform release notes | 2026-09-04 |
| https://stability.ai/core-models | Stability AI Core Models | 2026-09-04 |
| https://platform.stability.ai/docs | Stability AI API: Getting Started | 2026-09-04 |
| https://platform.stability.ai/docs/api-reference | StabilityAI REST API (v2beta) | 2026-09-04 |
| https://huggingface.co/stabilityai/stable-diffusion-3.5-medium | stabilityai/stable-diffusion-3.5-medium model card | 2026-09-04 |
| https://github.com/Stability-AI/sd3.5 | Stability-AI/sd3.5 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:stable-diffusion`, thread `stable-diffusion-development`, 1 dated events 2022-07-26 → 2022-07-26.
- **Practical note:** For the 2022-07-26 historical record, treat beta signup—not a confirmed public release—as the operational access route; confirm current availability and terms separately.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
