---
title: Multi-Agent Systems
category: llm-agents/agents
tags: [multi-agent, supervisor, crew-ai, autogen, swarm, agent-collaboration]
---

# Multi-Agent Systems

## Key Facts

- Multi-agent systems use multiple specialized LLMs working together, coordinated by a supervisor/orchestrator
- Analogy: CEO (supervisor LLM) delegates to specialized workers (sub-agent LLMs), each with their own tools and [[rag-pipeline]]
- Two main architectures: **vertical** (hierarchical supervisor-worker) and **horizontal** (peer-to-peer collaboration)
- Each agent can have different: LLM model, system prompt, tools, RAG knowledge base, temperature settings
- Frameworks: **CrewAI** (role-based, open-source), **AutoGen** (Microsoft, conversation-based), **Agency Swarm** (customizable), **LangGraph** supervisor pattern
- FlowWise provides drag-and-drop multi-agent building on top of [[langgraph]]
- Cost scales with agent count: N agents x M reasoning steps = N*M API calls minimum

## Patterns

```python
# Supervisor pattern with LangGraph
from langgraph.graph import StateGraph

def supervisor(state):
    """Decide which worker handles the task."""
    decision = llm.invoke(
        f"Task: {state['task']}\n"
        f"Available workers: researcher, writer, reviewer\n"
        f"Which worker should handle this? Or say DONE if complete."
    )
    return {"next_worker": decision.content.strip()}

def researcher(state):
    """Search and gather information."""
    result = search_tool.invoke(state["task"])
    return {"research": result, "next_worker": "supervisor"}

def writer(state):
    """Write content based on research."""
    draft = llm.invoke(f"Write about: {state['task']}\nResearch: {state['research']}")
    return {"draft": draft.content, "next_worker": "supervisor"}

# Wire up: supervisor -> routes to workers -> back to supervisor
```

```python
# CrewAI example
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Research Analyst",
    goal="Find accurate information about the topic",
    backstory="Expert researcher with attention to detail",
    tools=[search_tool],
    llm="gpt-4o-mini"
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging content based on research",
    backstory="Skilled writer who creates clear, compelling content",
    llm="gpt-4o-mini"
)

research_task = Task(
    description="Research {topic}",
    agent=researcher,
    expected_output="Detailed research notes"
)

writing_task = Task(
    description="Write article based on research",
    agent=writer,
    expected_output="Published article",
    context=[research_task]  # depends on research
)

crew = Crew(agents=[researcher, writer], tasks=[research_task, writing_task])
result = crew.kickoff(inputs={"topic": "AI agents in 2025"})
```

## Gotchas

- **Cost explosion**: 3 agents x 5 steps each = 15+ LLM calls per query. Monitor costs carefully
- **Coordination overhead**: agents miscommunicate, duplicate work, or create circular dependencies
- **Diminishing returns**: adding more agents doesn't always improve quality. Start with 2-3
- **Debugging nightmare**: tracing errors across multiple agents requires observability (LangSmith, logging)
- **Context loss**: information passed between agents gets summarized/lost. Use structured handoff formats
- **API rate limits**: many concurrent agents hit rate limits fast. Implement backoff and queuing
- **Simpler alternatives**: often a single well-prompted agent with multiple tools outperforms a multi-agent setup

## See Also

- [[agent-architectures]] - single-agent patterns that multi-agent systems build upon
- [[langgraph]] - framework for building multi-agent graphs
- [[function-calling]] - how individual agents interact with tools
- [[guardrails]] - safety in autonomous multi-agent systems
- https://docs.crewai.com/ - CrewAI documentation
- https://microsoft.github.io/autogen/ - AutoGen documentation
