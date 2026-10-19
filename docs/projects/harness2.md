---
title: "Harness^2: harness2-open-source-release — Harness2 Open Source Release"
category: "projects"
date: 2026-10-18
tags: ["harness2", "harness2-open-source-release", "project"]
aliases: ["Harness^2: harness2-open-source-release"]
---

# Harness^2: harness2-open-source-release — Harness2 Open Source Release

**Development line:** project:harness2 · thread harness2-open-source-release  
**Last event:** 2026-10-18 · 3 dated since 2026-10-18 · **Researched:** 2026-10-19 · confidence: high

## What it is

Harness² is a research framework for engineers testing whether an agent’s surrounding system can improve without changing model weights. It edits and evaluates prompts, guardrails, memory, tool guidance, subagents, skills, scripts, and plugins. It supports parallel and sequential recursion, OpenCode and Codex executors, and three benchmark integrations.

Model-backed runs need local setup and can incur API costs. Executor web access is unrestricted by default. Use Harness² for controlled harness-improvement experiments, not as evidence that a revised harness is safe for unreviewed production use.

## Development line

- **2026-10-18 — Harness^2 introduces recursive agent harness optimization for frozen language models.** Authors from Google introduced Harness^2, a framework that optimizes the harness of a frozen language model \(prompts, guardrails, skills, scripts, intermediate code\) without reference verifiers. It uses task-level and setup-level recursion with a reusable improvement library. Reported WorkBuddy-Bench average scores rose from 64.2 to 75.7 for GLM-5 at k=1, and to 80.8 at k=5. JobBench rose from 31.5/32.9 to 39.0. The post notes that checking multiple candidates increases inference token cost.
- **2026-10-18 — Google open-sources Harness² agent harness.** On 2026-10-18, the recorded link reported that Google released Harness² as open source. It describes a ready-to-use harness for recursive management of AI agents in open environments. Agents can learn from experience on tasks outside the harness’s original purpose. The harness has eight components: system prompt, guardrails, memory, tool-use instructions, subagents, skills, scripts, and plugins. The linked GitHub repository is google-research/harness2.
- **2026-10-18 — Google open-sources Harness² agent harness.** Google released Harness² as open source. It is described as a ready-to-use harness for recursive management of AI agents in an open environment. Its eight components are the system prompt, protective constraints, memory, tool-use instructions, subagents, skills, scripts, and plugins.
- **2026-10-18 — other reporting on this date.**
  - The accompanying paper says that the frozen-model harness has eight editable file-mounted components. Task-level refinement uses Propose–Probe–Compose without ground-truth feedback. A separate harnessing-level loop keeps evidence-supported lessons for later tasks. (2026-10-09) — <https://arxiv.org/abs/2610.14224>
  - The release is Apache-2.0 source code with a Linux/Python 3.12/uv installation path and a deterministic local demo that needs no model credentials. Model-backed benchmark runs add Node.js, Google Cloud CLI, benchmark-specific dependencies, and user model configuration. (undated) — <https://github.com/google-research/harness2>
  - The public implementation supports OpenCode and Codex executors, parallel or sequential recursion, and JobBench, LAB, and WorkBuddy-Bench. Its README warns that executor network access is unrestricted and that Codex runs with its sandbox disabled unless the operator configures network restrictions. (undated) — <https://github.com/google-research/harness2>

## What changed

Public release \(2026-10-18\): Harness² made its recursive-harness method available as an Apache-2.0 code repository. The paper describes task-level Propose–Probe–Compose refinement and persistent improvement-library updates across tasks.

## How to use this

1. On Linux with Python 3.12 and uv, create the documented virtual environment, install the editable package, and run the credential-free demo before connecting a model.
  — <https://github.com/google-research/harness2>
2. For a model-backed run, install the listed runtime and benchmark dependencies, configure model settings and authentication, then start with one benchmark task and a small selection.
  — <https://github.com/google-research/harness2>
3. Run checking, refinement, judging, and reporting with the same benchmark, executor, subset, recursion budget, mode, and seed. Use dry-run to inspect task selection without model calls.
  — <https://github.com/google-research/harness2>
4. Choose parallel recursion to explore candidate harnesses more widely, or sequential recursion to carry refinements through successive steps. Keep adopted harnesses only with their supporting execution evidence.
  — <https://github.com/google-research/harness2>

## Best practices

- Configure network restrictions before evaluation so public benchmark rubrics, answers, or grading criteria cannot leak into an executor with unrestricted web access.
  — <https://github.com/google-research/harness2>
- Keep the evaluation configuration identical to the refinement run when judging and reporting. Changing the benchmark, executor, subset, recursion mode, budget, or seed invalidates a like-for-like result.
  — <https://github.com/google-research/harness2>
- Treat larger recursion budgets as an explicit compute–performance trade-off. The paper counts both execution and improvement tokens, and its gains were measured only in the evaluated benchmark configurations.
  — <https://arxiv.org/abs/2610.14224>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The repository page does not provide a stable public release timestamp. Its event evidence is therefore marked undated rather than assigned an inferred repository date.
- No independent practitioner report of sustained use or benchmark reproduction was found in the qualified sources.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2610.14224 | Harness²: Recursive Agent Harnessing for an Open World | 2026-10-19 |
| https://github.com/google-research/harness2 | google-research/harness2: Recursive Agent Harnessing for an Open World | 2026-10-19 |

## Agent brief {#agent-brief}

- **Subject:** project:harness2, thread harness2-open-source-release, 3 dated events 2026-10-18 → 2026-10-18.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.