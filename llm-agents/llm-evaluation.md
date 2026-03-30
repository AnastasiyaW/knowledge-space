---
title: LLM Evaluation
category: llm-agents/quality
tags: [evaluation, benchmarks, metrics, testing, quality-assurance, llm-testing]
---

# LLM Evaluation

## Key Facts

- LLM evaluation measures how well a model/system performs on specific tasks
- Two categories: **offline** (benchmarks, test sets before deployment) and **online** (production monitoring, user feedback)
- Key metrics: accuracy, F1, BLEU/ROUGE (text similarity), human preference, latency, cost per query
- **LLM-as-judge**: use a stronger LLM to evaluate outputs of a weaker one. Cheaper than human evaluation
- Chatbot Arena (LMSYS): crowdsourced ELO ranking of models via blind A/B comparison
- Standard benchmarks: MMLU (knowledge), HumanEval (coding), GSM8K (math), HellaSwag (reasoning)
- For [[rag-pipeline]]: measure retrieval precision/recall separately from generation quality
- Evaluation is essential before deploying [[fine-tuning]] results or changing [[agent-architectures]]

## Patterns

```python
# LLM-as-judge evaluation
def evaluate_response(question: str, response: str, reference: str) -> dict:
    eval_prompt = f"""Rate the following response on a scale of 1-5 for:
    - Accuracy: Does it match the reference answer?
    - Completeness: Does it cover all key points?
    - Relevance: Does it stay on topic?

    Question: {question}
    Reference Answer: {reference}
    Model Response: {response}

    Return JSON: {{"accuracy": N, "completeness": N, "relevance": N, "reasoning": "..."}}"""

    result = client.chat.completions.create(
        model="gpt-4o",  # strong judge model
        messages=[{"role": "user", "content": eval_prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(result.choices[0].message.content)
```

```python
# RAG evaluation metrics
from ragas import evaluate
from ragas.metrics import (
    faithfulness,        # Is answer grounded in retrieved context?
    answer_relevancy,    # Is answer relevant to the question?
    context_precision,   # Are retrieved docs relevant?
    context_recall       # Were all needed docs retrieved?
)

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)
```

```python
# Simple A/B comparison
import random

def ab_test(question: str, model_a: str, model_b: str) -> dict:
    resp_a = generate(question, model=model_a)
    resp_b = generate(question, model=model_b)

    # Randomize order to avoid position bias
    if random.random() > 0.5:
        resp_a, resp_b = resp_b, resp_a

    # Use LLM judge or human to pick winner
    winner = judge(question, resp_a, resp_b)
    return {"winner": winner, "model_a": model_a, "model_b": model_b}
```

## Gotchas

- **Self-evaluation bias**: models rate their own output higher. Always use an independent judge model
- **Benchmark contamination**: models may have seen benchmark data during training. Use custom test sets
- **Position bias in LLM-as-judge**: judges prefer the first response shown. Randomize order
- **Metrics don't capture everything**: BLEU/ROUGE correlate poorly with human judgment for open-ended tasks
- **Eval data must match production**: test on realistic queries, not synthetic ones
- **Cost of evaluation**: comprehensive eval with GPT-4 judge can cost more than the system being evaluated
- **Regression testing**: always compare new version against previous version, not just against absolute threshold

## See Also

- [[model-selection]] - using evaluation to choose models
- [[fine-tuning]] - evaluating fine-tuned model quality
- [[rag-pipeline]] - RAG-specific evaluation metrics
- [[guardrails]] - runtime quality enforcement
- https://docs.ragas.io/ - RAGAS RAG evaluation framework
- https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard - Open LLM Leaderboard
- https://chat.lmsys.org/ - Chatbot Arena
