---
title: Origin — Code hosting
category: projects
date: 2026-08-19
tags: [code-hosting, cursor, origin, project]
aliases: ["Origin"]
---

# Origin — Code hosting

**Development line:** `project:origin` · thread `code-hosting`  
**Last event:** 2026-08-19 · 1 dated since 2026-08-19 · **Researched:** 2026-09-05 · confidence: high

## What it is

Origin is Cursor’s early-beta Git forge for paid Cursor users.

- Native repositories: host code with Origin as the source of truth.
- GitHub mirroring: mirror repositories while GitHub remains the source of truth.
- Code search and browsing: search and inspect code in the repository.
- Pull-request review: review diffs and checks before merging.
- Agent connections: connect cloud agents and automations to repositories.

Use it for Cursor-native code workflows or a GitHub mirror, but treat its API and beta contracts as changeable.

## Development line

- **2026-08-19 — Origin reached a code-hosting development milestone.** Native repositories, GitHub mirroring, code browsing, pull requests, and Cursor agents; the launch page itself is dated 2026-08-17.

## What changed

- 2026-08-19 — Origin entered early-beta rollout: native repositories, GitHub mirroring, code browsing, pull requests, and Cursor agents; the launch page itself is dated 2026-08-17.
- 2026-08-26 — The public API added repository labels and check-run annotations; reviewer webhook payloads changed shape.
- 2026-08-27 — The API specification became more generator-friendly and added optional check-run deadlines.
- 2026-08-28 — Passed deadlines began completing in-progress check runs as timed out; the API added repository tarballs and comparison-file listing.
- 2026-08-29 — API support expanded for requested reviewers, resolvable review threads, inline comments, and atomic review comments.
- 2026-09-01 — Repository-deletion and metadata-update webhooks were added.
- 2026-09-02 — List endpoints for check suites and check runs changed to return only the latest attempt, hiding superseded retries from normal listings.
- 2026-09-03 — Check-run and pull-request-comment listing gained filters for incremental polling.
- 2026-09-04 — App `slug` was removed from API and webhook actor metadata; integrations must use app `id` and optional `displayName`.

## How to use this

From 2026-08-19, practitioners evaluating code-hosting workflows should include Origin in their research, while confirming its exact capabilities and availability from primary documentation.

1. Confirm that your account has Origin access, claim a codebase namespace, and choose it carefully: it cannot be renamed during the beta.
  — <https://cursor.com/docs/origin>
2. Create a native repository from Codebase → New, select Internal or Private visibility, then copy its clone URL.
  — <https://cursor.com/docs/origin/create-repository>
3. Authenticate with the Origin CLI and clone or add the standard Git HTTPS remote; then push your branch.
  — <https://cursor.com/docs/origin/git>
4. For an existing GitHub repository, use Sync from GitHub; Origin becomes a mirror while GitHub remains authoritative for pushes.
  — <https://cursor.com/docs/origin/mirror-github>
5. Open a pull request after pushing a branch, review checks and diffs, request reviewers, then merge after review and CI pass.
  — <https://cursor.com/docs/origin/pull-requests>
6. Attach Cursor cloud agents or automations when you want agents to clone, branch, commit, push, or open pull requests against the repository.
  — <https://cursor.com/docs/origin/integrations>

## Best practices

- Treat a GitHub-synced repository as a mirror: GitHub Issues, Actions configuration, and secrets are not copied into Origin, and GitHub remains the source of truth.
  — <https://cursor.com/docs/origin/mirror-github>
- Choose the namespace before enabling Origin; beta namespaces cannot be changed or updated after claiming.
  — <https://cursor.com/docs/origin>
- For integrations, regenerate from the current OpenAPI specification and migrate app identity handling from `slug` to `id` plus optional `displayName`.
  — <https://cursor.com/docs/api/origin/changelog>
- Poll new pull-request comments with `since` or `until` filters rather than repeatedly paging an entire comment history.
  — <https://cursor.com/docs/api/origin/changelog>

## Superseded by this

- 2026-08-27 — guidance that an expired `deadlineAt` does not change a check-run status was superseded on 2026-08-28: expired in-progress runs now complete as `timed_out`.
- 2026-09-02 — integrations relying on list endpoints to expose every check attempt are obsolete: normal list responses now retain only the latest attempt; fetch a specific ID for superseded attempts.
- 2026-09-04 — integrations using app `slug` as an app-actor identifier are obsolete; use app `id` and optional `displayName`.

## Still unknown

- The supplied event date is 2026-08-19, but Cursor’s primary launch page is dated 2026-08-17; we retain 2026-08-19 as the event date.
- No independent production-use evidence was found for Origin; feature availability is documented as staged and early beta. Most post-launch changes found were API changes rather than a dated product-release narrative.

## Sources

| source | title | read |
|---|---|---|
| https://cursor.com/changelog/origin-code-hosting | Origin Code Hosting · Cursor | 2026-09-05 |
| https://cursor.com/docs/origin | Origin | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/create-repository | Create an Origin repository | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/git | Clone, Push & Pull | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/mirror-github | Mirror a GitHub repository | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/pull-requests | Pull requests | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/integrations | Origin integrations | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/api/origin/changelog | Origin API Changelog | Cursor Docs | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:origin`, thread `code-hosting`, 1 dated events 2026-08-19 → 2026-08-19.
- **Practical note:** From 2026-08-19, practitioners evaluating code-hosting workflows should include Origin in their research, while confirming its exact capabilities and availability from primary documentation.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
