---
title: Memory and Context Management
category: llm-agents/agents
tags: [memory, context-window, conversation-history, short-term-memory, long-term-memory, context-management]
---

# Memory and Context Management

## Key Facts

- LLMs have no inherent memory - they only see what's in the current context window (prompt + history)
- When context window is full, oldest messages are lost. The model "forgets" earlier conversation
- Memory types: **short-term** (conversation buffer), **long-term** (vector store of past interactions), **entity** (structured facts)
- Context window = working memory. [[vector-databases]] = long-term memory. [[rag-pipeline]] = retrieval from long-term
- Key challenge: keeping relevant context while staying within token limits
- Strategies: sliding window, summarization, retrieval-augmented memory, entity extraction
- KV context caching: LLM providers cache repeated prompt prefixes for faster/cheaper repeated queries
- For [[agent-architectures]]: reflexion agents use persistent memory to learn from past episodes

## Patterns

```python
# LangChain memory types
from langchain.memory import (
    ConversationBufferMemory,       # keep all messages (simple, expensive)
    ConversationBufferWindowMemory, # keep last K messages
    ConversationSummaryMemory,      # summarize old messages
    ConversationEntityMemory,       # extract and track entities
)

# Buffer window - keeps last 10 exchanges
memory = ConversationBufferWindowMemory(k=10, return_messages=True)

# Summary - compresses old conversation into summary
memory = ConversationSummaryMemory(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    return_messages=True
)
```

```python
# Manual context management with summarization
def manage_context(messages: list, max_tokens: int = 100000) -> list:
    """Summarize old messages when context gets too large."""
    total_tokens = count_tokens(messages)

    if total_tokens > max_tokens:
        # Keep system prompt and last 5 messages
        system_msg = messages[0]
        recent = messages[-5:]
        old = messages[1:-5]

        # Summarize old messages
        summary = llm.invoke(
            f"Summarize this conversation concisely:\n"
            + "\n".join([m["content"] for m in old])
        )

        return [
            system_msg,
            {"role": "assistant", "content": f"[Previous conversation summary: {summary}]"},
            *recent
        ]
    return messages
```

```python
# Long-term memory with vector store
class LongTermMemory:
    def __init__(self, vectorstore):
        self.store = vectorstore

    def save(self, interaction: str, metadata: dict):
        """Save interaction to long-term memory."""
        self.store.add_texts([interaction], metadatas=[metadata])

    def recall(self, query: str, k: int = 3) -> list[str]:
        """Retrieve relevant past interactions."""
        docs = self.store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
```

## Gotchas

- **Context window != infinite memory**: even 200K tokens fills up with long conversations
- **Lost in the middle**: models attend less to middle-of-context content. Put important info at start/end
- **Summary quality**: automated summarization loses nuance. Critical details may be dropped
- **Entity memory drift**: extracted entities can become stale or contradictory over time
- **Cost of memory**: every token of history is re-sent on each API call. Long history = expensive
- **Hallucinated memories**: models may "remember" things that weren't said. Always verify against stored history
- **Session boundaries**: plan for context loss between sessions. Use persistent storage for important state

## See Also

- [[tokenization]] - context window limits and token counting
- [[rag-pipeline]] - retrieval-based memory augmentation
- [[vector-databases]] - persistent storage for long-term memory
- [[agent-architectures]] - how agents use memory (reflexion, plan-and-solve)
- https://python.langchain.com/docs/how_to/#memory - LangChain memory guides
