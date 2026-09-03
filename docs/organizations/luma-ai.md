---
title: Luma AI — Luma AI Product Development
category: organizations
tags: [luma-ai, luma-ai-product-development, luma-dream-machine, organization]
aliases: ["Luma AI"]
---

# Luma AI — Luma AI Product Development

**Development line:** `organization:luma-ai` · thread `luma-ai-product-development`  
**Events:** 2 dated, 2023-10-05 → 2025-02-01 · **Researched:** 2026-09-03 · confidence: medium

## What it is

Luma AI is a creative workspace and developer API for teams producing image and video assets. — Ray3.2: text-to-video, image-to-video, video-to-video, and reframing. — UNI-1.1: image generation and reference/source-guided editing. — Luma App: agent-led multimodal workflows; Luma API: programmatic generation. Limit: public API video-to-video accepts a source clip of 18 seconds or less; generated video durations are 5 or 10 seconds. Verdict: start new work with Luma Ray and UNI, not the deprecated Dream Machine label.

## Development line

- **2023-10-05 — Luma AI linked its Interactive Scenes product page.** On 2023-10-05, a dated Luma AI message linked to its Interactive Scenes product page. The link indicates an identifiable product-development milestone for Luma AI, but the available evidence does not establish whether that date was a launch, update, or promotion.
- **2025-02-01 — Luma AI linked the Dream Machine website.** On 2025-02-01, a dated Luma AI message linked to the Dream Machine website. This is a material product-line development signal, while the available evidence does not establish the specific feature, release state, or announcement claim associated with the link.

## What changed

2023-10-05 — Interactive Scenes: Luma presented a 3D line for embeddable, shareable scenes on web and mobile; its page cites 30 fps browser playback, 8 MB objects, and 20 MB scenes. 2025-02-01 — Dream Machine: a separate image/video creation surface appears in the history; the accessible landing page today describes image and video production, not a successor to Interactive Scenes. Found today (2026-09-04) — Luma names Ray3.2, released 2026-06-09, as its current video model and UNI-1.1 as its current image model. It names Luma App and Luma API as active surfaces and marks Dream Machine and Ray2 deprecated.

## How to use this

As of 2025-02-01, practitioners should assess Luma AI through both its Interactive Scenes and Dream Machine product paths, while verifying current capabilities directly because these dated links alone do not establish launch scope or feature details.

1. Choose Luma App for a browser-based creative workspace, or Luma API when generation belongs inside a product or production pipeline.
  — <https://lumalabs.ai/llm-info>
2. For API work, submit a generation with `model: ray-3.2` and choose `video`, `video_edit`, or `video_reframe` as the generation type.
  — <https://docs.agents.lumalabs.ai/api/resources/generations/methods/create>
3. For video-to-video editing, provide the source by URL, data, file ID, or prior generation; include a video MIME type for URL/data input.
  — <https://docs.agents.lumalabs.ai/api/resources/generations/methods/create>
4. Add explicit keyframe anchors when a shot needs frame-level art direction; enable EXR export only together with HDR.
  — <https://docs.agents.lumalabs.ai/api/resources/generations/methods/create>
5. Treat generation as asynchronous: retain the returned job ID, wait for `completed`, and handle documented failure states before using an output.
  — <https://docs.agents.lumalabs.ai/api/resources/generations/methods/create>

## Best practices

- Start video-to-video from footage whose timing, framing, or performance is worth preserving, then deliberately select an `adhere_*`, `flex_*`, or `reimagine_*` edit strength.
  — <https://docs.agents.lumalabs.ai/api/resources/generations/methods/create>
- Use 360p for fast, lower-cost draft validation and raise resolution only after the shot direction is accepted.
  — <https://docs.agents.lumalabs.ai/api/resources/generations/methods/create>
- Bind guide images to explicit frame indexes rather than leaving important visual changes implicit in a prompt.
  — <https://docs.agents.lumalabs.ai/api/resources/generations/methods/create>
- For an API integration, send a stable opaque user ID without personal data and record both job state and machine-readable failure codes.
  — <https://docs.agents.lumalabs.ai/api/resources/generations/methods/create>
- Replace Dream Machine, Ray2, and standalone Photon instructions in new workflow documentation with current Ray and UNI terminology.
  — <https://lumalabs.ai/llm-info>

## Superseded by this

- 2025-02-01 — treating Dream Machine as Luma's current video model or primary product name is obsolete; Luma's current guidance replaces it with Ray3.2 and the Luma App/API surfaces.

## Still unknown

- Interactive Scenes is a WebGL 3D capture-and-sharing line, while Dream Machine is an image/video generation line. No first-party page accessed today proves a direct product-to-product succession between them.
- The Dream Machine landing page does not preserve a dated change log for 2025-02-01, so its exact feature set on that date is unverified.
- Current support status, migration terms, and account compatibility for the older Interactive Scenes product were not established by the accessed sources.

## Sources

| source | title | read |
|---|---|---|
| https://lumalabs.ai/interactive-scenes | Luma AI - Interactive Scenes | 2026-09-04 |
| https://dream-machine.lumalabs.ai/ | Boards | Dream Machine | 2026-09-04 |
| https://lumalabs.ai/llm-info | Luma — Official Information for AI Assistants | Luma | 2026-09-04 |
| https://lumalabs.ai/news/introducing-ray-3-2 | Luma Introduces Ray3.2 Model & API: Complete Creative Control for Video Generation | Luma | 2026-09-04 |
| https://docs.agents.lumalabs.ai/api/resources/generations/methods/create | Create a generation | Luma Agents | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:luma-ai`, thread `luma-ai-product-development`, 2 dated events 2023-10-05 → 2025-02-01.
- **Practical note:** As of 2025-02-01, practitioners should assess Luma AI through both its Interactive Scenes and Dream Machine product paths, while verifying current capabilities directly because these dated links alone do not establish launch scope or feature details.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
