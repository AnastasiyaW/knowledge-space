---
title: RAG Pipeline
category: techniques
tags: [llm-agents, rag, retrieval-augmented-generation, vector-search, knowledge-grounding]
---

# RAG Pipeline

Retrieval-Augmented Generation (RAG) supplements LLM generation with external knowledge retrieved at query time. It addresses hallucination on domain-specific questions and knowledge cutoff limitations without retraining the model.

## Key Facts
- RAG = retrieve relevant documents + inject into prompt context + generate answer
- RAG for knowledge updates, fine-tuning for behavior/style changes - often combined in production
- Simple RAG works but has structural reliability issues - answers can change between runs and look plausible while being wrong
- Signal-to-noise ratio of retrieved context directly determines output quality
- Even GPT-4 with uploaded PDFs makes RAG-type errors - this is a structural problem, not a framework problem

## Pipeline Architecture

### Indexing Phase (Offline)
1. **Load documents**: PDFs, web pages, databases, APIs
2. **Split into chunks**: recursive character, sentence-based, or semantic chunking
3. **Generate embeddings**: OpenAI, BGE, E5, Cohere, or local models
4. **Store in vector database**: Chroma, Pinecone, Qdrant, Weaviate, FAISS, pgvector

### Query Phase (Online)
1. **User query** arrives
2. **Embed query** using same embedding model as indexing
3. **Retrieve** top-K similar chunks from vector DB (cosine similarity)
4. **Optionally rerank** with cross-encoder
5. **Augment prompt**: retrieved chunks + user query + system instructions
6. **Generate answer** via LLM
7. **Optionally cite sources**

### LangChain RAG Chain

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Index
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Query
llm = ChatOpenAI(model="gpt-4")
chain = create_retrieval_chain(
    retriever,
    create_stuff_documents_chain(llm, prompt)
)
result = chain.invoke({"input": "What is the company revenue?"})
print(result["answer"])
print(result["context"])  # retrieved documents
```

## The Hallucination Problem

**Root cause experiment**: Use a niche domain where the LLM wasn't trained. Without context, the model confidently gives wrong answers. With conflicting sources, answers vary between runs. With a single authoritative source clearly marked, answers become correct and consistent.

**Key insight**: LLMs trust whatever input they receive. If the model doesn't know the domain, it can't distinguish authoritative from forum-quality sources unless given structural hints (headers indicating source type).

## Improvement Strategies

### Better Retrieval
- **Hybrid search**: combine vector similarity + keyword/BM25 search. Reciprocal Rank Fusion (RRF) to merge results without tuning alpha.
- **Query expansion**: LLM generates multiple search queries from user question
- **HyDE**: LLM generates hypothetical answer, embed that for retrieval
- **Reranking**: after initial retrieval, cross-encoder reranks by fine-grained relevance
- **Metadata filtering**: filter by date, source, category before similarity search

### Better Generation
- **Source attribution**: include chunk source references in answers
- **Faithfulness check**: verify answer is grounded in retrieved context
- **Structured prompting**: "Only use provided context. Say 'I don't know' if insufficient."
- **Map-reduce for long documents**: ask same question per chunk, then synthesize partial answers

## Evaluation Metrics

| Metric | What It Measures |
|--------|-----------------|
| **Context Precision** | Fraction of retrieved chunks that are relevant |
| **Context Recall** | Fraction of relevant chunks that were retrieved |
| **Faithfulness** | Is the answer grounded in context (no hallucination)? |
| **Answer Relevancy** | Does the answer address the user's question? |

**Frameworks**: RAGAS (automated RAG evaluation), DeepEval, LangSmith

## Production Patterns

### Router + Specialized Agents
LLM router classifies question type, routes to specialized agents with curated knowledge bases for high-accuracy categories. Generic RAG handles the rest (hybrid approach).

### Knowledge Base Without Vector Search
For structured data or limited question types: prepare data tables/documents manually, load directly into prompt. More reliable than vector search for known categories.

### Multi-Index RAG
Different document types in different indexes with different chunking strategies. Route queries to appropriate index based on question type.

## Gotchas
- Simple RAG produces answers that change between runs and are often wrong - don't deploy without evaluation
- Vector search can miss obviously present text that keyword search finds easily (cosine similarity failures)
- Embedding the same text produces slightly different vectors across API calls (non-deterministic)
- "Garbage in, garbage out" - if retrieval returns irrelevant chunks, the LLM will hallucinate from them confidently
- Always verify documents were actually indexed (FlowWise: click "Upsert" button) - without this, RAG returns nothing
- RAG doesn't eliminate hallucination, it reduces it - always validate critical outputs

## See Also
- [[chunking-strategies]] - How to split documents for optimal retrieval
- [[vector-databases]] - Storage and search infrastructure
- [[embeddings]] - How text becomes searchable vectors
- [[production-patterns]] - Advanced RAG patterns for production
- [[llmops]] - Evaluating and monitoring RAG quality
