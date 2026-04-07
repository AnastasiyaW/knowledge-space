---
title: Context Window Management
category: patterns
tags: [llm-memory, context-window, layered-loading, compaction, token-budget, re-injection]
---

# Context Window Management

Strategies for managing what enters the LLM's context window and when. The context window is finite working memory - everything the agent can reason about at once. Poor management is the primary cause of agent degradation on long tasks.

## Key Facts

- Context windows range from 4K to 2M tokens, but attention quality degrades in the middle ("lost in the middle" effect)
- Cost scales linearly with context size - 128K context at $3/M input = $0.38 per call
- Compaction (summarization) is irreversible - details are permanently lost once summarized
- Layered loading (always-on core + on-demand details) keeps base cost at ~170 tokens while enabling access to full memory
- Context anxiety: agents start rushing/shortcutting when they perceive context is filling up, even if there's room left

## Layered Loading Pattern

Divide memory into layers by criticality. Lower layers are always present; higher layers load on demand.

```
L0 - Identity (~50 tokens)     ← ALWAYS in context
  "You are an assistant for Project X. User is Alice, senior engineer."

L1 - Critical Facts (~120 tokens) ← ALWAYS in context
  "Tech stack: Python 3.12, PostgreSQL 16, deployed on K8s."
  "User prefers: concise answers, code examples, no emojis."

L2 - Topic Memory (variable)    ← Loaded when topic detected
  Retrieved from vector store based on current query.
  Budget: ~2000 tokens per retrieval.

L3 - Full History (variable)    ← Loaded on explicit request
  Complete conversation logs, raw documents.
  Only when agent specifically needs to review past interactions.
```

**Cost comparison:** L0+L1 always loaded = ~170 tokens/call = ~$10/year. Full summarization approach = ~$500/year. The layered approach is 50x cheaper.

## Token Budget Allocation

```python
class TokenBudget:
    def __init__(self, max_tokens: int = 128_000):
        self.allocations = {
            "system_prompt": 0.08,    # 8% - instructions, tool defs
            "identity_l0_l1": 0.02,   # 2% - always-on memory layers
            "state": 0.10,            # 10% - current plan, progress
            "retrieved_memory": 0.15, # 15% - L2 on-demand context
            "conversation": 0.25,     # 25% - recent exchanges
            "tool_results": 0.20,     # 20% - outputs from tools
            "generation": 0.20,       # 20% - reserved for response
        }

    def available(self, category: str) -> int:
        return int(self.max_tokens * self.allocations[category])
```

**Rule of thumb:** Reserve 20% for generation. If tool results are large, summarize them before inserting into context.

## Compaction Strategies

### Summarize-and-Replace

Replace old conversation history with a compressed summary:

```python
def compact(messages: list, keep_recent: int = 6) -> list:
    system = messages[0]
    recent = messages[-keep_recent:]
    old = messages[1:-keep_recent]

    if not old:
        return messages

    summary = llm.complete(f"""Summarize preserving:
    1. Key decisions made
    2. Important findings
    3. Failed approaches (DO NOT retry these)
    4. Current state of task
    History: {format_messages(old)}""")

    return [system,
            {"role": "system", "content": f"[Summary of earlier conversation]\n{summary}"},
            *recent]
```

### State File + Context Reset

For long tasks, prefer full context reset over compaction. Write state to files, start fresh:

```python
# Before reset
state = {
    "goal": "Migrate API from REST to GraphQL",
    "completed": ["schema design", "resolver stubs", "auth middleware"],
    "current": "pagination implementation",
    "findings": ["cursor pagination is 3x faster than offset for our dataset"],
    "failed": ["relay-style connections - too complex for our use case"],
    "blockers": []
}
save_json(".agent/state.json", state)

# After reset - agent reads state file, continues from where it left off
# No information loss from summarization
```

**Context reset > compaction** for tasks longer than ~30 minutes. Compaction preserves continuity but accumulates information loss. A fresh context with explicit state is cleaner.

### Re-injection After Compaction

If compaction is unavoidable, immediately re-inject critical state:

```python
def post_compaction_message(state_file: str) -> str:
    state = load_json(state_file)
    return f"""[Context was compacted. Current state:]

## Goal
{state['goal']}

## Completed Steps
{chr(10).join(f'- {s}' for s in state['completed'])}

## Current Step
{state['current']}

## Failed Approaches (DO NOT retry)
{chr(10).join(f'- {f}' for f in state['failed'])}

[Continue from current step. State above is authoritative.]"""
```

## Auto-Save Triggers

Save memory state automatically at key points:

- **Every N messages** (e.g., every 15 messages) - periodic checkpoint
- **Before compaction** - capture full state before lossy operation
- **Before context reset** - handoff artifact for next session
- **On topic change** - close out current topic's findings
- **On error/failure** - record what went wrong and why

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Stuffing everything in context | "Lost in the middle" - model ignores middle | Layered loading, JIT retrieval |
| No external state | Compaction kills critical details | File-based state management |
| Reactive retrieval every call | Latency compounds | Pre-fetch at plan phase start |
| Ignoring token costs | $3.80 per 10 calls at 128K | Shorter context when possible |
| Trusting compaction output | Summaries miss nuance | Always verify critical facts post-compaction |

## Gotchas

- **"Lost in the middle" is measurable and consistent.** LLMs attend strongly to the beginning and end of context but poorly to the middle. Place critical information (current task, plan, constraints) at the start, recent observations at the end. Never bury important state in the middle of a long history
- **Compaction loses information irreversibly.** Before compacting, save full state to files. After compaction, re-inject the structured state so the agent knows where it stands. Test by asking the agent questions about pre-compaction work - if it can't answer, your re-injection is incomplete
- **Auto-compact can loop.** If context refills quickly after compaction (e.g., large tool outputs), the agent can enter a compact-refill-compact cycle. Set a circuit breaker: after 3 compactions without progress, stop and report

## See Also

- [[memory-architectures]]
- [[session-persistence]]
- [[forgetting-strategies]]
- [[context-engineering]]
- [[agent-memory]]
