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

- **2022-07-12 — Midjourney beta access documented.** The archive recorded a beta-access item with a shortened link, but the link leaves eligibility, scope, and behavior unverified.
- **2022-11-07 — Midjourney V4 introduced.** The archive linked the official site and external coverage of Midjourney V4, without establishing exact features or access conditions.
- **2023-01-16 — Midjourney Blend command documented.** The archive recorded a Blend command item, but kept no source URL to verify behavior or rollout.
- **2023-03-09 — Midjourney opened V5 staging.** Output became more photographic and matched prompts more closely, though longer prompts were sometimes needed for the intended aesthetic.
- **2023-03-16 — Midjourney V5 documented.** The archive recorded a V5 milestone, but kept no URL to confirm timing, features, or availability.
- **2025-04-04 — Midjourney released V7 Alpha.** The archive linked the official V7 Alpha update page and official Imagine page, but the links do not establish full feature sets or access rules.

## What changed

On 2022-07-12, the beta-access note lacked accessible corroboration; official history places V3 as the default model from July 2022. On 2022-07-26, no URL or product change survived. On 2022-11-07, V4 introduced a new codebase and AI architecture, improving coherence, detail handling, image prompting, and multi-prompts after its November 2022 release. On 2023-01-16, a Blend event was recorded without an independent launch date; `/blend` remains available in Discord for combining 2–5 images. On 2023-03-09, V5 staging aligned with the March 2023 V5 release, offering more photographic output and closer prompt matching, with longer prompts needed for some aesthetics. On 2023-03-16, no surviving URL separated this mention from the March V5 rollout. On 2023-05-03, a community report alleged new V5.1 prompt blocking; official history dates V5.1 to May 4, 2023, introducing stronger default aesthetics, coherence, natural-language interpretation, and `--tile`, leaving the blocking policy unverified. On 2023-08-22, no surviving URL supports a product change. On 2025-04-04, V7 Alpha opened with default personalization, Draft Mode, and improved prompt/image coherence, while some editing functions temporarily fell back to V6. On 2025-06-17 (found today), V7 became the default model. On 2026-04-14 and 2026-06-10 (found today), V8.1 launched and then became the default, adding faster generations and optional 2K HD images. On 2026-07-24 (found today), V8.2 became the default, and its Edit Model replaced V7 Omni Reference, Character Reference, and Retexture in the V8 workflow.

## How to use this

As of 2025-04-04, treat model versions and alpha releases as distinct workflow targets: confirm availability through the official update and Imagine pages before adopting a version in production.

1. Sign in or create an account, pick a subscription plan, and open the [Create page](https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide).
2. Enter a concise visual prompt in the Imagine bar to generate an initial set of images as described in [Creating on Web](https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web).
3. Use V8.2 as the default, or pin a model with `--v #` via [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version) when repeatable behavior matters.
4. Supply up to four reference images or edit an image using written text with the [Edit Model](https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model).
5. Pick a solid result, then generate Subtle or Strong [Variations](https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations) instead of starting over.
6. For motion, turn a still into the initial frame of a 5-second [Video](https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video); select motion and plan settings deliberately because video consumes more GPU time.

## Best practices

- Write short, concrete visual descriptions covering only key subject, medium, setting, lighting, color, mood, and composition details, following [Prompt Basics](https://docs.midjourney.com/docs/prompts).
- Treat [Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts) as influence rather than exact copies: describe every required element in text, and use the Editor for fine edits.
- Use a [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference) to set appearance, and write the subject as fresh content rather than an instruction to modify the reference.
- Use `--seed` to compare prompt adjustments against an identical V8 starting point per [Seeds](https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds); do not use seeds as character or style locks.
- Build a Personalization profile or Moodboard per [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization) for recurring project styles; curated image selections yield a tighter match.
- Upload only images you own the rights to, and keep external edits compliant with service rules and applicable law under [Editor](https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor).

## Superseded by this

- 2022 beta and V3 access rules are obsolete for daily use: current work starts with a subscription and the web Create page or Discord bot.
- Guidance naming V4, V5, or V5.1 as the default model is superseded by V8.2; pin `--v` only when legacy output is required.
- 2023 Blend instructions do not apply to the web interface: pass multiple image prompts without text on web; `/blend` remains Discord-only.
- Guidance for V7 Omni Reference, V6 Character Reference, and Retexture is superseded by the V8 Edit Model.
- V7 as the default model is superseded by V8.2; V7 remains a selectable legacy model.

## Still unknown

- The claims behind the 2022-07-12 beta-access note and unlinked entries on 2022-07-26, 2023-03-16, and 2023-08-22 cannot be reconstructed from available records.
- The short link, V5 staging page, Discord message, Reddit post, and DTF page were unreachable during research and do not serve as factual support.
- Current documentation dates the V7 release to 2025-04-03, while the V7 Alpha announcement is dated 2025-04-04; the reason for this one-day gap remains unresolved.
- Current subscription prices and usage allowances were not gathered, so no specific tier is recommended.

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