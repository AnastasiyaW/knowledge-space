---
title: Agent Evaluation and Benchmarks
category: concepts
tags: [llm-agents, evaluation, benchmarks, testing, metrics, swe-bench]
---

# Agent Evaluation and Benchmarks

Evaluating agents is fundamentally harder than evaluating models. Agents have stochastic behavior, multi-step execution, tool interactions, and real-world side effects. A model that scores 90% on a benchmark may produce a 50% success rate agent.

## Evaluation Dimensions

### Task Completion

Binary: did the agent accomplish the goal?

```python
def evaluate_task_completion(agent, test_cases):
    results = []
    for case in test_cases:
        output = agent.run(case["input"])
        success = case["validator"](output)
        results.append({
            "task": case["name"],
            "success": success,
            "steps": output.step_count,
            "cost": output.total_cost,
            "time": output.elapsed_seconds,
        })

    pass_rate = sum(r["success"] for r in results) / len(results)
    avg_cost = sum(r["cost"] for r in results) / len(results)
    return {"pass_rate": pass_rate, "avg_cost": avg_cost, "results": results}
```

### Efficiency Metrics

- **Steps to completion**: fewer is better (less cost, less room for error)
- **Tool calls**: unnecessary tool calls waste tokens and time
- **Token usage**: total input + output tokens consumed
- **Wall clock time**: end-to-end latency
- **Cost**: total API spend per task

### Quality Metrics

- **Correctness**: output matches expected result
- **Completeness**: all parts of the task addressed
- **Safety**: no harmful actions taken
- **Robustness**: handles edge cases and errors gracefully

## Benchmark Suites

### SWE-Bench

Real GitHub issues resolved by agents. Gold standard for coding agents.

- **SWE-Bench Lite**: 300 issues, more tractable
- **SWE-Bench Verified**: human-verified subset
- Metric: % of issues resolved (patch applies + tests pass)
- Current SOTA: ~50% on Verified (as of early 2026)

### GAIA

General AI Assistants benchmark. Multi-step reasoning with tool use.

- 3 difficulty levels
- Requires web search, file reading, code execution
- Tests compositional reasoning across tools

### HumanEval / MBPP

Code generation benchmarks. Simpler than SWE-Bench (function-level, not repo-level).

### WebArena / VisualWebArena

Web navigation benchmarks. Agent completes tasks in real websites.

### AgentBench

Multi-environment benchmark: OS, database, web, game environments.

## Building Custom Evals

### Deterministic Validators

```python
# Exact match
def validate_exact(output, expected):
    return output.strip() == expected.strip()

# Contains required elements
def validate_contains(output, required_elements):
    return all(elem in output for elem in required_elements)

# Code execution test
def validate_code(output, test_cases):
    exec_env = {}
    try:
        exec(output, exec_env)
        for inp, expected_out in test_cases:
            assert exec_env["solution"](inp) == expected_out
        return True
    except (AssertionError, Exception):
        return False
```

### LLM-as-Judge

When deterministic validation is impossible:

```python
def llm_judge(task, agent_output, rubric):
    prompt = f"""
    Task: {task}
    Agent output: {agent_output}

    Evaluate on this rubric (1-5 scale for each):
    {rubric}

    Return JSON: {{"scores": {{"criterion": score}}, "explanation": "..."}}
    """
    judgment = judge_llm(prompt)
    return json.loads(judgment)

# Calibration: always include anchor examples
rubric = """
1. Correctness (1-5): Does the answer match the expected outcome?
   1 = completely wrong, 3 = partially correct, 5 = fully correct
2. Efficiency (1-5): Did the agent use minimal steps?
   1 = excessive tool calls, 3 = reasonable, 5 = optimal path
3. Safety (1-5): Were any dangerous actions taken?
   1 = destructive action, 3 = minor risk, 5 = completely safe
"""
```

### Trajectory Evaluation

Evaluate the process, not just the outcome:

```python
def evaluate_trajectory(trajectory):
    scores = {
        "redundant_calls": count_redundant_tool_calls(trajectory),
        "error_recovery": count_successful_recoveries(trajectory),
        "planning_quality": judge_plan_coherence(trajectory),
        "tool_selection_accuracy": correct_tools / total_tools,
    }
    return scores

def count_redundant_tool_calls(trajectory):
    """Detect repeated identical tool calls."""
    seen = set()
    redundant = 0
    for step in trajectory:
        key = (step.tool, frozenset(step.params.items()))
        if key in seen:
            redundant += 1
        seen.add(key)
    return redundant
```

## Statistical Rigor

```python
import numpy as np
from scipy import stats

# Confidence intervals for pass rate
def pass_rate_ci(successes, total, confidence=0.95):
    p = successes / total
    z = stats.norm.ppf((1 + confidence) / 2)
    margin = z * np.sqrt(p * (1-p) / total)
    return (p - margin, p + margin)

# Comparing two agents: paired bootstrap test
def compare_agents(scores_a, scores_b, n_bootstrap=10000):
    diffs = np.array(scores_a) - np.array(scores_b)
    boot_means = [np.mean(np.random.choice(diffs, len(diffs))) for _ in range(n_bootstrap)]
    p_value = np.mean(np.array(boot_means) <= 0)
    return {"mean_diff": np.mean(diffs), "p_value": p_value}
```

**Minimum sample sizes**: 100 test cases for rough estimates, 300+ for reliable comparisons between agents. Single-digit differences on < 50 cases are noise.

## Regression Testing

```python
# Track performance over agent versions
def regression_check(current_results, baseline_results, threshold=0.05):
    current_rate = sum(r["success"] for r in current_results) / len(current_results)
    baseline_rate = sum(r["success"] for r in baseline_results) / len(baseline_results)

    regression = baseline_rate - current_rate
    if regression > threshold:
        failing_cases = [
            r["task"] for r, b in zip(current_results, baseline_results)
            if b["success"] and not r["success"]
        ]
        return {"regression": True, "drop": regression, "failing_cases": failing_cases}
    return {"regression": False}
```

## Gotchas

- **LLM-as-judge is biased**: judges favor verbose outputs, outputs matching their own style, and outputs presented first in A/B comparisons. Calibrate with human annotations, randomize presentation order, and use multiple judge models for critical evaluations
- **Benchmark contamination**: if agent training data includes benchmark solutions, scores are inflated. Use held-out test cases, time-gated benchmarks (only issues after training cutoff), or create custom evals from your own production data
- **Non-determinism makes comparison hard**: same agent on same task can succeed or fail depending on LLM sampling. Run each test case 3-5 times and report mean + variance. A single pass/fail result is unreliable for agent comparison

## See Also

- [[agent-design-patterns]]
- [[llmops]]
- [[production-patterns]]
- [[agent-self-improvement]] - Using evaluation signals for agent self-improvement
- [[token-optimization]] - Efficiency metrics and token budget management
