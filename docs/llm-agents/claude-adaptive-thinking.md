---
title: "Claude Adaptive Thinking and Effort Control"
description: "Configure and evaluate Claude reasoning effort without relying on fixed, model-specific folklore."
tags: [llm-agents, claude, reasoning, effort-control, observability]
---

# Claude Adaptive Thinking and Effort Control (September 2026)

Version context: reasoning controls are model- and client-specific. The current Claude Code and Claude API documentation are the source of truth for supported effort levels, fixed-budget compatibility, and settings precedence. Recheck them whenever the model or client version changes.

Adaptive reasoning lets a model decide whether and how deeply to think on a given step. It is not a guarantee of correctness, and an effort label is not comparable across model families. Treat effort as a measured operating parameter alongside task success, latency, token use, and safety controls.

## The Controls Have Different Jobs

| Control | What it changes | What it does not guarantee |
|---|---|---|
| output_config.effort in the API | Overall work/token trade-off for a request | A fixed amount of hidden reasoning |
| Claude Code --effort | Launch/session effort setting | A permanent global policy |
| Interactive Claude Code /effort | Active-session setting; supported selections can persist per model | A uniform level across all models |
| CLAUDE_CODE_EFFORT_LEVEL | Explicit process-level override for supported clients/models | Support on every model or provider |
| Thinking display/toggle | Whether thinking is shown or enabled where supported | Cheaper execution or an audit log |
| max_tokens | A hard output ceiling | More reasoning by itself |

Claude Code documents low, medium, high, xhigh, and max where the selected model supports them. Available levels and defaults vary; unsupported values can be resolved differently by the active client. Confirm the effective level in the session UI or API response rather than assuming a setting was accepted.

## Adaptive Reasoning vs Fixed Thinking Budgets

In adaptive mode, a model may skip thinking for a straightforward action and spend more effort on a complex one. The current Claude Code documentation states that newer supported models always use adaptive reasoning, while some older model families can revert to a fixed thinking budget with compatible environment variables.

Therefore:

1. Choose effort for the normal workload.
2. Use an explicit fixed-budget mode only when the selected model and provider document it.
3. Do not copy a legacy MAX_THINKING_TOKENS recipe into a newer model without checking compatibility.
4. Treat a client upgrade as a configuration change that requires an evaluation run.

A high output ceiling is not a substitute for an appropriate effort level. It only permits a larger total response; it does not compel the model to use the space productively.

## API Configuration

Use a model identifier from an approved deployment allowlist. Keep the identifier outside source code so that a model upgrade is visible in configuration review.

```python
import os
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model=os.environ["ANTHROPIC_MODEL"],
    max_tokens=4096,
    output_config={"effort": "high"},
    messages=[
        {
            "role": "user",
            "content": "Review this migration plan and list blocking risks.",
        }
    ],
)

print(message.content)
```

The example demonstrates a configuration shape, not a universal production default. Confirm the current model supports the selected effort level and whether the selected provider exposes the same controls.

## Claude Code Configuration

Use an explicit session setting when the task needs a known reasoning posture:

```powershell
claude --effort high

$env:CLAUDE_CODE_EFFORT_LEVEL = "high"
claude
```

The environment variable is process-scoped and can override interactive choices. Remove or change it deliberately; a forgotten process-level override is a common source of surprising latency and usage. Interactive low, medium, high, and xhigh selections can also be saved per model for later sessions. Use /effort auto or review the model settings when an experiment should no longer affect future work.

Use /effort to inspect or adjust the active session. Use /effort auto only when returning to the documented model default is desired. Record the chosen level in a task receipt when it materially affects a benchmark or release decision.

## Select Effort by Measured Risk

| Workload | Starting posture | What to measure |
|---|---|---|
| Short, bounded transformation | low or medium after evaluation | Format validity, latency, retry rate |
| Routine coding task with tests | high as a candidate | Test pass rate, review findings, tool-call count |
| Architecture, security, or migration decision | high or xhigh as a candidate | Accepted design, blocker detection, human review |
| Critical one-off analysis | max only after comparison | Incremental task value versus cost and delay |

The table is a starting hypothesis. Keep the same model, tool policy, prompt shape, and evaluation set when comparing levels. Otherwise a result cannot be attributed to effort.

## Evaluation Loop

```text
freeze workload and acceptance criteria
        -> run baseline at approved effort
        -> record quality, latency, usage, and failure modes
        -> change one control
        -> run the same evaluation
        -> keep or revert with a receipt
```

Evaluate outcome-level properties: compilation/tests, structured-output validity, policy compliance, reviewer findings, task completion, and user-visible latency. Do not use the length of displayed reasoning as a quality metric.

## Tool Use and Cost

Effort affects an agent's whole behavior, including tool selection and the surrounding explanation. A higher level can make more tool calls or more detailed plans; that is useful only when the additional evidence improves the result.

Set separate controls for:

- tool allowlists and side-effect authorization;
- request and task budgets;
- timeout and maximum tool-call count;
- prompt/context size;
- trace retention and redaction;
- a kill switch for effectful work.

Reasoning tokens can be charged even when thought is collapsed or redacted. Budget alerts must use provider-reported usage, not an estimate based on visible output.

## Safe Observability

Store a redacted task receipt instead of raw private reasoning:

```json
{
  "task_id": "review-2026-09-003",
  "model_config_revision": "models/approved.yaml@42",
  "effort": "high",
  "policy_revision": "tool-policy@9",
  "result": "completed",
  "quality_gate": "tests-and-review-pass",
  "usage_source": "provider_response.usage"
}
```

This gives a reviewer enough context to reproduce the operating conditions without treating chain-of-thought content as a persistent system log.

## Gotchas

- **Effort labels are calibrated per model.** high on two models is not an apples-to-apples budget. **Fix:** compare only within a fixed model and client version.
- **An environment override can outlive an experiment.** It may silently affect later sessions. **Fix:** scope it to a process and verify the active effort in the session.
- **Fixed thinking budgets are not universal.** Some newer models always use adaptive reasoning. **Fix:** check the current model configuration documentation before applying a legacy variable.
- **More thinking can mean more tool calls and latency.** It is not automatically safer. **Fix:** keep authorization, budgets, and tool limits independent from effort.
- **Visible thinking is not an audit record.** It can be redacted, omitted, or unsafe to retain. **Fix:** log structured task and policy receipts instead.

## Sources

- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Claude Code environment variables](https://code.claude.com/docs/en/env-vars)
- [Claude API effort control](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Claude thinking steering and cost](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)
- [Claude extended-thinking model guidance](https://platform.claude.com/docs/en/about-claude/models/extended-thinking-models)

## See Also

- [[claude-code-ecosystem]]
- [[agent-design-patterns]]
- [[agent-evaluation]]
- [[context-engineering]]
- [[llm-api-integration]]
- [[production-patterns]]
