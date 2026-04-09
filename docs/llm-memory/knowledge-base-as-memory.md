---
title: Knowledge Base as Memory
category: patterns
tags: [llm-memory, knowledge-base, wiki, markdown, ingest, lint, persistent-knowledge]
---

# Knowledge Base as Memory

Using a structured markdown knowledge base as the agent's long-term memory. The agent reads, writes, and maintains a collection of articles that compound over time - knowledge is written once and maintained, not re-derived on every query.

## Key Facts

- Plain markdown collections with cross-references work up to ~100 articles / ~400K words without vector search
- The LLM navigates via summaries and index files - it doesn't need embeddings for moderate-scale knowledge
- One source ingested → ~10-15 wiki pages touched (created or updated)
- Knowledge bases are "persistent, compounding artifacts" - unlike RAG, they don't re-derive answers from raw sources each time
- LLMs handle bookkeeping well: they don't get bored, don't forget to update cross-references, can touch 15 files in one pass
- Beyond ~500 articles, add optional BM25/vector search with LLM reranking

## Architecture: Raw -> Wiki -> Schema

Three layers, each with a clear role:

### raw/ - Immutable Sources

```
raw/
  paper-attention-is-all-you-need.md
  meeting-notes-2026-03-15.md
  api-docs-stripe-v3.md
```

- PDFs converted to markdown, web articles clipped, datasets, meeting notes
- LLM reads these but NEVER modifies them
- Source of truth for verification and deduplication

### wiki/ - LLM-Generated Knowledge

```
wiki/
  index.md              # catalog with summaries - agent reads first
  log.md                # append-only chronological operation log
  transformer-architecture.md
  stripe-integration.md
  attention-mechanisms.md
```

- Encyclopedia-style articles for concepts and entities
- Summaries, comparisons, cross-references via `[[wiki-links]]`
- `index.md` - the agent's entry point, updated on every ingest
- `log.md` - append-only record of all operations (creates audit trail)

### schema - Configuration

The agent's operating instructions: knowledge base structure, naming conventions, workflows, quality standards. Equivalent to CLAUDE.md or a project's contributing guide.

## Three Operations

### 1. Ingest

New source arrives. The agent:

```
1. Read source from raw/
2. Discuss key takeaways (optionally with user)
3. Create/update wiki pages for new concepts and entities
4. Update index.md with new entries and summaries
5. Revisit related pages - add cross-references
6. Append to log.md: what changed and why
```

**Quality signal:** A good ingest touches 10-15 pages. If it only creates one page, the agent isn't cross-referencing enough.

### 2. Query

User asks a question. The agent:

```
1. Read index.md to locate relevant articles
2. Read specific wiki pages
3. Synthesize answer with citations to wiki pages
4. If the answer is valuable, create a new wiki page from it
```

No vector search needed at this scale. The index is the retrieval mechanism.

### 3. Lint / Health-Check

Periodic maintenance pass:

```python
# Automated checks (scriptable, deterministic)
checks = [
    "orphan_pages",        # pages not referenced from index or other pages
    "dead_links",          # [[wiki-links]] pointing to non-existent pages
    "missing_cross_refs",  # related pages that don't reference each other
    "stale_claims",        # facts with valid_to in the past
    "empty_sections",      # placeholder sections never filled
    "duplicate_topics",    # multiple pages covering the same concept
]

# LLM-assisted checks (need judgment)
llm_checks = [
    "contradictions",      # page A says X, page B says not-X
    "outdated_info",       # claims that may have changed
    "missing_context",     # pages that assume knowledge not in the KB
]
```

**Run lint periodically** - weekly for active knowledge bases, monthly for stable ones. Without maintenance, knowledge bases accumulate contradictions and stale information.

## Patterns

### Index-Driven Navigation

```markdown
# Knowledge Base Index

## Architecture (12 articles)
- microservices-patterns - saga, CQRS, event sourcing
- api-design - REST vs GraphQL, versioning, pagination

## Infrastructure (8 articles)
- kubernetes-ops - deployment strategies, HPA, resource limits
- observability - metrics, tracing, alerting stack

Last updated: 2026-04-08 | Total: 87 articles
```

The agent reads this first. ~500 tokens covers 100 articles with one-line summaries. This is the cheapest possible retrieval mechanism.

### Append-Only Operation Log

```markdown
# Operations Log

## 2026-04-08 14:30
- **Ingested:** Stripe API v3 migration guide
- **Created:** wiki/stripe-v3-migration.md
- **Updated:** wiki/stripe-integration.md (added v3 breaking changes)
- **Updated:** wiki/payment-processing.md (cross-ref to v3 migration)
- **Updated:** index.md (new entry under Payments)

## 2026-04-07 09:15
- **Query:** "How does our auth flow handle token refresh?"
- **Created:** wiki/auth-token-refresh.md (valuable answer, persisted)
```

The log serves as an audit trail and enables the agent to understand the knowledge base's evolution.

### Scaling Beyond Markdown

When the knowledge base outgrows pure navigation:

| Scale | Strategy |
|-------|----------|
| <100 articles | Index navigation only |
| 100-500 | Domain-specific indexes + keyword search |
| 500-5000 | Add BM25 search with LLM reranking |
| 5000+ | Full [[rag-pipeline]] with [[vector-databases]] |

## Tooling

- **Obsidian** - graph view for visualizing connections, Dataview plugin for YAML frontmatter queries
- **MkDocs Material** - static site generation from markdown, search built-in
- **Obsidian Web Clipper** - capture web sources directly into raw/

## Gotchas

- **The index is the bottleneck.** If index.md isn't maintained, the agent can't find anything. Treat index updates as mandatory on every ingest, not optional. Automate if possible
- **"One page per topic" breaks down for complex topics.** A single page on "Kubernetes" will grow unbounded. Split early: k8s-networking, k8s-storage, k8s-rbac. Better to have 10 focused pages than 1 sprawling page
- **LLMs over-create pages on ingest.** Without constraints, the agent creates a new page for every noun it encounters. Set a quality bar: a page must contain at least 3 substantive facts to justify its existence

## See Also

- [[memory-architectures]]
- [[memory-retrieval-patterns]]
- [[session-persistence]]
- [[context-window-management]]
- [[rag-pipeline]]
