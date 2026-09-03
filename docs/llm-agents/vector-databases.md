---
title: "Vector Databases and Retrieval"
description: "Build vector retrieval around versioned embeddings, authorized metadata filters, provenance, recall evaluation, and safe migration rather than static product rankings."
tags: [llm-agents, vector-db, embeddings, retrieval, rag, similarity-search, hybrid-search]
---

# Vector Databases and Retrieval (September 2026)

Version context: embedding models, distance metrics, vector dimensions, index algorithms, filtering semantics, hybrid-query APIs, and hosted-service limits change independently. Keep them in a reviewed retrieval configuration and validate the selected store against the actual corpus and workload.

A vector store retrieves candidates whose embedding representations are close to a query representation. It does not prove that a candidate is factual, current, authorized, or sufficient for a generated answer. Retrieval quality is a workflow property: ingestion, filtering, ranking, context construction, citations, and evaluation all matter.

## Start with a Retrieval Record

Each indexed item needs a stable identity, provenance, embedding revision, and policy metadata.

```json
{
  "record_id": "doc:policy-17:chunk-004",
  "source_ref": "repository:policies@4f31...",
  "content_digest": "sha256:...",
  "embedding_revision": "embedder@2026-09-03",
  "vector_space": "semantic-search-v4",
  "metadata": {
    "tenant_id": "tenant-42",
    "classification": "internal",
    "published_at": "2026-08-21T00:00:00Z",
    "language": "en"
  },
  "index_state": "ready"
}
```

The original source remains canonical. The vector record is an index entry that must be rebuildable from a controlled source manifest.

## Retrieval Is a Pipeline

```text
authorized query
  -> policy filter
  -> dense / lexical candidate retrieval
  -> fusion or reranking
  -> context selection with source references
  -> model answer
  -> citation and task validator
```

A system may use dense retrieval, lexical retrieval, metadata filtering, reranking, or a combination. "Hybrid" is a design choice, not a guarantee that any two scores can be added safely. Qdrant's current documentation, for example, illustrates separate dense and sparse candidate retrieval followed by a defined fusion query. [Qdrant hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/)

## Apply Authorization Before the Answer

Treat metadata filters as part of the access-control contract, not merely a relevance preference. A query must be constrained by tenant, classification, lifecycle, region, and any other policy dimension before retrieved text reaches a model.

Validate both stages:

1. **candidate stage:** no disallowed record appears in the retriever output;
2. **context stage:** no disallowed snippet or stale source reference reaches the prompt;
3. **answer stage:** citations identify the retained source records and the answer does not claim support it lacks.

A post-generation refusal does not repair an unauthorized context leak.

## Index Choice Is a Measured Trade-off

Approximate-nearest-neighbor indexes can reduce search cost while introducing recall/latency trade-offs. Exact search, quantization, graph indexes, inverted-file indexes, and database-native extensions make different trade-offs for a particular vector space and workload.

The FAISS project demonstrates the basic index lifecycle: define a fixed vector dimension, add vectors, then search for nearest neighbors. Some index types also require training before use. [FAISS getting started](https://github.com/facebookresearch/faiss/wiki/Getting-started)

Choose an implementation only after measuring:

| Requirement | Evidence to collect |
|---|---|
| Retrieval quality | recall or task success against a reviewed query set |
| Latency and capacity | tail latency, concurrency, memory, and build time |
| Filtering | authorization correctness under adversarial tenant/classification cases |
| Durability | backup, restore, and rebuild receipt from source manifest |
| Operations | upgrade, observability, incident recovery, and ownership |
| Cost | current storage, query, replication, and operational costs |

## Embed and Rebuild Idempotently

A safe ingestion worker should:

1. read a versioned source;
2. normalize and split it under a recorded chunking policy;
3. compute a content digest and embedding revision;
4. write by deterministic record ID or idempotency key;
5. confirm the index state and count against the manifest;
6. write a receipt with failures classified for retry or review.

Do not rely on a successful `upsert` response as proof that the whole corpus is searchable and authorized.

## Migrate Embeddings Deliberately

A new embedding model, dimension, normalization rule, or distance metric defines a new vector space. A changed chunking strategy changes corpus representation and index schema; it still requires a controlled reindex and evaluation even when the encoder and vector space remain compatible. Prefer a separate collection or namespace and a controlled dual-read or dual-write migration:

```text
baseline index + evaluation -> candidate index + same evaluation
  -> bounded traffic comparison -> promote or roll back
```

Do not silently mix incompatible vector spaces. Keep a chunking change in a separately evaluated index version, because record identity, source coverage, and retrieval behavior can change even when vector dimensions do not.

## Gotchas

- **Nearest is not true.** Similarity search produces candidates, not evidence for an answer. **Fix:** retain sources, rerank where appropriate, and validate citation coverage.
- **Metadata filtering is an access-control surface.** A missing tenant filter can expose another customer's data. **Fix:** make policy filters mandatory and test them before model context construction.
- **Embedding changes are schema changes.** Different vector spaces cannot be compared or mixed safely by intuition. **Fix:** version the embedding and migrate via separate, evaluated indexes.
- **Index success is not corpus completeness.** Partial ingestion, stale chunks, and failed deletes can remain invisible. **Fix:** reconcile counts and digests against a source manifest.
- **Hybrid scores need a defined method.** Dense and lexical signals have different scales. **Fix:** choose and evaluate a fusion/reranking strategy rather than adding raw scores.
- **A vector index is not a backup.** It is a rebuildable derivative. **Fix:** protect the source corpus and store index rebuild receipts.

## Sources

- [Qdrant hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/)
- [FAISS getting started](https://github.com/facebookresearch/faiss/wiki/Getting-started)
- [pgvector project](https://github.com/pgvector/pgvector)

## See Also

- [[embeddings]]
- [[rag-pipeline]]
- [[chunking-strategies]]
- [[tokenization]]
- [[llmops]]
- [[agent-security]]
