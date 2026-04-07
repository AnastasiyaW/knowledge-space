---
title: Forgetting Strategies
category: patterns
tags: [llm-memory, forgetting, compaction, archival, ttl, memory-management, pruning]
---

# Forgetting Strategies

When and how to remove information from LLM agent memory. Unbounded memory growth degrades retrieval quality - irrelevant results dilute relevant ones. Strategic forgetting is as important as strategic remembering.

## Key Facts

- Memory without pruning degrades retrieval precision over time - more entries means more false positives
- "Forgetting" usually means archival (move to cold storage), not deletion
- Token cost scales with memory size - even if retrieval is fast, injecting too much context is expensive
- Compaction (summarization) is a form of lossy forgetting - details are permanently lost
- The optimal memory size depends on retrieval method: index navigation degrades at ~500 entries, vector search degrades more gradually
- Never delete data that hasn't been archived first

## Forgetting Mechanisms

| Mechanism | What It Does | Reversible | Best For |
|-----------|-------------|------------|----------|
| **TTL (Time-to-Live)** | Auto-expire after fixed period | No (unless archived) | Temporary state, session data |
| **Relevance scoring** | Score entries, prune lowest | Yes (if archived) | Large memory with mixed quality |
| **Compaction** | Summarize, replace details | No | Conversation history |
| **Archival** | Move to cold storage | Yes | Old but potentially useful data |
| **Deduplication** | Merge redundant entries | Partially | Overlapping information |
| **Explicit deletion** | Remove on user request | No | Privacy, corrections |

## TTL-Based Expiry

Assign a time-to-live based on the type of information:

```python
TTL_CONFIG = {
    "session_state": timedelta(hours=24),       # task-specific, short-lived
    "project_status": timedelta(days=30),        # changes monthly
    "tool_output": timedelta(days=7),            # raw outputs are transient
    "decision": timedelta(days=365),             # decisions have long relevance
    "preference": timedelta(days=730),           # preferences are stable
    "identity": None,                            # never expires
}

def should_expire(entry: MemoryEntry, now: datetime) -> bool:
    ttl = TTL_CONFIG.get(entry.type)
    if ttl is None:
        return False
    return (now - entry.created_at) > ttl
```

**Don't delete on expiry - archive.** Move expired entries to a separate store. If they're needed later, they can be retrieved from archive.

## Relevance Scoring

Score each memory entry by utility. Factors:

```python
def relevance_score(entry: MemoryEntry, now: datetime) -> float:
    # Recency: newer is more relevant
    age_days = (now - entry.created_at).days
    recency = 1.0 / (1 + age_days / 30)  # 30-day half-life

    # Access frequency: more-retrieved is more relevant
    access_freq = min(entry.access_count / 10, 1.0)

    # Freshness: recently accessed is more relevant
    last_access_days = (now - entry.last_accessed).days
    freshness = 1.0 / (1 + last_access_days / 7)

    # Type weight: some types are inherently more valuable
    type_weights = {
        "decision": 1.0,
        "gotcha": 0.9,
        "preference": 0.8,
        "finding": 0.7,
        "observation": 0.5,
        "tool_output": 0.3,
    }
    type_weight = type_weights.get(entry.type, 0.5)

    return (0.3 * recency + 0.3 * access_freq + 0.2 * freshness + 0.2 * type_weight)
```

Prune entries below a threshold. Suggested: archive entries scoring < 0.2.

## Compaction

Lossy summarization of detailed history into compressed form. See [[context-window-management]] for conversation compaction specifics.

```python
def compact_memory_topic(topic: str, entries: list[MemoryEntry]) -> MemoryEntry:
    """Replace multiple entries with one summary."""
    full_text = "\n".join(e.text for e in entries)

    summary = llm.complete(f"""Summarize these {len(entries)} memory entries about '{topic}'.
Preserve: key decisions, current state, gotchas, preferences.
Discard: intermediate steps, superseded information, raw outputs.

{full_text}""")

    return MemoryEntry(
        text=summary,
        type="compacted_summary",
        created_at=max(e.created_at for e in entries),
        metadata={"compacted_from": len(entries), "topic": topic}
    )
```

**Warning:** Compaction is irreversible. Archive the original entries before compacting.

## Archival

Move old entries from active memory to cold storage:

```python
def archive_old_entries(active_store, archive_store, max_age_days: int = 90):
    now = datetime.utcnow()
    to_archive = []

    for entry in active_store.all():
        if should_archive(entry, now, max_age_days):
            to_archive.append(entry)

    for entry in to_archive:
        archive_store.add(entry)
        active_store.remove(entry.id)

    return len(to_archive)

def should_archive(entry: MemoryEntry, now: datetime, max_age: int) -> bool:
    # Don't archive: identity, active decisions, high-relevance entries
    if entry.type in ("identity", "active_decision"):
        return False
    if relevance_score(entry, now) > 0.5:
        return False
    return (now - entry.last_accessed).days > max_age
```

Active memory stays fast and focused. Archive is searchable but with higher latency.

## Deduplication

Multiple conversations often produce overlapping memories:

```python
def deduplicate(entries: list[MemoryEntry], similarity_threshold: float = 0.92):
    """Merge near-duplicate entries, keeping the most recent."""
    unique = []
    for entry in sorted(entries, key=lambda e: e.created_at, reverse=True):
        is_dup = False
        for existing in unique:
            sim = cosine_similarity(
                embed(entry.text), embed(existing.text)
            )
            if sim > similarity_threshold:
                # Keep existing (more recent), update metadata
                existing.metadata["also_from"] = entry.id
                is_dup = True
                break
        if not is_dup:
            unique.append(entry)
    return unique
```

## Memory Size Targets

| Memory Type | Target Size | Pruning Trigger |
|-------------|-------------|-----------------|
| Identity (L0) | <50 tokens | Never prune |
| Critical facts (L1) | <200 tokens | Manual review only |
| Active project memory | <5K tokens | When project completes |
| Historical memory | <50K tokens | Monthly archival |
| Archive | Unlimited | Annual review |

## Patterns

### Graduated Retention

```
0-7 days:   Keep everything (verbatim)
7-30 days:  Keep decisions, gotchas, preferences. Archive raw outputs
30-90 days: Compact findings into summaries. Archive details
90+ days:   Archive to cold storage. Keep only identity + decisions
```

### Access-Triggered Preservation

```python
def on_memory_access(entry_id: str):
    """Every time an entry is retrieved, extend its life."""
    entry = store.get(entry_id)
    entry.last_accessed = datetime.utcnow()
    entry.access_count += 1
    store.update(entry)
    # Frequently accessed entries never get archived
```

## Gotchas

- **Forgetting without archival is data destruction.** Always archive before pruning. The cost of storing old data in cold storage is negligible compared to the cost of losing information that turns out to be needed later
- **Compaction accumulates information loss.** If you compact a compacted summary, quality degrades exponentially. Track compaction depth and never compact more than twice. If memory is too large after two compactions, archive instead
- **Deduplication threshold is tricky to tune.** Too aggressive (>0.85 similarity = duplicate) merges genuinely different entries. Too conservative (<0.95) leaves redundancy. Start at 0.92 and adjust based on false positive rate. Always log what was merged for review

## See Also

- [[context-window-management]]
- [[temporal-memory]]
- [[memory-architectures]]
- [[verbatim-vs-extraction]]
- [[session-persistence]]
