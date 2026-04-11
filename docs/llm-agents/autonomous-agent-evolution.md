---
title: Autonomous Agent Evolution
category: patterns
tags: [llm-agents, multi-agent, evolution, workspace-isolation, shared-knowledge, heartbeat, self-improvement]
---

# Autonomous Agent Evolution

Replacing fixed evolutionary search (agents as stateless workers) with long-lived autonomous agents that control the entire search process: what to retrieve, when to evaluate, what to retain. Key innovation: workspace isolation + shared knowledge layer + periodic reflection.

## Core Architecture

### Isolated Workspaces

Each agent operates in a separate workspace (git worktree, container, or directory) to prevent interference. Agents can run different experiments in parallel without merge conflicts.

```
agent-0/          # git worktree for agent 0
agent-1/          # git worktree for agent 1
agent-2/          # git worktree for agent 2
.shared/          # shared knowledge (symlinked into each workspace)
  attempts/       # historical evaluations indexed by commit hash
  notes/          # markdown observations (hierarchical)
  skills/         # reusable procedures and scripts
```

```bash
# Setup per-agent worktrees from a base repo
git worktree add agent-0 -b agent-0-branch
git worktree add agent-1 -b agent-1-branch
# Symlink shared knowledge into each
ln -s $(pwd)/.shared agent-0/.shared
ln -s $(pwd)/.shared agent-1/.shared
```

**Why worktrees over branches**: agents need simultaneous filesystem access. Branch switching would serialize work. Worktrees give each agent a full working copy while sharing the git object store.

### Shared Knowledge Layer

Three artifact types, all readable by every agent:

| Artifact | Format | Purpose |
|----------|--------|---------|
| `attempts/` | `{commit-hash}.json` with score + metadata | Prevent re-evaluation of identical solutions |
| `notes/` | Hierarchical markdown files | Observations, patterns, failed approaches |
| `skills/` | Executable scripts + markdown docs | Reusable procedures discovered during search |

```json
// .shared/attempts/a3f2b1c.json
{
  "commit": "a3f2b1c",
  "agent": 2,
  "score": 0.3809,
  "approach": "greedy interval optimization with symmetry breaking",
  "timestamp": "2026-04-01T14:23:00Z",
  "parent_commit": "b7e4d2a",
  "delta_score": 0.0003
}
```

```markdown
<!-- .shared/notes/optimization/symmetry-breaking.md -->
# Symmetry Breaking in Interval Placement

Forcing the first interval to start at 0 eliminates ~50% of the search
space without losing optimal solutions. Confirmed by agents 0 and 2
across 8 independent evaluations.

Related attempts: a3f2b1c, d4e5f6g
```

### Heartbeat Mechanism

Three reflection types at different frequencies prevent tunnel vision:

**Per-iteration reflection** (every evaluation):

```
After eval #{n} with score {s}:
1. What did this change accomplish?
2. Was the score change expected?
3. Write 1-2 line observation to .shared/notes/
```

**Periodic consolidation** (every ~10 evaluations):

```
1. Review own progress over last 10 evals
2. Browse other agents' notes in .shared/notes/
3. Organize scattered observations into structured notes
4. Extract reusable patterns into .shared/skills/
5. Identify promising directions from other agents' work
```

**Stagnation redirection** (5 consecutive non-improving evaluations):

```
1. Forced reassessment: "Current approach is not working"
2. Read all recent notes from ALL agents
3. Identify unexplored directions
4. Pivot to fundamentally different approach
5. Log the pivot reason in notes
```

Without heartbeats, agents fixate on local optima and stop sharing knowledge. The consolidation step is critical - it forces cross-pollination between agents.

## Implementation Patterns

### File-Based Knowledge Sharing

The simplest approach for Claude Code / coding agent setups:

```python
import json
import glob
from pathlib import Path

SHARED = Path(".shared")

def log_attempt(commit: str, score: float, approach: str, agent_id: int):
    """Log evaluation result to shared knowledge."""
    entry = {
        "commit": commit,
        "agent": agent_id,
        "score": score,
        "approach": approach,
    }
    (SHARED / "attempts" / f"{commit}.json").write_text(json.dumps(entry, indent=2))

def get_best_score() -> float:
    """Read current best from shared attempts."""
    best = 0.0
    for f in glob.glob(str(SHARED / "attempts" / "*.json")):
        data = json.loads(Path(f).read_text())
        best = max(best, data["score"])
    return best

def check_stagnation(agent_id: int, window: int = 5) -> bool:
    """Detect if this agent has stagnated."""
    my_attempts = sorted(
        [json.loads(Path(f).read_text())
         for f in glob.glob(str(SHARED / "attempts" / "*.json"))
         if json.loads(Path(f).read_text())["agent"] == agent_id],
        key=lambda x: x["timestamp"],
    )
    if len(my_attempts) < window:
        return False
    recent = my_attempts[-window:]
    return all(a.get("delta_score", 0) <= 0 for a in recent)
```

### Evaluation Deduplication

Avoid re-running expensive evaluations on identical solutions:

```python
import hashlib

def solution_hash(code: str) -> str:
    """Content-based hash ignoring whitespace/comments."""
    # Strip comments and normalize whitespace
    lines = [l.strip() for l in code.splitlines()
             if l.strip() and not l.strip().startswith("#")]
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()[:12]

def already_evaluated(code: str) -> bool:
    h = solution_hash(code)
    return (SHARED / "attempts" / f"{h}.json").exists()
```

## CORAL Framework

Reference implementation: [github.com/Human-Agent-Society/Coral](https://github.com/Human-Agent-Society/Coral) (MIT, 429 stars). Multi-agent research infrastructure by MIT/NUS/Stanford/Meta.

### Setup and Launch

```bash
git clone https://github.com/Human-Agent-Society/CORAL.git && cd CORAL
uv sync --extra ui    # include web dashboard
uv run coral start -c examples/kernel_builder/task.yaml
```

### Task Definition (task.yaml)

```yaml
task_name: kernel_builder
num_agents: 4
runtime: claude-code   # or opencode, codex
grader: examples/kernel_builder/grader.py
max_iterations: 100
heartbeat_interval: 10  # consolidation every N evals
stagnation_threshold: 5
```

### Custom Grader

```python
from coral.grading import TaskGrader, ScoreBundle

class KernelGrader(TaskGrader):
    def evaluate(self, workspace: str) -> ScoreBundle:
        # Run benchmark, return structured scores
        cycles = run_kernel_benchmark(workspace)
        return ScoreBundle(
            primary=1.0 / cycles,          # lower cycles = higher score
            metrics={"cycles": cycles, "correctness": verify(workspace)},
        )
```

### Supported Runtimes

| Runtime | Command | Notes |
|---------|---------|-------|
| Claude Code | `claude` | Default, most tested |
| OpenCode | `opencode` | Open-source terminal agent |
| Codex | `codex` | OpenAI coding agent |

All require pre-installation. Runtime selection per `task.yaml`.

### Evaluation Flow

Agents call `uv run coral eval -m "description"` which atomically: stages changes, commits, runs grader, records attempt to `.coral/public/attempts/`, updates shared knowledge.

### Additional Features

- **Web dashboard** on port 8420 (`uv run coral ui`) - real-time agent monitoring
- **LiteLLM gateway** - custom model routing for non-default providers
- **Docker session mode** - containerized agent isolation
- **Warm-start literature review** - agents review prior art before optimization
- **Post-commit hooks** - automatic evaluation triggers

### Benchmarks

| Task | CORAL (4 agents) | AlphaEvolve | Speedup |
|------|-------------------|-------------|---------|
| Erdos Minimum Overlap | 99% of optimal, 34 min | 99% of optimal, 5.2h | ~9x |
| Anthropic Kernel | 1103 cycles | 1363 cycles | 19% better |

## Comparison with Linear Approaches

| Aspect | Linear (autoresearch) | Parallel Evolution |
|--------|----------------------|-------------------|
| Agents | 1 | 3-8 |
| Search strategy | Sequential keep/discard | Parallel diverse exploration |
| Knowledge sharing | Git history only | Explicit shared knowledge layer |
| Stagnation handling | Manual | Automatic redirection |
| Reflection | Optional | Built-in heartbeat |
| Improvement rate | ~9.5% (per eval) | ~36.8% (per eval) |
| Total evaluations needed | 84 (for same quality) | 19 |
| Cost per run | ~$0.10/cycle | ~$0.40/cycle (4 agents) |
| Effective cost/improvement | Higher | Lower (3-4x) |

The parallel approach reaches better solutions with fewer total evaluations because agents explore different directions simultaneously and share discoveries.

## Integration with Existing Patterns

**With [[agent-design-patterns]] (Reflexion)**: heartbeat reflection is a formalized version of self-critique applied to the search process itself, not just individual outputs.

**With [[multi-agent-systems]] (Shared State)**: the `.shared/` knowledge layer is a concrete implementation of the shared-state communication protocol using the filesystem.

**With [[context-engineering]]**: each agent maintains its own context focused on its current exploration direction. The shared knowledge layer acts as external memory, preventing context bloat from carrying all agents' history.

## Gotchas

- **File locking on shared writes**: multiple agents writing to `.shared/` simultaneously can corrupt JSON files. Use atomic writes (write to temp file, then rename) or per-agent subdirectories with periodic merge
- **Note quality degrades without structure**: agents generate vague notes ("tried X, didn't work") unless the heartbeat prompt explicitly requires structured observations with scores and hypotheses. Template the note format
- **Stagnation detection threshold matters**: too sensitive (2-3 evals) causes premature pivots away from promising directions. Too loose (10+ evals) wastes compute. 5 consecutive non-improving evals is a reasonable default but should be tuned per task complexity
- **Shared skills can propagate bad patterns**: if one agent writes a flawed skill to `.shared/skills/`, others will adopt it. Add a minimum score threshold before promoting observations to skills

## See Also

- [[agent-design-patterns]] - Reflexion and self-critique patterns
- [[multi-agent-systems]] - Agent collaboration architectures
- [[context-engineering]] - Managing agent working memory
- [[agent-self-improvement]] - Step-level rewards and learning from mistakes
- [[agent-memory]] - Memory types and persistence strategies
