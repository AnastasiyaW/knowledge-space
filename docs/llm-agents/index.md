---
title: LLM & AI Agents
type: MOC
---

# LLM & AI Agents

## Foundations
- [[transformer-architecture]] - A practical, version-aware guide to attention-based transformer structure, autoregressive decoding, positional information, and production configuration boundaries.
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
- [[vector-databases]] - Build vector retrieval around versioned embeddings, authorized metadata filters, provenance, recall evaluation, and safe migration rather than static product rankings.

## AI Agents
- [[agent-fundamentals]] - ReAct loop, agent components, types, agent vs workflow
- [[agent-design-patterns]] - Plan-and-execute, reflexion, MRKL, scratchpad, design principles
- [[multi-agent-systems]] - Supervisor, pipeline, hierarchical, debate patterns, CrewAI, AutoGen
- [[agent-memory]] - Short/long-term memory, HITL, copilot pattern, conversation management
- [[agent-security]] - Jailbreaks, prompt injection, data poisoning, defense strategies

## Frameworks and Tools
- [[langchain-framework]] - A version-aware guide to LangChain's current agent harness, provider integrations, middleware, state, and production boundaries.
- [[langgraph]] - Stateful graphs, conditional routing, human-in-the-loop, multi-agent orchestration
- [[no-code-platforms]] - n8n, FlowWise, Gradio UI building, deployment
- [[spring-ai]] - Java/Spring Boot LLM integration
- [[ai-coding-assistants]] - Copilot, Cursor, Claude Code, Aider, code generation patterns
- [[qwen-code]] - Qwen Code CLI installation, provider contract, and authentication history
- [[unsloth]] - Unsloth Core, Studio, Desktop, and model-specific fine-tuning bounds

## Model Operations
- [[fine-tuning]] - LoRA, QLoRA, PEFT, OpenAI fine-tuning, data quality
- [[model-optimization]] - Quantization (GGUF, GPTQ, AWQ), distillation, pruning
- [[ollama-local-llms]] - Local inference setup, quantization levels, model selection
- [[llmops]] - Evaluation, monitoring, cost optimization, CI/CD for LLM apps
- [[production-patterns]] - Deterministic context injection, copilot, workflow decomposition, logging

## Additional References

- [[adaptive-learning-systems]] - Architecture patterns for AI-powered education systems that adapt to individual learners
- [[adaptive-patterns-for-autonomous-agents]] - Adaptive agent architectures utilize dynamic hooks and structured state management to reduce
- [[agent-architectures]] - How to structure the control flow and state management of an LLM agent beyond individual patterns
- [[agent-deployment]] - Taking agents from prototype to production
- [[agent-evaluation]] - Evaluating agents is fundamentally harder than evaluating models
- [[agent-observability-dashboards]] - Real-time observability for multi-agent and sub-agent systems: hook-based telemetry, event
- [[agent-orchestration]] - Coordinate model calls, tools, handoffs, approvals, retries, and evidence through explicit task state rather than a framework-specific agent loop.
- [[agent-safety-alignment]] - Build agent safety as explicit authority, data, tool, approval, and evidence boundaries rather than as a prompt-only promise.
- [[agent-scope-evasion]] - Coding agents trained to reduce sycophancy exhibit a documented failure mode: when encountering
- [[agent-self-improvement]] - Techniques for agents to improve their own performance through reflection, step-level reward
- [[agentic-rl-competitive-programming]] - GrandCode (2026) achieves grandmaster-level performance on competitive programming problems by
- [[agentic-security-2026]] - A threat-model and control guide for tool-using agents, MCP integrations, persistent memory, and irreversible effects. Scope checked 2026-09-03.
- [[agentic-systems-landscape-2026]] - Multi-agent protocols, SDK comparison, orchestration patterns, and real-world coding agent
- [[ai-adaptive-learning-systems]] - A version-aware architecture for learner evidence, deterministic scheduling, constrained LLM tutoring, evaluation, and learner-data safeguards.
- [[ai-agent-ide-features]] - Design and evaluate AI-assisted coding environments around workspace isolation, explicit permissions, durable task artifacts, verification, and review.
- [[autonomous-agent-evolution]] - Replacing fixed evolutionary search (agents as stateless workers) with long-lived autonomous agents
- [[chinese-ai-coding-ecosystem]] - Chinese AI coding tools, patterns, and community practices: Trae, OpenSpec, MetaGPT, GLM-5
- [[claude-adaptive-thinking]] - Configure and evaluate Claude reasoning effort without relying on fixed, model-specific folklore.
- [[claude-code-degradation-2026]] - A receipt-based method for diagnosing coding-agent quality, configuration, cost, and availability changes without inventing a vendor incident.
- [[claude-code-ecosystem]] - Claude Code plugin system, hooks lifecycle, skills patterns, CLAUDE.md best practices, and the
- [[claude-code-harness-patterns]] - A practical boundary between instructions, tools, deterministic gates, review, and durable evidence for coding-agent work.
- [[claude-desktop-session-management]] - Claude Desktop stores conversation history and environment state in local session files
- [[claude-managed-agents]] - Managed agent runtimes separate the core model (Brain) from the execution sandbox (Hands) and the
- [[context-engineering]] - Managing what information goes into the LLM context window and when
- [[gradio-llm-interfaces]] - Rapid prototyping of chat UIs with streaming, markdown rendering, and multi-model comparison
- [[handoff-rollup-pattern]] - How to create a bounded, auditable rollup of long-running agent work without pretending that a summary is lossless.
- [[kv-cache-compression]] - Reducing KV cache memory during LLM inference to enable longer contexts and more concurrent
- [[llm-fine-tuning-practical]] - End-to-end guide for frontier API and QLoRA fine-tuning with when-to-use decision framework
- [[llm-persona-design-and-engineering]] - Persona design for LLM agents involves mapping abstract character traits to concrete linguistic
- [[managed-agents]] - A version-aware guide to Anthropic's managed agent harness: agent configuration, environments, sessions, events, permission policies, and data boundaries.
- [[multi-agent-messaging]] - Inter-agent communication patterns for Claude Code sessions: built-in Agent Teams, hook-based
- [[multi-agent-systems-architectures-2026]] - Multi-agent systems (MAS) have diverged into two primary architectural schools: role-based
- [[multi-session-coordination]] - Durable coordination patterns for several coding-agent sessions: isolated worktrees, manifests, append-only evidence, exclusive-resource leases, and verified integration.
- [[notebooklm-integration]] - Using Google NotebookLM as a free research backend for Claude Code - token-saving workflows
- [[oh-my-claudecode-omc-architecture]] - Oh My ClaudeCode (OMC) is an agentic framework extending Claude Code (v4.13.2) through a layered
- [[persona-adaptive-llm]] - A decision framework for profile fields, retrieval memory, and adapter-based personalization with tenant isolation, evaluation, consent, and deletion boundaries.
- [[scaling-laws-and-benchmarks]] - Chinchilla scaling law, standard benchmarks (ARC, DROP, HellaSwag), and model selection guidelines
- [[social-media-mcp-tools]] - A provider-neutral, approval-first design for using MCP to draft, validate, and publish social content without treating a social post as a reversible chat action.
- [[swarm-based-review-and-multisampling-in-agentic-workflows]] - Multisampling and swarm-based review are techniques used to scale LLM reasoning performance at
- [[telegram-managed-bots]] - Per-user isolated bot instances deployed via a manager bot
- [[token-optimization]] - Reducing token consumption in agent systems without degrading task performance
- [[tool-use-patterns]] - How to design, expose, and manage tools for LLM agents
- [[uml-driven-agent-development]] - Model-first approach to agent workflow design: specify behavior as diagrams-as-code before writing
