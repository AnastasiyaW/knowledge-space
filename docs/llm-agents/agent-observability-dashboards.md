---
title: "Agent Observability Dashboards"
description: "Real-time observability for multi-agent and sub-agent systems: hook-based telemetry, event transport pipeline, visualization patterns, and tool landscape."
---

# Agent Observability Dashboards

Real-time visibility into running sub-agents, tool usage, token spend, and skill assignment. Covers hook-based telemetry capture specific to Claude Code multi-agent sessions; for orchestration coordination patterns see [[multi-session-coordination]], for metrics/evaluation pipelines see [[llmops]].

## Key Facts

- Claude Code exposes 12 hook event types covering the full session and sub-agent lifecycle
- `SubagentStart` / `SubagentStop` are the entry points for per-agent dashboarding; each carries a `subagent_type` field that maps to the invoked skill
- Events flow: hooks (Python/bash process) → HTTP collector → SQLite WAL → WebSocket → browser
- SQLite WAL mode is mandatory for concurrent multi-session writes; default journal mode causes exclusive write locks — see [[multi-session-coordination]] for the pattern
- Self-hosted dashboards give raw hook events; SaaS tracing tools (LangSmith, Phoenix) require OpenTelemetry instrumentation separate from hooks
- The gap between hook events and skill/checklist visibility requires a small overlay (~200-400 LOC) — hook events do not natively carry skill metadata or checklist progress

## Event Model

### 12 Hook Event Types

| Category | Events |
|---|---|
| Session lifecycle | `SessionStart`, `SessionEnd`, `Stop` |
| Multi-agent | `SubagentStart`, `SubagentStop` |
| Tool execution | `PreToolUse`, `PostToolUse`, `PostToolUseFailure` |
| User interaction | `PermissionRequest`, `Notification`, `UserPromptSubmit` |
| Context | `PreCompact` |

`SubagentStart` and `SubagentStop` bracket each spawned agent's lifetime. `PreToolUse` / `PostToolUse` fire for every tool call inside that agent, enabling per-agent tool attribution when correlated by session ID.

### Minimal Event Schema

```json
{
  "event_type": "SubagentStart",
  "session_id": "sess_abc123",
  "parent_session_id": "sess_parent456",
  "timestamp": "2026-05-12T14:03:22.411Z",
  "subagent_type": "general-purpose",
  "task_prompt": "Review PR #47 for security issues",
  "model": "claude-opus-4-8",
  "metadata": {
    "hook_event_name": "SubagentStart",
    "app_name": "my-project"
  }
}
```

```json
{
  "event_type": "PostToolUse",
  "session_id": "sess_abc123",
  "timestamp": "2026-05-12T14:03:45.002Z",
  "tool_name": "Read",
  "tool_input": { "file_path": "/src/auth.py" },
  "tool_result": "...",
  "duration_ms": 84,
  "token_usage": { "input": 1200, "output": 340 }
}
```

## Pipeline

### Hooks → Collector → Store → Live UI

```text
Claude agent process
  │  (PreToolUse / PostToolUse / SubagentStart / SubagentStop ...)
  ▼
Python hook script (~/.claude/settings.json → hooks[])
  │  HTTP POST to local collector
  ▼
Bun/Node collector (TypeScript)
  │  INSERT INTO events (WAL mode)
  ▼
SQLite (WAL)
  │  SELECT polling or change-notification
  ▼
WebSocket server
  │  push to connected browsers
  ▼
Browser dashboard (Vue 3 / React + Tailwind)
```

### Minimal Hook Script

Hooks receive event data on `stdin` as JSON. The script reads it, enriches if needed, and POSTs to the collector.

```python
#!/usr/bin/env python3
# ~/.claude/hooks/emit_event.py
# Configured in settings.json under hooks[].command for each event type

import json
import sys
import urllib.request

COLLECTOR_URL = "http://localhost:3001/events"

def main():
    payload = json.load(sys.stdin)
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        COLLECTOR_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=1)
    except Exception:
        pass  # never block the agent

if __name__ == "__main__":
    main()
```

### Hook Registration (settings.json)

```json
{
  "hooks": {
    "SubagentStart": [{ "type": "command", "command": "python ~/.claude/hooks/emit_event.py" }],
    "SubagentStop":  [{ "type": "command", "command": "python ~/.claude/hooks/emit_event.py" }],
    "PreToolUse":    [{ "type": "command", "command": "python ~/.claude/hooks/emit_event.py" }],
    "PostToolUse":   [{ "type": "command", "command": "python ~/.claude/hooks/emit_event.py" }],
    "SessionStart":  [{ "type": "command", "command": "python ~/.claude/hooks/emit_event.py" }],
    "SessionEnd":    [{ "type": "command", "command": "python ~/.claude/hooks/emit_event.py" }]
  }
}
```

### Collector SQLite Schema (minimal)

```sql
CREATE TABLE events (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id  TEXT NOT NULL,
  parent_id   TEXT,
  event_type  TEXT NOT NULL,
  ts          TEXT NOT NULL,
  payload     TEXT NOT NULL  -- JSON blob
);
PRAGMA journal_mode=WAL;

CREATE INDEX idx_session ON events(session_id);
CREATE INDEX idx_type    ON events(event_type);
CREATE INDEX idx_ts      ON events(ts);
```

### What to Visualize

| View | Data source | Key dimensions |
|---|---|---|
| Session tree | `SubagentStart` parent/child linking | Agent nesting depth, subagent_type |
| Per-agent tool timeline | `PreToolUse` / `PostToolUse` grouped by session_id | Tool name, file path, duration_ms |
| Token spend | `PostToolUse.token_usage` aggregated | Input/output per agent, cumulative |
| Latency heatmap | `duration_ms` across tool calls | Tool type vs time |
| Live pulse | All events in rolling window | Color-coded by session |
| Skill assignment overlay | `SubagentStart.subagent_type` → SKILL.md lookup | Agent → skill description |
| Checklist tracker | Parse bullet items from `task_prompt` → match against subsequent tool calls | % items resolved |

The skill assignment overlay and checklist tracker are not provided by any off-the-shelf dashboard as of May 2026 — both require a thin overlay reading your project's skill definitions.

## Tooling Landscape

### Self-Hosted (Hook-Native)

| Tool | Architecture | Strengths | Gaps |
|---|---|---|---|
| **disler/claude-code-hooks-multi-agent-observability** | Python hooks → Bun TS → SQLite WAL → Vue 3 + Tailwind | Closest fit for Claude Code; captures all 12 event types; session color coding; chat transcript viewer; live pulse | No skill→agent mapping; no checklist tracker; Vue 3 (not React) |
| **Marc Nuri AI Coding Agent Dashboard** | Heartbeat model + WebSocket relay + enricher pattern | Multi-device; git branch / PR link per session; remote terminal attach; push notifications; workflow templates | Not open source (as of May 2026); focused on cross-device orchestration, not per-agent skill visibility |

### SaaS / General LLM Tracing

| Tool | Model | Self-host | Claude Code native | Best fit |
|---|---|---|---|---|
| **LangSmith** | Trace + eval | No (cloud) | No (LangChain ecosystem) | LangGraph production stacks |
| **Langfuse** | Open-source tracing | Yes | No (OTel required) | General LLM prod, budget-conscious |
| **Arize Phoenix** | ML-grade, 7 span types | Yes | No (OTel required) | Large-scale production, embedding eval |
| **AgentOps** | Session replay, time-travel debug | No (cloud) | Partial | Debugging agent regressions |
| **Helicone** | Drop-in proxy | Yes (partial) | No (proxies API calls, not hooks) | Cost visibility on raw API usage |

**OTel instrumentation** is required for Langfuse/Phoenix/LangSmith. Claude Code hooks produce raw JSON; bridging to OTel spans needs a shim that maps `SubagentStart`→`SPAN_KIND_CLIENT` and `PostToolUse`→child spans. No maintained shim exists as of May 2026.

### Span Type Mapping (for OTel bridge)

```python
EVENT_TO_OTEL = {
    "SubagentStart":    "AGENT",
    "SubagentStop":     "AGENT",   # end marker
    "PreToolUse":       "TOOL",
    "PostToolUse":      "TOOL",    # end marker + result
    "UserPromptSubmit": "LLM",
    "SessionStart":     "CHAIN",
    "SessionEnd":       "CHAIN",
}
```

## Gotchas

- **Issue:** Hook script that raises an exception or times out blocks the agent that fired it. -> **Fix:** Wrap all network calls in `try/except`, use a short timeout (1s), and always `sys.exit(0)` — hooks must never block or crash the parent agent process.

- **Issue:** Multiple parallel sub-agents write to SQLite simultaneously without WAL mode, causing `database is locked` errors and dropped events. -> **Fix:** Always open the collector database with `PRAGMA journal_mode=WAL`. WAL allows concurrent readers alongside a single writer; without it, every INSERT takes an exclusive lock and parallel hooks contend. See [[multi-session-coordination]] for the canonical pattern.

- **Issue:** `PostToolUse` fires for the hook script itself if the hook is registered as a Bash tool call, creating recursive event loops. -> **Fix:** Register hooks using `"type": "command"` (subprocess invocation), not as tool calls. Hooks fired via `command` do not themselves trigger `PreToolUse`/`PostToolUse`.

- **Issue:** `subagent_type` in `SubagentStart` carries the agent's declared type (`general-purpose`, `code-review`, etc.), not the skill name passed in the task prompt. Skill-to-agent mapping requires parsing the `task_prompt` field for skill invocation patterns. -> **Fix:** In the skill overlay, regex-match `task_prompt` against your skill manifest (e.g. `\bcode-review\b`) to reconstruct the assignment; do not rely on `subagent_type` alone.

## See Also

- [[multi-session-coordination]] — git worktrees, SQLite WAL, advisory leases, hook integration for coordination
- [[llmops]] — production monitoring metrics, structured logging schema, alerting thresholds
- [[agent-orchestration]] — orchestrator tiers and task decomposition patterns
- [[multi-agent-systems]] — sub-agent spawning models and trust boundaries
- [[claude-code-ecosystem]] — full Claude Code tooling map
- [disler/claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability) — reference open-source dashboard
- [Marc Nuri AI Coding Agent Dashboard](https://blog.marcnuri.com/ai-coding-agent-dashboard) — heartbeat + enricher architecture writeup
- [Claude Code sub-agents docs](https://code.claude.com/docs/en/sub-agents) — SubagentStart/Stop payload spec
