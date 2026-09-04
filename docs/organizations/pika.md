---
title: Pika — Pika product and platform development
category: organizations
tags: [organization, pika, pika-product-and-platform-development, pikaswaps]
aliases: ["Pika"]
---

# Pika — Pika product and platform development

**Development line:** `organization:pika` · thread `pika-product-and-platform-development`  
**Events:** 3 dated, 2025-02-20 → 2026-08-17 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Pika — separate products for editing short AI video, integrating generative media, and trying persistent creative agents. - PikaSwaps edits an existing video by replacing subjects or objects while retaining the scene. - Pika API Club exposes Pika and third-party image, video, and audio models through one API. - Pika Agents are persistent multimodal agents with skills and integrations, separate from Pika Video accounts. Limit: the PikaSwaps API supports 720p or 1080p output at 5 or 10 seconds and is not intended for pixel-perfect compositing; Pika Agents are explicitly experimental. Verdict: choose the product surface first—Pika is a company name, not one interchangeable tool or account.

## Development line

- **2025-02-20 — Pika introduced PikaSwaps.** On 2025-02-20, Pika published a dedicated PikaSwaps product page. This indicates PikaSwaps was presented as a distinct named product capability in Pika's development history. The supplied link alone does not establish its detailed functionality or rollout terms.
- **2025-08-12 — Pika made its Social AI Video app available on iOS.** On 2025-08-12, Pika was represented by an App Store listing for “Pika: Social AI Video.” The listing documents an iOS distribution channel for Pika's social AI video product. The dated link alone does not establish the app's exact launch scope, version, or feature set.
- **2026-08-17 — Pika published its Pika Audio model family and Pika Music playground.** On 2026-08-17, Pika published official pages for its Pika Audio models, developer API documentation, and a Pika Music playground. These links show that Pika extended its public product surface with audio-model and music-generation access. The supplied links alone do not establish model specifications, pricing, or availability terms.

## What changed

Pika — its current product line spans video editing, social video, agent workflows, and audio APIs. 2025-02-20 — PikaSwaps: Pika acquired a source-video editing workflow for changing a subject or object with a source video and text direction; current documentation adds optional replacement-image and ROI-or-mask controls. The historic public URL now redirects to sign-in, so its original release wording is unavailable. 2025-08-12 — Pika Social iOS: the mobile product centers on turning selfies into videos, GIFs, and memes, remixing styles, sounds, and lip-sync templates, then sharing them in a feed. Its current App Store name is AI Video Trend by Pika. 2026-02-21 — Pika.me: the current destination is Pika Agents, a persistent multimodal agent product with a separate account model from Pika Video, skills, integrations, an API, and MCP support. 2026-08-17 — Pika Audio: the linked first-party overview is dated 2026-08-14 and adds Soundtrack, Music, SFX, and Speech to the Pika API Club. Found today (2026-09-04) — Pika API Club is a single API catalogue for Pika models and other providers' media models; PikaSwaps and Pika Music are available through browser playgrounds and asynchronous job APIs.

## How to use this

From 2025-08-12, practitioners should evaluate Pika for mobile social AI-video workflows as well as web use. From 2026-08-17, they should consult Pika's audio-model API documentation and Pika Music playground when assessing audio or music-generation workflows, rather than treating Pika as a video-only tool.

1. Choose PikaSwaps when the task is to alter an existing clip rather than generate a new one; use its Playground or API reference to define the object or subject to change.
  — <https://dev.pika.art/models/pika/pikaswaps/video-to-video>
2. Provide a source video by public URL or Pika upload, write the edit prompt, then provide either a free-text region of interest or a mask; add a replacement reference image only when needed. Select 720p or 1080p and 5 or 10 seconds.
  — <https://dev.pika.art/models/pika/pikaswaps/video-to-video>
3. Submit the asynchronous PikaSwaps job, retain its ID, poll until it is completed or failed, and then retrieve the output URL.
  — <https://dev.pika.art/models/pika/pikaswaps/video-to-video>
4. For music, open Pika Music in the Playground; supply the required prompt and add lyrics, reference audio, source audio, or a voice sample only for the chosen workflow.
  — <https://dev.pika.art/models/pika/pika-audio/pika-music/playground>
5. For Pika Agents, create a separate account from Pika Video, then connect only the needed services through the Skills and Integrations controls.
  — <https://www.pika.me/>

## Best practices

- PikaSwaps is for short creative edits, not frame-exact rotoscoping, feature-length renders, pixel-perfect compositing, or precise on-screen text.
  — <https://dev.pika.art/models/pika/pikaswaps/video-to-video>
- Use a region of interest or a mask to constrain the replacement, and use a reference image when the replacement identity matters.
  — <https://dev.pika.art/models/pika/pikaswaps/video-to-video>
- Keep Pika API keys on the server, persist the returned job ID, and handle queued, completed, and failed states instead of treating submission as a finished result.
  — <https://dev.pika.art/models/pika/pika-audio/pika-music>
- Clone only voices for which you hold the rights; Pika Speech explicitly excludes voices you lack rights to clone.
  — <https://dev.pika.art/models/pika/pika-audio/pika-speech>
- Treat Pika Agent integrations as experimental and review their behaviour on connected platforms; Pika states that the user remains responsible for agent activity.
  — <https://www.pika.me/>

## Superseded by this

- 2025-02-20: the PikaSwaps landing URL is no longer usable as standalone operational guidance because it redirects to sign-in; use the current API or Playground reference.
- 2025-08-12: Pika Social is not the current App Store title for this listing; it now reads AI Video Trend by Pika.
- 2026-02-21: guidance to reuse a Pika Video account for Pika Agents is obsolete; Pika Agents states that an existing Pika account does not work and a new account is required.
- Before 2026-08-14: video-only Pika API guidance is incomplete for developers because Pika Audio now includes Soundtrack, Music, SFX, and Speech.

## Still unknown

- The dated links alone do not show whether every dated record was a launch, an update, or a re-share; this limits interpretation of the two 2025 entries.
- The original PikaSwaps public page now redirects to sign-in, so its February 2025 release copy and version cannot be independently reconstructed.
- Pika Video/PikaSwaps, the Pika Social iOS listing, Pika API Club, and Pika Agents are distinct product lines under the Pika name. Pika Agents explicitly require a separate account, so their histories and instructions should not be treated as one workflow.
- No first-party Simplified-Chinese guidance was found in the scoped search.

## Sources

| source | title | read |
|---|---|---|
| https://pika.art/pikaswaps | PikaSwaps (redirects to Pika sign-in) | 2026-09-04 |
| https://dev.pika.art/models/pika/pikaswaps/video-to-video | Pikaswaps | Pika API | 2026-09-04 |
| https://apps.apple.com/us/app/pika-social-ai-video/id6744712684 | AI Video Trend by Pika App - App Store | 2026-09-04 |
| https://www.pika.me/ | Pika – Create Your Pika Agent | AI Agent Platform | 2026-09-04 |
| https://experiment.pika.art/blog/pika-audio-models | Everything You Want to Hear | Pika Blog | 2026-09-04 |
| https://dev.pika.art/ | Pika API | 2026-09-04 |
| https://dev.pika.art/models/pika/pika-audio/pika-music | Pika Music | Pika API | 2026-09-04 |
| https://dev.pika.art/models/pika/pika-audio/pika-music/playground | Pika Music Playground | Pika API | 2026-09-04 |
| https://dev.pika.art/models/pika/pika-audio/pika-speech | Pika Speech | Pika API | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:pika`, thread `pika-product-and-platform-development`, 3 dated events 2025-02-20 → 2026-08-17.
- **Practical note:** From 2025-08-12, practitioners should evaluate Pika for mobile social AI-video workflows as well as web use. From 2026-08-17, they should consult Pika's audio-model API documentation and Pika Music playground when assessing audio or music-generation workflows, rather than treating Pika as a video-only tool.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
