---
title: LangChain
category: llm-agents/frameworks
tags: [langchain, chains, agents, framework, orchestration, llm-framework]
---

# LangChain

## Key Facts

- LangChain is the most widely adopted framework for building LLM-powered applications
- Core abstraction: chain together LLM calls, tools, retrievers, and memory into composable pipelines
- Ecosystem: **LangChain** (core library) -> **LangGraph** (agent graphs) -> **LangSmith** (observability) -> **LangServe** (deployment)
- Key components: Models, Prompts, Chains, Agents, Memory, Retrievers, Tools, Output Parsers
- LCEL (LangChain Expression Language): pipe syntax for composing chains: `prompt | llm | parser`
- Supports all major providers: OpenAI, Anthropic, Google, HuggingFace, Ollama, and 100+ integrations
- Higher-level tools built on LangChain: **FlowWise** (drag-and-drop UI), **LangFlow** (visual builder)
- Primary competitor: LlamaIndex (more RAG-focused)

## Patterns

```python
# LCEL chain composition
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()
result = chain.invoke({"input": "What is RAG?"})
```

```python
# RAG chain with retriever
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer based on context:\n{context}"),
    ("user", "{input}")
])

combine_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, combine_chain)

result = rag_chain.invoke({"input": "What is our return policy?"})
# result["answer"], result["context"]
```

```python
# Custom tool
from langchain.tools import tool

@tool
def search_database(query: str) -> str:
    """Search the product database for information."""
    # your database logic here
    return f"Results for: {query}"

# Use in agent
from langchain.agents import create_tool_calling_agent, AgentExecutor

agent = create_tool_calling_agent(llm, [search_database], prompt)
executor = AgentExecutor(agent=agent, tools=[search_database])
```

```python
# Conversation memory
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)
# ConversationSummaryMemory - summarizes old messages
# ConversationBufferWindowMemory - keeps last K messages
```

## Gotchas

- **Rapid API changes**: LangChain updates frequently. Pin versions, check migration guides
- **Over-abstraction**: for simple use cases, raw API calls are clearer and more maintainable
- **Debug difficulty**: deep chain nesting makes errors hard to trace. Use LangSmith for observability
- **Import confusion**: `langchain` vs `langchain_community` vs `langchain_openai` - packages were split
- **Memory isn't magic**: conversation memory still consumes context window tokens
- **LCEL learning curve**: pipe syntax is powerful but unfamiliar to many developers
- **Performance overhead**: LangChain adds latency over raw API calls. Matters for real-time applications

## See Also

- [[langgraph]] - graph-based agent orchestration (built on LangChain)
- [[rag-pipeline]] - RAG implementations in LangChain
- [[function-calling]] - tool integration patterns
- [[agent-architectures]] - agent patterns LangChain implements
- https://python.langchain.com/docs/ - LangChain Python documentation
- https://js.langchain.com/docs/ - LangChain JavaScript documentation
- https://smith.langchain.com/ - LangSmith observability platform
