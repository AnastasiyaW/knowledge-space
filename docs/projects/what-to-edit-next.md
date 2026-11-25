---
title: What to Edit Next — Public site reference
category: projects
date: 2026-08-17
tags: [alibaba/what-to-edit-next, project, public-site-reference, what-to-edit-next]
aliases: ["What to Edit Next"]
---

# What to Edit Next — Public site reference

**Development line:** `project:what-to-edit-next` · thread `public-site-reference`  
**Last event:** 2026-08-17 · 1 dated since 2026-08-17 · **Researched:** 2026-09-05 · confidence: medium

## What it is

What to Edit Next is a Qwen App method that suggests the next edit from the latest image, current query, and editing intent.

- Qwen3-VL-8B policy fine-tuned with curated intents and click feedback.
- Qwen3-VL-30B-A3B image-first verifier that rejects unsupported or redundant edits during training.

## Development line

- **2026-08-17 — What to Edit Next public site was referenced.** What to Edit Next’s project page was linked to establish a site reference. It records only the reference, not a launch, feature release, code release, or change in public access.

## What changed

- 2026-08-03: What to Edit Next v1 was submitted to arXiv, documenting the three-stage Qwen App method.
- 2026-08-17: What to Edit Next’s project page was linked; this establishes a site reference only, not a documented launch, feature release, code release, or public-access change.
- 2026-08-18: What to Edit Next arXiv v2 was submitted; its version history supplies no revision changelog.

## How to use this

As of 2026-08-17, start with the linked public project site to evaluate What to Edit Next. Check source material directly before assuming features or release state.

1. Start with the project page to assess the method, not to install it. Its visible navigation exposes paper, arXiv, and method material rather than a public integration entry point.
  — <https://what-to-edit-next.github.io/>
2. For a comparable implementation, form each input from the latest image, rewritten current query, and editing intent. Generate five to seven suggestions and randomly select three for display.
  — <https://arxiv.org/html/2608.07565v1>
3. Validate edits image-first. Inventory the image, split each candidate into required sources and desired targets, then reject missing sources and already-satisfied targets. An added object is a target and need not already be visible.
  — <https://arxiv.org/html/2608.07565v1>

## Best practices

- Do not optimize clicks alone. The authors report visual inconsistency rising from 3.0% after SFT to 3.7% after click RL, then falling to 0.9% with the grounding reward.
  — <https://arxiv.org/html/2608.07565v1>
- Observe the image before interpreting candidate instructions. Keep source-existence checks separate from target-state checks.
  — <https://arxiv.org/html/2608.07565v1>
- Treat the paper as a decision contract rather than a reproducible production package. It omits verbatim production prompts, product-specific lexicons, and exact post-processing triggers.
  — <https://arxiv.org/html/2608.07565v1>

## Superseded by this

- 2026-08-18: arXiv v1 (2026-08-03) stopped being the latest paper version when v2 was submitted. Do not attribute v2-specific material to 2026-08-17.

## Still unknown

- The project page has no publication timestamp. Its contents and availability on 2026-08-17 cannot be established from the current page.
- Visible links do not prove that code, weights, an API, or a demo do not exist elsewhere.
- arXiv v2 has no revision note, so its substantive differences from v1 are unknown.
- No dated first-party Chinese announcement or public implementation guide was located in the checked sources.
- The single dated record and matching preprint identify one subject; no second project under the same name was found.

## Sources

| source | title | read |
|---|---|---|
| https://what-to-edit-next.github.io/ | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems | 2026-09-05 |
| https://arxiv.org/abs/2608.07565v1 | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems, arXiv v1 | 2026-09-05 |
| https://arxiv.org/html/2608.07565v1 | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems, arXiv HTML v1 | 2026-09-05 |
| https://arxiv.org/abs/2608.07565 | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems, arXiv version history | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:what-to-edit-next`, thread `public-site-reference`, 1 dated events 2026-08-17 → 2026-08-17.
- **Practical note:** As of 2026-08-17, start evaluation from the linked public project site. Check source material directly before assuming features or release status.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
