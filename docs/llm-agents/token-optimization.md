---
title: "Token Optimization for Agents"
description: "Reduce the measured cost and latency of agent workflows without trading away task quality, safety, provenance, or reliable completion."
tags: [llm-agents, token-optimization, cost-optimization, context-engineering, prompt-caching, evaluation]
---

# Token Optimization for Agents (September 2026)

Version context: tokenizers, model context limits, billing categories, cache behavior, and batch or priority tiers are provider- and model-specific. Use the provider's current usage data and pricing schedule for the resolved deployment; do not carry forward a static price table or a universal token ratio.

The objective is not "use the fewest tokens." The objective is to minimize measured workflow cost and latency while meeting the task's quality, safety, and completion requirements. A terse answer that triggers retries, misses a legal qualifier, or performs the wrong tool action is an expensive failure.

## Establish a Measurement Boundary

Measure one task or workflow at a time. Record the release revision, task class, terminal outcome, provider-reported usage, latency, retries, cache signals where available, tool calls, and validator result.

```json
{
  "trace_id": "tr_01...",
  "release_id": "research-summarizer@18",
  "task_class": "source-grounded-summary",
  "usage": {
    "input": 0,
    "output": 0,
    "cache_read": 0
  },
  "latency_ms": 0,
  "retry_count": 0,
  "tool_call_count": 0,
  "validator_outcome": "pass",
  "terminal_state": "completed"
}
```

The categories above are deliberately generic. Provider response objects may use different names or expose additional usage fields. Keep the original typed response in a controlled log if audit requires it, and normalize only the data the operator needs.

## Optimize the Highest-Leverage Context First

The most durable improvements remove irrelevant work rather than compressing language until it becomes ambiguous.

| Lever | Safe implementation | Measurement to keep |
|---|---|---|
| Task routing | route only well-separated task classes to approved configurations | routing accuracy, fallback rate, task success |
| Context selection | retrieve or load only evidence relevant to the declared task | citation coverage, missed-evidence rate |
| Tool surface | expose only tools necessary for the task | tool selection errors, authorization denials |
| Tool results | return structured, bounded fields and durable artifact references | repeat-call rate, validator outcome |
| Output contract | specify a short schema or maximum only where completeness is preserved | completeness, correction rate, user outcome |
| Repeated instructions | reuse a reviewed stable prefix when the provider supports caching | cache signal, privacy/tenant test, release revision |
| Retry policy | fix recurrent validation or timeout causes instead of retrying blindly | retry count, duplicate-effect rate |

Do not use "keyword-only" or ungrammatical output as a default optimization. It can destroy names, qualifiers, dates, and instructions that another system or person needs to interpret safely.

## Context Is a Retrieval and Policy Problem

Before adding a document, tool result, or chat turn to a prompt, ask:

1. Does this item answer a required part of the task contract?
2. Is it authoritative enough for the decision?
3. Is it current, within the tenant boundary, and permitted by data policy?
4. Can a small reference or structured extraction replace the raw content?
5. Can the downstream reviewer locate the original source from the output?

Prefer a source ID, revision, and relevant excerpt over a full transcript. Preserve provenance: a shorter context that loses the original source is usually a quality regression.

## Use Caching as a Controlled Optimization

Where a provider supports prompt caching, arrange stable shared instructions and reviewed tool descriptions before changing task-specific data. Follow the provider's current cache rules rather than assuming a fixed threshold, discount, or retention behavior.

Include these values in the cache or release key where relevant:

```text
prompt_revision + policy_revision + tool_schema_revision
+ model/configuration + tenant or trust boundary
```

Caching is not a permission mechanism. Do not reuse a cached context across users, tenants, or classifications unless the provider contract and your data policy explicitly allow it. [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) and [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) document provider-specific behavior that must be rechecked at deployment.

## Cost and Capacity Decisions

Calculate a request cost from provider-reported usage and the current schedule for the exact resolved model and processing tier:

```text
request cost = sum(reported usage category × current unit price)
workflow cost = request costs + tool costs + retries + human review cost
```

Keep this calculation in deployment or billing configuration, not copied into a long-lived article. The relevant decision is whether the complete workflow stays within its approved budget while its quality and safety evaluation still pass.

A smaller model, shorter context, cache feature, or asynchronous tier is a candidate configuration. Release it only after it meets the same task-specific acceptance criteria as the baseline.

## Run an Evidence-Based Optimization Loop

| Step | Required receipt |
|---|---|
| Baseline | frozen task sample, configuration revision, usage and quality distribution |
| Hypothesis | one proposed change and expected trade-off |
| Candidate run | same sample, same evaluation criteria, normalized usage |
| Error review | failures, retries, citation gaps, and unsafe action attempts |
| Decision | keep, revert, or investigate with owner and evidence |
| Production check | bounded rollout plus verified terminal outcomes |

This loop prevents an apparent reduction in input tokens from hiding an increase in correction, tool, or support costs.

## Gotchas

- **Input token savings can shift cost elsewhere.** Missing context can cause retries, web searches, or human escalation. **Fix:** measure whole-workflow cost and terminal task success.
- **Provider token counts are not interchangeable.** Characters, words, and one provider's tokenizer cannot predict another's billing exactly. **Fix:** use provider-reported usage for accounting.
- **Cached context still has a trust boundary.** Reuse can be unsafe when it crosses a tenant, policy, or revision boundary. **Fix:** include those boundaries in the cache/release design and test isolation.
- **A router can be a new source of failures.** Cheap routing errors may send high-stakes work to an unsuitable configuration. **Fix:** evaluate routing accuracy and define a safe fallback.
- **Aggressive compression can erase provenance.** A summary may be shorter but no longer show where a claim came from. **Fix:** retain source references and validate citation coverage.
- **Retries are often the dominant hidden cost.** A lower-cost request is irrelevant if it fails more often. **Fix:** record retries and repair their cause before optimizing wording.

## Sources

- [OpenAI: model selection](https://developers.openai.com/api/docs/guides/model-selection)
- [OpenAI: prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [OpenAI: Responses API reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [Anthropic: prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

## See Also

- [[tokenization]]
- [[context-engineering]]
- [[prompt-engineering]]
- [[llmops]]
- [[llm-api-integration]]
- [[agent-observability-dashboards]]
