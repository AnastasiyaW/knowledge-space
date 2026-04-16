---
title: Session Persistence
category: patterns
tags: [llm-memory, session-handoff, persistent-state, memory-files, journal]
---

# Session Persistence

How to preserve knowledge, decisions, and progress between LLM agent sessions. Since each session starts with a blank context, explicit persistence mechanisms are required - the agent never "remembers" anything automatically.

## Key Facts

- Every LLM session starts with zero memory unless external state is loaded
- Structured handoff (500-2000 tokens) beats raw conversation dump (50-100K tokens) with ~50x compression
- Three questions define a good handoff: what works/broken/blocked, what NOT to retry, what's the ONE next step
- File-based state survives context compaction and session restarts - conversation history does not
- Auto-save at key points (every N messages, before compaction, on topic change) prevents data loss

## Persistence Mechanisms

| Mechanism | Persistence | Structure | Best For |
|-----------|------------|-----------|----------|
| **Handoff file** | Between sessions | Semi-structured markdown | Session continuity |
| **Memory file** | Permanent | Key-value index with links | User preferences, project facts |
| **State file** | Per-task | JSON/YAML | Multi-step task progress |
| **Journal** | Cumulative | Dated entries | Multi-day projects |
| **Conversation export** | Archive | Raw messages | Audit trail (not for loading) |

## Handoff File Pattern

Written at session end, read at session start. Structured briefing, not a dump.

```markdown
# Session Handoff - 2026-04-08 14:30

## Goal
Migrate payment API from Stripe v2 to v3

## Done
- Schema migration script (payments/migrate_v3.py) - tested
- Webhook handler updated for new event format
- Integration tests passing for charge/refund flows

## NOT Working (and why)
- Subscription renewal webhook - v3 changed event payload structure,
  our handler expects `subscription.id` but v3 sends `subscription_id`
- Retry logic - v3 uses idempotency keys differently, current retry
  creates duplicate charges

## Failed Approaches (DO NOT retry)
- monkey-patching stripe library to translate v2 events -> fails silently
  on edge cases (partial refunds, disputes)
- Using stripe's v2 compatibility mode -> deprecated, removed in April

## Key Decisions
- Chose direct v3 migration over gradual rollout because v2 sunset is May 1

## Next Step
Fix subscription webhook handler - map new field names in
payments/webhooks/subscription.py line 45
```

**Rules:**
- Max 1500 tokens - briefing, not log
- Include real error messages, not descriptions
- "Failed approaches" is mandatory, even if it seems obvious
- Absolute file paths for all referenced files
- Don't include: tool call history, intermediate reads, raw command output

## Memory File Pattern

Permanent key-value index that grows over time. Organized by topic with links to detail files.

```markdown
# Memory Index

## User
- user_profile - name, preferences, communication style

## Projects
- api-rewrite - REST->GraphQL, timeline, decisions
- ml-pipeline - training infra, model registry

## Infrastructure
- prod-cluster - K8s on GCP, 3 node pools, autoscaling
- ci-cd - GitHub Actions, deploy to staging/prod

## Decisions
- db-choice - PostgreSQL, reasons, alternatives considered
- api-style - GraphQL over REST, tradeoffs documented
```

Each linked file contains structured details. The index itself stays small enough to always fit in context.

## State File Pattern

For multi-step tasks. JSON/YAML with explicit progress tracking.

```json
{
  "task": "migrate-stripe-v3",
  "status": "in_progress",
  "plan": [
    {"step": "schema migration", "status": "done", "output": "payments/migrate_v3.py"},
    {"step": "webhook handlers", "status": "in_progress", "blocker": "subscription event format"},
    {"step": "retry logic", "status": "blocked", "reason": "idempotency key changes"},
    {"step": "integration tests", "status": "pending"},
    {"step": "load testing", "status": "pending"}
  ],
  "findings": [
    "v3 renames subscription.id -> subscription_id in all webhook payloads",
    "idempotency keys are now required, not optional"
  ],
  "failed_approaches": [
    "monkey-patch stripe lib - fails on partial refunds",
    "v2 compatibility mode - deprecated"
  ]
}
```

The agent reads state at step start, executes, updates state. This survives compaction and context resets.

## Journal Pattern

For multi-day projects. Append-only, dated entries.

```markdown
# Project Journal

## 2026-04-08
- Completed schema migration script
- Found: v3 webhook payload structure changed significantly
- Decided: direct migration, no compatibility layer
- Blocked: subscription webhook needs field mapping

## 2026-04-07
- Started Stripe v3 migration
- Read v3 changelog - 47 breaking changes identified
- Prioritized: payment flows first, subscription second
- Created: task plan in .agent/state.json
```

**When to use journal vs handoff:** Handoff is for session transitions (volatile, replaced each time). Journal is for project history (cumulative, append-only). Use both for long projects.

## Patterns

### Session Start Protocol

```text
1. Check for HANDOFF.md
   - If exists: read, summarize to user, ask to continue or start fresh
   - Archive to handoff-history/YYYY-MM-DD-HHMM.md

2. Check for state files (.agent/state.json, PLAN.md)
   - If exists: load current task state

3. Read MEMORY.md index
   - Load L0/L1 identity and critical facts

4. Ready to work with full context
```

### Session End Protocol

```sql
1. If session > 15 minutes:
   - Write/update HANDOFF.md
   - Update MEMORY.md if new permanent knowledge discovered
   - Update state files if task is in progress

2. Update journal if multi-day project

3. Commit state files if using version control
```

### Learning Extraction

After each session, extract reusable knowledge:

```bash
Categories to extract:
- [DECISION] - architectural choices with reasoning
- [GOTCHA] - unexpected behavior, edge cases
- [REUSE] - patterns worth remembering
- [CORRECTION] - user corrected the agent's approach

Flow:
Session ends → extract tagged findings → triage (future-relevant only)
  → transform into knowledge (rewrite as facts, not history)
  → merge into MEMORY.md or relevant knowledge base
```

## Gotchas

- **Raw conversation dumps are useless for continuity.** 50-100K tokens of conversation history is noise. A 500-token structured handoff contains more actionable information. Never dump raw transcripts as a persistence mechanism
- **Handoffs without "what failed" cause repeat failures.** The next session will try the same approaches and fail the same way. Always include failed approaches with specific reasons why they failed
- **Stale handoffs are worse than no handoff.** If the handoff references files that were deleted or code that was refactored, the agent will be confused. Date your handoffs and archive old ones. Keep only the last 10 in history

## See Also

- [[context-window-management]]
- [[memory-architectures]]
- [[knowledge-base-as-memory]]
- [[temporal-memory]]
- [[forgetting-strategies]]
