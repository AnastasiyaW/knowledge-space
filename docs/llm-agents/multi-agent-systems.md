---
title: Multi-Agent Systems
category: techniques
tags: [llm-agents, multi-agent, supervisor, crewai, autogen, agent-collaboration]
---

# Multi-Agent Systems

Multi-agent systems decompose complex tasks across specialized agents that collaborate. Research shows giving one LLM a specific narrow task makes it perform better than asking it to handle everything - multiple specialists outperform one generalist.

## Key Facts
- 2-3 agents: simple delegation, easy to debug
- 4-6 agents: specialized team, manageable complexity
- 7+ agents: risk of coordination overhead and message confusion
- Every message between agents is an LLM call - minimize unnecessary back-and-forth
- N agents ~ N x cost of a single agent

## Architectural Patterns

### Supervisor / Boss-Worker
One coordinator delegates to specialized workers:

```
User -> Supervisor
         -> Worker 1 (Researcher): gathers information
         -> Worker 2 (Analyst): analyzes data
         -> Worker 3 (Writer): produces output
       Supervisor compiles final response
```

**Supervisor responsibilities**: interpret user intent, assign tasks, determine execution order, synthesize results.

**Worker definition**: name, role description, system prompt, available tools, output format.

### Sequential Pipeline
Workers execute in fixed order:

```
Input -> Research Agent -> Analysis Agent -> Writing Agent -> Review Agent -> Output
```

**When to use**: process is well-defined, order doesn't change, clear input/output contracts.

### Hierarchical
Multiple levels of coordination:

```
Top Coordinator
  -> Team Lead A (Research)
       -> Researcher 1, Researcher 2
  -> Team Lead B (Production)
       -> Writer, Editor
```

### Debate / Consensus
Multiple agents with different perspectives argue until converging:

```
Agent A (conservative): proposes solution
Agent B (aggressive): critiques and proposes alternative
Moderator: synthesizes best aspects of both
```

## Frameworks

### CrewAI

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Research Analyst",
    goal="Find comprehensive information on the topic",
    backstory="Expert researcher with 10 years experience",
    tools=[search_tool, web_scraper],
    llm=ChatOpenAI(model="gpt-4")
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging articles from research",
    backstory="Award-winning journalist",
    llm=ChatOpenAI(model="gpt-4")
)

research_task = Task(
    description="Research the latest trends in AI agents",
    agent=researcher,
    expected_output="Detailed research report"
)

writing_task = Task(
    description="Write an article based on the research",
    agent=writer,
    expected_output="Published-quality article",
    context=[research_task]
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential  # or Process.hierarchical
)
result = crew.kickoff()
```

### AutoGen (Microsoft)
- **ConversableAgent**: base agent for sending/receiving messages
- **AssistantAgent**: LLM-powered agent
- **UserProxyAgent**: represents human, can execute code
- Group chat with multiple agents
- Sandboxed code execution support

### FlowWise Multi-Agent
Visual no-code approach:
1. Add Supervisor node + Worker nodes
2. Connect Chat Model (OpenAI/Ollama) to Supervisor
3. Define worker system prompts and tools
4. Set execution strategy in supervisor prompt

## Communication Protocols

| Protocol | Description | Best For |
|----------|-------------|----------|
| **Message passing** | Structured messages with from/to/content | Sequential workflows |
| **Shared state** | All agents read/write to shared workspace | Async collaboration |
| **Event-driven** | Agents subscribe to events, triggered by completions | Decoupled pipelines |

## Practical Agent Teams

### RAG Team
Router (classify query) -> Retrieval (search KB) -> Synthesis (generate answer) -> Citation (add sources)

### Content Creation Team
Research -> Outline -> Writing -> Editing -> SEO

### Customer Support Team
Triage (classify urgency) -> Knowledge (search FAQ) -> Action (execute operations) -> Escalation (route to human)

## Gotchas
- More agents = more messages = more tokens = higher cost and latency
- Don't use multi-agent when a single agent or workflow suffices
- Fully deterministic workflows should use code, not agents
- If latency is critical, each agent hop adds significant delay
- Debug by logging all inter-agent messages and tracking task state through the pipeline
- Evaluate each agent independently before composing them into a team

## See Also
- [[agent-fundamentals]] - Single agent architecture
- [[agent-design-patterns]] - Patterns for individual agents
- [[langgraph]] - Graph-based multi-agent orchestration
- [[agent-memory]] - Shared memory across agents
- [[no-code-platforms]] - Visual multi-agent building with FlowWise
- [[autonomous-agent-evolution]] - Multi-agent evolution with workspace isolation and shared knowledge
