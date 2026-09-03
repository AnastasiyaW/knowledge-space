---
title: "Agent Memory and State (September 2026)"
category: concepts
tags: [llm-agents, memory, state, context-management, persistence, authorization]
---

# Agent Memory and State (September 2026)

Reviewed 2026-09-03. "Memory" describes several different mechanisms. Keep execution state, user-specific memory, organizational knowledge, and authoritative source material distinct: they have different owners, retention rules, access scopes, and failure modes.

## Four Things Often Called Memory

| Type | Scope | Typical content | Control needed |
|---|---|---|---|
| Run state | One workflow execution | Steps, tool receipts, pending approval | Checkpointing and idempotent resume |
| Thread context | One conversation or task | Recent messages and selected artifacts | Token budget and compaction policy |
| Long-term memory | User, agent, or organization namespace | Preferences, facts, prior outcomes | Write policy, provenance, isolation, expiry |
| Knowledge corpus | Many users/tasks | Versioned source documents | Authority, citations, retrieval, publication policy |

A chat transcript is not a database, and a vector store is not permission to treat retrieved text as a remembered fact.

## Memory Record Contract

```json
{
  "memory_id": "user-193:preference-7",
  "namespace": ["user", "193"],
  "kind": "preference",
  "value": "Prefers concise weekly summaries",
  "source": "explicit-user-statement",
  "written_by": "memory-policy-v2",
  "created_at": "2026-09-03T12:00:00Z",
  "expires_at": null,
  "confidence": "confirmed",
  "access_policy": "user-193-only"
}
```

The record must say why it was written and who may read it. Do not let a model convert arbitrary untrusted text into durable policy or cross-user memory without a deterministic rule and review boundary.

## Read and Write Path

```text
incoming request
    -> authenticate and establish namespace
    -> retrieve only scoped, unexpired records
    -> select a bounded context slice
    -> run the workflow with checkpointed state
    -> propose memory candidates
    -> validate/provenance-check/approve writes
```

LangGraph distinguishes thread-scoped checkpointed state from cross-thread stores. Its documentation treats short-term and long-term memory as separate concepts; use that distinction even if another framework has different API names. [Memory overview](https://docs.langchain.com/oss/python/concepts/memory) [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

## Context Compaction Is a Policy

When a conversation grows, choose what can be summarized, dropped, re-retrieved, or preserved as a structured state field. Preserve open approvals, tool receipts, user-visible commitments, and references to authoritative sources. A free-form summary should not become the only record of a material action.

## Evaluation

Test the memory system with separate scenarios for:

1. correct recall within one user namespace;
2. no retrieval across users, tenants, or revoked permissions;
3. expiry, correction, and deletion of an obsolete record;
4. resistance to memory-write prompt injection;
5. recovery from interruption at a checkpoint.

Measure both helpful recall and harmful recall. A system that remembers more is not necessarily better.

## Gotchas

- **Issue: Writing a preference because an untrusted webpage said it.** External text can steer durable behavior. **Fix:** restrict writes to explicit user statements or validated application events with provenance.
- **Issue: Sharing an agent-wide namespace by default.** One user's data can influence another workflow. **Fix:** make scope explicit and default to the narrowest namespace.
- **Issue: Summarizing away a pending approval or receipt.** The workflow loses its recovery boundary. **Fix:** store these as typed state fields, not only prose.
- **Issue: Treating old memory as a source of truth.** Preferences and facts can change. **Fix:** attach time, provenance, confidence, and an expiry/review policy.

## See Also

- [[context-engineering]]
- [[agent-architectures]]
- [[production-patterns]]
- [[tokenization]]

## Sources

- [LangChain memory overview](https://docs.langchain.com/oss/python/concepts/memory)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph add memory](https://docs.langchain.com/oss/python/langgraph/add-memory)
