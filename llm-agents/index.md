---
title: "LLMs & AI Agents - Knowledge Map"
category: llm-agents
tags: [index, moc, map-of-content]
---

# LLMs & AI Agents - Knowledge Map

Reference knowledge base for building LLM-powered applications and AI agents.

## Fundamentals

- [[tokenization]] - tokens, BPE, context windows, token limits and pricing
- [[model-selection]] - choosing the right model (frontier vs open-source, cost vs quality)
- [[api-integration]] - connecting to LLM APIs (OpenAI, Anthropic, Gemini), authentication, rate limits

## Prompting & Output

- [[prompt-engineering]] - system/user prompts, few-shot, chain-of-thought, prompting techniques
- [[structured-output]] - JSON mode, Pydantic parsing, schema validation, checklist pattern

## Retrieval & Knowledge

- [[rag-pipeline]] - end-to-end retrieval-augmented generation architecture
- [[embeddings]] - text-to-vector conversion, similarity search, embedding models
- [[vector-databases]] - ChromaDB, Pinecone, FAISS, pgvector - storage and search
- [[chunking-strategies]] - document splitting, chunk size/overlap, PDF parsing

## Agents & Orchestration

- [[agent-architectures]] - ReAct, Reflection, Reflexion, Plan-and-Solve, workflow patterns
- [[function-calling]] - tool use, external API integration, structured tool schemas
- [[multi-agent-systems]] - supervisor-worker, CrewAI, AutoGen, agent collaboration
- [[memory-and-context]] - conversation history, long-term memory, context management

## Frameworks & Infrastructure

- [[langchain]] - chains, agents, retrievers, LCEL, ecosystem overview
- [[langgraph]] - stateful agent graphs, cycles, human-in-the-loop, checkpointing
- [[huggingface-transformers]] - model hub, pipeline API, sentence-transformers
- [[ollama-local-llms]] - running open-source LLMs locally, privacy, OpenAI-compatible API

## Training & Quality

- [[fine-tuning]] - SFT, LoRA, QLoRA, PEFT, RLHF, when to fine-tune vs RAG
- [[llm-evaluation]] - benchmarks, LLM-as-judge, A/B testing, RAGAS
- [[guardrails]] - safety, prompt injection defense, jailbreaks, output filtering

## Concept Graph

```
                    +-----------------+
                    | model-selection |
                    +--------+--------+
                             |
              +--------------+--------------+
              |                             |
    +---------v---------+        +----------v----------+
    | ollama-local-llms |        |   api-integration   |
    +-------------------+        +----------+----------+
                                            |
                              +-------------+-------------+
                              |                           |
                    +---------v--------+        +---------v---------+
                    | prompt-engineering|        | function-calling  |
                    +--------+---------+        +---------+---------+
                             |                            |
                    +--------v---------+        +---------v---------+
                    | structured-output|        | agent-architectures|
                    +------------------+        +---------+---------+
                                                          |
    +------------------+                        +---------v---------+
    |   fine-tuning    |                        | multi-agent-systems|
    +------------------+                        +-------------------+
                                                          |
    +------------------+    +------------------+   +------v---------+
    | chunking-strategies|-->|   rag-pipeline  |-->| memory-context |
    +------------------+    +--------+---------+   +----------------+
                                     |
                            +--------+---------+
                            |                  |
                   +--------v-----+   +--------v--------+
                   |  embeddings  |   | vector-databases |
                   +--------------+   +-----------------+

    +------------------+    +------------------+
    | llm-evaluation   |    |   guardrails     |
    +------------------+    +------------------+

    +------------------+    +------------------+
    |    langchain     |--->|    langgraph     |
    +------------------+    +------------------+
    |  huggingface-transformers                |
    +------------------------------------------+
```
