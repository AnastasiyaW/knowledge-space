---
title: "Multi-Agent Messaging Patterns"
description: "Inter-agent communication patterns for Claude Code sessions: built-in Agent Teams, hook-based polling, MCP brokers, file P2P, and WebSocket approaches with trade-offs."
---

# Multi-Agent Messaging Patterns

How independent Claude Code sessions communicate. When multiple agents work on the same repo simultaneously (separate terminals, separate contexts), each needs a mechanism to discover messages from others without sharing a process.

## Pattern Comparison

| Pattern | Push/Pull | Latency | Dependencies | Windows | Maturity |
|---------|-----------|---------|-------------|---------|----------|
| Agent Teams (built-in) | Pull (polling) | Varies | None | Partial | Experimental |
| Hook-based polling | Pull (on interaction) | Next user msg | None | Yes | Stable |
| claude-peers-mcp | Push (channel) | ~1s | Bun + broker | Unknown | Very new |
| Session Bridge | Pull (5s poll) | 5s | Bash | Linux/Mac | New |
| AgentChattr | Pull (MCP calls) | ~5s | Server | Unknown | New |
| Channels (MCP push) | Push | Instant | Plugin + login | Unknown | Research preview |

## Claude Code Agent Teams (Built-in)

Enable via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Ships with Claude Code v2.1.32+.

### Architecture

```text
Team Lead
  ├── Teammate A (own 1M context)
  ├── Teammate B (own 1M context)
  └── Task list at ~/.claude/tasks/{team-name}/
```

### Mailbox Protocol (File-Based)

```text
~/.claude/teams/{team-name}/inboxes/{agent-name}.json
```

Each entry in the JSON array:
```json
{
  "from": "agent-lead",
  "text": "Please review the auth module",
  "timestamp": "2026-04-11T10:00:00Z",
  "read": false,
  "type": "task_assignment"
}
```

Message types: `task_assignment`, `message`, `broadcast`, `shutdown_request`, `plan_approval_request`, `idle_notification`.

**How delivery works:** teammates poll their own inbox file. New messages are injected as synthetic conversation turns (appear as if the user sent them). Pure pull model - no background process.

**Task locking:** `flock()` on a `.lock` file prevents race conditions when multiple teammates attempt to claim the same task.

### Limitations

- Designed for lead-spawned teams only - not pre-existing independent sessions
- No session resumption for in-process teammates
- One team per session, no nested teams
- Lead role is fixed after team creation
- Split-pane view doesn't work on Windows Terminal

## Hook-Based Polling (Recommended for Independent Sessions)

Most practical approach for pre-existing named sessions. Works on Windows. Zero dependencies.

### Configuration

```json
{
  "hooks": {
    "SessionStart": [{
      "type": "command",
      "command": "python .claude/scripts/mail.py check --who ani --unread-only"
    }],
    "UserPromptSubmit": [{
      "type": "command",
      "command": "python .claude/scripts/mail.py check --who ani --unread-only"
    }]
  }
}
```

### How It Works

1. `SessionStart` - check mailbox when session opens
2. `UserPromptSubmit` - check mailbox before processing EVERY user message
3. Hook prints unread messages to stdout
4. Claude sees them as injected context and acts on them

```python
# mail.py - minimal implementation
import sys, json
from pathlib import Path

def check(who: str, unread_only: bool = True):
    inbox = Path(f".claude/mailbox/{who}.json")
    if not inbox.exists():
        return
    messages = json.loads(inbox.read_text())
    for msg in messages:
        if unread_only and msg.get("read"):
            continue
        print(f"[MESSAGE from {msg['from']}]: {msg['text']}")
        msg["read"] = True
    inbox.write_text(json.dumps(messages, indent=2))
```

**Trade-offs:**
- Messages arrive on next user interaction (not true push)
- If agent runs a long autonomous task, messages queue until task completion
- For most team use cases (questions between agents on different modules), this latency is acceptable

## claude-peers-mcp (Real-Time Broker)

```yaml
GitHub: louislva/claude-peers-mcp
```

Local broker daemon + per-session MCP servers:

```text
Session A ──MCP──┐
Session B ──MCP──┤── Broker (SQLite + HTTP :7899) ── 1s polling
Session C ──MCP──┘
```

Each session can:
- `discover()` - list other active sessions
- `send_message(to="session-b", text="...")` - send to specific session
- Receive via `claude/channel` push protocol (instant delivery)

**Setup:**
```bash
# Start broker
npx claude-peers-mcp broker

# Add to .mcp.json
{
  "servers": {
    "peers": {
      "command": "npx",
      "args": ["claude-peers-mcp", "serve"]
    }
  }
}
```

**Trade-offs:** requires Bun/Node, broker daemon, Channels research preview feature.

## Session Bridge (File-Based P2P)

```yaml
GitHub: PatilShreyas/claude-code-session-bridge
```

Two-session direct messaging via filesystem:

```text
~/.claude/session-bridge/sessions/<6-char-id>/
  inbox/    - JSON message files
  outbox/
```

```bash
# Terminal 1: Session gets ID "abc123"
# Terminal 2: connect to abc123

# bridge-watcher.sh polls inbox every 5 seconds
# New queries trigger: claude -p "respond to: <query>"
```

**Trade-offs:** designed for 2 sessions (not team routing), requires manual ID exchange, background bash polling process.

## AgentChattr (MCP + WebSocket)

```yaml
GitHub: bcurts/agentchattr
Server: HTTP + WebSocket on :8200
```

Richer features: channels, @mentions, presence detection:

```python
# Agent reads messages
chat_read(sender="agent-b", since_cursor=42)

# Agent sends
chat_send(channel="general", text="@agent-b can you check auth.py?")

# @mention injects prompt into target agent's terminal
```

Terminal buffer hashing every 1s for activity detection. Heartbeat ping every 5s.

**Trade-offs:** most feature-rich, requires running server, overkill for small teams.

## Custom Channel Plugin (Future Pattern)

When Channels API stabilizes from research preview, a file-watching channel plugin enables true async delivery:

```typescript
// channel-plugin: watches mailbox directory
import { watch } from "fs";

watch(".claude/mailbox/ani/", (event, filename) => {
  if (event === "rename" && filename) {
    const message = readMailboxFile(filename);
    pushToSession(message);  // claude/channel protocol
  }
});
```

This enables delivery even during long autonomous tasks, without polling.

## Mailbox Format Convention

Standard mailbox file format for file-based systems:

```json
[
  {
    "id": "msg-001",
    "from": "artem",
    "to": "ani",
    "text": "The auth module is ready for review",
    "timestamp": "2026-04-11T10:30:00Z",
    "read": false,
    "type": "message",
    "thread_id": null
  }
]
```

**Directory layout:**
```text
.claude/mailbox/
  ani.json       - ani's inbox
  artem.json     - artem's inbox
  nastya.json    - nastya's inbox
```

## Gotchas

- **Agent Teams cannot resume in-process teammates.** If a teammate session closes (crash, manual exit), the team lead cannot re-attach it. Teammates are ephemeral - design workflows to be resumable from state files, not from session continuity
- **Hook-based polling delivers messages as context injection, not as tool calls.** The session sees inbox messages as additional context before responding. If the agent is mid-task with a nearly-full context window, new messages may be truncated. Keep message payloads small; for large data, write to a file and include the file path in the message
- **File-based mailboxes have race conditions without locking.** If two agents try to mark messages as read simultaneously, writes can conflict. Use atomic file operations: write to `.tmp`, then rename to final filename (rename is atomic on most filesystems)
- **claude-peers-mcp requires claude.ai login** (not API key auth) for the Channels feature. API-key-only setups cannot use Channels-based push delivery

## See Also

- [[multi-agent-systems]]
- [[agent-orchestration]]
- [[multi-session-coordination]]
- [[claude-code-ecosystem]]
- [[session-persistence]]
