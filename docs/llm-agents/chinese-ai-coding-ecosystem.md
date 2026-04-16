---
title: "Chinese AI Coding Ecosystem"
description: "Chinese AI coding tools, patterns, and community practices: Trae, OpenSpec, MetaGPT, GLM-5, DeepSeek, and spec-first development methodology."
---

# Chinese AI Coding Ecosystem

The Chinese AI coding ecosystem has converged on several patterns that differ from Western approaches: specification-first development, role-based multi-agent systems, cost-sensitive model selection, and layered CLAUDE.md modularization. Tools like Trae (ByteDance) and frameworks like MetaGPT originated here before gaining global adoption.

## Tools Landscape

### Trae (ByteDance AI-native IDE)

Three modes in a single IDE:

| Mode | Behavior |
|------|----------|
| **Chat** | Completion and Q&A, traditional copilot |
| **Builder** | Natural language → full project scaffold |
| **SOLO** | Autonomous planning + multi-step execution |

SOLO mode is the key differentiator: fully autonomous agent that decomposes tasks, executes, and monitors results without per-step user confirmation. Uses MCP protocol. Multi-model: Doubao-1.5-pro, DeepSeek R1/V3, Claude 3.5 Sonnet, GPT-4o. v2.0 released March 2026, pay-per-token pricing.

### MetaGPT / MGX

Multi-agent framework simulating a software company:

```text
Product Manager → Architect → Project Manager → Engineer → QA Engineer
```

Each agent has a defined role, receives context from predecessors, and passes structured output forward. Shared memory + SOP (Standard Operating Procedures) across all agents. Planning an AppStore-style plugin marketplace for 2026.

**Unique aspect:** human-AI hybrid teams where the human takes one of the roles (e.g., Product Manager) and AI agents fill the rest.

### Hermes Agent

```yaml
GitHub: NousResearch/hermes-agent (17K+ stars, MIT, Python, v0.8.0)
```

Built-in learning loop:
- Auto-skill creation from successful patterns
- Self-improving skills (agent rewrites underperforming skills)
- Cross-session persistent memory
- Multi-platform: Terminal, Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant

Widely adopted in Chinese community as a reference implementation of "agent that learns."

### Dify

All-in-one toolchain for RAG applications. Local deployment, multi-model integration. Primary use: enterprise Q&A bots, domain-specific assistants. Simpler alternative to LangChain for teams that want visual workflow building with local deployment option.

## OpenSpec - Specification-Driven Development

Chinese-origin contribution to AI coding methodology:

```yaml
GitHub: ForceInjection/OpenSpec-practise
Docs:   radebit.github.io/OpenSpec-Docs-zh/
```

Workflow:
```text
Create Change (Proposal) → Implement (Apply) → Archive
```

A lightweight spec layer that forces AI-human consensus on architecture BEFORE code generation. Each change request is a structured document:

```markdown
# Change: Add user authentication

## Context
Current state: public API, no auth

## Proposal
JWT-based auth with refresh tokens

## Acceptance criteria
- POST /auth/login returns JWT + refresh token
- Protected endpoints return 401 without valid JWT
- Tokens expire in 1h, refresh tokens in 30d
```

Only after this document is approved does the AI start generating code. The agent cannot modify the spec after approval (spec freeze before build - mirrors [[agent-design-patterns]] pattern).

AGENTS.md integration: ships with pre-configured agent workflows that reference spec documents.

## Chinese CLAUDE.md Patterns

### @import Modularization

Chinese developers use `@import` for CLAUDE.md more aggressively than Western counterparts. The main CLAUDE.md acts as an index; detailed docs live in separate files:

```markdown
# CLAUDE.md

@import ./rules/git-workflow.md
@import ./rules/code-style.md
@import ./rules/api-conventions.md
@import ./rules/chinese-specific.md
```

Rationale: bilingual teams often need separate Chinese and English contexts; language-switching works better in modular files than inline.

Up to 5 levels of recursive import supported. `@import` is disabled inside code blocks.

### Conciseness Guidelines (community consensus)

- Keep CLAUDE.md under 300 lines
- Every line must answer: "Would removing this cause mistakes?" - if not, cut it
- Frontier CoT models follow ~150-200 explicit instructions with reasonable consistency
- Don't duplicate rules already enforced by tooling (eslint, prettier → don't write lint rules in CLAUDE.md)
- `IMPORTANT/MUST/NEVER/ALWAYS` increase compliance but use sparingly - overuse degrades effect

### Layered Configuration Structure

```text
~/.claude/CLAUDE.md       - global (all sessions)
./CLAUDE.md               - project root (team-shared)
./CLAUDE.local.md         - personal project overrides
.claude/rules/*.md        - conditional context injection
```

## Vibe Coding vs Context Coding vs Spec Coding

Chinese discourse developed a taxonomy more explicitly than English-language content:

| Term | Meaning |
|------|---------|
| **Vibe Coding** | Casual, natural language → code, low precision |
| **Context Coding** | Deliberate context engineering for precise results |
| **Spec Coding** | Specification-first, human-AI consensus before implementation |

Key insight from guangzhengli: "Claude Code chose Unix tools (grep, find, git, cat) for context retrieval instead of RAG. By 2026 the real skill is Spec Coding - humans and AI reach consensus on architecture before coding."

## Chinese Tech Company Practices

### DeepSeek

- Internally uses Claude Code, Cursor, Copilot for their own development
- DeepSeek-V3.2 training includes agent synthetic data with reasoning capabilities in tool-calling scenarios
- Actively hiring for: Tool Use, Planning, long-term memory, Multi-Agent collaboration positions

### Zhipu AI (GLM-5)

- GLM-5 (754B params): SWE-bench-Verified 77.8, Terminal Bench 2.0 56.2
- First Chinese model company to offer a Coding Plan tier
- GLM-OS concept: AutoGLM (50+ step autonomous operations), GLM-PC (desktop agent)
- AutoGLM claimed to approach Claude Opus 4.5 performance on agent benchmarks

### Meituan

Published research on AI Coding and unit testing co-evolution: shifting from verification-driven to test-driven AI coding patterns.

## Key Repos

```text
claude-code-chinese/claude-code-guide  - community guide, API proxy patterns for China
cfrs2005/claude-init                   - 9 sub-agents, 10 slash commands, 8 rules, hooks
xianyu110/awesome-claudcode-tutorial   - 212+ articles, 25 chapters
KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh - combined Claude Code + OpenClaw, 21 lessons
phodal/build-coding-agent-context-engineering - context engineering for agents
datawhalechina/vibe-vibe               - systematic Vibe Coding tutorial
ForceInjection/OpenSpec-practise       - spec-driven dev implementation
```

## Network/Access Infrastructure

Chinese developers treat API access as a first-class infrastructure concern:
- `claude-init` ships with built-in proxy support ("no-VPN" access)
- API relay/routing configuration is part of default templates
- Cost comparisons weight token-per-yuan heavily; domestic models (GLM-5, DeepSeek) positioned as cost-effective fallbacks

## Gotchas

- **OpenSpec "spec freeze" requires enforcement, not trust.** Agents will bypass spec documents if not explicitly blocked from editing them. Implement a hook or file permission to make spec documents read-only after approval
- **@import chains can create invisible CLAUDE.md bloat.** Each imported file counts toward the effective prompt prefix. If 5 imported files total 2000 lines, that's 2000 tokens loaded every session even when irrelevant. Use conditional imports (`.claude/rules/*.md`) for context that's only sometimes needed
- **Role-based multi-agent systems (MetaGPT pattern) require strict output contracts.** When Product Manager agent hands off to Architect, the output format must be precisely defined. Ambiguous handoffs cause downstream agents to hallucinate upstream context

## See Also

- [[ai-coding-assistants]]
- [[context-engineering]]
- [[multi-agent-systems]]
- [[agent-design-patterns]]
- [[claude-code-ecosystem]]
