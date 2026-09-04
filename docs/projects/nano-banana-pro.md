---
title: Nano Banana Pro
category: projects
date: 2025-11-26
tags: [nano-banana-pro, nano_banana, nano_banana_pro, project]
aliases: ["Nano Banana Pro"]
---

# Nano Banana Pro

**Development line:** `project:nano-banana-pro` · thread `nano-banana-pro`  
**Last event:** 2025-11-26 · 2 dated since 2025-11-20 · **Researched:** 2026-09-04 · confidence: high

## What it is

Nano Banana Pro is Google's Gemini 3 Pro Image model for creators and developers making complex visual assets.

- Generates and edits images from text and image inputs.
- Supports Google Search grounding, text rendering, localization, multi-reference composition, and up to 4K output.
- The stable API ID is `gemini-3-pro-image`; it accepts 65,536 input tokens and returns up to 32,768 output tokens, with up to six high-fidelity object references, five character references, or 14 total references depending on use.

## Development line

- **2025-11-20 — Google introduced Nano Banana Pro.** On 2025-11-20, Google published an official AI blog article for Nano Banana Pro and linked the model in Google AI Studio. This is the public introduction point for Nano Banana Pro in this development line.
- **2025-11-26 — Google published prompting guidance for Nano Banana Pro.** The linked prompting guide is dated 2025-11-20 and teaches use rather than announcing a revision.

## What changed

- 2025-11-20 — Nano Banana Pro launched as Gemini 3 Pro Image; its Gemini API preview endpoint was `gemini-3-pro-image-preview`.
- 2025-11-26 — No separate model release is verified: the linked prompting guide is dated 2025-11-20 and teaches use rather than announcing a revision.
- 2025-12-01 — Search AI Mode expanded Nano Banana Pro to more English-language countries for Google AI Pro and Ultra subscribers.
- 2025-12-17 — Search expanded Nano Banana Pro access to more people in the United States.
- 2025-12-23 — Google listed availability in Gemini, Search AI Mode, NotebookLM, Workspace, Flow, Mixboard, AI Studio, Vertex AI, and other developer surfaces.
- 2026-04-20 — Google AI Pro and Ultra subscriptions added greater AI Studio limits and Nano Banana Pro access.
- 2026-05-28 — `gemini-3-pro-image` became the GA API ID; the preview ID was deprecated with a June 25, 2026 shutdown date.

## How to use this

From 2025-11-20, we could use Nano Banana Pro through Google AI Studio; from 2025-11-26, follow Google's model-specific prompting guidance when working with it.

1. In Gemini Apps: with a Google AI Plan, create an image in Nano Banana 2 or Nano Banana 2 Lite, then choose More → Redo with Pro for the detailed pass; daily quota can block the redo.
  — <https://support.google.com/gemini/answer/14286560?hl=en-Documentation>
2. In Search AI Mode: select Pro, choose Image, then Create Images; describe the image or upload one to edit. Availability is English-only and account-, age-, plan-, and country-dependent.
  — <https://support.google.com/websearch/answer/16649374?co=GENIE.Platform%3DDesktop&hl=en-EN>
3. In the Gemini API: call the stable `gemini-3-pro-image` model with text and/or image inputs, then handle its image and text output.
  — <https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image?authuser=00>
4. Editing: supply an image with a direct change request, then continue the same conversation for follow-up edits.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>
5. Delivery: set `response_format.type` to `image` and request the needed `aspect_ratio` and `image_size` when framing or output resolution matters.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>

## Best practices

- Model selection: reserve it for complex professional assets and instructions; use Nano Banana 2 when the general cost-and-latency balance is more important.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>
- Prompts: specify subject, composition, action, location, style, and a direct edit instruction.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Composition: explicitly state the aspect ratio, camera, lighting, text placement, and factual constraints.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- References: name the role of each uploaded image, such as pose, style, or background.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Edits: iterate in a multi-turn conversation rather than restarting every revision.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>
- Outputs: independently check small text, spelling, facts in diagrams, translations, complex blends, and character consistency before use.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Inputs: upload only images for which you have the necessary rights.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>

## Superseded by this

- 2026-05-28 — Use `gemini-3-pro-image-preview` for a new Nano Banana Pro API integration. Superseded by the GA endpoint `gemini-3-pro-image`; the preview endpoint was scheduled to shut down on 2026-06-25.

## Still unknown

- The historical AI Studio deep link `https://aistudio.google.com/prompts/new_chat?model=nano-banana-pro` requires sign-in, so its current model preselection and quota were not independently verified from a public page.
- Consumer access varies by account, Google AI plan, language, age, country, and changing daily quotas; this does not establish eligibility for a particular account.

## Sources

| source | title | read |
|---|---|---|
| https://blog.google/technology/ai/nano-banana-pro/ | Introducing Nano Banana Pro | 2026-09-04 |
| https://blog.google/products/gemini/prompting-tips-nano-banana-pro/ | 7 tips to get the most out of Nano Banana Pro | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/changelog | Release notes | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image?authuser=00 | Gemini 3 Pro image | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/image-generation?authuser=00 | Image generation | Gemini API | Google AI for Developers | 2026-09-04 |
| https://blog.google/products-and-platforms/products/search/gemini-3-ai-mode-more-countries/ | Gemini 3 and Nano Banana Pro in Search are coming to more countries around the world. | 2026-09-04 |
| https://blog.google/products-and-platforms/products/search/google-ai-mode-update-gemini-3-flash/ | Gemini 3 Flash is rolling out globally in Google Search | 2026-09-04 |
| https://blog.google/products-and-platforms/products/gemini/where-to-use-nano-banana-pro/ | Here’s where you can use Nano Banana Pro | 2026-09-04 |
| https://blog.google/innovation-and-ai/technology/developers-tools/google-one-ai-studio/ | Start vibe coding in AI Studio with your Google AI subscription. | 2026-09-04 |
| https://support.google.com/gemini/answer/14286560?hl=en-Documentation | Generate & edit images with Gemini Apps - Computer - Gemini Apps Help | 2026-09-04 |
| https://support.google.com/websearch/answer/16649374?co=GENIE.Platform%3DDesktop&hl=en-EN | Create and edit images in Google Search - Computer - Google Search Help | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:nano-banana-pro`, thread `nano-banana-pro`, 2 dated events 2025-11-20 → 2025-11-26.
- **Practical note:** From 2025-11-20, practitioners could use Nano Banana Pro through Google AI Studio; from 2025-11-26, they should use Google's model-specific prompting guidance when working with it.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
