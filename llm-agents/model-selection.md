---
title: Model Selection
category: llm-agents/fundamentals
tags: [model-selection, benchmarks, frontier-models, open-source-llm, cost-optimization, model-comparison]
---

# Model Selection

## Key Facts

- Choosing the right model is critical: wrong model = wasted cost or inadequate quality
- Decision axes: **quality** (accuracy, reasoning), **cost** (per-token pricing), **speed** (latency), **context window**, **modality** (text/image/audio)
- Frontier models (closed-source): GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro - highest quality, highest cost
- Budget models: GPT-4o-mini, Claude 3 Haiku, Gemini Flash - 90% quality at 10% cost for most tasks
- Open-source: Llama 3.x, Mistral, Qwen 2.5, Gemma 2 - free, self-hosted, full control, lower capability ceiling
- As models converge in quality, the differentiator becomes **price and speed**
- Benchmarks help but don't tell the full story. Always test on your specific task
- Chatbot Arena (LMSYS) ELO ratings are the most reliable quality signal (crowdsourced human preference)

### Quick Decision Tree

| Need | Recommended |
|------|-------------|
| Best quality, cost irrelevant | GPT-4o / Claude Sonnet |
| Good quality, low cost | GPT-4o-mini / Claude Haiku |
| Max data privacy | Llama 3.x via [[ollama-local-llms]] |
| Long documents (>100K tokens) | Gemini 1.5 Pro (2M context) / Claude (200K) |
| Code generation | Claude Sonnet / GPT-4o |
| Multilingual | Qwen 2.5 / GPT-4o |
| Counting/math | O1-preview (reasoning model) |
| Image understanding | GPT-4o / Claude Sonnet / Gemini |

## Patterns

```python
# Cost-aware model routing
def select_model(task_complexity: str, budget: str = "normal") -> str:
    """Select model based on task complexity and budget."""
    if budget == "minimal":
        return "gpt-4o-mini"

    routing = {
        "simple_qa": "gpt-4o-mini",           # $0.15/1M input
        "summarization": "gpt-4o-mini",
        "code_generation": "claude-sonnet-4-20250514",
        "complex_reasoning": "gpt-4o",         # $2.50/1M input
        "math_proof": "o1-preview",
        "long_document": "gemini-1.5-pro",
    }
    return routing.get(task_complexity, "gpt-4o-mini")
```

```python
# A/B testing models
def evaluate_models(test_cases, models):
    results = {}
    for model in models:
        scores = []
        for case in test_cases:
            response = generate(case["input"], model=model)
            score = evaluate(response, case["expected"])
            scores.append(score)
        results[model] = {
            "avg_score": sum(scores) / len(scores),
            "cost": calculate_cost(model, test_cases)
        }
    return results
```

## Gotchas

- **Benchmark gaming**: models are sometimes trained on benchmark data. Real-world performance may differ
- **Letter counting**: most models fail at character-level tasks (counting letters) due to [[tokenization]]
- **Emerging intelligence**: all models are "just" predicting next tokens, but scale produces apparently intelligent behavior
- **Model deprecation**: providers retire old models. Pin versions but plan for migration
- **Rate limits vary**: higher-tier models have lower rate limits. Plan capacity accordingly
- **Temperature sensitivity**: same prompt + different temperature = very different outputs. Standardize in tests
- **Vendor lock-in**: OpenAI message format is standard, but tool schemas and features differ across providers

## See Also

- [[llm-evaluation]] - systematic model comparison
- [[api-integration]] - connecting to different model providers
- [[ollama-local-llms]] - running open-source models locally
- [[fine-tuning]] - customizing a selected model
- https://chat.lmsys.org/ - Chatbot Arena rankings
- https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard - Open LLM Leaderboard
- https://artificialanalysis.ai/ - LLM price/performance comparison
