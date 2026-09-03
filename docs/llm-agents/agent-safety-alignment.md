---
title: "Agent Safety and Alignment"
description: "Build agent safety as explicit authority, data, tool, approval, and evidence boundaries rather than as a prompt-only promise."
tags: [llm-agents, safety, alignment, guardrails, prompt-injection, sandboxing, approvals]
---

# Agent Safety and Alignment (September 2026)

Version context: model behavior, tool protocols, sandbox products, moderation features, and provider policy controls change. This page describes a product-level safety architecture that must be evaluated against the exact model, tools, data classes, and deployment environment.

An agent can summarize, plan, call tools, write files, or request external effects. Alignment language in a system prompt may guide behavior, but it does not create authorization, isolate data, validate a payment, or prove an action's outcome. Safety comes from layered technical and operational controls.

## Start with a Threat Model

Identify what is trusted, what is untrusted, and which effects require a separate authority decision.

| Boundary | Examples | Required control |
|---|---|---|
| Trusted policy | application configuration, approved schemas, signed rules | versioning, access control, change review |
| Untrusted content | user input, web pages, email, retrieved documents, tool output | treat as data; never as authority |
| Model output | proposed answer, tool arguments, routing decision | schema, business validation, authorization |
| Credentials and identity | service account, tenant scope, user session | least privilege, expiry, audit |
| External effect | send, publish, deploy, purchase, delete | approval, idempotency, terminal receipt |

A threat model should name assets, actors, entry points, failure impact, control owner, and the proof needed to say the control worked.

## Prompt Injection Is a Data-Boundary Problem

Instructions embedded in a document, web page, tool result, or user message are untrusted content. Pattern-based text removal alone cannot make them safe: attackers can rephrase instructions, encode them, or exploit a tool flow rather than a phrase.

Build a safer path:

1. identify trusted instructions and untrusted input explicitly;
2. pass only the minimum data needed for the task;
3. restrict the model to a narrow, locally approved tool set;
4. validate every proposed tool call outside the model;
5. keep authorization, tenant scope, and external effects in deterministic code;
6. test adversarial content in the actual retrieval and tool pipeline.

OpenAI's current safety guidance recommends constraining inputs and outputs and using human review where appropriate. Those are risk-reduction measures, not a guarantee that arbitrary content is safe. [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)

## Grant Capabilities, Not Broad Intent

Use a short-lived, immutable capability or approval reference for an action. Store it server-side or sign it; do not let the executor edit its fields:

```json
{
  "capability_id": "cap_01...",
  "capability_profile": "effect-capability/v1",
  "issuer": "policy-service",
  "issuer_key_id": "policy-service-key-2026-01",
  "subject": "workflow:research-review",
  "audience": "editorial-effect-service",
  "presenter_principal": "workload:research-reviewer@prod",
  "presenter_key_thumbprint": "sha256:...",
  "identity_source": "approved-workload-identity",
  "task_id": "publish-research-044",
  "action": "create_draft",
  "arguments_digest": "sha256:...",
  "resource_scope": "project:happyin-space",
  "data_classification": "public",
  "approval_decision_ref": "approval:appr_01...",
  "idempotency_key": "publish-research-044:v1",
  "expires_at": "2026-09-03T16:00:00Z",
  "policy_revision": "editorial-policy@6",
  "integrity_proof": "server-record-or-signature"
}
```

The agent may request an action, but the enforcement point resolves or verifies the immutable record and checks the profile, issuer, issuer-bound key, subject, task, action arguments digest, scope, expiry, approval decision, and idempotency key before execution. A server record must come from an authorized store; a signed capability must verify against an allowlisted issuer and that issuer's configured key. Unknown issuers, wrong profiles, and invalid signatures fail closed.

The effect service is the recipient and identity-termination boundary. It accepts a presenter identity only from its configured workload-identity verifier, never from a forwarded caller header. It requires the live authenticated principal to equal `presenter_principal` and proof of possession of the credential matching `presenter_key_thumbprint`; it separately requires `audience` to equal that local service. Missing or unequal values reject the action, so a copied capability cannot be replayed by another principal. Certificate- and key-bound token patterns provide examples of this binding and recipient validation. [RFC 8705](https://www.rfc-editor.org/rfc/rfc8705) [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725)

Any changed argument or scope requires a newly issued capability. An agent cannot extend its own scope by saying that an urgent task requires more access.

## Put Irreversible Effects Behind a Gate

Use a proposal-to-effect flow:

```text
propose -> parse and validate -> authorize -> approve if required
       -> atomically reserve effect key -> execute -> reconcile -> terminal receipt
```

The terminal receipt must say whether the external effect occurred, not merely that the model produced a success message. A timeout or disconnected browser is an unknown state until the effect is reconciled.

Before an external effect, atomically reserve the tuple `capability_id`, `idempotency_key`, canonical `arguments_digest`, and `resource_scope`. An identical retry returns the original terminal receipt; an in-progress duplicate waits for or triggers reconciliation. Reusing a key with a changed capability, arguments digest, or scope is a collision and must be rejected before another effect can occur.

For high-impact actions, reviewers need the source evidence and the exact proposed effect before approval. Reviewing only a model summary is not meaningful oversight.

## Sandboxing Reduces One Class of Risk

An isolated workspace can limit file-system or process impact, but it does not automatically constrain network egress, credentials, data visibility, tool capabilities, or a downstream service's permissions.

Define separately:

- file-system scope and writable paths;
- process, package, and interpreter policy;
- network destinations and request budget;
- mounted secrets and identity;
- data classification permitted in the environment;
- artifact export path and retention;
- cancellation and cleanup evidence.

MCP's host-client-server architecture places connection permissions, user consent, and authorization with the host. Treat that as a protocol boundary that still needs application-specific security policy. [MCP architecture](https://modelcontextprotocol.io/specification/latest/architecture)

## Validate Output at Three Levels

| Level | Question | Example evidence |
|---|---|---|
| Structural | does the response match the declared schema? | parser and schema-validator result |
| Business | is the requested action valid for this account and state? | policy and database validation |
| Safety and provenance | is it allowed, source-supported, and appropriately classified? | citation, approval, and policy receipt |

A valid JSON object or syntactically correct command is not a safe business action.

## Test the Actual System

A safety evaluation suite should include:

- hostile instructions in user input, retrieved files, tool results, and tickets;
- missing or conflicting authorization attributes;
- cross-tenant and stale-source retrieval attempts;
- malformed or valid-but-unsafe tool arguments;
- retry, cancellation, and lost-response paths for real-world effects;
- logging/redaction tests and incident replay from controlled references;
- independent human review for high-stakes workflows.

Record test input classifications and redacted evidence so the safety claim can be rechecked after a model, prompt, tool, or policy change.

## Gotchas

- **Regex stripping is not a prompt-injection defense.** It only catches phrases someone anticipated. **Fix:** preserve trust boundaries and authorize tools outside the model.
- **A safety prompt is not a permission system.** The model can still propose an unauthorized action. **Fix:** bind capabilities to application identity, scope, and expiry.
- **A sandbox with broad credentials remains high-risk.** Isolation does not neutralize the authority mounted inside it. **Fix:** use least privilege and block unnecessary egress.
- **Post-action review is not a rollback plan.** A reviewer cannot undo every message, deletion, or publication. **Fix:** gate irreversible effects before execution and use idempotency/reconciliation.
- **Logs can leak exactly what the sandbox protected.** Full prompts and tool results may become a shadow data store. **Fix:** emit redacted references, protect access, and enforce retention.
- **A refusal after retrieval is too late.** Data may already have crossed an authorization boundary. **Fix:** enforce policy before retrieval context reaches the model.

## Sources

- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 8725: JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725)

## See Also

- [[agent-security]]
- [[agent-orchestration]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[llmops]]
