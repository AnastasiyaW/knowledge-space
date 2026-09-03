---
title: "Social Media MCP Tools"
description: "A provider-neutral, approval-first design for using MCP to draft, validate, and publish social content without treating a social post as a reversible chat action."
tags: [mcp, social-media, publishing, approvals, oauth, agents]
---

# Social Media MCP Tools

**Scope checked: 2026-09-03.** A social-media MCP server is an integration boundary, not a publishing policy. Platform permissions, versioning, media rules, and commercial plans change frequently, so this page does not rank vendors or preserve static pricing. Instead, it defines a safe contract for connecting a news or project-content pipeline to a platform API.

## Treat Publication as an External Effect

A successful model response is not a published post. Separate the workflow:

```text
source evidence -> editorial draft -> policy validation -> human approval
                -> platform-specific publish -> provider receipt -> reconciliation
```

The agent may prepare a draft and a structured proposal. Only the effect service may use platform credentials or create the post, and it must retain the provider response that identifies the created resource.

## Minimal Publish Intent

Keep a platform-independent intent in the application, then translate it at the provider adapter:

```json
{
  "intent_id": "social-044",
  "project_ref": "happyin-space",
  "platform": "linkedin",
  "account_ref": "organization:public-channel",
  "content_revision": "draft:2026-09-03.2",
  "media_refs": ["asset:cover-044"],
  "schedule_at": null,
  "approval_ref": "approval:appr_01...",
  "idempotency_key": "social-044:linkedin:v1",
  "expires_at": "2026-09-03T18:00:00Z"
}
```

The executor derives the platform payload from this immutable intent and validates the current account, scope, media, audience, and time. It never accepts a free-form “post this everywhere” instruction as authority.

## MCP Tool Surface

Expose narrow verbs rather than one broad `social_admin` tool:

| Tool | Effect | Required checks |
|---|---|---|
| `list_connected_accounts` | read | caller and account scope |
| `create_draft` | reversible internal write | project, source references, content schema |
| `validate_publish` | read-only provider preflight | scope, media, format, current platform version |
| `publish_approved` | external effect | immutable approval, expiry, account, idempotency |
| `get_publication_receipt` | read | intent ID and caller scope |

Tool descriptions and annotations are untrusted unless they come from a server the host already trusts. Hosts should keep a human able to deny a tool invocation. [MCP tools](https://modelcontextprotocol.io/specification/latest/server/tools)

## Authorization Boundary

For remote MCP, use the protocol's authorization flow and validate tokens for the intended resource. The MCP server should keep platform OAuth credentials in a server-side vault; the MCP client receives only the result it needs, never a reusable platform access token. [MCP authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization)

For each connected account, record:

- platform account and owner reference;
- granted scopes and the date they were verified;
- current API version and content capabilities;
- media upload requirements and size limits;
- provider rate-limit and retry behavior;
- policy or review restrictions;
- credential rotation and revocation procedure.

The exact values are platform-specific and must be revalidated at connection time. For example, LinkedIn's Posts API currently requires versioned request headers and separate member/organization scopes; a successful creation returns a provider post identifier. [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)

## Approval and Idempotency

```text
draft -> reviewer approves exact content revision and account
      -> effect service reserves (intent_id, idempotency_key, content_revision)
      -> adapter creates one platform post
      -> record provider ID, response class, and final visibility
```

An identical retry returns the stored receipt. Reusing the idempotency key with a different account, revision, or media list must reject before a second post is created. If the network times out after the provider call, mark the state unknown and reconcile by the provider receipt or a safe lookup; do not publish again on assumption.

## Provider Qualification Gate

Evaluate a managed or self-hosted connector against current evidence, not a price table:

1. documented transport and OAuth flow;
2. explicit account, scope, and API-version model;
3. immutable request or idempotency support for publish;
4. media upload, post creation, and lookup receipts;
5. maintenance owner, release provenance, and dependency review;
6. a staging or test-account canary;
7. a human approval path that shows the actual outgoing content.

No community server should receive broad social credentials merely because its tool name sounds narrow.

## Operating Pattern for a News Portal

Use the portal's knowledge record as the source of truth:

| Portal state | Social action |
|---|---|
| Research collected | no social action |
| Drafted and source-reviewed | optional draft proposal |
| Approved for public release | create one platform-specific publish intent |
| Published and verified | attach provider receipt and canonical URL |
| Corrected or superseded | publish a new, linked revision; do not overwrite history silently |

This keeps news provenance, project pages, and social derivatives connected without letting social delivery redefine editorial truth.

## Gotchas

- **A scheduler receipt is not a publication receipt.** It may only mean the connector accepted the job. **Fix:** reconcile the provider resource ID and observed visibility.
- **MCP transport does not grant platform authority.** OAuth scopes and account roles still live at the platform boundary. **Fix:** validate them in the provider adapter for every effect.
- **Tool metadata can be malicious or stale.** A friendly description is not a security guarantee. **Fix:** trust the configured server identity and inspect schemas before enabling effectful tools.
- **Retries can duplicate a post.** Timeouts do not tell you whether the platform acted. **Fix:** atomically reserve an idempotency key and reconcile unknown outcomes.
- **Static vendor comparisons decay quickly.** Prices, platform coverage, and permissions are not stable documentation facts. **Fix:** keep a dated qualification receipt per connector.

## Sources

- [Model Context Protocol tools](https://modelcontextprotocol.io/specification/latest/server/tools)
- [Model Context Protocol authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization)
- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)

## See Also

- [[agent-safety-alignment]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[agent-orchestration]]
