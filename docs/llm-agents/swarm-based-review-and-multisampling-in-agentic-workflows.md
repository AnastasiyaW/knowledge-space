---
title: "Independent Review and Multisampling for Agent Workflows"
description: "Generate independent candidates, validate evidence, and select agent outputs through explicit acceptance criteria rather than fixed vote counts or model confidence."
tags: [llm-agents, multisampling, review, evaluation, evidence]
---

# Independent Review and Multisampling for Agent Workflows

**Scope checked: 2026-09-04.** Multiple agent outputs can expose different failure modes, but neither a majority vote nor an agent's confidence is evidence that an output is correct. Treat multisampling as a bounded way to create competing candidates; treat review as a separate verification activity with a named acceptance contract.

## Start with a Task Contract

Before generating alternatives, record what “done” means for this task. A useful contract makes candidates comparable and prevents a review swarm from silently changing the request.

```yaml
task_id: payment-retry-001
source_revision: immutable repository revision
deliverable: patch and test receipt
acceptance:
  - named test command passes
  - retry is idempotent
  - no production mutation during evaluation
authority:
  - repository read and local test only
escalation:
  - missing credential, production target, or unclear owner
```

The contract should distinguish a desired answer from the evidence that can prove it. For a source-backed answer, the evidence may be current primary sources. For a code change, it may be a diff, deterministic tests, and an independent review. For an external action, it must include the approval and resulting receipt.

## Separate Candidates from Verification

| Role | Allowed work | Output | Cannot prove on its own |
|---|---|---|---|
| candidate generator | propose an answer or patch within the contract | candidate plus cited assumptions | that the proposal works |
| evidence collector | locate sources, run allowed checks, preserve receipts | evidence bundle | that evidence meets every acceptance criterion |
| verifier | compare the candidate and evidence to the contract | pass, fail, or bounded uncertainty | authority to change the target |
| selector | chooses a proven candidate or returns no decision | selection rationale | correctness without verifier evidence |

Independence should be designed around differing evidence paths, not theatrical role names. For example, one candidate can trace a data-flow boundary while another attempts the stated acceptance test. Giving every agent the same draft, tools, and unstated assumptions creates correlated errors even if the prompts differ.

## Choose an Aggregation Rule That Fits the Claim

| Claim type | Preferred rule | Why a vote is insufficient |
|---|---|---|
| deterministic calculation or code behavior | execute the named validator | the test result is stronger than consensus |
| factual, time-sensitive statement | require current primary-source citations | many agents can repeat an obsolete source |
| design choice | compare trade-offs against explicit constraints | there may be more than one acceptable answer |
| security concern | retain the union as triage, then confirm each finding | rare findings can be valuable, but unverified findings are not vulnerabilities |
| irreversible action | require the declared approval and a side-effect receipt | agreement does not grant authority |

A selector may return “no candidate proven.” That is a healthy outcome when evidence is missing, the contract is ambiguous, or the allowed tools cannot inspect the relevant boundary.

## Bounded Multisampling Loop

1. Freeze the task contract, input revision, tool policy, and stopping condition.
2. Generate independent candidates that vary an evidence perspective or implementation approach.
3. Run deterministic validation before asking a model to judge prose about validation.
4. Send only the candidate and evidence bundle needed for a blind verifier to apply the contract.
5. Select a candidate only when its required evidence is present; otherwise record the gap and escalate or stop.

Set a budget in terms that operators can observe: allowed candidates, time, tool calls, or cost. Stop early when every criterion is proven, and stop at the budget boundary when it is not. Do not silently increase the sample count until a preferred answer wins.

## Evidence Record

Keep enough information for a later reviewer to reproduce the decision:

- task and candidate identifiers;
- source revision, configuration version, and input fixture;
- exact validation commands and exit results;
- source URLs or artifact digests;
- denied tools, approvals, and external side-effect receipts;
- selection rationale and unresolved uncertainty.

This record turns an agent ensemble into an auditable workflow. It also makes regression evaluation possible: a future run can use the same contract and disclose which input, tool, or source changed.

## Security Reviews Need Confirmation

Security-oriented agents may cast a wide net, but their output is a lead, not a release decision. Preserve the finding, affected revision, proposed trigger path, and evidence needed to reproduce it. Confirm through the safest available method—code inspection, a controlled test fixture, or an authorized environment—before labeling it a vulnerability or changing a production system. Avoid granting a review agent extra network, credential, or deployment authority merely to make its result look conclusive.

## Common Failure Modes

- **Majority as proof:** agreement can amplify a shared false premise.
- **Shared mutable scratchpad:** later candidates imitate the first candidate instead of testing it.
- **Unbounded debate:** more messages replace a missing acceptance test.
- **Blind trust in confidence scores:** confidence is not a calibrated correctness guarantee.
- **Security “union” shipped as fact:** triage findings require confirmation and owner review.
- **Lost provenance:** without a revision, fixture, and receipt, a future result cannot be compared honestly.

## References

- [OpenAI Evals documentation](https://platform.openai.com/docs/guides/evals) — evaluation definitions, runs, and graders.
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — a risk-management framing for generative-AI systems.
- [Claude Code subagents](https://code.claude.com/docs/en/subagents) — current documentation for scoped subagent definitions and delegated work.
