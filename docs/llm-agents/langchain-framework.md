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
