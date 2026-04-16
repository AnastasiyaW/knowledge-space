---
title: "Social Media MCP Tools"
description: "MCP servers for social media posting: Publora, Postiz, Ayrshare, community solutions. Comparison, pricing, integration setup."
---

# Social Media MCP Tools

MCP servers for posting to social platforms from AI agents (Claude Desktop, Cursor, Claude Code, etc.). Range from managed SaaS to self-hosted and single-platform community servers.

## Quick Decision Guide

| Need | Best option |
|------|-------------|
| Multi-platform, cheap, managed | Publora ($2.99/acc/mo) |
| Multi-platform, self-hosted, free | Postiz (Docker) |
| Enterprise, widest coverage (13+ platforms) | Ayrshare ($149+/mo) |
| X/Twitter only, fastest setup | OpenTweet ($11.99/mo) |
| Single platform, zero cost | Community MCP server |

## Managed SaaS Options

### Publora

Agent-first social media scheduler. Repositioned from B2C scheduling to AI-agent publishing (2025 acquisition by Sergey Bulaev).

**Supported platforms (11+):** LinkedIn, X/Twitter, Instagram (Reels/Stories/Carousel), Threads, Telegram, Facebook Pages, TikTok, YouTube, Mastodon, Bluesky, Pinterest

**Pricing:**

| Plan | Price | Posts/month | Notes |
|------|-------|-------------|-------|
| Starter (Free) | $0 | 15 | All except X/Twitter |
| Pro | $2.99/account/mo | 100/account | All 10+ platforms |
| Premium | $9.99/account/mo | 500/account | All 10+ platforms |

**Setup:**

```bash
# 1. Register + connect social accounts via OAuth at publora.com
# 2. Generate API key in dashboard
# 3. Configure MCP in Claude Desktop

# MCP endpoint
https://mcp.publora.com

# Skills install
npx skills add publora/skills
```

**Claude Desktop config (`claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "publora": {
      "command": "npx",
      "args": ["-y", "@publora/mcp"],
      "env": {
        "PUBLORA_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Skills repo:** `github.com/publora/skills` (MIT license, 9 skills covering all platforms)

**Skills structure:**

```text
skills/
  linkedin-post/      - posts with images, videos, documents
  threads-post/       - auto-threading support
  telegram-post/      - channel posting, markdown
  instagram-post/     - Reels, Stories, Carousels
  tiktok-post/        - videos with privacy controls
  bluesky-post/       - rich text + media
  x-post/             - X/Twitter with auto-threading
  social-post/        - unified: YouTube, Facebook, Mastodon
  linkedin-analytics/ - engagement metrics, follower data
```

### Ayrshare

Enterprise-grade. 13+ platforms, 75+ tools. REST API + MCP (community-maintained).

**Pricing:** $149-$599/mo + per-profile fees. For enterprise teams with budget.

**Platforms:** All Publora platforms + Reddit, Snapchat, more.

### OpenTweet

X/Twitter-only. 2-minute setup, MCP server included.

**Pricing:** $11.99/mo + free MCP tier.

Best for: X-heavy workflows where multi-platform is not needed.

## Self-Hosted: Postiz

Full open-source social media scheduling. Docker-based. Growing community (26K+ GitHub stars as of 2026).

**Platforms:** X, LinkedIn, Instagram, Facebook, Bluesky, Mastodon, Discord.

```bash
# Docker Compose setup
git clone https://github.com/gitroomhq/postiz-app
cd postiz-app
cp .env.example .env
# Configure OAuth credentials for each platform
docker-compose up -d
```

MCP integration: community-maintained, check repo for latest MCP adapter.

**When to choose:** privacy requirements, no monthly fees, team collaboration features.

## Community Single-Platform MCP Servers

Free, require own API keys, more technical setup.

| Platform | Available servers |
|----------|------------------|
| X/Twitter | 7+ (`sriramsowmithri`, `rafaljanicki`, `LuniaKunal`, others) |
| LinkedIn | 4 (`TuliEscobar`, `raghav18482`, `fredericbarthelet`, `AudienseCo`) |
| Instagram | 3 (`handoing`, `mosesblxk`, `taskmaster-ai`) |
| Bluesky | 4 (`LT-aitools`, `brianellin`, `morinokami`, `berenslab`) |
| TikTok | 1 (`Seym0n/tiktok-mcp`) |

**Discovery:** `github.com/TensorBlock/awesome-mcp-servers` - maintained list of community MCP servers by category.

## Platform Comparison

| Product | Platforms | Pricing | Open Source | MCP Quality |
|---------|-----------|---------|-------------|-------------|
| Publora | 11+ | Free / $2.99-$9.99/acc | Skills MIT | Official HTTP |
| Postiz | 7+ | Free (self-hosted) | Full | Community |
| Ayrshare | 13+ | $149-$599+/mo | No | Community |
| OpenTweet | X only | $11.99/mo + free tier | Partial | Official |
| Community servers | 1 each | Free | Yes | Varies |

## Workflow: Claude Code + Social Posting

```python
# Example: Claude Code agent posting research summary to LinkedIn
# Using Publora MCP
import anthropic

client = anthropic.Anthropic()

# Agent calls linkedin-post skill with structured content
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1000,
    tools=[{
        "name": "mcp__publora__linkedin-post",
        "description": "Post to LinkedIn",
    }],
    messages=[{
        "role": "user",
        "content": "Post this research summary to LinkedIn with appropriate hashtags: [summary]"
    }]
)
```

## Gotchas

- **X/Twitter excluded from Publora free tier.** The most demanded platform is gated - requires Pro plan ($2.99/mo) to post to X.
- **Publora doc-code mismatches.** The new owner found 269 discrepancies between documentation and actual API behavior (discovered via AI-agent testing across 7 review rounds). Test endpoints before building automation.
- **Community MCP servers require you to manage platform API credentials.** Platform APIs have rate limits and approval processes - Instagram Graph API, TikTok API require business accounts and app review.
- **Postiz OAuth setup is non-trivial.** Requires creating developer apps on each platform, managing redirect URIs, and keeping tokens refreshed. Budget 2-4 hours for initial setup.
- **LinkedIn API restricts organic posting.** LinkedIn's API only allows posting via approved LinkedIn Partner solutions for non-personal accounts. Personal account posting works; company page posting requires Partner status (Ayrshare has it, community servers may not).
- **MCP HTTP transport vs stdio.** Publora uses HTTP transport (`https://mcp.publora.com`). Some MCP clients only support stdio. Check client compatibility before committing.

## See Also

- [[ai-agent-ide-features]]
- [[agent-architectures]]
