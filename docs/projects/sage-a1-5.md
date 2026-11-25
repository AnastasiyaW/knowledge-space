---
title: "Sage-A1.5: sage-a1-5-release — Sage A1 5 Release"
category: "projects"
date: 2026-10-22
tags: ["project", "sage-a1-5", "sage-a1-5-release"]
aliases: ["Sage-A1.5: sage-a1-5-release"]
---

# Sage-A1.5: sage-a1-5-release — Sage A1 5 Release

**Development line:** project:sage-a1-5 · thread sage-a1-5-release  
**Last event:** 2026-10-22 · 2 dated since 2026-10-22 · **Researched:** 2026-10-23 · confidence: medium

## What it is

Sage-A1.5 is an open-weight 35B mixture-of-experts agentic foundation model. It is for researchers and software engineers running long-horizon tasks, and it competes directly with proprietary reasoning models.

- **Parallel subagents:** orchestrates them, each in an isolated execution context.
- **Self-verification:** checks itself inside its chain of thought, with no external reward model.
- **Scientific discovery:** runs workflows across disciplines.
- **Serving:** exposes an OpenAI-compatible API through vLLM or SGLang.

3B of 35B parameters are active per forward pass. Context is 256K tokens natively, expandable to 512K via YaRN. Under heavy concurrent subagent load, MoE routing overhead and memory capacity set the limit.

It is an efficient, self-hostable open base for complex agentic pipelines that need to correct themselves mid-trajectory.

## Development line

- **2026-10-22 — Shanghai AI Lab releases Sage-A1.5 agentic model.** It is a 35B-parameter MoE agentic model built on Qwen3.6-35B-A3B and Agents-A1. It was announced with a 262K-token context window and OpenAI-compatible serving via SGLang or vLLM. Reported scores: GAIA 95.1, XBench-DS 92.0, SWE-bench Pro 61.2, MLE-Lite 65.2.
- **2026-10-22 — other reporting on this date.**
  - The model is published under the Apache 2.0 license by Shanghai AI Lab's InternScience group. It activates 3B parameters per token out of 35B total. It adds native multi-agent task delegation through parallel isolated subagents. (2026-10-22) — <https://huggingface.co/InternScience/Sage-A1.5>
  - The model card describes self-verification built into the chain of thought, so the model corrects itself during execution without external verifiers. Context goes beyond the native 256K up to 512K tokens via YaRN. (2026-10-22) — <https://huggingface.co/InternScience/Sage-A1.5>

## What changed

The Agents-A1 series used dense models; Sage-A1.5 is a sparse mixture of experts based on Qwen3.6-35B-A3B. Single-agent sequential pipelines gave way to dynamic delegation to subagents with isolated contexts. Error correction within a trajectory used to rely on external critic models; now it is built into the chain of thought. Context grew from standard windows to 256K natively, scalable to 512K with YaRN.

## How to use this

1. Download the weights from the InternScience/Sage-A1.5 repository on Hugging Face or ModelScope.
  — <https://huggingface.co/InternScience/Sage-A1.5>
2. Deploy with vLLM or SGLang using the standard Qwen MoE configuration, so it exposes an OpenAI-compatible API endpoint.
  — <https://huggingface.co/InternScience/Sage-A1.5>
3. Enable subagent spawning in the agent runtime, so the model can split sub-tasks across isolated contexts in parallel.
  — <https://huggingface.co/InternScience/Sage-A1.5>
4. Turn on native verification in the generation parameters or the system prompt, so the model reviews itself and recovers from errors on long trajectories.
  — <https://huggingface.co/InternScience/Sage-A1.5>

## Best practices

- Give parallel investigative branches their own subagent contexts, so noisy intermediate tool output does not distract the root agent.
  — <https://huggingface.co/InternScience/Sage-A1.5>
- Apply YaRN scaling when a repository or a set of papers exceeds the native 256K-token window.
  — <https://huggingface.co/InternScience/Sage-A1.5>
- Serve FP8/INT4 quantizations with SGLang or vLLM to cut memory use while keeping MoE routing efficient.
  — <https://huggingface.co/InternScience/Sage-A1.5>

## Superseded by this

- Agents-A1 dense architectures and single-agent sequential pipelines are superseded by the Sage-A1.5 MoE architecture with native subagent orchestration.
  — <https://huggingface.co/InternScience/Sage-A1.5>
- External critic models for trajectory self-correction are superseded by Sage-A1.5's built-in chain-of-thought verification.
  — <https://huggingface.co/InternScience/Sage-A1.5>

## Still unknown

- Community reception and practical bug reports from practitioner forums could not be checked: search results led only to redirect pages.
- Memory bandwidth needs and performance on different domestic hardware accelerators have not been benchmarked independently yet.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/InternScience/Sage-A1.5 | InternScience/Sage-A1.5 · Hugging Face | 2026-10-23 |

## Agent brief {#agent-brief}

- **Subject:** project:sage-a1-5, thread sage-a1-5-release, 2 dated events 2026-10-22 → 2026-10-22.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
