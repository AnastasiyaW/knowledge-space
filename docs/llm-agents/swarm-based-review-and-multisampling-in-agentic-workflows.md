# Swarm-Based Review and Multisampling in Agentic Workflows

Multisampling and swarm-based review are techniques used to scale LLM reasoning performance at inference time. These methods leverage diverse sampling, specialized agent personas, and iterative review cycles to surface edge cases that single-pass generation typically misses.

## Multisampling and Diversity Scaling
Multisampling (Best-of-N) relies on the principle that multiple independent reasoning paths increase the probability of hitting a correct solution.

- **Diversity over Identity:** Using diverse prompts (different phrasing or personas) for the same task outperforms identical prompt sampling. Diverse prompting shows gains of +10.8% in reasoning and +9.5% in coding tasks [2502.11027].
- **Scaling Law (N=4 to N=16):** The most significant performance gains occur between n=4 and n=16. Beyond n=16, returns diminish rapidly. Best-of-8 strategies can achieve a ~22% speedup in reaching a target accuracy threshold [2502.12668].
- **Self-Consistency:** A foundational pattern where the model generates multiple Chain-of-Thought (CoT) paths followed by a majority vote on the final answer [2203.11171].

### Confidence-Weighted Self-Consistency (CISC)
CISC optimizes token usage by weighting samples based on model confidence, reducing the number of required samples by up to 46% while maintaining accuracy.

## Swarm Review Architecture (Plan Swarming)
Swarm review involves an iterative, multi-round process where specialized agents audit a plan or code snippet. Each round unmasks deeper issues as earlier ones are resolved.

- **Round 1 (Baseline):** A single agent identifies surface-level issues (e.g., 10-12 findings).
- **Round 2 (Multisampling):** Multiple parallel agents with diverse personas identify unique edge cases.
- **Round 3 (Aspect Focusing):** Agents are assigned specific domains (security, performance, style).
- **Round 4 (Deep Audit):** High-N multisampling (e.g., 25+ runs) focused on specific medium-to-high risk areas.

### Parallel Specialized Agents
In production code review environments, using parallel specialized agents increases substantive findings from 16% to 54%. Large pull requests (>1000 lines) see a significant boost in recall (up to 84%) using this pattern.

## Aggregation and Selection Mechanisms
Majority voting is effective for consensus but often discards "minority-correct" findings—unique, high-value catches made by only one agent in the swarm.

- **Reasoning Tree Audit:** Instead of voting on the final answer, a "Judge" agent audits the reasoning steps. This can recover 65-82% of correct findings that are in the minority [2602.09341].
- **Voting vs. Debate:** Simple voting is often as effective as full multi-agent debate (MAD) while being significantly cheaper. Debate acts as a martingale and does not always improve expected correctness [2508.17536].
- **Union Voting for Security:** In vulnerability detection, the union of all agent findings is preferred over consensus to maximize recall, even if it increases false positives.

## Specialized Vulnerability Detection Pipelines
Modern pipelines for security and correctness use multi-level stages to identify complex logic flaws.

- **Hypothesis-Validation Pattern:** 
    1. Identify a sensitive operation.
    2. Generate a hypothesis for a vulnerability.
    3. Construct a trigger path.
    4. Verify via execution or symbolic audit.
- **Multi-Level Pipeline (MultiVer):** Uses specialized agents for security, performance, and correctness. This approach achieves ~82.7% recall, outperforming many fine-tuned static models [2602.17875].
- **Coarse-to-Fine Routing:** A router agent directs code to specific detector agents, followed by cross-model prompt evolution where one model (e.g., Claude) generates prompts and another (e.g., GPT-4o) evaluates their effectiveness [2601.18847].

## Gotchas
- **Consensus Bias:** Majority voting (Self-Consistency) naturally suppresses rare but correct edge-case detections. In security contexts, strictly following the majority leads to critical misses.
- **Diminishing Returns:** Attempting to scale N beyond 16-32 without changing the prompt diversity or agent personas usually results in wasted tokens for negligible accuracy gains.
- **Unmasking Effect:** Fixing issues identified in Round 1 of a swarm review often changes the context enough to "unmask" bugs that were previously hidden or ignored by the LLM.

## See Also
- [[agent-orchestration]]
- [[agent-design-patterns]]
- [[multi-agent-systems]]
- [[agent-evaluation]]
- [[agent-memory]]

