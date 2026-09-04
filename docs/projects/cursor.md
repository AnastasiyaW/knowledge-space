---
title: Cursor — Product development
category: projects
date: 2026-06-29
tags: [cursor, product-development, project]
aliases: ["Cursor"]
---

# Cursor — Product development

**Development line:** `project:cursor` · thread `product-development`  
**Last event:** 2026-06-29 · 1 dated since 2026-06-29 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Cursor is a coding editor and agent for developers who need to understand a repository, delegate edits, and merge changes.

- Codebase indexing to map the repository, plan features, write code, fix bugs, and review diffs.
- Cross-platform runtime across the desktop app, isolated cloud VMs, web, and iOS, with session handoff between local and cloud runs.
- Context injection through Rules, `AGENTS.md`, skills, and MCP for repository-specific guidance.

## Development line

- **2026-06-29 — Cursor announced an iOS mobile app.** Cursor announced its iOS mobile app on 2026-06-29 in a blog post and an App Store listing. The release expands the editor onto iOS devices. The announcement links confirm the release date, but they omit specific features, regional availability, and final release status.

## What changed

Cursor evolved from a single web entry point into a multi-device agent workspace.

- 2023-08-21 — `cursor.so` served as the original public address. The site now redirects and drops earlier feature descriptions, leaving no verifiable feature baseline for that date.
- 2026-04-02 (found today) — Cursor 3 added a unified multi-workspace agent interface with parallel local and cloud agents, session handoffs, diff and PR workflows, an integrated browser, and plugins.
- 2026-06-29 — Cursor shipped a native iOS app in public beta to launch cloud agents, control local agents remotely, track notifications, inspect artifacts, and merge PRs.
- 2026-09-04 (found today) — Current documentation links iOS to the shared desktop and web agent backend. It lists Cloud Agent entry points across desktop, web, iOS, Slack, source-control comments, Linear, and the API.

## How to use this

From 2026-06-29, test Cursor's iOS app alongside current workflows if mobile access is needed. The dated sources provide no basis for a full migration or broader feature recommendations.

1. Install the desktop application, authenticate, and open the project directory.
  — <https://cursor.com/docs/get-started/quickstart>
2. Ask Agent to explain repository structure, entry points, and primary modules before proposing edits.
  — <https://cursor.com/docs/get-started/quickstart>
3. Start with a small, low-risk change, and switch to Plan Mode for research, multi-file tasks, or sensitive approvals.
  — <https://cursor.com/docs/get-started/quickstart>
4. Add repository instructions under `.cursor/rules/*.mdc`, or place a root `AGENTS.md` file for global project guidance.
  — <https://cursor.com/docs/rules>
5. Review generated diffs, then run existing test suites, type checks, linters, or builds before accepting any change.
  — <https://cursor.com/docs/get-started/quickstart>
6. Connect source control for background tasks, configure the Cloud Agent runtime in an isolated VM, and inspect the resulting artifacts, diffs, and pull requests.
  — <https://cursor.com/docs/cloud-agent>
7. Sign in on iPhone or iPad, select the repository and target branch, instruct the agent, and review or merge pull requests away from the desk.
  — <https://cursor.com/docs/cloud-agent/mobile>

## Best practices

- Keep project Rules scoped and under 500 lines so they remain actionable. Split oversized rule sets, reference canonical files instead of copying text, and commit them to Git.
  — <https://cursor.com/docs/rules>
- Supply repository context before delegating work. Test a small edit before attempting broad changes, and run Plan Mode when implementation requires research or sign-off.
  — <https://cursor.com/docs/get-started/quickstart>
- Configure Cloud Agent environments before running tasks. Inject secrets via the dashboard, use OIDC rather than long-lived cloud keys, allowlist required outbound network routes, and run tests without external dependencies.
  — <https://cursor.com/docs/cloud-agent/best-practices>
- Treat all agent output as draft work. Inspect the diff and run repository checks before deciding to merge.
  — <https://cursor.com/docs/get-started/quickstart>
- Run Quick Agent Review for brief sanity checks. Apply Deep review for complex logic, security-sensitive edits, or large refactors.
  — <https://cursor.com/docs/agent/agent-review>

## Superseded by this

- 2023-08-21 — `cursor.com` replaces the legacy `cursor.so` domain. The old URL redirects to the new site, and current setup steps live in official documentation.
- 2026-04-02 — Single-editor desktop assumptions are obsolete. Cursor 3 coordinates local and cloud agents across multiple workspaces while keeping IDE-level inspection.
- 2026-06-29 — Treating mobile apps as read-only notification feeds is outdated. The native iOS client initiates and steers agents, inspects output, and merges pull requests.

## Still unknown

- The 2023 source redirects to the main site without preserving original launch notes, version numbers, or feature details.
- The June 2026 post describes iOS as a public beta. Current documentation details its features but omits whether it reached general availability.
- Current documentation does not clarify active model choices, subscription tiers, pricing limits, or regional App Store availability.

## Sources

| source | title | read |
|---|---|---|
| https://www.cursor.so/ | AI Coding Agent for Building Ambitious Software | Cursor | 2026-09-04 |
| https://cursor.com/blog/cursor-3 | Meet the new Cursor | Cursor | 2026-09-04 |
| https://cursor.com/blog/ios-mobile-app | Build from anywhere with Cursor for iOS | Cursor | 2026-09-04 |
| https://apps.apple.com/app/cursor/id6767085653 | Cursor App | App Store | 2026-09-04 |
| https://cursor.com/docs/get-started/quickstart | Quickstart | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/rules | Rules | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/cloud-agent | Cloud Agents | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/cloud-agent/best-practices | Cloud Agent Best Practices | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/agent/agent-review | Agent Review | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/cloud-agent/mobile | Cursor for iOS | Cursor Docs | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:cursor`, thread `product-development`, 1 dated events 2026-06-29 → 2026-06-29.
- **Practical note:** From 2026-06-29, teams needing mobile support should evaluate Cursor's iOS client alongside current tools. The reviewed links do not support a broader platform migration or feature rollout.
- **Confidence:** medium. Dated supersedes above remain the source for obsolete workflows.
