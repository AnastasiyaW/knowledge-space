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

- Flight, train, bus, suburban train, and hotel search
- Room details and customer review data
- Checkout handoff links

The server selects options and forwards to checkout; it does not process payments.
It supplies Tutu inventory for agentic travel search, but we verify final orders directly on Tutu.

## Development line

- **2026-06-18 — Tutu MCP public endpoint referenced.** On 2026-06-18, a Tutu MCP development update referenced the public MCP endpoint at mcp.tutu.ru/mcp. The message linked related public traces of project development.

## What changed

- 2026-06-18 — added recognition for branded trains, including Lastochka and double-decker rolling stock.
- 2026-06-22 — Tutu announced AI agent access to search and booking for flights, trains, buses, suburban trains, and hotels.
- 2026-08-19 — 2026-08-21 — hackathon held around the server: 71 teams participated, 42 submitted projects; this expanded frontend and agent scenarios without changing the confirmed endpoint contract.

## How to use this

From 2026-06-18, we treat https://mcp.tutu.ru/mcp as the public Tutu MCP endpoint to evaluate or integrate, while confirming its current protocol and access requirements.

1. Add `https://mcp.tutu.ru/mcp` as a remote Streamable HTTP MCP endpoint without authentication.
  — <https://mcp.tutu.ru/mcp>
2. In Claude Code, run `claude mcp add --transport http tutu https://mcp.tutu.ru/mcp`.
  — <https://mcp.tutu.ru/mcp>
3. Pass origin, destination, dates, budget, transport type, and constraints to the agent; compare routes using price and duration searches.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>
4. Verify final conditions and finish checkout via the Tutu link; third-party apps must not accept payment instead of Tutu.
  — <https://github.com/chemisttt/tutu-mcp-kit>

## Best practices

- Do not call the endpoint directly in a browser as an API: use a same-origin proxy, or CORS blocks the request.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>
- Do not substitute mock offers when live MCP returns empty; show no results or diagnose the failure.
  — <https://github.com/chemisttt/tutu-mcp-kit>
- Query transport and hotels separately for combined trips, deduplicate results, and create checkout links only from the received `checkout_ref`.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>

## Superseded by this

- 2026-07-16 — passenger cart registration with a single-use checkout link replaced the older flow that stopped at data entry; the date comes from a secondary message and needs primary confirmation.

## Still unknown

- The response schema lacks `event_findings` and `new_events` fields; development details sit in `what_changed` without unsupported fields.
- A secondary source confirms branded train recognition for the 2026-06-18 event, but lacks its own publication date, so it is not listed as a dated event finding.
- No primary dated Tutu source was found for release statuses on 2026-06-23, 2026-07-01, 2026-07-08, 2026-07-09, and 2026-07-16; we cannot treat them as confirmed product chronology.

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