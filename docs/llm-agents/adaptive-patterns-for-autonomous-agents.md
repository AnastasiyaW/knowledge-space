---
title: "Adaptive Patterns for Autonomous Agents"
description: "Use explicit task state, bounded hooks, capability-scoped subagents, and evidence-based gates instead of opaque keyword triggers or arbitrary ambiguity scores."
tags: [agents, orchestration, hooks, subagents, task-state, verification]
---

# Adaptive Patterns for Autonomous Agents

**Scope checked: 2026-09-04.** An adaptive agent system should change behavior because an observable condition and a declared policy require it, not because a vague keyword or a model guess happened to fire. Current Claude Code extension points provide skills, hooks, subagents, agent teams, and plugins; they do not make arbitrary automation safe by default. [Extension overview](https://code.claude.com/docs/en/features-overview) [Hooks guide](https://code.claude.com/docs/en/hooks-guide)

## Match the Mechanism to the Need

| Need | Smallest useful mechanism | Evidence of success |
|---|---|---|
| recurring project constraints | committed instruction or rule file | a task follows the declared invariant |
| reusable procedure | skill with a narrow trigger | the procedure produces its expected artifact |
| deterministic pre/post condition | command hook | exit status or structured receipt |
| focused side task | capability-scoped subagent | bounded result plus source/test evidence |
| parallel independent work | agent team or isolated worktree | no shared-state collision and joined review |
| long-running delivery | durable task record | each item reaches a terminal receipt |

Do not introduce a hook merely because a behavior might be useful. A lifecycle hook is appropriate when the trigger, allowed action, output, failure signal, and owner are all known.

## Prefer Declared Activation Over Keyword Guessing

Claude Code can load skills when relevant and can run hooks for lifecycle events such as UserPromptSubmit, PreToolUse, PostToolUse, and SubagentStop. A hook can run a command, HTTP request, MCP tool, prompt, or agentic verifier. Command hooks are the stable choice for deterministic enforcement; agent hooks are documented as experimental. [Hooks reference](https://code.claude.com/docs/en/hooks) [Agent-based hooks](https://code.claude.com/docs/en/hooks-guide)

Use a small policy table instead of a regex that silently changes permissions:

```json
{
  "event": "PreToolUse",
  "condition": "requested action writes to a production target",
  "action": "require approved change record",
  "on_unknown": "block with a visible reason",
  "receipt": "change-record id and tool outcome"
}
```

Keyword matching may be useful only for non-mutating context selection. It must never grant credentials, choose a tenant, expand tool access, or initiate an external side effect by itself.

## Use Questions as a Risk Gate, Not a Score Ritual

An arbitrary threshold such as “20% ambiguity” is neither a safety proof nor a product requirement. Ask for clarification when an answer is necessary to choose an irreversible target, interpret an authorization boundary, or define the acceptance criterion. Otherwise execute the next reversible, in-scope action and report the evidence.

| Observation | Safe response |
|---|---|
| target or delete scope is unknown | stop before mutation and request the exact target |
| user intent is clear but implementation has choices | select the smallest reversible implementation and verify it |
| test/receipt is missing | create or run the task's real validation before declaring success |
| source claim is time-sensitive | retrieve the primary documentation and date the result |
| subtask would overload the main context | delegate it with explicit tools, scope, and expected receipt |

This avoids both silent guessing and an endless interview loop.

## Durable Task State

Conversation history is not a reliable transaction log. Keep work items in a repository-visible record with a stable id, source revision, owner, terminal status, and evidence reference:

```json
{
  "task_id": "DOC-042",
  "source_revision": "immutable-git-sha",
  "status": "RUNNING",
  "acceptance": ["strict build passes", "fresh review passes"],
  "attempt": 1,
  "idempotency_key": "docs:la051-055:revision",
  "evidence": ["reports/doc-042/links.txt"],
  "next_recheck": "named command or external event"
}
```

Valid state transitions should be explicit, for example PENDING to RUNNING to PASS, BLOCKED_EXTERNAL, or FAILED_RETRYABLE. A green-looking chat message is not a terminal state without the named receipt.

## Couple State to the Actual Workspace

Record the Git revision, worktree, and validation command that produced a result. If a branch changes, a previous pass may no longer apply. For parallel changes:

1. give each writer an isolated worktree or exclusive ownership of files;
2. keep shared mutable resources behind a visible lock and external health check;
3. reserve external IDs or URLs before work begins when duplicates are harmful;
4. re-run the causal validation after an integration or rebase;
5. use a fresh reviewer for material public, security, or release work.

Subagents are useful because each gets an independent context, custom instructions, and scoped tools. They do not replace a merge gate or make their own conclusions authoritative. [Subagents](https://code.claude.com/docs/en/subagents)

## Memory Is a Publishable Input

Keep operational knowledge navigable:

- index durable project decisions and current state;
- attach claims to source revisions, logs, tests, or external receipts;
- distinguish a dated observation from a reusable rule;
- make stale records visible rather than silently treating them as current;
- validate links and ownership of documents that automation will rely on.

An agent cannot safely act on information it cannot retrieve and validate through its available tools.

## Gotchas

- **A keyword activates a powerful tool.** Natural language is ambiguous and can be attacker-controlled. **Fix:** use keywords only for non-mutating routing; make permissions and external effects explicit.
- **A prompt hook calls an LLM to decide an invariant.** The result can vary and be hard to audit. **Fix:** use deterministic hooks for hard policy; keep model judgment advisory.
- **A task file says done after a partial run.** A process may have stopped before the final side effect. **Fix:** require a terminal receipt that proves the requested outcome.
- **A subagent reports a clean review of its own output.** That is not independent verification. **Fix:** use a separate fresh reviewer for material work.
- **A stale lock is reclaimed on its timestamp alone.** The original process may still own the resource. **Fix:** check the actual process or external service before reclaiming it.

## Sources

- [Claude Code extension overview](https://code.claude.com/docs/en/features-overview)
- [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
- [Claude Code subagents](https://code.claude.com/docs/en/subagents)

## See Also

- [[agent-design-patterns]]
- [[context-engineering]]
- [[agent-memory]]
- [[agent-orchestration]]
