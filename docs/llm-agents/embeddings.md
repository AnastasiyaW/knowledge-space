---
title: Embeddings
category: concepts
tags: [llm-agents, embeddings, vectors, semantic-search, similarity, cosine]
---

# Embeddings

Embeddings convert text into high-dimensional numeric vectors where proximity represents semantic similarity. They are the foundation of vector search, RAG systems, and semantic understanding in LLM applications.

## Key Facts
- Embedding models produce fixed-size vectors (e.g., 1536 dimensions for OpenAI text-embedding-3-large)
- Points close in vector space are semantically similar
- Embeddings capture meaning, not exact words - "car" and "automobile" are close, "bank" (financial) and "bank" (river) are far
- Modern models classify text on ~1000+ abstract features - individual dimensions don't have interpretable meaning

## Similarity Metrics

**Cosine similarity** is the standard metric - measures the angle between vectors:

```python
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))
# Range: -1 to 1 (1 = identical direction)
```

Other metrics: Euclidean distance (L2), dot product (when vectors are normalized, equals cosine similarity).

## Embedding Models

| Model | Dimensions | Provider | Notes |
|-------|-----------|----------|-------|
| text-embedding-3-large | 1536/3072 | OpenAI | Adjustable dimensions via `dimensions` param |
| text-embedding-3-small | 512/1536 | OpenAI | Cheaper, lower quality |
| BGE-large | 1024 | BAAI | Open-source, strong performance |
| E5-large | 1024 | Microsoft | Good for retrieval tasks |
| Cohere embed-v3 | 1024 | Cohere | Multilingual, search-optimized |
| Ollama embeddings | Varies | Local | Use same Ollama server, free, private |

## Patterns

### Generate Embeddings (OpenAI)
```python
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="What is machine learning?"
)
vector = response.data[0].embedding  # list of floats
```

### Generate Embeddings (LangChain)
```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector = embeddings.embed_query("What is machine learning?")
doc_vectors = embeddings.embed_documents(["doc1", "doc2", "doc3"])
```

### Test-Time Reranking
After initial embedding retrieval, use a cross-encoder to rerank by fine-grained relevance:

```python
from sentence_transformers import CrossEncoder

cross = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
pairs = [(query, candidate) for candidate in candidates]
scores = cross.predict(pairs)
best_idx = int(scores.argmax())
```

### Self-Consistency (Best-of-N)
Sample N answers, pick most frequent - embeddings can measure answer similarity for clustering:

```python
import collections
def majority_vote(candidates):
    return collections.Counter(candidates).most_common(1)[0]
```

## Visualizing Embeddings with t-SNE

Since embeddings have 1000+ dimensions, use dimensionality reduction to project them to 2D or 3D for visual inspection:

```python
from sklearn.manifold import TSNE
import plotly.graph_objects as go
import numpy as np

# Get all embeddings from vector store
collection = vectorstore._collection
result = collection.get(include=["embeddings", "documents", "metadatas"])
vectors = np.array(result["embeddings"])

# Project to 2D
tsne = TSNE(n_components=2, random_state=42)
reduced = tsne.fit_transform(vectors)

# Color by document type
colors = [metadata.get("source_type", "unknown") for metadata in result["metadatas"]]
color_map = {"employee": "green", "contract": "red", "product": "blue", "company": "gold"}

fig = go.Figure(data=go.Scatter(
    x=reduced[:, 0], y=reduced[:, 1],
    mode="markers",
    marker=dict(color=[color_map.get(c, "gray") for c in colors]),
    text=[doc[:100] for doc in result["documents"]],  # hover text
    hoverinfo="text"
))
fig.show()
```

**What you observe:** Documents cluster by semantic similarity - employee records group together, product descriptions cluster separately, contract terms sit near product features (shared vocabulary). The embedding model was never told document types - it inferred semantic structure purely from content.

**3D projection** (`n_components=3`) gives rotatable views but is often less clear than 2D. Use `go.Scatter3d` with the same pattern.

**Practical use:** Embedding visualization reveals:
- Whether chunks from different sources are semantically separated (good for retrieval precision)
- Outlier documents that may be mislabeled or irrelevant
- Cross-topic overlap zones where retrieval might return unexpected results

## Known Issues

- **Non-determinism**: OpenAI embeddings produce slightly different vectors across API calls for the same text. Small absolute differences but breaks deterministic unit tests.
- **Cosine similarity misses**: can fail to find obviously present text. String/keyword match succeeds where embedding search falls below typical 0.6 threshold.
- **Semantic vs lexical confusion**: "risk of liquidity" may match "liquidity amount" even though they mean different things.
- **Embedding model must match**: query and documents must use the same embedding model. Mixing models produces meaningless similarity scores.

## Gotchas
- Always use the same embedding model for indexing and querying - mixing models gives garbage results
- Embedding quality degrades for very short texts (1-2 words) and very long texts (beyond model's max input)
- Multilingual embeddings exist but cross-lingual similarity is weaker than same-language
- Embedding API calls add latency and cost to every query - consider caching for repeated queries
- Dimension reduction (e.g., text-embedding-3-large with fewer dimensions) trades quality for speed/cost

## See Also
- [[vector-databases]] - Storage and search for embedding vectors
- [[rag-pipeline]] - How embeddings power retrieval-augmented generation
- [[tokenization]] - Text to tokens before embedding
- [[chunking-strategies]] - Optimal text sizes for embedding
