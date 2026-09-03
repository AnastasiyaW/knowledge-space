---
title: "Coding-Agent Harness Patterns"
description: "A practical boundary between instructions, tools, deterministic gates, review, and durable evidence for coding-agent work."
tags: [coding-agents, harness, hooks, skills, testing, verification]
---

# Coding-Agent Harness Patterns

**Scope checked: 2026-09-03.** A harness is the operating environment around a coding agent. Its job is not to make an agent sound disciplined; it makes the intended workflow inspectable and lets deterministic checks reject an invalid change.

This guide avoids claimed universal speedups, product rankings, and hard-coded third-party tool recommendations. Measure a harness in its own repository against a declared delivery criterion.

## Five Boundaries

| Boundary | Owns | Must not own |
|---|---|---|
| task contract | acceptance criteria, scope, authority | hidden implementation decisions |
| instructions | project conventions and routing | a substitute for executable policy |
| tools and skills | repeatable domain workflows | final approval of their own output |
| deterministic gates | build, tests, schema, formatting, link checks | judgment about unstated product intent |
| independent review | semantic and release risk | an unbounded rewrite of a settled task |

When a layer cannot be inspected, invoked, or verified by the agent, it is not an operational control.

## Start With a Delivery Contract

Write acceptance criteria before editing:

1. name the paths or external behavior in scope;
2. state the exact verification command or observable receipt;
3. list irreversible or approval-gated actions;
4. identify the owner of each mutable resource;
5. name the required reviewer when self-review is insufficient.

Keep task state in a durable artifact, not only in chat history. A concise manifest can track `PENDING`, `RUNNING`, `PASS`, and `BLOCKED` plus the receipt that justifies a terminal state.

## Instructions Are Scoped Configuration

Current Claude Code distinguishes shared project settings, project-local settings, user settings, and managed policy. Put team-safe, versioned configuration in shared project scope; keep personal overrides and credentials out of the repository. `/status` reports the sources the active session loaded. [Claude Code settings](https://code.claude.com/docs/en/settings)

Project instructions should answer only questions that cannot be derived cheaply from code:

- where authoritative architecture and deployment documentation live;
- how to run required checks;
- protected files, secrets boundaries, and approval rules;
- the expected handoff and review artifacts.

Do not turn an instruction file into a changelog or a prompt dump. Point to durable documents for detailed knowledge.

## Deterministic Controls Come Before Model Judgment

Run inexpensive mechanical checks directly:

| Change risk | Example control | Evidence |
|---|---|---|
| syntax or format | formatter, parser, type checker | process exit and report |
| changed contract | targeted test or schema validation | assertion output |
| documentation | link and frontmatter checks | lint receipt |
| release artifact | build or package verification | immutable artifact reference |
| risky behavior | integration or user-visible test | trace, screenshot, or service receipt |

An LLM can interpret a failing report and propose a correction. It must not convert a failed check into a pass by explanation alone.

## Hooks and Skills Have Different Roles

Claude Code supports hooks around lifecycle and tool events, and custom subagents can carry focused context and tool permissions. These are integration surfaces, not proof that a workflow was followed. [Hooks reference](https://code.claude.com/docs/en/hooks) [Custom subagents](https://code.claude.com/docs/en/sub-agents)

| Mechanism | Good use | Required guard |
|---|---|---|
| skill | domain procedure or reusable checklist | trigger conditions and a runnable verification |
| hook | record an event or block a prohibited action | stable input/output and fail-closed release behavior |
| subagent | bounded exploration or independent review | file ownership, no self-certification, clear return format |
| script | deterministic inventory or validation | versioned source, exit status, retained report |

Do not make an untrusted tool result executable authority. Parse, validate, and route it through the same approval boundary as any other input.

## A Minimal Change Loop

```text
freeze acceptance criteria
        ↓
inspect code and relevant documentation
        ↓
make the smallest coherent change
        ↓
run the named deterministic checks
        ↓
collect receipts and inspect the diff
        ↓
independent review for material risk
        ↓
publish only after every required gate passes
```

The loop becomes useful when every arrow has a durable artifact. A status message without a test output, diff, or runtime receipt is not evidence.

## Worktree and Reviewer Isolation

Use a separate Git worktree when concurrent work would otherwise share a mutable checkout. Git documents linked worktrees as separate working trees attached to one repository, allowing more than one branch to be checked out at a time. [git-worktree](https://git-scm.com/docs/git-worktree)

For a material public change, the reviewer should read the final diff independently and return either `PASS` or a concrete finding with file, line, impact, and minimal fix. The author applies fixes; the reviewer does not silently certify a changed implementation from memory.

## Measure Locally, Not by Marketing

If a team wants to compare harness variants, define:

- fixed task corpus and repository revisions;
- same model, permissions, and tool availability;
- a primary quality metric such as accepted tests or reviewer findings;
- cost and elapsed-time capture;
- a rule for keeping, reverting, or repeating an experiment.

Without that design, a reported percentage is anecdote rather than an engineering result.

## Gotchas

- **A skill says to run a check, but no script exists.** The rule is not enforceable. **Fix:** add or reference the smallest runnable check before treating it as a gate.
- **A hook has broad write authority.** It can become a hidden deployment path. **Fix:** keep hooks narrow, logged, and unable to bypass normal release approval.
- **The same agent writes and approves a risky change.** It has the same blind spots in both roles. **Fix:** require a fresh reviewer or deterministic external check.
- **A test suite passes after the task changed shape.** It may not test the requested behavior. **Fix:** map each acceptance criterion to its own evidence.
- **Parallel agents share a checkout.** File races erase intent. **Fix:** use worktrees or explicit ownership boundaries before editing.

## Sources

- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Git worktrees](https://git-scm.com/docs/git-worktree)

## See Also

- [[agent-design-patterns]]
- [[agent-orchestration]]
- [[multi-session-coordination]]
- [[handoff-rollup-pattern]]
- [[production-patterns]]
