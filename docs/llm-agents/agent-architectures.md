---
title: Agent Cognitive Architectures
category: concepts
tags: [llm-agents, architecture, cognitive, state-machine, dag, loop]
---

# Agent Cognitive Architectures

How to structure the control flow and state management of an LLM agent beyond individual patterns. Covers the computational graph that defines how an agent reasons, acts, and learns within a single task execution.

## Architecture Taxonomy

### Single-Loop Agent

Simplest: one LLM call decides next action, observe result, repeat.

```
while not done:
    action = llm(prompt + history)
    observation = execute(action)
    history.append((action, observation))
```

Pros: simple, easy to debug. Cons: no planning, no self-correction, context window fills quickly.

### Planner-Executor Split

Separate planning from execution. Planner creates steps, executor handles each one.

```python
# Planner generates structured plan
plan = planner_llm(f"""
Task: {user_request}
Available tools: {tool_descriptions}
Output a numbered list of steps.
""")

# Executor handles each step independently
results = []
for step in parse_plan(plan):
    result = executor_llm(f"""
    Execute this step: {step}
    Previous results: {results}
    """)
    results.append(result)

# Replanner if needed
if not satisfactory(results):
    revised_plan = planner_llm(f"""
    Original plan failed at step {failed_step}.
    Error: {error}
    Revise the plan.
    """)
```

### State Machine Agent

Explicit states with defined transitions. Most reliable for production.

```python
from enum import Enum

class AgentState(Enum):
    UNDERSTAND = "understand"
    PLAN = "plan"
    EXECUTE = "execute"
    VERIFY = "verify"
    RESPOND = "respond"
    ERROR = "error"

class StateMachineAgent:
    def __init__(self):
        self.state = AgentState.UNDERSTAND
        self.context = {}
        self.max_retries = 3

    def run(self, user_input):
        self.context["input"] = user_input

        while self.state != AgentState.RESPOND:
            if self.state == AgentState.UNDERSTAND:
                self.context["intent"] = classify_intent(user_input)
                self.state = AgentState.PLAN

            elif self.state == AgentState.PLAN:
                self.context["plan"] = create_plan(self.context)
                self.state = AgentState.EXECUTE

            elif self.state == AgentState.EXECUTE:
                try:
                    self.context["result"] = execute_plan(self.context["plan"])
                    self.state = AgentState.VERIFY
                except Exception as e:
                    self.context["error"] = str(e)
                    self.state = AgentState.ERROR

            elif self.state == AgentState.VERIFY:
                if verify_result(self.context["result"]):
                    self.state = AgentState.RESPOND
                else:
                    self.state = AgentState.PLAN  # replan

            elif self.state == AgentState.ERROR:
                if self.context.get("retries", 0) < self.max_retries:
                    self.context["retries"] = self.context.get("retries", 0) + 1
                    self.state = AgentState.PLAN
                else:
                    self.state = AgentState.RESPOND

        return format_response(self.context)
```

### DAG (Directed Acyclic Graph) Agent

Tasks organized as dependency graph. Parallel execution of independent nodes.

```python
# DAG definition
task_graph = {
    "search_web": {"deps": [], "tool": "web_search"},
    "search_db": {"deps": [], "tool": "database_query"},
    "analyze": {"deps": ["search_web", "search_db"], "tool": "llm_analyze"},
    "format": {"deps": ["analyze"], "tool": "format_output"},
}

import asyncio

async def execute_dag(graph, context):
    completed = {}
    pending = set(graph.keys())

    while pending:
        ready = [t for t in pending if all(d in completed for d in graph[t]["deps"])]
        results = await asyncio.gather(*[
            execute_node(t, graph[t], {d: completed[d] for d in graph[t]["deps"]})
            for t in ready
        ])
        for task, result in zip(ready, results):
            completed[task] = result
            pending.remove(task)

    return completed
```

## Memory Architecture

### Working Memory (In-Context)

Current conversation + recent observations. Limited by context window.

### Short-Term Memory (Session)

Persists across multiple LLM calls within one task:

```python
class SessionMemory:
    def __init__(self):
        self.facts = []       # discovered facts
        self.plan = []        # current plan steps
        self.errors = []      # failed approaches
        self.scratchpad = ""  # working notes

    def to_context(self, max_tokens=2000):
        """Serialize for LLM context injection."""
        return f"""
Known facts: {self.facts[-10:]}
Current plan: {self.plan}
Failed approaches (do NOT retry): {self.errors[-5:]}
"""
```

### Long-Term Memory (Cross-Session)

Vector store or structured DB for persistent knowledge:

```python
# Episodic memory: store successful task completions
def store_episode(task, solution, outcome):
    embedding = embed(f"{task} -> {solution}")
    vector_db.upsert(
        id=str(uuid4()),
        vector=embedding,
        metadata={"task": task, "solution": solution, "outcome": outcome}
    )

# Retrieve similar past experiences
def recall(current_task, k=3):
    results = vector_db.query(embed(current_task), top_k=k)
    return [r.metadata for r in results if r.metadata["outcome"] == "success"]
```

## Routing Architecture

For complex systems, route requests to specialized sub-agents:

```python
class AgentRouter:
    def __init__(self):
        self.agents = {
            "code": CodeAgent(),
            "research": ResearchAgent(),
            "data": DataAnalysisAgent(),
            "general": GeneralAgent(),
        }

    def route(self, query):
        # Classifier determines which agent handles the request
        category = classify(query)  # lightweight LLM or rule-based
        agent = self.agents.get(category, self.agents["general"])
        return agent.run(query)
```

## Checkpointing and Recovery

```python
import json

class CheckpointableAgent:
    def save_checkpoint(self, path):
        state = {
            "current_state": self.state.value,
            "context": self.context,
            "step_count": self.step_count,
        }
        with open(path, 'w') as f:
            json.dump(state, f)

    def load_checkpoint(self, path):
        with open(path) as f:
            state = json.load(f)
        self.state = AgentState(state["current_state"])
        self.context = state["context"]
        self.step_count = state["step_count"]
```

## Gotchas

- **Infinite loops without exit conditions**: agents can get stuck retrying the same failed approach. Always implement max iteration limits, timeout budgets, and track failed approaches to avoid repeating them. A stuck agent burns tokens indefinitely
- **Context window overflow kills long-running agents**: as conversation history grows, older context gets truncated and the agent loses track of its plan. Implement explicit memory management: summarize old observations, maintain a structured state object, and re-inject only critical context after compaction
- **Overengineered architectures for simple tasks**: a state machine with 10 states and DAG execution for a task that needs one LLM call + one tool use. Start with the simplest architecture (single loop), add complexity only when failures demand it

## See Also

- [[agent-design-patterns]]
- [[agent-memory]]
- [[multi-agent-systems]]
- [[langgraph]]
