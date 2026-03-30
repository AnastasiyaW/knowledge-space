---
title: Agent Architectures
category: llm-agents/agents
tags: [ai-agents, react, reflection, rewoo, planning, reasoning, single-agent, agentic-workflows]
---

# Agent Architectures

## Key Facts

- AI agents = LLMs + tools + reasoning loops. Unlike workflows (fixed steps), agents decide their own actions
- **Workflow vs Agent**: workflows follow predefined code paths; agents dynamically choose tools and strategies
- Anthropic's rule: always start with the simplest solution. Use agents only when tasks are ambiguous/dynamic
- Building blocks: perception, reasoning/planning, memory/retrieval, action/execution, feedback/adaptation, evaluation, guardrails
- Agent stagnation: ReAct agents can get stuck repeating the same thought-action loop. Needs human intervention or max-iterations cap

### Single-Agent Patterns

| Pattern | Key Idea | Best For |
|---------|----------|----------|
| **ReAct** | Reason then Act, observe result, repeat | Multi-step tasks with external tools |
| **Reflection** | Self-evaluate output quality before acting | Tasks requiring high accuracy |
| **Reflexion** | ReAct + persistent memory of past reflections | Long-term learning across episodes |
| **Plan-and-Solve** | Create full plan, then execute steps | Well-defined complex tasks |
| **ReWOO** | Separate planning from execution | Reducing LLM calls (cheaper) |
| **Tree of Thought** | Explore multiple reasoning branches | Complex problem solving |

### Workflow Patterns (not agents, but related)

| Pattern | Key Idea | Best For |
|---------|----------|----------|
| **Prompt Chaining** | Output of one LLM -> input of next | Sequential transformations |
| **Routing** | Classify input, route to specialized handler | Multi-domain systems |
| **Parallelization** | Split task, process concurrently, aggregate | Independent subtasks |
| **Orchestrator-Worker** | Dynamic task decomposition by planner LLM | Unpredictable subtask count |
| **Evaluator-Optimizer** | Generator + Evaluator iterative refinement | Content requiring polish |

## Patterns

```python
# ReAct agent with LangChain
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

tools = [
    Tool(name="Search", func=search_func, description="Search the web"),
    Tool(name="Calculator", func=calc_func, description="Do math"),
]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = create_react_agent(llm, tools, prompt_template)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=10,  # prevent infinite loops
    verbose=True
)
result = executor.invoke({"input": "What is the population of Tokyo squared?"})
```

```python
# Simple Evaluator-Optimizer loop
def generate_and_refine(task: str, max_rounds: int = 3) -> str:
    draft = llm.invoke(f"Generate: {task}")

    for i in range(max_rounds):
        evaluation = llm.invoke(
            f"Evaluate this output for quality:\n{draft}\n"
            f"List specific improvements needed. Say APPROVED if ready."
        )
        if "APPROVED" in evaluation:
            return draft
        draft = llm.invoke(
            f"Original task: {task}\n"
            f"Previous draft: {draft}\n"
            f"Feedback: {evaluation}\n"
            f"Create improved version:"
        )
    return draft
```

## Gotchas

- **Complexity tax**: every layer of agent autonomy adds debugging difficulty, latency, and cost
- **Overly complex agents bring volatility**: uncertain outputs, hard to debug, increased latency
- **ReAct stagnation**: model may loop generating same thoughts/actions. Always set `max_iterations`
- **Tool selection errors**: with many tools, the agent may pick the wrong one. Keep tool count under 10-15
- **Token cost explosion**: each reasoning step = full context re-sent. A 10-step agent uses 10x the tokens
- **Reflection token limits**: persistent memory grows unbounded. Need retrieval strategy for past reflections
- **Testing difficulty**: non-deterministic behavior makes unit testing hard. Use [[llm-evaluation]] benchmarks

## See Also

- [[function-calling]] - the mechanism agents use to interact with tools
- [[multi-agent-systems]] - multiple agents collaborating
- [[memory-and-context]] - how agents retain information
- [[langgraph]] - framework for building agent graphs
- [[guardrails]] - safety constraints for autonomous agents
- https://www.anthropic.com/engineering/building-effective-agents - Anthropic agent patterns
- https://react-lm.github.io/ - ReAct paper
