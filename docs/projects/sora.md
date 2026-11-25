---
title: Sora
category: projects
date: 2025-09-30
tags: [project, sora, sora-access-expansion, sora-public-development]
aliases: ["Sora", "Sora 2"]
---

# Sora

**Development line:** `project:sora` · thread `sora-public-development`  
**Last event:** 2025-09-30 · 4 dated since 2024-02-15 · **Researched:** 2026-09-04 · confidence: high

## What it is

Sora is OpenAI's model family for generating, extending and editing short video with audio from text or image prompts.

- Text-to-video: generates video from text prompts.
- Image-guided generation: creates video using reference images.
- Character persistence: reuses consistent characters across generations.
- Extension: lengthens existing video clips.
- Targeted edit: alters specific sections within video.
- MP4 download: exports completed generations as video files.

Sora 2 and Sora 2 Pro support 16- and 20-second clips; the API is deprecated and shuts down on 2026-09-24. Starting new production work on it is temporary and risky; existing integrations need a migration plan and an export of results.

## Development line

- **2024-02-15 — OpenAI publicly introduced Sora.** On 2024-02-15, OpenAI published the Sora project page, marking its public introduction. An accompanying social link indicated contemporaneous public discussion without supplied post content. We retain this as the opening public milestone for the project.
- **2024-12-09 — OpenAI documented Sora-supported countries.** Sora Turbo launched on sora.com for ChatGPT Plus and Pro subscribers, with clips up to 1080p and 20 seconds, storyboard, remix, blend and extension. The rollout initially excluded the UK, Switzerland and the EEA.
- **2024-12-09 — Sora received a public-facing service and video presentation.** Sora Turbo launched on sora.com for ChatGPT Plus and Pro, supporting clips up to 1080p and 20 seconds, storyboard, remix, blend and extension. Initial access excluded the UK, Switzerland and the EEA.
- **2025-09-30 — Sora exposed an Explore destination on ChatGPT.** The release added video and audio generation, multi-shot directing control, characters and a separate social iOS application. Sora 2 Pro served higher-quality 1080p exports.

## What changed

- **2024-02-15:** OpenAI introduced Sora as a research diffusion transformer using spacetime patches. The technical report confirmed variable durations, resolutions and aspect ratios with a claimed maximum of one minute of HD video, but no public product existed.
- **2024-03-14:** An interview with CTO Mira Murati, published on 2024-03-13, confirmed a planned public release in 2024 while training data, errors and safety remained open questions.
- **2024-12-09:** The research preview became the production model Sora Turbo on sora.com for ChatGPT Plus and Pro. At launch, Plus included up to 50 videos at 480p or fewer at 720p, while Pro offered a tenfold volume. It generated clips up to 1080p and 20 seconds with storyboard, remix, blend and extension. The rollout initially excluded the UK, Switzerland and the EEA.
- **2024-12-21:** The referenced X post could not be verified, leaving no confirmed additions for this date.
- **2025-02-27:** OpenAI expanded Sora availability to the EU, UK, Switzerland, Norway, Liechtenstein and Iceland.
- **2025-09-30:** OpenAI released Sora 2 with video and audio generation, multi-shot control, characters and a standalone social iOS app. The production API introduced `sora-2` and `sora-2-pro` for 16- and 20-second clips, with Sora 2 Pro delivering higher-quality 1080p exports.
- **2026-03-25:** The referenced X page failed to load, leaving no independent dated clarification for this day.
- **2026-04-26:** OpenAI discontinued the web and mobile application versions of Sora.
- **2026-09-05:** The API remains documented but deprecated, scheduled for shutdown on 2026-09-24.

## How to use this

As of 2024-12-09, verify Sora's country availability on the public service rather than assuming the February 2024 announcement implied universal access.

1. If you need new generations before the shutdown date, verify that the short API lifetime fits your product. Use `sora-2` for fast iterations and `sora-2-pro` for 1080p export.
  — <https://developers.openai.com/api/docs/guides/video-generation>
2. Create an asynchronous task through `POST /videos`, specifying model, text prompt, dimensions and duration.
  — <https://developers.openai.com/api/docs/guides/video-generation>
3. Receive the result through the `video.completed` or `video.failed` webhook, then download the MP4 file using `GET /videos/{video_id}/content`.
  — <https://developers.openai.com/api/docs/guides/video-generation>
4. For content created in the closed web or app versions of Sora, open `sora.chatgpt.com/sunset`, select Export and wait for the email confirmation.
  — <https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation>

## Best practices

- Start with short, low-resolution clips to test prompts, motion and composition; reserve 1080p and longer renders for final exports.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Specify shot type, subject, action, environment and lighting so unwanted details stay out.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Handle `video.failed` events and listen for webhooks rather than polling in production pipelines.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Do not submit human faces, public figures, copyrighted characters or music, because current API limits reject them.
  — <https://developers.openai.com/api/docs/guides/video-generation>
- Export past work and avoid new dependencies on the Sora API without a migration plan before 2026-09-24.
  — <https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation>

## Superseded by this

- 2024-02-15: research Sora with claimed one-minute generation does not describe the available Sora 2 API.
- 2024-12-09: Sora Turbo and its tier limits were replaced by Sora 2 and Sora 2 Pro, and no longer serve as integration guidance.
- 2025-09-30: instructions to use Sora through the iOS or web applications became obsolete on 2026-04-26 when those products shut down.
- 2026-09-24: any recommendation to build new dependencies on the Sora Videos API becomes obsolete after the scheduled shutdown.

## Still unknown

- Content from the 2024-12-21 X post at `https://x.com/rohanjamin/status/1870525134664278331?s=46&t=AR_orbfYSU6RyY_sYcnmhQ` was unavailable for verification, so we cannot confirm an access expansion or other release.
- The `https://x.com/soraofficialapp` account failed to open on 2026-03-25; it may relate to a separate app or handle rather than model or API changes.
- Official documentation confirms the API shutdown timeline, but live API calls in this pass did not verify it.

## Sources

| source | title | read |
|---|---|---|
| https://openai.com/index/video-generation-models-as-world-simulators/ | Video generation models as world simulators | 2026-09-05 |
| https://www.youtube.com/watch?v=mAUpxN-EIgU | OpenAI's Sora Made Me Crazy AI Videos—Then the CTO Answered (Most of) My Questions | 2026-09-05 |
| https://openai.com/index/sora-is-here/ | Sora is here | 2026-09-05 |
| https://techcrunch.com/2025/02/27/openais-sora-is-now-available-in-the-eu-uk/ | OpenAI’s Sora is now available in the EU, UK | 2026-09-05 |
| https://openai.com/index/sora-2/ | Sora 2 is here | 2026-09-05 |
| https://developers.openai.com/api/docs/guides/video-generation | Video generation with Sora | 2026-09-05 |
| https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | What to know about the Sora discontinuation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:sora`, thread `sora-public-development`, 4 dated events 2024-02-15 → 2025-09-30.
- **Practical note:** As of 2024-12-09, practitioners should verify Sora's current country availability and use the public Sora service surface rather than assume that the February 2024 announcement implied universal access.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
