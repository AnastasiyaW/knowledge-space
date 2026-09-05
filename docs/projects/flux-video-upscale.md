---
title: FLUX Video Upscale — Black Forest Labs
category: projects
date: 2026-08-21
tags: [black-forest-labs, flux-video-upscale, project]
aliases: ["FLUX Video Upscale"]
---

# FLUX Video Upscale — Black Forest Labs

**Development line:** `project:flux-video-upscale` · thread `black-forest-labs`  
**Last event:** 2026-08-21 · 1 dated since 2026-08-21 · **Researched:** 2026-09-05 · confidence: high

## What it is

FLUX Video Upscale is a FLUX 3-powered video super-resolution endpoint for API users.

- Regenerates video at 1.5×–3× scale, up to 4K.
- Offers Precise mode for identity-sensitive footage and Creative mode for generated detail.
- Preserves the source audio track.

Inputs are at most 20 seconds, 50 MB, and 2560×1440; output frames cap at about 14.4 MP.

Use Precise for faces, products and brand assets; use Creative for generated scenery and textures where detail matters more than exact identity.

## Development line

- **2026-08-21 — Black Forest Labs introduced FLUX Video Upscale.** On 2026-08-21, Black Forest Labs linked an official blog announcement, product documentation, and a playground model for FLUX Video Upscale. The links confirm the public launch, but do not show detailed capabilities, availability, pricing, or performance.

## What changed

2026-08-21 — FLUX Video Upscale became available as the standalone `POST /v1/flux-tools/video-upscale-v1` tool, following BFL’s August 20 release. The launch added 1.5×–3× video super-resolution, two `creativity` modes, preserved audio, and output-only pricing.

2026-08-26 — BFL’s current tool catalog listed Video Upscale alongside its other editing endpoints, confirming its role as a FLUX Tool with the same asynchronous submit-and-poll workflow.

## How to use this

From 2026-08-21, practitioners should evaluate FLUX Video Upscale through Black Forest Labs’ documented workflow and linked playground rather than treating it as an unannounced or undocumented capability.

1. Prepare an MP4 no longer than 20 seconds and either host it at an accessible HTTPS URL or encode it as base64.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
2. POST `input_video`, an `upscale_factor` from 1.5 to 3, and `creativity` to `/v1/flux-tools/video-upscale-v1`.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
3. Poll the returned `polling_url` until status is `Ready`, then download `result.sample` before its signed URL expires.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>

## Best practices

- Use `creativity: 0` for faces, products, logos and other material whose identity must remain stable.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
- Use `creativity: 1` for generated footage, textures, crowds and scenery; add a short content prompt only when steering invented detail is useful.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
- Upscale the least-compressed source after editing and trimming, so artifacts are not amplified and output-only billing covers only retained footage.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The entry date is 2026-08-21, while BFL’s first-party release note and blog date the launch to 2026-08-20; distribution was likely tracked one day later.
- No independently accessible playground response was available during research, so current browser UI controls and account-tier availability were not verified.

## Sources

| source | title | read |
|---|---|---|
| https://bfl.ai/blog/flux-video-upscale | FLUX Upscale: 2K and 4K for Video | 2026-09-05 |
| https://docs.bfl.ai/flux_tools/flux_video_upscale | FLUX Video Upscale | 2026-09-05 |
| https://docs.bfl.ai/release-notes | Release Notes | 2026-09-05 |
| https://help.bfl.ai/articles/5950329591-what-are-the-flux-tools | What are the FLUX Tools? | 2026-09-05 |
| https://bfl.ai/video-upscaler | FLUX Video Upscale: AI Video Upscaler to 1080p, 2K and 4K | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:flux-video-upscale`, thread `black-forest-labs`, 1 dated events 2026-08-21 → 2026-08-21.
- **Practical note:** From 2026-08-21, practitioners should evaluate FLUX Video Upscale through Black Forest Labs’ documented workflow and linked playground rather than treating it as an unannounced or undocumented capability.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
