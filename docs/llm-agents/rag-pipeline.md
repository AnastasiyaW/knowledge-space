---
title: "RAG Pipeline Design (September 2026)"
category: techniques
tags: [llm-agents, rag, retrieval, grounding, citations, evaluation]
---

# RAG Pipeline Design (September 2026)

Reviewed 2026-09-03. Retrieval-augmented generation (RAG) supplies selected external evidence to a generation step at runtime. It can improve access to changing or private knowledge, but it does not automatically make an answer factual, current, authorized, or correctly cited.

## Build It as a Data Product

```text
authoritative sources
    -> ingest with provenance and access policy
    -> normalize and split into citation-preserving units
    -> embed/index as an immutable generation
    -> retrieve and filter candidates at query time
    -> generate only from allowed evidence
    -> validate citations, outcome, and feedback
```

Every arrow is a release boundary. If a document changes, the system should be able to identify the affected chunks, embeddings, index generation, and published answers.

## Source Record Before Chunking

| Field | Purpose |
|---|---|
| Stable ID and locator | Lets an answer point back to a human-readable source |
| Revision/time | Distinguishes current evidence from superseded content |
| Owner and authority | Shows whether a source can support a claim |
| Access scope | Prevents retrieval from becoming a permissions bypass |
| Parser/splitter version | Explains a changed retrieval result |

Do not ingest a URL or file merely because it is reachable. Make its authority, license, and freshness policy explicit first.

## Query-Time Contract

1. Classify the request and its access scope.
2. Retrieve candidates from the named index generation.
3. Apply deterministic metadata/authorization filters before the model sees content.
4. Pass excerpts together with stable source locators and revision metadata.
5. Require the answer layer to cite evidence or emit an explicit insufficiency state.
6. Store the retrieval receipt separately from the generated prose.

```json
{
  "query_id": "q-482",
  "index_generation": "kb-2026-09-03-02",
  "candidates": [
    {"source_id": "policy-14", "revision": "sha256:...", "locator": "policy.md#citations"}
  ],
  "access_policy": "editorial-internal",
  "outcome": "EVIDENCE_SUFFICIENT"
}
```

## Evaluate Retrieval Separately

An answer can sound helpful even when retrieval failed. Maintain a test set of queries with expected/forbidden source identifiers, expected citation granularity, and relevant authorization boundaries. Investigate failures by category: no evidence, wrong document, stale revision, missing section, wrong language, permission leak, or unsupported synthesis.

Public framework defaults are hypotheses, not your corpus evaluation. The useful chunk size, overlap, retriever, and reranker depend on document structure and the task's evidence requirement.

## Update and Rollback

Create a new index generation when changing corpus content, embeddings, chunking, or retrieval policy. Validate it beside the active generation; switch the reader atomically; retain the previous generation long enough to investigate and roll back. A partial in-place reindex is hard to evaluate and nearly impossible to explain.

## Gotchas

- **Issue: Treating retrieved text as automatically trusted.** A source may be outdated, injected, or beyond the requester's access scope. **Fix:** retain authority/revision/access metadata and filter deterministically before prompting.
- **Issue: Testing only final answers.** Retrieval failures are invisible once prose is fluent. **Fix:** store and score a retrieval receipt independently of answer quality.
- **Issue: Hiding missing evidence.** The model may fill the gap with plausible text. **Fix:** expose an `EVIDENCE_INSUFFICIENT` outcome and route it to search, clarification, or a human.
- **Issue: Reindexing in place.** Users can receive mixed old/new evidence. **Fix:** publish immutable index generations and atomically change the reader alias.

## See Also

- [[embeddings]]
- [[chunking-strategies]]
- [[vector-databases]]
- [[production-patterns]]

## Sources

- [Original RAG paper](https://arxiv.org/abs/2005.11401)
- [LangChain retrieval overview](https://docs.langchain.com/oss/python/langchain/retrieval)
- [OpenAI retrieval guide](https://developers.openai.com/api/docs/guides/retrieval)
