---
title: Token Optimization for Agents
category: techniques
tags: [llm-agents, token-optimization, cost-reduction, compression, caveman-prompting, response-format]
---

# Token Optimization for Agents

Reducing token consumption in agent systems without degrading task performance. Agent costs scale with tokens (input + output) x number of calls x number of agents. A 75% token reduction in a 5-agent system with 20 calls each = 75x fewer tokens billed.

## Response Compression Techniques

### Caveman Prompting

Force terse, keyword-dense responses by instructing the model to use minimal grammar:

```
System: Reply in compressed style. No articles, no filler words.
Skip "the", "a", "is", "are". Use arrows, abbreviations.
Max info per token. Like telegram.

User: What are the main causes of the 2008 financial crisis?

Normal response (180 tokens):
"The 2008 financial crisis was primarily caused by several
interconnected factors. First, there was a massive expansion of
subprime mortgage lending..."

Compressed response (45 tokens):
"2008 crisis causes: subprime mortgage expansion -> securitization
(MBS/CDO) -> credit rating failures -> overleveraged banks ->
Lehman collapse -> credit freeze -> global contagion"
```

**Savings**: 75% token reduction. Works best for factual/analytical tasks. Quality degrades on creative or nuanced tasks.

### Structured Output Compression

Replace natural language agent responses with structured formats:

```python
# Instead of: "I searched the database and found 3 results.
# The most relevant one is the user profile for John with ID 12345..."

# Use:
{"action": "search_db", "results": 3, "top": {"id": 12345, "type": "user"}}
```

### Scratchpad Compression

Agent reasoning traces consume most tokens. Compress intermediate steps:

```python
# Verbose scratchpad (typical):
"""
Thought: I need to find the error in the code. Let me look at the
stack trace first. The error message says "IndexError: list index
out of range" which means we're trying to access an element at an
index that doesn't exist. Let me check the function where this occurs.
Action: read_file("main.py")
Observation: [200 lines of code]
Thought: I can see the issue. On line 45, we access arr[i] but the
loop goes from 0 to len(arr) inclusive, which means when i equals
len(arr), we get an out of bounds error...
"""

# Compressed scratchpad:
"""
T: IndexError line 45: loop 0..len(arr) inclusive, off-by-one
A: read_file("main.py")
O: [relevant lines only: 43-47]
T: Fix: range(len(arr)) not range(len(arr)+1)
"""
```

**Implementation**: set a word budget in the system prompt:

```
Reasoning budget: max 30 words per thought. Use abbreviations.
T=thought, A=action, O=observation (first 5 relevant lines only).
```

## Cost-Aware Architecture Patterns

### Model Cascading

Route cheap tasks to cheap models, expensive tasks to expensive models:

```python
def route_to_model(task: dict) -> str:
    """Select model based on task complexity."""
    complexity = estimate_complexity(task)
    if complexity < 0.3:
        return "haiku"          # ~$0.25/M tokens
    elif complexity < 0.7:
        return "sonnet"         # ~$3/M tokens
    else:
        return "opus"           # ~$15/M tokens

def estimate_complexity(task: dict) -> float:
    """Heuristic complexity scoring."""
    score = 0.0
    if task.get("requires_reasoning"):
        score += 0.3
    if task.get("multi_step"):
        score += 0.3
    if task.get("code_generation"):
        score += 0.2
    if len(task.get("context", "")) > 10000:
        score += 0.2
    return min(score, 1.0)
```

### Subagent Token Budget

Enforce per-subagent token limits:

```python
class TokenBudgetAgent:
    def __init__(self, max_input: int = 4000, max_output: int = 1000):
        self.max_input = max_input
        self.max_output = max_output

    def run(self, task: str, context: str) -> str:
        # Truncate context to budget
        context = truncate_to_tokens(context, self.max_input - count_tokens(task))

        response = llm.generate(
            messages=[{"role": "user", "content": f"{task}\n\nContext:\n{context}"}],
            max_tokens=self.max_output,
        )
        return response
```

### Caching and Deduplication

```python
import hashlib
from functools import lru_cache

# Cache identical tool call results
@lru_cache(maxsize=256)
def cached_tool_call(tool_name: str, params_hash: str):
    return execute_tool(tool_name, unhash(params_hash))

# Deduplicate context across agent calls
def deduplicate_context(messages: list[dict]) -> list[dict]:
    """Remove duplicate tool observations."""
    seen_observations = set()
    deduped = []
    for msg in messages:
        if msg["role"] == "tool":
            h = hashlib.md5(msg["content"].encode()).hexdigest()
            if h in seen_observations:
                continue
            seen_observations.add(h)
        deduped.append(msg)
    return deduped
```

### Prompt Caching

Modern APIs cache repeated prompt prefixes. Structure prompts so the stable portion comes first:

```python
messages = [
    # STABLE PREFIX (cached after first call - 90% cheaper on subsequent)
    {"role": "system", "content": long_system_prompt},      # ~2000 tokens
    {"role": "user", "content": reference_documents},        # ~5000 tokens

    # VARIABLE SUFFIX (changes each call)
    {"role": "user", "content": current_task},               # ~200 tokens
]
# First call: 7200 tokens at full price
# Subsequent calls: 200 tokens at full price + 7000 at 10% price
```

## Measuring Token Efficiency

```python
def token_efficiency_report(agent_runs: list[dict]) -> dict:
    """Calculate token efficiency metrics across runs."""
    total_tokens = sum(r["tokens_used"] for r in agent_runs)
    successful = [r for r in agent_runs if r["success"]]
    failed = [r for r in agent_runs if not r["success"]]

    return {
        "total_tokens": total_tokens,
        "tokens_per_success": total_tokens / max(len(successful), 1),
        "tokens_per_task": total_tokens / len(agent_runs),
        "waste_ratio": sum(r["tokens_used"] for r in failed) / total_tokens,
        "avg_steps": sum(r["steps"] for r in agent_runs) / len(agent_runs),
        "cost_usd": total_tokens * 0.000003,  # adjust per model
    }
```

Track `tokens_per_success` over time - it should decrease as you optimize. A high `waste_ratio` means the agent burns tokens on doomed attempts - improve early failure detection.

## Gotchas

- **Aggressive compression kills nuance**: caveman prompting works for factual extraction but causes the model to miss subtleties in analysis tasks. Test quality metrics before deploying compressed prompts in production - measure pass rate, not just token count
- **Scratchpad truncation causes reasoning failures**: if you cut the reasoning trace too aggressively, the model loses track of its chain-of-thought. Start with a 50% compression target and measure task success rate. Never compress below the point where success rate drops
- **Caching stale results**: tool call caching can serve outdated data if the underlying state changed between calls. Add TTL to cached results and invalidate on state-changing actions (write, delete, update)
- **Model cascading routing errors are expensive**: sending a hard task to a cheap model wastes those tokens entirely when it fails, then you pay again for the expensive model. When in doubt, route up not down

## See Also

- [[context-engineering]] - Managing what goes into the context window
- [[prompt-engineering]] - Prompt-level optimization and formatting
- [[model-optimization]] - Model-level optimization (quantization, distillation)
- [[agent-evaluation]] - Measuring agent efficiency metrics
- [[production-patterns]] - Cost management in production agent systems
