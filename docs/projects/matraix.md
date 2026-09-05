---
title: MatrAIx
category: projects
date: 2026-08-11
tags: [matraix, persona-8b-public-documentation, project]
aliases: ["MatrAIx"]
---

# MatrAIx

**Development line:** `project:matraix` · thread `persona-8b-public-documentation`  
**Last event:** 2026-08-11 · 1 dated since 2026-08-11 · **Researched:** 2026-09-05 · confidence: high

## What it is

MatrAIx is infrastructure for running LLM agents with user profiles across Survey, AI Chatbot, Web, and App tasks.

- 1 290 categorical persona attributes.
- Public Persona 1M dataset with 599 847 grounded and 400 000 synthetic entries.
- 1 010 benchmark tasks across more than 25 domains.

It generates and stress-tests hypotheses, but does not replace research with real people. It fits reproducible product and agent evaluations if we do not present the results as human validation.

## Development line

- **2026-08-11 — MatrAIx Persona 8B was publicly referenced with a visual playground quickstart.** Practical scope covers Survey, AI Chatbot, Web, and OS-app. Live runs require model provider API keys. Docker is required for Web and OS-app tasks.

## What changed

2026-08-04 — MatrAIx published its technical report. Persona 8B claims 8.3 billion records, a Playground with four environments, and 18 189 completed eval trajectories. 2026-08-11 — MatrAIx became available as an open Playground and task library. Practical scope covers Survey, AI Chatbot, Web, and OS-app. Live runs require model provider API keys, and Docker is required for Web and OS-app. Note on the 2026-08-11 milestone: the initial release is MatrAIx-Persona-8B, not a standalone Persona-8B inference model. Its public dataset is Persona 1M, not the full 8.3 billion claimed personas. New dated milestones: 2026-07-31 opened the Playground and task library; 2026-08-01 published Persona 1M; 2026-08-04 presented the report on arXiv.

## How to use this

As of 2026-08-11, start evaluating MatrAIx Persona 8B using its repository and visual playground quickstart.

1. Install Python 3.12, uv, and Docker. On Windows, use WSL2 because native PowerShell and cmd do not support task verifiers.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
2. Clone the repository, create a uv environment, and install the core package alongside Playground, Rewardkit, and Harbor-LangSmith.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
3. Verify the environment with a Survey and Chat smoke test without Docker, then run Harbor smoke for Web and OS-app with Docker.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
4. For real evaluation, set a compatible model provider API key, select a task and persona, generate a job recipe, and run it with matraix run. Retrieve results with matraix results.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B/blob/main/docs/quickstart.md#10-playground--play-tasks-visually>
5. For cohort testing rather than smoke checks, download Persona 1M and specify it as the dataset in the Playground or CLI.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>

## Best practices

- Start with dev-sample and smoke tests to check the installation, not to draw conclusions about user populations.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
- Use Persona 1M for research instead of the local sample of roughly 200 personas. Fix the recipe, model, and cohort so runs remain reproducible.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
- Treat simulation as hypothesis generation and stress testing. Validate product decisions with real user data afterward.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>
- Do not run Web and OS-app evaluations without Docker. On Windows, keep the repository inside the WSL2 filesystem instead of /mnt/c.
  — <https://github.com/MatrAIx-ai/MatrAIx-Persona-8B>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Official sources show no separate release dated exactly 2026-08-11. The date reflects the state of the repository and documentation, not a formal release tag.
- No independent benchmark proves that these simulation results predict user behavior in a specific product.
- The repository does not use GitHub Releases. Commit compatibility with future model provider APIs is not pinned to a release version.

## Sources

| source | title | read |
|---|---|---|
| https://matraix.ai/ | MatrAIx — Simulate Before Reality | 2026-09-05 |
| https://github.com/MatrAIx-ai/MatrAIx-Persona-8B | MatrAIx-Persona-8B repository | 2026-09-05 |
| https://github.com/MatrAIx-ai/MatrAIx-Persona-8B/blob/main/docs/quickstart.md#10-playground--play-tasks-visually | MatrAIx Quickstart | 2026-09-05 |
| https://arxiv.org/abs/2608.04205 | MatrAIx: Simulating the World with 8.3 Billion Persona Agents | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:matraix`, thread `persona-8b-public-documentation`, 1 dated events 2026-08-11 → 2026-08-11.
- **Practical note:** As of 2026-08-11, practitioners should begin evaluation or hands-on use of MatrAIx Persona 8B from its repository and visual-playground quickstart.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
