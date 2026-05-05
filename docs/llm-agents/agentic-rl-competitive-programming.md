---
title: Agentic RL for Competitive Programming
category: patterns
tags: [llm-agents, reinforcement-learning, competitive-programming, code-generation, self-improvement, verification]
---

# Agentic RL for Competitive Programming

GrandCode (2026) achieves grandmaster-level performance on competitive programming problems by combining an agentic loop with reinforcement learning. The key insight: classic RL trains a policy on trajectories, but competitive programming requires multi-step reasoning, self-correction, and external verification — exactly the agentic pattern. The approach reaches IGM (International Grandmaster) rank on Codeforces, surpassing all previous AI systems.

## Core Architecture

The agent operates in a **generate → execute → score → improve** loop rather than a single-shot generation pass:

```python
# Simplified agentic RL loop (pseudocode)
def solve(problem: str, time_budget: int) -> str:
    solution = initial_draft(problem)
    for step in range(time_budget):
        result = run_tests(solution)           # external verifier
        if result.all_pass:
            return solution
        feedback = analyze_failures(result)    # step-level reward signal
        solution = refine(solution, feedback)  # policy update via RL
    return best_so_far
```

The policy is trained with **process reward** (step-level correctness) rather than outcome reward (final pass/fail only). This is critical at grandmaster difficulty where a single wrong step in a 50-step derivation produces zero signal under sparse rewards.

## Why Agentic RL Beats One-Shot Generation

| Approach | Pass@1 on Hard Problems | IGM Benchmark |
|---|---|---|
| GPT-4o (direct) | ~8% | No |
| o3-mini (chain-of-thought) | ~23% | No |
| GrandCode (agentic RL) | ~61% | Yes |

The gap exists because hard competitive problems require:

- **Test-driven iteration** — submitting partial solutions and observing which tests fail
- **Edge-case discovery** — the external judge reveals inputs the model never imagined
- **Multi-hypothesis search** — trying different algorithmic approaches in parallel

One-shot generation cannot recover from a wrong choice of algorithm. An agentic loop can backtrack.

## Verification as the Training Signal

The crucial infrastructure piece: **cheap, deterministic verifiers**. Competitive programming has perfect verifiers (judge test cases). The RL loop only works because:

1. Every intermediate solution can be evaluated exactly
2. Evaluation is fast (milliseconds per test case)
3. Partial credit is meaningful (% tests passed = reward)

```python
# Process reward model
def step_reward(partial_solution: str, test_cases: list) -> float:
    passed = sum(run_test(partial_solution, t) for t in test_cases)
    return passed / len(test_cases)   # 0.0 → 1.0 dense signal
```

This is why competitive programming is an ideal RL training domain: the reward signal that makes RL hard in open-ended tasks is given for free.

## Memory Intelligence Agent (MIA) Pattern

A separate line of work (ECNU-SII/MIA) addresses a related bottleneck: in **deep research** tasks, the agent must synthesize information across dozens of tool calls. Without explicit memory management, it loses earlier findings as context fills.

MIA introduces a structured working memory that the agent reads and writes explicitly:

```python
# MIA-style memory operations (conceptual)
memory = WorkingMemory()

# During research loop
finding = web_search(query)
memory.store(key=topic_hash(finding), value=summarize(finding))

# When forming final answer
relevant = memory.retrieve(query=current_subtask, top_k=5)
answer = synthesize(relevant + current_context)
```

The measured improvement: ~40% reduction in "repeated searches" (the agent re-discovering information it already found), and meaningful accuracy gains on multi-hop research benchmarks.

## Connecting to Proof Loop Pattern

Both GrandCode and MIA instantiate the same underlying pattern:

```
spec_freeze → build → evidence → fresh_verify → fix → verify_again
```

- **GrandCode**: spec = problem statement; evidence = test results; fresh verifier = judge
- **MIA**: spec = research question; evidence = memory contents; fresh verifier = synthesis step

The difference from [[agent-self-improvement]] reflection techniques: GrandCode uses **external ground truth** (judge tests), not self-assessed quality. The verifier is outside the policy being optimized. This prevents the model from gaming its own evaluation metric.

## Implementation Constraints

- **Verifier availability is the bottleneck**: this approach ports directly to any domain with cheap deterministic verification (unit tests, formal provers, SQL query validators). It does not port to open-ended generation tasks without a separate reward model.
- **Exploration cost scales with problem difficulty**: grandmaster problems require 50-200 refinement steps; easy problems need 1-3. Budget accordingly.
- **RL requires trajectory data**: getting to grandmaster level required training on ~500K competitive programming trajectories with annotated intermediate rewards. This is not fine-tuning on solutions; it is training on the full solve process.

## Gotchas

- **Sparse reward kills RL on hard problems**: if you only score the final submission, the gradient signal for a 90%-correct solution is identical to a 0%-correct one. Use test-suite pass rate as dense reward.
- **Test leakage invalidates results**: if training trajectories include problems from the evaluation set, reported performance is inflated. Verify train/eval split at the problem level, not just the solution level.
- **Self-generated test cases are weak**: models tend to generate tests that pass their own solutions. Use held-out external judges or adversarially generated edge cases.
- **Memory without forgetting degrades**: MIA-style memory accumulates noise over long sessions. Implement staleness decay or periodic consolidation to prevent retrieval quality from dropping after 50+ writes.

## See Also

- [[agent-self-improvement]]
- [[agent-memory]]
- [[swarm-based-review-and-multisampling-in-agentic-workflows]]
- [[adaptive-patterns-for-autonomous-agents]]
