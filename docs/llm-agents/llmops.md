---
title: LLMOps
category: infrastructure
tags: [llm-agents, llmops, monitoring, evaluation, cost-optimization, observability]
---

# LLMOps

LLMOps adapts MLOps practices for LLM-specific workflows: prompt management, model serving, evaluation, monitoring, and cost control. The key difference from traditional MLOps is that iteration happens through prompt editing and RAG tuning, not model retraining.

## Key Facts
- Primary iteration loop: edit prompt -> run evaluation suite -> compare metrics -> deploy if improved
- Biggest cost driver: token usage, especially output tokens
- LLM-as-Judge is the most scalable automated evaluation method
- Structured logging of every request is essential and disk is cheap
- Prompt changes need regression testing just like code changes

## LLMOps vs Traditional MLOps

| Aspect | Traditional MLOps | LLMOps |
|--------|------------------|--------|
| Training | Custom model training | Prompt engineering or fine-tuning |
| Deployment | Model binary + inference server | API calls or self-hosted models |
| Versioning | Model weights + data | Prompts + configs + adapter weights |
| Evaluation | Fixed metrics (accuracy, F1) | LLM-as-judge, human eval, task-specific |
| Cost | Compute for training/inference | Token-based API pricing |
| Iteration | Retrain model | Edit prompt, adjust RAG |

## Evaluation Pipeline

### LLM-as-Judge Pattern
```python
def evaluate_response(question, response, reference, judge_llm):
    prompt = f"""Rate this response on 1-5:
    Question: {question}
    Response: {response}
    Reference: {reference}
    Rate on: accuracy, completeness, clarity.
    Output JSON: {{"accuracy": X, "completeness": X, "clarity": X}}"""
    return judge_llm.invoke(prompt)
```

### Key Metrics

| Metric | What It Measures |
|--------|-----------------|
| **Faithfulness** | Answer grounded in context? |
| **Answer Relevancy** | Addresses the question? |
| **Context Precision** | Retrieved docs relevant? |
| **Context Recall** | All relevant docs found? |
| **Toxicity** | Harmful content? |
| **Latency** | End-to-end response time |
| **Cost** | Token usage per query |

### Evaluation Frameworks
- **RAGAS**: automated RAG evaluation
- **DeepEval**: comprehensive LLM testing
- **LangSmith**: integrated tracing + evaluation
- **Promptfoo**: prompt testing and comparison
- **Arize Phoenix**: LLM observability

## Model Serving

### Self-Hosted Options
- **vLLM**: high-throughput with PagedAttention
- **TGI**: HuggingFace inference server
- **Ollama**: simple local serving
- **TensorRT-LLM**: NVIDIA-optimized
- **llama.cpp**: CPU-optimized for GGUF models

### Serving Optimizations
- **KV-cache**: cache key-value pairs for seen tokens
- **Continuous batching**: process multiple requests simultaneously
- **Speculative decoding**: small model drafts, large model verifies
- **Quantization**: reduce precision for faster inference

## Monitoring in Production

### Key Metrics
- Response latency (p50, p95, p99)
- Token usage (input + output per request)
- Error rate (API failures, malformed responses)
- Hallucination rate (periodic human review)
- User satisfaction (thumbs up/down)
- Cost per conversation / per user
- Retrieval quality (for RAG)

### Structured Logging
```json
{
    "request_id": "uuid",
    "timestamp": "2024-01-15T10:30:00Z",
    "user_id": "user123",
    "input_tokens": 500,
    "output_tokens": 200,
    "model": "gpt-4",
    "latency_ms": 1200,
    "tools_called": ["search_db", "calculate"],
    "cost_usd": 0.015,
    "feedback": null
}
```

Store full trace (intermediate steps, tool calls, LLM responses) for debugging.

### Alerting
- Response latency exceeds threshold
- Error rate spikes
- Token usage anomaly (possible injection attack)
- Provider degradation/outage
- Cost exceeds daily/monthly budget

## Cost Optimization

### Strategies
1. **Smallest effective model**: GPT-4o-mini for simple tasks, GPT-4 only for complex
2. **Response caching**: identical/similar queries return cached results
3. **Prompt compression**: minimize system prompt token count
4. **Smart routing**: easy questions to cheap models, hard to expensive
5. **Token caching**: Anthropic/OpenAI prompt caching (25% premium, then 10x cheaper)
6. **Batch processing**: group similar requests

### Cost Formula
```text
Cost/request = (input_tokens * input_price + output_tokens * output_price)

GPT-4o example: 1000 in + 500 out = ~$0.0075
At 10,000 requests/day: ~$75/day
```

## CI/CD for LLM Applications

1. **Code changes**: standard CI/CD (tests, lint, deploy)
2. **Prompt changes**: run evaluation suite, compare against baseline, deploy if improved
3. **Model changes**: A/B test, monitor metrics, full rollout if stable
4. **RAG data changes**: re-index, run retrieval quality tests, deploy new index

## Gotchas
- LLM-as-Judge has biases (prefers verbose answers, favors certain styles) - calibrate with human labels
- Evaluation metrics can be gamed - use multiple complementary metrics
- Cost tracking must include ALL token sources (system prompts, function schemas, retries)
- Prompt regression testing is essential - a prompt improvement for one case can break another
- Production hallucination rate is hard to measure without periodic human review
- Model provider updates can change behavior without notice - pin model versions where possible

## See Also
- [[llm-api-integration]] - API monitoring and cost tracking
- [[rag-pipeline]] - RAG evaluation metrics
- [[langchain-framework]] - LangSmith for tracing
- [[production-patterns]] - Logging and evaluation patterns
- [[frontier-models]] - Model selection for cost optimization
