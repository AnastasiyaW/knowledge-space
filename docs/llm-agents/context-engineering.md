---
title: Context Engineering for Agents
category: patterns
tags: [llm-agents, context-window, memory, state-management, compaction, retrieval]
---

# Context Engineering for Agents

Managing what information goes into the LLM context window and when. The context window is the agent's working memory - everything it can reason about at once. Poor context management is the primary cause of agent degradation on long tasks.

## The Context Problem

LLMs have fixed context windows (4K-2M tokens). Long-running agents accumulate:
- Conversation history (user messages + assistant responses)
- Tool call results (often large: web pages, code files, database results)
- System instructions and tool definitions
- Internal reasoning traces

**When context fills up**: model loses access to early information, quality degrades, hallucination increases, cost per call rises linearly with context size.

## Context Budget Allocation

```python
class ContextBudget:
    def __init__(self, max_tokens=128000):
        self.max_tokens = max_tokens
        self.allocations = {
            "system": 0.10,        # 10% for system prompt + tools
            "state": 0.10,         # 10% for current state/plan
            "history": 0.30,       # 30% for conversation history
            "tool_results": 0.30,  # 30% for tool outputs
            "generation": 0.20,    # 20% reserved for model output
        }

    def budget_for(self, category):
        return int(self.max_tokens * self.allocations[category])

    def fits(self, category, token_count):
        return token_count <= self.budget_for(category)
```

## State Management Patterns

### Structured State Object

Instead of relying on conversation history, maintain explicit state:

```python
class AgentState:
    def __init__(self):
        self.goal = ""
        self.plan = []
        self.completed_steps = []
        self.current_step = None
        self.key_findings = []
        self.failed_approaches = []
        self.open_questions = []

    def to_context(self) -> str:
        """Serialize for injection into LLM context."""
        return f"""
## Current Goal
{self.goal}

## Plan
{self._format_plan()}

## Key Findings So Far
{chr(10).join(f'- {f}' for f in self.key_findings[-10:])}

## Failed Approaches (DO NOT retry)
{chr(10).join(f'- {f}' for f in self.failed_approaches[-5:])}

## Open Questions
{chr(10).join(f'- {q}' for q in self.open_questions[-5:])}
"""

    def _format_plan(self):
        lines = []
        for i, step in enumerate(self.plan):
            if i < len(self.completed_steps):
                lines.append(f"[DONE] {step}")
            elif i == len(self.completed_steps):
                lines.append(f"[CURRENT] {step}")
            else:
                lines.append(f"[ ] {step}")
        return "\n".join(lines)
```

### File-Based State (For Long Tasks)

```python
# Write state to disk, read back when needed
import json

STATE_FILE = ".agent/state.json"
PLAN_FILE = ".agent/PLAN.md"
FINDINGS_FILE = ".agent/findings.md"

def save_state(state: AgentState):
    with open(STATE_FILE, 'w') as f:
        json.dump(state.__dict__, f, indent=2)

def load_state() -> AgentState:
    with open(STATE_FILE) as f:
        data = json.load(f)
    state = AgentState()
    state.__dict__.update(data)
    return state

# Agent reads state from file at start of each step
# This survives context compaction and session restarts
```

## Context Compaction Strategies

### Summarization

Replace detailed history with compressed summary:

```python
def compact_history(messages, target_tokens=2000):
    """Summarize conversation history to fit budget."""
    # Keep system message and last 3 exchanges intact
    preserved = messages[:1] + messages[-6:]

    # Summarize everything in between
    middle = messages[1:-6]
    if not middle:
        return messages

    summary_prompt = f"""
    Summarize this conversation history, preserving:
    1. Key decisions made
    2. Important findings
    3. Current state of the task
    4. What was tried and failed

    History to summarize:
    {format_messages(middle)}
    """
    summary = llm.complete(summary_prompt, max_tokens=target_tokens)

    return [messages[0],
            {"role": "system", "content": f"[Previous conversation summary]\n{summary}"},
            *preserved]
```

### Selective Retention

Keep only relevant parts of tool results:

```python
def truncate_tool_result(result: str, max_tokens: int = 1000) -> str:
    """Truncate tool output to fit budget."""
    token_count = count_tokens(result)
    if token_count <= max_tokens:
        return result

    # Try to extract key information
    summary = llm.complete(
        f"Extract only the key facts from this tool output (max {max_tokens} tokens):\n{result}",
        max_tokens=max_tokens
    )
    return f"[Summarized from {token_count} tokens]\n{summary}"
```

### Re-injection After Compaction

```python
def post_compaction_reinject(state: AgentState) -> str:
    """After context compaction, re-inject critical state."""
    return f"""
[Context was compacted. Here is the current state to continue from:]

{state.to_context()}

[Continue from where you left off. The plan and findings above are accurate.]
"""
```

## Retrieval-Augmented Context

Pull relevant information on-demand instead of keeping everything in context:

```python
class ContextRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.cache = {}

    def get_relevant_context(self, query: str, k: int = 5) -> str:
        """Fetch relevant documents/history for current query."""
        results = self.vector_store.search(query, top_k=k)
        return "\n\n".join([
            f"[Relevant context {i+1}]:\n{r.text}"
            for i, r in enumerate(results)
        ])

    def index_interaction(self, query: str, response: str, metadata: dict):
        """Index completed interactions for future retrieval."""
        text = f"Q: {query}\nA: {response}"
        self.vector_store.add(text, metadata=metadata)
```

## Context Window Sizing Guide

| Task Type | Recommended Window | Reason |
|-----------|-------------------|--------|
| Simple Q&A | 4K-8K | Minimal context needed |
| Code editing | 32K-128K | Need surrounding code |
| Research | 64K-200K | Multiple sources to synthesize |
| Long refactoring | 128K+ state files | Context resets between steps |

## Anti-Patterns

- **Stuffing everything into context**: leads to "lost in the middle" - model ignores information in the middle of long contexts. Put important info at the beginning and end
- **No explicit state management**: relying on conversation history alone. After compaction, critical details vanish. Always maintain external state
- **Ignoring token costs**: 128K context at $3/M input tokens = $0.38 per LLM call. Ten calls = $3.80. Use shorter context when possible

## Gotchas

- **Context compaction loses information irreversibly**: once you summarize, details are gone. Before compacting, save full state to files. After compaction, re-inject the structured state object so the agent knows where it stands. Test by verifying the agent can answer questions about pre-compaction work
- **"Lost in the middle" is real and measurable**: LLMs attend strongly to the beginning and end of context, but poorly to the middle. Place the most critical information (current task, plan, constraints) at the start of context, and recent observations at the end. Never bury important state in the middle of a long history
- **Retrieval latency breaks agent flow**: if every agent step requires a vector search, latency adds up. Pre-fetch likely-needed context at the start of each plan phase, not reactively on every LLM call. Batch retrieval queries when possible

## See Also

- [[agent-memory]]
- [[agent-architectures]]
- [[rag-pipeline]]
- [[embeddings]]
- [[context-window-management]] - Layered loading, token budgets, compaction strategies
- [[session-persistence]] - Handoff files, state files, journal patterns
