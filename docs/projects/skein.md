---
title: "Skein: skein-agent-task-graph-tracker — Skein Agent Task Graph Tracker"
category: "projects"
date: 2026-11-21
tags: ["project", "skein", "skein-agent-task-graph-tracker"]
aliases: ["Skein: skein-agent-task-graph-tracker"]
---

# Skein: skein-agent-task-graph-tracker — Skein Agent Task Graph Tracker

Skein is an experimental coding agent runtime that edits its own context through event logs, instead of the append-only ReAct history.

**Development line:** project:skein · thread skein-agent-task-graph-tracker  
**Last event:** 2026-11-21 · 1 dated since 2026-11-21 · **Researched:** 2026-11-22 · confidence: medium

## What it is

Skein is an experimental runtime for software development agents. It runs tasks through structured event logs and non-monotonic context editing, not an append-only message history.

- Execution tracking: every step is recorded as an event.
- Context editing: messages are pruned and overwritten by program, so context does not only grow.
- Hypothesis states: the workflow is split into states, each built around one hypothesis.
- Tool scoping: only the tools needed for the active subtask are available.

It works on local event records and does not ask a language model to summarize. That prevents attention degradation and avoids the cost of a second model call.

## Development line

- **2026-11-21 — Skein: development agent with non-monotonic context.** A Habr article presents Skein, an experimental software development agent built on the ReAct architecture. Its context can shrink: new messages overwrite earlier ones, and the language model takes no part in that.
  - The technical analysis by mefrill covers the limits of standard ReAct context accumulation in agents like Claude Code and Cursor. It describes Skein's structured event logging, which allows programmatic context pruning and hypothesis state resets without LLM summarization. (2026-11-21) — <https://habr.com/ru/articles/1110628/>

## What changed

Agent context tracking moved from a linear chat history to structured event logs, so messages can be replaced by program. Workflow management was then refactored into separate hypothesis states, each with its own stopping criteria. Context can now be cleared between steps deterministically, with no language model involved.

## How to use this

1. Start agent execution with a structured event log. It records model outputs, tool calls and environment feedback.
  — <https://habr.com/ru/articles/1110628/>
2. Split complex development tasks into hypothesis states. Give each one an objective and a termination condition.
  — <https://habr.com/ru/articles/1110628/>
3. Apply pruning rules at each state transition, so intermediate tool outputs are dropped without LLM summarization.
  — <https://habr.com/ru/articles/1110628/>

## Best practices

- Group tool calls and verification steps into bounded hypothesis states, so history can be pruned deterministically.
  — <https://habr.com/ru/articles/1110628/>
- Prune the event log by rule, not by LLM summary, so compiler diagnostics and trace tokens stay verbatim.
  — <https://habr.com/ru/articles/1110628/>

## Superseded by this

- Monotonic append-only history in ReAct software engineering agents.
  — <https://habr.com/ru/articles/1110628/>
- Relying only on LLM summarization to compress context in coding agents.
  — <https://habr.com/ru/articles/1110628/>

## Still unknown

- Whether a public standalone repository exists, and what its release versions are, for the Skein SWE-agent tracker. Beyond the Habr article, this could not be checked in public code repositories.
- No independent community discussions, issue threads or third-party SWE-bench benchmarks turned up.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/articles/1110628/ | Skein: агент разработки с немонотонным контекстом | 2026-11-22 |

## Agent brief {#agent-brief}

- **Subject:** project:skein, thread skein-agent-task-graph-tracker, 1 dated events 2026-11-21 → 2026-11-21.
- **Practical note:** the usage and practice sections above are sourced, and their limits apply.
- **Confidence:** medium. The dated entries under "Superseded by this" say what is obsolete.
