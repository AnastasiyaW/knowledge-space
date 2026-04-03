---
title: LangGraph
category: frameworks
tags: [llm-agents, langgraph, state-machine, agent-graph, orchestration, workflow]
---

# LangGraph

LangGraph is a framework for building stateful, multi-step agent workflows as directed graphs. Part of the LangChain ecosystem but focused on complex agent orchestration with explicit control flow, typed state, and native support for cycles.

## Key Facts
- Agents are defined as graphs: nodes (functions) connected by edges (transitions)
- State is a typed dictionary passed between nodes
- Supports conditional routing, cycles (retry loops), and parallel execution
- Built-in interrupt nodes for human-in-the-loop
- More control than LangChain agents but requires explicit graph design

## LangGraph vs LangChain Agents

| Feature | LangChain Agents | LangGraph |
|---------|-----------------|-----------|
| Control flow | Implicit (LLM decides) | Explicit (graph defines) |
| State management | Limited (memory) | Rich (typed state dict) |
| Debugging | Hard (agent decides path) | Clear (follow graph edges) |
| Cycles/loops | Limited | Native support |
| Human-in-the-loop | Manual | Built-in interrupt nodes |

## Core Concepts

### State
```python
from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    messages: list
    next_step: str
    results: dict
```

### Nodes
Functions that receive state, process it, and return modified state:

```python
def research_node(state: AgentState) -> AgentState:
    result = search_tool.invoke(state["messages"][-1])
    state["results"]["research"] = result
    return state

def analyze_node(state: AgentState) -> AgentState:
    analysis = llm.invoke(f"Analyze: {state['results']['research']}")
    state["results"]["analysis"] = analysis
    return state
```

### Edges (including conditional)
```python
graph = StateGraph(AgentState)
graph.add_node("research", research_node)
graph.add_node("analyze", analyze_node)
graph.add_node("respond", respond_node)

# Simple edge
graph.add_edge("analyze", "respond")

# Conditional routing
graph.add_conditional_edges(
    "research",
    route_function,  # returns node name based on state
    {"needs_analysis": "analyze", "ready": "respond"}
)
```

### Compilation and Execution
```python
app = graph.compile()
result = app.invoke({
    "messages": [user_message],
    "next_step": "research",
    "results": {}
})
```

## Patterns

### Human-in-the-Loop
```python
def human_review_node(state):
    action = state["proposed_action"]
    approval = get_human_approval(action)
    state["approved"] = approval
    return state

graph.add_node("propose", agent_propose)
graph.add_node("review", human_review_node)
graph.add_node("execute", agent_execute)

graph.add_edge("propose", "review")
graph.add_conditional_edges(
    "review",
    lambda s: "execute" if s["approved"] else "propose",
    {"execute": "execute", "propose": "propose"}
)
```

### Retry Loop
```python
def should_retry(state):
    if state["quality_score"] < 0.8 and state["attempts"] < 3:
        return "retry"
    return "done"

graph.add_conditional_edges("evaluate", should_retry, {
    "retry": "generate",
    "done": "output"
})
```

### Multi-Agent Graph
```python
# Supervisor routes to specialized agents
graph.add_node("supervisor", supervisor_node)
graph.add_node("researcher", research_agent)
graph.add_node("writer", writing_agent)

graph.add_conditional_edges(
    "supervisor",
    lambda s: s["next_agent"],
    {"research": "researcher", "write": "writer", "done": END}
)
graph.add_edge("researcher", "supervisor")
graph.add_edge("writer", "supervisor")
```

## When to Use LangGraph
- Multi-step workflows with conditional branching
- Agents needing explicit state management
- Human-in-the-loop approval steps
- Complex multi-agent orchestration
- Workflows requiring retry logic or iterative refinement
- When you need to debug exactly which path the agent took

## Gotchas
- Graph design requires upfront planning - more work than a simple ReAct agent
- State must be serializable for persistence/checkpointing
- Conditional edge functions must handle all possible state values
- Cycles without termination conditions create infinite loops
- Debugging requires understanding the full graph structure, not just individual nodes

## See Also
- [[langchain-framework]] - Foundation framework that LangGraph extends
- [[agent-design-patterns]] - Patterns implemented as graphs
- [[multi-agent-systems]] - Multi-agent patterns in graph form
- [[agent-memory]] - Human-in-the-loop patterns
