---
title: "Yandex 360: yandex-360-mcp-server — Yandex 360 Mcp Server"
category: "projects"
date: 2026-11-20
tags: ["project", "yandex-360", "yandex-360-mcp-server"]
aliases: ["Yandex 360: yandex-360-mcp-server"]
---

# Yandex 360: yandex-360-mcp-server — Yandex 360 Mcp Server

Yandex 360 MCP server lets AI agents use Yandex 360 mail, calendar and disk; a counterpart to Google Workspace and Microsoft 365 connectors.

**Development line:** project:yandex-360 · thread yandex-360-mcp-server  
**Last event:** 2026-11-20 · 1 dated since 2026-11-20 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Yandex 360 MCP server is a middleware server. It gives external AI agents and LLM clients access to the Yandex 360 virtual office through the Model Context Protocol. It competes with the Google Workspace and Microsoft 365 API connectors.

Abilities:

- Mail, Calendar, Disk and corporate user directory operations as callable MCP tools
- Connection of external LLM clients, including Claude, ChatGPT and DeepSeek, to Yandex 360 enterprise data
- Integration with Yandex Alice AI for business and Yandex AI Studio agent workflows

Limit: the permissions of the underlying OAuth token and the Organization ID set which tools can run and which organization data is reachable.

It is a standard gateway for enterprise automation. It replaces bespoke API wrappers with the open Model Context Protocol.

## Development line

- **2026-11-20 — Yandex 360 opens its services to external AI agents via MCP server.** Yandex 360 launched an MCP server that lets AI agents reach the data and tools of its virtual office. Developers can connect Yandex 360 services to their own systems. Users can work with it through external AI interfaces such as ChatGPT, Claude and DeepSeek, as well as Yandex's Alice AI for business and agents built on Yandex AI Studio.
  - Yandex 360 launched an official MCP (Model Context Protocol) server interface. External LLM agents and clients can use it to operate virtual office tools directly: ChatGPT, Claude, DeepSeek, Alice AI for business and Yandex AI Studio. The tools cover corporate mail, calendar, cloud disk and directory management. (2026-11-20) — <https://habr.com/ru/articles/1110214/>

## What changed

Yandex 360 had closed proprietary interfaces. It now has a dedicated Model Context Protocol server, so the platform is open at the protocol level. Development moves from writing custom REST wrappers to standard client-side configuration across the corporate office services.

## How to use this

1. Get the OAuth authorization token and the Organization ID from the Yandex 360 administrative settings.
  — <https://habr.com/ru/articles/1110214/>
2. Configure the target MCP client with the Yandex 360 MCP server endpoint and the required authentication headers.
  — <https://habr.com/ru/articles/1110214/>
3. Ask the AI assistant to check calendar schedules, search emails, inspect files on Yandex Disk or manage the organization structure.
  — <https://habr.com/ru/articles/1110214/>

## Best practices

- Limit the OAuth token to the Yandex 360 services the agent needs, such as Mail, Calendar or Disk, so external agents keep least-privilege access.
  — <https://habr.com/ru/articles/1110214/>
- Check the organization ID and the domain administrative rights before giving teams access to the MCP server.
  — <https://habr.com/ru/articles/1110214/>

## Superseded by this

- Connecting external AI agents to Yandex 360 virtual office services used to need custom proprietary REST API integrations or manual data retrieval. Standard Model Context Protocol tool execution replaces that.
  — <https://habr.com/ru/articles/1110214/>

## Still unknown

- The exact public GitHub source repository and the official developer documentation have no direct deep URLs here. Search snippets only exposed opaque redirect URLs, so only the first-party Habr announcement is cited directly.
- Simplified Chinese developer channels and forums show no dedicated native documentation or discussions for Yandex 360 MCP server. That is a gap in Chinese.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/articles/1110214/ | Яндекс 360 открыл свои сервисы для внешних ИИ-агентов через MCP-сервер | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** project:yandex-360, thread yandex-360-mcp-server, 1 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** medium. The dated supersedes above say what is obsolete.
