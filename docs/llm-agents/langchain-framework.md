---
title: LangChain Framework
category: frameworks
tags: [llm-agents, langchain, lcel, chains, agents, rag, framework]
---

# LangChain Framework

LangChain is a Python/JS framework providing abstractions for building LLM applications: chains, agents, RAG, memory. It offers a unified interface across providers and composable patterns via LCEL (LangChain Expression Language).

## Key Facts
- Unified API for OpenAI, Anthropic, Ollama, Google, and many other providers
- LCEL pipe syntax (`prompt | llm | parser`) for composing chains
- Includes document loaders, text splitters, vector store integrations, memory, and agent toolkits
- LangSmith companion provides tracing, evaluation, and monitoring
- For simple prompts, plain Python may suffice - LangChain adds value for complex pipelines

## Core Components

### Models
```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama

llm = ChatOpenAI(model="gpt-4", temperature=0)
response = llm.invoke("Hello")  # same interface for all providers
```

### Prompts
```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specialized in {domain}"),
    ("human", "{question}")
])

chain = prompt | llm  # LCEL pipe syntax
response = chain.invoke({"domain": "finance", "question": "What is ROI?"})
```

### Chains (LCEL)
```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"domain": "legal", "question": "What is a tort?"})
```

### Document Loaders
```python
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

loader = PyPDFLoader("report.pdf")
docs = loader.load()
```

### Text Splitters
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
```

### Vector Stores
```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
```

### Memory
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(return_messages=True)
# Also: ConversationSummaryMemory, ConversationBufferWindowMemory
```

## Advanced LCEL Patterns

### RunnablePassthrough

Identity function in LangChain - passes input through unchanged. Used to route data in complex chain compositions:

```python
from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()
passthrough.invoke("hello")  # -> "hello"
passthrough.invoke([1, 2, 3])  # -> [1, 2, 3]
```

Primary use: carry original input alongside chain output for downstream processing.

### Piping Chains Together

Chain output from one prompt into another using LCEL pipe syntax:

```python
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4")

# Chain 1: list tools for a profession
tools_prompt = ChatPromptTemplate.from_template(
    "List the 5 most essential tools for a {profession}."
)
tools_chain = tools_prompt | llm | StrOutputParser()

# Chain 2: strategies to master those tools
strategy_prompt = ChatPromptTemplate.from_template(
    "Given these tools: {tools}\nSuggest strategies to master them."
)
strategy_chain = strategy_prompt | llm | StrOutputParser()

# Pipe: output of chain 1 feeds into chain 2
full_chain = tools_chain | (lambda tools: {"tools": tools}) | strategy_chain
result = full_chain.invoke({"profession": "data engineer"})
```

### RunnableParallel

Execute multiple runnables concurrently with the same input:

```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    books=books_chain,      # "Recommend books for {topic}"
    projects=projects_chain  # "Suggest projects for {topic}"
)
result = parallel.invoke({"topic": "machine learning"})
# result = {"books": "...", "projects": "..."}

# Feed parallel results into a downstream chain
time_prompt = ChatPromptTemplate.from_template(
    "Given books: {books} and projects: {projects}, estimate completion time."
)
full_chain = parallel | time_prompt | llm | StrOutputParser()
```

`RunnableParallel` runs branches concurrently (uses asyncio under the hood). For chains with multiple independent LLM calls, this is significantly faster than sequential execution.

### MarkdownHeaderTextSplitter

Splits documents by markdown headers, preserving document structure in metadata:

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers_to_split = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split)
chunks = splitter.split_text(markdown_text)
# Each chunk retains header hierarchy in metadata:
# chunks[0].metadata = {"h1": "Introduction", "h2": "Background"}
```

Use when documents have meaningful header structure (documentation, wiki pages, reports). Produces semantically coherent chunks compared to character-count splitting.

## Patterns

### RAG Chain
```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

chain = create_retrieval_chain(
    retriever,
    create_stuff_documents_chain(llm, prompt)
)
result = chain.invoke({"input": "What is the company revenue?"})
print(result["answer"])
print(result["context"])  # retrieved documents
```

### Conversational RAG
```python
from langchain.chains import ConversationalRetrievalChain

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True
)
```

### LangChain Agents
```python
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return web_search(query)

agent = create_openai_tools_agent(llm, [search_web], prompt)
executor = AgentExecutor(agent=agent, tools=[search_web], verbose=True)
result = executor.invoke({"input": "Latest news about AI agents"})
```

## LangSmith Monitoring

Observability platform for LLM applications:
- **Tracing**: full trace of chain/agent execution (inputs, outputs, latency per step)
- **Evaluation**: run test datasets, measure quality
- **Monitoring**: production metrics, error rates, token usage
- **Datasets**: manage test/evaluation datasets

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "lsv2_..."
# All LangChain operations automatically traced
```

When an agent fails in production, LangSmith shows the exact chain of thought, tool calls, and failure point.

## Gotchas
- LangChain adds abstraction overhead - for simple prompt+response, use the provider SDK directly
- LCEL pipe syntax is concise but can be hard to debug for complex chains
- Version compatibility: LangChain evolves rapidly, breaking changes between versions
- Memory implementations have limitations - ConversationBufferMemory grows unbounded
- verbose=True on AgentExecutor is essential for debugging but noisy in production

## See Also
- [[langgraph]] - Graph-based agent orchestration (LangChain ecosystem)
- [[rag-pipeline]] - RAG patterns using LangChain components
- [[function-calling]] - Tool use that LangChain wraps
- [[agent-fundamentals]] - Agent concepts LangChain implements
- [[llmops]] - LangSmith for production monitoring
