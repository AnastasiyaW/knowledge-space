---
title: WithEveryone
category: projects
date: 2026-08-22
tags: [project, witheveryone]
aliases: ["WithEveryone"]
---

# WithEveryone

**Development line:** `project:witheveryone` · thread `witheveryone`  
**Last event:** 2026-08-22 · 1 dated since 2026-08-22 · **Researched:** 2026-09-05 · confidence: medium

## What it is

WithEveryone is a research system for generating a single group scene with 5–10 specified people.

- Reference binding: binds each reference to a separate ID token.
- Layout planning: builds an identity-layout plan and uses it during generation.

The authors tested only 5–10 identities, and the research checkpoint cannot be released under the base model license. Today this is a method to study, not an available generator.

## Development line

- **2026-08-22 — WithEveryone public project site linked.** On 2026-08-22, the public WithEveryone project site went online. The site describes the method without releasing code, weights, or a demo.

## What changed

- **2026-08-20** — arXiv published v1 of the preprint describing the method for groups of 5–10 reference identities.
- **2026-08-22** — The public WithEveryone project site appeared, without code, weights, a demo, or a package release.

## How to use this

From 2026-08-22, use the public WithEveryone site as a project reference, and verify its claims before relying on them.

1. Match the task to the method scope: one group scene with 5–10 reference identities, not a general service for arbitrary group sizes.
  — <https://arxiv.org/html/2608.20336v1>
2. Read the paper and project page as a method reference: separate ID tokens, identity-layout planning, and region-grounded supervision.
  — <https://doby-xu.github.io/WithEveryone/>
3. Do not plan deployment or inference yet: watch the official repository for code and checkpoints, as the open version is still training.
  — <https://github.com/Doby-Xu/WithEveryone/>

## Best practices

- Obtain consent from everyone in reference images, and attach provenance signals to generated outputs.
  — <https://arxiv.org/html/2608.20336v1>
- Treat reported metrics as an author evaluation on a single 210-sample benchmark, not independent proof of quality across arbitrary groups.
  — <https://arxiv.org/html/2608.20336v1>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No dated first-party archive of the page exists for 2026-08-22, so we cannot verify which technical details appeared that day.
- The release date, base model, quality, license, and hardware requirements for the open replacement are unstated; the paper names only the research foundation HunyuanImage 3.5-preview.
- Primary sources offer no independent reproduction of the claimed results.

## Sources

| source | title | read |
|---|---|---|
| https://doby-xu.github.io/WithEveryone/ | WithEveryone: Unified Planning and Identity Grounding for Group Image Generation | 2026-09-05 |
| https://github.com/Doby-Xu/WithEveryone/ | Doby-Xu/WithEveryone | 2026-09-05 |
| https://arxiv.org/abs/2608.20336 | [2608.20336] WithEveryone: Unified Planning and Identity Grounding for Group Image Generation | 2026-09-05 |
| https://arxiv.org/html/2608.20336v1 | WithEveryone: Unified Planning and Identity Grounding for Group Image Generation (HTML v1) | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:witheveryone`, thread `witheveryone`, 1 dated events 2026-08-22 → 2026-08-22.
- **Practical note:** From 2026-08-22, use the public WithEveryone site as a project reference, and verify its claims before relying on them.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
