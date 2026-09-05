---
title: ZCode 3.0 — ZCode IDE
category: projects
date: 2026-06-15
tags: [project, zcode, zcode-ide, zcode_ide]
aliases: ["ZCode 3.0"]
---

# ZCode 3.0 — ZCode IDE

**Development line:** `project:zcode` · thread `zcode-ide`  
**Last event:** 2026-06-15 · 1 dated since 2026-06-15 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ZCode 3.0 is Z.ai’s desktop ADE. It works as a GUI harness for an agent rather than a terminal-only coding agent. The environment combines ZCode Agent, file and workspace references, terminal commands, execution permissions, Git state, Review, and remote control. Current downloads provide v3.11.2. Official documentation centers the product on GLM-5.3 and its stated 1M-token context. We use it for its integrated desktop workflow, not as a drop-in that recursively loads existing CLAUDE.md rules.

## Development line

- **2026-06-15 — ZCode installation documentation appeared.** On 2026-06-15, Z.ai published English ZCode installation documentation. The official installation URL marks an onboarding milestone for the ZCode 3.0 line. Available evidence does not establish product release details, supported platforms, or whether the guide itself first appeared that day.

## What changed

- **2026-06-15** — The ZCode 3.0 installation link pointed to the desktop client. The related 2026-06-13 release switched to the in-house ZCode Agent tuned for GLM-5.2. It added grouped task workspaces, Zread project knowledge, a Git branch graph, monitoring, and attachment input.
- **2026-08-14** — ZCode v3.7.7 made GLM-5.3 available.
- **2026-08-20** — ZCode v3.8.1 added global and workspace agent-capability controls, plus workspace-level Hooks.
- **2026-08-26** — ZCode v3.9.2 added GLM-5.3 Flash and explicit computer-control permission prompts.
- **2026-09-04** — ZCode v3.11.2 added PDF/media previews in conversations and workspace-specific plugin installation.

## How to use this

From 2026-06-15, use the official English installation guide for setup. Available sources do not confirm supported environments or release capabilities.

1. Download the current build for macOS, Windows, or Linux and install it.
  — <https://zcode.z.ai/en/docs/install>
2. On first launch, choose the project directory as the workspace and send a small instruction to verify that the Agent responds.
  — <https://zcode.z.ai/en/docs/install>
3. Connect a Z.ai or BigModel account, or configure a compatible third-party/API-key provider.
  — <https://zcode.z.ai/en/docs/configuration>
4. Place durable team rules, validation commands, and high-risk-file guidance in the workspace-root AGENTS.md.
  — <https://zcode.z.ai/en/docs/agents>
5. State a concrete goal, attach relevant files with @, then select an execution mode appropriate to the task’s risk.
  — <https://zcode.z.ai/en/docs/agents>

## Best practices

- Use Plan mode or Ask before changes for critical files, shell commands, and broad changes. Reserve Full access for clear, lower-risk work.
  — <https://zcode.z.ai/en/docs/agents>
- Keep important project rules in the current workspace AGENTS.md. ZCode does not merge nested files or expand imports.
  — <https://zcode.z.ai/en/docs/agents>
- For a Coding Plan API key, use its coding-specific endpoint rather than the general API endpoint.
  — <https://zcode.z.ai/en/docs/configuration>
- Use commands for a simple reusable prompt. Use Skills when the workflow also needs scripts, templates, or examples.
  — <https://zcode.z.ai/en/docs/commands>
- Configure a required proxy inside ZCode. An empty proxy field connects directly and does not inherit HTTP_PROXY.
  — <https://zcode.z.ai/en/docs/install>

## Superseded by this

- 2026-08-14 — Default model selection no longer relies on GLM-5.2 from the ZCode 3.0 release. Release v3.7.7 made GLM-5.3 available, and current ZCode Agent documentation centers on the GLM-5.3 family.
- 2026-09-04 — Downloading ZCode 3.0 is obsolete for new setups. The current official download is v3.11.2.

## Still unknown

- We found no dated first-party ZCode 3.0 release note or immutable v3.0 installer hash in indexed official history. A dated secondary report supports the 2026-06-13 release detail instead of an archived primary release note.
- We have not independently benchmarked the reported 150% in-app quota advantage or claims of stronger task completion than third-party agents. We do not recommend them.
- Current plan quotas, provider availability, and desktop versions are mutable. We give no price or quota recommendation.

## Sources

| source | title | read |
|---|---|---|
| https://zcode.z.ai/en/docs/install | Install | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/docs/agents | ZCode Agent | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/docs/configuration | Connect Models | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/docs/commands | Command | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/changelog | ZCode Releases & Updates | GLM-5.3 Coding Agent | 2026-09-05 |
| https://zcode.z.ai/cn/docs/install | 安装 | ZCode Docs | 2026-09-05 |
| https://www.ithome.com/0/963/985.htm | 智谱 AI 编程工具 ZCode 3.0 版本发布：切换自研 ZCode Agent 内核，深度适配 GLM-5.2 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:zcode`, thread `zcode-ide`, 1 dated events 2026-06-15 → 2026-06-15.
- **Practical note:** From 2026-06-15, practitioners evaluating ZCode should use the official English installation guide as the setup entry point. Available sources do not confirm supported environments or release capabilities.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
