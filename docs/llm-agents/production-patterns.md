---
title: "Production LLM and Agent Patterns (September 2026)"
category: techniques
tags: [llm-agents, production, evaluation, observability, human-in-the-loop]
---

# Production LLM and Agent Patterns (September 2026)

Reviewed 2026-09-03. A production LLM system is an application with probabilistic components. Make data authority, side effects, evaluation, and recovery explicit in application code; do not try to encode them solely in prompt wording.

## Core Control Plane

| Concern | Production contract |
|---|---|
| Input | Typed work item, source reference, and data-classification policy |
| Model | Exact model/provider configuration and prompt version |
| Tools | Allowlist, schema, timeout, identity, and side-effect policy |
| State | Run ID, retry count, checkpoint, and idempotency key |
| Output | Schema validation plus task-specific acceptance criteria |
| Evidence | Tool receipts, source references, validator result, reviewer decision |
| Operations | Trace, budget, error category, owner, and rollback path |

The OpenAI Agents SDK distinguishes code-controlled orchestration from model-controlled orchestration. Use code when the decision is a policy, authorization, budget, or deterministic routing rule. [Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)

## Retrieval Is a Data Product

Retrieval is appropriate when the answer must be grounded in changing or proprietary content. Treat it as a separate system with ingestion, access control, document versioning, retrieval evaluation, and citation checks.

| Question | Direct context is sufficient when | Retrieval is needed when |
|---|---|---|
| Source set | It is small, known, and versioned | It is large, changing, or user-specific |
| Authority | One controlled artifact is the truth | Multiple sources need ranking and traceability |
| Failure mode | Missing context is obvious | Wrong or stale retrieval can silently mislead |

Never claim that a vector search result is authoritative merely because it was retrieved. Record the source identity and version with the answer.

## Deterministic Validation

Keep validators small and task-specific. This Python 3.11+ example validates a candidate that must cite a known source and use an allowed status.

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    status: str
    source_id: str
    summary: str


def validate(candidate: Candidate, allowed_sources: set[str]) -> list[str]:
    errors: list[str] = []
    if candidate.status not in {"draft", "approved"}:
        errors.append("invalid_status")
    if candidate.source_id not in allowed_sources:
        errors.append("unknown_source")
    if not candidate.summary.strip():
        errors.append("empty_summary")
    return errors


if __name__ == "__main__":
    item = Candidate("draft", "source-42", "Verified change summary.")
    print(validate(item, {"source-42"}))
```

Use a separate human or independent evaluator for editorial judgment, safety review, or semantic correctness that a deterministic validator cannot measure.

## Side Effects Need an Approval State

```text
PENDING -> GENERATED -> VALIDATED -> AWAITING_APPROVAL -> PUBLISHED
                       |                    |
                       v                    v
                     REJECTED             HELD
```

Publication, email, payment, data mutation, and external tickets should use an explicit approval state. A model-generated sentence is never the receipt for a side effect.

## Observability

Trace workflows, model turns, tools, validators, and approvals under one run ID. The GenAI semantic-conventions project covers spans, metrics, and events for GenAI clients and MCP; add application-specific, namespaced fields for work-item and evidence identity. [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai)

Minimum operator questions:

- Which run and configuration produced this output?
- Which sources and tools influenced it?
- Did a validator or approver accept it?
- Did an external action complete, fail, or become uncertain?
- Can the same work item be replayed without duplicating a side effect?

## Gotchas

- **Issue: Collecting raw prompts and tool results by default.** Traces become a secondary sensitive-data store. **Fix:** retain references and allowlisted metadata by default; require controlled capture for full payloads.
- **Issue: Retrying a timeout as if it were a clean failure.** The external action may have completed. **Fix:** persist an idempotency key and reconcile the provider receipt before retrying.
- **Issue: Letting a model choose a governance action.** An instruction is not an access-control system. **Fix:** enforce approval, budget, and publication gates in deterministic code.
- **Issue: Calling a successful model response production-ready.** It may lack sources, validation, and recovery behavior. **Fix:** require a testable acceptance contract and operational evidence.

## See Also

- [[agent-observability-dashboards]]
- [[agent-evaluation]]
- [[function-calling]]
- [[rag-pipeline]]
- [[tool-use-patterns]]

## Sources

- [OpenAI Agents SDK: Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
- [Claude: How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
