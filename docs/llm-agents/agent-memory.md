---
title: Agent Memory
category: concepts
tags: [llm-agents, memory, context-management, conversation-history, human-in-the-loop]
---

# Agent Memory

Agent memory systems manage context across interactions - from short-term conversation buffers to persistent long-term knowledge stores. Since LLMs are stateless (each API call is independent), memory must be explicitly managed.

## Key Facts
- LLMs are stateless - the client must send full conversation history with each request
- Token usage grows with conversation length - must be managed (truncation, summarization, windowing)
- System prompt + retrieved context + history + new message must all fit in context window
- Long-term memory persists across sessions via vector stores, databases, or file systems

## Memory Types

### Short-Term (Conversation Buffer)
Current dialogue history, cleared when session ends.

```python
from langchain.memory import ConversationBufferMemory
# Stores all messages (grows unbounded)

from langchain.memory import ConversationBufferWindowMemory
# Keeps last K exchanges (sliding window)

from langchain.memory import ConversationSummaryMemory
# Summarizes old messages, keeps recent ones verbatim
```

### Long-Term Memory
Persists across sessions. Stored in vector databases, traditional databases, or file systems. Enables remembering user preferences, past interactions, learned facts.

### Episodic Memory
Specific interaction records: "Last time user asked about X, the answer was Y." Useful for personalization and avoiding repeated work.

### Semantic Memory
General accumulated knowledge. Domain-specific facts, company information. Usually implemented as a RAG knowledge base.

### Working Memory (Scratchpad)
Agent's intermediate reasoning during task execution. Accumulated thoughts, actions, observations in the ReAct loop. Grows with each step and must be managed.

## Memory Management Strategies

| Strategy | Mechanism | Tradeoff |
|----------|-----------|----------|
| **Truncation** | Drop oldest messages | Simple, but loses early context |
| **Summarization** | Periodically summarize older conversation | Preserves key info, costs tokens to summarize |
| **Selective retention** | Keep important messages, drop filler | Best quality, hardest to implement |
| **External storage** | Write to DB, retrieve relevant parts on demand | Unlimited history, but adds retrieval latency |
| **Sliding window** | Keep last K exchanges | Predictable cost, loses older context |

## Human-in-the-Loop (HITL)

### Why HITL
- Agent actions have real-world consequences (sending emails, modifying data)
- LLMs make mistakes - human oversight catches errors
- Compliance/regulatory requirements may mandate human approval
- Builds trust during agent deployment

### HITL Patterns

**Approval gate**: agent proposes action, waits for human approval:
```python
from langgraph.graph import StateGraph

def human_review_node(state):
    action = state["proposed_action"]
    approval = get_human_approval(action)  # UI, webhook, etc.
    state["approved"] = approval
    return state

graph.add_node("propose_action", agent_propose)
graph.add_node("human_review", human_review_node)
graph.add_node("execute_action", agent_execute)

graph.add_conditional_edges(
    "human_review",
    lambda s: "execute" if s["approved"] else "revise",
    {"execute": "execute_action", "revise": "propose_action"}
)
```

**Escalation**: agent handles simple cases autonomously, escalates complex/uncertain cases to human.

**Copilot pattern**: automate boring/repetitive parts, keep human for judgment. Agent handles 70-80% of work, human reviews in seconds. 3x productivity gain typical.

**Feedback loop**: human corrections after agent acts improve future performance.

## Conversation History Management

```python
# Stateless API - must send full history each time
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "First question"},
    {"role": "assistant", "content": "First answer"},
    {"role": "user", "content": "Follow-up question"}
]
response = client.chat.completions.create(model="gpt-4", messages=messages)
```

Track token count and trim when approaching the limit. Keep system prompt and recent messages, summarize or drop older ones.

## Gotchas
- Conversation history grows unbounded without management - eventually exceeds context window
- Summary memory loses nuance - critical details may be dropped
- External memory (vector store) adds retrieval latency to every query
- Human-in-the-loop adds latency but prevents costly mistakes
- Never assume the agent "remembers" from a previous session without explicit long-term memory
- Memory retrieval (via embeddings) has the same cosine similarity failures as RAG

## See Also
- [[agent-fundamentals]] - Where memory fits in agent architecture
- [[agent-design-patterns]] - Scratchpad management in agent loops
- [[rag-pipeline]] - Long-term memory via retrieval
- [[vector-databases]] - Storage for persistent memory
- [[tokenization]] - Context window constraints on memory
