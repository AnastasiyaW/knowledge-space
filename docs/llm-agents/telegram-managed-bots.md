---
title: "Telegram Managed Bots"
description: "A production-safe guide to Telegram's manager-bot model: creation, token rotation, access settings, state isolation, and lifecycle receipts."
tags: [telegram, bot-api, managed-bots, security, deployment]
---

# Telegram Managed Bots

**Scope checked: 2026-09-04.** Telegram's Managed Bots let a manager bot create and operate a bot on behalf of its owner. The capability arrived in Bot API 9.6; the current API continues to document its creation flow, token methods, access settings, and update types. It is a Telegram control-plane feature, not a complete application-tenancy or data-isolation system. [Bot API changelog](https://core.telegram.org/bots/api-changelog) [Managed Bots guide](https://core.telegram.org/bots/features#managed-bots)

## What Telegram Provides

The manager is an ordinary bot with Bot Management Mode enabled in BotFather. A user follows a newbot deep link, confirms an editable suggested bot name and username, and Telegram sends the manager a **managed_bot** update. The update contains a **ManagedBotUpdated** object with the owner and the managed bot. The manager can then obtain its token through **getManagedBotToken**. [Managed Bots guide](https://core.telegram.org/bots/features#managed-bots) [Bot API objects](https://core.telegram.org/bots/api#managedbotupdated)

Telegram also documents:

- **replaceManagedBotToken**, which revokes the old token and returns a new token;
- **getManagedBotAccessSettings** and **setManagedBotAccessSettings**, which expose and change the bot's access policy;
- subsequent managed-bot updates when a managed bot's token or owner changes.

Those capabilities identify and control the Telegram bot. They do not partition your database, object storage, model provider account, analytics, or operator access. Design those boundaries explicitly.

## Production Topology

Use a manager/control plane and a separate tenant runtime:

```text
owner confirms bot creation
        |
manager bot receives managed_bot update
        |
control plane records owner, bot id, lifecycle version
        |
secret store retains the token; application reads it by bot id
        |
tenant runtime processes that bot's updates under an authenticated tenancy
```

The routing key should be a server-side bot record, not a user-supplied chat ID or prompt field. Bind every inbound update to the managed bot that received it, then resolve its owner and permitted resources outside the model.

## Register the Creation Event

Bot-library method names differ, so keep the lifecycle contract independent of a particular SDK:

```python
# Pseudocode: validate the webhook before parsing an update.
def register_managed_bot(update, telegram_api, registry):
    managed = update.get("managed_bot")
    if not managed:
        return

    owner_id = managed["user"]["id"]
    bot_id = managed["bot"]["id"]
    token = telegram_api.get_managed_bot_token(user_id=owner_id)

    registry.upsert(
        bot_id=bot_id,
        owner_id=owner_id,
        token_secret_ref=store_secret(token),
        lifecycle_event_id=update["update_id"],
    )
```

Persist the update identifier or another idempotency key before provisioning a worker. Telegram notes that update identifiers are useful for ignoring duplicates and restoring order; a webhook can also be retried by Telegram. [Update](https://core.telegram.org/bots/api#update) [Webhooks](https://core.telegram.org/bots/api#setwebhook)

Never return, log, commit, or place a managed-bot token in a task transcript. Treat token retrieval, replacement, and worker bootstrap as secret-handling operations.

## Receiving Updates Safely

For each managed bot, choose one delivery mode: long polling or a webhook. Telegram documents them as mutually exclusive. A webhook should use HTTPS and a unique secret token; Telegram sends the matching value in the X-Telegram-Bot-Api-Secret-Token header. [Getting updates](https://core.telegram.org/bots/api#getting-updates) [setWebhook](https://core.telegram.org/bots/api#setwebhook)

Before dispatching an update:

1. verify the transport and webhook secret;
2. resolve the managed bot record from the ingress endpoint or authenticated runtime;
3. deduplicate the update id and record the delivery receipt;
4. load only that bot's tenant policy, conversation state, tools, and secrets;
5. apply authorization and rate controls before calling any model or external service;
6. retain a redacted audit event with bot id, owner reference, action, and outcome.

Do not claim a static throughput limit for a managed-bot product. Limits and delivery behavior belong to Telegram's current Bot API and FAQ and can change; test the exact outbound pattern and observe API responses. [Bot API FAQ](https://core.telegram.org/bots/faq)

## Isolation Is an Application Contract

Use a managed bot when a separate Telegram identity and owner-scoped lifecycle are useful. Still enforce the application boundary:

| Layer | Required isolation |
|---|---|
| Telegram credentials | one secret reference per managed bot; rotation receipt |
| application state | tenant or bot key on every read and write |
| files and retrieval | namespaced storage plus authorization at retrieval time |
| tools | allowlist selected by authenticated owner policy |
| billing and quotas | metering keyed to the same server-side tenant record |
| operations | audit trail and incident rollback per bot |

Separate tokens alone do not prove that Worker A cannot retrieve Worker B's data.

## Lifecycle and Deletion

Treat a managed-bot update as an event that may create, rotate, or transfer ownership. Re-fetch and replace the secret only through the documented API; reconcile the new lifecycle state before resuming delivery. **replaceManagedBotToken** revokes the current token, but it does not delete your tenant records, files, or model history. [Token methods](https://core.telegram.org/bots/api#getmanagedbottoken)

An owner-requested deletion workflow should have its own receipt:

1. authenticate the owner through the current bot and application policy;
2. disable ingress and revoke or rotate the token as appropriate;
3. remove tenant access to data, jobs, and integrations;
4. execute the applicable retention/deletion policy for stored content;
5. record the completed action without retaining the token or message content.

Do not invent a Telegram feature for legal erasure, backup deletion, or cross-service revocation. Those remain your system's responsibilities.

## Gotchas

- **A creation update is processed twice.** Retries can provision duplicate workers. **Fix:** make registration idempotent on the update id and managed bot id.
- **A prompt chooses a bot or tenant.** That allows cross-tenant data selection. **Fix:** resolve the bot and owner from authenticated ingress, not model output.
- **A token appears in a diagnostic log.** It grants API access. **Fix:** redact secrets, store a reference, and rotate promptly if exposure is suspected.
- **A token was rotated but the old worker keeps serving.** Local configuration is now stale. **Fix:** stop old ingress, reload the new secret, and retain a successful health receipt.
- **An owner loses access.** Telegram control may change while application state remains. **Fix:** consume lifecycle updates and define a documented suspension/recovery policy.

## Sources

- [Telegram Bot API changelog](https://core.telegram.org/bots/api-changelog)
- [Telegram Managed Bots guide](https://core.telegram.org/bots/features#managed-bots)
- [Telegram Bot API: updates, webhooks, and managed-bot methods](https://core.telegram.org/bots/api)
- [Telegram Bot API FAQ](https://core.telegram.org/bots/faq)

## See Also

- [[multi-agent-messaging]]
- [[agent-deployment]]
- [[tool-use-patterns]]
- [[agentic-security-2026]]
