---
title: AI Coding Assistants
category: tools
tags: [llm-agents, copilot, cursor, claude-code, aider, code-generation]
---

# AI Coding Assistants

AI-powered development tools that assist with code completion, generation, editing, debugging, and explanation. They range from inline completions to full autonomous coding agents.

## Key Facts
- AI amplifies developer expertise, doesn't replace it
- More context = better completions (current file, imports, project structure, git history)
- First generation is a starting point - iterate through dialogue
- Always verify generated code, especially for security patterns
- Most effective for boilerplate, scaffolding, and repetitive patterns

## Tool Categories

### Code Completion (Inline)
- **GitHub Copilot**: inline completions, chat, context-aware suggestions
- **Cursor**: AI-native IDE with deep codebase understanding (Cmd+K for edits)
- **Cody (Sourcegraph)**: context-aware with codebase graph
- **Tabnine**: privacy-focused, runs locally
- **Amazon Q Developer**: AWS-integrated, security scanning

### CLI Agents
- **Claude Code (Anthropic)**: terminal-based coding agent with tool use
- **Aider**: terminal pair programming with Git integration
- **OpenAI Codex CLI**: command-line AI coding

### Chat-Based
- **ChatGPT**: good for explanations and snippets
- **Claude**: excellent at long code analysis, system design
- **Gemini**: multimodal (can analyze code screenshots)

## How They Build Context

1. Current file content (cursor position, selection)
2. Related files (imports, references)
3. Project structure (file tree, package.json)
4. Language server info (types, definitions)
5. Git history (recent changes)
6. Documentation (README, comments)

## Code Generation Patterns

| Pattern | Example |
|---------|---------|
| **Completion** | Predict next lines from context |
| **Instruction** | "Write a Fibonacci function" |
| **Edit** | "Refactor to async/await" |
| **Explain** | "What does this regex do?" |
| **Debug** | "Why is this null pointer?" |
| **Test generation** | "Write unit tests for this function" |
| **Documentation** | "Add JSDoc comments" |
| **Port** | "Convert this Python to Go" |

## Best Practices

1. **Verify everything**: AI generates plausible but sometimes incorrect code
2. **Provide context**: more context = better results
3. **Iterate**: refine through dialogue, don't expect perfection on first try
4. **Use for boilerplate**: most effective for repetitive scaffolding
5. **Review security**: AI may use insecure patterns (SQL injection, hardcoded secrets)
6. **Understand generated code**: don't blindly copy what you don't understand
7. **Generate tests alongside code**: tests verify correctness
8. **Domain expertise matters**: AI amplifies your knowledge, doesn't replace it

## Gotchas
- AI-generated code may contain security vulnerabilities - always review
- Generated tests may not cover edge cases - treat as starting point
- Code style may not match project conventions without explicit guidance
- Large context windows help but don't guarantee the tool reads all relevant code
- Over-reliance on AI assistance can slow skill development for new developers
- License concerns: some generated code may resemble training data

## See Also
- [[prompt-engineering]] - Writing effective coding prompts
- [[function-calling]] - How tools integrate with LLMs
- [[frontier-models]] - Which models are best for code
- [[production-patterns]] - Code as translation patterns
