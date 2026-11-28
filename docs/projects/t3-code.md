---
title: "T3 Code: t3-code — T3 Code"
category: "projects"
date: 2026-11-27
tags: ["project", "t3-code"]
aliases: ["T3 Code: t3-code"]
---

# T3 Code: t3-code — T3 Code

**Development line:** project:t3-code · thread t3-code  
**Last event:** 2026-11-27 · 2 dated since 2026-11-27 · **Researched:** 2026-11-28 · confidence: medium

## What it is

T3 Code is an open-source control plane and graphical interface for developers who run terminal-first AI coding tools such as Claude Code, OpenAI Codex CLI, Cursor, Grok and Antigravity. Abilities:

- Local CLI link: connects to the agent CLIs already installed on the machine, using personal login and existing subscriptions, with no model reselling and no token markup.
- Git worktrees: puts each concurrent agent task in its own worktree, with side-by-side diff review, commit creation and direct GitHub pull request generation.
- Session sync: keeps agent sessions in step across desktop operating systems, the web interface, and iOS and Android apps, so steps can be approved remotely.
- Agent handoff: switches a task or hands it off between different coding agents within the same thread.

Limit: it needs locally installed agent CLI binaries and valid third-party credentials. It ships no built-in models and no managed execution sandbox. For anyone running several CLI coding agents at once across branches, it is a coordination layer that adds no second subscription fee.

## Development line

- **2026-11-27 — T3 Code Open-Source AI Agent IDE.** T3 Code is presented as an open-source IDE control panel for AI agents (including Claude Code, Codex, Cursor, Grok and Antigravity) that run on user subscriptions without token markups. It features branch-per-thread workflows, direct PR creation, mobile apps for iOS and Android, and over 81,000 GitHub stars.
- **2026-11-27 — Overview of T3 Code open-source IDE agent control hub and multi-platform support.** T3 Code is presented as an open-source IDE hub and control panel for running several coding agents at once across separate Git branches, on existing user subscriptions. It comes with iOS and Android mobile apps.
- **2026-11-27 — other reporting on this date.**
  - The project is made by Theo Browne (@theo / Ping Labs) as an open-source, MIT-licensed interface (a CLI-to-GUI bridge) under pingdotgg/t3code. It runs via npx t3@latest or system package managers, with no token resale. The 81,000 GitHub stars figure mixes in secondary metrics. Primary distribution works through Agent Client Protocol (ACP) compatibility and local authentication. (2026-11-27) — <https://github.com/pingdotgg/t3code>
  - Confirms the architecture: T3 Code is an orchestration control plane, not a standalone language model or cloud compute runtime. It isolates threads in Git worktrees, shows side-by-side diffs, generates GitHub pull requests, and pairs with iOS and Android apps for remote approval prompts. (2026-11-27) — <https://t3.codes/>

## What changed

The project moved from early concepts to an open-source graphical control plane. Its aim is to ease terminal congestion when several agents run at once. It now creates a Git worktree automatically for each task thread. It offers visual diff inspection and sends pull requests straight to GitHub. Desktop, web and mobile companion clients all give access for remote approvals. The design settled on running locally authenticated CLI binaries directly, across the major coding agent tools, under an MIT license.

## How to use this

1. Launch T3 Code with npx t3@latest, or install it through a package manager (brew install --cask t3-code on macOS, winget install T3Tools.T3Code on Windows).
  — <https://github.com/pingdotgg/t3code>
2. Check that the local CLI coding tools (Claude Code, Codex CLI, Cursor or Antigravity) are installed and logged in.
  — <https://github.com/pingdotgg/t3code>
3. Open a local Git repository and create agent task threads. Each one is assigned to its own Git worktree automatically.
  — <https://t3.codes/>
4. Inspect the generated diffs in the interface, apply the changes, and push pull requests directly to GitHub.
  — <https://t3.codes/>
5. Optionally pair the iOS or Android companion app to follow agent progress and approve steps remotely.
  — <https://t3.codes/>

## Best practices

- Keep each concurrent agent task in its own Git worktree, so working directories do not clash and uncommitted changes are not overwritten by accident.
  — <https://github.com/pingdotgg/t3code>
- Log in to the underlying CLI agent binaries in the local terminal before launching tasks from the GUI.
  — <https://github.com/pingdotgg/t3code>
- Read the code diffs in the desktop interface before granting remote execution approvals or sending pull requests.
  — <https://t3.codes/>

## Superseded by this

- Running several AI coding agents at once meant switching between terminal windows and handling separate Git branch checkouts by hand.
  — <https://t3.codes/>
- A visual management interface for coding agents meant buying extra API credits or paying token markups on top of the base model subscriptions.
  — <https://github.com/pingdotgg/t3code>

## Still unknown

- The exact canonical URLs of independent community threads (such as Reddit threads on telemetry and background credential storage) could not be retrieved directly without redirect intermediaries.
- Long-term mobile sync topology, and self-hosted server options beyond local pairing, remain unverified in public documentation.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/pingdotgg/t3code | GitHub - pingdotgg/t3code: Open-source AI agent control plane and GUI | 2026-11-28 |
| https://t3.codes/ | T3 Code - The Control Plane for Coding Agents | 2026-11-28 |

## Agent brief {#agent-brief}

- **Subject:** project:t3-code, thread t3-code, 2 dated events 2026-11-27 → 2026-11-27.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
