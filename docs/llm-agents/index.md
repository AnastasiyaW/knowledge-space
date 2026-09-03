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
- [[multi-agent-systems]] - Coordinate multiple agents through task contracts, ownership, authority, state, and evidence boundaries; add agents only when a measured decomposition needs them.
- [[agent-memory]] - Short/long-term memory, HITL, copilot pattern, conversation management
- [[agent-security]] - Jailbreaks, prompt injection, data poisoning, defense strategies

## Frameworks and Tools
- [[langchain-framework]] - A version-aware guide to LangChain's current agent harness, provider integrations, middleware, state, and production boundaries.
- [[langgraph]] - Stateful graphs, conditional routing, human-in-the-loop, multi-agent orchestration
- [[no-code-platforms]] - n8n, FlowWise, Gradio UI building, deployment
- [[spring-ai]] - Java/Spring Boot LLM integration
- [[ai-coding-assistants]] - Operate AI coding assistants through explicit scope, data, tool, approval, and evidence boundaries instead of product rankings or trust in generated code.
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
- [[adaptive-patterns-for-autonomous-agents]] - Use explicit task state, bounded hooks, capability-scoped subagents, and evidence-based gates instead of opaque keyword triggers or arbitrary ambiguity scores.
- [[agent-architectures]] - How to structure the control flow and state management of an LLM agent beyond individual patterns
- [[agent-deployment]] - Taking agents from prototype to production
- [[agent-evaluation]] - Evaluate agent behavior with versioned task fixtures, deterministic validators, controlled side-effect checks, and reproducible evidence rather than a single benchmark score.
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
- [[claude-code-ecosystem]] - Use Claude Code plugins, skills, hooks, project instructions, and subagents as explicit, versioned governance surfaces; verify their current schema and effective scope before rollout.
- [[claude-code-harness-patterns]] - A practical boundary between instructions, tools, deterministic gates, review, and durable evidence for coding-agent work.
- [[claude-desktop-session-management]] - Use supported export, account, and extension controls rather than relying on unversioned local cache internals for conversation recovery or cross-device synchronization.
- [[claude-managed-agents]] - Define organization-managed Claude Code subagents with explicit scope, precedence, tool limits, and verification rather than treating managed configuration as a cloud execution runtime.
- [[context-engineering]] - Treat model context as a bounded working input and preserve task state, evidence, authority, and retrieval provenance in versioned artifacts rather than fixed token allocations.
- [[gradio-llm-interfaces]] - Rapid prototyping of chat UIs with streaming, markdown rendering, and multi-model comparison
- [[handoff-rollup-pattern]] - How to create a bounded, auditable rollup of long-running agent work without pretending that a summary is lossless.
- [[kv-cache-compression]] - Reducing KV cache memory during LLM inference to enable longer contexts and more concurrent
- [[llm-fine-tuning-practical]] - End-to-end guide for frontier API and QLoRA fine-tuning with when-to-use decision framework
- [[llm-persona-design-and-engineering]] - Design an LLM persona as a versioned behavioral policy with explicit authority, privacy, escalation, and evaluation boundaries rather than as an assumed model personality.
- [[managed-agents]] - A version-aware guide to Anthropic's managed agent harness: agent configuration, environments, sessions, events, permission policies, and data boundaries.
- [[multi-agent-messaging]] - Inter-agent communication patterns for Claude Code sessions: built-in Agent Teams, hook-based
- [[multi-agent-systems-architectures-2026]] - Multi-agent systems (MAS) have diverged into two primary architectural schools: role-based
- [[multi-session-coordination]] - Durable coordination patterns for several coding-agent sessions: isolated worktrees, manifests, append-only evidence, exclusive-resource leases, and verified integration.
- [[notebooklm-integration]] - Using Google NotebookLM as a free research backend for Claude Code - token-saving workflows
- [[oh-my-claudecode-omc-architecture]] - How to adopt the fast-moving OMC plugin without mistaking third-party commands, model routing, or generated state for a stable security or release boundary.
- [[persona-adaptive-llm]] - A decision framework for profile fields, retrieval memory, and adapter-based personalization with tenant isolation, evaluation, consent, and deletion boundaries.
- [[scaling-laws-and-benchmarks]] - Chinchilla scaling law, standard benchmarks (ARC, DROP, HellaSwag), and model selection guidelines
- [[social-media-mcp-tools]] - A provider-neutral, approval-first design for using MCP to draft, validate, and publish social content without treating a social post as a reversible chat action.
- [[swarm-based-review-and-multisampling-in-agentic-workflows]] - Generate independent candidates, validate evidence, and select agent outputs through explicit acceptance criteria rather than fixed vote counts or model confidence.
- [[telegram-managed-bots]] - A production-safe guide to Telegram's manager-bot model: creation, token rotation, access settings, state isolation, and lifecycle receipts.
- [[token-optimization]] - Reducing token consumption in agent systems without degrading task performance
- [[tool-use-patterns]] - How to design, expose, and manage tools for LLM agents
- [[uml-driven-agent-development]] - Use small, versioned sequence, state, and trust-boundary diagrams to clarify agent workflows, then validate them in the renderer and CI target that will publish them.
