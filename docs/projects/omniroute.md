---
title: OmniRoute
category: projects
date: 2026-07-25
tags: [omniroute, project]
aliases: ["OmniRoute"]
---

# OmniRoute

**Development line:** `project:omniroute` · thread `omniroute`  
**Last event:** 2026-07-25 · 1 dated since 2026-07-25 · **Researched:** 2026-09-05 · confidence: high

## What it is

OmniRoute is an MIT-licensed gateway connecting Claude Code, Codex, Cursor, Cline and other clients to model providers through one endpoint.

- Providers and models: route traffic to upstream targets.
- Fallback and combo routing: handle failover across multiple endpoints.
- Quotas: track usage limits.
- MCP/A2A: connect tool and agent protocols.
- Desktop/PWA: run local and web interfaces.

The README lists 352 providers and 1 312 chat-model IDs for line v3.8.50. It fits self-hosted deployment and manages multiple API sources. Check free quota data before sizing traffic.

## Development line

- **2026-07-25 — OmniRoute GitHub repository reference.** Support for Gemini 3.6 flash-high, flash-medium and flash-low was added through the Antigravity CLI provider, but waited for release v3.8.49. The maintainer confirmed this on 2026-07-26.

## What changed

2026-07-25 — published v3.8.48 lagged behind development: support for Gemini 3.6 flash-high, flash-medium and flash-low was added through the Antigravity CLI provider, but waited for release v3.8.49; the maintainer confirmed this on 2026-07-26. 2026-08-06 — the roadmap committed the transition from line v3.8.x to v3.9.0 LTS and modular v4: v3 remains the stable line, while new features move to v4.

## How to use this

From 2026-07-25, practitioners should use the linked OmniRoute GitHub repository as the starting point for source inspection, without inferring a supported feature set or release status until the repository is researched.

1. To develop from source, clone the repository, run npm install, npm run build and npm start; start the development server with npm run dev on port 20128.
  — <https://github.com/diegosouzapw/OmniRoute/discussions/8556>
2. Connect a compatible client to the OmniRoute endpoint and configure providers, models and fallback rules in the dashboard or project configuration.
  — <https://github.com/diegosouzapw/OmniRoute>

## Best practices

- Do not mistake a model in development for availability in a published release: Gemini 3.6 on 25 July required release/v3.8.49 or a build from source.
  — <https://github.com/diegosouzapw/OmniRoute/discussions/8556>
- For production, choose the stable v3/LTS line; use nightly and release builds only to test new features.
  — <https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.51/ROADMAP.md>

## Superseded by this

- 2026-07-25: assuming published v3.8.48 included Gemini 3.6 is obsolete; support existed only in upcoming release/v3.8.49.
- 2026-08-06: adding all new features to v3 is replaced by splitting into stable v3/LTS and modular v4.

## Still unknown

- The given schema lacks event_findings and new_events fields. Event detail for 2026-07-25 and subsequent event 2026-08-06 are saved in what_changed; the primary source for the first addition is dated 2026-07-26.
- The current stable published release is unconfirmed by these sources: the repository shows release/v3.8.51, but that does not prove a published release.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/diegosouzapw/OmniRoute | OmniRoute repository and README | 2026-09-05 |
| https://github.com/diegosouzapw/OmniRoute/discussions/8556 | New Release? — maintainer answer on Gemini 3.6 and release/v3.8.49 | 2026-09-05 |
| https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.51/ROADMAP.md | OmniRoute Roadmap | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:omniroute`, thread `omniroute`, 1 dated events 2026-07-25 → 2026-07-25.
- **Practical note:** From 2026-07-25, practitioners should use the linked OmniRoute GitHub repository as the starting point for source inspection, without inferring a supported feature set or release status until the repository is researched.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
