---
title: "Agent Self-Improvement"
description: "A safe experiment loop for improving agent prompts, tools, code, and policies with frozen evaluations and rollback"
---

# Agent Self-Improvement (September 2026)

Version context: treat an improvement loop as an experimental system. Its metric, evaluation set, guard conditions, candidate revision, and rollback rule are versioned inputs; changing any of them starts a new experiment series.

An agent should not declare itself improved. Improvement is a measured comparison against a baseline on a held-out evaluation, with safety and operational guard checks.

## What May Improve

| Target | Safe initial method | Evidence required |
|---|---|---|
| Prompt/instructions | One scoped edit | Frozen task eval and output review |
| Tool descriptions/allowlist | Reduce or clarify the tool set | Tool-use correctness and denied-action tests |
| Retrieval policy | One retrieval/reranking change | Source-grounded answer and citation evaluation |
| Workflow code | Isolated branch/worktree change | Tests, build, independent review |
| Model selection/configuration | Compare candidates | Same suite, latency/cost/safety record |
| Long-term memory policy | Controlled sandbox trial | Poisoning, expiry, provenance, privacy tests |

Do not mutate production source, global tools, credentials, or memory based solely on model reflection. Use an isolated environment and promote only verified artifacts.

## Minimal Experiment Contract

```json
{
  "experiment_id": "agent-routing-2026-09-03-001",
  "baseline_revision": "git:abc123",
  "candidate_revision": "git:def456",
  "suite_digest": "sha256:...",
  "primary_metric": "accepted_task_rate",
  "guard_metrics": {
    "policy_violations_max": 0,
    "p95_latency_ms_max": 3000,
    "cost_per_task_max": 0.05
  },
  "decision": "pending"
}
```

A metric without a guard is vulnerable to optimization that damages safety, cost, latency, or reliability. A candidate without a fixed baseline and suite cannot prove a causal change.

## Keep/Reject Rule

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluation:
    primary: float
    policy_violations: int
    p95_latency_ms: int
    cost_per_task: float


def accept(
    baseline: Evaluation,
    candidate: Evaluation,
    *,
    latency_limit: int,
    cost_limit: float,
) -> bool:
    return (
        candidate.primary > baseline.primary
        and candidate.policy_violations == 0
        and candidate.p95_latency_ms <= latency_limit
        and candidate.cost_per_task <= cost_limit
    )
```

Real evaluation also needs confidence intervals or repeated runs when sampling variance is material. The conservative default is to reject ties and regressions.

## Controlled Improvement Loop

1. Freeze the acceptance criteria, test suite, and baseline receipt.
2. Generate or select one candidate change.
3. Apply it only in an isolated branch/worktree or sandbox.
4. Run deterministic tests plus the same agent evaluation suite.
5. Have an independent evaluator inspect the evidence and adverse cases.
6. Keep the candidate only if it improves the primary metric and passes every guard.
7. Preserve the rejected candidate and its receipt; do not silently overwrite history.

The core idea of agent-driven experimental projects such as autoresearch is useful only when the evaluation is real and the change scope is controlled. It is not a license for unbounded self-modification.

## Reflection and Trajectory Data

Model reflection can help generate hypotheses: a failed task may suggest missing tool context, an ambiguous prompt, a faulty parser, or an incomplete stop condition. It is not ground truth.

Store a structured failure record:

```json
{
  "task_id": "eval_431",
  "revision": "git:def456",
  "terminal_state": "failed",
  "evidence": ["tool receipt: timeout", "output schema: invalid"],
  "hypothesis": "retry policy is missing an eligible timeout branch",
  "review_state": "unverified"
}
```

Use the evidence to drive a testable candidate. Do not train on or promote model-authored explanations until their underlying facts are checked.

## Evaluation Design

A useful suite contains:

- representative normal tasks;
- difficult boundary and recovery tasks;
- malformed input and tool-result cases;
- policy denials and adversarial injection attempts;
- regression cases discovered in production;
- cost, latency, and retry measurements.

Keep a holdout set that no optimizer or prompt-tuning loop can inspect. Rotate new hidden examples into the holdout after each major release.

## Promotion Boundary

A candidate can progress through:

```text
sandbox experiment -> local validation -> independent review
                   -> staged/canary evaluation -> production release
```

Production feedback is evidence, but it is not authorization for a system to rewrite itself. All promotion remains bound to change control and rollback capability.

## Gotchas

- **The agent can optimize the metric instead of the outcome.** A narrow scorer can be gamed. **Fix:** use multiple guards, adversarial cases, and manual review of representative outputs.
- **Test leakage creates fake improvement.** Repeated optimization against the same visible set eventually overfits it. **Fix:** preserve a hidden holdout and treat it as release-only evidence.
- **Multiple edits destroy causality.** A better score cannot identify which change helped. **Fix:** change one scoped variable per experiment and retain the full receipt.
- **Model reflections may invent causes.** Plausible explanations are not diagnostics. **Fix:** link hypotheses to logs, receipts, or reproducible tests before editing.
- **A rollback without artifact integrity is not a rollback.** Mutable branches and overwritten files lose the last known good state. **Fix:** use immutable commit IDs and versioned evaluation records.

## Sources

- [OpenAI API: working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
- [Git worktree documentation](https://git-scm.com/docs/git-worktree)

## See Also

- [[agent-evaluation]]
- [[agent-design-patterns]]
- [[autonomous-agent-evolution]]
- [[production-patterns]]
- [[llm-fine-tuning-practical]]
