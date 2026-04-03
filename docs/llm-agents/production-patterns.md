---
title: Production LLM Patterns
category: techniques
tags: [llm-agents, production, patterns, copilot, knowledge-base, instruction-distillation]
---

# Production LLM Patterns

Battle-tested patterns for deploying LLM systems in production. These patterns address the gap between demo-quality RAG and reliable business applications, focusing on deterministic context injection, workflow decomposition, and human-in-the-loop automation.

## Key Facts
- Three business archetypes: data extraction (simplest), AI search/assistants (most popular), AI platforms (largest)
- Deterministic context injection often outperforms vector search for known question categories
- Workflow decomposition: simpler steps = fewer cognitive demands on the LLM
- Copilot pattern (partial automation) delivers 2-3x productivity gains
- Collect everything: request ID, timestamp, query, full trace - disk is cheap

## Patterns

### Pattern 1: Deterministic Context Injection (No RAG)

Instead of vector search, prepare data and feed directly to LLM:

```python
# For liquidity comparison question:
context = """
| Company | Liquidity (EUR) |
|---------|----------------|
| Dior Group | 7,040,000,000 |
| Bellevue Group | 890,000,000 |
| Unica Group | 2,100,000,000 |
"""
# LLM gives perfect answers every time
```

Use for high-accuracy categories while RAG handles general questions. This "cheating" scales better than you'd think.

### Pattern 2: Knowledge Base as Structured Files

Not a vector DB - folders with markdown files, Google Sheets, Confluence pages, databases. Information retrieved by known paths, not semantic search.

**Example - Business Translator:**
1. Script examines source document structure
2. Pulls translation guidelines for target language
3. Pulls domain-specific terminology dictionary
4. Pulls error history (past mistakes and corrections)
5. Assembles into context/prompt for LLM
6. Result: accurate domain-specific translations at low cost

### Pattern 3: Instruction Distillation

GPT-4 writes compressed instructions for weaker/cheaper models:
1. Describe business process to GPT-4
2. GPT-4 distills into executable instructions
3. Instructions are human-readable - reviewable by non-technical stakeholders
4. If a step fails, feed errors back: "rewrite so this doesn't happen"
5. Iterate until acceptable error rate

**Cross-model distillation**: GPT-4 writing instructions for local Mistral, iteratively simplifying until the weak model executes correctly.

### Pattern 4: Dedicated Agent Abstraction

Wrap prompt + context + knowledge base into a "dedicated agent" with name, role, specialization, example queries:
- Understandable by business stakeholders ("virtual specialist")
- Simplifies routing (router has list of agent descriptions)
- Enables dynamic scaling (new agents via configuration)
- Users can "train" new agents via simple forms

**Router pattern**: LLM classifies request against list of agents (name + specialization + examples). Routes to best match. Handles hundreds of specialists.

**Hybrid**: RAG handles 80% general queries. Router intercepts 20% high-accuracy categories to dedicated agents.

### Pattern 5: Workflow Decomposition

Break complex processes into simple sequential steps:

**Example - B2B Sales Assistant:**
1. Query expansion: user request -> search queries
2. Internet search + document download
3. Index downloaded content
4. Full-text + vector search
5. Result review (loop back to step 1 if insufficient)
6. Answer synthesis

**Advantages**: simpler steps, isolated debugging, human-verifiable, clear failure tracing.

### Pattern 6: Copilot / Human Envelope

Automate boring/repetitive parts, keep humans for judgment:

**Marketing Content Generator:**
- Human picks topic -> LLM discovers materials -> human verifies
- LLM generates 3 plans -> human picks best -> LLM writes draft -> human reviews
- 2-3x productivity (5-6 articles/day vs 1-2)

**Support Copilot:**
- Customer calls -> speech-to-text -> LLM processes in parallel
- LLM provides: customer profile, likely issue, proposed answer
- Human verifies and responds (70-80% faster) or overrides

### Pattern 7: Logging and Evaluation

**Collect everything**: request ID, timestamp, query, full trace (prompts, tokens, outputs, logprobs).

**Evaluation pipeline:**
1. Evaluate end-to-end quality
2. Trace issues to specific step
3. Identify problem (e.g., router misclassifying)
4. Build dataset of correct/incorrect
5. Modify prompt -> run against dataset -> measure
6. If better, deploy. If worse, rollback.

This is regular engineering - incremental improvements with measurements.

## LLM Known Limitations

| Limitation | Solution |
|-----------|---------|
| Math errors | Extract to Python/calculator tool |
| String manipulation | Use Python string operations |
| Physical world reasoning | Add chain-of-thought |
| Niche domains | Provide domain context explicitly |
| Rhyme detection | Text models lack phonetic training |

## Gotchas
- AI search/assistants statistically fail more often than data extraction due to hallucination
- Don't default to RAG when deterministic injection works for your category
- "Improving the system through training" is better business communication than "editing prompts"
- Always have a human fallback path for when the LLM fails
- Workflow decomposition adds latency but dramatically improves reliability
- Log storage is cheap - over-log rather than under-log

## See Also
- [[rag-pipeline]] - RAG approach for the general case
- [[prompt-engineering]] - Instruction distillation and prompt patterns
- [[agent-fundamentals]] - Agent abstraction concepts
- [[llmops]] - Monitoring and evaluation infrastructure
- [[agent-memory]] - Copilot and human-in-the-loop patterns
