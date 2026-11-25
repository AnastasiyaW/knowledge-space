---
title: Disney Research — Interactive Generative Motion Editing
category: organizations
tags: [disney-research, disney_research, interactive-generative-motion-editing, organization]
aliases: ["Disney Research"]
---

# Disney Research — Interactive Generative Motion Editing

**Development line:** `organization:disney-research` · thread `interactive-generative-motion-editing`  
**Events:** 1 dated, 2026-08-01 → 2026-08-01 · **Researched:** 2026-09-03 · confidence: medium

## What it is

Disney Research — DisneyResearch|Studios publishes machine-learning and visual-computing research for animation, VFX, and research teams. — public papers and technical demonstrations; — 2022 work on face re-aging in video; — 2026 work on editable skeletal motion. Limit: the reviewed official pages name papers and videos, not a public installer, API, or source release. Verdict: use it as an R&D reference or reproduction target, not as an off-the-shelf tool.

## Development line

- **2026-08-01 — Disney Research documented interactive generative motion editing via scheduled inpainting.** On 2026-08-01, this line recorded Disney Research's work titled “Interactive Generative Motion Editing via Scheduled Inpainting,” linked from its Studios site. The accompanying video link indicates that the work included a visual demonstration of the motion-editing approach.

## What changed

Disney Research — the dated items are research publications, not versions of one product. — 2022-12-02: the linked video documents FRAN, published by Disney Research on 2022-11-30: a U-Net approach to video face re-aging with localized artist control, aimed at reducing frame-by-frame 2D painting while preserving identity and temporal stability. — 2026-08-01: the linked publication, dated 2026-07-30 by Disney and 2026-07-31 on arXiv, introduces scheduled inpainting: an inference-time method for editing pretrained generative skeletal-motion models through a preservation schedule and a spatiotemporal mask; it supports extension, stitching, and compositing without additional training. — Found today (2026-09-04): DisneyResearch|Studios still presents itself as a machine-learning and visual-computing research organization with continuing publications. Limit: the later work addresses body motion, not facial re-aging. Verdict: scheduled inpainting does not supersede FRAN; they are separate research tracks.

## How to use this

As of 2026-08-01, practitioners evaluating generative motion-editing workflows should consider Disney Research's scheduled-inpainting approach as a documented research direction and review its linked demonstration before selecting an implementation.

1. Choose a concrete research output from the current catalogue; Disney Research is a publisher of machine-learning and visual-computing work rather than a software endpoint.
  — <https://studios.disneyresearch.com/research/>
2. Treat Scheduled Inpainting as an internal reproduction or prototype target: the official page supplies a paper and demonstration, not a named public installation, API, or code repository.
  — <https://studios.disneyresearch.com/2026/07/30/interactive-generative-motion-editing-via-scheduled-inpainting/>
3. Provide a base skeletal-motion clip and spatial joint constraints to a pretrained generative motion model that supports direct manipulation.
  — <https://arxiv.org/html/2607.29133>
4. Set a temporal preservation schedule and per-joint, per-frame mask: retain unchanged motion and permit synthesis around the intended edit; use the same mechanism for extension, stitching, or compositing.
  — <https://arxiv.org/html/2607.29133>
5. Review outputs for constraint following, continuity, foot sliding, and behavior outside the model’s learned motion distribution before admitting them to an animation pipeline.
  — <https://arxiv.org/html/2607.29133>

## Best practices

- Make the broad structural edit with full-body constraints first, then refine motion curves with individual position and orientation constraints.
  — <https://arxiv.org/html/2607.29133>
- Align clip origin and direction and normalize scale before blending motions; the paper associates missing alignment with warps, discontinuities, and sliding artifacts.
  — <https://arxiv.org/html/2607.29133>
- Use a smoothly decaying Gaussian influence region around an edit so neighboring frames remain partly anchored to the base motion instead of changing cadence abruptly.
  — <https://arxiv.org/html/2607.29133>
- Do not expect reliable reconstruction far outside the model’s learned motion distribution; exaggerated or periodic motion may need added extrema constraints and creates more constraints to manage later.
  — <https://arxiv.org/html/2607.29133>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The 2022 face-re-aging work and the 2026 skeletal-motion work share an organization but no reviewed source establishes a predecessor or successor relation between them.
- The reviewed official project pages do not name a public code repository, weights, API, installer, or license; public implementation availability is unverified.
- No separate Chinese-language first-party source was found in today’s bounded search.
- The reviewed sources do not disclose whether either method was deployed in a Disney production after publication.

## Sources

| source | title | read |
|---|---|---|
| https://studios.disneyresearch.com/research/ | Research | Disney Research Studios | 2026-09-04 |
| https://www.youtube.com/watch?v=ZP1ApcdyAjk | Production Ready Face Re Aging for Visual Effects - YouTube | 2026-09-04 |
| https://studios.disneyresearch.com/2022/11/30/production-ready-face-re-aging-for-visual-effects/ | Production-Ready Face Re-Aging for Visual Effects | Disney Research Studios | 2026-09-04 |
| https://studios.disneyresearch.com/2026/07/30/interactive-generative-motion-editing-via-scheduled-inpainting/ | Interactive Generative Motion Editing via Scheduled Inpainting | Disney Research Studios | 2026-09-04 |
| https://arxiv.org/html/2607.29133 | Interactive Generative Motion Editing via Scheduled Inpainting | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:disney-research`, thread `interactive-generative-motion-editing`, 1 dated events 2026-08-01 → 2026-08-01.
- **Practical note:** As of 2026-08-01, practitioners evaluating generative motion-editing workflows should consider Disney Research's scheduled-inpainting approach as a documented research direction and review its linked demonstration before selecting an implementation.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
