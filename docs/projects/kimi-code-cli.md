---
title: Kimi Code CLI — Public project reference
category: projects
date: 2026-06-09
tags: [kimi-code-cli, kimi_code, project, public-project-reference]
aliases: ["Kimi Code CLI"]
---

# Kimi Code CLI — Public project reference

**Development line:** `project:kimi-code-cli` · thread `public-project-reference`  
**Last event:** 2026-06-09 · 1 dated since 2026-06-09 · **Researched:** 2026-09-07 · confidence: medium

## What it is

Kimi Code CLI — a terminal coding agent for developers, not a standalone model.

- Reads and edits code, runs shell commands, searches files, and fetches web pages.
- Uses Kimi Code OAuth, a Kimi Platform API key, or configured compatible providers; supports ACP editor integration.
- Current documented release: v0.41.0 on 2026-09-04; npm installation requires Node.js 22.19+, and Windows requires Git for Windows.

Permission modes and version checks are operating controls, not setup details.

## Development line

- **2026-06-09 — Kimi Code CLI documentation and source repository were publicly linked.** On 2026-06-09, a dated post for Kimi Code CLI linked the project's English documentation and GitHub repository. This establishes a public reference point for the CLI's documentation and source. The supplied evidence does not identify a version, release mechanism, or feature set.

## What changed

2026-06-09 — Kimi Code CLI v0.12.0 added `/swarm` with live progress and rate-limit-aware retries. It moved goals, background questions, and sub-skill discovery out of experimental flags. It added proxy and Homebrew support, and enabled micro-compaction by default. On the same date, v0.12.1 fixed obsolete experimental-config compatibility and xhigh effort passthrough for OpenAI-compatible Chat Completions.

## How to use this

1. Install with the official script, or install `@moonshot-ai/kimi-code` through npm; on Windows, install Git for Windows before first launch.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html>
2. Enter the repository directory, run `kimi`, then use `/login` for Kimi Code OAuth or a Kimi Platform API key.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html>
3. Start with a read-only orientation request, such as asking Kimi to explain the project directories; use `kimi -p` for a one-off instruction.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html>
4. Review approvals before making changes, and use `/plan` before complex or high-risk work.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html>
5. For multi-turn work, use `/goal` with a finish condition and evidence that proves completion.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/goals.html>
6. Configure non-Kimi providers and model aliases in `~/.kimi-code/config.toml`; ambient shell API-key variables are not automatically used as provider credentials.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html>

## Best practices

- Keep Always Ask or Plan mode for complex or risky changes; Never Ask runs fully unattended, including sensitive access and plan exits.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html>
- Write `/goal` objectives with a finish line and verification evidence; avoid open-ended goals such as finding every bug.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/guides/goals.html>
- Use durable allow, deny, and ask rules with exact tool-command patterns; keep the dangerous-command guard enabled unless another control gates commands.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html>
- Verify the installed version before automating a workflow: recent releases changed permission and command behavior.
  — <https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html>

## Superseded by this

- :{
- claim
- Kimi Code CLI guidance to disable experimental micro-compaction through `/experiments` is obsolete: v0.23.0 removed the feature and its toggle.
- obsolete_since
- 2026-07-06
- source_url
- https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html
- claim
- The `kimi server` command tree is deprecated; use foreground `kimi web` and stop it with Ctrl+C.
- obsolete_since
- 2026-07-20
- source_url
- https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html

## Still unknown

- Original wording for the 2026-06-09 event is unavailable, so we cannot tell whether it referred to v0.12.0, v0.12.1, or both; the official changelog records both on that date.
- The interaction guide uses Always Ask, Ask When Needed, and Never Ask, while configuration examples retain `manual`, `yolo`, and `auto`; we did not test label-alias compatibility independently.

## Sources

| source | title | read |
|---|---|---|
| https://moonshotai.github.io/kimi-code/en/ | Kimi Code CLI Docs | 2026-09-07 |
| https://github.com/MoonshotAI/kimi-code | GitHub - MoonshotAI/kimi-code: Kimi Code CLI — The Starting Point for Next-Gen Agents | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/release-notes/changelog.html | Changelog | Kimi Code Docs | 2026-09-07 |
| https://www.kimi.com/code/docs/kimi-code-cli/release-notes/changelog.html | 变更记录 | Kimi Code 文档 | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started.html | Getting started | Kimi Code Docs | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html | Interaction and input | Kimi Code Docs | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/guides/goals.html | Goals | Kimi Code Docs | 2026-09-07 |
| https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html | Configuration files | Kimi Code Docs | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:kimi-code-cli`, thread `public-project-reference`, 1 dated events 2026-06-09 → 2026-06-09.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
