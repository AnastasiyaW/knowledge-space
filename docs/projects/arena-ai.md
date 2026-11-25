---
title: Arena.ai — Agent Mode
category: projects
date: 2026-06-04
tags: [agent-mode, arena-ai, arena_ai, project]
aliases: ["Arena.ai"]
---

# Arena.ai — Agent Mode

**Development line:** `project:arena-ai` · thread `agent-mode`  
**Last event:** 2026-06-04 · 1 dated since 2026-06-04 · **Researched:** 2026-09-05 · confidence: high

## What it is

Arena.ai Agent Mode is a browser workspace for multi-step tasks rather than isolated chat responses.

- Plans tasks and executes them with web search, image generation, uploads, code help, and sandboxed Bash.
- Connects a GitHub repository to clone into a sandbox, display diffs, and create pull requests.
- Routes each session to an undisclosed orchestrator model chosen at random.

A repository session creates only one pull request and cannot push further work once merged or closed.
Use it for bounded deliverables we can inspect; the leaderboard reflects Arena's environment rather than a universal guarantee.

## Development line

- **2026-06-04 — Arena.ai documented an Agent Mode development update.** Arena.ai launched Agent Mode with tool-using multi-step workflows and an Agent Arena leaderboard built on real session traces.

## What changed

- 2026-06-04: Arena.ai launched Agent Mode with a tool-using multi-step workflow and the Agent Arena leaderboard derived from real session traces.
- 2026-06-29: Arena reported 5M+ Agent Mode turns per month and 10% week-over-week growth.
- 2026-08-14: Agent Arena gained Code, Chat, and Work filters plus cost-per-task and Pareto views.
- 2026-08-24: Agent Mode gained GitHub-connected coding with sandbox clones, live diffs, commits, pushes, and pull requests.

## How to use this

From 2026-06-04, practitioners evaluating Arena.ai should check its Agent Mode workflow and agent product surface as part of their tool assessment, while verifying capabilities directly because this line contains no researched feature evidence.

1. Open Agent Mode directly.
  — <https://arena.ai/agent>
2. Describe the desired multi-step outcome, attach relevant files, and start the workflow from the chat bar.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>
3. Use Workspace to retrieve output: download a ZIP without a repository, or inspect the Diff and pull request when a repository is connected.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>
4. For repository work, connect GitHub, select the organizations and repositories Arena may access, and enable GitHub in Agent Mode.
  — <https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode>
5. Review the diff and automated Checks before merging; keep the task within the current one-pull-request-per-chat limit.
  — <https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode>

## Best practices

- Use Agent Mode for connected research, coding, analysis, or iteration; use Battle, Side-by-Side, or Direct for a simple one-step query.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>
- Choose an agent model from the relevant Code, Chat, or Work view and compare task cost, rather than treating one overall rank as universal.
  — <https://arena.ai/blog/agent-categories-and-cost>
- For GitHub work, scope a session to one reviewable pull request and inspect both the Diff and Checks before merge.
  — <https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode>
- Push or download work before merging or closing a pull request, because the session cannot deliver subsequent files through that closed workflow.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>

## Superseded by this

- Since 2026-08-14, choosing an Agent Arena model from the single overall ranking alone is incomplete; use category and cost views.
- Since 2026-08-24, describing Agent Mode as a sandbox with no repository-delivery workflow is outdated; it can connect GitHub repositories and create pull requests.

## Still unknown

- Arena does not disclose the orchestrator model after feedback, so a completed session cannot be pinned to a named model from the public interface described here.
- The checked sources do not establish Agent Mode pricing, rate limits, retention, or a service-level commitment.
- Repository permissions and live delivery behavior were not tested directly in a logged-in session.

## Sources

| source | title | read |
|---|---|---|
| http://arena.ai/blog/agent-mode/ | Empowering Users to Get More Done With Agent Mode | 2026-09-05 |
| https://arena.ai/agent | Agent Mode | Autonomous AI Agents for Real-World Tasks | 2026-09-05 |
| https://arena.ai/blog/agent-arena-methodology | Agent Arena: Causal Evaluation of Agents in the Real World | 2026-09-05 |
| https://help.arena.ai/articles/5432423882-how-to-use-agent-mode | How to use Agent Mode on Arena | 2026-09-05 |
| https://arena.ai/blog/arena-100m-revenue | Arena Reaches $100M in 8 Months | 2026-09-05 |
| https://arena.ai/blog/agent-categories-and-cost | Agent Leaderboard Improvements: Categories & Task Cost | 2026-09-05 |
| https://arena.ai/blog/coding-in-agent-mode | Coding in Agent Mode: From Idea to Shipping with GitHub | 2026-09-05 |
| https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode | How to use coding in Agent Mode | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:arena-ai`, thread `agent-mode`, 1 dated events 2026-06-04 → 2026-06-04.
- **Practical note:** From 2026-06-04, practitioners evaluating Arena.ai should check its Agent Mode workflow and agent product surface as part of their tool assessment, while verifying capabilities directly because this line contains no researched feature evidence.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.