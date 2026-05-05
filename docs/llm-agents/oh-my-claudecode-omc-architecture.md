# Oh My ClaudeCode (OMC) Architecture

Oh My ClaudeCode (OMC) is an agentic framework extending Claude Code (v4.13.2) through a layered system of specialized agents, workflow skills, and lifecycle hooks. It focuses on high-precision planning and autonomous execution using multi-model dispatch.

## Specialist Agent Layer
The framework employs 19 specialist agents defined via YAML frontmatter and XML-structured system prompts. Agents are categorized by their operational scope:

- **Strategic Agents:** `architect` (strategic advisor), `planner` (structured plan creation), `critic` (evaluation).
- **Quality & Security:** `code-reviewer` (severity-gated reviews), `security-reviewer` (vulnerability detection), `verifier` (post-execution validation).
- **Execution Agents:** `executor` (general tasks), `designer` (UI/UX), `git-master` (version control).
- **Exploration & Research:** `explore` (fast codebase mapping), `scientist` (hypothesis testing), `tracer` (lightweight execution tracing).

### Agent Definition Format
Agents utilize a standardized XML body to enforce constraints and output formats:
```yaml
name: code-reviewer
description: Senior quality engineer
model: claude-3-5-opus
level: senior
disallowedTools: [run_shell_command]
```
```xml
<Role>Expert Code Reviewer</Role>
<Success_Criteria>Zero P0 bugs in merged code</Success_Criteria>
<Rules>
  1. Never approve without evidence of test execution.
  2. Flag complexity increases as warnings.
</Rules>
<Output_Format>JSON-structured review summary</Output_Format>
```

## Planning Paradigms
OMC implements four distinct planning modes to handle varying request clarity:

- **Interview Mode:** Socratic questioning triggered when ambiguity scoring exceeds 20%. Each question targets specific missing technical dimensions.
- **Consensus (RALPLAN-DR):** A multi-agent loop involving `Planner` -> `Architect` -> `Critic`. It runs up to 5 rounds to produce an Architecture Decision Record (ADR).
- **Direct Mode:** Immediate plan generation for well-defined, low-ambiguity tasks.
- **Review Mode:** External evaluation of existing plans by the `Critic` agent to identify edge cases before execution starts.

## PRD-Driven Persistence
The `Ralph` pattern ensures execution continuity across session interruptions by utilizing a `prd.json` state file.

- **Acceptance Criteria:** Every user story in the PRD is linked to specific testable criteria.
- **Evidence-Based Progress:** Tasks are marked `passed: true` only when automated verification provides empirical evidence (logs, test passes).
- **State Storage:** All plans and state transitions are persisted to `.omc/plans/`, allowing the pipeline to resume from the last verified story.

### Persistence Schema
```json
{
  "project": "core-engine",
  "stories": [
    {
      "id": "ST-001",
      "description": "Implement buffer rotation",
      "criteria": ["No data loss on overflow", "O(1) insertion"],
      "status": "verified",
      "evidence": "tests/test_buffer.py:L45"
    }
  ]
}
```

## Evolutionary Self-Improvement
The framework includes a tournament-based optimization cycle for its own logic and benchmarks.

1. **Research:** Agents identify optimization targets in the current workflow.
2. **Execution:** Alternative code patterns are generated and benchmarked.
3. **Tournament Selection:** Successful patterns are compared in a "tournament." Only those outperforming the baseline are merged.
4. **Benchmark Integrity:** Evaluation relies on sealed benchmark files that are protected from agent modification to prevent self-referential score inflation.

## Gotchas
- **State Sprawl:** The framework generates significant metadata across 8+ directories; periodic manual cleanup of `.omc/` is required as no unified garbage collection exists.
- **Destructive Command Risk:** The autonomous autopilot lacks a hard guardrail for destructive shell commands; it relies on the pre-tool enforcer which can be bypassed in high-autonomy modes.
- **Token Inflation:** A single RALPLAN-DR consensus loop involving Opus can consume $50-$100 in API tokens for complex architectural decisions without warning.

## See Also
- [[agent-design-patterns]]
- [[claude-code-ecosystem]]
- [[managed-agents]]
- [[agent-orchestration]]

