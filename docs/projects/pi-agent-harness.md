---
title: "Pi Agent Harness: pi-agent-harness-1-0-release — Pi Agent Harness 1 0 Release"
category: "projects"
date: 2026-10-04
tags: ["pi-agent-harness", "pi-agent-harness-1-0-release", "project"]
aliases: ["Pi Agent Harness: pi-agent-harness-1-0-release"]
---

# Pi Agent Harness: pi-agent-harness-1-0-release — Pi Agent Harness 1 0 Release

**Development line:** project:pi-agent-harness · thread pi-agent-harness-1-0-release  
**Last event:** 2026-10-04 · 1 dated since 2026-10-04 · **Researched:** 2026-11-28 · confidence: high

## What it is

Pi is a minimal, extensible agent harness from Earendil that users can make their own. It is used as a coding agent and as a base for building agentic applications. Earendil says hundreds of thousands of people use it every week. Pi and Pi Durable are both MIT licensed.

## Development line

- **2026-10-04 — Pi 1.0 agent harness release.** Pi 1.0 was announced as a minimal, flexible agent harness with MIT licensing and hundreds of thousands of weekly users. Listed changes include native MCP support via Codemode, extensions for virtual models, deferred tool loading, Anthropic cache warming, mid-dialogue system prompt changes, and a new TUI theme with full-screen default. The post also introduces Pi Durable, an experimental platform for long-running agent applications.
  - Earendil's announcement is dated 1 October 2026 and says Pi 1.0 shipped that day. It describes 1.0 as the result of months of hardening based on user issues and pull requests. Earendil says it adopts a feature only after it has proven itself, weighing its functionality against the complexity it adds, and that many candidate features were dropped. Pi Durable is described as a new substrate for long-running agentic applications. It comes from the aim of using Pi outside the coding agent and the terminal, reachable from different surfaces and supporting longer conversations and tasks. The announcement says Pi Durable shares Pi's principles of minimalism and supermalleability. It is shipped as an experimental package. Pi 1.0 is installed with a shell script, and Pi Durable with npm. (2026-10-01) — <https://earendil.com/posts/pi-1-0/>
  - The page gives demo examples. In the Codemode example, Pi writes a script that boils a week of commits down to a short summary. In the virtual-model example, Pi writes itself an extension, a router/auto model. Planning runs on Claude Opus, Jev detects the switch to implementation and hands over to GPT, and /session then breaks down cost per model and cache use. (2026-10-01) — <https://earendil.com/posts/pi-1-0/>

## What changed

Pi 1.0 adds Codemode \(native MCP support plus support for non-LLM models such as Jev and image models\), extension support for virtual models, deferred tool loading, cache warming for Anthropic models, mid-conversation system messages \(transcript-aware prompt and tool changes\), a new TUI theme, and full-screen mode by default. Earendil also released Pi Durable, an experimental package for long-running agentic applications that extends Pi's minimalism and malleability beyond the terminal and the coding agent.

## How to use this

1. Install Pi 1.0 on macOS or Linux with: curl -fsSL https://pi.dev/install.sh \| sh
  — <https://earendil.com/posts/pi-1-0/>
2. On Windows, install Pi 1.0 with: powershell -c "irm https://pi.dev/install.ps1 \| iex"
  — <https://earendil.com/posts/pi-1-0/>
3. To try Pi Durable, the experimental package, run: npm install @earendil-works/pi-durable @earendil-works/pi-ai @earendil-works/chord
  — <https://earendil.com/posts/pi-1-0/>
4. Read the documentation at pi.dev and browse the code at github.com/earendil-works/pi.
  — <https://earendil.com/posts/pi-1-0/>

## Best practices

- Run /session to see a per-model cost breakdown and cache use, especially when a virtual model routes work across several models.
  — <https://earendil.com/posts/pi-1-0/>
- Treat Pi Durable as experimental. Use Pi 1.0 itself for stable, general use, since Earendil describes 1.0 as hardened and dependable.
  — <https://earendil.com/posts/pi-1-0/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The linked announcement is dated 1 October 2026, while the reviewed event is dated 4 October 2026.
- The linked pages do not give technical details of Codemode, Jev, or Pi Durable. Earendil says they are covered in separate write-ups that were not among the linked pages.
- No independent reviews or community reactions were available among the linked pages.

## Sources

| source | title | read |
|---|---|---|
| https://earendil.com/posts/pi-1-0/ | Pi 1.0 \| Earendil | 2026-10-04 |

## Agent brief {#agent-brief}

- **Subject:** project:pi-agent-harness, thread pi-agent-harness-1-0-release, 1 dated events 2026-10-04 → 2026-10-04.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
