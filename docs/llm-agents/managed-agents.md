---
title: "Claude Managed Agents"
description: "Anthropic's hosted agent infrastructure - container sandboxes, tool orchestration, event streaming, outcomes evaluation. Open beta April 2026."
---

# Claude Managed Agents

Hosted agent platform from Anthropic. You define agent config (model, prompt, tools), Anthropic runs it in managed cloud containers with built-in code execution, web access, file I/O, and event streaming. No Docker, no orchestration code, no tool execution layer.

Key difference from Messages API: Messages API gives direct model access (you build everything). Managed Agents gives a complete agent platform (containers, tools, persistence, fault recovery included).

## Four Core Concepts

| Concept | What it is | Lifecycle |
|---------|-----------|-----------|
| **Agent** | Versioned config: model + system prompt + tools + MCP servers | Create once, reference by ID |
| **Environment** | Container template: OS packages, network rules, language runtimes | Reusable across sessions |
| **Session** | Running agent instance inside an environment | Holds conversation history, filesystem, status |
| **Events** | SSE stream between your app and the agent | User messages in, agent responses + tool calls out |

## Quick Start

```bash
# Install CLI
brew install anthropics/tap/ant          # macOS
# or curl from GitHub releases for Linux

# Install SDK
pip install anthropic                    # Python
npm install @anthropic-ai/sdk           # TypeScript

export ANTHROPIC_API_KEY="your-key"
```

### Create Agent + Environment + Session

```python
from anthropic import Anthropic

client = Anthropic()

# 1. Agent config
agent = client.beta.agents.create(
    name="Coding Assistant",
    model="claude-sonnet-4-6",
    system="You are a helpful coding assistant. Write clean, well-documented code.",
    tools=[{"type": "agent_toolset_20260401"}],
)

# 2. Container template
environment = client.beta.environments.create(
    name="dev-env",
    config={
        "type": "cloud",
        "networking": {"type": "unrestricted"},
        "packages": {"pip": ["pandas", "numpy"]},  # optional
    },
)

# 3. Start session
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="My first session",
)

# 4. Send task and stream results
with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[{
            "type": "user.message",
            "content": [{"type": "text", "text": "Create a Fibonacci script"}],
        }],
    )
    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    print(block.text, end="")
            case "agent.tool_use":
                print(f"\n[Tool: {event.name}]")
            case "session.status_idle":
                print("\n\nDone.")
                break
```

## Built-in Tools

`agent_toolset_20260401` includes all tools:

| Tool | Description |
|------|-------------|
| `bash` | Shell commands in container |
| `read` | Read files |
| `write` | Write files |
| `edit` | String replacement in files |
| `glob` | File pattern matching |
| `grep` | Regex search |
| `web_fetch` | Download URL content |
| `web_search` | Internet search |

### Selective Tool Configuration

```python
# Disable specific tools
{"type": "agent_toolset_20260401",
 "configs": [
     {"name": "web_fetch", "enabled": False},
     {"name": "web_search", "enabled": False}]}

# Enable only specific tools (everything else disabled)
{"type": "agent_toolset_20260401",
 "default_config": {"enabled": False},
 "configs": [
     {"name": "bash", "enabled": True},
     {"name": "read", "enabled": True}]}
```

### Custom Tools

```python
agent = client.beta.agents.create(
    tools=[
        {"type": "agent_toolset_20260401"},
        {
            "type": "custom",
            "name": "get_weather",
            "description": "Get current weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"],
            },
        }],
)
```

Custom tool best practices: 3-4 sentence descriptions (what, when, limitations). Group related operations under one tool with `action` parameter. Use namespace prefixes (`db_query`, `storage_read`). Return only essential data.

## Permission System

Two modes, combinable per-tool:

| Mode | Behavior | Use case |
|------|----------|----------|
| `always_allow` | Auto-execute | Trusted internal agents |
| `always_ask` | Pause for approval | User-facing agents |

MCP tools default to `always_ask`. This is more production-ready than LangGraph/CrewAI/AutoGen - none offer per-tool permissions out of the box.

## Usage Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Event-triggered** | External system fires agent | Sentry: bug detected -> agent writes patch -> opens PR |
| **Scheduled** | Cron-style | Daily GitHub digest, team task summary |
| **Fire-and-forget** | Human submits task, gets result | Asana AI Teammates |
| **Long-horizon** | Hours of work, persistent state | Research projects, large codebase migrations |

**CLI + SDK pattern**: agent templates as YAML in git (model, prompt, tools, MCP). CLI deploys via CI pipeline. SDK manages sessions at runtime.

## Outcomes (Research Preview)

Turns sessions from conversations into goal-oriented work. Define what "done" looks like with a rubric. A separate grader process evaluates quality independently.

```python
client.beta.sessions.events.send(
    session_id=session.id,
    events=[{
        "type": "user.define_outcome",
        "description": "Build a DCF model for Costco in .xlsx",
        "rubric": {"type": "text", "content": RUBRIC_TEXT},
        "max_iterations": 5,  # default 3, max 20
    }],
)
```

Rubric tips: concrete, verifiable criteria ("CSV contains price column with numeric values"), not vague ("data looks good").

| Result | What happens |
|--------|-------------|
| `satisfied` | Session goes idle |
| `needs_revision` | Agent starts new iteration |
| `max_iterations_reached` | Final attempt, then idle |
| `failed` | Rubric doesn't match task |

Retrieve output files via Files API from `/mnt/session/outputs/`.

## Multi-Agent (Research Preview)

One orchestrator delegates to sub-agents. Each runs in its own thread with isolated context, but all share the container filesystem.

```python
orchestrator = client.beta.agents.create(
    name="Engineering Lead",
    model="claude-sonnet-4-6",
    system="Coordinate engineering work. Delegate code review to reviewer, tests to test agent.",
    tools=[{"type": "agent_toolset_20260401"}],
    callable_agents=[
        {"type": "agent", "id": reviewer.id, "version": reviewer.version},
        {"type": "agent", "id": test_writer.id, "version": test_writer.version}],
)
```

**Limitation**: single delegation level only. Orchestrator calls agents, agents cannot call other agents.

Stream sub-agent threads independently:

```python
for thread in client.beta.sessions.threads.list(session.id):
    print(f"[{thread.agent_name}] {thread.status}")
```

## Architecture

Three independent components with minimal assumptions about each other:

- **Brain** - Claude + agent loop (tool selection, reasoning)
- **Hands** - sandboxes and tools (execution)
- **Session** - event journal (persistence)

Each can fail or be replaced independently. Built-in: prompt caching, context compaction, automatic infrastructure recovery.

## Pricing

Standard Claude API token rates + **$0.08/hour** active session time. A 10-minute coding session costs a few cents for compute.

| Operation | Rate Limit |
|-----------|-----------|
| Create (agents, sessions, environments) | 60 req/min |
| Read (get, list, stream) | 600 req/min |

## Gotchas

- **Outcomes grader runs in separate context** - it cannot see the agent's reasoning, only the output. This is by design (prevents self-evaluation bias) but means your rubric must be evaluable from artifacts alone, not from the conversation
- **Single delegation level** - orchestrator -> agents, but agents cannot call sub-agents. Design flat hierarchies. For deeper nesting, use sequential sessions where one agent's output feeds another's input
- **Container state is per-session** - files created in one session don't carry to another unless you explicitly download and re-upload. Use the Files API for persistence across sessions
- **`always_ask` pauses the entire session** - if your app doesn't handle the approval event promptly, the agent sits idle burning session time. Implement approval webhooks or polling with timeouts

## See Also

- [[agent-orchestration]] - orchestration patterns and frameworks
- [[agent-deployment]] - deployment strategies for AI agents
- [[claude-code-ecosystem]] - Claude Code plugin/hooks/skills system
- [[multi-agent-systems]] - multi-agent coordination architectures
- [[tool-use-patterns]] - tool design best practices
