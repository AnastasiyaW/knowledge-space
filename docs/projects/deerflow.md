---
title: DeerFlow 2.0 — Agent Platforms
category: projects
date: 2026-03-12
tags: [agent-platforms, agent_platforms, deerflow, project]
aliases: ["DeerFlow 2.0"]
---

# DeerFlow 2.0 — Agent Platforms

**Development line:** `project:deerflow` · thread `agent-platforms`  
**Last event:** 2026-03-12 · 1 dated since 2026-03-12 · **Researched:** 2026-09-07 · confidence: medium

## What it is

DeerFlow 2.0 — an open-source runtime for teams that need an agent harness rather than a research-only framework.

- Subagent delegation: plans and delegates work to subagents.
- Execution environment: combines memory, skills/tools, and a sandboxed filesystem.
- Model support: supports multiple model providers and self-hosted deployment.

The Gateway defaults to one worker. Multi-worker operation needs the documented shared persistence and event stack. Use it for a trusted, operator-managed Docker deployment, not as an internet-facing endpoint by default.

## Development line

- **2026-03-12 — DeerFlow 2.0 was surfaced through its official site, workspace, and repository.** On 2026-03-12, DeerFlow 2.0 connected its public product and source-code presence to its official website, workspace, and Bytedance GitHub repository. The linked resources establish a public product and source-code presence, without asserting a particular release, feature set, or availability change.

## What changed

2026-03-12 — no DeerFlow 2.0 release artifact is verified for this date. Community reports described tool errors that could abort agent flows. Other reports noted a custom Postgres checkpointer ignored by `make dev/start`. Neither report proves shipped behavior or a new version.

## How to use this

1. Clone the repository and run `make setup` to choose a model provider, optional search, and sandbox/Bash/file-write settings; this creates `config.yaml` and `.env`.
  — <https://github.com/bytedance/deer-flow>
2. Run `make doctor`, then use `make docker-init` and `make docker-start` for Docker development; the local application is served at `localhost:2026`.
  — <https://github.com/bytedance/deer-flow>
3. Use `make check`, `make install`, and `make dev` for local development; on Windows, run the local scripts through Git Bash rather than native PowerShell or cmd.
  — <https://github.com/bytedance/deer-flow>
4. Treat the public workspace as a demo: its observed demo state has no To-dos, so validate scheduling on a self-hosted instance instead.
  — <https://deerflow.tech/workspace/>

## Best practices

- Use Linux plus Docker for a persistent service; the documented starting server size is 8 vCPU, 16 GB RAM, and 40 GB free SSD.
  — <https://github.com/bytedance/deer-flow>
- Keep `GATEWAY_WORKERS=1` unless Postgres, the Redis stream bridge, run-ownership heartbeats, and database-backed run events are configured.
  — <https://github.com/bytedance/deer-flow>
- Keep the Gateway loopback-only initially. Before remote exposure, create an admin account and add an IP allowlist, reverse-proxy pre-authentication, and network isolation.
  — <https://github.com/bytedance/deer-flow>
- Use Docker/AIO, Kubernetes, or E2B when shell access needs an enforceable filesystem boundary; host Bash with the local sandbox is for fully trusted workflows only.
  — <https://github.com/bytedance/deer-flow>

## Superseded by this

- 2026-02-14 — Treating the active `main` line as the original DeerFlow 1.x framework is superseded for new work by the maintainer's instruction to use main with the new version. The legacy line remains separately maintained.
- 2026-06-25 — Immutable `v2.0.0` (`7e7f041`) supersedes RC selection status as the formal 2.0 release baseline. This does not retroactively certify the March 12 feature set.

## Still unknown

- The event has links but no public source text or frozen March snapshot, so no exact DeerFlow 2.0 commit, tag, or complete feature set can be attached to 2026-03-12.
- No dated first-party March source establishes the exact supported model list; current model recommendations are current guidance, not March evidence.
- `bytedance/deerflow` is the supplied subject key, while the official repository slug is `bytedance/deer-flow`.
- We ran no self-hosted instance during this research; current operating statements are documentation evidence only.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/bytedance/deer-flow | GitHub - bytedance/deer-flow | 2026-09-07 |
| https://deerflow.tech/ | DeerFlow | 2026-09-07 |
| https://deerflow.tech/workspace/ | DeerFlow workspace | 2026-09-07 |
| https://github.com/bytedance/deer-flow/issues/824 | Release Plan of DeerFlow 2.0 · Issue #824 | 2026-09-07 |
| https://github.com/bytedance/deer-flow/issues/1109 | Tool-call failure should degrade to error ToolMessage instead of aborting conversation · Issue #1109 | 2026-09-07 |
| https://github.com/bytedance/deer-flow/issues/1118 | checkpointer not working with "make start" command · Issue #1118 | 2026-09-07 |
| https://deerflow.tech/blog/posts | All Posts | 2026-09-07 |
| https://github.com/bytedance/deer-flow/releases/tag/v2.0.0 | DeerFlow 2.0.0 released | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:deerflow`, thread `agent-platforms`, 1 dated events 2026-03-12 → 2026-03-12.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium.
