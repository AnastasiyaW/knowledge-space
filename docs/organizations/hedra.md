---
title: Hedra — Hedra product development
category: organizations
tags: [hedra, hedra-product-development, hedra_release, organization, product_releases]
aliases: ["Hedra"]
---

# Hedra — Hedra product development

**Development line:** `organization:hedra` · thread `hedra-product-development`  
**Events:** 3 dated, 2025-04-02 → 2026-02-20 · **Researched:** 2026-09-03 · confidence: medium

## What it is

Hedra — a single workflow for people who would otherwise combine a talking-avatar service, video generator, voice tool, and model API. — Agent and Studio for image, video, speech, editing, references, and reusable instructions. — First-party character models: Character 3, Avatar, and Omnia; the API also exposes image, video, and audio models. Limit: Character 3 accepts image, text, and audio for videos up to 10 minutes; Omnia is intended for short clips of about eight seconds at 1080p. Verdict: use it when character performance and a shared creation/API workflow matter; select and validate the model per job rather than treating all video modes as interchangeable.

## Development line

- **2025-04-02 — Hedra’s public video application route was cited.** On 2025-04-02, a dated Hedra reference cited the public `/app/video` route. This records a public video-product entry point in the development line, while the link alone does not establish its launch date, capabilities, or access conditions.
- **2025-07-24 — Hedra’s public avatar application route was cited.** On 2025-07-24, a dated Hedra reference cited the public `/app/avatar` route. This records an avatar-product entry point in the development line, without claiming a specific release, model, workflow, or availability change.
- **2026-02-20 — Hedra linked developer quickstart documentation with application entry points.** On 2026-02-20, a dated Hedra reference included its application home route and developer quickstart documentation. This records a public developer-documentation surface alongside product entry points, but does not establish the contents, release date, or availability of any API or feature.

## What changed

2024-08-17 — Hedra’s home page was recorded, but no release text survives with the event; a specific product change cannot be reconstructed safely. 2025-03-07 — Character 3 replaced Character 2 in March 2025. It changed Hedra’s character-video core to jointly use image, text, and audio for lip-sync and character animation. 2025-04-02 — The recorded /app/video route is now a Video workspace with manual tools. The available record does not establish a distinct release beyond that video-creation entry point. 2025-07-24 — The recorded /app/avatar route now redirects to /app/home, which starts an Agent workspace. This is evidence of a changed entry route, not evidence that the current Hedra Avatar model launched in July 2025. 2026-02-20 — A developer quickstart was recorded. Its current version requires a paid account, API key, credits, and a model-list request before generation; this is current documentation, not proof of its exact February 2026 state. 2026-02-05 — Hedra launched Omnia, adding scene motion, dynamic environments, and directed camera control to audio-conditioned character video. 2026-09-04 (found today) — Hedra is now organized around an Agent/Studio workflow plus a developer API, rather than only a character-video playground.

## How to use this

As of 2026-02-20, practitioners evaluating Hedra should consult its public application entry points and developer quickstart before assuming which video, avatar, or developer workflows are available.

1. For Studio work, create a Space, state the goal, audience, output format, constraints, and reference material, then review and direct iterations on the canvas.
  — <https://www.hedra.com/docs/pages/app/getting-started/overview>
2. For a speaking character video, prepare a portrait and clean audio; use an avatar workflow where audio drives lip-sync and motion.
  — <https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video>
3. For Omnia, provide image and audio, then explicitly direct subject motion, camera, and background in the prompt.
  — <https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model>
4. For API work, use a paid account, create an API key with sufficient credits, and request the current model catalog before choosing a model.
  — <https://www.hedra.com/docs/pages/developer/getting_started/quickstart>
5. Upload required assets, submit the generation, and poll its status until it is complete and returns the output asset.
  — <https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video>

## Best practices

- Use a clear, well-lit close portrait and clean voice audio; describe delivery and restrained motion when the intended performance is specific.
  — <https://www.hedra.com/models/video/hedra/character-3>
- For Omnia, use one subject, explicit camera direction, 16:9, clear paced audio, and assemble longer work from short clips of about eight seconds at 1080p.
  — <https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model>
- Call the model catalog before generation and inspect its slug, input requirements, duration, resolution, and pricing; prefer the stable slug over an environment-specific model ID.
  — <https://www.hedra.com/docs/api-reference/public/list-models>
- Treat generation as asynchronous: poll status and use the returned asset only after completion.
  — <https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video>

## Superseded by this

- March 2025 — Character 2 is superseded by Character 3 for Hedra’s core character-video model.
- 2025-07-24 — Do not use /app/avatar as a stable current entry path: observed on 2026-09-04, it redirects to /app/home.
- February 2026 — Guidance that treats Hedra as only a locked-camera talking-avatar tool is incomplete: Omnia adds directed camera and environment motion, with a short-clip limit.
- 2026-09-04 — Guidance that treats Hedra as only a web video playground is obsolete: current documentation exposes an Agent workspace, manual media tools, and a developer API.

## Still unknown

- The 2024-08-17 event contains only a home-page URL; its specific release claim is unavailable.
- The 2025-03-07 event has no extracted URL, so connecting it to Character 3 relies on the official model page’s March 2025 release date rather than preserved event text.
- The 2025-04-02 and 2025-07-24 route references do not preserve enough text to identify a separate release or feature launch.
- The linked X status URL could not be retrieved, and http://hedra.com/app/home returned no readable page; neither is used as factual evidence.

## Sources

| source | title | read |
|---|---|---|
| https://www.hedra.com/ | Hedra — Visual Inference Models and Infrastructure | 2026-09-04 |
| https://www.hedra.com/app/video | Hedra Video Playground | 2026-09-04 |
| https://www.hedra.com/app/avatar | Hedra Agent — General Visual Intelligence | 2026-09-04 |
| https://www.hedra.com/docs/pages/developer/getting_started/quickstart | Hedra API Quickstart Guide | 2026-09-04 |
| https://www.hedra.com/docs/pages/app/getting-started/overview | Meet Hedra Agent | 2026-09-04 |
| https://www.hedra.com/models/video/hedra/character-3 | Hedra Character 3: Omnimodal Character Video | 2026-09-04 |
| https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model | Hedra Omnia: Unified AI Video for Character-Driven Content | 2026-09-04 |
| https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video | Generate an Avatar Video | 2026-09-04 |
| https://www.hedra.com/docs/api-reference/public/list-models | List Available AI Models | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:hedra`, thread `hedra-product-development`, 3 dated events 2025-04-02 → 2026-02-20.
- **Practical note:** As of 2026-02-20, practitioners evaluating Hedra should consult its public application entry points and developer quickstart before assuming which video, avatar, or developer workflows are available.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
