---
title: Perceptron Mk1 — Initial public release
category: projects
date: 2026-05-14
tags: [initial-public-release, perceptron-mk1, perceptron_mk1, project]
aliases: ["Perceptron Mk1"]
---

# Perceptron Mk1 — Initial public release

**Development line:** `project:perceptron-mk1` · thread `initial-public-release`  
**Last event:** 2026-05-14 · 1 dated since 2026-05-14 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Perceptron Mk1 is a closed vision-language model for teams adding image and video analysis to APIs, not a video generator.

- Multimodal input: accepts text, images, and video.
- Structured output: returns text with spatial or temporal annotations.
- Visual tasks: handles Q&A, OCR, object detection, captioning, video-event clipping, and in-context visual examples.
- Configuration: sets `vision_config` for reasoning and typed grounding.

## Development line

- **2026-05-14 — Perceptron Mk1 public introduction.** On 2026-05-14, Perceptron Mk1 appeared on a public introduction page. The post links to a demo, documentation, and an OpenRouter model page, marking a material public development milestone. Those links alone do not establish model capabilities, technical design, or access terms.

## What changed

2026-05-14 — Perceptron published the Mk1 announcement; official release history dates the actual launch to 2026-05-12, adding image/video input, 32K context, reasoning, model specifications, and video guides. 2026-06-09 — A dedicated `/v1/detect` endpoint added direct grounded detection from categories, exemplars, or exhaustive requests. 2026-06-15 — A Files API added reusable uploaded image and video references across requests. 2026-06-22 — Chat completions gained timestamped inline `video_frames` as an alternative to a video URL.

## How to use this

As of 2026-05-14, start with the public documentation and demo, then verify current OpenRouter availability and terms before adoption.

1. Open the demo, sign in if prompted, and test a concrete prompt on a sample asset before integrating.
  — <https://www.perceptron.inc/demo>
2. Create a Perceptron API key, select `perceptron-mk1`, and use the Python SDK, cURL, or an OpenAI-compatible client.
  — <https://docs.perceptron.inc/>
3. Send text plus a JPEG, PNG, WebP, MP4, or WebM asset to the chat-completions API.
  — <https://docs.perceptron.inc/>
4. Choose the result contract upfront: enable thinking for reasoning tasks, or request `point`, `box`, `polygon`, or `clip` annotations for grounded output.
  — <https://docs.perceptron.inc/perceptron-mk1/models/perceptron-mk1>
5. For assets reused across requests, upload them once and reference the file ID; each file is capped at 128 MiB.
  — <https://docs.perceptron.inc/perceptron-mk1/guides/files>
6. As a routed alternative, select `perceptron/perceptron-mk1` through OpenRouter and check the current model card before deployment.
  — <https://openrouter.ai/perceptron/perceptron-mk1>

## Best practices

- Use observable prompts and typed output requests: named classes for detection and an exact event predicate for clipping.
  — <https://docs.perceptron.inc/perceptron-mk1/best-practices/prompting-reference>
- Enable thinking for text Q&A, OCR, captioning, and clips; leave it off for point, box, and polygon localization.
  — <https://docs.perceptron.inc/perceptron-mk1/models/perceptron-mk1>
- For video clips, ask for the exact moment or range; treat a returned single timestamp as an approximate instant rather than a zero-length interval.
  — <https://docs.perceptron.inc/perceptron-mk1/capabilities/video-clipping>
- Keep interactive timeouts and `max_tokens` tight; resize media client-side and honor `Retry-After` with jitter after a 429.
  — <https://docs.perceptron.inc/perceptron-mk1/guides/scaling>
- Store keys in environment variables or a secret manager, strip PII from persisted prompts and logs, and protect annotated examples as proprietary imagery.
  — <https://docs.perceptron.inc/perceptron-mk1/best-practices/security>

## Superseded by this

- 2026-06-22 — None documented: the public changelog describes the June capabilities as additions without deprecating Mk1, chat completions, or `video_url` input.

## Still unknown

- The supplied launch article at `https://www.perceptron.inc/blog/introducing-perceptron-mk1` returned 403 during this check, so its text and publication timestamp were not used as primary proof.
- The 2026-05-14 date may reflect when the post appeared rather than the actual product launch; unavailable private text prevents confirmation.
- No later Mk1 model revision appears in the public changelog after 2026-06-22, though undocumented service changes remain possible.
- First-party documentation says 32K context while OpenRouter displays 33K; OpenRouter also specifies 32,768 tokens, so this looks like rounding rather than a material conflict.
- No first-party Simplified-Chinese release was found. The cited Chinese roundup corroborates launch claims without independently validating vendor performance claims.

## Sources

| source | title | read |
|---|---|---|
| https://www.perceptron.inc/demo | Perceptron demo | 2026-09-06 |
| https://docs.perceptron.inc/ | Quickstart - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/models/perceptron-mk1 | Perceptron Mk1 - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/changelog | Changelog - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/best-practices/prompting-reference | Prompting reference - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/capabilities/video-clipping | Video Clipping - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/guides/files | Files - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/guides/scaling | Scaling guide - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/best-practices/security | Security - Perceptron Docs | 2026-09-06 |
| https://openrouter.ai/perceptron/perceptron-mk1 | Perceptron Mk1 - API Pricing & Providers | OpenRouter | 2026-09-06 |
| https://b.coolplus.me/archives/ai--2026-05-13 | AI 新闻摘要 2026-05-13 - 酷加的博客 | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:perceptron-mk1`, thread `initial-public-release`, 1 dated events 2026-05-14 → 2026-05-14.
- **Practical note:** As of 2026-05-14, test the public documentation and demo first, then verify current OpenRouter availability and terms before adoption.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
