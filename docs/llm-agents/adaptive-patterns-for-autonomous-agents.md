# Adaptive Patterns for Autonomous Agents

Adaptive agent architectures utilize dynamic hooks and structured state management to reduce ambiguity and automate skill selection during the development lifecycle.

## Keyword-Triggered Skill Activation
Instead of manual tool invocation, a `UserPromptSubmit` hook scans the input stream for specific tokens to pre-activate relevant environment skills.

- **Mechanism:** A Python-based interceptor maps regex patterns to specialized sub-agents or toolsets.
- **Common Triggers:** `plan`, `review`, `security`, `handoff`, `research`.
- **Integration:** Hooks reside in the configuration layer to modify the context before the LLM generates the primary response.

### Implementation Example
```python
import re

def prompt_hook(text):
    triggers = {
        r"\bplan\b": "project_planner",
        r"\bsecurity\b": "security_audit_tool",
        r"\bhandoff\b": "session_summarizer"
    }
    active_skills = [skill for pattern, skill in triggers.items() if re.search(pattern, text, re.I)]
    return active_skills
```

## Multi-Dimensional Ambiguity Scoring
To prevent hallucination during the planning phase, agents employ a "Deep Interview" pattern that quantifies uncertainty across weighted dimensions.

- **Dimensions:** Scope, Constraints, Success Criteria, and Edge Cases.
- **Threshold Gate:** The agent is prohibited from execution if the ambiguity score exceeds a set limit (e.g., 20%).
- **Interactive Refinement:** The system generates targeted questions focusing exclusively on the dimension with the highest uncertainty score.

### Scoring Schema
```json
{
  "dimensions": {
    "scope": {"weight": 0.4, "score": 0.1},
    "constraints": {"weight": 0.3, "score": 0.5},
    "success_criteria": {"weight": 0.3, "score": 0.2}
  },
  "total_ambiguity": 0.25,
  "status": "REJECTED_NEEDS_INFO"
}
```

## PRD-Driven Persistence
State management is handled via a persistent `prd.json` file that synchronizes user stories with verifiable acceptance criteria.

- **Persistence:** High-level goals are decoupled from the transient conversation history.
- **Verification Loop:** Each story includes a `passes` boolean, updated only after successful test execution or manual validation.
- **Learning Log:** A sibling `learnings.md` file tracks non-obvious project constraints discovered during implementation to prevent regression.

### PRD Structure
```json
{
  "version": "1.1",
  "stories": [
    {
      "id": "USER-01",
      "description": "Implement OAuth2 flow",
      "acceptance_criteria": ["Token refresh works", "Expired tokens fail"],
      "status": "verified"
    }
  ]
}
```

## Formal XML Agent Specifications
Standardizing agent definitions using XML sections enforces strict boundary compliance for specialized sub-agents.

- **Role:** Explicit persona and expertise level.
- **Rules:** Immutable behavioral constraints.
- **Examples:** Few-shot patterns showing "Good" vs "Bad" outputs.
- **Escalation:** Conditions under which the agent must stop and request intervention.

### Definition Format
```xml
<AgentDefinition>
  <Role>Senior Security Auditor</Role>
  <Constraints>Do not modify source code; only report vulnerabilities.</Constraints>
  <Escalation>Trigger if P0 credential leak is detected.</Escalation>
</AgentDefinition>
```

## Memory Integrity and Wiki Linting
As agent memory files (e.g., `MEMORY.md`, `JOURNAL.md`) scale, automated linting prevents information fragmentation.

- **Orphan Detection:** Identifies markdown files not linked from the primary index.
- **Stale Content Tracking:** Flags entries not updated within N sessions or those contradicting newer `prd.json` states.
- **Link Validation:** Ensures all `[[wiki-links]]` resolve to existing files within the workspace.

## Gotchas
- **Issue:** Keyword triggers can cause "tool loops" if the agent's response contains the trigger word, causing the hook to fire recursively. → **Fix:** Implement a recursion depth limit or ignore trigger keywords within the assistant's own output.
- **Issue:** Over-interrogation in ambiguity scoring can lead to "prompt fatigue" where the user provides low-quality answers to bypass the gate. → **Fix:** Allow manual "forced override" for low-risk tasks or provide suggested answers (multiple choice).
- **Issue:** Local state files (`prd.json`) getting out of sync with the actual codebase after manual `git checkout` operations. → **Fix:** Include state file checksums or integrate the linting process into pre-commit hooks.

## See Also
- [[agent-design-patterns]]
- [[context-engineering]]
- [[agent-memory]]
- [[agent-orchestration]]

