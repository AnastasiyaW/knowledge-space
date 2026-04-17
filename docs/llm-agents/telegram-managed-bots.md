---
title: Telegram Managed Bots (Bot API 9.6)
category: reference
tags: [telegram, bot-api, managed-bots, per-user-isolation, ai-agents, deployment, bot-factory]
---

# Telegram Managed Bots (Bot API 9.6)

Per-user isolated bot instances deployed via a manager bot. Introduced in Bot API 9.6 (April 2026). Enables one-click deployment of personal AI agent instances to 900M+ MAU without app install or account registration.

**Docs:** core.telegram.org/bots/features#managed-bots  
**Changelog:** core.telegram.org/bots/api-changelog

## Architecture

### Deployment Flow

```
User clicks deep link:
  https://t.me/newbot/{manager_bot}/{suggested_username}?name={display_name}
      ↓
Telegram shows "Create bot?" confirmation dialog
      ↓
User confirms (one tap)
      ↓
Manager bot receives ManagedBotUpdated update
      ↓
Manager calls getManagedBotToken → gets access token
      ↓
Manager uses standard Bot API on behalf of new bot
  (sendMessage, setMyCommands, setWebhook, etc.)
```

### New API Objects (9.6)

**Methods:**
- `getManagedBotToken` — retrieve access token for a managed bot
- `replaceManagedBotToken` — rotate token (security/compromise recovery)
- `savePreparedKeyboardButton` — save buttons for Mini App flows

**Types:**
- `ManagedBotUpdated` — update when managed bot is created/modified; fields: `user` (creator), `bot` (new bot object)
- `KeyboardButtonRequestManagedBot` — keyboard button triggering managed bot creation
- `ManagedBotCreated` — system message confirming creation
- `PreparedKeyboardButton` — pre-saved keyboard button for Mini App

**User field:**
- `can_manage_bots` (bool) — whether a user has permission to create managed bots

### Enabling Manager Mode

```python
# 1. In @BotFather: Bot Management Mode → Enable
# 2. Implement update handler:
@bot.message_handler(content_types=['managed_bot'])
def handle_managed_bot(update):
    new_bot = update.managed_bot  # ManagedBotUpdated
    token = bot.get_managed_bot_token(new_bot.bot.id)
    # Initialize worker for this user with isolated state
    worker_registry.create(user_id=new_bot.user.id, token=token)

# 3. Share deep link to users
```

## Multi-Worker Architecture (OpenClaw Pattern)

One manager host running N isolated workers:

```text
Manager Gateway
  ├── Worker(user_1): token_A, memory_A, files_A, tools_A
  ├── Worker(user_2): token_B, memory_B, files_B, tools_B
  └── Worker(user_N): token_N, memory_N, files_N, tools_N
```

**Isolation guarantees:**
- Separate Telegram bot tokens per user
- Physical data separation (different state stores per worker)
- Per-bot rate limits (30 msg/sec per managed bot, not shared across users)
- Worker A cannot access Worker B's data even on shared host

**Manager routes messages** based on incoming bot token — each managed bot gets its own webhook or polling loop handled by the corresponding worker.

## Classic Bot vs. Managed Bot

| Dimension | Classic Bot (pre-9.6) | Managed Bot (9.6+) |
|-----------|----------------------|-------------------|
| Deployment | One bot, shared context for all users | Per-user isolated instance |
| Onboarding | Find bot → /start → configure | Click deep link → confirm (2 taps) |
| Data isolation | Logical (all users in one DB) | Physical (separate token, separate state) |
| Rate limits | Shared across all users | Per-bot (per-user) |
| Token management | Manual via @BotFather | Programmatic: getManagedBotToken, replaceManagedBotToken |
| Token rotation | Manual, takes service down | In-place via replaceManagedBotToken |

## Use Case Fit

**Ideal for managed bots:**
- Personal AI assistants (email, calendar, writing)
- Per-user business tools (sales assistant, personal CRM)
- Any "one user = one isolated data space" requirement
- SaaS products distributing to Telegram users without a separate app

**Not required (use classic bot) when:**
- Small shared team (2-10 users) with shared state
- Public bot with no per-user isolation needed
- Simple command/response bot without persistent state

## Token Security

```python
# Token rotation (e.g., when worker compromise suspected):
def rotate_token(managed_bot_id):
    new_token = manager_bot.replace_managed_bot_token(managed_bot_id)
    worker = worker_registry.get_by_bot_id(managed_bot_id)
    worker.update_token(new_token)
    # Old token immediately invalidated — no downtime
```

## Rate Limits and Constraints

- Per managed bot: 30 messages/second (same as any bot)
- 20 messages/minute to any single group
- Maximum managed bots per manager: not officially documented; likely tied to creator account limits at BotFather (historically 20 bots per account, managed bots may have separate quota)

## Gotchas

- **Manager ban = orphaned workers**: if the manager bot account is banned or deleted, behavior of existing managed bots is undefined (Telegram has not documented this edge case). Maintain a secondary manager or export tokens to cold storage periodically.
- **No native user revocation UI**: users cannot revoke a managed bot through standard Telegram UI. The manager must implement an explicit "delete my bot" command that calls token revocation and deletes the worker. Missing this creates GDPR right-to-erasure compliance gaps.
- **Zero-friction = zero quality filter**: the architecture makes it trivial for malicious managers to mass-deploy phishing/scam bots. The consent friction is on the user confirming creation, not on the manager bot's behavior quality. Verify manager source before deploying a managed bot to users.
- **can_manage_bots flag required**: the creating user must have `can_manage_bots = true` in their User object. This flag is not universally set — verify before presenting the deep link flow to ensure users can actually create the managed bot.

## See Also

- [[multi-agent-messaging]] - inter-agent communication patterns
- [[agent-deployment]] - deployment and infrastructure for agents
- [[tool-use-patterns]] - Bot API as tool integration surface
- [[production-patterns]] - scaling considerations for agent backends
