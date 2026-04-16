---
title: Vector Databases
category: infrastructure
tags: [llm-agents, vector-db, chroma, pinecone, qdrant, faiss, ann, similarity-search]
---

# Vector Databases

Vector databases store embedding vectors and enable fast similarity search. They are the persistence and retrieval layer for RAG systems, semantic search, and recommendation engines.

## Key Facts
- Vector DBs use Approximate Nearest Neighbor (ANN) algorithms for sub-linear search time
- Exact nearest neighbor is O(n) - impractical for millions of vectors
- Metadata filtering allows pre-filtering before similarity search
- In-memory stores (Chroma, FAISS) are fast but don't persist across restarts without explicit saving
- Hybrid search (vector + keyword/BM25) catches both semantic and lexical matches

## Database Comparison

| Database | Type | Best For | Key Feature |
|----------|------|----------|-------------|
| **Chroma** | Embedded/server | Prototyping, small projects | Simple API, Python-native, in-memory |
| **Pinecone** | Managed cloud | Production at scale | Fully managed, auto-scaling, metadata filtering |
| **Qdrant** | Self-hosted/cloud | Production with control | Rust-based, fast, rich filtering, payload storage |
| **Weaviate** | Self-hosted/cloud | Multimodal search | GraphQL API, hybrid search built-in |
| **FAISS** | Library (Meta) | Research, high-performance | Fastest similarity search, GPU support, no built-in persistence |
| **pgvector** | PostgreSQL extension | Existing Postgres stack | SQL integration, ACID transactions, familiar tooling |

## ANN Algorithms

### HNSW (Hierarchical Navigable Small World)
- Most popular in production vector DBs
- Builds layered graph structure, O(log n) search
- High recall (>95%) at very fast speeds
- Memory-intensive (stores graph in RAM)

### IVF (Inverted File Index)
- Clusters vectors, searches only relevant clusters
- Lower memory than HNSW
- Good for very large datasets
- Slightly lower recall

### Indexing Strategy Selection

| Strategy | Dataset Size | Memory | Speed | Accuracy |
|----------|-------------|--------|-------|----------|
| Flat | <100K vectors | High | Slow (exact) | Perfect |
| IVF-Flat | Medium | Medium | Fast | Good |
| IVF-PQ | Large | Low | Fast | Moderate |
| HNSW | Any | High | Very fast | Very good |

## FAISS vs Chroma: Practical Comparison

FAISS (Facebook AI Similarity Search) and Chroma are both commonly used with LangChain, but serve different purposes:

| Aspect | FAISS | Chroma |
|--------|-------|--------|
| **Type** | Library (similarity search) | Database (embedded/server) |
| **Persistence** | In-memory only (manual save/load) | Persistent on disk by default |
| **Best for** | High-performance search, research | Prototyping, small-to-medium apps |
| **GPU support** | Yes (massive speedup) | No |
| **Metadata filtering** | Limited (via IDSelector) | Built-in |
| **Install** | `pip install faiss-cpu` or `faiss-gpu` | `pip install chromadb` |

### Swapping Vector Stores in LangChain

LangChain's abstractions make switching trivial - same retriever interface:

```python
# Option A: Chroma (persistent, simpler)
from langchain_community.vectorstores import Chroma
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

# Option B: FAISS (in-memory, faster search)
from langchain_community.vectorstores import FAISS
vectorstore = FAISS.from_documents(chunks, embeddings)
# To save: vectorstore.save_local("./faiss_index")
# To load: vectorstore = FAISS.load_local("./faiss_index", embeddings)

# Both use identical retriever interface
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
results = retriever.invoke("query text")
```

**When to use FAISS**: need raw search speed, have GPU available, dataset fits in memory, don't need complex metadata filtering. FAISS is the standard choice for benchmarks and research.

**When to use Chroma**: need persistence across restarts, want metadata filtering, building RAG prototypes, don't want to manage save/load. Chroma is the default choice for LangChain tutorials.

## Patterns

### Metadata Filtering (Qdrant)
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

client = QdrantClient("localhost", port=6333)
results = client.search(
    collection_name="docs",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="source", match=MatchValue(value="annual_report")),
            FieldCondition(key="year", range=Range(gte=2023))
        ]
    ),
    limit=5
)
```

### LangChain Vector Store
```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
results = retriever.invoke("What is the company revenue?")
```

### Hybrid Search
Combine vector similarity with keyword/BM25 search:

```toml
hybrid_score = alpha * vector_score + (1 - alpha) * bm25_score
```

**Reciprocal Rank Fusion (RRF)**: Alternative merging without tuning alpha:
```toml
score = sum(1 / (rank + k)) across all search methods
```

## Gotchas
- In-memory vector stores lose data on restart - always persist for production
- FAISS is a library, not a database - no built-in CRUD, persistence, or filtering
- pgvector performance degrades with millions of vectors without proper index tuning
- Metadata filtering happens before vector search in most DBs - design metadata schema carefully
- Index building can be slow for large datasets - plan for initial indexing time
- Different distance metrics (cosine, L2, dot product) can give different ranking results - match to your embedding model's training

## See Also
- [[embeddings]] - How text becomes vectors for storage
- [[rag-pipeline]] - How vector search fits in the RAG pipeline
- [[chunking-strategies]] - Preparing documents for vector storage
- [[production-patterns]] - When to use vector search vs deterministic lookup
