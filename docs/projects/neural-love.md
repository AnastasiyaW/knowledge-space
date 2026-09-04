---
title: neural.love
category: projects
date: 2022-12-23
tags: [neural-love, neural-love-image-tools, neural_love, project]
aliases: ["neural.love"]
---

# neural.love

**Development line:** `project:neural-love` · thread `neural-love-image-tools`  
**Last event:** 2022-12-23 · 2 dated since 2022-09-09 · **Researched:** 2026-09-04 · confidence: medium

## What it is

neural.love is a browser and API platform for creators who need AI image generation, image processing, and media workflows.

- Text-to-image generation with model, style, prompt, layout, HD, and image-input options.
- Image processing to upscale, sharpen, colorize, restore, and uncrop.
- Video-related creator workflows.

The documented API default is 300 requests per five minutes, and paid work consumes credits. We use it for bounded current work, but we do not make it a new long-term production dependency until ownership and support continuity are confirmed.

## Development line

- **2022-09-09 — neural.love linked an AI art generation route and documentation.** The AI Art Generator route was present; an earlier public listing makes this a visibility milestone, not a confirmed initial launch.
- **2022-12-23 — neural.love linked a dedicated image uncropping route.** The Uncrop route was present; its original model, settings, price, and limits remain unverified.

## What changed

- 2022-09-09: The AI Art Generator route was present; an earlier public listing makes this a visibility milestone, not a confirmed initial launch.
- 2022-12-23: The Uncrop route was present; its original model, settings, price, and limits remain unverified.
- 2023-08-28: NL 1.01 text-to-image and an updated HD mode went live, alongside image-to-image remix, category, search, and dark-theme updates.
- 2023-10-16: Uncrop 2.0 targeted glitches and aspect-ratio conversion.
- 2024-09-11: Uncrop 4 added three variants per input and retained one- or two-pass outpainting.
- 2024-11-11: MiniMax Video 01 brought image-to-video and text-to-video generation to the product.
- 2025-03-22: The suite added text-command image editing, agentic image stories, subject-reference text-to-video, Imgen 3, and a prompt-augmentation off switch.
- 2026-03-12: The owner put the product, brand, domain, codebase, and operating materials up for sale and said it would no longer make meaningful investment.

## How to use this

As of 2022-12-23, practitioners should treat neural.love’s visible image-tool line as spanning both AI art generation and a dedicated uncropping route, while verifying the contemporaneous feature scope before relying on either workflow.

1. For browser image generation, open AI Art Generator, choose a model and style, refine the prompt, and generate.
  — <https://neural.love/ai-art-generator>
2. For API access, sign in, open Settings, generate an API token, and send it as a Bearer token.
  — <https://docs.neural.love/>
3. For API image generation, POST to /v1/ai-art/generate with explicit prompt, style, layout, amount, isHd, and isPublic values; retain orderId and poll for completion.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
4. For API processing, obtain a presigned upload URL, upload the source, then create an image-processing order; use image_uncrop alone with outpainting or aspect_ratio and poll the returned order.
  — <https://docs.neural.love/ai-images-processing-api>
5. For browser outpainting, use the live Uncrop route to extend borders or change an image aspect ratio, then inspect the generated result before using it.
  — <https://neural.love/uncrop>

## Best practices

- Estimate credits with the same generation parameters before submitting a paid job.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
- Poll orders with increasing intervals such as 30, 45, 60, 90, and 150 seconds rather than tight-looping.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
- Set isPublic explicitly and run a non-sensitive canary before handling private material; the current documentation gives conflicting defaults.
  — <https://docs.neural.love/faq>
- Keep image_uncrop in its own processing job; the API says it cannot be combined with other image parameters.
  — <https://docs.neural.love/ai-images-processing-api>
- Treat Uncrop as creative expansion, not historical reconstruction: the product warns that inputs are downscaled, results vary, and historical accuracy is not its goal.
  — <https://neural.love/blog/uncrop-4-image-expansion>
- Replace deployed credentials before generating a new API token, because only one token is active per account and a new one disables the old token.
  — <https://docs.neural.love/>

## Superseded by this

- 2022-09-09 as the initial public availability of AI Art Generator — obsolete since 2022-08-23.
- Pre-Uncrop-4 instructions as current guidance — obsolete since 2024-09-11.
- The present owner still making meaningful product investment — obsolete since 2026-03-12.

## Still unknown

- No dated first-party launch note was found for the 2022-09-09 AI Art Generator link or the 2022-12-23 Uncrop link; their original model, inputs, price, and limits remain unverified.
- The historic https://docs.neural.love/docs route could not be retrieved today; its 2022 content may have moved, but is not verified here.
- Current API documentation conflicts on default art-generation visibility: the tutorial says all generations are public by default, while the FAQ says API generations are private by default.
- The asset-sale notice gives no closing date, buyer, transition plan, support commitment, or API SLA.
- A Simplified-Chinese search found no dated first-party corroboration for the two 2022 routes.

## Sources

| source | title | read |
|---|---|---|
| https://neural.love/ai-art-generator | AI Art Generator & AI Image Generator | neural.love | 2026-09-04 |
| https://neural.love/uncrop | Uncrop Image Online – Extend Photos for Free | neural.love | 2026-09-04 |
| https://docs.neural.love/ | Getting Started | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api | How to generate AI art with neural.love API | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/ai-images-processing-api | AI Images Processing API | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/faq | neural.love API - Frequently Asked Questions | The neural.love API Developer Hub | 2026-09-04 |
| https://akinix.com/forums/topic/209-curated-ai-art-generator-by-neurallove/ | Curated AI art generator by neural.love - General discussions - Akinix | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/xev8ds | Free stable diffusion generation website – neural.love | 2026-09-04 |
| https://neural.love/blog/new-text-to-image-model-and-future-roadmap | New text-to-image model is here & Future Roadmap | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/uncrop-2-0-feature-update | Feature Update: Uncrop 2.0 – Less Glitches | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/uncrop-4-image-expansion | Introducing Uncrop 4: Expand Your Images Like Never Before | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/video-generation-launch | Introducing Video Generation: Transform Images into Motion with neural.love | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/march-2025-release-notes | Product Updates: March 2025 Release Notes | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/neural-love-is-for-sale | neural.love assets are for sale | neural.love blog about AI stuff | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:neural-love`, thread `neural-love-image-tools`, 2 dated events 2022-09-09 → 2022-12-23.
- **Practical note:** As of 2022-12-23, practitioners should treat neural.love’s visible image-tool line as spanning both AI art generation and a dedicated uncropping route, while verifying the contemporaneous feature scope before relying on either workflow.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
