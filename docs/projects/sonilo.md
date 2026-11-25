---
title: Sonilo
category: projects
date: 2026-06-29
tags: [project, sonilo, sonilo-v1-1]
aliases: ["Sonilo"]
---

# Sonilo

**Development line:** `project:sonilo` · thread `sonilo-v1-1`  
**Last event:** 2026-06-29 · 1 dated since 2026-06-29 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Sonilo is an API-first audio tool for editors, creative-product teams, and developers who need music or sound tied to a cut.

- generates music from text or video;
- generates text- and video-led sound effects;
- mixes supplied voice and music with automatic ducking.

## Development line

- **2026-06-29 — Sonilo v1.1 linked to a text-to-music endpoint.** It delivers tighter video-to-music alignment, preserves original speech, and adds per-segment prompts. The first-party release itself is dated 2026-06-18.

## What changed

2026-06-29 — Sonilo v1.1 delivers tighter video-to-music alignment, preserves original speech, and adds per-segment prompts. The first-party release itself is dated 2026-06-18.

## How to use this

From 2026-06-29, we treat Sonilo v1.1 as a distinct candidate endpoint to evaluate through the linked text-to-music route and Sonilo platform, without assuming capabilities or migration requirements until the source pages are researched.

1. Create an API key, keep it server-side, and add the required API balance before attempting generation.
  — <https://platform.sonilo.com/docs/quickstart>
2. Preflight the account’s enabled services and usage, then select text-to-music for a musical brief or video-to-music for a locked visual timeline.
  — <https://platform.sonilo.com/docs/api>
3. For direct text generation, POST a prompt and a 5–360 second duration to /v1/text-to-music.
  — <https://platform.sonilo.com/docs/text-to-music>
4. Consume streamed audio chunks only through the complete event, or use async mode and poll the returned task ID to a terminal state.
  — <https://platform.sonilo.com/docs/text-to-music>
5. If the product already uses fal, call the v1.1 text model at sonilo/v1.1/text-to-music rather than building a separate provider integration.
  — <https://fal.ai/models/sonilo/v1.1/text-to-music>

## Best practices

- Keep API keys in a server-side environment variable. Revoke and replace an exposed key rather than embedding it in a client app.
  — <https://platform.sonilo.com/docs>
- Treat 401, 402, 403, and 429 as distinct setup, balance, service-access, and backoff conditions. Do not create placeholder audio after a failed request.
  — <https://platform.sonilo.com/docs/text-to-music>
- Use video input when timing, cuts, or voice space must guide the soundtrack. Use text input when the task is a standalone cue.
  — <https://platform.sonilo.com/docs/api>
- For paid or client work, review the generated track against voice-over and scene changes, retain the output and account record, and confirm that the current plan covers the intended release.
  — <https://sonilo.com/blog/ai-music-video-creators-2026>

## Superseded by this

- 2026-06-18 — For video scoring that requires preserved dialogue or scene-specific direction, v1.1 supersedes v1.0-style generation without those controls. The release does not state that v1.0 endpoints were retired.
- 2026-08-03 — Where a project already has separate voice and music assets, the documented audio-ducking endpoint supersedes manual volume riding when its two-input workflow fits.

## Still unknown

- The supplied event is dated 2026-06-29, while Sonilo’s release page dates v1.1 to 2026-06-18; no primary source found explains the eleven-day difference.
- The v1.1 comparison figures are vendor-reported and no public evaluation protocol or independent replication was found.
- The direct Sonilo text endpoint documents a 360-second ceiling, while the fal v1.1 text endpoint documents 600 seconds; treat limits as route-specific until confirmed for the intended account.
- No public primary source found in this pass declares a successor model after v1.1.

## Sources

| source | title | read |
|---|---|---|
| https://sonilo.com/news/sonilo-v1-1 | Introducing Sonilo v1.1 | Sonilo | 2026-09-05 |
| https://fal.ai/models/sonilo/v1.1/text-to-music | Sonilo V1.1 Text to Music (Text to Audio) API on fal | 2026-09-05 |
| https://platform.sonilo.com/ | Sonilo API — Enterprise AI Music API | 2026-09-05 |
| https://platform.sonilo.com/docs | Introduction · Sonilo Docs | 2026-09-05 |
| https://platform.sonilo.com/docs/quickstart | Quickstart · Sonilo Docs | 2026-09-05 |
| https://platform.sonilo.com/docs/text-to-music | Text to Music · Sonilo Docs | 2026-09-05 |
| https://platform.sonilo.com/docs/api | API reference | 2026-09-05 |
| https://sonilo.com/zh-CN/news/sonilo-v1 | 介绍 Sonilo v1.0 | Sonilo | 2026-09-05 |
| https://sonilo.com/blog/sonilo-comfyui | Exciting News: Sonilo is Now Live on ComfyUI! | Sonilo | 2026-09-05 |
| https://sonilo.com/blog/product/audio-ducking-api-guide | Audio Ducking API: Automatically Mix Voice and Music | Sonilo | 2026-09-05 |
| https://sonilo.com/blog/ai-music-video-creators-2026 | Licensed AI Music for YouTube, Ads, and Client Videos (2026 Guide) | Sonilo | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:sonilo`, thread `sonilo-v1-1`, 1 dated events 2026-06-29 → 2026-06-29.
- **Practical note:** From 2026-06-29, we treat Sonilo v1.1 as a distinct candidate endpoint to evaluate through the linked text-to-music route and Sonilo platform, without assuming capabilities or migration requirements until the source pages are researched.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
