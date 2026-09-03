---
title: "Frontier Model Selection (September 2026)"
category: concepts
tags: [llm-agents, model-selection, evaluation, deployment, open-weights]
---

# Frontier Model Selection (September 2026)

Reviewed 2026-09-03. “Frontier model” is a moving market label, not a stable technical tier. Select a model family by a tested workload contract, then pin an exact provider model ID or open-weight artifact for each deployment.

## Start with the Workload Contract

| Contract dimension | Question to freeze | Evidence |
|---|---|---|
| Task | What output is accepted? | Schema, rubric, or test fixture |
| Modality | Which input and output media are required? | Representative input set |
| Tool use | Must the model plan, call tools, or only produce text? | Tool-call success and recovery rate |
| Deployment | Cloud API, private endpoint, or local runtime? | Data-flow and access policy |
| Operations | What latency, budget, and availability bounds apply? | Trace and cost envelope |
| Governance | Who may change the model or release a prompt? | Versioned approval record |

Do not turn a provider leaderboard into a routing policy. Benchmarks are useful for creating hypotheses, but deployment decisions need evaluation data from the actual prompts, documents, tools, languages, and failure modes of the product.

## Capability Dimensions

| Dimension | What to test | Common false proxy |
|---|---|---|
| Structured output | Schema-valid results after validation | A fluent JSON-looking answer |
| Tool use | Correct tool, arguments, and recovery on tool error | Number of tools advertised |
| Long context | Retrieval and answer quality at the required position | Maximum context-window size |
| Multimodal work | Accuracy on the media formats actually supplied | A generic “multimodal” label |
| Coding | Repository-level tasks with tests and diffs | One benchmark score |
| Local deployment | Memory, latency, licensing, and evaluation fit | Parameter count alone |

The current provider catalog is the authority for supported model IDs, context limits, and deprecations. Record the exact identifier in configuration; do not hard-code a family name such as “GPT” or “Claude” as if it were immutable.

## Evaluation Set

Maintain a small, versioned evaluation set before switching models:

1. Include normal inputs, adversarial inputs, long-context cases, and real tool failures.
2. Define automatic checks for schema validity, citations, tests, or policy constraints.
3. Sample human review for quality dimensions that cannot be reduced to a validator.
4. Compare candidates under the same tool policy, prompt version, temperature, and budget.
5. Keep the result, model ID, prompt/configuration hash, and reviewer decision as a release receipt.

### Decision Matrix

| Need | Preferred property | Required guardrail |
|---|---|---|
| High-stakes extraction | Strict structured output and deterministic validation | Reject invalid or incomplete fields |
| Fresh-data assistant | Reliable tool loop and source attribution | Tool allowlist and citation policy |
| Private/local workload | Compatible open-weight artifact and local runtime | License, model-file, and network review |
| Coding workflow | Repository tools and independent test gate | Diff review and targeted tests |
| Cost-sensitive bulk work | Measured quality at a lower-cost tier | Sampled quality audit before rollout |

## Release Pattern

```text
candidate model + prompt + tool policy
              |
              v
offline evaluation -> approval -> canary traffic
              |                         |
              v                         v
          HOLD / revise            trace + rollback signal
```

The release unit is the combination of model, provider endpoint, system instructions, tool schemas, retrieval configuration, and validator. Changing any one can alter behavior.

## Open Weights vs Managed APIs

| Choice | Strength | Operational responsibility |
|---|---|---|
| Managed API | Fast access to provider capabilities and managed capacity | Provider policy, regional availability, data handling, rate limits |
| Open weights | More control over hosting, inference stack, and fine-tuning | License, artifact provenance, serving, observability, and security |
| Hybrid | Workload-specific routing | Explicit data and fallback policy; no silent provider switch |

Treat licensing and data residency as separate checks. “Open” in a model name does not by itself answer either question.

## Gotchas

- **Issue: Selecting by a stale comparison table.** Model identifiers, limits, and retirement dates change faster than an article. **Fix:** use the provider catalog at release time and save the exact ID in the evaluation receipt.
- **Issue: Comparing candidates with different prompts or tools.** The experiment measures the harness, not the model. **Fix:** freeze the task, context, tool policy, and validator before a comparison.
- **Issue: Using a huge context window as a retrieval strategy.** Relevant evidence can still be missed or diluted. **Fix:** evaluate placement, retrieval, and citation quality on long inputs.
- **Issue: Treating an open-weight model as automatically private.** Telemetry, download sources, remote tools, and deployment configuration can still move data. **Fix:** review the complete data path.

## Limitations

No static page can rank a changing model market reliably. This reference defines a repeatable selection process; it intentionally does not publish a permanent “best model” list or price table.

## See Also

- [[function-calling]]
- [[tool-use-patterns]]
- [[model-optimization]]
- [[agent-evaluation]]
- [[ollama-local-llms]]

## Sources

- [OpenAI model documentation](https://platform.openai.com/docs/models)
- [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Gemini API model documentation](https://ai.google.dev/gemini-api/docs/models)
- [Hugging Face Hub model documentation](https://huggingface.co/docs/hub/models-the-hub)
