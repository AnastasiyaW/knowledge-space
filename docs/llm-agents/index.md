---
title: LLM & AI Agents
type: MOC
---

# LLM & AI Agents

## Foundations
- [[transformer-architecture]] - Self-attention, encoder/decoder, multi-head attention, positional encoding
- [[tokenization]] - BPE, WordPiece, SentencePiece, context windows, token counting
- [[embeddings]] - Vector representations, similarity metrics, embedding models, known issues
- [[frontier-models]] - GPT, Claude, Llama, Mistral, Gemini comparison and selection guide

## Prompting and Generation
- [[prompt-engineering]] - System prompts, few-shot, chain-of-thought, checklist pattern, instruction distillation
- [[function-calling]] - OpenAI/Anthropic tool use APIs, tool descriptions, validation
- [[llm-api-integration]] - Chat completions, message roles, streaming, parameters, cost management

## Retrieval-Augmented Generation
- [[rag-pipeline]] - RAG architecture, hallucination problem, improvement strategies, evaluation
- [[chunking-strategies]] - Text splitting, chunk sizes, semantic chunking, document loaders
- [[vector-databases]] - Chroma, Pinecone, Qdrant, FAISS, ANN algorithms, hybrid search

## AI Agents
- [[agent-fundamentals]] - ReAct loop, agent components, types, agent vs workflow
- [[agent-design-patterns]] - Plan-and-execute, reflexion, MRKL, scratchpad, design principles
- [[multi-agent-systems]] - Supervisor, pipeline, hierarchical, debate patterns, CrewAI, AutoGen
- [[agent-memory]] - Short/long-term memory, HITL, copilot pattern, conversation management
- [[agent-security]] - Jailbreaks, prompt injection, data poisoning, defense strategies

## Frameworks and Tools
- [[langchain-framework]] - LCEL, chains, agents, RAG chains, LangSmith monitoring
- [[langgraph]] - Stateful graphs, conditional routing, human-in-the-loop, multi-agent orchestration
- [[no-code-platforms]] - n8n, FlowWise, Gradio UI building, deployment
- [[spring-ai]] - Java/Spring Boot LLM integration
- [[ai-coding-assistants]] - Copilot, Cursor, Claude Code, Aider, code generation patterns

## Model Operations
- [[fine-tuning]] - LoRA, QLoRA, PEFT, OpenAI fine-tuning, data quality
- [[model-optimization]] - Quantization (GGUF, GPTQ, AWQ), distillation, pruning
- [[ollama-local-llms]] - Local inference setup, quantization levels, model selection
- [[llmops]] - Evaluation, monitoring, cost optimization, CI/CD for LLM apps
- [[production-patterns]] - Deterministic context injection, copilot, workflow decomposition, logging
