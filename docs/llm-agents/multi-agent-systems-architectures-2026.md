---
title: "Multi-Agent Systems Architectures (September 2026)"
description: "Production patterns for routing, fan-out, evaluation, and durable recovery in multi-agent systems; reviewed 2026-09-03."
---

# Multi-Agent Systems Architectures (September 2026)

Reviewed 2026-09-03. A multi-agent system is a workflow with more than one model-driven worker. Its architecture is defined by authority, state, data flow, and validation—not by anthropomorphic job titles.

## Choose a Pattern by Control Flow

| Pattern | Controller | Best for | Main risk |
|---|---|---|---|
| Manager plus specialists-as-tools | Manager | One final answer assembled from bounded sub-results | Manager prompt becomes an untestable policy engine |
| Explicit handoff | Router then selected specialist | A specialist must own the active user interaction | Ambiguous ownership after routing |
| Fan-out / fan-in | Deterministic scheduler | Independent partitions, search, or review dimensions | Duplicate work and non-deterministic merge |
| Generator / evaluator | Workflow controller | High-cost outputs with explicit acceptance criteria | Same-context self-review |
| Durable workflow | State-machine controller | Jobs that can outlive a process or call external systems | Retrying a side effect without reconciliation |

In the OpenAI Agents SDK, an agent used as a tool leaves the manager in control; a handoff moves the active conversation to the selected specialist. The distinction is architectural even if both use model calls. [Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)

## Shared Work Contract

Every worker receives a bounded work item and emits one result envelope. Avoid sharing a mutable free-form transcript as the system of record.

```json
{
  "work_item_id": "research:chunk-07",
  "run_id": "run_01J...",
  "parent_run_id": "run_01J-parent",
  "objective": "extract claims from this source set",
  "input_refs": ["source:42", "source:43"],
  "allowed_tools": ["fetch_source", "quote_locator"],
  "deadline_at": "2026-09-03T16:00:00Z",
  "output_schema": "claim-set/v1",
  "idempotency_key": "research:chunk-07:v1"
}
```

The result must contain a terminal status, source/evidence references, and an error category. A synthesizer should receive validated result envelopes, not raw worker traces by default.

## Deterministic Fan-Out / Fan-In

Use fan-out only when every partition is independent and the merge rule is deterministic. This Python 3.11+ example is provider-agnostic; replace the worker body with a model call that returns the declared result schema.

```python
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable


@dataclass(frozen=True)
class Result:
    item_id: str
    status: str
    value: str


async def run_partition(item_id: str) -> Result:
    # Replace with a bounded model/tool invocation.
    await asyncio.sleep(0)
    return Result(item_id=item_id, status="passed", value=item_id.upper())


async def run_all(
    item_ids: list[str],
    worker: Callable[[str], Awaitable[Result]],
    concurrency: int = 4,
) -> list[Result]:
    semaphore = asyncio.Semaphore(concurrency)

    async def guarded(item_id: str) -> Result:
        async with semaphore:
            return await worker(item_id)

    results = await asyncio.gather(*(guarded(item_id) for item_id in item_ids))
    failures = [result for result in results if result.status != "passed"]
    if failures:
        raise RuntimeError(f"partition failures: {[item.item_id for item in failures]}")
    return sorted(results, key=lambda result: result.item_id)


async def main() -> None:
    results = await run_all(["a", "b", "c"], run_partition, concurrency=2)
    print([result.value for result in results])


if __name__ == "__main__":
    asyncio.run(main())
```

The reducer must define how it handles duplicate claims, conflicting answers, missing partitions, and evaluator failure before work starts.

## Independent Evaluation

Use a generator/evaluator split when an output needs a quality or safety decision that the generator cannot certify itself.

| Step | Input | Output | Authority |
|---|---|---|---|
| Generate | Work contract and sources | Candidate artifact | Generator |
| Validate | Candidate plus frozen criteria | Pass/fail findings | Deterministic validator |
| Evaluate | Candidate, sources, criteria | Review verdict | Independently scoped evaluator |
| Decide | Validator/evaluator receipts | Publish, retry, or hold | Workflow controller |

The evaluator should not inherit the generator's private reasoning as its evidence. Give it the artifact, the accepted criteria, and the relevant primary sources. This reduces correlated failure; it does not guarantee correctness.

## Durable Workflow Boundary

Persist state before an external call and reconcile after a timeout.

```text
PENDING -> RUNNING -> VALIDATING -> PASSED
                    |               |
                    v               v
                 RETRYABLE        PUBLISHED
                    |
                    v
                 FAILED
```

Rules for the state machine:

- A controller, not a worker, owns terminal transitions.
- Each external call carries a stable idempotency key.
- A timeout is unknown, not failed. Query the external receipt before retrying.
- Publication requires a separate approval state when editorial or legal review is required.
- A restart resumes from the last persisted state and does not replay completed side effects.

## Cross-Service Agents

Use a cross-service protocol only when agents are independently deployed or owned. A2A provides an interoperability boundary for agent communication; MCP provides a host-managed boundary for tools and context. [A2A Protocol](https://a2a-protocol.org/latest/) [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

For agents inside one application, a typed internal API is usually simpler. Introduce a public protocol only after defining compatibility, authentication, discovery, timeout, and versioning rules.

## Roles Are Documentation, Not Architecture

Names such as researcher, reviewer, or coordinator are useful only when they map to a different contract:

- **Researcher:** read-only source access and citation-shaped output.
- **Reviewer:** no mutation authority and a pass/fail rubric.
- **Coordinator:** owns scheduling, budgets, and state transitions.
- **Publisher:** may write public output only after an approval receipt.

If two roles have the same tools, data, budget, and validator, merge them until a concrete separation is needed.

## Gotchas

- **Issue: Parallel workers edit the same record.** Last-writer-wins corruption can look like a successful merge. **Fix:** partition immutable inputs and give one reducer exclusive ownership of mutable output.
- **Issue: The evaluator is just the generator asked to praise or critique itself.** It inherits the same blind spots and may optimize for its own wording. **Fix:** use separate context, frozen criteria, and source-grounded checks.
- **Issue: A handoff loses who is responsible for the final answer.** The user sees a response but the system has no accountable owner. **Fix:** record the current owner, routing reason, and post-handoff completion rule.
- **Issue: A timeout is retried as a clean failure.** The first request may already have acted. **Fix:** reconcile by idempotency key or provider receipt before issuing another call.

## Limitations

Multi-agent systems increase cost, latency, and operational surface area. Parallelism improves throughput only for genuinely independent work. An extra agent cannot compensate for missing source authority, an unclear acceptance criterion, or a side effect without an idempotency contract.

## See Also

- [[agent-architectures]]
- [[agent-orchestration]]
- [[managed-agents]]
- [[multi-agent-messaging]]
- [[multi-session-coordination]]

## Sources

- [OpenAI Agents SDK: Agent Orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [A2A Protocol](https://a2a-protocol.org/latest/)
- [Model Context Protocol Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
