---
title: Agent Orchestration Frameworks
category: tools
tags: [llm-agents, orchestration, langgraph, crewai, autogen, workflow]
---

# Agent Orchestration Frameworks

Frameworks that handle the boilerplate of agent execution: state management, tool routing, multi-agent coordination, human-in-the-loop, and persistence. Choosing the right one depends on complexity needs and control requirements.

## Framework Comparison

| Framework | Control Level | Best For | Learning Curve |
|-----------|--------------|----------|----------------|
| LangGraph | High (explicit graph) | Complex stateful agents | Medium |
| CrewAI | Medium (role-based) | Team simulations | Low |
| AutoGen | Medium (conversation) | Multi-agent chat | Low |
| Semantic Kernel | High (.NET/Python) | Enterprise integration | Medium |
| Haystack | Medium (pipeline) | RAG + agent hybrid | Medium |
| Raw SDK | Full | Maximum flexibility | High |

## LangGraph

Graph-based agent orchestration. Nodes are functions, edges are transitions.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    plan: str
    current_step: int
    results: dict

def planner(state: AgentState) -> AgentState:
    plan = llm.invoke(f"Create plan for: {state['messages'][-1]}")
    return {"plan": plan.content, "current_step": 0}

def executor(state: AgentState) -> AgentState:
    step = state["plan"].split("\n")[state["current_step"]]
    result = execute_step(step, state["results"])
    return {
        "results": {**state["results"], f"step_{state['current_step']}": result},
        "current_step": state["current_step"] + 1
    }

def should_continue(state: AgentState) -> str:
    steps = state["plan"].split("\n")
    if state["current_step"] >= len(steps):
        return "respond"
    return "execute"

# Build graph
graph = StateGraph(AgentState)
graph.add_node("plan", planner)
graph.add_node("execute", executor)
graph.add_node("respond", responder)

graph.set_entry_point("plan")
graph.add_edge("plan", "execute")
graph.add_conditional_edges("execute", should_continue, {
    "execute": "execute",
    "respond": "respond"
})
graph.add_edge("respond", END)

app = graph.compile()
result = app.invoke({"messages": ["Research quantum computing trends"]})
```

### LangGraph Checkpointing

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Persistent state across sessions
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
app = graph.compile(checkpointer=checkpointer)

# Resume from checkpoint
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke({"messages": ["Continue where we left off"]}, config=config)
```

### Human-in-the-Loop with LangGraph

```python
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

# Interrupt before sensitive actions
graph.add_node("tools", ToolNode(tools))

def route_after_agent(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        tool_name = last_message.tool_calls[0]["name"]
        if tool_name in SENSITIVE_TOOLS:
            return "human_review"  # pause for approval
    return "tools"

# Compile with interrupt
app = graph.compile(interrupt_before=["human_review"])
```

## CrewAI

Role-based multi-agent with built-in task delegation:

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Senior Research Analyst",
    goal="Find comprehensive data on the topic",
    backstory="Expert researcher with 20 years experience",
    tools=[web_search, arxiv_search],
    llm="claude-sonnet",
    max_iter=5,
    verbose=True,
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear, accurate technical content",
    backstory="Award-winning technical writer",
    tools=[write_document],
    llm="claude-sonnet",
)

research_task = Task(
    description="Research the latest advances in {topic}",
    expected_output="Comprehensive research summary with sources",
    agent=researcher,
)

write_task = Task(
    description="Write a technical report based on the research",
    expected_output="Well-structured technical report, 2000 words",
    agent=writer,
    context=[research_task],  # depends on research
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff(inputs={"topic": "graph neural networks"})
```

## AutoGen

Conversation-based multi-agent:

```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "claude-sonnet"},
    system_message="You are a helpful coding assistant.",
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="TERMINATE",
    code_execution_config={"work_dir": "workspace"},
    max_consecutive_auto_reply=10,
)

# Two-agent conversation
user_proxy.initiate_chat(
    assistant,
    message="Write a Python script that analyzes CSV data and generates a report."
)
```

## Building Custom Orchestration

When frameworks add more complexity than value:

```python
class SimpleOrchestrator:
    def __init__(self, agents: dict, workflow: list):
        self.agents = agents
        self.workflow = workflow
        self.state = {}

    async def run(self, initial_input):
        self.state["input"] = initial_input

        for step in self.workflow:
            agent = self.agents[step["agent"]]
            context = self.build_context(step.get("context_keys", []))

            result = await agent.run(context)
            self.state[step["output_key"]] = result

            # Quality gate
            if step.get("validator"):
                if not step["validator"](result):
                    return {"status": "failed", "step": step["agent"]}

        return {"status": "success", "output": self.state}

# Usage
orchestrator = SimpleOrchestrator(
    agents={"researcher": ResearchAgent(), "writer": WriterAgent()},
    workflow=[
        {"agent": "researcher", "context_keys": ["input"], "output_key": "research"},
        {"agent": "writer", "context_keys": ["input", "research"], "output_key": "report",
         "validator": lambda r: len(r) > 500},
    ]
)
```

## Gotchas

- **Framework lock-in**: deep integration with LangGraph or CrewAI makes switching expensive. Keep core agent logic framework-agnostic - implement business logic as plain functions, use framework only for orchestration plumbing. Test agents independently of the framework
- **Agent chatter burns tokens**: in multi-agent setups (especially AutoGen), agents can have long back-and-forth conversations that waste tokens without progress. Set strict iteration limits and implement convergence detection - if no new information in last 2 exchanges, force termination
- **State management complexity compounds**: LangGraph state grows with every node. Large state objects slow down checkpointing and increase memory usage. Be selective about what goes into state - store references (file paths, IDs) instead of full content. Prune completed step results

## See Also

- [[langgraph]]
- [[multi-agent-systems]]
- [[agent-design-patterns]]
- [[agent-architectures]]
