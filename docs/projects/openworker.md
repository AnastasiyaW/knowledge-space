---
title: OpenWorker — Project introduction
category: projects
date: 2026-08-05
tags: [openworker, project, project-introduction]
aliases: ["OpenWorker"]
---

# OpenWorker — Project introduction

**Development line:** `project:openworker` · thread `project-introduction`  
**Last event:** 2026-08-05 · 1 dated since 2026-08-05 · **Researched:** 2026-09-05 · confidence: high

## What it is

OpenWorker is an MIT-licensed desktop AI coworker with a local Python agent server and a Tauri/React GUI. It supports bring-your-own models and 25+ integrations.

- Documents and reports: generates them from files, Slack, and automations.
- Guardrails: requires approval for risky actions.

Status is open beta. The Windows build has no Authenticode signature.

## Development line

- **2026-08-05 — OpenWorker was publicly referenced through its GitHub repository.** On 2026-08-05, the recorded link pointed to the OpenWorker GitHub repository and Andrew Ng's biographical page. That establishes a dated public reference point for the project. The links alone do not confirm a release, feature set, or operational status.

## What changed

2026-08-05 — The recorded link pointed to a standalone OpenWorker repository. The primary source shows no release or announcement dated on that day.

2026-08-24 — v0.2.0 added skills, cross-session memory, three security coworkers, and reviewer-based auto-approve. It also improved MCP configuration and fixed approval and security bugs.

2026-08-25 — v0.2.1 added Ox Alpha through OpenRouter to the picker, with 1M tokens of context and tool calling.

## How to use this

Start from the OpenWorker GitHub repository as of 2026-08-05. Treat capabilities and release status as unverified until we inspect repository evidence.

1. Install the macOS or Windows build, open the application, and connect a provider API key or local Ollama.
  — <https://github.com/andrewyng/openworker>
2. Grant folder access only in the required mode and specify the desired result in plain language. Artifacts save to a temporary workspace by default.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>
3. Create an automation for recurring work. It runs while the application stays open, so enable launch on login for background execution.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>
4. Connect an MCP server through Manage → Integrations, then set approval controls for its tools.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>

## Best practices

- Start with a scoped folder, and approve shell commands and writes outside granted directories. Do not confuse a local-first setup with zero data transfer to the chosen model provider.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>
- Keep a human in the approval inbox for unattended automations so unattended runs do not approve their own side effects.
  — <https://github.com/andrewyng/openworker>
- Expect a SmartScreen warning on Windows because current builds are not code-signed.
  — <https://github.com/andrewyng/openworker>

## Superseded by this

- 2026-08-24 — OpenWorker is no longer just a generic desktop coworker: v0.2.0 added skills, project memory, security coworkers, and an auto-approve reviewer.
- 2026-08-25 — The original model list is outdated: v0.2.1 added Ox Alpha through OpenRouter with a claimed 1M tokens of context.

## Still unknown

- The response schema omits event_findings and new_events fields, so new dated facts sit in what_changed.
- No primary source published on 2026-08-05 was found that adds verifiable detail to the step itself.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/andrewyng/openworker | andrewyng/openworker — README | 2026-09-05 |
| https://github.com/andrewyng/openworker/releases/tag/v0.2.0 | OpenWorker v0.2.0 — GitHub Release | 2026-09-05 |
| https://github.com/andrewyng/openworker/releases | OpenWorker releases — GitHub | 2026-09-05 |
| https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md | OpenWorker quickstart — aisuite documentation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:openworker`, thread `project-introduction`, 1 dated events 2026-08-05 → 2026-08-05.
- **Practical note:** As of 2026-08-05, start from the OpenWorker GitHub repository. Treat its capabilities and release status as unverified until we review repository evidence.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
