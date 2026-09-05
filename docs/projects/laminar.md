---
title: Laminar
category: projects

tags: [laminar, laminar-development, project]
aliases: ["Laminar"]
---

# Laminar

**Development line:** `project:laminar` · thread `laminar-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

Laminar is an OpenTelemetry-native platform for agent builders. It is an alternative to agent-focused tracing layers such as Langfuse or Helicone, not an LLM gateway.

Abilities:
- Traces: trace LLM and tool calls.
- Browser sessions: inspect browser interactions.
- Debugger: replay a failed run from a breakpoint.
- Evaluations: run evaluation datasets.
- Signals: detect recurring failures.
- SQL: query run data directly.

Self-hosting requires a multi-service stack. Signals requires a Google Generative AI API key.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-03-16 — Laminar announced a $3 million seed round and positioned its product around debugging and monitoring long-running agents: trace transcript views, browser-session replay, step-level debugger, Signals, SQL analysis, and evaluation datasets.
- 2026-03-18 — The reported funding was $3 million, led by Atlantic.vc with participation from Y Combinator, AAL.vc, Ben Sigelman, and Ant Wilson; the product scope was agent observability rather than a model release.
- 2026-07-09 — Release v0.2.1 added a refreshed Clusters UI, configurable frontend base path, API-key expiration metadata, CLI connection in onboarding, and Signals/alerting changes.

## How to use this

As of 2026-03-18, make no implementation or adoption change yet; first verify the linked Laminar announcement, repository state, and model reference.

1. Create a project and project API key, install the TypeScript SDK, and call Laminar.initialize at application startup before making model calls.
  — <https://github.com/lmnr-ai/lmnr>
2. Wrap agent entrypoints and meaningful application functions with observe so the trace contains the workflow rather than only a root span.
  — <https://github.com/lmnr-ai/lmnr>
3. For Python, install lmnr with only the instrumentations required by the application, initialize it once early in startup, and supply LMNR_PROJECT_API_KEY through the environment.
  — <https://github.com/lmnr-ai/lmnr-python>
4. Choose managed hosting for the shortest path, or self-host with Docker Compose; use the full Compose configuration for production workloads.
  — <https://github.com/lmnr-ai/lmnr>
5. Review traces and Signals, then use the built-in SQL editor to turn production observations into datasets and run evaluations against them.
  — <https://laminar.sh/blog/2026-03-16-laminar-launch>

## Best practices

- Initialize the SDK once and as early as possible, rather than repeatedly per request or tool call.
  — <https://github.com/lmnr-ai/lmnr-python>
- Preserve an existing OpenTelemetry span design and point its OTLP exporter to Laminar instead of duplicating instrumentation.
  — <https://github.com/lmnr-ai/lmnr/blob/main/frontend/assets/blog/2026-03-05-migrate-from-helicone-to-laminar.mdx>
- Use the lightweight Docker Compose stack only for quick starts or light usage; use managed hosting or docker-compose-full.yml for production workloads.
  — <https://github.com/lmnr-ai/lmnr>
- Do not treat Laminar as a replacement for gateway functions such as provider routing, response caching, or rate limiting.
  — <https://github.com/lmnr-ai/lmnr/blob/main/frontend/assets/blog/2026-03-05-migrate-from-helicone-to-laminar.mdx>

## Superseded by this

- 2026-03-16 — The initial launch description is incomplete for current deployment planning: release v0.2.1 added configurable frontend base paths and API-key expiration metadata.

## Still unknown

- The supplied Hugging Face short link could not be retrieved, so it was not used as evidence.
- The required event_findings and new_events fields are not present in the response schema supplied for this task; their supported facts sit in what_changed instead.

## Sources

| source | title | read |
|---|---|---|
| https://laminar.sh/ | Laminar — Open-source observability for AI agents | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr | lmnr-ai/lmnr — Laminar open-source observability platform | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr-python | lmnr-ai/lmnr-python — Laminar Python SDK | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr/releases | lmnr-ai/lmnr releases | 2026-09-05 |
| https://laminar.sh/blog/2026-03-16-laminar-launch | Laminar raised $3M to build observability for long-running agents | 2026-09-05 |
| https://startuprise.co.uk/laminar-raises-3m-seed-round-led-by-atlantic-vc-to-expand-ai-agent-observability/ | Laminar Raises $3M Seed Round Led by Atlantic.vc To Expand AI Agent Observability | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr/blob/main/frontend/assets/blog/2026-03-05-migrate-from-helicone-to-laminar.mdx | Migrate from Helicone to Laminar | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:laminar`, thread `laminar-development`, 0 dated events - → -.
- **Practical note:** As of 2026-03-18, make no implementation or adoption change yet; first verify the linked Laminar announcement, repository state, and model reference.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
