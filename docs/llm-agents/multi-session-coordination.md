---
title: "Multi-Session Agent Coordination"
description: "Patterns and tools for coordinating multiple Claude Code sessions: git worktrees, tmux orchestration, advisory leases, pre-commit guards, and orchestrator tiers."
---

# Multi-Session Agent Coordination

Running multiple Claude Code sessions in parallel on the same repository. Each session needs filesystem isolation, task ownership, coordination signals, and safe merge paths. The ecosystem has converged on a small set of primitives used across all major tools.

## Core Primitives (Ecosystem Consensus)

| Primitive | Role | Why |
|-----------|------|-----|
| **Git worktrees** | Filesystem isolation | Each agent gets its own working tree, no file conflicts |
| **tmux** | Session management | Persistent terminals, multiplexing, scriptable |
| **SQLite WAL mode** | Coordination database | Concurrent reads + writes without full locking |
| **Advisory file leases** | Task ownership | Soft locks that survive crashes (unlike hard locks) |
| **Pre-commit guards** | Enforcement point | Hooks fire at commit time, not runtime |
| **Claude Code hooks** | Integration surface | SessionStart, PreToolUse, PostToolUse as coordination events |

## Orchestrator Tiers

### Tier 1 - Lightweight Orchestrators

**multiclaude** (Dan Lorenc)
- tmux + git worktrees
- Single-player and multiplayer modes
- Each agent gets own worktree: `git worktree add .worktrees/agent-a`

**Gas Town** (Steve Yegge)
- Three-tier watchdog architecture
- htmx dashboard for monitoring session state
- Designed for long-running autonomous agents

**oh-my-claudecode**
- 32 specialized agents with auto model routing
- 3-5x speedup claim vs single session
- Opinionated defaults for common workflows

### Tier 2 - Full Orchestration

**Composio Agent Orchestrator**
- Agent-agnostic (works with Claude Code, Codex, etc.)
- Worktree-per-agent automatic provisioning
- Auto CI fix: agent reads CI failure, patches, re-runs

**Overstory** (Jaymin West)
- 11 runtime adapters
- SQLite WAL mail (messages stored in SQLite, not JSON files)
- Native Claude Code hooks integration

**claude-swarm**
- Dependency graph: tasks with explicit dependencies prevent ordering errors
- Parallel execution where dependency graph allows
- Designed for large codebases with clear module boundaries

### Tier 3 - Session Management UI

**Nimbalyst** - desktop app, kanban view for 10+ simultaneous sessions
**Parallel Code** - tiled view, worktree per session, QR monitoring for remote sessions

## Git Worktrees Pattern

Foundation for all multi-session setups:

```bash
# Create isolated working trees for each agent
git worktree add .worktrees/feature-auth origin/main
git worktree add .worktrees/feature-api origin/main
git worktree add .worktrees/feature-tests origin/main

# Each agent cd's to its worktree, full git history accessible
# Branches are independent, no file conflicts
cd .worktrees/feature-auth && claude
```

**Why worktrees over branches in the same directory:**
- Agents can't accidentally edit each other's files
- `git status` is clean in each context
- Parallel `npm install` / `cargo build` don't conflict

```bash
# List worktrees
git worktree list

# Clean up after merge
git worktree remove .worktrees/feature-auth
```

## Advisory File Leases

Soft locks that express intent without blocking:

```text
.agent-locks/
  auth-module.lock       - "ani is working on this"
  api-routes.lock        - "artem is working on this"
```

```json
{
  "agent": "ani",
  "task": "refactor auth module",
  "started": "2026-04-11T10:00:00Z",
  "files": ["src/auth/*.ts"],
  "ttl": 3600
}
```

**Advisory vs hard locks:**
- Hard lock: if holder crashes, other agents block indefinitely
- Advisory lease: other agents see the lock, can choose to wait, ask, or proceed
- TTL ensures stale leases expire automatically

**MCP Agent Mail** (Dicklesworthstone) extends this with:
- Git-backed mailboxes (messages persist through crashes)
- Pre-commit guard as enforcement (not just advisory)
- Rust version for production deployments

## Pre-Commit Guard Pattern

Hooks at `pre-commit` time are more reliable than runtime checks:

```bash
#!/bin/bash
# .git/hooks/pre-commit (or via husky)

# Check if any locked file is being committed
for file in $(git diff --cached --name-only); do
  lock_file=".agent-locks/${file//\//-}.lock"
  if [ -f "$lock_file" ]; then
    owner=$(jq -r '.agent' "$lock_file")
    current=$(git config user.name)
    if [ "$owner" != "$current" ]; then
      echo "ERROR: $file is locked by $owner"
      exit 1
    fi
  fi
done
```

Pre-commit fires on every `git commit`, making it the natural enforcement point for ownership rules regardless of which tool or workflow triggered the commit.

## Claude Code Hooks Integration

Multi-session systems hook into Claude Code's lifecycle:

```json
{
  "hooks": {
    "SessionStart": [{
      "type": "command",
      "command": "python .agent/register.py --name ani"
    }],
    "PreToolUse": [{
      "type": "command",
      "command": "python .agent/check_lock.py",
      "if": "Write(*) | Edit(*)"
    }],
    "Stop": [{
      "type": "command",
      "command": "python .agent/release_locks.py --name ani"
    }]
  }
}
```

This integrates lock acquisition/release directly into the session lifecycle.

## Inter-Agent Messaging

For message passing between sessions, see [[multi-agent-messaging]]. Summary:

- **Hook-based polling** (UserPromptSubmit) - simplest, works on Windows, no dependencies
- **Agent Teams mailbox** - built-in but designed for spawned teams, not pre-existing sessions
- **SQLite WAL** (Overstory pattern) - concurrent readers, message persistence
- **MCP broker** (claude-peers-mcp) - real-time but requires Bun + running broker

## Known Issues (Claude Code native)

| Issue | Impact |
|-------|--------|
| #32292 | Multi-tab coordination not enforced - two sessions can edit the same file |
| #19364 | Session lock files requested (upvoted) - no native file locking |
| #25609 | OAuth race condition on concurrent session start |
| #14124 | SQLite contention with many parallel sessions |

These issues inform why external coordination layers are needed even with Agent Teams available.

## Hidden Swarm Mode

Feature-flagged in Claude Code binary (discovered by PaddoDev). Not yet in stable release. Suggests native multi-agent coordination is on the roadmap beyond Agent Teams.

## Architecture Insight

From Addy Osmani's analysis:
> "Three focused agents consistently outperform one generalist agent working three times as long."

From DORA report (Mike Mason):
> "9% bug rate increase with 90% AI adoption" - coordination and review quality matter as much as generation speed.

From sdd.sh community analysis:
> Convergence on git worktrees + tmux/daemon pattern across the ecosystem - this is the de facto standard, not a niche choice.

## Gotchas

- **Worktrees share the `.git` directory but not the working tree.** Running `git fetch` in any worktree updates refs for all worktrees. Running `git checkout` in one worktree does NOT affect others. But `git stash` is per-worktree
- **SQLite WAL mode is required for concurrent multi-session reads.** Default SQLite journal mode uses exclusive write locks. WAL (Write-Ahead Logging) allows concurrent readers alongside a writer. Always open coordination databases with `PRAGMA journal_mode=WAL`
- **Advisory leases must have TTL enforcement.** Without TTL, a crashed agent's lease blocks others indefinitely. Implement a background cleanup or check TTL on every lease read: `if (Date.now() - lease.started) > lease.ttl * 1000: delete lease`
- **Pre-commit guards fire in the agent's worktree git context.** If the guard script uses relative paths, ensure they resolve from the worktree root, not the main repo root. Use `$(git rev-parse --show-toplevel)` to get the correct base path

## See Also

- [[multi-agent-systems]]
- [[multi-agent-messaging]]
- [[agent-orchestration]]
- [[claude-code-ecosystem]]
- [[session-persistence]]
