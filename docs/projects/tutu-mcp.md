---
title: Tutu MCP
category: projects
date: 2026-06-18
tags: [project, tutu, tutu-mcp, tutu-mcp-development]
aliases: ["Tutu MCP"]
---

# Tutu MCP

**Development line:** `project:tutu-mcp` · thread `tutu-mcp-development`  
**Last event:** 2026-06-18 · 1 dated since 2026-06-18 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Tutu MCP is a Streamable HTTP MCP endpoint for Claude, Claude Code, ChatGPT, OpenCode, and compatible agents.

- Search for flights, trains, buses, suburban trains, and hotels.
- Room details and user reviews.
- Checkout link handoff.

The server selects options and transfers to checkout without accepting payments. Verify the final order on the Tutu page before payment.

## Development line

- **2026-06-18 — Tutu MCP public endpoint referenced.** On 2026-06-18, a Tutu MCP development update referenced the public MCP endpoint at mcp.tutu.ru/mcp.

## What changed

- 2026-06-18 — added recognition of branded trains, including Lastochka and double-decker cars.
- 2026-06-22 — Tutu announced AI agent access for searching and booking flights, trains, buses, suburban trains, and hotels.
- 2026-08-19 — 2026-08-21 — Tutu ran a hackathon around the server: 71 teams participated, 42 submitted projects. This expanded frontend and agent scenarios without changing the confirmed endpoint contract.

## How to use this

From 2026-06-18, practitioners should treat https://mcp.tutu.ru/mcp as the public Tutu MCP endpoint to evaluate or integrate, while confirming its protocol and access requirements.

1. Add the endpoint `https://mcp.tutu.ru/mcp` as a remote Streamable HTTP MCP without authentication.
  — <https://mcp.tutu.ru/mcp>
2. In Claude Code, run `claude mcp add --transport http tutu https://mcp.tutu.ru/mcp`.
  — <https://mcp.tutu.ru/mcp>
3. Pass origin and destination cities, dates, budget, transport type, and limits to the agent; compare routes by price and time.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>
4. Check final terms and complete booking on Tutu; third-party apps must not accept payment instead of Tutu.
  — <https://github.com/chemisttt/tutu-mcp-kit>

## Best practices

- Do not open the endpoint in a browser as an API: use a same-origin proxy for browser clients so CORS does not block requests.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>
- Do not substitute mock offers when live MCP returns empty results: show the empty state or diagnose the failure.
  — <https://github.com/chemisttt/tutu-mcp-kit>
- For split trips, query transport and hotels separately, deduplicate results, and build checkout links only from the returned `checkout_ref`.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>

## Superseded by this

- 2026-07-16 — passenger cart registration and one-time checkout links replaced the flow where the agent stopped at the data entry page. The date comes from a secondary message and needs primary confirmation.

## Still unknown

- The response schema lacks `event_findings` and `new_events` fields; development updates stay in `what_changed` without unsupported fields.
- A secondary source confirms branded train recognition for the 2026-06-18 update, but its publication date was unavailable.
- No primary dated Tutu source was found for release statuses on 2026-06-23, 2026-07-01, 2026-07-08, 2026-07-09, and 2026-07-16, so they remain unconfirmed product chronology.

## Sources

| source | title | read |
|---|---|---|
| https://mcp.tutu.ru/mcp | Tutu MCP — ИИ спланирует поездку за вас | 2026-09-05 |
| https://companies.rbc.ru/news/Q1Aa56ondv/servis-puteshestvij-tutu-otkryil-bronirovanie-poezdok-cherez-ii-agentov/ | Сервис путешествий Туту открыл бронирование поездок через ИИ-агентов | 2026-09-05 |
| https://hackathon2026.tutu.ru/ | ИИ-хакатон — Туту MCP | 2026-09-05 |
| https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md | tutu-mcp-kit: MCP operator guide | 2026-09-05 |
| https://github.com/chemisttt/tutu-mcp-kit | chemisttt/tutu-mcp-kit | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:tutu-mcp`, thread `tutu-mcp-development`, 1 dated events 2026-06-18 → 2026-06-18.
- **Practical note:** From 2026-06-18, practitioners should treat https://mcp.tutu.ru/mcp as the public Tutu MCP endpoint to evaluate or integrate, while independently confirming its current protocol and access requirements.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
