---
title: Agent Fundamentals
category: concepts
tags: [llm-agents, ai-agents, react, agent-loop, tool-use, reasoning]
---

# Agent Fundamentals

An AI agent is an autonomous system that uses an LLM as its reasoning engine to perceive its environment, reason about situations, take actions via tools, and adapt based on results. Unlike a chatbot (single-turn responses), an agent connects to databases, APIs, and tools to autonomously complete multi-step tasks.

## Key Facts
- Agent = LLM brain + tools + memory + planning
- More capable models produce more capable agents (GPT-4 >> GPT-3.5 for complex agents)
- Function calling capability is essential - the model must reliably output structured tool calls
- Each reasoning step costs tokens - a single request may require 5-20 LLM calls
- Use workflows (fixed step sequences) when the process is known; use agents only when dynamic decision-making is needed

## Agent Components

### 1. LLM Brain (Reasoning Engine)
Core decision-making. Processes context, reasons about next steps, generates tool calls.

### 2. Tools
External capabilities: search, code execution, file operations, APIs, communication. Any function with a description for the LLM.

### 3. Memory
- **Short-term**: current conversation context
- **Long-term**: persistent knowledge across sessions (vector stores, databases)
- **Working memory (scratchpad)**: accumulated thoughts, actions, observations during execution

### 4. Planning
- **No planning**: direct tool call from user request
- **Sequential**: step-by-step execution plan
- **Hierarchical**: subtasks handled by sub-agents
- **Iterative refinement**: plan -> execute -> evaluate -> revise

## The ReAct Loop

The foundational agent execution pattern (Reasoning + Acting):

```text
1. THOUGHT: Analyze situation, decide next action
2. ACTION: Call a tool with specific inputs
3. OBSERVATION: Receive tool output
4. Repeat until task complete
5. FINAL ANSWER: Synthesize and respond
```

**Example:**
```yaml
User: What's the weather in Paris and should I bring an umbrella?

Thought: I need to check weather in Paris
Action: weather_api(city="Paris")
Observation: Temperature: 15C, Rain probability: 80%

Thought: High rain probability means umbrella needed
Final Answer: Paris is 15C with 80% chance of rain. Bring an umbrella.
```

## Agent Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Tool-Use** | LLM decides which tool to call. No complex planning. | Simple API integrations |
| **Conversational** | Maintains dialogue, asks clarifying questions | Customer support |
| **Plan-and-Execute** | Creates full plan first, then executes step by step | Complex multi-step tasks |
| **Self-Correcting (Reflexion)** | Evaluates own output, critiques, retries | Code generation, analysis |

## Agent vs Workflow

| Factor | Agent (autonomous) | Workflow (predefined) |
|--------|-------------------|----------------------|
| Flexibility | High - adapts to novel situations | Low - follows fixed steps |
| Predictability | Low - may take unexpected actions | High - deterministic path |
| Debugging | Hard - trace through reasoning | Easy - check each step |
| Cost | Higher - more LLM calls | Lower - minimal LLM calls |
| Best for | Open-ended research, dynamic tasks | Known processes, pipelines |

## Agent Architectures

### Single Agent
One LLM handles everything. Simple but limited for complex tasks.

### Router Pattern
LLM classifier routes to specialized agents:
```php
User Request -> Router (classifies intent)
  -> FAQ Agent
  -> Technical Agent
  -> Billing Agent
```

### Supervisor Pattern
Boss agent delegates to specialized workers:
```php
User Request -> Supervisor
  -> Worker 1 (Research)
  -> Worker 2 (Analysis)
  -> Worker 3 (Writing)
-> Supervisor synthesizes
```

## Agent Perception: Sensors and Environment

### Sensors (Input Mechanisms)

Sensors are the means by which agents receive input from their environment - analogous to human senses. Different agent types use different sensor combinations:

| Agent Type | Sensors |
|-----------|---------|
| **Self-driving car** | Cameras, LiDAR, GPS, radar, cloud connection |
| **Shopping assistant** | Web scrapers, product APIs, user history, price feeds, weather API |
| **Code assistant** | File system access, terminal output, git history, error logs |
| **Research agent** | Web search, document loaders, database queries, API calls |

Sensors determine the agent's **observability** - what portion of the environment the agent can perceive. More sensors = richer perception but higher cost and complexity.

### Environment Types

The environment is everything the agent perceives and interacts with:

- **Digital-only**: web pages, databases, APIs (most current LLM agents)
- **Physical + digital**: self-driving cars, robotics (cameras + APIs)
- **Dynamic**: environment changes while agent acts (stock market, live traffic)
- **Static**: environment unchanged between actions (document analysis)

**Key insight**: an agent's environment may include data the user doesn't consciously consider. A shopping agent considers weather forecasts, seasonal trends, and historical price patterns - not just the product catalog. The environment definition determines agent capability boundaries.

## Error Handling

Agents can fail at multiple points:
- Malformed tool calls from LLM
- Tool execution failures (API error, timeout)
- Infinite loops
- Misunderstanding task and taking wrong action

**Mitigation**: max iteration limits (10-20 typical), output validation, fallback to human, structured error recovery.

## Agent Benchmarks

| Benchmark | What It Tests |
|-----------|--------------|
| **SWE-bench** | Real GitHub issues (code understanding + fixing) |
| **WebArena** | Web browsing agent evaluation |
| **GAIA** | General AI assistants |
| **ToolBench** | Tool-use across diverse APIs |

## Gotchas
- Start with workflows, add agency gradually - don't make everything autonomous
- Local/small models produce errors with complex agent workflows - use capable models
- Agent cost estimate: $0.01-$1.00 per request depending on complexity
- The scratchpad (accumulated history) grows with each step - must be managed (truncation, summarization)
- Logging everything (thoughts, actions, observations) is essential for debugging agents

## See Also
- [[agent-design-patterns]] - ReAct, plan-and-execute, reflexion patterns in detail
- [[function-calling]] - How agents invoke tools
- [[multi-agent-systems]] - Multi-agent architectures
- [[agent-memory]] - Memory management for agents
- [[agent-security]] - Securing agent systems
