---
title: AI IDE Rules and Context Configuration
category: misc/ai-coding-tools
tags: [ai-ide, rules, context-engineering, claude-code, antigravity, cursor, workspace-config]
---

# AI IDE Rules and Context Configuration

## Key Facts

- AI coding IDEs (Claude Code, Cursor, Google Antigravity, Gemini CLI) use **rules files** to inject persistent context into every conversation
- Rules = runtime config for the AI agent, not documentation for humans
- Two scopes: **global** (all projects on machine) and **workspace** (project-specific) - workspace overrides global
- Rule activation modes vary by IDE:
  - **Always-on** - loaded into every conversation automatically
  - **Model decision** - agent decides when to load based on a description field
  - **Glob pattern** - activated for specific file types (e.g., `*.tsx`, `*.py`)
  - **Manual** - loaded only when explicitly @-mentioned
- The description field is the **trigger** - it tells the model WHEN to load the rule, not what the rule does for humans
- A general/project rule should always be created FIRST before any coding work - it teaches the agent about your repo's tech stack, conventions, and structure
- Rules are portable across IDEs: a `skill.md` or `CLAUDE.md` works in Antigravity, Claude Code, and Codex with minor adjustments

### Rule File Locations by IDE

| IDE | Global | Workspace |
|-----|--------|-----------|
| Claude Code | `~/.claude/CLAUDE.md` | `./CLAUDE.md`, `.claude/rules/` |
| Antigravity | `~/.gemini/gemini.md` | `.agent/rules/*.md` |
| Cursor | `~/.cursor/rules/` | `.cursorrules` |

## Patterns

```markdown
# Example: Always-on general rule (.agent/rules/general.md)
# Activation: always_on

This is a React + TypeScript web application using Vite.
Tech stack: React 18, TypeScript 5, Tailwind CSS, Vitest.
Test command: `npm run test`
Build command: `npm run build`
All components are in src/components/.
Follow existing code style - functional components with hooks.
```

```markdown
# Example: Model-decision rule (.agent/rules/seo.md)
# Activation: model_decision
# Description: Apply when a new component is created or modified

## SEO Best Practices for React Components
- Add semantic HTML (header, main, nav, section)
- Include meta tags via react-helmet
- Use descriptive alt text on images
- Add internal linking where appropriate
```

```markdown
# Example: Glob-based rule (.agent/rules/api.md)
# Activation: glob
# Pattern: src/api/**/*.ts

## API Endpoint Conventions
- Use zod for request/response validation
- Return consistent error format { error: string, code: number }
- Add rate limiting middleware to all public endpoints
```

## Gotchas

- Rule content is injected into the context window - overly long rules waste tokens and can degrade model performance
- When model starts hallucinating, create a **new conversation** to clear context - don't keep adding corrections
- Rules don't take effect until a new conversation is started (the agent loads rule descriptions at conversation start)
- A bad description on a model-decision rule means the agent will never load it - test by explicitly asking the agent to use the rule
- Community rule directories (cursor.directory) provide starting templates but should be customized to your actual project

## See Also

- [[ai-coding-skills]] - reusable skill folders with instructions and support files
- [[ai-ide-workflow-modes]] - planning vs execution modes for AI coding
