---
title: Stable Audio
category: projects
date: 2025-09-12
tags: [model_release, project, stable-audio, stable-audio-releases]
aliases: ["Stable Audio"]
---

# Stable Audio

**Development line:** `project:stable-audio` · thread `stable-audio-releases`  
**Last event:** 2025-09-12 · 2 dated since 2023-09-13 · **Researched:** 2026-09-04 · confidence: high

## What it is

Stable Audio is a web application, API, and model family for text-to-audio, audio-to-audio, inpainting, and audio editing.

- Music: generates tracks and full mixes.
- SFX: creates sound effects and audio clips.
- Samples and variations: creates alternative takes.
- Separate tracks: isolates individual stems.
- Local execution: runs select open-weight models.

Limits depend on the model: Stable Audio 3.0 Medium and Large are rated for more than six minutes. Choose Stable Audio 3.0 and its deployment modes for new work rather than older 1.0 or 2.5 limits.

## Development line

- **2023-09-13 — Stable Audio was introduced.** Text-to-audio in the browser generates audio from text prompts and duration targets.
- **2025-09-12 — Stable Audio 2.5 was introduced for enterprise sound production.** Three-minute tracks, text-to-audio, audio-to-audio, and audio inpainting.

## What changed

- 2023-09-13 — Stable Audio launched as a commercial product with browser text-to-audio from descriptions and set durations.
- 2025-09-12 — Stable Audio 2.5 arrived for enterprise audio production, adding three-minute tracks, text-to-audio, audio-to-audio, and audio inpainting.
- 2026-05-20 — Stable Audio 3.0 launched with open-weight Small SFX, Small, and Medium models alongside API and self-hosted Large models, extending generation length to more than six minutes on Medium and Large.

## How to use this

From 2023-09-13, practitioners could treat Stable Audio as a dedicated audio-generation product; from 2025-09-12, they should evaluate Stable Audio 2.5 and its ComfyUI availability when an enterprise-oriented sound-production workflow is needed.

1. Choose a path: browser Studio for creation and edits, open-weight Small SFX, Small, or Medium for local infrastructure, or API and self-hosted Large for high-volume products.
  — <https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models>
2. Create a session and start with Full Mix, setting genre, instruments, tempo, mood, and target duration in the prompt.
  — <https://stableaudio.com/docs>
3. Use Multi-Track for structured arrangement, and attach references only to guide tempo and key.
  — <https://stableaudio.com/docs>
4. Fix an individual track or time range with regenerate, replace section, or extend, then export the completed mix.
  — <https://stableaudio.com/docs>

## Best practices

- Write specific prompts: genre, instruments, BPM, mood, and era control output better than a broad genre tag.
  — <https://stableaudio.com/docs>
- Start with Full Mix when literal prompt interpretation matters; Multi-Track eases stem mixing, but its arrangement agent can drift from the prompt.
  — <https://stableaudio.com/docs>
- Choose Small SFX or Open Small for short SFX, foley, and production elements; choose Small, Medium, or Large for full music based on length and hosting setup.
  — <https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models>
- Do not upload copyrighted audio into audio-to-audio or inpainting tools: terms require that uploaded material does not infringe copyrights.
  — <https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale>

## Superseded by this

- 2023-09-13 — Limits of the first web product: up to 45 seconds on the free tier and 90 seconds on Pro no longer describe the active lineup; 3.0 Medium and Large generate for more than six minutes.
- 2025-09-10 — Positioning Stable Audio 2.5 as the latest model became obsolete once Stable Audio 3.0 launched on 2026-05-20.

## Still unknown

- Current pricing tiers, credit quotas, and partner integrations change independently of model releases; verify availability directly in your chosen access channel before purchasing or production rollout.

## Sources

| source | title | read |
|---|---|---|
| https://stableaudio.com/ | Stable Audio — Generative AI for music & sound fx | 2026-09-05 |
| https://stableaudio.com/docs | How to use Stable Audio | 2026-09-05 |
| https://stability.ai/news-updates/stable-audio-using-ai-to-generate-music | Announcing Stable Audio, a product for music & sound generation | 2026-09-05 |
| https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale | Stability AI Introduces Stable Audio 2.5, the First Audio Model Built for Enterprise Sound Production at Scale | 2026-09-05 |
| https://stability.ai/news-updates/stable-audio-2-0 | Introducing Stable Audio 2.0 | 2026-09-05 |
| https://stability.ai/news-updates/introducing-stable-audio-open | Introducing Stable Audio Open - An Open Source Model for Audio Samples and Sound Design | 2026-09-05 |
| https://stability.ai/news-updates/stability-ai-and-arm-release-stable-audio-open-small-enabling-real-world-deployment-for-on-device-audio-control | Stability AI and Arm Collaborate to Release Stable Audio Open Small, Enabling Real-World Deployment for On-Device Audio Generation | 2026-09-05 |
| https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models | Meet Stable Audio 3.0, the model family built for artistic experimentation with open-weight models | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:stable-audio`, thread `stable-audio-releases`, 2 dated events 2023-09-13 → 2025-09-12.
- **Practical note:** From 2023-09-13, practitioners could treat Stable Audio as a dedicated audio-generation product; from 2025-09-12, they should evaluate Stable Audio 2.5 and its ComfyUI availability when an enterprise-oriented sound-production workflow is needed.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.