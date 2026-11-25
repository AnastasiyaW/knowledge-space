---
title: "Sampling Is Not Curiosity Llm Agents: sampling-is-not-curiosity-llm-agents-curiosity-requirements — Sampling Is Not Curiosity Llm Agents Curiosity Requirements"
category: "projects"
date: 2026-11-20
tags: ["project", "sampling-is-not-curiosity-llm-agents", "sampling-is-not-curiosity-llm-agents-curiosity-requirements"]
aliases: ["Sampling Is Not Curiosity Llm Agents: sampling-is-not-curiosity-llm-agents-curiosity-requirements"]
---

# Sampling Is Not Curiosity Llm Agents: sampling-is-not-curiosity-llm-agents-curiosity-requirements — Sampling Is Not Curiosity Llm Agents Curiosity Requirements

Sampling Is Not Curiosity is a framework of five requirements for curiosity in LLM agents, set against temperature scaling and best-of-N.

**Development line:** project:sampling-is-not-curiosity-llm-agents · thread sampling-is-not-curiosity-llm-agents-curiosity-requirements  
**Last event:** 2026-11-20 · 1 dated since 2026-11-20 · **Researched:** 2026-11-21 · confidence: high

## What it is

It is an agent architecture framework for builders of autonomous language model agents. It lists what an agent needs to explore on its own. It contrasts that with stochastic sampling, such as temperature scaling and best-of-N selection.

The framework names five capabilities:

- Predictive world model: estimates how the environment changes after each agent action
- Online updating: the model learns from feedback during continuous interaction
- Action selection: picks actions by how much they are expected to improve the model
- State persistence: keeps state beyond the context window
- Autonomous goal formulation: the agent sets its own questions, with no external prompt steering

Current search, memory and automated discovery agents miss up to four of the five criteria. None of them has both autonomous goal formulation and persistent model updating. More sampling diversity at inference time is not curiosity unless the agent also keeps an evolving, persistent model of its environment.

## Development line

- **2026-11-20 — Position paper proposes architectural requirements for curiosity in LLM agents.** A position paper by Amayuelas, Piękos, Wang, Wang, Schmidhuber and Pentland makes one argument. Sampling or prompt variation in frozen language models only diversifies actions. Real curiosity needs a predictive world model, action selection that improves it, and updates that persist beyond the context window. The authors set out five architectural requirements. Popular search, memory and scientific-discovery agents do not meet them. Only architectures with explicit hypothesis tracking or a learned world model satisfy four of the requirements.
  - The paper is titled 'Sampling Is Not Curiosity: Why LLM Agents Should Investigate' and is accepted to NeurIPS 2026. It formalizes five requirements adapted from reinforcement learning: predictive world models, online parameter updates, intrinsic reward from expected model improvement, persistent memory beyond context windows, and autonomous goal formulation. (2026-11-20) — <https://arxiv.org/abs/2611.10501>
  - The analysis covers temperature variations, best-of-N sampling, Monte Carlo Tree Search and RAG. Each one only re-samples or conditions a static token distribution. None updates the agent's internal world representation. (2026-11-20) — <https://arxiviq.substack.com/p/sampling-is-not-curiosity-why-llm>

## What changed

Criteria for artificial curiosity moved from reinforcement learning theory to language model agent benchmarks. The first evaluations tested stochastic sampling, prompt perturbation and retrieval pipelines against formal curiosity criteria. Later analyses benchmarked existing automated discovery agents. Architectures without persistent state updates and a predictive world model did not reach real exploration.

## How to use this

1. Audit each candidate agent against the five criteria, so it is clear whether exploration comes from stochastic sampling or from active world model updates.
  — <https://arxiv.org/abs/2611.10501>
2. Give the agent an explicit predictive structure that models environment transitions, so it does not rely only on next-token probabilities.
  — <https://arxiv.org/abs/2611.10501>
3. Add online updates and persistent external memory, so learned feedback survives beyond the context window.
  — <https://arxiv.org/abs/2611.10501>

## Best practices

- Do not treat temperature adjustments, best-of-N reranking or retrieval-augmented generation as curiosity mechanisms. They leave the agent's internal environment model unchanged.
  — <https://arxiviq.substack.com/p/sampling-is-not-curiosity-why-llm>
- Choose exploratory actions by expected model improvement and prediction error reduction, not by random sampling over frozen model weights.
  — <https://arxiv.org/abs/2611.10501>

## What practitioners say

- Stochastic sampling gives autonomous research agents an illusion of exploration. Real discovery needs hypotheses that are kept and updated across execution steps. (2026-11-20)
  — <https://arxiviq.substack.com/p/sampling-is-not-curiosity-why-llm>

## Superseded by this

- The view that temperature scaling, prompt perturbation and stochastic sampling are enough for curiosity and exploration in autonomous agents.
  — <https://arxiv.org/abs/2611.10501>

## Still unknown

- Whether any widely adopted open-source autonomous research agent implements all five requirements end-to-end without auxiliary fine-tuning overhead.
- Performance differences across individual benchmark domains: the available summaries do not itemize them in full.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2611.10501 | Sampling Is Not Curiosity: Why LLM Agents Should Investigate | 2026-11-21 |
| https://arxiviq.substack.com/p/sampling-is-not-curiosity-why-llm | Sampling Is Not Curiosity: Why LLM Agents Should Investigate - ArxivIQ | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** project:sampling-is-not-curiosity-llm-agents, thread sampling-is-not-curiosity-llm-agents-curiosity-requirements, 1 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** the usage and practice sections above carry the sources and their limits.
- **Confidence:** high. The dated entries under "Superseded by this" say what is obsolete.
