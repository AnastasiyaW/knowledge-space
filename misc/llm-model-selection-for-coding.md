---
title: LLM Model Selection for Coding Tasks
category: misc/ai-coding-tools
tags: [model-selection, reasoning, context-window, cost-optimization, coding-agent, benchmarks]
---

# LLM Model Selection for Coding Tasks

## Key Facts

- Coding tasks split into two categories requiring different model tiers: **planning** (high reasoning) and **execution** (fast/cheap)
- Using a single expensive model for everything wastes budget and hits rate limits faster
- Key model properties for coding: **reasoning level**, **context window size**, **parameter count**, and **cost per token**
- Reasoning level = how well the model handles multi-step logic. High-reasoning models use internal chain-of-thought before answering
- Context window = working memory. Planning tasks need large context (200K+ tokens) to see the full codebase picture
- Parameter count correlates with capability but also with cost and latency
- LM Arena (lmsys.org) leaderboard is the most reliable quality signal - crowdsourced blind comparisons
- OpenRouter rankings in the "programming" category show which models developers actually use in practice

### Model Tier Strategy

| Tier | Use For | Models (2026) | Cost |
|------|---------|---------------|------|
| Planning | Architecture, complex features, debugging | Opus 4.5, Gemini 3 Pro High, GPT-5.2 | $$$$ |
| Execution | Code generation, simple changes, formatting | Sonnet 4.5, Gemini Flash, GPT-4o-mini | $ |
| Review | Code review, test generation | Medium-tier models | $$ |

### Decision Process

1. What type of task? Planning = high reasoning. Execution = fast model.
2. How much context? Long files/many files = large context window model.
3. What's the budget? Free tier with limits vs paid with generous quotas.
4. Check benchmarks monthly - the landscape changes rapidly.

## Patterns

```python
# Model routing based on task type
def select_coding_model(task_type: str) -> dict:
    models = {
        "planning": {
            "model": "claude-opus-4-5",
            "reasoning": "high",
            "use_when": "architecture, complex features, debugging"
        },
        "execution": {
            "model": "claude-sonnet-4-5",
            "reasoning": "medium",
            "use_when": "code generation, simple refactors"
        },
        "review": {
            "model": "claude-sonnet-4-5",
            "reasoning": "medium",
            "use_when": "code review, test writing"
        },
        "quick_question": {
            "model": "claude-haiku-3-5",
            "reasoning": "low",
            "use_when": "explain code, simple lookups"
        }
    }
    return models.get(task_type, models["execution"])
```

```
# Practical session flow:
# Step 1: Plan with expensive model
Mode: Planning | Model: Opus 4.5
Prompt: "Plan a cron expression generator component..."
-> Review plan, add comments, iterate

# Step 2: Execute with cheap model
Mode: Fast | Model: Sonnet 4.5
Prompt: "Yes, proceed with the plan"
-> Code generated, review diffs

# Step 3: Verify
Mode: Fast | Model: Sonnet 4.5
Prompt: "Run tests, use browser to verify"
-> Tests pass, screenshots captured
```

## Gotchas

- AI IDE providers don't publish exact rate limits - they adjust dynamically based on token consumption per request
- Free tiers have strict limits that may not be enough for a full day of development work
- Some models have free preview periods that inflate their usage rankings - check if rankings reflect real adoption
- The same prompt can produce different responses even with the same model - non-determinism is fundamental
- High-reasoning models with internal "thinking" (chain of thought) cost more because the thinking tokens are also billed
- Context window size != effective context utilization. Models degrade in quality with very long contexts (lost-in-the-middle problem)
- Don't rely solely on benchmarks - always test models on YOUR specific codebase and task types

## See Also

- [[ai-ide-workflow-modes]] - how planning and execution modes use different models
- [[ai-assistant-security]] - cost management and API key budgets
