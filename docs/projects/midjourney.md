---
title: Midjourney
category: projects
date: 2025-04-04
tags: [midjourney, midjourney-beta-access, midjourney-model-and-feature-releases, midjourney_blend_command, midjourney_v4, midjourney_v5, project, releases]
aliases: ["Midjourney"]
---

# Midjourney

**Development line:** `project:midjourney` · thread `midjourney-model-and-feature-releases`  
**Last event:** 2025-04-04 · 6 dated since 2022-07-12 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Midjourney is a subscription image-and-video generator for art direction, concept work, and rapid visual iteration.

- Generates stills from text, image prompts, style references, personalization, and Edit Model references.
- Supports variations, inpainting, outpainting, canvas expansion, and turning a still into a 5-second video.

## Development line

- **2022-07-12 — Midjourney opened beta access.** On 2022-07-12, beta access began with a shortened link, without public details on eligibility or rollout.
- **2022-11-07 — Midjourney introduced V4.** On 2022-11-07, Midjourney released V4 with official links and external coverage, leaving exact access conditions unspecified.
- **2023-01-16 — Midjourney documented the Blend command.** On 2023-01-16, Blend appeared as a user-facing milestone without a surviving source URL for its rollout.
- **2023-03-09 — Midjourney opened V5 staging evaluation.** Output became more photographic and matched prompts more closely, though users needed longer prompts for the intended aesthetic.
- **2023-03-16 — Midjourney documented V5.** On 2023-03-16, V5 marked a major model milestone, without a surviving URL for release timing or feature availability.
- **2025-04-04 — Midjourney released V7 Alpha.** On 2025-04-04, Midjourney linked the official V7 Alpha update and Imagine pages, marking the milestone without detailing full account rules.

## What changed

- **2022-07-12** — The beta-access note lacks an accessible source; official documentation places V3 as the default model from July 2022.
- **2022-07-26** — No surviving URL or corroborated product change.
- **2022-11-07** — V4, released in November 2022, introduced a new codebase and AI architecture, with stronger coherence, detail handling, image prompting, and multi-prompts.
- **2023-01-16** — Blend launch date is not independently verifiable; `/blend` remains available in Discord for combining 2–5 images.
- **2023-03-09** — V5 staging aligns with the March 2023 V5 release: more photographic output and closer prompt matching, though longer prompts could be needed for the intended aesthetic.
- **2023-03-16** — No surviving URL separates this V5 mention from the March V5 rollout.
- **2023-05-03** — A community report claimed new V5.1 prompt blocking. Official history dates V5.1 to May 4, 2023, recording stronger default aesthetics, coherence, natural-language interpretation, and `--tile`; the specific blocking claim is unverified.
- **2023-08-22** — No surviving URL supports a distinct product change.
- **2025-04-04** — V7 Alpha opened for testing with personalization enabled by default, Draft Mode, and improved prompt/image coherence; some editing functions initially fell back to V6.
- **2025-06-17** — V7 became the default model.
- **2026-04-14 / 2026-06-10** — V8.1 launched, then became default, adding faster generations and optional 2K HD images.
- **2026-07-24** — V8.2 became the default. Its Edit Model replaced V7 Omni Reference, Character Reference, and Retexture in the current V8 workflow.

## How to use this

As of 2025-04-04, treat Midjourney model versions and alpha releases as distinct workflow targets: confirm current availability on the official update and Imagine pages before adopting a version in production.

1. Create or sign in to an account, choose a subscription plan, and open the Create page.  
  — <https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide>
2. Type a concise visual prompt in the Imagine bar and submit it to generate an initial set of images.  
  — <https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web>
3. Keep V8.2 as the default or pin a model with `--v #` when a project needs repeatable version-specific behavior.  
  — <https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version>
4. Add up to four reference images or edit an existing image with written instructions through the V8 Edit Model.  
  — <https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model>
5. Choose a promising result, then make Subtle or Strong variations instead of restarting from scratch.  
  — <https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations>
6. When motion is needed, use a still as the first frame and generate a 5-second video; choose motion and plan settings deliberately because video uses more GPU time.  
  — <https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video>

## Best practices

- Write short, concrete visual descriptions; include only the subject, medium, setting, lighting, color, mood, and composition details that matter.  
  — <https://docs.midjourney.com/docs/prompts>
- Treat image prompts as influence rather than copying: describe every required final element in text, and use the Editor for precise edits.  
  — <https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts>
- For a consistent look, use a Style Reference for style and write the desired subject as content, not as an instruction to modify the reference.  
  — <https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference>
- Use `--seed` to compare prompt changes under a near-identical V8 starting point; do not treat a seed as a reusable style or character lock.  
  — <https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds>
- Build a Personalization profile or Moodboard for recurring project aesthetics; more deliberate image selections improve the profile's fit.  
  — <https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization>
- Upload only images you have rights to use and keep external-image edits within the service rules and applicable law.  
  — <https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor>

## Superseded by this

- 2022 beta and V3 access rules are obsolete for default work: start with a subscription on the web Create page or Discord bot.
- V8.2 supersedes default guidance for V4, V5, and V5.1; pin `--v` only when a project requires legacy behavior.
- 2023 Blend advice is no longer the web workflow: use multiple image prompts without text on the web; `/blend` remains Discord-only.
- The Edit Model supersedes V7 Omni Reference, V6 Character Reference, and Retexture in the V8 workflow.
- V8.2 supersedes V7 as the default model; V7 remains a selectable legacy version rather than the current default.

## Still unknown

- Claims behind the 2022-07-12 beta-access event and unlinked events on 2022-07-26, 2023-03-16, and 2023-08-22 cannot be reconstructed from available evidence.
- The short link, V5 staging page, linked Discord message, linked Reddit post, and linked DTF page were not retrievable in this research session; their claims were not used as factual support.
- Official current documentation dates the V7 release to 2025-04-03, while the V7 Alpha announcement is dated 2025-04-04; the one-day difference remains unresolved.
- Current plan prices and usage allowances were not collected, so we do not recommend a specific subscription tier.

## Sources

| source | title | read |
|---|---|---|
| https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features | Legacy Features – Midjourney | 2026-09-04 |
| https://updates.midjourney.com/v7-alpha/ | V7 Alpha | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version | Version – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide | Getting Started Guide – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web | Creating on Web – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model | Edit Model – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations | Variations – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video | Video – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/docs/prompts | Prompt Basics – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts | Image Prompts – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference | Style Reference – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds | Seeds – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization | Personalization – Midjourney | 2026-09-04 |
| https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor | Editor – Midjourney | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:midjourney`, thread `midjourney-model-and-feature-releases`, 6 dated events 2022-07-12 → 2025-04-04.
- **Practical note:** As of 2025-04-04, practitioners should treat Midjourney model versions and alpha releases as distinct workflow targets: confirm current availability through the official update and Imagine pages before adopting a version in a production workflow.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
