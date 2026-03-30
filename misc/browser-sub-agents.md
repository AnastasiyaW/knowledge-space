---
title: Browser Sub-Agents for Verification
category: misc/ai-coding-tools
tags: [browser-automation, sub-agent, visual-verification, testing, screenshots, artifacts]
---

# Browser Sub-Agents for Verification

## Key Facts

- AI coding IDEs include a **browser sub-agent** - a specialized model that can control a browser to verify code changes visually
- The browser sub-agent runs a different model optimized for page interaction (separate from the main coding model)
- Available actions: click, scroll, type, read console logs, take screenshots, record video
- While the sub-agent controls a page (shown with a blue overlay border), you can work in other tabs
- Primary use case: **visual verification** after code changes - the agent opens the app and confirms the UI matches expectations
- Secondary use case: **automation testing** - agent navigates user flows, checks elements, verifies functionality
- Sub-agent creates **artifacts**: screenshots, video recordings, walkthroughs documenting what it verified
- This replaces the manual "save code, refresh browser, check visually" cycle

### Browser Sub-Agent vs E2E Testing

| Aspect | Browser Sub-Agent | E2E Tests (Playwright/Cypress) |
|--------|-------------------|-------------------------------|
| Setup | Zero - built into IDE | Framework setup required |
| Determinism | Non-deterministic (AI-driven) | Deterministic (scripted) |
| Maintenance | No test scripts to maintain | Tests break when UI changes |
| Coverage | Ad-hoc, guided by prompt | Systematic, repeatable |
| CI/CD | Not suitable | Designed for CI/CD |
| Best for | Quick verification during dev | Regression testing |

## Patterns

```
# Triggering browser sub-agent in a prompt
Prompt: "Use the browser sub-agent to verify the default
value changed to 3 on the UUID generator page"

# Agent flow:
# 1. Opens managed browser with blue overlay
# 2. Navigates to the target URL
# 3. Takes screenshot for verification
# 4. Confirms the value matches expectation
# 5. Generates artifacts (screenshot + video playback)
```

```
# Combining code change with browser verification
Prompt: "Change the default quantity from 1 to 3,
then use the browser to verify it works"

# Agent:
# 1. Modifies source code
# 2. Waits for hot-reload / rebuilds
# 3. Opens browser sub-agent
# 4. Navigates to the page
# 5. Checks the quantity field shows "3"
# 6. Creates verification artifact
```

## Gotchas

- Don't interact with the tab while the sub-agent has the blue overlay - it will interfere with the agent's actions
- The browser sub-agent is NOT a replacement for proper E2E tests - it's for quick verification during development
- Some actions execute very fast (milliseconds) - you may not see them happen, but they appear in the video recording artifact
- Browser sub-agent requests consume tokens from your model quota - complex page interactions can be expensive
- Pages with anti-bot protection, CAPTCHAs, or login requirements may block the sub-agent
- The sub-agent can only access pages on localhost or public URLs - it can't access pages behind VPN or auth walls without setup

## See Also

- [[ai-ide-workflow-modes]] - browser verification as part of the plan-execute-verify cycle
- [[ai-coding-skills]] - skills can instruct the agent when to use browser verification
