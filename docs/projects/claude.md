---
title: Claude — Claude product development
category: projects
tags: [claude, claude-product-development, project]
aliases: ["Claude", "Claude 2.1"]
---

# Claude — Claude product development

**Development line:** `project:claude` · thread `claude-product-development`  
**Events:** 2 dated, 2023-05-12 → 2023-11-22 · **Researched:** 2026-09-04 · confidence: high

## What it is

Claude — Anthropic’s model family for chat users, application developers, and software teams. - accepts text and images and returns text; - supports multilingual work, vision, tool use, and long-context tasks; - is available through chat, the Messages API, and Claude Code for repository work. Limit: current API models expose 200K or 1M input tokens and 64K or 128K output tokens, depending on the model. Verdict: select and evaluate a current model for a defined task; Claude 2.x is no longer an API option.

## Development line

- **2023-05-12 — Claude expanded to 100K-token context windows.** On 2023-05-12, Anthropic announced that Claude could work with context windows of up to 100,000 tokens. This was a material expansion of the Claude product line's capacity to handle long documents and extended conversations.
- **2023-11-22 — Claude 2.1 introduced a 200K-token context window.** On 2023-11-22, Anthropic introduced Claude 2.1 with a 200,000-token context window. The release represented a new Claude version and described reliability-oriented improvements alongside the larger-context capability.

## What changed

Claude — the dated development line. - 2023-05-12: the 100K-context release expanded Claude from 9K to 100K tokens, making whole-document analysis and codebase-scale prompts practical; the official article is dated 2023-05-11. - 2023-11-22: Claude 2.1 raised the limit to 200K tokens, added system prompts and beta tool use, and reported lower false-statement rates; the official article is dated 2023-11-21. - 2026-09-04 (found today): current documentation describes a model family with text-and-image input, tool use, model-specific limits, and a 200K–1M-token context range. Limit: the historical 100K and 200K figures are release-era limits, not a current default. Verdict: use the dated posts as history, but use the live model and deprecation pages for deployment decisions.

## How to use this

From 2023-05-12, practitioners could consider Claude for workflows requiring up to 100K tokens of context; from 2023-11-22, Claude 2.1 extended that planning envelope to 200K tokens.

1. Choose the surface: use Claude.ai for chat, the Console and API for an application, or Claude Code for a repository task.
  — <https://docs.anthropic.com/en/docs/about-claude/models/overview>
2. For an API integration, create a Claude Console account and API key, export it as ANTHROPIC_API_KEY, then install the supported SDK.
  — <https://docs.anthropic.com/en/docs/get-started>
3. Choose a current model against capability, latency, cost, effort, and your task evaluation before committing to production.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
4. Make a Messages API call with the selected model, a max_tokens limit, and the user message; add tools, files, or context-management features only when the task needs them.
  — <https://docs.anthropic.com/en/docs/get-started>
5. For codebase work, install Claude Code on a supported surface, start it in the project directory, and review the file and command actions it performs.
  — <https://code.claude.com/docs/en/overview>

## Best practices

- Define specific, measurable success criteria and an evaluation set before changing prompts or models.
  — <https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>
- State the task, context, constraints, output format, and ordered steps explicitly; use relevant examples when output consistency matters.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- For inputs above 20K tokens, place long documents before the query, structure multiple documents clearly, and ask for supporting quotations before synthesis.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Treat model choice and effort as performance controls alongside prompting; use evaluations to trade capability against latency and cost.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
- Use pinned model IDs for reproducibility and monitor their lifecycle; dateless IDs from the 4.6 generation onward are fixed snapshots, not moving aliases.
  — <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions>

## Superseded by this

- 2023-05-12: treating 100K tokens as Claude’s operational context ceiling is obsolete; current models range from 200K to 1M input tokens.
- 2023-11-22: deploying Claude 2.1 guidance is obsolete; API model claude-2.1 was retired on 2025-07-21.
- 2023-11-22: treating tool use as a beta-only capability is obsolete; current-model documentation lists tool use as a supported capability.
- Pre-4.6 alias assumptions are obsolete for current dateless model IDs: each current ID identifies a fixed model snapshot.

## Still unknown

- The two dated events are not a complete release chronology between 2023 and today; the current documentation is used only as a live snapshot.
- The supplied event dates are one day later than the official article dates: 2023-05-12 versus 2023-05-11, and 2023-11-22 versus 2023-11-21.
- Plan availability, region, platform, and pricing can differ by account and change after this snapshot; verify them in the Console before rollout.

## Sources

| source | title | read |
|---|---|---|
| https://www.anthropic.com/index/100k-context-windows | Introducing 100K context windows | Anthropic | 2026-09-04 |
| https://www.anthropic.com/index/claude-2-1 | Introducing Claude 2.1 | Anthropic | 2026-09-04 |
| https://docs.anthropic.com/en/docs/about-claude/models/overview | Models overview | Claude Platform Docs | 2026-09-04 |
| https://docs.anthropic.com/en/docs/get-started | Get started with Claude | Claude Platform Docs | 2026-09-04 |
| https://code.claude.com/docs/en/overview | Overview | Claude Code Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/models/choosing-a-model | Choosing the right model | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Define success criteria and build evaluations | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Prompting best practices | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions | Model IDs and versioning | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/model-deprecations | Model deprecations | Claude Platform Docs | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:claude`, thread `claude-product-development`, 2 dated events 2023-05-12 → 2023-11-22.
- **Practical note:** From 2023-05-12, practitioners could consider Claude for workflows requiring up to 100K tokens of context; from 2023-11-22, Claude 2.1 extended that planning envelope to 200K tokens.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
