---
title: FLUX 3
category: projects
date: 2026-08-05
tags: [flux-3, flux-3-development, flux_3, project]
aliases: ["FLUX 3"]
---

# FLUX 3

**Development line:** `project:flux-3` · thread `flux-3-development`  
**Last event:** 2026-08-05 · 2 dated since 2026-07-24 · **Researched:** 2026-09-04 · confidence: medium

## What it is

FLUX 3 is a BFL preview video model for creators and API teams who make short audiovisual shots.

- Video generation: text-to-video, image or keyframe-to-video, and video continuation run through the flux-3-video endpoint.
- Output specification: 24 fps video with synchronized speech, sound effects, and ambience.

## Development line

- **2026-07-24 — Black Forest Labs published a FLUX 3 blog update.** FLUX 3 entered Early Access as a unified multimodal model. Black Forest Labs staged Video, Image, Action, and Dev access separately.
- **2026-08-05 — FLUX 3 was linked across Black Forest Labs product surfaces.** The model and Quick Start pages carry no dates. The linked Playground route returns an error.

## What changed

2026-07-24 — The cited launch material is dated 2026-07-23: FLUX 3 entered Early Access as a unified multimodal model, while Video, Image, Action, and Dev access were staged separately. 2026-08-04 — BFL made an initial FLUX 3 Video generally available through its API and selected partners. 2026-08-05 — We can verify no separate capability release: the model and Quick Start pages are undated, and the associated Playground route now returns an error. 2026-08-20 — FLUX Upscale launched as a separate endpoint that can regenerate video up to native 4K.

## How to use this

Consult the FLUX 3 model page, quick-start documentation, and prompt-to-image playground from 2026-08-05 before testing FLUX 3, so features and access stay verified against primary sources.

1. Create a BFL account, add credits, then use the Playground or the API.
  — <https://docs.bfl.ai/flux_3>
2. For a new clip, POST mode=t2v, a prompt, and optional duration to the /v1/flux-3-video endpoint with your BFL API key.
  — <https://docs.bfl.ai/flux_3>
3. For image-led video use mode=i2v with keyframes; for an extension use mode=v2v with start_video.
  — <https://docs.bfl.ai/flux_3>
4. Poll the returned polling_url until the job is Ready, then download the result before its signed URL expires.
  — <https://docs.bfl.ai/flux_3>
5. Prototype with draft=true; send the selected result's draft_cache in mode=draft_enhance to render that same shot at full quality.
  — <https://docs.bfl.ai/flux_3>

## Best practices

- Use draft and draft_enhance after approving a preview, because a fresh full render can reinterpret the shot.
  — <https://docs.bfl.ai/flux_3>
- Pin keyframes to exact timestamps when a transition must be controlled; i2v accepts one to ten images, including start and end pins.
  — <https://docs.bfl.ai/flux_3>
- Download a Ready result promptly, because its signed URL expires after about two hours.
  — <https://docs.bfl.ai/flux_3>
- Use Upscale Precise mode when identity or reference detail must stay consistent, because Creative can change or replace identity.
  — <https://bfl.ai/blog/flux-video-upscale>

## Superseded by this

- 2026-08-04: “FLUX 3 Video is available only through Early Access” is obsolete; BFL made an initial version generally available through its API and selected partners.

## Still unknown

- The 2026-08-05 Playground URL currently returns an internal error, so we cannot verify its original model, prompt, and output.
- The 2026-08-05 source bundle mixes a prompt-to-image Playground route with current BFL documentation that exposes FLUX 3 as video; without the original source text, we do not know whether this is the same FLUX 3 product or a generic dashboard link.
- The first-party public sources checked do not establish a release date or public endpoint for FLUX 3 Image, FLUX 3 Dev, or FLUX 3 Action after their staged launch plans.

## Sources

| source | title | read |
|---|---|---|
| https://bfl.ai/blog/flux-3 | FLUX 3 - Real World Models: Towards Multimodal Flow Models as the Backbone of Visual Intelligence. | 2026-09-04 |
| https://bfl.ai/blog/flux-3-video | FLUX 3 Video, Part 1: Generation | 2026-09-04 |
| https://bfl.ai/blog/flux-video-upscale | FLUX Upscale: 2K and 4K for Video | 2026-09-04 |
| https://docs.bfl.ai/flux_3 | FLUX 3 - Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/quick_start/introduction | The frontier of visual intelligence - Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/7655484417-what-flux-models-are-available | What FLUX models are available? | Black Forest Labs Knowledge Base | 2026-09-04 |
| https://bfl.ai/models/flux-3 | FLUX 3: One Multimodal Model | Black Forest Labs | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:flux-3`, thread `flux-3-development`, 2 dated events 2026-07-24 → 2026-08-05.
- **Practical note:** Consult the FLUX 3 model page, quick-start documentation, and prompt-to-image playground from 2026-08-05 before testing FLUX 3, so capabilities and eligibility stay confirmed against primary sources.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
