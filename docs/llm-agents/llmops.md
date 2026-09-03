---
title: "LLMOps"
description: "Run language-model systems with versioned evaluations, release gates, observable receipts, and data-minimizing telemetry."
tags: [llm-agents, llmops, evaluation, observability, governance, cost-optimization]
---

# LLMOps (September 2026)

Version context: model aliases, API behavior, pricing, cache rules, retention controls, and tool semantics change independently. Treat every resolved model, prompt, retrieval configuration, tool policy, and evaluation set as a reviewed release input rather than as permanent documentation.

LLMOps is the operational discipline for an LLM-backed workflow. Its purpose is not to collect every request in a dashboard. Its purpose is to decide whether a change improved a real task, to release that change safely, and to reconstruct or roll back a result when something goes wrong.

## Define the Unit of Change

A prompt edit can alter safety, quality, latency, and cost as materially as a code change. Put the complete candidate in a small release manifest:

```json
{
  "release_id": "support-triage-2026-09-03.1",
  "task_contract": "support-triage/v3",
  "model_key": "approved-triage-model",
  "resolved_model_revision": "recorded-at-deploy",
  "prompt_revision": "sha256:...",
  "retrieval_revision": "catalog@17",
  "tool_policy_revision": "tools@9",
  "eval_suite_revision": "triage-evals@12",
  "data_policy_revision": "retention@5",
  "owner": "support-platform"
}
```

The manifest identifies a behavior without copying secrets, full customer content, or a provider SDK object into source control. Store a protected reference or digest when replay needs input material.

## Release Lifecycle

| Stage | Question | Required evidence | Terminal outcome |
|---|---|---|---|
| Task contract | What must the workflow do and never do? | input/output schema, authorization boundary, acceptance criteria | approved or rejected scope |
| Baseline | What does the current release achieve? | frozen representative eval set and baseline receipt | comparable reference |
| Candidate | What changed? | one reviewed manifest diff and migration notes | evaluable candidate |
| Offline evaluation | Did it improve without breaking known cases? | deterministic checks, labeled cases, and reviewed failure sample | pass, hold, or reject |
| Staging or shadow run | Does it operate safely under realistic conditions? | trace, policy checks, latency and error evidence | ready or blocked |
| Canary | Does a bounded real route preserve the contract? | explicit cohort, rollback point, terminal receipts | promote or roll back |
| Archive | Can an operator explain the result later? | immutable release/eval/decision references | reproducible record |

Do not promote an apparently better prompt merely because one demo looks good. A release decision needs a comparison against the same task contract and a record of the cases that still fail.

## Build an Evaluation Contract

Use several forms of evidence because they catch different errors:

| Evidence type | Best for | Limitation |
|---|---|---|
| Deterministic assertion | schemas, exact labels, permissions, forbidden fields | cannot assess every semantic answer |
| Labeled reference set | known task outcomes and regressions | coverage is limited to the data selected |
| Human review | nuance, usefulness, policy interpretation | requires calibrated rubric and sampling |
| Model-based grader | scalable triage of well-defined criteria | is a signal to audit, not an unbounded authority |
| Production receipt | actual terminal state and user-visible failure | must be privacy-aware and sampled safely |

OpenAI's evaluation guidance illustrates test criteria such as an exact string check against a reference label. That pattern is useful when the task has an objective answer; it is not a substitute for human review of ambiguous or high-impact outcomes. [Working with evals](https://developers.openai.com/api/docs/guides/evals)

Freeze the test inputs, evaluator version, and acceptance thresholds before comparing candidates. If a model-based grader changes, treat that as a separate candidate change and calibrate it against reviewed examples.

## Trace Work Without Creating a Data Leak

One user-visible workflow or durable task should have one trace ID. Model calls, retrieval, tool calls, approvals, validators, retries, and handoffs become child events. Emit references and structured fields by default, not unrestricted prompts or tool output.

```json
{
  "schema_version": "llmops-event/v1",
  "trace_id": "tr_01...",
  "release_id": "support-triage-2026-09-03.1",
  "operation": "model.complete",
  "outcome": "completed",
  "duration_ms": 842,
  "usage": {"input": 0, "output": 0},
  "input_ref": "protected:request/...",
  "output_ref": "protected:result/...",
  "tool_policy_revision": "tools@9",
  "attempt": 1
}
```

A useful event answers which release ran, what authority was used, how it ended, and where the controlled evidence lives. The OpenTelemetry GenAI semantic-conventions project is a useful interoperability reference; application-specific fields should remain documented and namespaced. [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Make Safety and Authorization Release Gates

A model or its prompt is not an authority boundary. Keep authorization, tenant isolation, side-effect approval, and business invariants in deterministic application code.

For each candidate, test at least:

1. malformed, missing, and adversarial inputs;
2. tool arguments that are valid JSON but unauthorized;
3. conflicting instructions embedded in retrieved or user-controlled text;
4. duplicate delivery and timeout paths for effectful work;
5. redaction and retention behavior in traces and evaluator inputs;
6. a known-safe rollback to the previous release manifest.

The current [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices) are a provider-specific starting point, not a replacement for a product threat model.

## Operate Costs as Measurements, Not Folklore

Collect provider-reported usage, cache signals where available, model revision, latency, retry count, tool-call count, and task outcome for each release. Resolve price only from the current pricing schedule for the exact model and processing tier at planning or billing time.

Use a budget as a release condition:

```text
quality and safety SLOs met
    AND measured workload cost is within the approved budget
    AND no unaccounted retry or tool side effect exists
        => candidate may advance
```

A lower token count is not automatically a cost improvement if it increases retries, defers work to an expensive tool, or lowers task success.

## Incident and Rollback Practice

An incident record should link the trace, release ID, input/output references, external receipts, and evaluator findings. Its first question is operational: did an external action occur? Its second is causal: which release input changed the behavior?

Rollback by restoring a previously verified manifest and confirming the resolved model/configuration at runtime. Do not roll back by guessing a historic model alias, prompt text, or cache configuration.

## Gotchas

- **Averages hide harmful tails.** Mean latency or average score can conceal a small class of catastrophic failures. **Fix:** segment evaluations and telemetry by task, locale, tool path, tenant policy, and terminal state.
- **LLM-as-judge is not self-validating.** A grader can drift or share the same blind spot as the candidate. **Fix:** calibrate it against human-reviewed cases and retain disagreements for audit.
- **Trace payloads can become a shadow data store.** Logging full prompts, retrieved files, or tool output creates retention and access risks. **Fix:** emit controlled references, redact early, and enforce a retention policy.
- **A canary without a rollback receipt is a production experiment.** A small cohort does not make an unknown side effect reversible. **Fix:** define the halt condition, idempotency strategy, and rollback release before traffic moves.
- **A model alias is not a reproducibility record.** Providers may update aliases or availability. **Fix:** record the resolved model/configuration observed by the running release.

## Sources

- [OpenAI: working with evals](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI: Responses API reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [OpenAI: safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## See Also

- [[agent-evaluation]]
- [[agent-observability-dashboards]]
- [[llm-api-integration]]
- [[prompt-engineering]]
- [[token-optimization]]
- [[agent-security]]
