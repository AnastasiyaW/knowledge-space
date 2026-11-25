---
title: "Genxr Bench: genxr-bench-release — Genxr Bench Release"
category: "projects"
date: 2026-10-23
tags: ["genxr-bench", "genxr-bench-release", "project"]
aliases: ["Genxr Bench: genxr-bench-release"]
---

# Genxr Bench: genxr-bench-release — Genxr Bench Release

**Development line:** project:genxr-bench · thread genxr-bench-release  
**Last event:** 2026-10-23 · 1 dated since 2026-10-23 · **Researched:** 2026-10-25 · confidence: high

## What it is

GenXR-Bench is an open software engineering benchmark for coding agents that build interactive extended reality (XR) apps on consumer hardware. Its tasks are XR applications, not the usual 2D script repositories. What it covers:

- 112 expert-curated tasks: whole app generation, feature implementation and bug repair
- A natural-language spec plus an editable project scaffold for each task
- A held-out test suite with scripted interaction, adaptive user behaviour, programmatic checks and visual assertions
- Candidate code that runs directly on consumer XR hardware and interactive runtimes

The leading models reach 50.9% Pass@1. They fail mostly on asynchronous sensor lifecycles and on grounding spatial coordinates. GenXR-Bench is the first rigorous standard for spatial code generation, where static unit tests do not reflect runtime correctness.

## Development line

- **2026-10-23 — GenXR-Bench released for evaluating coding agents on XR development.** Researchers announced it on arXiv: 112 expert-authored tasks for agents that build interactive XR apps. Across 10 models, the best configuration reached 50.9% overall Pass@1.
  - The tasks split into 67 app generation, 24 feature implementation and 21 bug repair. The test suites mix scripted and adaptive interaction with programmatic and visual assertions, and they agree with blinded human experts 96.5% of the time. Top models stop at 50.9% Pass@1 because of failures in asynchronous sensor lifecycles and physical grounding. (2026-10-23) — <https://arxiv.org/abs/2610.29014>

## What changed

Text-centric and single-file benchmarks such as SWE-bench check code with static diffs and unit tests. They cannot measure dynamic 3D rendering or asynchronous hardware input, and GenXR-Bench was built to fill that gap. The first testbed has 112 curated tasks across app synthesis, feature addition and bug fixing. Baseline runs on ten commercial and open coding agents set the starting difficulty. They show that physical interaction semantics are still the main obstacle for automated spatial software engineering.

## How to use this

1. Pick an XR task from the benchmark repository. Give the coding agent its natural-language spec and editable project scaffold.
  — <https://arxiv.org/abs/2610.29014>
2. Let the agent generate the app, add the requested features or repair spatial bugs inside the scaffold.
  — <https://arxiv.org/abs/2610.29014>
3. Run the result in the benchmark harness on consumer XR hardware or a simulator, with automated scripted and adaptive interaction sequences.
  — <https://arxiv.org/abs/2610.29014>
4. Collect results from programmatic assertions and visual checks, then compute overall Pass@1.
  — <https://arxiv.org/abs/2610.29014>

## Best practices

- Test XR coding agents on continuous multimodal interaction and visual assertions, not on static code diffs or pure-function unit tests.
  — <https://arxiv.org/abs/2610.29014>
- Write agent prompts and tool APIs so they account for asynchronous sensor lifecycles and embodied spatial coordinate systems.
  — <https://arxiv.org/abs/2610.29014>

## Superseded by this

- The idea that 2D repository tasks with static unit tests are enough, on their own, to check an AI coding agent's skill at interactive 3D spatial computing.
  — <https://arxiv.org/abs/2610.29014>

## Still unknown

- Individual Pass@1 scores for each of the 10 evaluated models, beyond the overall top score of 50.9%
- A public repository link and licence terms for downloading the task scaffolds and evaluation harnesses

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2610.29014 | GenXR-Bench: A Benchmark for Evaluating Coding Agents on Interactive Extended Reality Development | 2026-10-25 |

## Agent brief {#agent-brief}

- **Subject:** project:genxr-bench, thread genxr-bench-release, 1 dated events 2026-10-23 → 2026-10-23.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
