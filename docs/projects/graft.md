---
title: "Graft: graft-execution-guided-agent-design — Graft Execution Guided Agent Design"
category: "projects"
date: 2026-11-20
tags: ["graft", "graft-execution-guided-agent-design", "project"]
aliases: ["Graft: graft-execution-guided-agent-design"]
---

# Graft: graft-execution-guided-agent-design — Graft Execution Guided Agent Design

**Development line:** project:graft · thread graft-execution-guided-agent-design  
**Last event:** 2026-11-20 · 1 dated since 2026-11-20 · **Researched:** 2026-11-21 · confidence: medium

## What it is

GRAFT is an agent design framework for ML researchers and agent developers, an alternative to standard evolutionary search and prompt-based meta-agents.

- Guided crossover: semantic crossover and integrated mutation use each parent's execution traces, not scalar fitness scores alone.
- Trace reuse: execution samples come from bounded evaluation runs, with no ground-truth labels exposed and no added inference overhead.
- Recombination: prompt patterns, task decomposition routines and multi-agent coordination architectures are mixed across open-weight models.

Limits: it was evaluated only on bounded reasoning and programming benchmarks with open-weight models. It needs deterministic execution feedback to build parent traces. On algorithmic benchmarks, concrete success and failure traces gave a better signal for recombination than unguided crossover.

## Development line

- **2026-11-20 — GRAFT: execution-guided genetic recombination for LLM agent design.** On 2026-11-20 an arXiv preprint (arXiv:2611.23509) introduced GRAFT. It uses parent-specific execution evidence from bounded run samples to guide semantic crossover and mutation in evolutionary search for LLM agent architectures. The authors report a mean test accuracy of 82.0% across six reasoning and programming settings, 9.8 points above the strongest baseline. Ablations show that execution evidence improves accuracy under fixed conditions.
  - The authors are Sevda Ebrahimi, Mohammed Saidul Islam, Xiaodan Zhu and Elham Dolatabadi. Their paper is titled Execution-Guided Genetic Recombination for Agent Design. Aggregate fitness still drives selection and survival. Bounded execution traces, both successes and failures from parent evaluation runs, go straight into the crossover and mutation prompts. No ground-truth labels leak, and no extra model runs happen during recombination. Tested on six programming and reasoning benchmarks with open-weight foundation models, it reached 82.0% mean accuracy, 9.8 percentage points above the strongest baseline. (2026-11-17) — <https://arxiv.org/abs/2611.23509>

## What changed

Earlier evolutionary agent design systems ranked and selected candidate architectures by aggregate scalar scores only. They discarded the intermediate run histories. GRAFT puts parent run traces into the crossover prompts, so partial problem-solving mechanisms survive across generations.

## How to use this

1. Define the candidate agent search space: allowed prompt templates, decomposition steps and coordination protocols for the target tasks.
  — <https://arxiv.org/abs/2611.23509>
2. Run the parent architectures on the evaluation benchmarks. Collect scalar scores and sample execution logs of successes and failures.
  — <https://arxiv.org/abs/2611.23509>
3. Select parents by aggregate fitness. Then build recombination prompts that show each parent's code next to its bounded execution traces.
  — <https://arxiv.org/abs/2611.23509>
4. Prompt the recombination LLM to write offspring designs. They keep the behaviors that succeeded and mutate the parts that failed, without showing gold answers.
  — <https://arxiv.org/abs/2611.23509>

## Best practices

- Reuse the traces from the normal fitness evaluations, and skip auxiliary inference runs, so search compute stays bounded.
  — <https://arxiv.org/abs/2611.23509>
- Keep intermediate traces and ground-truth labels apart in crossover prompts, so the search does not overfit the benchmark or leak test data.
  — <https://arxiv.org/abs/2611.23509>
- Keep aggregate fitness for top-level tournament selection. Limit execution-guided feedback to the crossover and mutation operators.
  — <https://arxiv.org/abs/2611.23509>

## Superseded by this

- Evolutionary agent architecture search that uses only aggregate scalar fitness to direct genetic recombination and LLM crossover.
  — <https://arxiv.org/abs/2611.23509>

## Still unknown

- Whether GRAFT has an official public code repository or packaged release. The preprint abstract and search metadata do not name one.
- Independent discussion, benchmarks or replication reports on developer forums (e.g. GitHub issues, Reddit, Hacker News) have not appeared yet.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2611.23509 | GRAFT: Execution-Guided Genetic Recombination for Agent Design | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** project:graft, thread graft-execution-guided-agent-design, 1 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** the usage and practice sections above carry the sources and the limits.
- **Confidence:** medium. The dated supersedes above say what is obsolete.
