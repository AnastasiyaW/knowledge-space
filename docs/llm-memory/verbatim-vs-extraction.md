---
title: Verbatim Storage vs LLM Extraction
category: concepts
tags: [llm-memory, verbatim, extraction, memory-quality, retrieval-accuracy]
---

# Verbatim Storage vs LLM Extraction

Whether to store raw text or LLM-extracted facts in memory. Empirically, raw verbatim text with default embeddings achieves 96.6% recall@5 on long-memory benchmarks, while extraction-based systems plateau around 85%. This is counterintuitive - but extraction is lossy.

## Key Facts

- Verbatim + default embeddings = 96.6% R@5 on LongMemEval without any LLM calls at retrieval time
- Extraction-based systems (Mem0, Zep) = ~85% R@5 - significantly worse despite using LLM at both write and read time
- Adding lightweight LLM rerank (~$0.001/query) pushes verbatim retrieval to ~100% (500/500)
- The gap exists because extraction discards context, nuance, and reasoning
- Cost difference: ~$10/year for verbatim storage vs ~$500/year for systems that summarize on every write

## Why Extraction Loses Information

When the LLM extracts "user prefers PostgreSQL" from a conversation, it loses:

1. **The reasoning**: "...because pgvector lets us do similarity search without a separate vector DB, and we already have Postgres in production"
2. **The context**: this preference was stated while evaluating databases for a specific ML pipeline project
3. **The constraints**: "...but only for datasets under 10M rows, beyond that we'd consider ClickHouse"
4. **The temporal context**: when this decision was made and what alternatives were considered
5. **The emotional weight**: "we tried MySQL for 3 months and it was painful" - signals strong preference

The extracted fact is technically correct but insufficient for the agent to reason well about future database decisions.

## Retrieval Quality Comparison

| Approach | R@5 | LLM Calls (Write) | LLM Calls (Read) | Cost/Year |
|----------|-----|-------------------|-------------------|-----------|
| Verbatim + embeddings | 96.6% | 0 | 0 | ~$10 |
| Verbatim + LLM rerank | ~100% | 0 | 1 (cheap) | ~$15 |
| Extraction (Mem0-style) | ~85% | 1 per write | 1 per read | ~$500 |
| Summarization | ~80% | 1 per write | 0-1 | ~$300 |

## When Verbatim Wins

- **Conversational memory**: user preferences, decisions, feedback - the *why* matters as much as the *what*
- **Episodic recall**: "what happened in that meeting?" - needs original phrasing, not a summary
- **Multi-step reasoning**: agent needs to reconstruct the chain of thought that led to a decision
- **Low-volume, high-value**: <100K entries where storage cost is negligible

## When Extraction Wins

- **Structured lookups**: "what is the user's timezone?" - a key-value fact, no nuance needed
- **Cross-session aggregation**: combining information from 50 conversations into a user profile
- **Storage-constrained environments**: embedded devices, edge deployments with limited storage
- **High-volume, low-value**: millions of entries where most will never be retrieved

## Patterns

### Hybrid: Verbatim + Extracted Index

Store both - verbatim for retrieval quality, extracted for structured access:

```python
def store_memory(text: str, metadata: dict):
    # Store verbatim for high-quality retrieval
    vector_store.add(
        documents=[text],
        metadatas=[metadata],
        ids=[generate_id()]
    )

    # Extract structured facts for direct lookup
    facts = extract_facts(text)  # LLM call
    for fact in facts:
        structured_store.upsert(
            key=fact["key"],
            value=fact["value"],
            source_id=metadata["id"],
            valid_from=metadata["timestamp"]
        )
```

### Verbatim with Metadata Enrichment

Skip LLM extraction but add structured metadata for filtering:

```python
def store_with_metadata(text: str, context: dict):
    metadata = {
        "timestamp": context["timestamp"],
        "wing": context.get("person", "general"),
        "room": context.get("topic", "misc"),
        "hall": classify_type(text),  # simple rule-based, not LLM
        "token_count": count_tokens(text),
    }
    vector_store.add(documents=[text], metadatas=[metadata])
```

### Compression Approaches That Preserve Quality

Lossy abbreviation schemes (custom dialects, acronym compression) empirically degrade retrieval. Tested on benchmarks: 96.6% baseline drops to 84.2% with aggressive compression. Token counting bugs in compression implementations are common - always validate with a proper tokenizer, not `len(text) // 3`.

Standard text compression (gzip) works at the storage level but doesn't reduce embedding costs since you decompress before embedding.

## Gotchas

- **LLM extraction has a fundamental information bottleneck.** The LLM must decide what's "important" at write time, but importance depends on future queries that haven't happened yet. Verbatim storage defers this decision to retrieval time, which has the query context
- **Token count estimation is error-prone.** Never use `len(text) // 3` or `len(text) // 4` to estimate tokens. Use a proper tokenizer (tiktoken for OpenAI, tokenizers for HuggingFace). Wrong estimates lead to incorrect cost comparisons and budget overflows
- **Verbatim doesn't mean unprocessed.** Clean the text before storing: remove UI artifacts, normalize whitespace, strip irrelevant metadata. The content should be verbatim, but the formatting should be clean

## See Also

- [[memory-architectures]]
- [[memory-retrieval-patterns]]
- [[embeddings]]
- [[chunking-strategies]]
- [[forgetting-strategies]]
