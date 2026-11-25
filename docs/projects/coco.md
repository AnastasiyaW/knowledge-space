---
title: CoCo
category: projects
date: 2026-03-15
tags: [coco, coco-development, project]
aliases: ["CoCo"]
---

# CoCo

**Development line:** `project:coco` · thread `coco-development`  
**Last event:** 2026-03-15 · 1 dated since 2026-03-15 · **Researched:** 2026-09-05 · confidence: medium

## What it is

CoCo is a research workflow that turns text prompts into executable Python and Matplotlib scene code. It renders a draft in a sandbox, checks the layout against the prompt, and refines the draft into a final image. It targets structured layouts, spatial relations and dense text. Across three benchmarks, it reports a 10K draft–final training set and gains of 68.83%, 54.8% and 41.23% over direct generation. It works as a research reference, not a ready inference package.

## Development line

- **2026-03-15 — CoCo public project resources linked.** On 2026-03-15, CoCo was referenced through linked GitHub and Hugging Face project resources. This creates a dated public reference point for the project's code and model-related materials.

## What changed

- 2026-03-15 — CoCo appeared with code and a Hugging Face model link. The repository documents the code-to-draft-to-refinement method, but ships no documented end-user inference command.
- 2026-08-06 — arXiv v2 became the current paper version and recorded ECCV 2026 acceptance.

## How to use this

From 2026-03-15, start from the linked GitHub repository and Hugging Face page to locate public assets. Review the source files directly before using them.

1. Start from the repository’s method description: generate executable Matplotlib scene-layout code from a prompt, render the draft, then use it as the intermediate plan for image refinement.
  — <https://github.com/micky-li-hd/CoCo>
2. Treat the bundled sandbox as research code: it executes supplied Python with an `exec` call, so run it only in an isolated environment and do not feed it untrusted code.
  — <https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py>
3. Use the paper for the training and evaluation design; the public Hugging Face page has no model card, tracked downloads, or hosted inference provider.
  — <https://arxiv.org/abs/2603.08652>

## Best practices

- Use an executable draft where prompt-only planning loses spatial or structural precision; verify the draft before committing to final image generation.
  — <https://arxiv.org/abs/2603.08652>
- Keep code execution isolated and time-bounded: the supplied sandbox performs a dangerous-code check and applies a timeout, but still executes generated Python.
  — <https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py>

## Superseded by this

- 2026-08-06 — arXiv v1 (2026-03-09) is no longer the current paper version; use v2 when citing the paper.

## Still unknown

- The Hugging Face page has no model card or tracked-download data, and the repository contains only a README, figures, and sandbox code. A reproducible public inference setup, checkpoint contents, hardware requirements and license are not documented in the inspected sources.
- The repository announces the paper’s release on 2026-03-09, while the dated event is 2026-03-15. The inspected first-party sources do not establish what changed specifically on 2026-03-15.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/micky-li-hd/CoCo | CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation — official repository | 2026-09-05 |
| https://huggingface.co/mickyhimself/CoCo | mickyhimself/CoCo — Hugging Face model page | 2026-09-05 |
| https://arxiv.org/abs/2603.08652 | CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation | 2026-09-05 |
| https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py | CoCo sandbox.py | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:coco`, thread `coco-development`, 1 dated events 2026-03-15 → 2026-03-15.
- **Practical note:** From 2026-03-15, practitioners should use the linked GitHub repository and Hugging Face page as the starting points for locating CoCo's public resources; their contents and applicability still require source-level review.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
