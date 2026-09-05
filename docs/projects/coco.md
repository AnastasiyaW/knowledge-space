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

CoCo is a research workflow that turns text prompts into executable Python and Matplotlib scene code for image generation.

We use it to generate structured layouts, spatial relations and dense text:
- Scene preview: renders a draft layout in a sandbox and checks it against the prompt.
- Image refinement: uses the draft layout to guide final generation.

The paper reports a 10K draft–final training set and gains of 68.83%, 54.8% and 41.23% over direct generation across three benchmarks. It is a research reference, not a ready inference package.

## Development line

- **2026-03-15 — CoCo public project resources linked.** On 2026-03-15, project resources linked CoCo to GitHub and Hugging Face as public references for its code and model materials.

## What changed

- 2026-03-15 — CoCo appeared as code plus a Hugging Face model link. The public repository describes the code-to-draft-to-refinement method, but ships no documented end-user inference command.
- 2026-08-06 — The paper's arXiv v2 became the current version and records ECCV 2026 acceptance.

## How to use this

From 2026-03-15, use the linked GitHub repository and Hugging Face page to locate public resources. Review their contents at source level before use.

1. Start from the repository method description: generate executable Matplotlib scene-layout code from a prompt. Render the draft, then use it as the intermediate plan for image refinement.
  — <https://github.com/micky-li-hd/CoCo>
2. Treat the bundled sandbox as research code. It executes supplied Python with an `exec` call, so run it only in an isolated environment and do not feed it untrusted code.
  — <https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py>
3. Use the paper for the training and evaluation design. The public Hugging Face page has no model card, tracked downloads, or hosted inference provider.
  — <https://arxiv.org/abs/2603.08652>

## Best practices

- Use an executable draft when prompt-only planning loses spatial or structural precision. Verify the draft before committing to final image generation.
  — <https://arxiv.org/abs/2603.08652>
- Keep code execution isolated and time-bounded. The supplied sandbox checks for dangerous code and applies a timeout, but it still executes generated Python.
  — <https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py>

## Superseded by this

- 2026-08-06 — arXiv v1 (2026-03-09) is no longer current. Use v2 when citing the paper.

## Still unknown

- The Hugging Face page has no model card or tracked-download data. The repository contains only a README, figures, and sandbox code. Checkpoint contents, hardware requirements, license, and a reproducible public inference setup remain undocumented.
- The repository announces the paper release on 2026-03-09, while the dated event is 2026-03-15. First-party sources do not state what changed on 2026-03-15.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/micky-li-hd/CoCo | CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation — official repository | 2026-09-05 |
| https://huggingface.co/mickyhimself/CoCo | mickyhimself/CoCo — Hugging Face model page | 2026-09-05 |
| https://arxiv.org/abs/2603.08652 | CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation | 2026-09-05 |
| https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py | CoCo sandbox.py | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:coco`, thread `coco-development`, 1 dated events 2026-03-15 → 2026-03-15.
- **Practical note:** From 2026-03-15, use the linked GitHub repository and Hugging Face page to locate public resources. Review their contents at source level before use.
- **Confidence:** medium. Dated supersedes above govern what is obsolete.
