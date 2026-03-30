---
title: Vector Databases
category: llm-agents/infrastructure
tags: [vector-db, chroma, pinecone, faiss, qdrant, weaviate, milvus, similarity-search]
---

# Vector Databases

## Key Facts

- Vector databases store [[embeddings]] and enable fast similarity search over millions/billions of vectors
- Core operation: given a query vector, find the top-K nearest neighbors by distance metric
- Distance metrics: **cosine similarity** (direction), **Euclidean/L2** (magnitude), **dot product** (scaled similarity)
- Indexing algorithms: HNSW (most common, fast approximate), IVF (inverted file), PQ (product quantization for compression)
- Critical for [[rag-pipeline]] - store document chunk embeddings, retrieve relevant chunks at query time
- Categories: **managed** (Pinecone, Weaviate Cloud) vs **self-hosted** (Chroma, Qdrant, Milvus, pgvector)

### Comparison

| Database | Type | Best For | Notes |
|----------|------|----------|-------|
| ChromaDB | Embedded/self-hosted | Prototyping, small-medium | Python-native, in-memory or persistent |
| Pinecone | Managed SaaS | Production, serverless | Free tier available, fully managed |
| Qdrant | Self-hosted/cloud | High performance | Rust-based, rich filtering |
| pgvector | Postgres extension | Existing Postgres stacks | SQL interface, ACID transactions |
| FAISS | Library (Meta) | Research, batch search | No server, in-memory, very fast |
| Weaviate | Self-hosted/cloud | Multi-modal, GraphQL | Built-in vectorization modules |
| Milvus | Self-hosted/cloud | Billion-scale | Distributed, GPU-accelerated |

## Patterns

```python
# ChromaDB - simplest local vector store
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

# Add documents (auto-embeds with default model)
collection.add(
    documents=["Cat is an animal", "Dog is a pet", "Python is a language"],
    ids=["doc1", "doc2", "doc3"],
    metadatas=[{"source": "wiki"}, {"source": "wiki"}, {"source": "docs"}]
)

# Query
results = collection.query(
    query_texts=["furry pet"],
    n_results=2,
    where={"source": "wiki"}  # metadata filtering
)
```

```python
# FAISS - fast similarity search (no server needed)
import faiss
import numpy as np

d = 1536  # dimension
index = faiss.IndexFlatL2(d)  # exact search
# index = faiss.IndexIVFFlat(quantizer, d, nlist)  # approximate

vectors = np.random.random((1000, d)).astype('float32')
index.add(vectors)

query = np.random.random((1, d)).astype('float32')
distances, indices = index.search(query, k=5)
```

```python
# pgvector - Postgres-native
# CREATE EXTENSION vector;
# CREATE TABLE docs (id serial, embedding vector(1536), content text);
# CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops);

# SELECT content, embedding <=> query_vector AS distance
# FROM docs ORDER BY distance LIMIT 5;
```

## Gotchas

- **Embedding dimension must match**: index dimension must equal your embedding model's output dimension
- **ANN is approximate**: HNSW/IVF may miss exact nearest neighbors. Tune `ef_search`/`nprobe` for recall vs speed
- **Metadata filtering first**: filter by metadata before vector search to reduce search space
- **Index rebuild cost**: changing distance metric or dimensions requires full re-indexing
- **Memory requirements**: 1M vectors x 1536 dims x 4 bytes = ~6GB RAM for FAISS flat index
- **ChromaDB limitations**: not designed for production at scale (>1M vectors). Use Qdrant/Pinecone/Milvus
- **Hybrid search**: combine vector similarity with keyword search (BM25) for best retrieval quality

## See Also

- [[embeddings]] - vectors that populate the database
- [[rag-pipeline]] - the pipeline that uses vector search
- [[langchain]] - framework with vector store integrations
- https://docs.trychroma.com/ - ChromaDB documentation
- https://docs.pinecone.io/ - Pinecone documentation
- https://github.com/facebookresearch/faiss - FAISS library
