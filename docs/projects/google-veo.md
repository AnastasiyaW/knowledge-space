---
title: Veo 3.1
category: projects
tags: [google-veo, project, veo-3-1]
aliases: ["VEO 3.1 Fast", "Veo 3.1"]
---

# Veo 3.1

**Development line:** `project:google-veo` · thread `veo-3-1`  
**Events:** 0 dated, - → - · **Researched:** 2026-09-04 · confidence: medium

## What it is

Veo 3.1 — Google’s video-generation model for creators and product teams that need native audio, reference-image direction, first/last-frame transitions, or Veo clip extension rather than a general conversational editor. - Text-to-video, image-to-video, reference-image direction, interpolation, and extension. - Native audio, 16:9 or 9:16 output, and Standard, Fast, and Lite tiers. Limit: 4-, 6-, or 8-second, 24fps clips; 1080p/4K and reference images require eight seconds, extension is 720p, and English is the fully evaluated prompt language. Verdict: use Veo 3.1 for controlled shot construction or existing Veo pipelines; Google now recommends Gemini Omni Flash as the default for new general video-generation work.

## Development line

- (no material events recorded)

## What changed

Veo 3.1 — the model line moved from early third-party access pages to Google Preview, then GA and additional tiers. - 2025-10-13: A Higgsfield Veo 3.1 page appeared. Its current content is a third-party access surface; it does not prove that Google launched the model or those features on this date. - 2025-10-15: Google introduced Veo 3.1 and Veo 3.1 Fast in Vertex AI Preview. Flow added audio to Ingredients to Video, Frames to Video, and Extend, plus multi-image direction, first/last-frame transitions, and clip extension. The same-day Flowith invitation could not be read; the Hugging Face Space is an independently hosted, currently running front end rather than evidence of a separate Google model. - Found today — 2025-11-17: Google’s enterprise model page records GA Standard and Fast IDs, veo-3.1-generate-001 and veo-3.1-fast-generate-001. - Found today — 2026-01-13: Ingredients-to-Video consistency, native 9:16, 4K, and improved 1080p reached the Gemini API and AI Studio. - Found today — 2026-04-03: Lite and a standalone Veo upscaler made the line a three-tier family. - Found today — 2026-06-30: Google changed Gemini API routing: Gemini Omni Flash is the default for general video work, while Veo 3.1 remains for extension, last-frame control, and legacy pipelines.

## How to use this

As of 2025-10-15, treat these third-party Veo 3.1 links as unverified research leads; do not change a production workflow until the product version, provider relationship, and capabilities are independently confirmed.

1. For a no-code workflow, open Google Flow, select Veo 3.1, then choose Text to Video, Frames to Video, Ingredients to Video, or Video Extension; available features vary by subscription, platform, and region.
  — <https://flow.google/>
2. For a new programmatic workflow, first decide whether Veo-specific controls are required. Use Gemini Omni Flash for general generation; use Veo 3.1 when extension, first/last-frame control, or a legacy Veo integration is required.
  — <https://ai.google.dev/gemini-api/docs/video?authuser=01>
3. In the Gemini API, start an asynchronous generation with the Veo 3.1 preview model appropriate to the job, supply text or an initial image, optionally add up to three reference images, and set aspect ratio, duration, and resolution.
  — <https://ai.google.dev/gemini-api/docs/veo?authuser=01>
4. Poll the returned operation until it is done, then download and retain the result within two days; handle safety or audio processing blocks as a non-output result.
  — <https://ai.google.dev/gemini-api/docs/veo?authuser=01>
5. For Gemini Enterprise Agent Platform, use the GA Standard or Fast IDs in us-central1 with provisioned throughput or fixed quota, after confirming that this access path fits the account and region.
  — <https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate?hl=en>

## Best practices

- Write one clear shot: subject, action, style, then optional camera movement, composition, focus, and ambience. Put exact dialogue in quotes and name sound effects or ambient sound explicitly.
  — <https://ai.google.dev/gemini-api/docs/veo?authuser=01>
- For continuity, use one to three consistent reference images; use first and last frames for a bounded transition, and extend a generated Veo clip rather than asking the model to reason across multiple videos.
  — <https://ai.google.dev/gemini-api/docs/veo?authuser=01>
- Choose Standard for final-shot fidelity, Fast for routine iteration, and Lite for high-volume applications; use the separate upscaler when the task is improving an existing video rather than generating a new shot.
  — <https://cloud.google.com/blog/products/ai-machine-learning/veo-3-1-lite-and-a-new-veo-upscaling-capability-on-vertex-ai/>
- Budget for an asynchronous job taking roughly 11 seconds to six minutes, save the output before its two-day retention window ends, and account for SynthID watermarking and safety filters.
  — <https://ai.google.dev/gemini-api/docs/veo?authuser=01>
- Do not treat Veo 3.1 as the default choice for all new Gemini API video work; reserve it for its control features and select Gemini Omni Flash for general conversational generation and editing.
  — <https://ai.google.dev/gemini-api/docs/video?authuser=01>

## Superseded by this

- 2026-06-30 — Guidance to use Veo 3.1 as the default Gemini API video model is obsolete; Google now names Gemini Omni Flash as the default for general video generation.
- 2026-06-30 — Veo 3.0 and Veo 3.0 Fast endpoint guidance is obsolete after their stated shutdown; integrations must use an applicable Veo 3.1 route instead.
- 2026-04-03 — A two-model choice between Veo 3.1 and Veo 3.1 Fast is incomplete; Lite and a separate upscaling capability are now part of the practical product line.

## Still unknown

- The 2025-10-13 Higgsfield page has no archived evidence here of what it offered then or whether it preceded Google availability.
- The Flowith invitation returned an internal error, so its product access and 2025-10-15 significance are unverified.
- The Hugging Face Space proves only that a community-hosted page named veo3.1-fast was running; it does not identify its underlying provider, authorization, or historical model ID.
- The three dated URLs mix a Google model release with third-party access layers; they do not support treating google-veo and veo-3-1 as separate Google products.
- Google’s Chinese Gemini API guide confirms native audio, while the Chinese Enterprise Agent Platform page currently marks sound generation unsupported for Standard and Fast even though the English Enterprise page marks it supported. Validate the target surface, account, and region before committing to audio-dependent production work.

## Sources

| source | title | read |
|---|---|---|
| https://higgsfield.ai/veo3.1 | Veo 3.1 — AI Video Generation on Higgsfield | 2026-09-04 |
| https://flowith.io/?inv=ST9RZ0NKRMJSEF0Q | Flowith invitation URL — unreadable at observation | 2026-09-04 |
| https://huggingface.co/spaces/akhaliq/veo3.1-fast | veo3.1-fast - a Hugging Face Space by akhaliq | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/veo-updates-flow/ | Introducing Veo 3.1 and advanced capabilities in Flow | 2026-09-04 |
| https://docs.cloud.google.com/vertex-ai/docs/release-notes?authuser=19 | Vertex AI release notes | 2026-09-04 |
| https://blog.google/innovation-and-ai/technology/developers-tools/veo-3-1-gemini-api/ | Enhanced Veo 3.1 capabilities are now available in the Gemini API. | 2026-09-04 |
| https://cloud.google.com/blog/products/ai-machine-learning/veo-3-1-lite-and-a-new-veo-upscaling-capability-on-vertex-ai/ | Introducing Veo 3.1 Lite and a new Veo upscaling capability on Vertex AI | 2026-09-04 |
| https://flow.google/ | Google Flow - AI Creative Studio for Video, Images & Custom Tools | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/video?authuser=01 | Video generation in the Gemini API | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/veo?authuser=01 | Generate videos with Veo 3.1 in Gemini API | 2026-09-04 |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate?hl=en | Veo 3.1 | Gemini Enterprise Agent Platform | Google Cloud Documentation | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/changelog | Release notes | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/veo?hl=zh-CN | 在 Gemini API 中使用 Veo 3.1 生成视频 | 2026-09-04 |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate?hl=zh-cn | Veo 3.1 | Gemini Enterprise Agent Platform | Google Cloud Documentation | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:google-veo`, thread `veo-3-1`, 0 dated events - → -.
- **Practical note:** As of 2025-10-15, treat these third-party Veo 3.1 links as unverified research leads; do not change a production workflow until the product version, provider relationship, and capabilities are independently confirmed.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
