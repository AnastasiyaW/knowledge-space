---
title: "Autonomous Agent Evolution"
description: "Run parallel agent experiments safely with isolated worktrees, append-only evidence, resource locks, and independent evaluation"
---

# Autonomous Agent Evolution (September 2026)

Version context: this page describes a controlled experiment architecture, not a claim that autonomous agents should modify production systems. Pin the repository revision, evaluator, task manifest, environment image, and resource policy for every run.

Parallel agents can explore independent candidate changes, but only when the work has a measurable objective, isolated mutation space, and a promotion path that rejects unsupported results.

## Admission Gate

Do not launch a parallel evolution run until all conditions hold:

1. A task manifest enumerates every candidate unit of work.
2. A deterministic or independently reviewable evaluator exists.
3. Each worker has an isolated branch/worktree or sandbox.
4. Shared mutable resources have explicit locks and external verification.
5. Output artifacts have stable IDs, digests, and retention policy.
6. A coordinator owns promotion, rollback, and terminal accounting.

Without these conditions, parallel agents create concurrent edits and unverified narratives rather than evidence.

## Isolation Model

Git worktrees permit multiple checked-out branches of one repository. They isolate file changes by branch, but they do not isolate processes, network access, credentials, mounted drives, or cloud resources.

```text
coordinator
  ├── worker-a: worktree + branch + task shard
  ├── worker-b: worktree + branch + task shard
  └── evaluator: fresh context, read-only evidence review
shared: append-only receipts + explicit resource locks
```

Use environment-level controls when workers must not share secrets, GPU capacity, ports, databases, or external-service credentials.

## Manifest-Backed Work

```json
{
  "run_id": "evolution-2026-09-03",
  "baseline_commit": "abc123",
  "evaluator_revision": "git:eval456",
  "objective": "accepted_task_rate",
  "guard_metrics": {"policy_violations_max": 0},
  "shards": [
    {"id": "A", "state": "pending", "owner": null},
    {"id": "B", "state": "pending", "owner": null}
  ],
  "promotion_state": "hold"
}
```

A shard is complete only after it has a terminal evaluation receipt. A worker process, branch, or progress message is not proof of completion.

## Worker Protocol

For each assigned shard:

1. Check that the shard is still `pending` under the manifest lock.
2. Create or claim an isolated worktree/branch from the recorded baseline.
3. Apply one bounded candidate change.
4. Run the named evaluator and preserve raw result, digest, environment, and commit ID.
5. Mark the shard `passed`, `rejected`, or `blocked_external` with a reason.
6. Send only evidence references to the coordinator; never promote directly to the baseline.

A worker should not reuse an attempted task without reconciling the prior receipt and idempotency key.

## Shared Knowledge Without Races

Keep shared information in two categories:

| State | Safe representation | Rule |
|---|---|---|
| Evidence, observations, receipts | Per-run append-only files | Never rewrite another worker's record |
| Locks, reservations, current winner | One resource-specific file | Claim atomically; check external state before recovery |

Example receipt:

```json
{
  "shard_id": "A",
  "candidate_commit": "def456",
  "parent_commit": "abc123",
  "evaluator_digest": "sha256:...",
  "primary_metric": 0.0,
  "guards": {"policy_violations": 0},
  "verdict": "rejected",
  "recorded_at": "2026-09-03T18:00:00Z"
}
```

Observations are helpful but are not shared instructions. Treat agent-authored notes as untrusted hypotheses until the referenced evaluator or source confirms them.

## Selection and Promotion

The coordinator compares only receipts produced by the same evaluator revision and comparable environment. A candidate wins only when it improves the primary objective and passes every guard.

```text
candidate receipt -> independent evaluator -> selection record
                  -> integration test -> staged/canary evidence -> promotion
```

Use a fresh evaluator context for final acceptance. The worker that made a change cannot certify its own semantic correctness.

## Resource Locks

Git is not a lock manager for GPUs, ports, databases, remote queues, or external URLs. For each mutable resource, record owner, heartbeat, process ID or reservation ID, attempt budget, and recovery procedure.

Before reclaiming a stale lock, verify externally that the owner process or remote operation is no longer active. Do not infer that a resource is free from an old timestamp alone.

## Stagnation and Stop Conditions

Stop or redirect a run when:

- every shard has a terminal receipt;
- the evaluator is invalid or unavailable;
- repeated candidates regress under the same measurement;
- a resource/security guard is triggered;
- the configured attempt/cost/time budget is reached.

Changing the metric after a plateau is a new experiment, not a continuation. Preserve rejected evidence so future workers do not repeat the same failed candidate.

## Gotchas

- **Worktrees are not full isolation.** They share the host's processes, credentials, and mounted resources. **Fix:** add environment-level isolation and per-resource locks where needed.
- **Parallel progress messages can hide duplicate work.** Two workers may evaluate the same candidate. **Fix:** reserve shards in a manifest with an idempotency key and receipt check.
- **Shared notes can spread a false hypothesis.** An agent's summary may be wrong or stale. **Fix:** link every reusable observation to an evaluator receipt or primary source.
- **A higher score can be an invalid comparison.** Different environment, seed, data, or evaluator revision changes the experiment. **Fix:** compare only compatible receipts and record all material inputs.
- **Automatic promotion is an authority escalation.** A passing worker test does not authorize production mutation. **Fix:** require independent evaluation, integration evidence, and a defined release owner.

## Sources

- [Git worktree documentation](https://git-scm.com/docs/git-worktree)
- [OpenAI API: working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI Agents SDK: agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [OpenAI Agents SDK: tracing](https://openai.github.io/openai-agents-python/tracing/)

## See Also

- [[agent-self-improvement]]
- [[agent-evaluation]]
- [[multi-agent-systems]]
- [[agent-architectures]]
- [[production-patterns]]
