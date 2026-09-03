---
title: "LangGraph (September 2026)"
category: frameworks
tags: [llm-agents, langgraph, state-machine, workflow, orchestration]
---

# LangGraph (September 2026)

Reviewed 2026-09-03. LangGraph is a low-level orchestration framework and runtime for long-running, stateful agent workflows. It can use LangChain components, but a LangGraph workflow can also use other model and tool integrations. [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)

## What the Graph Owns

| Graph concern | Keep explicit |
|---|---|
| State | Typed fields and merge semantics |
| Nodes | One bounded operation per node |
| Edges | Deterministic or auditable routing rules |
| Persistence | Checkpoint identity and resume contract |
| Interrupts | Human approval or external wait boundary |
| Terminal state | Pass, hold, retryable failure, or failure |

Use a graph when the workflow needs visible state, branching, restartability, or a human boundary. A single application-controlled agent loop is simpler for one bounded task.

## Minimal StateGraph

This Python 3.11+ example contains no model call. Replace the deterministic nodes with provider calls only after the state and terminal criteria are clear.

```python
from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ReviewState(TypedDict):
    text: str
    verdict: str


def classify(state: ReviewState) -> dict[str, str]:
    verdict = "review" if "citation" in state["text"].lower() else "pass"
    return {"verdict": verdict}


def route(state: ReviewState) -> str:
    return "human_review" if state["verdict"] == "review" else "done"


def human_review(state: ReviewState) -> dict[str, str]:
    return {"verdict": "held_for_review"}


builder = StateGraph(ReviewState)
builder.add_node("classify", classify)
builder.add_node("human_review", human_review)
builder.add_node("done", lambda state: {})
builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route)
builder.add_edge("human_review", END)
builder.add_edge("done", END)
graph = builder.compile()


if __name__ == "__main__":
    print(graph.invoke({"text": "add a citation", "verdict": ""}))
```

## Design Rules

| Rule | Reason |
|---|---|
| Keep state serializable | Checkpoints and debugging need a durable representation |
| Make node outputs narrow | Reduces accidental mutation and ambiguous merges |
| Put policy routes in code | Budgets, permissions, and publication gates are not model preferences |
| Use model routing only for open-ended classification | It can be evaluated as a separate task |
| Store external receipts in state references | A text answer is not proof of an external side effect |

## Interrupt and Resume

An interrupt is a state transition, not a UI convenience. Before pausing for approval or external input, persist:

- workflow/run ID;
- checkpoint or state reference;
- requested action and evidence;
- approver identity/role required;
- expiration and resume rule.

On resume, revalidate time-sensitive inputs and permissions. Do not replay a side effect merely because the process restarted.

## LangGraph vs Application Code

| Use LangGraph when | Use plain application code when |
|---|---|
| The workflow has durable state, branches, and recovery | The task is one bounded model/tool loop |
| Operators need a visible execution path | A simple typed function pipeline is sufficient |
| A human approval must survive a restart | Approval is synchronous and local |
| Multiple independently tested nodes share a state contract | Splitting would add only ceremony |

## Gotchas

- **Issue: Treating a node name as an authorization boundary.** A node can still call any tool exposed to its runtime. **Fix:** enforce a separate tool policy at the application/tool gateway.
- **Issue: Mutating nested state in place.** Concurrent or resumed paths can see unintended changes. **Fix:** return narrow updates and define merge behavior explicitly.
- **Issue: Looping on model feedback without a limit.** A self-correction loop can spend budget forever. **Fix:** persist attempt count, validator result, and a terminal HOLD state.
- **Issue: Resuming an external write without reconciliation.** The previous attempt may have succeeded. **Fix:** store an idempotency key and external receipt reference in state.

## See Also

- [[agent-orchestration]]
- [[multi-agent-systems]]
- [[multi-agent-messaging]]
- [[agent-evaluation]]
- [[production-patterns]]

## Sources

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph documentation index](https://docs.langchain.com/llms.txt)
