---
title: Grok Build
category: projects
date: 2026-07-16
tags: [grok-build, project]
aliases: ["Grok Build"]
---

# Grok Build

**Development line:** `project:grok-build` · thread `grok-build`  
**Last event:** 2026-07-16 · 1 dated since 2026-07-16 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Grok Build is a terminal AI coding agent for software work.

- Codebase editing: reads and edits project files.
- Shell execution: runs shell commands.
- Web search: searches the web for technical information.
- Task management: handles long tasks through a full-screen TUI, headless CLI, or ACP.

Documentation names grok-4.6 as the powering model and permits custom-model configuration.
The released binary is the practical entry point; the Apache-2.0 source is open for inspection and local builds, but xAI accepts no external contributions.

## Development line

- **2026-07-16 — Grok Build public repository reference.** On 2026-07-16, the Grok Build thread referenced xAI’s public Grok Build GitHub repository. This creates a dated public source reference for the project, though we have not researched the repository contents or the message’s exact context.

## What changed

- **2026-05-25** — Grok Build entered early beta as a terminal coding agent with plan review, hooks, skills, MCP support, subagents, headless mode, and ACP.
- **2026-06-11** — Grok Build added a built-in plugin marketplace with commit-pinned remote plugin installs.
- **2026-07-15** — Grok Build’s Rust CLI/TUI and agent runtime were published as open source, with local-first custom inference documented.
- **2026-07-16** — Grok Build v0.2.102 added per-session minimal/fullscreen flags, `/jump`, a timeline sidebar, remote permission configuration, and improved login/session behavior.
- **2026-07-23** — Grok Build added generated, reusable workflows for background multi-agent orchestration.
- **2026-08-19** — Grok Build expanded a separate web/mobile app-building surface to every plan, with publishing, sharing, GitHub export, secrets, and connectors.

## How to use this

From 2026-07-16, treat the linked xAI GitHub repository as the starting public reference for Grok Build. Verify its contents before relying on any implementation details.

1. Install the released binary for your platform, then run `grok --version`.
  — <https://github.com/xai-org/grok-build>
2. Enter the target repository and run `grok`. Authenticate in the browser or supply an API key in a non-browser environment.
  — <https://docs.x.ai/build/overview>
3. Start complex work in Plan mode. Review or edit the plan, approve execution, and inspect the resulting diffs.
  — <https://x.ai/news/grok-build-cli>
4. Automate a bounded prompt with `grok -p`. Use streaming JSON when another program consumes the result.
  — <https://docs.x.ai/build/overview>
5. Configure model, project permissions, plugins, and MCP sources deliberately. Run `grok inspect` to verify the configuration actually loaded.
  — <https://docs.x.ai/build/settings>

## Best practices

- Keep Ask as the initial permission mode and use Plan mode for reviewable changes. Do not confuse Auto or Always-approve with a replacement for plan review.
  — <https://docs.x.ai/build/features/permissions>
- Run untrusted repositories with a strict sandbox and narrow permission rules. Add explicit denies for `.env`, private keys, and other credential paths because built-in profiles do not permanently protect them.
  — <https://docs.x.ai/build/features/sandbox>
- Use `grok inspect` after changing configuration so active instruction, skill, plugin, hook, MCP, and model sources stay visible.
  — <https://docs.x.ai/build/settings>
- Treat third-party plugins as executable code and install only sources you have reviewed. Marketplace pinning verifies a selected revision, but it does not make third-party code endorsed or safe.
  — <https://github.com/xai-org/plugin-marketplace>

## Superseded by this

- 2026-07-15 — Guidance that the Grok Build harness was unavailable for source inspection or local compilation is obsolete; xAI published the CLI/TUI and agent-runtime source.
- 2026-08-19 — The Early Beta access restriction for the web/mobile app-building surface is obsolete; xAI states that surface is available on every plan. This does not establish identical access terms for the terminal CLI.

## Still unknown

- The requested event_findings and new_events fields are not available in the supplied response schema. The dated event’s additions are represented in what_changed: the July 15 open-source announcement and the July 16 v0.2.102 changelog entry.
- Grok Build names two connected but operationally different surfaces: the GitHub repository covers the terminal coding agent, while the August announcement describes a web/mobile app builder that can export projects to GitHub and continue in the terminal. xAI does not document their exact shared implementation lineage.
- The August announcement describes the web/mobile Early Beta as limited to SuperGrok Heavy, whereas the May terminal-CLI launch described early-beta access for SuperGrok and X Premium Plus. We should not treat the access policies as one historical entitlement.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/xai-org/grok-build | xai-org/grok-build | 2026-09-05 |
| https://x.ai/news/grok-build-cli | Introducing Grok Build | 2026-09-05 |
| https://x.ai/news/grok-plugin-marketplace | Grok Build Plugin Marketplace | 2026-09-05 |
| https://x.ai/news/grok-build-open-source | Grok Build is Now Open Source | 2026-09-05 |
| https://x.ai/build/changelog | Grok Build Changelog | 2026-09-05 |
| https://x.ai/news/workflows | Workflows in Grok Build | 2026-09-05 |
| https://x.ai/news/grok-build-for-everyone | Grok Build on web and mobile | 2026-09-05 |
| https://docs.x.ai/build/overview | Grok Build: SpaceXAI's Coding Agent | 2026-09-05 |
| https://docs.x.ai/build/settings | Grok Build Settings | 2026-09-05 |
| https://docs.x.ai/build/features/permissions | Grok Build Permissions | 2026-09-05 |
| https://docs.x.ai/build/features/sandbox | Grok Build Sandbox | 2026-09-05 |
| https://github.com/xai-org/plugin-marketplace | xai-org/plugin-marketplace | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:grok-build`, thread `grok-build`, 1 dated events 2026-07-16 → 2026-07-16.
- **Practical note:** From 2026-07-16, practitioners should treat the linked xAI GitHub repository as the starting public reference for Grok Build and verify its contents before relying on any implementation details.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
