---
title: "Verbatim Storage vs Extraction in Agent Memory"
description: "Why raw verbatim storage beats LLM extraction for agent memory retrieval - benchmarks, MemPalace architecture, layered loading patterns, and temporal knowledge graphs."
---

# Verbatim Storage vs Extraction in Agent Memory

Counter-intuitive finding: storing raw text verbatim outperforms LLM-extracted summaries for agent memory retrieval. Extraction is lossy - when you extract "user prefers Postgres", you lose WHY.

## Key Finding

**Raw verbatim text in ChromaDB with default embeddings = 96.6% R@5 on LongMemEval without any LLM calls.**

This beats:
- Mem0: ~85%
- Zep: ~85%
- Mastra: 94.87%

All three use LLM extraction/summarization. The penalty is measurable and consistent across benchmarks.

Adding lightweight LLM reranking (e.g., Haiku at ~$0.001/query) pushes verbatim retrieval to 100% (500/500 on LongMemEval).

## Why Extraction Loses

Extraction compresses context in ways that eliminate:
- **Reasoning chains** - "user chose Postgres because they had licensing concerns about MySQL and already knew Postgres from job X"
- **Uncertainty signals** - "user mentioned possibly wanting to switch to TimescaleDB later"
- **Implicit preferences** - tone, style, level of technical detail the user prefers

The extracted fact is correct, but the surrounding context that makes it useful is gone.

## MemPalace Architecture

Hierarchical structure mirroring the memory palace mnemonic:

```text
Wings     (person / project context)
  └── Rooms     (topic areas)
        └── Halls   (types: facts / events / discoveries / preferences / advice)
              └── Closets   (summaries)
                    └── Drawers   (verbatim text)

Tunnels = cross-links between rooms from different wings
```

Graph built from ChromaDB metadata, no external graph database required.  
Temporal relationships tracked in SQLite: entity-relationship triples with `valid_from` / `valid_to`.

## Four-Layer Loading

```text
L0 (~50 tokens)    identity, persistent identity facts   → ALWAYS loaded
L1 (~120 tokens)   critical facts, active context        → ALWAYS loaded
L2/L3              domain knowledge, full history         → loaded on demand
```

Total always-loaded context: ~170 tokens.  
Cost comparison: ~$10/year (layered) vs ~$507/year (full summarization).

## Temporal Knowledge Graph

SQLite triples with validity windows solve the staleness problem:

```sql
CREATE TABLE facts (
  entity      TEXT,
  relation    TEXT,
  value       TEXT,
  valid_from  TEXT,  -- ISO-8601
  valid_to    TEXT,  -- NULL = currently valid
  source      TEXT   -- message/session this came from
);
```

When a fact changes: close old record (`valid_to = now`), insert new record. Query "current facts" with `WHERE valid_to IS NULL`.

## Auto-Save Triggers

Reliable memory requires saving at predictable points:
- Every N messages (e.g., every 15 interactions)
- Before context compaction (critical - once compacted, detail is lost)
- On session end
- On explicit user feedback ("remember that..." triggers immediate save)

## Hybrid Entity Resolution

Before each processing batch, build an in-memory index of all known entities:

```python
knowledge_index = {
  "people":         [{"name": "...", "aliases": [...], "file": "..."}],
  "organizations":  [...],
  "projects":       [...],
  "topics":         [...]
}
```

Inject index as a formatted table into the agent prompt. The agent resolves "John Smith" to the existing `[[People/John Smith]]` note rather than creating a duplicate.

This is simpler than vector-based deduplication and more accurate for named entity resolution.

## Rowboat Knowledge Pipeline Pattern

Three-stage pipeline for continuous knowledge accumulation:

**Stage 1: Labeling** - classify incoming content (noise vs signal, topic, relationship type). Noise-first filtering: decide what to SKIP before deciding what to keep.

**Stage 2: Graph Building** - extract entities, resolve to canonical names via knowledge index, write/update notes with bidirectional wiki-links. Track file state by `mtime + SHA-256 hash` to avoid reprocessing.

**Stage 3: Tagging** - apply structured tags for retrieval facets (relationship type, topic, action-required, etc.)

State tracked per file to ensure partial progress survives failures.

## Gotchas

- **30x compression claims from AAAK dialect are not verified.** Community analysis found token counting errors (using `len(text)//3` instead of a real tokenizer) and regression on LongMemEval: 96.6% → 84.2%. Verbatim wins - don't apply lossy compression.
- **Verbatim approach requires good embedding + rerank pipeline.** Default embeddings give 96.6%, but the 3.4% gap matters for production use. Add a lightweight reranking step (Haiku/Flash) to close the gap to near-100%.
- **Temporal knowledge graphs require discipline on `valid_to` management.** If you forget to close old facts when new ones arrive, queries return conflicting information. Add a constraint: only one valid fact per (entity, relation) pair can have `valid_to IS NULL`.
- **Auto-save before compaction is critical.** Once Claude compacts context, the details of earlier messages are compressed. If your session memory hasn't been saved to disk before compaction, that knowledge is permanently reduced. Hook into `PreCompact` or `Stop` events.

## See Also

- [[memory-architectures]]
- [[session-persistence]]
- [[knowledge-graph-memory]]
- [[temporal-memory]]
