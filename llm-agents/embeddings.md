---
title: Embeddings
category: llm-agents/representations
tags: [embeddings, vectors, semantic-search, text-embedding, similarity]
---

# Embeddings

## Key Facts

- Embeddings convert text (words, sentences, documents) into dense numerical vectors in high-dimensional space
- Semantically similar texts produce vectors that are close together (measured by cosine similarity or dot product)
- Embedding models are separate from generation models - they encode meaning, not generate text
- Standard dimensions: 384 (MiniLM), 768 (BERT), 1536 (OpenAI ada-002), 256-3072 (text-embedding-3)
- Key property: `similarity("cat", "dog") > similarity("cat", "airplane")`
- Used in [[rag-pipeline]], [[vector-databases]], semantic search, clustering, classification, anomaly detection
- Two families: **sparse** (BM25/TF-IDF, keyword-based) and **dense** (neural, semantic meaning)

## Patterns

```python
# OpenAI embeddings
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",  # 1536 dims, cheapest
    input=["Your text here", "Another text"]
)
vectors = [item.embedding for item in response.data]

# Cosine similarity
import numpy as np
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

```python
# HuggingFace sentence-transformers (local, free)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dims
embeddings = model.encode(["cat", "dog", "airplane"])
# embeddings[0] @ embeddings[1] > embeddings[0] @ embeddings[2]
```

```python
# Dimensionality reduction for visualization
from openai import OpenAI
client = OpenAI()

# text-embedding-3 supports native dimension reduction
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello world",
    dimensions=256  # reduce from 1536 to 256
)
```

## Gotchas

- **Model lock-in**: once you embed with a model, switching requires re-embedding everything. Choose carefully
- **Max input length**: most models truncate at 512 or 8192 tokens. Long documents need [[chunking-strategies]]
- **Not all embeddings are equal**: models trained on different data excel at different tasks. E5, BGE, GTE often outperform general-purpose models on retrieval
- **Cosine vs dot product**: normalized vectors make cosine = dot product. Some vector DBs default to one or the other
- **Batch embedding**: always batch API calls (up to 2048 inputs per call with OpenAI) for cost efficiency
- **Stale embeddings**: if underlying data changes, vectors must be re-computed
- **Multilingual**: not all models handle non-English well. Use multilingual-e5-large or cohere-multilingual

## See Also

- [[rag-pipeline]] - primary consumer of embeddings
- [[vector-databases]] - where embeddings are stored and searched
- [[tokenization]] - how text is split before embedding
- https://huggingface.co/spaces/mteb/leaderboard - MTEB embedding benchmark
- https://platform.openai.com/docs/guides/embeddings - OpenAI embeddings docs
- https://www.sbert.net/ - Sentence Transformers library
