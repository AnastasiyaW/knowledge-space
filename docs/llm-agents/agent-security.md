---
title: "Agent Security and Safety"
description: "Threat-model and control LLM agents across prompts, tools, memory, identities, supply chain, and observability"
---

# Agent Security and Safety (September 2026)

Version context: use the current OWASP agentic-applications guidance, current provider security documentation, and the protocol revisions actually deployed. Threat models must be reviewed whenever tools, data sources, identities, or memory behavior change.

Agent risk comes from the combination of untrusted content, model decisions, and side effects. A model can be helpful and still be induced to misuse an authorized capability. Security therefore lives in the system boundary, not in prompt wording alone.

## Threat Model

Inventory every trust boundary:

| Surface | Typical threat | Required control |
|---|---|---|
| User input | Direct prompt injection, unsafe request | Input policy, scope validation, rate limit |
| Retrieved web/document content | Indirect instructions, poisoned facts | Treat as data, provenance, action isolation |
| Tool metadata / skills | Misleading description, supply-chain compromise | Identity, review, pinned revision, allowlist |
| Long-term memory | Context or memory poisoning | Write authorization, provenance, expiry, review |
| Tool execution | Excessive scope, parameter abuse, exfiltration | Server-side authz, schemas, least privilege |
| Agent-to-agent exchange | Overscoped context, confused authority | Typed handoff, identity, policy per action |
| Telemetry | Sensitive input/output disclosure | Redaction, retention, access controls |

OWASP's 2026 Top 10 for Agentic Applications is a useful taxonomy, but it does not replace a system-specific abuse-case review.

## Non-Negotiable Boundary

```text
untrusted content -> model proposal -> schema validation -> policy authorization
                  -> scoped tool execution -> immutable receipt -> response
```

Untrusted content may influence a model's answer, but it must never directly change its permissions, tool allowlist, identity, or approval state.

## Tool Authorization

Every tool call needs a declared side-effect class and a server-enforced scope.

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolRequest:
    actor_id: str
    tenant_id: str
    action: str
    resource_id: str
    arguments: dict[str, Any]


def authorize_export(request: ToolRequest) -> None:
    if request.action != "export_report":
        raise PermissionError("action is not available")
    if not request.resource_id.startswith(f"{request.tenant_id}:"):
        raise PermissionError("resource is outside tenant scope")
    if "destination" not in request.arguments:
        raise ValueError("destination is required")
```

After authorization, validate the full typed input and bind the service credential to the least privilege necessary for that action. Do not give the model a broadly privileged token and ask it to be careful.

## Prompt Injection and Retrieved Content

Prompt injection is an input-integrity problem. Defensive prompts and classifiers can reduce risk, but cannot make untrusted text trustworthy.

Controls:

1. Label data from users, web pages, email, files, and tool responses as untrusted.
2. Keep untrusted text outside instructions and policy definitions.
3. Require explicit user/authorization context before external side effects.
4. Restrict which tools are available at each stage; do not expose a global tool universe.
5. Verify source provenance and citations before relying on retrieved claims.
6. Test multi-step indirect injection scenarios in a controlled environment.

Never copy instructions from a retrieved document into a system prompt, memory record, or skill without review.

## Memory and Context Integrity

Long-term memory is a writable attack surface. Each record needs a writer identity, source reference, timestamp, schema, tenant scope, confidence/provenance, retention rule, and optional approval status.

Use an explicit promotion gate:

```json
{
  "memory_id": "mem_01J...",
  "writer": "service:knowledge-curator",
  "source_ref": "artifact://approved/...",
  "tenant_id": "tenant_42",
  "classification": "internal",
  "expires_at": "2026-12-31T00:00:00Z",
  "promotion_state": "approved"
}
```

A model-generated suggestion is not automatically eligible for durable memory. It must pass the same source and authorization rules as any other content.

## Identity, Secrets, and Supply Chain

- Give each agent/service identity only the permissions it needs.
- Keep credentials in a secret manager or delegated workload identity, never in prompts, tool descriptions, logs, or memory.
- Pin dependencies and tool/skill revisions; review provenance before installation.
- Separate read-only research credentials from write-capable operational credentials.
- Disable or require approval for external messaging, payment, destructive writes, and privilege changes.
- Rotate or revoke an agent identity when a tool, skill, or memory source is suspected compromised.

Git worktrees help isolate branch checkouts but are not a sandbox for network, credentials, processes, or mounted storage. Add OS/container/cloud controls where those boundaries are needed.

## Observability, Response, and Red Teaming

Log redacted model/tool events with task ID, policy revision, actor/tenant scope, tool decision, receipt, and terminal state. Alert on denied high-risk attempts, unexpected data volume, repeated retries, cross-tenant access attempts, and unexpected destinations.

An incident plan needs a kill switch for tool execution, identity revocation, trace preservation, affected-memory quarantine, dependency rollback, and a documented revalidation before re-enabling autonomy.

Red-team the real flow: direct and indirect injection, poisoned memory, malformed tool output, duplicate requests, compromised dependency metadata, overscoped handoffs, and refusal bypass attempts.

## Gotchas

- **System prompts are not an authorization layer.** They can be ignored or manipulated. **Fix:** enforce authorization and side-effect controls in code before a tool runs.
- **Retrieved documents are not instructions.** They can contain hostile text or misleading metadata. **Fix:** isolate them as untrusted data and require source/provenance checks.
- **Memory makes compromise persistent.** A poisoned record can affect later runs. **Fix:** use write permissions, immutable provenance, expiry, and a quarantine/review path.
- **Guardrails can leak data through telemetry.** Traces may capture raw prompts and tool inputs. **Fix:** test redaction, retention, and access controls with representative sensitive content.
- **Worktrees are not a security sandbox.** They share host resources and credentials unless separately constrained. **Fix:** isolate credentials, network, processes, and storage at the environment layer.

## Sources

- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenAI Agents SDK: guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [Git worktree documentation](https://git-scm.com/docs/git-worktree)

## See Also

- [[agent-fundamentals]]
- [[agent-memory]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[production-patterns]]
