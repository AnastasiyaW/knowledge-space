---
title: "Context Engineering and Durable Task State"
description: "Treat model context as a bounded working input and preserve task state, evidence, authority, and retrieval provenance in versioned artifacts rather than fixed token allocations."
tags: [llm-agents, context-engineering, state, retrieval, compaction, evidence]
---

# Context Engineering and Durable Task State

**Scope checked: 2026-09-04.** Model context is a bounded input to one turn or run. It is not a durable database, an audit log, or a permission system. Context engineering is the discipline of selecting, validating, and refreshing the smallest information set that lets an agent complete a defined task safely.

## Separate the Information Planes

| Plane | Purpose | Source of truth |
|---|---|---|
| operating policy | repository rules, tool limits, and escalation | reviewed configuration and instruction files |
| task state | goal, acceptance criteria, current step, and blockers | versioned task artifact |
| evidence | test output, source citations, target receipts, and reviews | durable artifact with revision or timestamp |
| conversation transcript | dialogue continuity | session record, not the sole task record |
| retrieved material | task-relevant documents or data | cited source plus retrieval metadata |
| personal memory | user-approved preferences or facts | documented consent, retention, and deletion path |

Do not use a chat summary as the only copy of a decision, credential boundary, or deployment result. Claude Code's memory documentation distinguishes repository-level guidance from the transient session context that consumes it. [How Claude remembers your project](https://code.claude.com/docs/en/memory)

## Admit Context by Contract

Before placing material into a prompt, ask five questions:

1. **Relevance:** does it change the current task's next decision?
2. **Authority:** is this source allowed to influence the task, or is it untrusted input?
3. **Freshness:** can the claim have changed, and is the revision or retrieval time recorded?
4. **Sensitivity:** does the task truly need this data, and is the selected tool/provider approved for it?
5. **Evidence:** can a reviewer recover the original source instead of trusting the summary?

These checks are more durable than a universal percentage split between instructions, history, tools, and output. Context size, pricing, cache behavior, and model limits change by provider and model; measure them from the current target contract.

## Persist Task State Outside the Turn

For work that spans more than one turn, keep a small task directory or equivalent durable record.

```text
task/
  spec.md          frozen acceptance criteria and authority
  state.json       current phase, owner, attempt, and blocker
  sources.md       primary-source URLs and retrieval dates
  evidence/        test output, receipts, screenshots, or digests
  review.md        independent verdict and required fixes
```

The state record should identify the input revision and whether an external side effect is only planned, running, completed, or blocked. Append-only evidence is safer than repeatedly rewriting a shared summary; mutable coordination state needs a clear owner and conflict policy.

## Build Context in Layers

A practical context assembly order is:

1. load the operating policy and frozen task contract;
2. add the smallest source or code slice needed for the next decision;
3. retrieve additional material only against a named question;
4. label retrieved text with origin, revision/date, and trust level;
5. run allowed tools and save their receipts outside the prompt;
6. inject a compact state pointer or verified summary for the next turn.

This keeps volatile tool output from becoming permanent instruction. It also makes a context reset recoverable: the next agent reads the task artifacts rather than guessing what a previous conversation meant.

## Compaction Is Lossy

A summary can preserve an outcome, but it should disclose omitted detail and link back to the evidence it summarizes. Before compaction, persist facts that would be expensive or unsafe to rediscover: acceptance criteria, tested revisions, external side effects, unresolved conflicts, approvals, and source locations.

After compaction, reintroduce only the current task contract and pointers to durable evidence. Do not re-inject an ever-growing “master summary” that becomes an unreviewed authority source.

## Retrieval Is a Security Boundary

Retrieved repositories, tickets, web pages, and tool output may contain instructions written for humans or other systems. Treat them as data. They cannot authorize a tool, change a policy, request secrets, or override a higher-priority task contract.

For an agent that can call tools, record the retrieval query, selected source, extractor version if applicable, and document revision. This makes it possible to investigate a misleading answer or a prompt-injection attempt without preserving all raw content in every context window. [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)

## Evaluate the Context Strategy

Evaluate context changes with a fixed task set and a defined failure model:

| Question | Evidence |
|---|---|
| does the agent find the required authoritative source? | source citation and retrieval trace |
| does it preserve task constraints after compaction? | rerun or independent verifier against the same task artifact |
| does it avoid prohibited data/tool use? | permission and tool-call audit |
| does a shorter context preserve acceptance results? | comparable fixture and validator output |
| can a new session continue safely? | state artifact plus evidence pointers, not oral history |

A lower token count is not automatically an improvement. Keep a change only when it preserves the required outcome, authority boundaries, and reproducibility.

## Common Failure Modes

- **Context as database:** important state exists only in a chat transcript.
- **Source-free summary:** a compressed claim has no recoverable evidence.
- **Everything retrieval:** unrelated or stale material crowds out the current task.
- **Prompt injection by retrieval:** untrusted text is treated as executable policy.
- **Fixed-budget folklore:** a model-specific token split is published as universal guidance.
- **Compaction without checkpoint:** a restart loses the only record of approvals or side effects.

## References

- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
