---
title: ShotVerse
category: projects
date: 2026-03-14
tags: [project, shotverse, shotverse-development]
aliases: ["ShotVerse"]
---

# ShotVerse

**Development line:** `project:shotverse` · thread `shotverse-development`  
**Last event:** 2026-03-14 · 1 dated since 2026-03-14 · **Researched:** 2026-09-06 · confidence: high

## What it is

ShotVerse is a research system for creators and researchers who need explicit, consistent camera trajectories across multiple shots.

- Planner turns a global description and per-shot descriptions into camera trajectories.
- Controller renders multi-shot video from text and trajectories.

ShotVerse-Bench reports 20 500 clips and 12 million frames; experiments assemble scenes of 2–4 shots with 249 frames each. As of 2026-09-06, this is a method specification and benchmark rather than an installable tool: the official repository still marks weights, inference code, dataset, and training as future deliveries.

## Development line

- **2026-03-14 — ShotVerse public project references were shared.** On 2026-03-14, ShotVerse was referenced with links to its project website, GitHub repository, and a Hugging Face destination. Together, these links establish a dated public reference point for the project and its associated resources.

## What changed

2026-03-14 — ShotVerse was introduced as a research method for explicit camera control in multi-shot video. Primary materials with direct dates do not confirm a runnable public release on that day.

## How to use this

As of 2026-03-14, use the ShotVerse website and GitHub repository as the starting points for public project resources. The linked Hugging Face destination requires separate verification before use.

1. Read the current paper and match your task to its input: a global description plus per-shot descriptions, not a single text prompt.
  — <https://arxiv.org/abs/2603.11421>
2. Check the project page and the Prompt Details examples to evaluate camera moves and editing structure.
  — <https://shotverse.github.io/>
3. Check the repository before planning adoption: official installation and inference pipelines do not exist yet, so paper settings are not a runnable recipe.
  — <https://github.com/Songlin1998/ShotVerse>

## Best practices

- Keep the two-level input for research reproduction: a global scene context and a separate description for each shot, because Planner expects this structure.
  — <https://arxiv.org/html/2603.11421v1>
- Treat the metrics, the Qwen3-VL-2B/HoloCine stack, and training on 96 H20 as experimental setup, not a verified user workflow.
  — <https://arxiv.org/html/2603.11421v1>
- Do not put ShotVerse into a production pipeline before official artifacts arrive: a public repository does not mean an available model.
  — <https://github.com/Songlin1998/ShotVerse>

## Superseded by this

- 2026-08-24 — arXiv v2 replaces v1 from 2026-03-12 as the current paper version. This does not backdate the 2026-03-14 status or prove that code or weights were released.

## Still unknown

- We found no primary archival proof that the current site or repository existed on 2026-03-14.
- We found no independent reproducible run, model license, checkpoints, public dataset, or verified user practices.
- Chinese search queries returned aggregator summaries rather than primary documentation or practical reports.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2603.11421v1 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation (arXiv v1) | 2026-09-06 |
| https://arxiv.org/html/2603.11421v1 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation (arXiv v1 full text) | 2026-09-06 |
| https://arxiv.org/abs/2603.11421 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation (current arXiv record) | 2026-09-06 |
| https://shotverse.github.io/ | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation | 2026-09-06 |
| https://github.com/Songlin1998/ShotVerse | GitHub - Songlin1998/ShotVerse | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:shotverse`, thread `shotverse-development`, 1 dated events 2026-03-14 → 2026-03-14.
- **Practical note:** As of 2026-03-14, treat the ShotVerse website and linked GitHub repository as the starting points for public project resources. The linked Hugging Face destination requires separate verification before use.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
