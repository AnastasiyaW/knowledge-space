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

### DIY RAG (Keyword Matching)
The simplest possible RAG - string matching to inject relevant context:

```python
# Load documents into a dict: {"Lancaster": "Avery Lancaster, CEO...", "HomeElm": "..."}
context = {}
for f in os.listdir("knowledge_base/employees"):
    name = f.replace(".md", "").split("_")[-1]
    context[name] = open(f"knowledge_base/employees/{f}").read()

def get_relevant_context(message: str) -> list[str]:
    return [details for title, details in context.items()
            if title.lower() in message.lower()]

def add_context(message: str) -> str:
    relevant = get_relevant_context(message)
    if relevant:
        context_str = "\n\n".join(relevant)
        return f"{message}\n\nThe following context may help:\n{context_str}"
    return message
```

**Why this fails in production:**
- Case-sensitive: "lancaster" vs "Lancaster" breaks matching
- Requires exact keyword: "Avery" alone won't match if keyed by surname
- No semantic understanding: "Who founded the company?" returns nothing
- Fragile at scale: adding new document types requires new matching logic

This approach demonstrates *why* vector search exists - it replaces fragile string matching with semantic similarity. Use it only for prototyping or when the question space is fully known and small.

**Strong system prompts reduce hallucination in keyword RAG:**
```python
system = """You are an expert at answering questions about InsureElm.
Give brief, accurate answers.
If you don't know the answer, say so.
Do NOT make anything up if you lack relevant context."""
```

### Multi-Index RAG
Different document types in different indexes with different chunking strategies. Route queries to appropriate index based on question type.

## LangChain RAG Abstractions

LangChain provides three key abstractions that compose into a conversational RAG pipeline:

### LLM Abstraction
Wraps any language model (OpenAI, Anthropic, local) behind a unified interface:

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0)
```

### Retriever Abstraction
Interface for anything that returns documents given a query. Vector stores expose `.as_retriever()`:

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
# retriever.invoke("query") returns list of Document objects
```

### Memory Abstraction
Maintains conversation history for multi-turn RAG chat:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# ConversationalRetrievalChain combines all three
from langchain.chains import ConversationalRetrievalChain
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)
result = chain.invoke({"question": "What is the revenue?"})
```

### Document Indexing Pipeline

Full document-to-answer pipeline in LangChain:

1. **Load**: `DirectoryLoader`, `PyPDFLoader`, `WebBaseLoader`
2. **Split**: `RecursiveCharacterTextSplitter`, `CharacterTextSplitter`
3. **Embed**: `OpenAIEmbeddings`, `OllamaEmbeddings`
4. **Store**: `Chroma.from_documents()`, `FAISS.from_documents()`
5. **Retrieve + Generate**: chain with retriever + LLM

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load all PDFs from directory
loader = DirectoryLoader('./docs/', glob="**/*.pdf")
docs = loader.load()

# Split with overlap
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
)
chunks = splitter.split_documents(docs)

# Index
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())

# Manage: add, update, delete documents
vectorstore.add_documents(new_chunks)
vectorstore.delete(ids=["doc_id_1", "doc_id_2"])
```

### Vector Store Document Management

After initial indexing, vector stores need ongoing management:
- **Add**: `vectorstore.add_documents(new_docs)` - incremental indexing
- **Delete**: `vectorstore.delete(ids=[...])` - remove outdated docs
- **Update**: delete old version + add new version (no in-place update)
- **Inspect**: `vectorstore.get()` to view stored documents and metadata
- **Similarity search with score**: `vectorstore.similarity_search_with_score(query)` returns (doc, score) tuples

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
