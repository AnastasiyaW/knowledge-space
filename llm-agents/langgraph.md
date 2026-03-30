---
title: LangGraph
category: llm-agents/frameworks
tags: [langgraph, agent-graph, state-machine, multi-agent, orchestration, workflow-engine]
---

# LangGraph

## Key Facts

- LangGraph is a framework for building stateful, multi-step agent applications as directed graphs
- Built on top of [[langchain]] but designed specifically for agentic workflows with cycles and branching
- Core concepts: **Nodes** (functions/LLM calls), **Edges** (transitions), **State** (shared data between nodes)
- Unlike linear chains, LangGraph supports **cycles** (agent loops), **conditional branching**, and **human-in-the-loop**
- State is a typed dictionary that flows through the graph - each node reads and updates it
- Built-in persistence: checkpoint state to resume interrupted workflows
- FlowWise provides a drag-and-drop UI that uses LangGraph under the hood
- Primary use case: complex agents that need deterministic control flow with LLM flexibility

## Patterns

```python
# Basic LangGraph agent
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    messages: Annotated[list, add]
    next_step: str

def call_model(state: AgentState) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"
    return END

def call_tools(state: AgentState) -> dict:
    # Execute tool calls from last message
    results = execute_tools(state["messages"][-1].tool_calls)
    return {"messages": results}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", call_tools)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")  # cycle back after tool execution

app = graph.compile()
result = app.invoke({"messages": [HumanMessage("What's 2+2?")]})
```

```python
# Human-in-the-loop with interrupt
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["dangerous_action"]  # pause before this node
)

# Run until interrupt
config = {"configurable": {"thread_id": "1"}}
result = app.invoke(input, config)

# Resume after human approval
app.invoke(None, config)  # continues from checkpoint
```

```python
# Multi-agent with supervisor
def supervisor(state):
    """Route to the right specialist agent."""
    response = llm.invoke(
        f"Given the task: {state['task']}, "
        f"which agent should handle it? Options: researcher, writer, coder"
    )
    return {"next_agent": response.content.strip()}

graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher_agent)
graph.add_node("writer", writer_agent)
graph.add_conditional_edges("supervisor", route_to_agent)
```

## Gotchas

- **State management**: all nodes share state. Careless mutations cause hard-to-debug issues
- **Graph complexity**: deep graphs with many conditional edges become hard to reason about
- **Checkpointing overhead**: persistence adds latency. Use in-memory checkpointer for development
- **Streaming**: LangGraph supports streaming but requires careful node design for partial outputs
- **Debugging**: use LangSmith integration for graph execution traces
- **Not for simple chains**: if your workflow is linear (A->B->C), use plain [[langchain]] LCEL instead

## See Also

- [[langchain]] - foundation framework LangGraph builds on
- [[agent-architectures]] - patterns implemented as graphs
- [[multi-agent-systems]] - multi-agent coordination
- [[memory-and-context]] - state persistence across interactions
- https://langchain-ai.github.io/langgraph/ - LangGraph documentation
- https://github.com/langchain-ai/langgraph - LangGraph source code
