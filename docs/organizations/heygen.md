---
title: HeyGen
category: organizations
date: 2025-05-07
tags: [avatar-platform-and-developer-integration, heygen, heygen_avatars, heygen_video_translate, organization]
aliases: ["HeyGen"]
---

# HeyGen

**Development line:** `organization:heygen` · thread `avatar-platform-and-developer-integration`  
**Last event:** 2025-05-07 · 2 dated since 2024-07-12 · **Researched:** 2026-09-04 · confidence: medium

## What it is

HeyGen is a video platform for teams and developers making avatar, translated, and prompt-driven video.

- AI Studio: edits script, avatar, voice, scenes, timing, and assets.
- Digital Twins and Photo Avatars: generate video from footage or still images.
- Video Translation and Video Agent: translate footage and build videos via API, CLI, or MCP.

## Development line

- **2024-07-12 — HeyGen shared an Expressive Photo Avatar capability.** On 2024-07-12, a HeyGen Labs URL pointed to Expressive Photo Avatar. The page marks a new avatar surface. The link alone does not confirm release status, availability, or behavior.
- **2025-05-07 — HeyGen shared MCP server developer materials.** On 2025-05-07, links pointed to HeyGen avatars, MCP server documentation, and the heygen-com/heygen-mcp repository. This added a developer MCP integration to the avatar platform. The pages do not show feature coverage, version, or readiness.

## What changed

The product moved from avatar and template entry points toward Studio, translation, avatar engines, and developer access.

- 2023-08-10 — links pointed to the homepage and a Typeform destination. The form returned no usable content, so its launch or program remains unknown.
- 2023-09-08 — a video-translation entry linked a guest-template route. The route no longer renders, showing a translation direction rather than a capability release.
- 2024-03-25 — an entry linked the application home without a recoverable named feature.
- 2024-07-12 — HeyGen Labs exposed an Expressive Photo Avatar route. The page yields no content, so experiment status and limits remain unverified.
- 2024-12-13 — no usable public source survives, so we make no claim.
- 2025-05-07 — an MCP documentation route and GitHub repository joined the avatars page. This was the first agent integration marker.
- 2026-04-13, found today — HeyGen announced developer tools for Video Agent, video generation, translation, and lipsync APIs.
- 2026-04-15, found today — HeyGen introduced Avatar V, separating video-based Avatar V from photo-based workflows.
- 2026-04-28, found today — HyperFrames announced an open-source HTML, CSS, and JavaScript video framework for AI agents.
- 2026-09-04, found today — Remote MCP now uses OAuth with an existing HeyGen plan, and direct API access remains open.

## How to use this

Since 2025-05-07, evaluate the MCP server documentation and repository alongside the browser app so you do not assume browser-only workflows. Test capability and readiness separately before production.

1. For a still-image presenter, open Avatars, choose New Avatar, then Upload Photo or Design with AI; name it and wait for validation before using it in Studio.
  — <https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars>
2. For a repeatable personal presenter, use Avatars → Create New Avatar → Digital Twin, record or upload footage, then have the depicted person complete the consent video.
  — <https://help.heygen.com/en/articles/12089286-create-your-first-digital-twin-video-avatar-with-avatar-iv>
3. In AI Studio, choose the avatar and voice, write script scenes, preview the voice, adjust pauses and timing, then submit the final video for generation.
  — <https://help.heygen.com/en/articles/11049837-create-your-first-video-in-our-studio>
4. For localization, import an MP4, MOV, WEBM, supported YouTube URL, Google Drive URL, or existing project; select source and target languages, choose the translation engine, submit, then review the output.
  — <https://help.heygen.com/en/articles/10029081-how-to-get-started-with-video-translation>
5. For automation, detect an authenticated MCP, CLI, or API path first; use Video Agent for ordinary prompt-to-video work and a callback URL for production jobs.
  — <https://developers.heygen.com/docs/for-ai-agents>

## Best practices

- Record Digital Twin footage in one continuous, stable take with good light, visible face, and clean audio; avoid cuts, wide head turns, busy clothing, and camera drift.
  — <https://help.heygen.com/en/articles/8389138-digital-twin-video-avatar-filming-tips>
- Use a clear, front-facing Photo Avatar image with visible eyes and lips; create it as an avatar, not as a Studio asset.
  — <https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars>
- Preview voice and individual scenes before full rendering so you do not waste credits on re-renders.
  — <https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits>
- Pick the avatar path deliberately: Avatar V handles video looks, while Avatar IV handles photo looks. Fix input footage instead of correcting a bad render.
  — <https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits>
- Feed translation a single-language source, select the intended language variant, and verify with script proofing or SRT guidance. Recreate videos in Studio when on-screen text must change.
  — <https://help.heygen.com/en/articles/10029081-how-to-get-started-with-video-translation>
- For agent integrations, verify authentication before building, stick to one route among MCP, CLI, or API, and use callbacks instead of indefinite polling in production.
  — <https://developers.heygen.com/docs/for-ai-agents>

## Superseded by this

- 2023-09-08 — do not rely on the historical guest-template URL as a current workflow; it did not render when checked, while current Studio and Video Translation flows are documented.
- 2024-07-12 — the Labs Expressive Photo Avatar route is not a current operating reference; use Avatars → New Avatar → Upload Photo or Design with AI, then Studio.
- 2025-05-07 — treat the legacy docs.heygen.com MCP route and heygen-com/heygen-mcp repository as historical pointers rather than setup instructions; current Remote MCP uses OAuth, and the agent guide selects MCP, CLI, or API after authentication.
- Before 2026-04-15 — generic avatar-engine guidance is incomplete now: current documentation distinguishes Avatar V for video-based looks from Avatar IV for photo-based workflows.

## Still unknown

- The 2023 Typeform and guest-template destinations, the 2024 Labs destination, and the legacy 2025 MCP endpoints no longer exposed usable content in this check; their original feature scope and launch status remain unverified.
- The 2024-12-13 entry has no preserved public URL, so no product-change claim can be made for that date.
- HeyGen is a company-level subject, while avatars, translation, Video Agent, and HyperFrames are distinct product lines. The generic HeyGen label is therefore not a reliable single-product history.
- The current Remote MCP material does not state when or how the 2025 legacy MCP documentation and repository were migrated.

## Sources

| source | title | read |
|---|---|---|
| https://www.heygen.com/ | HeyGen: Create Realistic AI Videos of Yourself in Minutes | 2026-09-04 |
| https://www.heygen.com/model-context-protocol | Contextual AI Integration | AI Video Solutions | HeyGen | 2026-09-04 |
| https://developers.heygen.com/docs/for-ai-agents | For AI Agents - HeyGen Documentation | 2026-09-04 |
| https://help.heygen.com/en/articles/11049837-create-your-first-video-in-our-studio | Create your first video in our Studio! | HeyGen Help Center | 2026-09-04 |
| https://help.heygen.com/en/articles/12089286-create-your-first-digital-twin-video-avatar-with-avatar-iv | Create your first Digital Twin (Video Avatar) with Avatar IV! | HeyGen Help Center | 2026-09-04 |
| https://help.heygen.com/en/articles/12092609-recording-your-consent-video | Recording your Consent Video | HeyGen Help Center | 2026-09-04 |
| https://help.heygen.com/en/articles/8389138-digital-twin-video-avatar-filming-tips | Digital Twin (Video Avatar): Filming Tips | HeyGen Help Center | 2026-09-04 |
| https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars | How to Get Started with Photo Avatars | HeyGen Help Center | 2026-09-04 |
| https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits | Avatar & Voice FAQ: Troubleshooting, Best Practices, and Credits | HeyGen Help Center | 2026-09-04 |
| https://help.heygen.com/en/articles/10029081-how-to-get-started-with-video-translation | How to Get Started with Video Translation | HeyGen Help Center | 2026-09-04 |
| https://am8evw00qys.typeform.com/to/wauwjUYP?typeform-source=t.co | Legacy Typeform destination for the 2023 avatar entry; content unavailable when read | 2026-09-04 |
| https://app.heygen.com/guest/templates?cid=d9a269e9 | HeyGen guest-template destination; content unavailable when read | 2026-09-04 |
| https://app.heygen.com/home | HeyGen - AI Spokesperson Video Creator | 2026-09-04 |
| https://labs.heygen.com/expressive-photo-avatar | HeyGen Labs | 2026-09-04 |
| https://app.heygen.com/avatars | HeyGen - AI Spokesperson Video Creator | 2026-09-04 |
| https://docs.heygen.com/docs/heygen-mcp-server | HeyGen MCP Server legacy documentation endpoint; content unavailable when read | 2026-09-04 |
| https://github.com/heygen-com/heygen-mcp | heygen-com/heygen-mcp legacy repository endpoint; content unavailable when read | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:heygen`, thread `avatar-platform-and-developer-integration`, 2 dated events 2024-07-12 → 2025-05-07.
- **Practical note:** From 2025-05-07, evaluate the published MCP server documentation and repository alongside the browser app rather than assuming browser-only workflows; capability and production readiness still require separate verification.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
