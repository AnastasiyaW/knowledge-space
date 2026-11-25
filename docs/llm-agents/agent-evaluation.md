---
title: "Agent Evaluation and Evidence"
description: "Evaluate agent behavior with versioned task fixtures, deterministic validators, controlled side-effect checks, and reproducible evidence rather than a single benchmark score."
tags: [llm-agents, evaluation, testing, benchmarks, evidence, swe-bench]
---

# Agent Evaluation and Evidence

**Scope checked: 2026-09-06.** An agent run combines a model with instructions, tools, state, data, permissions, and an execution environment. A benchmark result can be useful evidence about one defined harness; it does not prove that a production integration is safe, current, or suitable for a different task.

## Define the Evaluation Object

State exactly what is being evaluated before comparing results:

- task fixture and immutable input revision;
- agent instructions, model configuration, and tool versions;
- available authority, data scope, and environment;
- expected outcome and prohibited side effects;
- validator order and the release decision that the result may support.

A reproducible evaluation record binds those facts together.

```json
{
  "run_id": "support-triage-2026-09-04-a",
  "source_revision": "immutable commit or content digest",
  "fixture_revision": "versioned test data",
  "agent_configuration": "policy and tool configuration digest",
  "authority": "local test only",
  "validators": ["schema", "unit", "sandboxed integration"],
  "result": "pass | fail | blocked",
  "evidence": ["test output", "external receipt if applicable"]
}
```

Do not reuse an old run identifier after changing the fixture, source revision, environment, or configuration. It makes cache reuse and historical comparison ambiguous.

## Evaluate More Than Task Completion

| Dimension | Question | Strongest practical evidence |
|---|---|---|
| functional outcome | did the task meet its acceptance criteria? | deterministic test or validated artifact |
| quality | is the answer accurate, complete, and usable for its audience? | rubric with calibrated human or model-judge review |
| safety and side effects | did the run avoid prohibited access or mutations? | capability log, sandbox record, and external receipts |
| authority | did the agent stay within allowed tools, data, and approvals? | effective policy plus tool-call audit |
| operational behavior | were retries, timeouts, and resource use within the declared budget? | structured run telemetry |
| reproducibility | can a reviewer re-run or inspect the same conditions? | versioned fixture, configuration, and retained evidence |

The correct metric follows the task contract. A low tool-call count is not inherently better if it skips validation; a fast successful response is not a safe production action without the required receipt.

## Validator Order

Run the cheapest, most deterministic checks first and only then use subjective judgment:

1. validate schemas, permissions, and static constraints;
2. execute unit or fixture tests in a controlled environment;
3. run authorized integration checks against isolated or reversible targets;
4. inspect external state and preserve receipts where an action is permitted;
5. use calibrated human review or model judges for qualities a deterministic test cannot decide.

Generated code and tool calls should not receive unrestricted local or production authority merely to simplify evaluation. Use the smallest sandbox or test fixture that can establish the relevant behavior. A failure to observe an external condition is a blocked or incomplete result, not an automatic pass.

## Stochastic Runs Need Transparent Reporting

When an agent samples nondeterministically, retain every run result and report the distribution relevant to the decision: success/failure counts, variance in cost or latency, error categories, and any observed side effects. Use a fixed task set for comparisons, keep a holdout set for regression checks, and disclose configuration changes.

Choose repeat count and budget from the risk, expected variance, and cost of a wrong decision. There is no universal sample count that turns an agent result into proof. If a release needs a confidence bound, define it in the evaluation plan before running the experiment.

## Benchmarks Are Harnesses, Not Production Certificates

[SWE-bench](https://github.com/SWE-bench/SWE-bench) evaluates software-engineering tasks through a specific dataset and execution harness. Its current command-line tooling records a run identifier and can skip instances that already have a report for that run. Treat the run ID, task subset, environment, and harness version as part of the result identity; otherwise a cached result can be mistaken for a fresh evaluation. [SWE-bench CLI reference](https://www.swebench.com/SWE-bench/reference/cli/)

A benchmark can reveal a regression or compare a defined system to its prior version. It cannot demonstrate that a repository's tests pass, that an organization's credentials are protected, or that an external deployment behaved correctly. Preserve those as separate proof cells.

## Release Gate

A release decision should name the evidence required for its risk level:

| Change class | Minimum evidence |
|---|---|
| text or local non-executable change | link/build validation and editorial review |
| code change without external effects | relevant automated tests, diff review, and source revision |
| integration with reversible test target | controlled integration receipt and failure-path check |
| external or production effect | explicit authority, idempotency/rollback plan, fresh target receipt, and independent review |

A single aggregate score is a dashboard signal, not a replacement for the individual gate that protects a user, database, payment, deployment, or published claim.

## Match the Completion Claim to the Evidence

Use separate proof levels instead of one undifferentiated `PASS`. The following is an engineering reporting convention, not an SDK status taxonomy.

| Observed level | What it establishes | What remains unproven |
|---|---|---|
| source review | the inspected revision contains the intended instruction or implementation | whether any active system loads it |
| focused fixture | the named inputs and assertions passed in the recorded environment | behavior outside those cases or in another runtime |
| installation and registration | expected bytes are installed and the active entry point selects them | whether a real invocation reaches the changed branch |
| consuming workflow | the requested user path produced its specified result in the named environment | unrelated paths, versions, workloads, and quality dimensions |

The required level follows the request. Reviewing an instruction file may complete a source audit. It does not complete a request to install that instruction and demonstrate its effect. A test double can prove a local interaction contract; it cannot establish that the real service accepted a request. Retain the input, revision, assertion, actual observation, and supported claim together.

Registration itself can hide reachability gaps. In the OpenAI Agents SDK for TypeScript, input guardrails apply to the first agent, output guardrails to the final output, and tool guardrails to supported function-tool calls. Input checks can run concurrently with the agent. Consequently, seeing a guardrail in configuration does not establish that it ran before every side effect. Verify the actual path and execution mode. [SDK guardrail scope and execution](https://openai.github.io/openai-agents-js/guides/guardrails/)

## Continue Until the Accepted Outcome, Not Until the Next Report

A useful completion contract connects the requested result to the next executable action and its acceptance evidence. A finding, review, handoff, or failed attempt changes that state; it does not automatically close the task.

| Current observation | Action within the existing task and authority | Terminal evidence |
|---|---|---|
| reproducible local implementation defect | make a causal correction, then re-run the affected check | corrected behavior on the failing case and relevant controls |
| work completed in a branch but not installed | finish the requested delivery through the established route | source revision, installation result, and required consumer check |
| process exited without a final result | reconcile partial effects before an idempotent repair or resume | complete output or an evidenced boundary that prevents continuation |
| required approval or external dependency is genuinely unavailable | preserve partial work and identify the exact pending decision or recheck | observed refusal, pending approval, or dependency response |
| all accepted criteria have sufficient evidence | close the task | criterion-to-evidence mapping, with proof limits stated |

This is an operating policy derived from separating task state from agent messages. It is not a mandate to retry indefinitely or expand authority. A failed local test is not, by itself, an external blocker. Conversely, a completion objective does not authorize deletion, a new publication destination, or an unapproved production mutation.

The SDK supports both model-directed orchestration and explicit code control flow. A deterministic state transition is appropriate when the next action follows a known condition; language-model judgment is still useful for diagnosis. When a tool really requires approval, the human-in-the-loop mechanism preserves the interrupted run for an explicit approval or rejection rather than treating the tool as executed. [Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/), [approval and resume](https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

Do not compensate for premature stopping with compulsory extra review rounds. Repeat checks because a failed criterion, changed dependency, or newly observed material risk invalidates their earlier evidence. Preserve still-valid results for unchanged areas. Stop expanding once the entire accepted scope is satisfied; optional polishing is a separate decision. For concurrent work, bind each result to its owner and revision: [[multi-session-coordination]], [[swarm-based-review-and-multisampling-in-agentic-workflows]].

## Gotchas

- **Benchmark substitution:** treating a score as proof of an unrelated production workflow.
- **Mutable fixtures:** results cannot be compared because the task data changed silently.
- **Cache ambiguity:** reusing a run identifier across different code or configurations.
- **Judge-only acceptance:** a model declares success without deterministic or external evidence.
- **Unsafe evaluation:** generated code receives network, credential, or production access without a bounded test target.
- **Average-only reporting:** rare failures and costly outliers disappear behind a summary number.
- **Report-as-result:** a finding or successful review is recorded as terminal even though the requested installation or user workflow is still missing.
- **Installation-as-execution:** matching installed hashes is presented as proof that a live request exercised the changed behavior.
- **Review self-feed:** a passed review triggers another generic review without a changed risk, leaving the accepted delivery unfinished.

## Limitations

These conventions organize evidence; they do not prove that an acceptance criterion is sufficient or that an automated judge is correct. Visual quality, domain validity, and infrequent failures can require different measurements. A bounded observation cannot establish universal absence of failures. Keep untested conditions explicit rather than turning either uncertainty or a local green check into a claim about the whole product.

## References

- [OpenAI Evals documentation](https://platform.openai.com/docs/guides/evals) — current concepts for evaluation definitions, runs, and graders.
- [SWE-bench repository](https://github.com/SWE-bench/SWE-bench) and [CLI reference](https://www.swebench.com/SWE-bench/reference/cli/) — benchmark and run-artifact behavior.
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — risk framing for generative-AI evaluation.
