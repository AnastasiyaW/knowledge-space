---
title: Google Veo — Veo model and access releases
category: projects
date: 2026-04-01
tags: [google-veo, google_veo, google_veo_access, project, veo-model-and-access-releases, veo_model_releases]
aliases: ["Google Veo", "Google Veo 2", "Veo 3"]
---

# Google Veo — Veo model and access releases

**Development line:** `project:google-veo` · thread `veo-model-and-access-releases`  
**Last event:** 2026-04-01 · 4 dated since 2025-04-14 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Google Veo is Google DeepMind's video generation model family, offered through the Gemini app, Gemini API, Google AI Studio, and Flow.

- Users: developers building video features through the Gemini API or AI Studio, and creators working in the Gemini app or Flow.
- Key capability: text-to-video and image-to-video; the Veo 3 generation adds native audio, reference-image control, scene extension, and first/last-frame transitions.
- Limits: Veo 3.1 Lite is a paid preview with 720p or 1080p output and 4, 6, or 8 second clips. Google states that natural spoken audio "remains an area of active development." Outputs carry SynthID watermarks.

## Development line

- **2025-04-14 — Veo accessible through Google AI Studio (not verified).** The stub recorded this date. The research did not find a primary source for it.
- **2025-05-20 — Google introduced Veo 3.** Announced at Google I/O on 2025-05-20. Gemini app access at launch was limited to US AI Ultra subscribers, and Vertex AI access opened at the same time.
- **2025-08-23 — Gemini access route for Veo (not verified as a dated event).** Gemini-app access already existed at the May 2025 launch; no August 2025 primary source was found.
- **2026-03-31 — Veo 3.1 Lite preview (date corrected from 2026-04-01).** Google's announcement post is dated March 31, 2026.

## What changed

- 2025-05-20 — Veo 3 introduced at Google I/O (Gemini app for AI Ultra in the US; Vertex AI).
- 2025-06 — Veo 3 entered preview on Vertex AI (press reporting; date approximate).
- 2026-03-31 — Veo 3.1 Lite released as a paid preview in the Gemini API and Google AI Studio, priced below 50% of Veo 3.1 Fast per Google, with text-to-video and image-to-video, 16:9 and 9:16, 720p and 1080p, and 4/6/8 second durations.
- 2026-04-07 — Google stated a planned Veo 3.1 Fast price reduction. Execution was not verified.

## How to use this

1. As of 2026-11, pick the route: Veo 3.1 Lite through the Gemini API or Google AI Studio (paid preview); Veo features in the Gemini app or Flow for consumer workflows. — <https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/>
2. Check the model documentation for the exact model id and limits. The ai.google.dev page redirects to AI Studio documentation; this research did not read it. — <https://ai.google.dev/gemini-api/docs/models/veo-3.1-lite-generate-preview>
3. Choose 720p or 1080p, a 4, 6, or 8 second duration, and 16:9 or 9:16. Cost scales with duration. — <https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/>
4. Review capability claims on the Veo model page (native audio, reference images, extension, outpainting, object insertion and removal, 1080p and 4K) before selecting a route. — <https://deepmind.google/models/veo/>

## Best practices

- Run a small paid batch to measure your cost per second of output before scaling; the announcement gives only relative pricing (the figures were in an image). — <https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/>
- Keep spoken segments short and check audio quality by listening, because Google describes natural speech as still in development. — <https://deepmind.google/models/veo/>
- Confirm regional availability, preview terms, and quotas before production use. — <https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Exact model ids, quotas, rate limits, and general-availability status for Veo 3.1 Lite were not verified from the model documentation.
- Price figures for Veo 3.1 Lite and Veo 3.1 Fast were not read (image-only in the announcement).
- The 2025-04-14 AI Studio date and the 2025-08-23 Gemini event are not verified.
- Vertex AI general availability for Veo 3 was reported but no GA date was confirmed.
- Regional availability and the Gemini app tiers as of 2026-11 were not checked.

## Sources

| source | title | read |
|---|---|---|
| https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/ | Veo 3.1 Lite announcement (Google blog) | 2026-11-21 |
| https://deepmind.google/models/veo/ | Veo model page (Google DeepMind) | 2026-11-21 |
| https://ai.google.dev/gemini-api/docs/models/veo-3.1-lite-generate-preview | Veo 3.1 Lite model documentation (redirects to AI Studio docs; not read) | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:google-veo`, thread `veo-model-and-access-releases`, 4 dated events 2025-04-14 → 2026-03-31 (one date corrected, two not verified).
- **Practical note:** As of 2026-11, evaluate Veo 3.1 Lite through the Gemini API or AI Studio as a paid preview. Verify current model id, quotas, region, and pricing from the model documentation before production adoption.
- **Confidence:** medium. Announcement and model page read; model documentation and pricing not read. Dated supersedes above are the authority for what is obsolete.
