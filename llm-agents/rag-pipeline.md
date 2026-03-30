---
title: RAG Pipeline
category: llm-agents/retrieval
tags: [rag, retrieval-augmented-generation, vector-search, context-augmentation, knowledge-grounding]
---

# RAG Pipeline

## Key Facts

- RAG (Retrieval-Augmented Generation) injects external knowledge into LLM context at query time, bypassing the need for [[fine-tuning]]
- Standard pipeline: **documents -> chunking -> [[embeddings]] -> [[vector-databases]] -> retrieval -> prompt augmentation -> LLM generation**
- Primary use case: give LLMs access to private/current data without retraining
- RAG is cheaper and faster to deploy than fine-tuning; fine-tuning changes model behavior, RAG adds knowledge
- Context window limits constrain how many retrieved chunks can be injected (typical: 3-10 chunks)
- Quality depends heavily on chunking strategy, embedding model quality, and retrieval precision

## Patterns

```python
# Minimal RAG pipeline with OpenAI + ChromaDB
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " "]
)
chunks = splitter.split_documents(documents)

# 2. Embed and store
vectorstore = Chroma.from_documents(
    chunks,
    OpenAIEmbeddings(model="text-embedding-3-small")
)

# 3. Retrieve and generate
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    retriever=retriever,
    return_source_documents=True
)
result = qa_chain.invoke({"query": "What is the return policy?"})
```

```python
# Advanced: Hybrid search (keyword + semantic)
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

bm25 = BM25Retriever.from_documents(chunks, k=5)
semantic = vectorstore.as_retriever(search_kwargs={"k": 5})

hybrid = EnsembleRetriever(
    retrievers=[bm25, semantic],
    weights=[0.4, 0.6]
)
```

## Gotchas

- **Chunk size matters**: too small = lost context, too large = noise dilution. Start with 500-1000 chars with 10-20% overlap
- **Embedding model mismatch**: query and document must use the same embedding model
- **Garbage in, garbage out**: poor document parsing (especially PDFs with tables/images) degrades everything downstream. Use `unstructured`, `PyMuPDF`, or vision models for complex layouts
- **Lost in the middle**: LLMs attend less to middle context chunks. Put most relevant chunks first and last
- **Not a silver bullet**: RAG adds knowledge but doesn't change model behavior/tone. For style changes, use [[fine-tuning]]
- **Hallucination still possible**: LLM may ignore retrieved context or fabricate connections between chunks
- **Cost scaling**: each query embeds the question + retrieves + generates. High QPS = significant API costs

## See Also

- [[embeddings]] - vector representations used for semantic search
- [[vector-databases]] - storage and indexing for embedding vectors
- [[prompt-engineering]] - system prompt design for RAG contexts
- [[chunking-strategies]] - document splitting approaches
- https://docs.llamaindex.ai/en/stable/ - LlamaIndex RAG framework
- https://python.langchain.com/docs/tutorials/rag/ - LangChain RAG tutorial
- https://www.pinecone.io/learn/retrieval-augmented-generation/ - Pinecone RAG guide
