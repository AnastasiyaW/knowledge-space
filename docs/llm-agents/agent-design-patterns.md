---
title: Agent Design Patterns
category: techniques
tags: [llm-agents, react, plan-and-execute, reflexion, mrkl, agent-patterns]
---

# Agent Design Patterns

Established patterns for structuring agent behavior, from simple tool-calling to sophisticated self-correcting loops. Pattern choice depends on task complexity, required reliability, and cost constraints.

## Key Facts
- ReAct (Reasoning + Acting) is the foundational pattern for most agent implementations
- Explicitly generating reasoning traces before actions improves tool selection accuracy
- Plan-and-execute is better for complex multi-step tasks where the plan can be reviewed
- Self-critique loops improve output quality but multiply cost (2-5x more LLM calls)
- Design principles: minimize scope, prefer deterministic steps, log everything, set iteration limits

## Patterns

### ReAct (Reasoning + Acting)

LLM interleaves thinking with tool calling:

```
Thought -> Action -> Observation -> Thought -> ... -> Final Answer
```

**Key insight**: generating reasoning traces before actions dramatically improves tool selection and parameter accuracy vs. direct action-only approaches.

### Plan-and-Execute

Two-phase approach:

1. **Planning phase**: LLM generates ordered list of steps with dependencies
2. **Execution phase**: execute each step, re-plan if results differ from expectations

**Advantages over ReAct**: better for complex tasks, plan reviewable by human, easier to debug (which step failed?).

**Disadvantage**: initial plan may not account for unexpected tool outputs.

### MRKL (Modular Reasoning, Knowledge, and Language)

LLM as router/coordinator with specialist modules (calculator, search, SQL executor). LLM decides which module to invoke and how to interpret output. Foundation for most tool-use agent architectures.

### Reflexion / Self-Critique

Agent evaluates its own output and iteratively improves:

```
1. Generate initial response
2. Critique: "What's wrong with this response?"
3. Identify specific issues
4. Generate improved response
5. Repeat until satisfactory or max iterations
```

**Use cases**: code generation (write -> test -> fix -> test), complex analysis, creative writing.

### Scratchpad Management

The accumulated history of thoughts, actions, and observations fed back to the LLM at each step. Grows with each iteration.

**Management strategies**:
- Truncation: drop oldest entries when approaching context limit
- Summarization: periodically summarize older entries
- Selective retention: keep key decisions, drop routine observations

## Tool Selection Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Static tool set** | Fixed list of available tools | Well-defined domains |
| **Dynamic discovery** | Agent searches for tools at runtime | Open-ended tasks |
| **Tool composition** | Chain tool outputs as inputs | Multi-step data processing |

## Design Principles

1. **Minimize agent scope**: each agent does one thing well
2. **Prefer deterministic steps**: use code/scripts for deterministic operations, LLM only for reasoning
3. **Log everything**: full trace of thoughts, actions, observations for debugging
4. **Set iteration limits**: prevent infinite loops (max 10-20 steps typical)
5. **Validate outputs**: check tool call parameters before execution
6. **Human-in-the-loop**: require human approval for high-stakes actions
7. **Start with workflows, add agency gradually**: don't make everything autonomous

## Structured Output from Agents

Force agents to produce structured data at each step:

```python
# Tool call schema
{
    "tool": "search_database",
    "parameters": {
        "query": "quarterly revenue 2024",
        "filters": {"department": "sales"}
    },
    "reasoning": "Need sales figures to answer user's revenue question"
}
```

## Gotchas
- Agent enters infinite loop: always set max_iterations (10-20)
- Scratchpad overflow: summarize or truncate older entries
- Model generates invalid tool calls: add validation before execution
- Over-engineering: simple ReAct handles 80% of use cases, don't add complexity prematurely
- Reflexion multiplies cost: each self-critique loop is an additional LLM call

## See Also
- [[agent-fundamentals]] - Agent components and architecture overview
- [[multi-agent-systems]] - Patterns for multiple collaborating agents
- [[function-calling]] - How tool calls work at the API level
- [[langchain-framework]] - Framework implementations of these patterns
- [[langgraph]] - Graph-based agent orchestration
- [[agent-self-improvement]] - Self-critique extended to agent self-modification
- [[autonomous-agent-evolution]] - Heartbeat reflection pattern for long-running agents
