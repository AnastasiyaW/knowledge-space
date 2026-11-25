---
title: MiniMax Music
category: projects
date: 2025-10-31
tags: [minimax-music, minimax-music-development, model_releases, project]
aliases: ["MiniMax Music", "MiniMax Music 2.0"]
---

# MiniMax Music

**Development line:** `project:minimax-music` · thread `minimax-music-development`  
**Last event:** 2025-10-31 · 1 dated since 2025-10-31 · **Researched:** 2026-09-04 · confidence: medium

## What it is

MiniMax Music produces complete songs from lyrics and a style brief for creators and developer teams.

- Vocal songs from text prompts and lyrics.
- Instrumental music without vocal parts.
- Reference-audio covers from existing audio files.
- Local serving via open weights for Music 3.

New paid Music and Lyrics API access stopped on 2026-08-20, and local Music 3 requires CUDA with 24 GB+ VRAM on the full Diffusers path. Start on MiniMax Audio or self-host Music 3 if you are new; keep the API path only if you are an existing paying customer.

## Development line

- **2025-10-31 — MiniMax Music generation became available through documented model endpoints.** MiniMax launched an official product page and API reference for music generation on 2025-10-31. A hosted fal.ai model endpoint provided another developer-facing access path on the same date.

## What changed

- 2025-10-31 — MiniMax Music 2.0 launched with more natural vocals, multi-vocal/a-cappella examples, instrument control, and songs up to five minutes.
- 2026-01-28 — MiniMax Music 2.5 added paragraph-level section control, 14 structural variations, 100+ instruments, and updated mixing.
- 2026-02-09 — No independently retrievable source body establishes a separate MiniMax Music release or capability change for this date.
- 2026-03-04 — MiniMax Music 2.5+ added instrumental-only generation, expanding the line beyond vocal song creation.
- 2026-03-18 — Music-2.6 appeared in official model release notes as a music/cover update; current docs call it the previous-generation text-to-music model.
- 2026-08-13 — MiniMax Music 3.0 became the next-generation open-weights release for complete songs up to five minutes.
- 2026-08-20 — New paid Music and Lyrics API users were cut off and free music-generation APIs were discontinued; existing paying users retained access.

## How to use this

Before selecting an integration route from 2025-10-31, check the official music-generation API documentation and supported hosted-model endpoints.

1. Choose the access route first: as a new user, use MiniMax Audio or self-host Music 3; new paid Music/Lyrics API access is closed and free endpoints are discontinued. Existing paying API users can continue.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
2. As an existing paid API user, send JSON with Bearer authentication to POST /v1/music_generation and select music-3.0, marked as recommended in the reference.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
3. Describe genre, mood, and scenario in prompt; pass sectioned lyrics in lyrics, or set lyrics_optimizer=true when lyrics are absent. Set is_instrumental=true for a no-vocal track.  
  — <https://platform.minimax.io/docs/guides/music-generation>
4. For a cover, select music-cover and provide exactly one reference-audio URL or base64 payload; the accepted reference is 6 seconds to 6 minutes and at most 50 MB.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
5. For local Music 3, download MiniMaxAI/MiniMax-Music3 and serve it with SGLang-Omni. Put lyrics in input and the music description in instructions; Diffusers and ComfyUI are also supported.  
  — <https://huggingface.co/MiniMaxAI/MiniMax-Music3>

## Best practices

- Keep music direction in prompt and lyric text in lyrics. Use documented section tags to control arrangement instead of mixing directions into the lyric body.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
- When you do not supply lyrics, set lyrics_optimizer; when you want no vocals, explicitly set is_instrumental and omit lyrics.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
- Download a URL-format result within 24 hours, or use hex output when streaming, because streaming supports only hex.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
- For local Music 3, describe global metadata, vocal details, and arrangement thoroughly. Put lyric tags on their own lines, and treat requested tempo, key, instrumentation, and structure as generative controls rather than guarantees.  
  — <https://huggingface.co/MiniMaxAI/MiniMax-Music3>
- Check local capacity before loading Music 3: CUDA is required; the documented direct Diffusers path fits 24 GB+ VRAM, while CPU/layer offloading fits 8 GB but is slower.  
  — <https://huggingface.co/MiniMaxAI/MiniMax-Music3>

## Superseded by this

- 2026-08-13 — MiniMax Music 2.0 as the current default MiniMax music model.
- 2026-03-04 — Guidance that MiniMax Music always requires vocals and supplied lyrics.
- 2026-08-13 — Music-2.6 as the recommended text-to-music API model.
- 2026-08-20 — Guidance for new users to enroll in the paid Music API or use Music-3.0-free, Music-2.6-free, or music-cover-free.

## Still unknown

- The 2026-02-09 source set does not establish a distinct MiniMax Music release: the WeChat page could not be retrieved and the X page exposed no post body, so it cannot safely be equated with Music 2.5 or another version.
- The API reference retains model examples and free-model names beside the 2026-08-20 closure notice; existing-customer continuation is stated, but fresh registration and entitlement paths were not independently tested.
- Current MiniMax Audio pricing, regional availability, commercial licensing, and web-product quotas were not verified. Fal's $0.03 figure applies only to its own v2 endpoint.
- The Music3 card says no Hugging Face Inference Provider hosts the model; a managed hosted-inference route beyond MiniMax Audio was not verified.

## Sources

| source | title | read |
|---|---|---|
| https://www.minimax.io/audio/music | MiniMax Audio | AI Music Generator | 2026-09-04 |
| https://www.minimax.io/news/minimax-music-20 | Making Music Creation Accessible to Everyone - MiniMax News | MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/music-generation | Music Generation - MiniMax API Docs | 2026-09-04 |
| https://fal.ai/models/fal-ai/minimax-music/v2 | MiniMax Music 2.0: State of the Art AI Text-to-Music Generator | fal | 2026-09-04 |
| https://mp-weixin-qq-com.translate.goog/s/hy1RzvAytRSxX63qodEExw?_x_tr_sl=zh-CN&_x_tr_tl=en&_x_tr_hl=en | WeChat article via Google Translate (title unavailable) | 2026-09-04 |
| https://x.com/wavespeed_ai/status/2020165909646586220?s=20 | WaveSpeed AI X post 2020165909646586220 (body unavailable) | 2026-09-04 |
| https://www.minimax.io/news/minimax-music-25 | MiniMax Music 2.5: Breakthrough Across All Dimensions — Direct the Detail. Define the Real - MiniMax News | MiniMax | 2026-09-04 |
| https://www.minimax.io/news/minimax-music-25-2 | MiniMax Music 2.5+: Unlock instrumental music, break through style boundaries. - MiniMax News | MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/release-notes/models | Models - MiniMax API Docs | 2026-09-04 |
| https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model | MiniMax Music 3.0: Next-Generation Open-Weights, Production-Ready & Versatile Music Model - MiniMax Research | MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/guides/music-generation | Music Generation - MiniMax API Docs | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-Music3 | MiniMaxAI/MiniMax-Music3 · Hugging Face | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:minimax-music`, thread `minimax-music-development`, 1 dated events 2025-10-31 → 2025-10-31.
- **Practical note:** Check official MiniMax API docs and hosted endpoints before picking an integration path from 2025-10-31.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.