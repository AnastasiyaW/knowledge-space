---
title: UMO
category: projects
date: 2026-03-19
tags: [project, umo]
aliases: ["UMO"]
---

# UMO

**Development line:** `project:umo` · thread `umo`  
**Last event:** 2026-03-19 · 1 dated since 2026-03-19 · **Researched:** 2026-09-06 · confidence: medium

## What it is

UMO is a research framework for teams building 3D human-motion pipelines. It fine-tunes HY-Motion-Lite instead of shipping a downloadable motion tool.

- Motion generation: generates text-conditioned human motion.
- Motion control: completes, edits, and controls source motion through preserve, generate, and edit operations.
- Task encoding: encodes trajectories, obstacles, and two-person reactions as text-conditioned tasks.

## Development line

- **2026-03-19 — UMO’s public project site and source repository were linked.** The authors presented UMO as a unified 3D human-motion research method with qualitative demonstrations and a linked repository. That repository is not a runnable implementation today.

## What changed

2026-03-19: The authors presented UMO as a unified 3D human-motion research method with qualitative demonstrations and a linked repository. That repository is not a runnable implementation today. 2026-08-17: ECCV's preliminary accepted-papers list added a poster listing for UMO (#96, Poster Session 3). This changed publication status, but not code, weights, or API availability.

## How to use this

As of 2026-03-19, start from the linked UMO project site and GitHub repository for documentation and source inspection.

1. Decide whether the target is 3D skeletal human motion rather than image or video generation: evaluated tasks include text-to-motion, inpainting, instruction editing, text-serialized geometry, and reactions.
  — <https://arxiv.org/html/2603.15975v1>
2. Use the paper and author demonstrations to map a research experiment to a natural-language description or edit, a structured trajectory, or a textual spatial constraint.
  — <https://oliver-cong02.github.io/UMO.github.io/>
3. Check the official repository for both code and model artifacts before scheduling implementation. No official install or inference path is currently published.
  — <https://github.com/Oliver-Cong02/UMO>

## Best practices

- Do not substitute unmodified HY-Motion for UMO on inpainting or geometry tasks: the paper reports that zero-shot or training-free repurposing fails substantially.
  — <https://arxiv.org/html/2603.15975v1>
- Treat the paper's 4×B200 training, 100k steps, 50-step Euler solver, and CFG 2.0 as study settings, not a published minimum specification.
  — <https://arxiv.org/html/2603.15975v1>
- Verify the paper title and author-linked repository before acting on the name UMO. ByteDance uses the same name for a separate image-customization project.
  — <https://github.com/bytedance/UMO>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No first-party changelog or immutable snapshot establishes the exact 2026-03-19 launch action, so that date is treated as the public project/repository window, not as a proven code or model release date.
- Official sources provide no UMO checkpoint, license, install instructions, CLI/API, input-file contract, or minimum hardware specification.
- The generic name UMO is also used by an unrelated ByteDance image-customization project. The author names, paper title, and Oliver-Cong02 repository identify this work as the human-motion project.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2603.15975 | UMO: Unified In-Context Learning Unlocks Motion Foundation Model Priors — arXiv v1 record | 2026-09-06 |
| https://arxiv.org/html/2603.15975v1 | UMO: Unified In-Context Learning Unlocks Motion Foundation Model Priors — full paper HTML | 2026-09-06 |
| https://oliver-cong02.github.io/UMO.github.io/ | UMO — authors' project page and qualitative demonstrations | 2026-09-06 |
| https://github.com/Oliver-Cong02/UMO | Oliver-Cong02/UMO — official repository landing page | 2026-09-06 |
| https://eccv.ecva.net/Conferences/2026/AcceptedPapers | ECCV 2026 preliminary accepted-papers list | 2026-09-06 |
| https://eccv.ecva.net/Conferences/2026 | ECCV 2026 conference announcements | 2026-09-06 |
| https://github.com/bytedance/UMO | bytedance/UMO — unrelated image-customization project with the same name | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:umo`, thread `umo`, 1 dated events 2026-03-19 → 2026-03-19.
- **Practical note:** As of 2026-03-19, practitioners should use the linked UMO project site and GitHub repository as the starting points for documentation and source inspection.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
