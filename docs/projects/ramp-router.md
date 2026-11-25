---
title: Ramp Router
category: projects
date: 2026-07-21
tags: [project, ramp-router]
aliases: ["Ramp Router"]
---

# Ramp Router

**Development line:** `project:ramp-router` · thread `ramp-router`  
**Last event:** 2026-07-21 · 1 dated since 2026-07-21 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Ramp Router is an OpenAI Responses-compatible LLM gateway for US developers and teams that want one integration across supported providers.

- Model listing: shows models available to an account key and creates buffered or streaming responses.
- Routing: directs calls through a chosen model, an ordered fallback list, or benchmark aliases.
- Telemetry: records provider, tokens, latency, cost, and fallback attempts.

## Development line

- **2026-07-21 — Ramp Router request-access milestone.** On 2026-07-21, Ramp linked the project to its product page and a separate request-access page. Those dated links indicate a public access step. We do not have the original announcement wording, capabilities, or availability terms.

## What changed

2026-07-21 — Ramp Router entered early access as a one-endpoint LLM router across multiple model providers. Users requested access through Ramp-hosted pages.

## How to use this

From 2026-07-21, treat Ramp Router as a project with a request-access route. Verify eligibility and availability through that route before planning use.

1. Confirm that the current Beta and US-only eligibility fits the team, then create a Router account and API key; a lifetime spend cap can be set on the key.
  — <https://docs.router.com/getting-started/quickstart>
2. Call GET /v1/models with the Router key and use a returned model ID rather than assuming a provider model name is available.
  — <https://docs.router.com/getting-started/quickstart>
3. Point an OpenAI Responses-compatible client at https://api.router.com/v1 and authenticate it with RAMP_ROUTER_API_KEY.
  — <https://docs.router.com/getting-started/connect>
4. Send POST /v1/responses with either one model or an ordered models fallback list; the two selectors are mutually exclusive.
  — <https://docs.router.com/getting-started/overview>
5. Inspect Router Logs after the request settles for model, provider, status, tokens, cost, and latency.
  — <https://docs.router.com/getting-started/quickstart>

## Best practices

- Read GET /v1/models at runtime; the catalog and key-specific callable IDs can change, so do not hardcode display labels or provider public names.
  — <https://docs.router.com/guides/choose-a-model>
- Verify that every candidate supports the request tools, input types, and output schema before adding a fallback; set the client deadline long enough for the entire fallback list.
  — <https://docs.router.com/guides/fallbacks>
- Bound startup and provider timeouts separately for streaming; fallback ends once the stream has started.
  — <https://docs.router.com/guides/fallbacks>
- Choose the account-wide content-recording setting before sending sensitive production traffic: recording is on by default, retains inputs, outputs, and tool calls for one year, and opt-out affects future recording after propagation.
  — <https://docs.router.com/resources/faq>

## Superseded by this

- 2026-08-19 — self-service public Router.com onboarding superseded the 2026-07-21 early-access and request-access framing; the product nevertheless remains Beta and US-only today.

## Still unknown

- We found no dated first-party launch post for 2026-07-21. Ramp’s 2026-07-28 post identifies that week as an early-access launch, but the former request-access page no longer exposes the original eligibility, model catalog, or API contract.
- Ramp’s current public status is internally mixed: Router.com says it is open to everyone, while Ramp’s support page still classifies it as Beta and US-only. We read this as public self-service for eligible US users, not unrestricted global availability.

## Sources

| source | title | read |
|---|---|---|
| https://ramp.com/router | Ramp Router: The LLM Gateway That Cuts Inference Costs | 2026-09-05 |
| https://ramp.com/router/request-access | Request access — Ramp Router | Ramp Router | 2026-09-05 |
| https://ramp.com/blog/technology-partner-program | Introducing Ramp’s Technology Partner Program | 2026-09-05 |
| https://ramp.com/blog/ai-token-spend-launch | See Your AI Spend, Understand It & Control It | 2026-09-05 |
| https://builders.ramp.com/post/thompson-sampling-model-routing | Online Learning for Cost-Efficient LLM Routing | 2026-09-05 |
| https://ramp.com/blog/router-launch | Introducing Router.com: The best model changes. Your application shouldn't. | 2026-09-05 |
| https://support.ramp.com/router-overview | Router overview | 2026-09-05 |
| https://docs.router.com/getting-started/overview | Overview · Docs · Ramp Router | 2026-09-05 |
| https://docs.router.com/getting-started/quickstart | Quickstart · Docs · Ramp Router | 2026-09-05 |
| https://docs.router.com/getting-started/connect | Connect your app · Docs · Ramp Router | 2026-09-05 |
| https://docs.router.com/guides/choose-a-model | Choose a model · Docs · Ramp Router | 2026-09-05 |
| https://docs.router.com/guides/fallbacks | Add fallbacks · Docs · Ramp Router | 2026-09-05 |
| https://docs.router.com/resources/faq | Frequently asked questions · Docs · Ramp Router | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ramp-router`, thread `ramp-router`, 1 dated events 2026-07-21 → 2026-07-21.
- **Practical note:** From 2026-07-21, treat Ramp Router as a project with a request-access route. Verify eligibility and availability through that route before planning use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.