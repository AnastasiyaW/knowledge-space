---
title: Agent Self-Improvement
category: patterns
tags: [llm-agents, self-improvement, reflection, reward-shaping, learning-from-mistakes, autoresearch]
---

# Agent Self-Improvement

Techniques for agents to improve their own performance through reflection, step-level reward signals, and code self-modification - without gradient-based training. Three approaches: runtime reflection (improve during task), trajectory learning (improve between tasks), and code self-modification (improve the agent itself).

## Step-Level Reward Shaping

### The Sparse Reward Problem

Standard agent training provides reward only at trajectory end (task success/failure). This makes credit assignment hard - which specific step caused the failure?

```
Step 1: Search docs       -> ?
Step 2: Parse results     -> ?
Step 3: Write wrong query -> ?  (actual mistake)
Step 4: Get bad results   -> ?
Step 5: Wrong answer      -> Reward: 0  (only signal)
```

**Step-level rewards** assign credit to individual actions:

```
Step 1: Search docs       -> +0.1 (useful action)
Step 2: Parse results     -> +0.1 (correct parsing)
Step 3: Write wrong query -> -0.3 (identified as error)
Step 4: Get bad results   -> -0.1 (wasted compute)
Step 5: Wrong answer      -> -0.2 (final failure)
```

### Constructing Step-Level Rewards from Trajectories

Given a failed trajectory `T_fail` and a successful trajectory `T_success` for the same task, identify the divergence point:

```python
def find_divergence(t_fail: list[Step], t_success: list[Step]) -> int:
    """Find first step where trajectories meaningfully diverge."""
    for i, (sf, ss) in enumerate(zip(t_fail, t_success)):
        if sf.action_type != ss.action_type or sf.target != ss.target:
            return i
    return min(len(t_fail), len(t_success))

def construct_step_rewards(t_fail: list[Step], t_success: list[Step]) -> list[float]:
    """Assign per-step rewards based on trajectory comparison."""
    div = find_divergence(t_fail, t_success)
    rewards = []
    for i, step in enumerate(t_fail):
        if i < div:
            rewards.append(0.0)       # shared prefix - neutral
        elif i == div:
            rewards.append(-1.0)      # divergence point - mistake
        else:
            rewards.append(-0.1)      # cascading from mistake
    return rewards
```

### MCTS-Inspired Exploration for Error Recovery

Use tree search to find recovery paths from mistakes:

```python
def explore_alternatives(state_at_step: State, budget: int = 5) -> list[Trajectory]:
    """Generate alternative continuations from a given state."""
    alternatives = []
    for _ in range(budget):
        # Roll out from the state with temperature > 0 for diversity
        traj = agent.rollout(state_at_step, temperature=0.8)
        alternatives.append(traj)
    return sorted(alternatives, key=lambda t: t.final_reward, reverse=True)
```

When a trajectory fails at step N, rewind to step N-1 and explore `budget` alternative continuations. The best alternative becomes a positive training signal; the original becomes a negative one.

## Reflection-Based Self-Improvement

### Post-Task Reflection

After each task attempt, the agent writes a structured reflection:

```
## Reflection on Task #{n}
Result: FAIL (score: 0.3)

### What went wrong
- Step 3: searched with overly broad query, got irrelevant results
- Step 5: attempted to answer without sufficient context

### What to do differently
- Use more specific search queries with exact error messages
- If first search returns < 3 relevant results, reformulate before proceeding

### Pattern to remember
When debugging errors: search for EXACT error message first, not general topic
```

### Reflection -> Code Modification Loop

The most powerful form: agent edits its own source code based on reflection:

```python
def self_improve_cycle(agent_code_path: str, benchmark: list[Task], iterations: int = 10):
    """Agent improves its own code through reflection."""
    for i in range(iterations):
        # 1. Run benchmark
        results = run_benchmark(agent_code_path, benchmark)
        score = results["pass_rate"]

        # 2. Analyze failures
        failures = [r for r in results["details"] if not r["success"]]
        failure_analysis = analyze_failures(failures)

        # 3. Generate reflection
        reflection = generate_reflection(
            current_score=score,
            failure_patterns=failure_analysis,
            agent_code=read_file(agent_code_path),
        )

        # 4. Propose code edit
        proposed_edit = propose_improvement(reflection, agent_code_path)

        # 5. Apply edit and re-test
        apply_edit(agent_code_path, proposed_edit)
        new_results = run_benchmark(agent_code_path, benchmark)
        new_score = new_results["pass_rate"]

        # 6. Keep or revert
        if new_score > score:
            git_commit(f"improvement: {score:.1%} -> {new_score:.1%}")
        else:
            git_revert()
```

Results from research: this pattern achieves 17% -> 53% on SWE-Bench Verified without any gradient training. The key is measuring improvement mechanically (test results) rather than relying on the agent's self-assessment.

## Trajectory Collection and Training

### Building a Training Set from Agent Runs

```python
def collect_training_pairs(task_pool: list[Task], agent, n_attempts: int = 3):
    """Run each task multiple times, extract success/failure pairs."""
    pairs = []
    for task in task_pool:
        trajectories = []
        for _ in range(n_attempts):
            traj = agent.run(task)
            trajectories.append(traj)

        successes = [t for t in trajectories if t.success]
        failures = [t for t in trajectories if not t.success]

        for fail in failures:
            if successes:
                # Pair with most similar successful trajectory
                best_match = min(successes, key=lambda s: trajectory_distance(fail, s))
                pairs.append((fail, best_match))
    return pairs
```

### Preference Learning from Trajectories

Step-level reward pairs can train the agent via DPO (Direct Preference Optimization) or similar:

```python
# For each divergence point, create a preference pair:
# preferred = successful step at divergence
# dispreferred = failed step at divergence
preference_data = []
for t_fail, t_success in training_pairs:
    div = find_divergence(t_fail, t_success)
    if div < len(t_fail) and div < len(t_success):
        preference_data.append({
            "context": t_fail[:div],  # shared prefix
            "preferred": t_success[div],  # correct next step
            "dispreferred": t_fail[div],  # wrong next step
        })
```

## Practical Self-Improvement Without Training

For prompt-based agents (no fine-tuning access), accumulate learnings in persistent memory:

```markdown
<!-- .agent/learnings.md - updated after each session -->

## Error Patterns (auto-extracted)
1. **Broad search queries**: 73% of search failures use < 3 keywords. Fix: always include exact identifiers
2. **Missing validation**: 45% of code generation failures lack input validation. Fix: add validation step
3. **Premature answers**: 28% of failures attempt to answer before gathering enough context. Fix: require 3+ sources

## Successful Strategies
1. **Error message search**: searching exact error text succeeds 89% of the time vs 34% for paraphrased
2. **Test-first approach**: writing test before implementation succeeds 71% vs 52% for code-first
```

This file is injected into the system prompt at session start. Over time, the agent accumulates domain-specific heuristics.

## Gotchas

- **Self-assessment bias**: agents rate their own outputs higher than warranted. Always use mechanical verification (tests, benchmarks, external evaluators) rather than asking the agent "did you do well?" Research shows agents claim success on failed tasks ~40% of the time
- **Improvement plateaus are real**: the reflection-edit loop typically plateaus after 10-20 iterations on a fixed benchmark. At that point, either change the benchmark, increase diversity of exploration, or switch to a different improvement strategy
- **Reverting is as important as improving**: without strict revert-on-regression, agents accumulate harmful changes that individually look neutral but collectively degrade performance. Always compare against the last-known-good checkpoint, not just the previous iteration
- **Step-level rewards require trajectory diversity**: if all attempts fail the same way, there are no divergence points to learn from. Ensure exploration diversity through temperature variation, different initial prompts, or multiple agent configurations

## See Also

- [[autonomous-agent-evolution]] - Multi-agent parallel evolution with shared knowledge
- [[agent-evaluation]] - Benchmarks and metrics for measuring improvement
- [[agent-design-patterns]] - Reflexion pattern as foundation for self-critique
- [[prompt-engineering]] - Prompt-level optimization techniques
- [[production-patterns]] - Deploying self-improving agents safely
