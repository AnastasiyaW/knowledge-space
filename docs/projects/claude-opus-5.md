---
title: Claude Opus 5
category: projects
date: 2026-07-24
tags: [claude-opus-5, claude-opus-5-development, claude_opus_5, project]
aliases: ["Claude Opus 5"]
---

# Claude Opus 5

**Development line:** `project:claude-opus-5` · thread `claude-opus-5-development`  
**Last event:** 2026-07-24 · 1 dated since 2026-07-24 · **Researched:** 2026-09-07 · confidence: high

## What it is

Anthropic’s active Opus-tier model for teams building long-running coding agents and enterprise workflows.

- Complex coding, tool use, long-context, vision, and document tasks.
- 1M-token context and 128K standard maximum output; the Batch API’s 300K ceiling is beta-only.
- $5 per million input tokens and $25 per million output tokens.

Use it when your own evaluation justifies the output-token and latency cost.

## Development line

- **2026-07-24 — Anthropic published a Claude Opus 5 news announcement.** On 2026-07-24, Anthropic published an official news item whose link identifies it as relating to Claude Opus 5. The available evidence does not establish the announcement's capabilities, availability, pricing, or technical details, so this history entry records only the dated development milestone.

## What changed

2026-07-24 — Claude Opus 5 launched as `claude-opus-5` with a 1M-token context, 128K maximum output, adaptive thinking on by default, 5 effort levels, and beta mid-conversation tool changes.  
2026-08-01 — Claude Opus 5 became supported in the Dreams research preview.  
2026-08-05 — Claude Opus 4.1 retired; Anthropic named Claude Opus 5 the upgrade path.  
2026-08-19 — Claude Opus 5 became compatible on the Claude API with the GA computer-use toolset and the newly launched browser-use client toolset.  
2026-08-20 — Those toolsets became available for Claude Opus 5 on Google Cloud.  
2026-09-01 — The Claude API added beta per-message effort changes for Claude Opus 5 while preserving the prompt cache.

## How to use this

1. Create a Messages API request with `model="claude-opus-5"`, set `max_tokens`, and send the complete message history for a multi-turn conversation.
  — <https://platform.claude.com/docs/en/claude_api_primer>
2. When migrating an Opus 4.8 integration, select response blocks by `type`, return thinking blocks unmodified after tool calls, and remove `thinking.disabled` at `xhigh` or `max`.
  — <https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5>
3. Start at the default `high` effort, run an effort sweep on your own evaluations, then choose `low`, `medium`, `xhigh`, or `max`; set a large `max_tokens` at `xhigh` or `max`.
  — <https://platform.claude.com/docs/en/build-with-claude/effort>
4. For 1 Claude Code session, start `claude --model claude-opus-5`.
  — <https://support.claude.com/en/articles/11940350-claude-code-model-configuration>

## Best practices

- Give complex work the complete task specification up front, and explicitly bound scope for narrow work.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>
- Ask for the visible response length you need; effort controls thinking volume, not reliably the length of the answer.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>
- Start at `high`, then change effort only after an effort sweep on your own evaluations; lower it where quality holds and reserve `xhigh` or `max` for capability-sensitive work.
  — <https://platform.claude.com/docs/en/build-with-claude/effort>
- Remove inherited final-verification or verifier-subagent instructions unless the task truly requires them; on Opus 5 they can cause over-verification and wasted tokens.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>

## Superseded by this

- 2026-07-24 — The Opus 4.8 assumption that adaptive thinking is opt-in and `content[0]` is text is obsolete for Claude Opus 5; response blocks must be handled by type.
- 2026-07-24 — `thinking: {"type": "disabled"}` at `xhigh` or `max` is no longer a valid Claude Opus 5 request; it returns HTTP 400.
- 2026-08-05 — `claude-opus-4-1-20250805` is retired and now errors; Anthropic’s stated upgrade target is Claude Opus 5.
- 2026-08-19 — Treating `computer_toolset_20260801` as beta-only on the Claude API is obsolete; the toolset is GA, while earlier beta versions remain available.

## Still unknown

- No source in this set establishes account-specific quotas, regional capacity, or contract pricing; verify the target console or cloud catalog before rollout.
- The launch announcement’s benchmark and early-access claims were not independently reproduced here.
- No official source found in this research says that Fable 5.1 retires or supersedes Claude Opus 5; the current model page still lists Opus 5 as active.

## Sources

| source | title | read |
|---|---|---|
| https://www.anthropic.com/news/claude-opus-5 | Introducing Claude Opus 5 | 2026-09-07 |
| https://platform.claude.com/docs/en/release-notes/overview | Claude Platform release notes | 2026-09-07 |
| https://platform.claude.com/docs/en/models/opus-5/overview | Claude Opus 5 | 2026-09-07 |
| https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5 | What’s new in Claude Opus 5 | 2026-09-07 |
| https://platform.claude.com/docs/en/claude_api_primer | API usage primer for Claude | 2026-09-07 |
| https://platform.claude.com/docs/en/build-with-claude/effort | Effort | 2026-09-07 |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | Prompting Claude Opus 5 | 2026-09-07 |
| https://support.claude.com/en/articles/11940350-claude-code-model-configuration | Claude Code model configuration | 2026-09-07 |
| https://platform.claude.com/docs/zh-CN/release-notes/overview | Claude Platform 发布说明 | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:claude-opus-5`, thread `claude-opus-5-development`, 1 dated events 2026-07-24 → 2026-07-24.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
