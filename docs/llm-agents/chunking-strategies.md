---
title: "Chunking Strategies for Retrieval (September 2026)"
category: techniques
tags: [llm-agents, chunking, retrieval, rag, document-processing]
---

# Chunking Strategies for Retrieval (September 2026)

Reviewed 2026-09-03. Chunking creates the retrieval units for a document corpus. There is no universal best chunk size: a useful strategy preserves evidence and metadata while optimizing retrieval and answer quality against a real evaluation set.

## Start from the Retrieval Contract

| Question | Design implication |
|---|---|
| What must the answer cite? | Preserve source, version, page/section, and stable locator |
| What is the user asking for? | Choose a unit that contains enough evidence to answer it |
| What structure exists? | Prefer headings, records, tables, and semantic boundaries |
| Which model consumes the result? | Measure token budget with the exact tokenizer |
| How are documents updated? | Keep chunk identity/version stable enough to delete and re-index |

LangChain describes retrieval as a modular pipeline of loaders, text splitters, embeddings, vector stores, and retrievers. A splitter is one component, not the whole quality system. [LangChain retrieval](https://docs.langchain.com/oss/python/langchain/retrieval)

## Strategies

| Strategy | Use when | Main risk |
|---|---|---|
| Structure-aware | Headings, records, and paragraphs carry meaning | Broken input structure creates bad boundaries |
| Token-bounded | The downstream context limit is strict | Tokenizer/version mismatch |
| Parent-child | Small units retrieve precisely but larger units answer well | Parent linkage and storage complexity |
| Table/record-aware | Facts live in rows or fields | Flattening loses relationships |
| Semantic boundary | Cohesive sections matter more than fixed length | Boundary heuristic can be inconsistent |

Choose overlap only when it solves an evaluated boundary-loss problem. Overlap increases index size, retrieval duplication, and prompt cost.

## Structure-Aware Splitter

This Python example uses the current standalone LangChain text-splitters package. It creates bounded chunks while preferring paragraph and line boundaries.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=80,
    separators=["\n\n", "\n", ". ", " ", ""],
)

chunks = splitter.split_text(
    "Heading\n\nFirst paragraph with evidence.\n\nSecond paragraph with context."
)
print(chunks)
```

Treat the numeric values as a baseline for evaluation, not a default suitable for every corpus.

## Metadata Contract

```json
{
  "chunk_id": "policy-2026-09:section-4:chunk-02",
  "document_id": "policy-2026-09",
  "document_version": "sha256:...",
  "source_locator": {"section": "4", "page": 12},
  "parent_id": "policy-2026-09:section-4",
  "text": "..."
}
```

Metadata must survive retrieval and reach the answer generator. If the final response cannot identify which version and section supported a claim, the retrieval pipeline cannot provide reliable citation.

## Evaluation

Evaluate the complete path, not just embedding similarity:

1. Create representative questions with accepted sources and expected answer constraints.
2. Measure whether the retrieved set contains sufficient evidence.
3. Measure answer correctness and citation accuracy after generation.
4. Inspect failures: extraction, segmentation, embedding, ranking, context packing, or model use.
5. Re-index under a new document/version identity after a material splitter change.

## Gotchas

- **Issue: Flattening tables into unlabelled prose.** Row/column relationships disappear before retrieval. **Fix:** retain structured fields or render a stable, labelled representation with a source locator.
- **Issue: Using character counts for a token-limited model.** A chunk can overflow after formatting or multilingual tokenization. **Fix:** measure the final packed context with the deployment tokenizer.
- **Issue: Indexing duplicates created by overlap.** Retrieval can return near-identical chunks and hide diverse evidence. **Fix:** deduplicate or diversify results and justify overlap with evaluation data.
- **Issue: Re-indexing without a document version.** Old chunks can remain retrievable after a source changes. **Fix:** tie every chunk to an immutable document version and delete or filter superseded versions.

## See Also

- [[rag-pipeline]]
- [[embeddings]]
- [[tokenization]]
- [[vector-databases]]
- [[production-patterns]]

## Sources

- [LangChain retrieval overview](https://docs.langchain.com/oss/python/langchain/retrieval)
- [LangChain text splitters](https://python.langchain.com/docs/concepts/text_splitters/)
