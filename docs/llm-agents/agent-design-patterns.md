---
title: "Agent Design Patterns"
description: "Select bounded control-flow patterns for LLM systems: direct tools, ReAct, plans, state machines, and specialist handoffs"
---

# Agent Design Patterns (September 2026)

Version context: patterns are architectural choices, not framework features. Pin the model, tool schemas, policy revision, and evaluation suite used by a deployed flow.

A good agent pattern makes the decision boundary explicit: the model may propose the next action, while deterministic code decides whether that action is allowed, records the result, and chooses the terminal state.

## Start Below Agency

Use the least dynamic shape that meets the task:

| Shape | Model decides | System decides |
|---|---|---|
| Direct tool call | Nothing beyond input content | Tool, parameters, authorization, response |
| Fixed workflow | Content within a known step | Step order, retries, state transitions |
| Bounded ReAct loop | Next allowed read/reasoning step | Tool allowlist, budget, termination |
| Plan and execute | Candidate plan and replanning request | Plan validation, step execution, approval |
| Specialist handoff | Suitable authorized specialist | Identity, history projection, capability |
| DAG | Node-local proposal | Dependencies, joins, concurrency, receipts |

A fixed workflow is usually easier to test and safer to operate. Add an agent loop only when the next step genuinely depends on information that cannot be enumerated beforehand.

## Bounded ReAct

The ReAct paper describes interleaving reasoning traces with actions and observations. In production, do not treat raw model reasoning as an audit log or a permission grant. Persist structured action proposals and tool receipts instead.

```text
input -> model proposes an allowed action -> policy validates
      -> tool executes -> receipt persists -> next state or terminal result
```

Every loop needs a stop condition: successful evidence, insufficient information, denied action, exhausted attempt/cost/time budget, or external approval required.

## Action Proposal Contract

Require the model to emit a schema that is independent of any provider SDK:

```json
{
  "action": "search_documents",
  "arguments": {"query": "invoice INV-42"},
  "purpose": "find the authorized invoice record",
  "expected_receipt": "document-list-v1"
}
```

The `purpose` is an operator-visible summary, not hidden chain-of-thought. The policy layer validates action name, argument schema, actor scope, and remaining budget before any tool runs.

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ActionProposal:
    action: str
    arguments: dict[str, Any]
    purpose: str


ALLOWED_ACTIONS = {"search_documents", "get_invoice"}


def authorize(proposal: ActionProposal, remaining_steps: int) -> None:
    if remaining_steps <= 0:
        raise RuntimeError("step budget exhausted")
    if proposal.action not in ALLOWED_ACTIONS:
        raise PermissionError(f"action is not allowed: {proposal.action}")
    if not proposal.purpose.strip():
        raise ValueError("operator-visible purpose is required")
```

## Plan and Execute

A plan is a mutable hypothesis, not a command. Use a plan when:

- the task has multiple dependent objectives;
- an operator needs to inspect a proposed approach before side effects;
- intermediate results may trigger an authorized replan;
- each step can produce a receipt and a defined failure state.

Keep planning and execution separate. Validate a plan against current permissions and facts immediately before each step; never execute an old plan blindly after tools, data, or policy have changed.

## Reflection and Verification

A self-critique model call can produce useful hypotheses, but it is not verification. Use it to generate candidate checks, then run deterministic tests, source retrieval, schema validation, or an independent evaluator.

| Need | Suitable mechanism |
|---|---|
| Validate JSON / typed output | Schema validator |
| Verify a calculation | Deterministic code |
| Verify a source claim | Retrieved primary source with citation |
| Verify a code change | Test/build plus independent review |
| Generate alternative strategy | Model critique or planner |
| Approve high-impact action | Authorized human or policy service |

## Tool Discovery and Composition

Dynamic tool discovery expands the attack surface and the model's decision space. Prefer a small task-scoped allowlist. If discovery is required, treat tool metadata as untrusted until its identity, schema, permissions, and side-effect class are verified.

Tool composition needs a contract at every edge: output schema, tenant/actor scope, error behavior, deadline, idempotency key, and receipt. An observation that lacks provenance must not drive a side-effecting step.

## Handoffs

A handoff is appropriate when a distinct capability or authority owns the next task. It must carry a typed request, an approved context projection, a deadline, a trace reference, and a defined owner for the final response.

Do not hand an entire conversation to a specialist by default. Minimize it to the facts and artifacts the specialist is authorized to see.

## Pattern Selection Checklist

1. Write the terminal result and evidence required to call it complete.
2. Identify every side effect and authorization boundary.
3. Implement the shortest deterministic workflow that meets the task.
4. Add a bounded agent decision only where the next step is genuinely unknown.
5. Instrument action proposals, policy decisions, tool receipts, and stop reason.
6. Evaluate the whole flow against representative and adversarial cases.

## Gotchas

- **A model-generated plan can become stale.** Tool output and permissions change after planning. **Fix:** authorize and validate immediately before each action, then replan from current receipts.
- **Raw reasoning is not a security control.** It may be incomplete, sensitive, or misleading. **Fix:** persist structured proposals, policies, and receipts rather than relying on hidden reasoning text.
- **Reflection can amplify the same mistake.** The same model may rationalize an incorrect answer. **Fix:** use independent deterministic checks or a separately calibrated evaluator.
- **Dynamic discovery is not authorization.** An advertised tool can be unsuitable or malicious. **Fix:** enforce identity, schema, and task-scoped permission checks outside the model.

## Sources

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [OpenAI Agents SDK: agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [OpenAI model guidance: tool orchestration](https://developers.openai.com/api/docs/guides/latest-model)

## See Also

- [[agent-fundamentals]]
- [[agent-architectures]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[multi-agent-systems]]
