---
title: AI Coding Skills and Extensibility
category: misc/ai-coding-tools
tags: [skills, ai-agents, extensibility, skill-marketplace, claude-code, antigravity, openclaw]
---

# AI Coding Skills and Extensibility

## Key Facts

- A **skill** is a folder containing a `skill.md` file with instructions that teach an AI coding agent how to perform a specific task
- Skills are the universal extension mechanism across AI coding tools: Claude Code, Antigravity, OpenClaw, Codex
- Skill folder structure: `skill.md` (required) + optional support files (scripts, examples, templates, references)
- `skill.md` contains two key fields: **name** (optional, defaults to folder name) and **description** (critical - determines when the agent loads the skill)
- Skills are loaded lazily: only the name + description are in context initially; full content is loaded when the agent decides the skill is relevant
- Skill scopes: **workspace** (project-specific) and **global** (all projects)
- Skills are **portable** across IDEs - the same skill.md works in Claude Code, Antigravity, and Gemini CLI
- Community skill directories (ClawHub, GitHub repositories) provide hundreds of pre-built skills for common tasks

### Skill Loading Flow

1. Agent starts conversation - loads **name + description** of all available skills
2. User sends prompt - agent scans skill descriptions for relevance
3. Agent selects relevant skills - loads full `skill.md` content
4. Agent may also load additional files from the skill folder if needed

### Best Practices

- **One skill = one responsibility** - don't create a "do-everything" skill
- **Description = trigger** - write it for the model, not for humans. Include specific phrases that match user intents
- **Include decision trees** for complex skills - help the agent choose the right approach based on context
- Keep `skill.md` under 5000 words - details go in `references/` subfolder
- Critical validations should be **scripts**, not prose - deterministic code beats natural language instructions

## Patterns

```
# Skill folder structure
.claude/skills/
  design/
    skill.md          # Main instructions
    references/       # Detailed docs
    scripts/          # Automation scripts
    examples/         # Example outputs
```

```markdown
# skill.md template
---
name: Test Generator
description: >
  Generate tests for recent or selected code changes.
  Use when: user says "generate tests", "write tests",
  "add test coverage", or after implementing a new feature.
---

# Test Generator

## Workflow
1. Detect the testing setup (framework, config, conventions)
2. Understand the code being tested
3. Plan the test coverage
4. Generate tests following repo conventions
5. Run tests and iterate until they pass

## Decision Tree
- Unit tests? -> Check if function is pure, mock dependencies
- Integration tests? -> Check API endpoints, database interactions
- E2E tests? -> Check user workflows, browser interactions
```

## Gotchas

- A vague description means the agent never loads the skill - be explicit about trigger phrases
- Skills aren't loaded mid-conversation if the agent already started working - start a new conversation after adding skills
- Community skills from marketplaces may contain unsafe instructions (credential access, web scraping) - review before installing
- Some skill actions conflict with service terms (e.g., YouTube scraping, social media automation) - the skill may work but violates platform policies
- Workspace skills override global skills with the same name

## See Also

- [[ai-ide-rules-and-context]] - persistent context rules (always-on vs triggered)
- [[ai-ide-workflow-modes]] - planning and execution modes
