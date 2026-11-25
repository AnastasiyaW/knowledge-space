---
title: Suno — Product development and industry relationships
category: organizations
date: 2025-11-28
tags: [organization, product-development-and-industry-relationships, suno]
aliases: ["Suno"]
---

# Suno — Product development and industry relationships

**Development line:** `organization:suno` · thread `product-development-and-industry-relationships`  
**Last event:** 2025-11-28 · 2 dated since 2025-06-27 · **Researched:** not yet · confidence: unresearched

## What it is

Suno is an AI music generator expanding into professional songwriting and music production. We have not run present-state research yet, so this page carries only the dated events and practical guidance.

## Development line

- **2025-06-27 — Suno acquired Wavtool to expand professional music-production capabilities.** On 2025-06-27, Suno acquired Wavtool to strengthen capabilities for professional songwriters and producers.
- **2025-11-28 — Warner Music Group settled with Suno and entered an AI-music agreement.** On 2025-11-28, Warner Music Group settled with Suno and entered a first-of-its-kind agreement with the AI music generator.

## How to use this

From 2025-06-27, evaluate Suno as a platform expanding toward professional songwriting and production workflows. From 2025-11-28, verify current rights and licensing terms before relying on Warner-linked music use cases.

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

We have not researched the present state against first-party sources. The Wavtool integration outcome and the full operational terms of the Warner agreement remain unverified.

## Sources

| source |
|---|
| https://www.musicbusinessworldwide.com/warner-music-group-settles-with-suno-strikes-first-of-its-kind-deal-with-ai-song-generator/ |
| https://www.prnewswire.com/news-releases/suno-acquires-wavtool-to-level-up-capabilities-for-professional-songwriters--producers-302491932.html |

## Agent brief {#agent-brief}

- **Subject:** `organization:suno`, thread `product-development-and-industry-relationships`, 2 dated events 2025-06-27 → 2025-11-28.
- **Practical note:** From 2025-06-27, evaluate Suno as a platform expanding toward professional songwriting and production workflows. From 2025-11-28, verify current rights and licensing terms before relying on Warner-linked music use cases.
- **Confidence:** unresearched. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:820b6c2b2aa379b2505f60a4008ba715af6a3f999d2270fec71d2c23982c1cac -->
## 2026-11-19 — Suno launches public Model Context Protocol server for AI assistants and IDEs

Suno launched an official Model Context Protocol server at api.suno.com/mcp. It generates tracks and creates Suno Visuals directly inside Claude, ChatGPT, Gemini, Claude Code and Cursor. Sign-in uses OAuth, and generation draws on existing account credits.

## 2026-11-19 — Suno releases MCP server connector with account library synchronization

Suno published client setup configurations for Claude, ChatGPT, Gemini and Cursor, all connecting to api.suno.com/mcp. Generated songs sync into the user's web library automatically. No API keys are needed.

### Usage and practices

- Configure the MCP client in Claude, ChatGPT, Gemini or Cursor with the remote server endpoint URL https://api.suno.com/mcp. [Source](https://suno.com/mcp)
- Finish the OAuth sign-in to link your Suno account and allow credit use. [Source](https://suno.com/mcp)
- Prompt the assistant with a style description, genre preferences or a lyric draft to get full tracks, extensions or video clips. [Source](https://suno.com/mcp)
- Log into the right Suno account before starting OAuth in the assistant, so it does not link the wrong profile. [Source](https://suno.com/mcp)
- Put explicit genre keywords, tempo and vocal preferences in the prompt, so credits are not spent on redundant generations. [Source](https://suno.com/mcp)

### Additional evidence

- 2026-11-19: Claude Code and Cursor are set up through HTTP transport at https://api.suno.com/mcp. Authentication is interactive OAuth inside the session. It uses active account credits and needs no developer API keys. [Source](https://suno.com/mcp)
- 2026-11-19: The integration supports track extensions from timestamps and Suno Visuals clip generation. All audio generated in chat syncs automatically into the user's web library. [Source](https://suno.com/mcp)

### Superseded guidance (retained for history)

- 2026-11-19: Before this, generating Suno audio tracks meant going to the web interface by hand or managing separate API keys. [Source](https://suno.com/mcp)

### Limits and open questions

- The entity display name 'Product development and industry relationships' looks like a generic topic label or metadata placeholder, not a product or company name. The underlying development events describe Suno's public MCP server launch.
- Credit pricing tiers per MCP tool call versus web dashboard generations could not be independently verified from public documentation.


<!-- Retained base: f8a0be5d0b18437f3ca9f9f4f5c270299fc0569a; article blob: d2ebe5e7f2bbb8a775eb3f8acbd0448770efa636 -->
