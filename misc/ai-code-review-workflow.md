---
title: AI-Assisted Code Review Workflow
category: misc/ai-coding-tools
tags: [code-review, pull-request, ai-review, diff-review, accept-reject, implementation-plan]
---

# AI-Assisted Code Review Workflow

## Key Facts

- AI coding IDEs generate code that must be **reviewed like any other contributor's code** - the developer is responsible for what ships
- Code changes are presented as **diffs** with per-line and per-file accept/reject controls
- Three levels of review: accept/reject **individual lines**, accept/reject **per file**, accept/reject **all changes at once**
- Implementation plans serve as a **contract** between you and the AI - review the plan thoroughly before approving execution
- Plan review supports **inline comments**: select text in the plan, add a comment, agent regenerates incorporating feedback
- After AI generates code, always run the **full test suite** - agents often fix the targeted area but introduce regressions elsewhere
- Create a separate branch for AI-generated changes and open a PR for human review before merging
- Review AI code with extra scrutiny for: duplicated components, missing error handling, hardcoded values, broken existing tests

### Review Checklist for AI-Generated Code

- [ ] Does the change match the approved plan?
- [ ] Are existing components reused instead of duplicated?
- [ ] Do all existing tests still pass?
- [ ] Are there new tests for the new functionality?
- [ ] Does the code follow project conventions and style?
- [ ] Are there any hardcoded values that should be configurable?
- [ ] Does the change work on both desktop and mobile?
- [ ] Has the agent modified files outside the intended scope?

## Patterns

```
# Plan review workflow

1. Write detailed planning prompt with:
   - Feature description
   - Mockups/screenshots (attach images)
   - Tagged reference files (@components/Base64.tsx)
   - Explicit instruction to reuse existing components
   - Reference to design/style guidelines

2. Review implementation plan:
   - Check file list - are the right files being modified?
   - Check for component reuse vs duplication
   - Check navigation/routing updates
   - Comment on anything you disagree with

3. After approval, switch to execution:
   - Change mode from planning to fast
   - Change model from expensive to execution tier
   - Tell agent to proceed

4. Review generated code:
   - Use diff view to inspect each change
   - Accept/reject per line or per file
   - Run test suite before accepting

5. Post-acceptance:
   - Create branch, commit changes
   - Run full project test suite
   - Open PR for team review
```

```bash
# Post-AI-generation verification commands
# Always run these BEFORE creating PR:

npm run test         # Run all tests
npm run build        # Ensure build succeeds
npm run lint         # Check code style
npm run type-check   # TypeScript type verification
```

## Gotchas

- AI-generated code often looks correct but has subtle bugs - never approve without testing
- The agent may create entirely new components instead of reusing existing ones even when told to - verify the file list in the plan
- Accepting "all changes" is risky - review at least per-file to catch unintended modifications
- AI may update navigation, routing, or config files as a side effect - check for changes outside the main feature scope
- The "rollback" feature in AI IDEs lets you revert to an earlier conversation point - use it if the agent went off track
- Test-driven verification (agent runs tests as part of workflow) catches regressions early but may mask integration issues
- Don't merge AI code without a PR, even for small changes - the diff review catches things the inline review misses

## See Also

- [[ai-ide-workflow-modes]] - planning vs execution modes for code generation
- [[ai-ide-rules-and-context]] - rules that guide code generation style and conventions
