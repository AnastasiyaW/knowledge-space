---
title: Odysseus
category: projects
date: 2026-06-01
tags: [odysseus, project]
aliases: ["Odysseus"]
---

# Odysseus

**Development line:** `project:odysseus` · thread `odysseus`  
**Last event:** 2026-06-01 · 1 dated since 2026-06-01 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Odysseus is a self-hosted workspace for users wanting a ChatGPT- or Claude-style interface with local or API-backed models.

- Chat and agents: runs tools, MCP, files, shell, skills, and memory.
- Research and documents: handles deep research, model comparison, documents, email, notes, tasks, calendar, and a model-serving Cookbook.

## Development line

- **2026-06-01 — Odysseus GitHub repository linked.** On 2026-06-01, we recorded links to the GitHub repository pewdiepie-archdaemon/odysseus and its Git endpoint. The link gives a source location, but we have not verified the repository contents, release state, or functionality.

## What changed

- 2026-06-01 — The project sought contributors for cross-platform testing, documentation, security review, and Cookbook or local model reliability. A first-run credentials report on the same day exposed onboarding friction.
- 2026-07-12 — A `main` commit bumped the code version to 1.0.2.
- 2026-08-25 — A `main` commit prepared a 1.0.3 image hotfix.

## How to use this

As of 2026-06-01, we use the recorded Odysseus GitHub repository as a source reference, and verify its operational status separately.

1. Clone `https://github.com/odysseus-dev/odysseus.git`. Use `main` for curated code instead of default `dev`.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/README.md>
2. For Docker, copy `.env.example` to `.env`, run `docker compose up -d --build`, and wait for healthy containers.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md>
3. Open `http://localhost:7000`, retrieve the temporary admin password from `docker compose logs odysseus`, then change it in Settings.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md>
4. For native Windows instead of Docker, run `powershell -ExecutionPolicy Bypass -File .\launch-windows.ps1`. Configure Ollama at `http://localhost:11434/v1` for a local Windows model.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md>

## Best practices

- Use `main` for curated code. Choose `dev` only when you deliberately want newest changes.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/README.md>
- Keep authentication enabled and localhost bypass disabled for network-accessible deployments. Use HTTPS and a trusted proxy, VPN, or private-access layer beyond localhost.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/SECURITY.md>
- Keep model and support-service ports internal. Protect `.env`, data, logs, uploads, session files, databases, backups, and API credentials.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/SECURITY.md>
- Limit shell, filesystem, email, MCP, and model-serving access to trusted administrators. Agent shell and filesystem tools have no sandbox or egress filter.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/THREAT_MODEL.md>
- Smoke-test the exact Docker, native, WSL, GPU, and provider path before relying on it. Fresh-install coverage remains a high-priority roadmap item.
  — <https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/ROADMAP.md>

## Superseded by this

- 2026-07-12 — Version 1.0.2 supersedes v1.0 as the current `main` code version after the version-bump commit.
- 2026-08-25 — A commit preparing a 1.0.3 image hotfix supersedes 1.0.2 as the current `main` development target, but is not a formal GitHub Release.
- 2026-09-05 — `odysseus-dev/odysseus` supersedes `pewdiepie-archdaemon/odysseus` as the canonical clone namespace via redirect; the transfer date is unknown.

## Still unknown

- We have no recorded date or terms for the move from `pewdiepie-archdaemon` to `odysseus-dev`. The redirect establishes only the current canonical route.
- We have no reconstructable code snapshot for 2026-06-01, so current documentation and later commits cannot verify June capabilities.
- We found no formal GitHub Release and no project-published immutable stable version or tag.
- We found no first-party Simplified-Chinese documentation or reproducible Chinese-language operating evidence.
- We found no bundled foundation-model ID. Odysseus is an application layer that needs a configured local or API-backed model.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/pewdiepie-archdaemon/odysseus | GitHub - odysseus-dev/odysseus: Self-hosted AI workspace. | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/README.md | Odysseus README (dev branch) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/website/setup.md | Odysseus Setup Guide (dev branch) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/SECURITY.md | Odysseus Security Policy (dev branch) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/THREAT_MODEL.md | Odysseus Threat Model (dev branch) | 2026-09-05 |
| https://raw.githubusercontent.com/odysseus-dev/odysseus/dev/ROADMAP.md | Odysseus Roadmap (dev branch) | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/discussions/551 | Who can help? · Discussion #551 | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/issues/395 | what kind of credentials does it expect on first run · Issue #395 | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/commits/main/ | Commits · odysseus-dev/odysseus · main | 2026-09-05 |
| https://github.com/odysseus-dev/odysseus/releases | Releases · odysseus-dev/odysseus | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:odysseus`, thread `odysseus`, 1 dated events 2026-06-01 → 2026-06-01.
- **Practical note:** As of 2026-06-01, practitioners can use the recorded Odysseus GitHub repository as a source-location reference, while separately verifying its contents and operational status.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
