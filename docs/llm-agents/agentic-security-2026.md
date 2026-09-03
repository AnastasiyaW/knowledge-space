---
title: "Agentic AI Security"
description: "A threat-model and control guide for tool-using agents, MCP integrations, persistent memory, and irreversible effects. Scope checked 2026-09-03."
tags: [agent-security, mcp, prompt-injection, authorization, supply-chain, ai-safety]
---

# Agentic AI Security

**Scope checked: 2026-09-03.** Agent security is an application-security problem with a probabilistic planner inside it. Do not rely on an attack-rate headline, a single CVE, or a prompt filter as the security boundary. Start with a threat model, enforce authority outside the model, and preserve receipts for every external effect.

OWASP's Agentic Top 10 highlights goal hijack, tool misuse, identity and privilege abuse, supply-chain vulnerabilities, and unexpected code execution among the critical risk classes. [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)

## Threat Model First

Map the actual data and authority flow:

```text
untrusted input -> retrieval / context -> model planner -> tool request
                       |                    |              |
                    private data          memory         effect executor
                                                               |
                                                         external system
```

For each boundary, record the principal, data classification, allowed action, expiration, audit event, and recovery path. A high-risk architecture combines all three of these in one unconstrained loop:

1. reads private data;
2. processes attacker-influenced input;
3. can take an external action.

The response is separation and enforced mediation, not merely a stronger system prompt.

## Core Risk Classes

| Risk | Example | Control boundary |
|---|---|---|
| Goal hijack / prompt injection | web page asks the agent to override policy | label content untrusted; tool executor ignores model prose as authority |
| Tool misuse | model selects a valid tool for an invalid business action | schema, authorization, approvals, and idempotency at the executor |
| Identity and privilege abuse | leaked or overbroad token reaches a connector | workload identity, narrow scopes, audience validation, revocation |
| Supply-chain compromise | dependency or remote MCP server changes behavior | provenance, pinning, review, controlled rollout |
| Unexpected code execution | tool input reaches shell or interpreter | sandbox, allowlisted commands, no broad mounts or credentials |
| Memory poisoning | hostile text becomes durable instruction | source provenance, write policy, reviewable change history |
| Data exfiltration | permitted read is encoded into a permitted outbound call | end-to-end egress and action-graph controls |

## Enforce Capability, Not Intent

The agent can propose an action. A deterministic effect service decides whether it happens:

```json
{
  "task_id": "research-044",
  "action": "create_draft",
  "resource_scope": "project:happyin-space",
  "arguments_digest": "sha256:...",
  "approval_ref": "approval:appr_01...",
  "idempotency_key": "research-044:v1",
  "expires_at": "2026-09-03T18:00:00Z"
}
```

Before an effect, verify the caller identity, recipient audience, immutable request, scope, approval, expiry, and idempotency reservation. Changed arguments require a new capability. An unknown outcome is reconciled from a provider receipt before retrying.

See [[agent-safety-alignment]] for a concrete capability and atomic replay contract.

## MCP Boundaries

MCP makes tools discoverable; it does not make them trusted. The protocol advises hosts to keep user consent and control over data access and tool invocation, and says tool descriptions should be treated as untrusted unless they come from a trusted server. [MCP architecture](https://modelcontextprotocol.io/specification/latest/architecture) [MCP tools](https://modelcontextprotocol.io/specification/latest/server/tools)

For remote MCP servers:

1. verify server identity and transport before registering it;
2. request minimum OAuth scope and validate tokens are intended for that resource;
3. keep upstream credentials server-side rather than passing them through;
4. expose only tools required for the current workflow;
5. require user or policy approval for high-impact calls;
6. log tool call, caller, request digest, and resulting receipt.

MCP authorization requires resource/audience binding and rejects token passthrough as a safe general pattern. [MCP authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization)

## Memory Is Data, Not Policy

Persistent memory may contain claims from users, retrieved pages, tools, or earlier model outputs. Store provenance and treat every write as data:

| Field | Purpose |
|---|---|
| source reference | identify where the claim originated |
| trust label | distinguish user assertion, approved policy, and untrusted retrieval |
| authorizing principal | show who allowed the write |
| expiry or review date | prevent stale instruction from becoming permanent authority |
| revision history | audit changes and roll back safely |

Never elevate a retrieved instruction into a permission, routing rule, or credential reference solely because it appears in a trusted-looking document.

## Security Test Matrix

Exercise the integrated workflow, not isolated prompts:

- direct and indirect injection in web pages, attachments, records, and tool output;
- cross-tenant retrieval and output attempts;
- mutated tool arguments and schema-valid but policy-invalid actions;
- stale approvals, expired capabilities, and identity/audience mismatch;
- duplicate and lost-response paths for publication, deletion, or payment;
- compromised dependency or server-version simulation;
- cancellation, sandbox escape, egress, and log-redaction checks.

Record the test input class, policy revision, expected decision, and evidence. A “safe” text completion is not proof that the effect executor would reject an unsafe call.

## Incident-Ready Observability

For every material tool request, retain a redacted trace containing:

- task and session identifiers;
- authenticated caller and policy revision;
- normalized action and argument digest;
- approval or denial decision;
- tool/server version;
- external receipt or reconciliation state.

Protect this data: observability can otherwise create the same data-exposure path the agent was meant to avoid.

## Gotchas

- **Injection filtering is not a permission system.** Novel instructions can evade text patterns. **Fix:** enforce authorization and scope after the model proposes a call.
- **A sandbox can contain broad authority.** Mounted tokens and permissive egress can defeat filesystem isolation. **Fix:** minimize credentials, paths, processes, and destinations together.
- **A tool can be safe alone but unsafe in a chain.** Read, encode, and send may exfiltrate data without any one “dangerous” tool. **Fix:** model end-to-end action paths and outbound policy.
- **Memory creates delayed attacks.** A poisoned note can influence future sessions. **Fix:** attach provenance, expiry, and review to memory writes.
- **A retry can duplicate harm.** Timeouts hide whether the external service acted. **Fix:** reserve idempotency before the effect and reconcile before repeating it.

## Sources

- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [Model Context Protocol tools](https://modelcontextprotocol.io/specification/latest/server/tools)
- [Model Context Protocol authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

## See Also

- [[agent-safety-alignment]]
- [[agent-security]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[social-media-mcp-tools]]
