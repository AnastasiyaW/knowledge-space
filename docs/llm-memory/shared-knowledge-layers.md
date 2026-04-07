---
title: Shared Knowledge Layers for Multi-Agent Systems
category: patterns
tags: [llm-memory, multi-agent, shared-memory, knowledge-sharing, heartbeat]
---

# Shared Knowledge Layers for Multi-Agent Systems

When multiple agents work in parallel, they need a structured way to share discoveries without interfering with each other's work. The pattern: isolated workspaces + shared knowledge layer through files.

## Key Facts

- Each agent gets an **isolated workspace** (git worktree, separate directory, container) - can't break others
- A **shared public layer** is accessible to all agents via symlinks or shared mount:
  - `attempts/` - historical evaluations with scores and commit hashes
  - `notes/` - markdown observations organized hierarchically by topic
  - `skills/` - reusable procedures and scripts distilled from successful runs
- Agents read shared layer before starting work, write to it after completing evaluations
- Without shared layer: agents duplicate work, repeat failed approaches, don't build on each other
- With shared layer: 3-10x higher improvement rates, 4x fewer evaluations needed

## Patterns

### Heartbeat Mechanism

Periodic forced reflection that prevents agents from fixating on one approach:

```
Per-iteration (after each eval):
  -> Write observation to notes/
  -> Record attempt score in attempts/

Periodic consolidation (every ~10 evals):
  -> Review own progress
  -> Read other agents' notes
  -> Distill patterns into skills/
  -> Reorganize notes hierarchy

Stagnation redirection (5+ non-improving):
  -> Forced reassessment
  -> Read all shared notes for inspiration
  -> Pivot to different approach
```

### File-Based Shared Memory

```
.shared/
  attempts/
    eval-001.json     # {approach, score, commit, timestamp}
    eval-002.json
  notes/
    optimization/
      learning-rate.md
      batch-size.md
    architecture/
      attention-variants.md
  skills/
    grid-search.sh
    evaluate-model.py
```

### Implementation with Claude Code Agents

```bash
# Agent 1 workspace
git worktree add agent-1 main
ln -s ../shared agent-1/.shared

# Agent 2 workspace  
git worktree add agent-2 main
ln -s ../shared agent-2/.shared

# Each agent's CLAUDE.md includes:
# "Before starting: read .shared/notes/ for context"
# "After each significant finding: write to .shared/notes/"
# "Every 10 iterations: consolidate and share skills"
```

### Stagnation Detection

```python
def check_stagnation(attempts_dir, threshold=5):
    """Detect if agent is stuck on non-improving approaches."""
    recent = sorted(Path(attempts_dir).glob("*.json"))[-threshold:]
    scores = [json.loads(f.read_text())["score"] for f in recent]
    
    if len(scores) >= threshold:
        best = max(scores[:-threshold]) if len(scores) > threshold else 0
        recent_best = max(scores[-threshold:])
        if recent_best <= best:
            return True  # Stagnant - force pivot
    return False
```

## Gotchas

- **Issue:** Agents write conflicting observations to shared notes simultaneously -> **Fix:** Use append-only files or agent-prefixed filenames (`agent-1-note-003.md`). Never overwrite others' notes
- **Issue:** Shared skills become stale as the problem evolves -> **Fix:** Tag skills with the evaluation score they produced. Agents can judge relevance by score recency
- **Issue:** Too much shared state causes agents to converge on the same approach -> **Fix:** Limit note reading to consolidation phases (not every iteration). Diversity of approaches is valuable
- **Issue:** Heartbeat consolidation is expensive (reads all notes, rewrites) -> **Fix:** Use incremental consolidation - only process notes newer than last consolidation timestamp

## See Also

- [[memory-architectures]] - hierarchical memory structures
- [[session-persistence]] - preserving knowledge between sessions
- [[temporal-memory]] - validity windows for shared facts
- [[agent-orchestration]] - coordinating multiple agents
