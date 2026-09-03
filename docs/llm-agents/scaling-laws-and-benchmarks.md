---
title: "LLM Scaling Laws and Benchmarks"
description: "Use scaling-law research and benchmark suites without turning historical fits or leaderboard snapshots into product decisions"
---

# LLM Scaling Laws and Benchmarks (September 2026)

Version context: scaling-law fits and benchmark scores are empirical results under stated datasets, compute budgets, architectures, prompts, and evaluation harnesses. They are not universal sizing rules or durable model rankings.

## What Scaling Laws Answer

Scaling-law research studies how a measured loss or capability changes as training compute, model size, data, and related variables increase. It is useful for:

- planning a controlled pretraining or continued-pretraining program;
- selecting which costly experiments to run next;
- detecting obviously under-trained candidate configurations;
- framing a compute/data trade-off within a fixed methodology.

It does not by itself choose a production model, prove downstream safety, or predict latency and cost under a real serving workload.

The Chinchilla study reported that, for its compute-optimal setting, model size and training tokens should scale proportionally. That result is a historical fit to a particular experimental regime. Use it as a `tokens-per-parameter` procurement rule only after validating it on the actual architecture, data, and objective.

## Separate Three Decisions

| Decision | Evidence that decides it |
|---|---|
| Pretraining allocation | Controlled loss/capability experiments, compute and data provenance |
| Serving design | Measured latency, throughput, memory, availability, and unit cost |
| Product acceptance | Frozen task suite, safety checks, and user-relevant error review |

Mixing these leads to false conclusions: a larger model can be a worse product choice if it fails the target workflow, misses an SLO, or cannot be operated safely.

## Benchmark Inventory

A benchmark is useful only when its task, version, prompt, scoring method, and contamination risk are known.

| Category | Example use | Release question |
|---|---|---|
| Broad knowledge/reasoning | MMLU-like suite | Does the candidate regress on general capability relevant to the product? |
| Domain task set | Internal labeled corpus | Does it solve the actual work correctly? |
| Robustness / adversarial set | Prompt injection, refusal, malformed input | Does it fail safely? |
| Tool-use evaluation | Recorded tool contracts | Does it select permitted actions and respect schemas? |
| Operations test | Load and fault exercise | Can it meet latency, error, and cost bounds? |

MMLU is a widely cited academic benchmark, but a single aggregate score is not evidence that an agent is reliable on an organization's task. Keep benchmark results as diagnostic signals alongside product-specific evaluation.

## Evaluation Record

Every comparison needs an immutable receipt. This prevents a leaderboard number from losing the settings that produced it.

```json
{
  "evaluation_id": "support-routing-2026-09-03",
  "candidate": {"model": "candidate-id", "revision": "immutable-revision"},
  "baseline": {"model": "baseline-id", "revision": "immutable-revision"},
  "suite": {"name": "support-routing-v4", "digest": "sha256:..."},
  "harness": {"commit": "git-sha", "prompt_policy": "prompt-v7"},
  "metrics": {
    "route_accuracy": 0.0,
    "schema_valid_rate": 0.0,
    "p95_latency_ms": 0,
    "cost_per_accepted_output": 0.0
  },
  "verdict": "hold"
}
```

Use the same input set, decoding policy, tool availability, and scoring method for baseline and candidate. If any changes, start a new comparison rather than merging numbers.

## Contamination and Reproducibility

Public benchmarks may be present in pretraining or instruction-tuning data. A high score can indicate memorization, prompt sensitivity, or test-specific optimization instead of transferable performance.

Mitigations:

1. Track the benchmark revision and source license.
2. Keep a private, newly collected task suite that is never used for tuning.
3. Rotate hidden cases while preserving stable regression cases.
4. Record prompts, random seeds, sampling parameters, and tool policy.
5. Manually inspect representative successes and failures.

## Model Selection Procedure

1. Define an acceptance contract: outcome quality, safety, latency, availability, and budget.
2. Establish a baseline with the deployed prompt/tool policy.
3. Test a small set of candidate tiers on the same frozen suite.
4. Review error slices, not just the average.
5. Select the least costly candidate that meets every required threshold.
6. Preserve the receipt and schedule a re-evaluation when model, prompts, tools, or corpus change.

## Gotchas

- **A scaling-law coefficient is not a deployment parameter.** It was estimated under specific assumptions. **Fix:** use it to choose experiments, then measure the workload that will actually be served.
- **Aggregate scores hide unacceptable slices.** A model can improve an average while failing a regulated language, difficult cohort, or safety condition. **Fix:** set explicit per-slice release thresholds.
- **Leaderboard snapshots drift.** Harnesses, prompts, datasets, and model revisions change. **Fix:** publish the complete evaluation receipt instead of an uncited score.
- **Benchmark success does not prove tool safety.** Multiple-choice accuracy cannot verify side effects, permissions, or retries. **Fix:** test recorded tool contracts and adversarial operational scenarios separately.

## Sources

- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
- [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)
- [Measuring Massive Multitask Language Understanding](https://arxiv.org/abs/2009.03300)
- [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)

## See Also

- [[frontier-models]]
- [[model-optimization]]
- [[agent-evaluation]]
- [[llm-fine-tuning-practical]]
