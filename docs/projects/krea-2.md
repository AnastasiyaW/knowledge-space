---
title: Krea 2 — Open-source release and ecosystem
category: projects
date: 2026-06-24
tags: [krea-2, open-source-release, project]
aliases: ["Krea 2"]
---

# Krea 2 — Open-source release and ecosystem

**Development line:** `project:krea-2` · thread `open-source-release`  
**Last event:** 2026-06-24 · 2 dated since 2026-06-23 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Krea 2 is an image generation model family for designers, developers, and researchers. The hosted API provides Medium, Large, and Medium Turbo with style references, moodboards, LoRA, and image-to-image. The open-source release provides RAW and Turbo weights with code for local text-to-image and LoRA training.

- Cloud: API, reference images, moodboards, sliders, and jobs.
- Local: RAW for fine-tuning and LoRA, Turbo for fast generation.

Local RAW is recommended up to 1K, Turbo runs at 1K–2K and 8 steps, and hosted Medium Turbo takes only 1K. Choose hosted Krea 2 for reference-driven workflows and RAW or Turbo for controlled local generation, as the checkpoint surfaces are related but not proven identical.

## Development line

- **2026-06-23 — Krea 2’s early community tooling and model artifacts surfaced.** RAW became the base for training and LoRA, and Turbo became the 8-step checkpoint for text-to-image.
- **2026-06-24 — Krea published Krea 2’s official open-source and deployment materials.** The open-weight version corresponds to Medium, while moodboard and style reference modules are omitted from the open release.

## What changed

On 2026-06-23, the official technical report, inference code, and open RAW and Turbo weights established the local pipeline: RAW became the base for training and LoRA, and Turbo became the 8-step checkpoint for text-to-image. On 2026-06-24, Krea clarified the release boundary: the open-weight version corresponds to Medium, and the moodboard and style reference modules are not included in the open release.

## How to use this

From 2026-06-24, practitioners should begin Krea 2 evaluation with the linked official Raw or Turbo resources and the named ComfyUI Turbo workflow, while treating the 2026-06-23 community artifacts as unverified alternatives.

1. Choose the surface: use open-weight RAW or Turbo for local generation and custom LoRA; use the hosted API for reference images, moodboards, and managed jobs.
  — <https://www.krea.ai/krea-2-open-source>
2. For local execution, take the official repository, run `uv sync`, download checkpoints, and set paths in `OSS_RAW` and `OSS_TURBO`.
  — <https://github.com/krea-ai/krea-2>
3. Start with official parameters: RAW at 52 steps and CFG 3.5 up to 1K; Turbo at 8 steps, CFG 0, `mu=1.15`, and size 1K–2K.
  — <https://github.com/krea-ai/krea-2>
4. In ComfyUI, import the official Turbo text-to-image workflow; its starting setup is 1024×1024 and KSampler at 8 steps.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_krea2_turbo_t2i.json>
5. For the hosted API, send a Bearer-authenticated POST to `.../krea-2/medium-turbo` with prompt, aspect ratio, and 1K resolution; save `job_id` and retrieve the result through the job endpoint or webhook.
  — <https://www.krea.ai/docs/api-reference/krea/krea-2-turbo>

## Best practices

- Train LoRA on RAW and run inference on Turbo; do not use RAW as the default fast production checkpoint.
  — <https://github.com/krea-ai/krea-2>
- Write natural detailed prompts; place words intended as text in the image in quotation marks.
  — <https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md>
- In hosted Krea, keep the prompt unchanged and adjust one slider at a time; 0 is the neutral value, and Raw/Low Creativity works best for precise control.
  — <https://www.krea.ai/blog/generative-sliders>
- For hosted LoRA, take a narrow dataset starting from three images, check auto-captions manually, and avoid mixing character, style, and product in the initial LoRA.
  — <https://www.krea.ai/blog/krea-2-lora-training>
- In the API, treat responses as asynchronous: 200 can return a pending job; use a webhook or status polling and handle failed or cancelled states explicitly.
  — <https://www.krea.ai/docs/api-reference/krea/krea-2-turbo>
- Run safety testing for your scenario before deploying open weights, and follow the Krea 2 Community License alongside the code license.
  — <https://huggingface.co/krea/Krea-2-Raw>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact mapping between hosted Krea 2 Medium or Medium Turbo and open-weight RAW or Turbo lacks published hash- or checkpoint-level correspondence; the AMA only states that the open-source version corresponds to Medium.
- The open model card lists 13B parameters, while the release page lists 12B dense DiT; these may be different counting boundaries, but without parameter accounting they cannot be reconciled into a single count.
- Official pages show no public RAW or Turbo checkpoint newer than 2026-06-24; current API documentation does not prove updates to open weights.
- The content of the X post from the 2026-06-23 event was not available for verification and was not used as evidence.

## Sources

| source | title | read |
|---|---|---|
| https://www.krea.ai/blog/krea-2-image-model | Introducing Krea 2 | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-lora-training | Krea 2 LoRA training is now available | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-api-launch | Krea 2 API | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-turbo | Krea 2 Turbo: Generate Images in 2 Seconds | 2026-09-04 |
| https://www.krea.ai/blog/generative-sliders | Introducing Generative Sliders | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-technical-report | Krea 2 Technical Report | 2026-09-04 |
| https://huggingface.co/krea/Krea-2-Raw | krea/Krea-2-Raw | 2026-09-04 |
| https://github.com/krea-ai/krea-2 | Krea 2 (K2) — official inference code | 2026-09-04 |
| https://www.krea.ai/krea-2-open-source | Krea 2 Open Source | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/1udnm0a/we_are_the_team_behind_krea_2_ask_us_anything/ | We are the team behind Krea 2. Ask us anything! | 2026-09-04 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_krea2_turbo_t2i.json | image_krea2_turbo_t2i.json | 2026-09-04 |
| https://www.krea.ai/docs/api-reference/introduction | Krea API reference: models, endpoints, and schemas | 2026-09-04 |
| https://www.krea.ai/docs/api-reference/krea/krea-2-turbo | Krea 2 Turbo API | 2026-09-04 |
| https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md | Prompting guidelines | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:krea-2`, thread `open-source-release`, 2 dated events 2026-06-23 → 2026-06-24.
- **Practical note:** From 2026-06-24, practitioners should begin Krea 2 evaluation with the linked official Raw or Turbo resources and the named ComfyUI Turbo workflow, while treating the 2026-06-23 community artifacts as unverified alternatives.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.