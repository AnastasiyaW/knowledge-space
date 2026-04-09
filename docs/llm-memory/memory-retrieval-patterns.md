---
title: Memory Retrieval Patterns
category: patterns
tags: [llm-memory, retrieval, semantic-search, bm25, hybrid-search, reranking, index-navigation]
---

# Memory Retrieval Patterns

How agents find relevant information in their memory. The retrieval method determines recall quality, latency, and cost. Different approaches work at different scales.

## Key Facts

- Index-based navigation works up to ~500 articles with zero retrieval cost
- BM25 (keyword) catches exact matches that semantic search misses
- Vector similarity catches semantic matches that keyword search misses
- Hybrid (BM25 + vector) with reranking is the most reliable approach for production
- Lightweight LLM reranking (~$0.001/query) can push recall from 96.6% to ~100%
- Retrieval latency compounds in agent loops - pre-fetch at plan start, not on every step

## Retrieval Methods Comparison

| Method | Scale | Cost/Query | Recall | Latency | Best For |
|--------|-------|-----------|--------|---------|----------|
| **Index navigation** | <500 articles | ~0 | Depends on index quality | <100ms | Small knowledge bases |
| **Keyword/BM25** | Any | ~0 | High for exact matches | <10ms | Known terminology |
| **Vector similarity** | Any | Embedding cost | High for semantic | 10-100ms | Fuzzy/conceptual queries |
| **Hybrid (BM25+vector)** | Any | Embedding cost | Highest | 20-150ms | Production systems |
| **LLM rerank** | Any | ~$0.001 | Near-perfect | +200-500ms | Critical accuracy needs |

## Index-Based Navigation

The simplest retrieval: agent reads an index, picks relevant files, reads them.

```markdown
# Memory Index (agent reads this first)

## User Preferences
- db-preference - PostgreSQL, pgvector, reasons
- editor - Neovim, plugins, keybindings

## Current Projects
- api-rewrite - GraphQL migration, Q2 deadline
```

**How it works:** The index fits in context (~500 tokens for 100 entries). The agent pattern-matches the user's query against index entries and reads the relevant files. No embeddings, no search infrastructure.

**Scaling:** At ~500 entries, the index itself exceeds comfortable context size. Split into domain indexes or add search.

## Keyword Search (BM25)

Term frequency-based retrieval. Finds documents containing the query's exact words.

```python
from rank_bm25 import BM25Okapi

class KeywordMemory:
    def __init__(self, documents: list[str]):
        tokenized = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)
        self.documents = documents

    def search(self, query: str, top_k: int = 5) -> list[str]:
        tokens = query.lower().split()
        scores = self.bm25.get_scores(tokens)
        top_indices = scores.argsort()[-top_k:][::-1]
        return [self.documents[i] for i in top_indices if scores[i] > 0]
```

**Strengths:** Fast, free, deterministic, catches exact terminology.
**Weaknesses:** Misses semantically similar but lexically different content ("car" won't find "automobile").

## Vector Similarity Search

Embed query and documents, find closest vectors. See [[embeddings]] and [[vector-databases]] for details.

```python
import chromadb

collection = client.get_collection("memory")

results = collection.query(
    query_texts=["What database does the user prefer?"],
    n_results=5,
    where={"valid_to": None}  # only current facts
)
```

**Strengths:** Semantic understanding, handles paraphrasing, works across languages.
**Weaknesses:** Misses exact keyword matches sometimes, non-deterministic, requires embedding infrastructure.

## Hybrid Search

Combine BM25 and vector search. Two merging strategies:

### Weighted Sum

```python
def hybrid_search(query: str, alpha: float = 0.5, top_k: int = 5):
    bm25_scores = get_bm25_scores(query)      # normalized 0-1
    vector_scores = get_vector_scores(query)    # normalized 0-1

    combined = {}
    for doc_id in set(bm25_scores) | set(vector_scores):
        combined[doc_id] = (
            alpha * vector_scores.get(doc_id, 0) +
            (1 - alpha) * bm25_scores.get(doc_id, 0)
        )

    return sorted(combined.items(), key=lambda x: -x[1])[:top_k]
```

**Problem:** `alpha` needs tuning per domain. 0.5 is rarely optimal.

### Reciprocal Rank Fusion (RRF)

Merge by rank position, no alpha tuning needed:

```python
def rrf_merge(ranked_lists: list[list], k: int = 60) -> list:
    """Merge multiple ranked lists using Reciprocal Rank Fusion."""
    scores = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (rank + k)
    return sorted(scores.items(), key=lambda x: -x[1])
```

**RRF is preferred** because it doesn't require score normalization or alpha tuning. Works with any number of retrieval methods.

## LLM Reranking

After initial retrieval, use an LLM to rerank candidates by relevance:

```python
def llm_rerank(query: str, candidates: list[str], top_k: int = 3) -> list[str]:
    prompt = f"""Rate each candidate's relevance to the query (0-10).
Query: {query}

Candidates:
{chr(10).join(f'{i+1}. {c[:200]}' for i, c in enumerate(candidates))}

Return JSON: [{{"index": 1, "score": 8}}, ...]"""

    scores = llm.complete(prompt, model="haiku")  # cheap model suffices
    ranked = sorted(scores, key=lambda x: -x["score"])
    return [candidates[s["index"]-1] for s in ranked[:top_k]]
```

**Cost:** ~$0.001/query with a small model. Pushes recall from 96.6% to ~100% on benchmarks.

**Alternative:** Cross-encoder reranking (no LLM needed):

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
pairs = [(query, doc) for doc in candidates]
scores = reranker.predict(pairs)
```

Cross-encoders are faster and cheaper than LLM reranking but less flexible.

## Patterns

### Pre-Fetch at Plan Start

Don't retrieve on every agent step. Batch retrieval at the start of each plan phase:

```python
def start_plan_phase(phase: str, subtasks: list[str]):
    # Pre-fetch all likely-needed context
    queries = [phase] + subtasks
    context = {}
    for q in queries:
        context[q] = memory.search(q, top_k=3)

    # Inject aggregated context once
    return format_context(context)
```

This avoids retrieval latency on every LLM call and keeps the agent's flow uninterrupted.

### Metadata-Filtered Retrieval

Narrow the search space before similarity computation:

```python
results = collection.query(
    query_texts=["deployment configuration"],
    n_results=5,
    where={
        "$and": [
            {"wing": "project-api"},
            {"valid_to": None},
            {"room": {"$in": ["infrastructure", "deployment"]}}
        ]
    }
)
```

Metadata filtering happens before vector search in most databases - design your metadata schema carefully.

## Cost Comparison

For 1000 queries/month against 10K documents:

| Method | Infrastructure | Per-Query | Monthly Total |
|--------|---------------|-----------|---------------|
| Index navigation | ~$0 (files) | ~$0 | ~$0 |
| BM25 only | ~$5 (compute) | ~$0 | ~$5 |
| Vector only | ~$20 (vector DB) | ~$0.0005 | ~$20.50 |
| Hybrid + rerank | ~$20 (vector DB) | ~$0.001 | ~$21 |

The cost difference between approaches is small. Choose by recall quality, not price.

## Gotchas

- **Vector search can miss obviously present text.** Cosine similarity sometimes fails where keyword search succeeds trivially. Always combine with BM25 for critical applications. See [[embeddings]] for known similarity failures
- **Retrieval latency compounds in agent loops.** An agent that runs 20 steps with vector search on each step adds 2-4 seconds of retrieval latency. Pre-fetch at plan start or cache results within a task. Batch retrieval queries where possible
- **Metadata filtering design is permanent.** Changing metadata schema requires re-indexing all documents. Plan your metadata fields (wing, room, type, valid_from, valid_to) before initial indexing. Adding new fields later means re-processing everything

## See Also

- [[memory-architectures]]
- [[verbatim-vs-extraction]]
- [[knowledge-base-as-memory]]
- [[vector-databases]]
- [[embeddings]]
- [[rag-pipeline]]
