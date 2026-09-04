---
title: Cursor — Product development
category: projects
tags: [cursor, product-development, project]
aliases: ["Cursor"]
---

# Cursor — Product development

**Development line:** `project:cursor` · thread `product-development`  
**Events:** 1 dated, 2026-06-29 → 2026-06-29 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Cursor — a coding agent and editor for developers who want to understand a repository, delegate changes, and decide what to merge. - Maps a codebase, plans and builds features, fixes bugs, and reviews changes. - Works across the desktop app, isolated cloud VMs, web, and iOS; agent sessions can move between local and cloud work. - Carries repository-specific instructions through Rules, `AGENTS.md`, skills, and MCP. Limit: Cloud Agents need connected source control and a VM-testable environment with configured secrets and egress; their output remains a review candidate. Verdict: use Cursor to accelerate bounded, testable repository work, then inspect the diff and run normal checks before merge.

## Development line

- **2026-06-29 — Cursor announced an iOS mobile app.** On 2026-06-29, Cursor announced an iOS mobile app, as indicated by the dated Cursor blog link and App Store listing. This marked a material expansion of Cursor's product presence to iOS. The dated links alone do not establish the app's detailed capabilities, regional availability, or release status.

## What changed

Cursor — development line from an early public entry point to a cross-device agent workspace. - 2023-08-21 — `cursor.so` was the linked public entry point. Its current redirect does not preserve the contemporaneous feature set, so no feature-level historical claim is retained. - 2026-04-02 (found today) — Cursor 3 introduced a unified, multi-workspace agent interface: parallel local and cloud agents, handoff between them, diff/PR work, an integrated browser, and plugins. - 2026-06-29 — Cursor released its native iOS app in public beta for launching cloud agents or remotely directing local agents, with notifications, artifact review, and PR merging. - 2026-09-04 (found today) — current documentation places iOS on the same agent backend as desktop and web, and documents Cloud Agent entry points from desktop, web, iOS, Slack, source-control comments, Linear, and API. Limit: the original 2023 page is not an archive of its launch-era capabilities. Verdict: current operating guidance should be based on the reviewed agent workflow, not the old product link.

## How to use this

From 2026-06-29, practitioners who need mobile access should evaluate Cursor's iOS app alongside their existing workflow; the dated links alone do not support a more specific migration or feature recommendation.

1. Install the desktop app, sign in, and open the repository folder.
  — <https://cursor.com/docs/get-started/quickstart>
2. Ask Agent to explain the codebase, entry points, and key modules before requesting a change.
  — <https://cursor.com/docs/get-started/quickstart>
3. Start with a small, low-risk change; use Plan Mode for multi-file, research-heavy, or approval-sensitive work.
  — <https://cursor.com/docs/get-started/quickstart>
4. Add version-controlled repository instructions in `.cursor/rules/*.mdc`, or use a root `AGENTS.md` for simpler global project guidance.
  — <https://cursor.com/docs/rules>
5. Review the generated diff and run the repository's existing tests, type checks, linting, or build before accepting the change.
  — <https://cursor.com/docs/get-started/quickstart>
6. For asynchronous work, connect source control, configure the Cloud Agent environment, start an isolated VM agent, then review its artifacts, diff, and pull request.
  — <https://cursor.com/docs/cloud-agent>
7. On iPhone or iPad, sign in, choose the repository and branch, direct the agent, and review or merge its pull request when away from the desktop.
  — <https://cursor.com/docs/cloud-agent/mobile>

## Best practices

- Keep project Rules focused, actionable, scoped, and under 500 lines; split large rules, cite canonical files instead of copying them, and commit them to Git.
  — <https://cursor.com/docs/rules>
- Give the agent actual repository context first, make a small change before a broad one, and use Plan Mode when implementation needs research or approval.
  — <https://cursor.com/docs/get-started/quickstart>
- Prepare Cloud Agent environments before launch: provide required secrets through the dashboard, prefer OIDC to long-lived cloud keys, whitelist needed egress, and make local testing work without inaccessible services.
  — <https://cursor.com/docs/cloud-agent/best-practices>
- Treat every agent result as reviewable output: inspect the diff and run project checks before merge.
  — <https://cursor.com/docs/get-started/quickstart>
- Use Quick Agent Review for small sanity checks and Deep review for complex logic, security-sensitive changes, or large refactors.
  — <https://cursor.com/docs/agent/agent-review>

## Superseded by this

- 2023-08-21 — the legacy `cursor.so` address is superseded by `cursor.com`; it now redirects there, and current operational guidance lives in the current documentation.
- 2026-04-02 — a desktop-only, single-editor workflow is no longer a sufficient mental model: Cursor 3 coordinates local and cloud agents across multiple workspaces while retaining IDE-level inspection.
- 2026-06-29 — treating mobile as notification-only is obsolete: the native iOS app can start and direct agents, inspect work, and review or merge pull requests.

## Still unknown

- The 2023 source now redirects and does not retain its original announcement text, version, or exact feature set.
- The June 2026 post calls iOS a public beta; current documentation describes the app but does not explicitly state whether it has reached general availability.
- Current model availability, pricing, plan entitlements, and regional App Store availability are not established by the sources reviewed.

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
- **Practical note:** From 2026-06-29, practitioners who need mobile access should evaluate Cursor's iOS app alongside their existing workflow; the dated links alone do not support a more specific migration or feature recommendation.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
