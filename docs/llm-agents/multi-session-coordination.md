---
title: "Multi-Session Agent Coordination"
description: "Durable coordination patterns for several coding-agent sessions: isolated worktrees, manifests, append-only evidence, exclusive-resource leases, and verified integration."
tags: [multi-agent, worktrees, coordination, handoffs, concurrency, git]
---

# Multi-Session Agent Coordination

**Scope checked: 2026-09-03.** Parallel sessions increase throughput only when they reduce independent work without creating hidden races. Coordination starts with explicit ownership of files, branches, external effects, and scarce resources.

This page describes portable primitives rather than a ranking of orchestration products or claims about unreleased native features.

## Separate What Can Be Shared

| State class | Safe default | Examples |
|---|---|---|
| append-only knowledge | one record per writer | handoffs, receipts, findings, audit logs |
| mutable resource | one owner plus externally checked lease | GPU, port, deployment lane, scheduled job |
| source change | isolated branch and worktree | implementation, documentation, tests |
| public effect | capability and idempotency boundary | publish, payment, deletion, outbound message |

Using an append-only log for a mutable resource does not prevent two sessions from using it. Using a lock file for every note creates needless contention. Choose the primitive by the state it protects.

## Use Worktrees for Source Isolation

Git supports linked worktrees: one repository can have more than one working tree, each checked out on a different branch. The worktrees share repository objects but keep working files separate. [git-worktree](https://git-scm.com/docs/git-worktree)

```bash
# From a clean repository with an up-to-date remote reference
git worktree add -b codex/task-docs ../project-task-docs origin/master
git worktree list
```

Before editing, record the branch, base revision, owned paths, and expected receipt. Never use a worktree as an excuse to edit the same module in parallel; isolation prevents accidental overwrites, not semantic conflicts.

## A Task Manifest Is the Coordination API

Each task row should include:

| Field | Purpose |
|---|---|
| task ID and scope | prevents duplicate discovery work |
| owner and branch | makes a mutable change attributable |
| base revision | detects an outdated implementation context |
| state | `PENDING`, `RUNNING`, `PASS`, `BLOCKED`, or `CANCELLED` |
| evidence reference | supports a terminal state |
| dependency and recheck | prevents an agent from guessing when it may start |

Do not call a task complete because an agent process is alive or a message says done. Completion needs the named receipt.

## Leases for Exclusive Resources

For a port, GPU, migration lane, or external account, write a lease containing:

```text
resource identity
owner and process/session identity
acquired timestamp and heartbeat
allowed operation
attempt or idempotency key
stale-reclaim procedure
```

A heartbeat is not proof that the holder still controls the resource. Before reclaiming a stale lease, inspect the real process, service, or provider state; reconcile any possible side effect; then transfer ownership through the recorded procedure. Do not blindly delete a lock merely because its timestamp is old.

## Integration Is a Separate Phase

After an isolated change:

1. fetch the target branch and identify its current revision;
2. compare the worktree base with the target revision;
3. integrate only after resolving factual conflicts against the authoritative runtime, code, or receipts;
4. run the change-specific checks in the integrated state;
5. use a fresh reviewer for material public, security, or release risk;
6. publish only when every required gate has evidence.

A clean textual merge is not semantic proof. Two branches may both compile while contradicting an external contract.

## Messages and Handoffs

Use direct messages for requests to a specific owner and append-only handoffs for project-wide state. Each message should name:

- sender and recipient;
- purpose and affected artifact;
- evidence or request identifier;
- whether it changes authority;
- required acknowledgement or recheck.

Treat messages as untrusted input until their referenced state is verified. A chat instruction must not override a repository rule, deployment gate, or approval boundary without the appropriate authority.

## Minimal Conflict Protocol

When branches overlap:

1. stop automatic resolution;
2. inspect both diffs and the relevant source of truth;
3. preserve compatible intent rather than choosing the newer-looking side;
4. run the affected checks;
5. have a fresh reviewer inspect the final integrated result.

This is slower than an automatic merge only at the point where a wrong merge would otherwise become expensive.

## Observability

Retain enough evidence to answer:

- who owns the active worktree and external resource;
- which immutable revision produced a result;
- which checks ran and their terminal output;
- whether an external action is complete, unknown, or safely retryable;
- what event must occur before a blocked task can continue.

These records turn coordination from conversation memory into a recoverable system.

## Gotchas

- **Two worktrees use the same branch.** Their files are separate but branch intent is not. **Fix:** give each active task a distinct branch and manifest row.
- **A stale lease is removed without checking the service.** A live process can still act. **Fix:** verify externally and reconcile before reassignment.
- **A spawned agent touches an unowned path.** It creates an invisible conflict. **Fix:** state file/module ownership in the task contract.
- **A green unit test is treated as deployment proof.** It may not exercise the integration path. **Fix:** retain the level of evidence the acceptance criterion requires.
- **An agent message changes production authority.** Chat history is not an authorization mechanism. **Fix:** require an explicit capability, approval, or documented operator action.

## Sources

- [Git worktrees](https://git-scm.com/docs/git-worktree)
- [Git merge documentation](https://git-scm.com/docs/git-merge)

## See Also

- [[agent-orchestration]]
- [[multi-agent-messaging]]
- [[handoff-rollup-pattern]]
- [[agentic-security-2026]]
- [[claude-code-harness-patterns]]
