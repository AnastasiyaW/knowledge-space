---
title: Memory Architectures for LLM Agents
category: concepts
tags: [llm-memory, memory-systems, hierarchical-memory, graph-memory, vector-stores]
---

# Memory Architectures for LLM Agents

Structural approaches to organizing persistent knowledge for LLM agents. The architecture determines retrieval quality, storage cost, and how well the agent can reason across stored information.

## Key Facts

- LLMs are stateless - all memory is external infrastructure the agent reads/writes
- Memory architecture directly constrains what the agent can recall and how accurately
- Simple flat files outperform complex systems up to ~100 articles / ~400K words
- Beyond that threshold, structured retrieval (index-based or vector) becomes necessary
- Raw verbatim storage with default embeddings achieves 96.6% R@5 on long-memory benchmarks - beating extraction-based systems (~85%)
- Adding lightweight LLM reranking pushes retrieval to ~100% at negligible cost (~$0.001/query)

## Architecture Comparison

| Architecture | Scale | Cost | Retrieval | Maintenance |
|-------------|-------|------|-----------|-------------|
| **Flat files** (markdown) | <100 articles | Minimal | LLM navigates via index | Manual or LLM-assisted |
| **Hierarchical graph** | 100-10K entries | Low-medium | Metadata-guided traversal | Auto-organized by taxonomy |
| **Vector store** (verbatim) | 1K-1M entries | Medium | Embedding similarity | Auto-indexed on ingest |
| **Knowledge graph** (triples) | Any | High | Structured queries + traversal | Complex, needs entity resolution |
| **Hybrid** | Any | Varies | Multiple retrieval paths | Most complex, best results |

## Flat File Architecture

Plain markdown files with cross-references and a maintained index. The LLM navigates by reading the index, then drilling into specific files.

```bash
knowledge/
  index.md          # catalog with summaries (LLM reads first)
  log.md            # append-only operation log
  raw/              # immutable source materials
  wiki/             # LLM-generated structured articles
    concept-a.md
    entity-b.md
```

**Three operations:**
1. **Ingest** - new source arrives, LLM reads it, creates/updates ~10-15 wiki pages, updates index
2. **Query** - LLM reads index, navigates to relevant pages, synthesizes answer with citations
3. **Lint** - periodic health check: find contradictions, stale claims, orphan pages, missing cross-references

**When it works:** The LLM is the retrieval engine. With good summaries in the index, it navigates ~100 articles without vector search. Knowledge compounds - written once, maintained incrementally, not re-derived on every query.

**When it breaks:** Beyond ~500 articles, index becomes too large for context window. Need to split into domain indexes or add search.

## Hierarchical Graph Architecture

Organizes memory into a navigable taxonomy using spatial metaphors:

```text
Wing (person/project)
  └── Room (topic)
       └── Hall (type: facts/events/discoveries/preferences/advice)
            └── Closet (summary)
                 └── Drawer (verbatim text)
```

- **Cross-links** ("tunnels") connect rooms across different wings
- Metadata in [[vector-databases]] encodes the hierarchy - no separate graph DB needed
- [[embeddings]] on verbatim text in drawers handle similarity search
- Temporal knowledge graph in SQLite stores entity-relationship triples with validity periods

**Key advantage:** Navigation is structured. The agent doesn't search the entire memory - it narrows by wing, then room, then hall. This reduces false positives and makes retrieval explainable.

## Vector Store Architecture

Store text chunks with [[embeddings]], retrieve by semantic similarity.

```python
# Simplest viable memory
import chromadb

client = chromadb.Client()
collection = client.create_collection("memory")

# Store verbatim
collection.add(
    documents=["User prefers Postgres because of jsonb support and pgvector"],
    ids=["mem_001"],
    metadatas=[{"wing": "user", "room": "preferences", "valid_from": "2026-01-15"}]
)

# Retrieve
results = collection.query(query_texts=["database preference"], n_results=5)
```

**Critical finding:** Raw verbatim text with default embeddings significantly outperforms LLM-extracted summaries. Systems that extract facts like "user prefers Postgres" lose the *why* - and the why is what makes retrieval useful. See [[verbatim-vs-extraction]].

## Knowledge Graph Architecture

Entity-relationship triples with temporal validity:

```text
(User, prefers, PostgreSQL, valid_from=2026-01, valid_to=null)
(PostgreSQL, supports, pgvector, valid_from=2024-06, valid_to=null)
(User, evaluated, MySQL, valid_from=2025-11, valid_to=2025-12)
```

- Best for reasoning across relationships ("what tools does the user prefer that support vector search?")
- Expensive to maintain - entity resolution, deduplication, validity tracking
- Often combined with vector store for hybrid retrieval

## Hybrid Architecture

Production systems combine multiple approaches:

```text
L0: Identity core (flat file, ~50 tokens, always loaded)
L1: Critical facts (flat file, ~120 tokens, always loaded)
L2: Topic-specific memory (vector store, loaded on demand)
L3: Full history (vector store, loaded on explicit request)
```

See [[context-window-management]] for the layered loading pattern.

## Patterns

### Index-First Navigation

```markdown
# Memory Index

## User Preferences
- database-choice - PostgreSQL, reasons, migration history
- editor-setup - Neovim config, plugins, keybindings

## Project: API Rewrite
- architecture-decisions - REST vs GraphQL, chosen GraphQL
- deployment - K8s on GCP, Terraform managed
```

The agent reads this index first, then opens only the files it needs. This is JIT context loading - minimal tokens until specific knowledge is required.

### Ingest Workflow

```bash
Source material arrives
  → LLM reads source (raw/ - immutable)
  → LLM creates/updates wiki pages
  → LLM updates index.md with new entries
  → LLM appends to log.md
  → LLM revisits related pages for cross-references
```

One source typically touches 10-15 wiki pages. The LLM handles bookkeeping reliably - it doesn't get bored and doesn't forget to update cross-references.

## Gotchas

- **Flat files hit a ceiling around 400K words.** The index itself becomes too large for the context window. Solution: split into domain-specific indexes, add optional BM25/vector search with LLM reranking
- **Graph DBs add complexity without proportional benefit for most use cases.** Metadata fields in a vector store (wing, room, type, valid_from) give you 80% of graph navigation at 20% of the complexity. Only use a dedicated graph DB when you need multi-hop relationship queries
- **Memory without maintenance degrades.** Facts become stale, contradictions accumulate, orphan pages appear. Schedule periodic lint/health-check passes - find contradictions, verify temporal validity, prune dead links

## See Also

- [[verbatim-vs-extraction]]
- [[context-window-management]]
- [[knowledge-base-as-memory]]
- [[memory-retrieval-patterns]]
- [[agent-memory]]
- [[vector-databases]]
