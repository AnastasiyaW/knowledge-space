---
title: LLM Memory & Knowledge Persistence
type: MOC
---

# LLM Memory & Knowledge Persistence

Patterns and architectures for organizing persistent knowledge when working with LLM agents. Not about building RAG systems (see [[agent-fundamentals]]) - about how agents remember, forget, and manage knowledge across sessions.

## Memory Architecture
- [[memory-architectures]] - Flat files, hierarchical graphs, vector stores, knowledge graphs, hybrid approaches
- [[verbatim-vs-extraction]] - Why raw text beats LLM extraction (96.6% vs 85%), when to use each

## Context & Window Management
- [[context-window-management]] - Layered loading (L0-L3), token budgets, compaction, re-injection patterns

## Knowledge Organization
- [[knowledge-base-as-memory]] - Raw->wiki->schema pipeline, plain markdown vs RAG, ingest/query/lint operations
- [[session-persistence]] - Handoff files, memory files, state files, journal patterns

## Temporal & Retrieval
- [[temporal-memory]] - Validity periods, staleness detection, time-decay, contradiction resolution
- [[memory-retrieval-patterns]] - Index navigation, BM25, vector, hybrid search, reranking, cost comparison

## Memory Lifecycle
- [[forgetting-strategies]] - Compaction, archival, TTL, relevance scoring, memory size management
