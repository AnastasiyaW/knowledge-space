---
title: AI IDE Workflow Modes
category: misc/ai-coding-tools
tags: [planning, execution, code-review, ai-workflow, implementation-plan, artifacts]
---

# AI IDE Workflow Modes

## Key Facts

- AI coding IDEs separate work into two phases: **planning** (design/architecture) and **execution** (code generation)
- Each phase benefits from different models: high-reasoning for planning, fast/cheap for execution
- **Planning mode**: agent creates an implementation plan, waits for human review before making any code changes
- **Fast/execution mode**: agent directly modifies code without creating a plan first
- Implementation plans are **artifacts** - structured documents showing what files will change, what approach will be taken
- Plans can be **commented on** inline - select text, add comment, agent regenerates plan incorporating feedback
- After plan approval, switch to a cheaper/faster model for the actual code generation
- **Browser sub-agent**: a specialized agent that controls a browser to visually verify changes (click, scroll, type, screenshot, video recording)
- Artifacts include: implementation plans, screenshots, video recordings, code diffs, test results

### Model Selection by Phase

| Phase | Model Tier | Why |
|-------|-----------|-----|
| Planning | High reasoning (Opus, Gemini Pro High, GPT-5) | Need deep analysis, multi-step logic |
| Execution | Fast (Sonnet, Gemini Flash, GPT-4o-mini) | Code generation doesn't need max reasoning |
| Review/QA | Medium | Balance between thoroughness and cost |

### Feature Development Workflow

1. Write detailed prompt with **context**: mockups, tagged files, images
2. Set mode to **planning** with a high-reasoning model
3. Review the implementation plan - add comments, request changes
4. Approve plan, switch to **fast** mode with execution model
5. Agent generates code - review each file change (accept/reject per-file or per-line)
6. Browser sub-agent verifies changes visually
7. Run existing tests to ensure nothing broke
8. Create branch, commit, open PR for human review

## Patterns

```
# Prompt engineering for planning prompts
# Include ALL relevant context to minimize back-and-forth

Plan a new tool for cron expression explainer and generator.
Two main functionalities:
1. User pastes cron expression -> tool explains the interval
2. User configures interval -> tool generates cron expression

[Attach: desktop-mockup.png, mobile-mockup.png]
[Tag: @src/components/Base64.tsx]  # existing component to reuse

Base64 has components you can reuse - check before generating new ones.
Follow the design skill guidelines.
```

```
# Mode switching pattern in a single session:
# 1. Planning prompt -> Opus/Pro High -> review plan
# 2. "Yes, proceed" -> switch to Sonnet/Flash -> execute
# 3. Verification -> browser sub-agent screenshots
# 4. Test run -> check all existing tests pass
```

## Gotchas

- Don't use expensive planning models for execution - wastes budget and hits rate limits faster
- Always review generated code as if it were written by a junior developer - you are responsible for what ships
- The agent may generate duplicate components instead of reusing existing ones - explicitly tell it to check for reusable code
- After committing AI-generated changes, run the full test suite - agents often fix the targeted area but break adjacent functionality
- Browser sub-agent creates an overlay (blue border) while controlling the page - don't interact with the same tab simultaneously
- Rate limits are not published by most IDE providers - if you hit limits, switch to cheaper models for routine tasks

## See Also

- [[ai-ide-rules-and-context]] - persistent rules that guide planning and execution
- [[ai-coding-skills]] - reusable instruction sets for specific tasks
- [[ai-assistant-security]] - safety practices for AI coding tools
