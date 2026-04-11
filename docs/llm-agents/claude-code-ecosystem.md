---
title: "Claude Code Ecosystem (2026)"
description: "Claude Code plugin system, hooks lifecycle, skills patterns, CLAUDE.md best practices, and the managed agents architecture as of April 2026."
---

# Claude Code Ecosystem (2026)

Claude Code's plugin/skill/hooks ecosystem as it stands in April 2026. Covers the plugin manifest format, all hook event types, skills patterns, CLAUDE.md organization, and the Managed Agents meta-harness introduced in April 2026.

## Plugin System

A plugin is a directory with a `.claude-plugin/plugin.json` manifest:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "commands": ["commands/"],
  "agents": ["agents/"],
  "skills": ["skills/"],
  "hooks": ["hooks/"],
  "mcp": ".mcp.json"
}
```

Install and test:
```bash
# Development/testing without install
claude --plugin-dir ./my-plugin

# Install from directory
claude plugin install ./my-plugin

# Install from registry
claude plugin install @org/plugin-name
```

Plugin settings.json can activate a custom agent as the main thread:
```json
{
  "agent": "agents/my-specialist.md"
}
```

## Hooks System

21 lifecycle events across 4 handler types:

| Handler Type | Mechanism | Use Case |
|---|---|---|
| `command` | Shell command execution | Linting, validation, git checks |
| `http` | HTTP request | External notifications, webhooks |
| `prompt` | LLM-based handler | Contextual analysis |
| `agent` | Agent handler | Complex routing decisions |

### Key Hook Events

| Event | Blocking? | Notes |
|-------|-----------|-------|
| `PreToolUse` | YES (only blocking hook) | Can deny, defer, or modify tool calls |
| `PostToolUse` | No | Observe completed tool calls |
| `SessionStart` | No | Load state, check mailboxes |
| `UserPromptSubmit` | No | Check inboxes before response |
| `TaskCreated` | No | React to sub-agent task spawning |
| `Stop` | No | Write handoff, archive state |
| `PermissionDenied` | No | Can return `{retry: true}` to re-attempt |

### Conditional Hooks (v2.1.89+)

```json
{
  "hooks": {
    "PreToolUse": [{
      "type": "command",
      "command": "validate_git.sh",
      "if": "Bash(git *)"
    }]
  }
}
```

`if` field reduces overhead - hook only runs when the condition matches the tool call pattern. Supports `mcp__<server>__<tool>` patterns for MCP tool calls.

### Defer Decision for Headless Agents

```bash
# Hook returns defer to pause headless session before destructive ops
echo '{"decision": "defer"}'
# Session resumes with: claude -p --resume <session-id>
```

### CLAUDE.md vs Hooks

```
CLAUDE.md → guidelines ("prefer Bun over npm")
Hooks     → rules that must never be broken ("always run prettier before commit")
```

Hooks are shell processes - they execute mechanically on every matching event. CLAUDE.md is read as context - it can be deprioritized under context pressure.

## Skills

Skills are SKILL.md files in `.claude/skills/` or `skills/` inside a plugin. Claude uses them automatically when relevant, or via `/skill-name` invocation.

```markdown
# SKILL.md format

## Description
[What this skill does + WHEN to use it - specific trigger phrases]

## Steps
1. ...
2. ...

## Gotchas
- ...
```

### Skills Best Practices (2026)

- Skills under 2,000 tokens perform best - split larger skills
- Create a skill when you paste the same playbook more than 3 times
- Use `$ARGUMENTS` for parameterized behavior: `/deploy staging` passes `staging` as `$ARGUMENTS`
- Skills for domain-specific knowledge; CLAUDE.md for session-invariant config
- On-demand hooks in skills: `/careful` activates PreToolUse guard against destructive commands
- Measure skill usage with PostToolUse hooks to find undertriggering skills

## CLAUDE.md Organization

```
~/.claude/CLAUDE.md            - global (loads in all sessions)
./CLAUDE.md                    - project root (team-shared, check into git)
./CLAUDE.local.md              - personal project overrides (gitignored)
./path/to/subdir/CLAUDE.md     - monorepo subproject context
.claude/rules/*.md             - conditional context injection (topic-specific)
```

**Authoring principles:**
- For each instruction: "Would removing this cause a mistake?" - if no, cut it
- Commands before explanations: `npm test` before describing what tests do
- Code examples over prose descriptions for style guides
- Don't duplicate what deterministic tooling already enforces (linters, formatters)
- Commit project CLAUDE.md to git - knowledge compounds over time

## AGENTS.md (Cross-Tool Standard)

Open standard under Linux Foundation AAIF. Supported by 25+ tools: Codex, Copilot, Cursor, Windsurf, Jules, Amp, Kilo, Factory. Claude Code uses CLAUDE.md instead (issue #6235, 3200+ upvotes for native AGENTS.md support).

Best practices from 2,500+ repo analysis:
- Max ~150 lines (fits in single cached prompt prefix)
- 6 core areas: commands, testing, project structure, code style, git workflow, boundaries
- Start simple, iterate when agent makes mistakes - don't front-load everything
- Nested AGENTS.md per package/subproject, nearest wins

## Managed Agents (April 2026)

New meta-harness approach from Anthropic:

```python
# Core interface
execute(name: str, input: str) -> str
```

Decouples "brain" from "hands". The orchestrating agent calls `execute("test-runner", "run tests for auth module")` and gets back a string result. The named agent handles its own tool use, context, and execution.

Key properties:
- Supports any custom tool + any MCP server
- Opinionated about interfaces (session state + sandbox)
- Unopinionated about specific harness design
- Public beta launched April 2026

**Context engineering shift (2026 Agentic Coding Trends Report):**
> Bottleneck shifted from "agent doesn't understand what I want" to "agent doesn't have the context it needs." Context engineering now dominates over prompt engineering.

## Recent Version Features (v2.1.89 - v2.1.98)

| Version | Feature |
|---------|---------|
| v2.1.89 | Conditional hooks (`if` field), `defer` for headless agents, `PermissionDenied` event, autocompact circuit breaker (stops after 3 refills) |
| v2.1.98 | Monitor tool for streaming background script events, subprocess sandboxing (PID namespace isolation on Linux), `CLAUDE_CODE_SCRIPT_CAPS` per-session script limit, fixed Bash permission bypass |
| March 2026 | Computer Use (Pro/Max), Scheduled Tasks (`/loop` cron, `/schedule` cloud), Auto Mode (heuristic permissions), PowerShell tool (Windows preview) |

### Auto Mode

Heuristic-based permission management:
- Low-stakes operations (rename var, format) proceed automatically
- Risky actions (delete, deploy, push) blocked or require confirmation
- Aggressiveness tunable via settings

### Monitor Tool (v2.1.98)

```bash
# Stream events from a background script into the session
claude monitor ./my-background-process.sh
```

Allows headless agents to observe long-running processes without polling.

## Community Resources

| Repo | Stars | Contents |
|------|-------|----------|
| rohitg00/awesome-claude-code-toolkit | 380+ | 135 agents, 35 skills, 42 commands, 176+ plugins, 20 hooks |
| alirezarezvani/claude-skills | - | 220+ skills (engineering, marketing, product, compliance) |
| hesreallyhim/awesome-claude-code | - | Agentic patterns with Mermaid diagrams, subagent orchestration |
| anthropics/skills | Official | Official skill marketplace |

## Gotchas

- **PreToolUse is the ONLY blocking hook.** PostToolUse, SessionStart, and other events are observation-only. If you need to prevent an action, it must be a PreToolUse hook - no other event can stop execution
- **Skills with `$ARGUMENTS` fail silently when invoked without arguments.** If your skill uses `$ARGUMENTS` and a user invokes it with no arguments, the variable is empty string. Add a guard: check `[[ -z "$ARGUMENTS" ]]` and return a usage hint
- **Autocompact circuit breaker triggers after 3 context refills.** Long sessions with rapid context growth will halt at the 3rd compaction rather than running indefinitely. Design long-running agents to write state to files (not rely on context) before each potential compaction point
- **`defer` decision requires `--resume` to be called explicitly.** A deferred headless session sits paused until resumed. If nothing calls `claude -p --resume <id>`, the session blocks indefinitely. Always implement a timeout or supervisor that handles deferred sessions

## See Also

- [[ai-coding-assistants]]
- [[context-engineering]]
- [[multi-agent-systems]]
- [[agent-orchestration]]
- [[multi-agent-messaging]]
- [[chinese-ai-coding-ecosystem]]
