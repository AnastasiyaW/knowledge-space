---
title: OpenCut
category: projects
date: 2026-07-18
tags: [opencut, opencut-development, project]
aliases: ["OpenCut"]
---

# OpenCut

**Development line:** `project:opencut` · thread `opencut-development`  
**Last event:** 2026-07-18 · 1 dated since 2026-07-18 · **Researched:** 2026-09-05 · confidence: medium

## What it is

OpenCut is an MIT-licensed video editor for creators who want a CapCut workflow.

- Web workspace: provides a public early-beta entry point.
- Multiplatform rewrite: uses a Rust core for web, desktop, and mobile.
- v0.3.0 release: documents masks, keyframe curves, speed controls, volume controls, and caption import from transcript files.

## Development line

- **2026-07-18 — OpenCut website and source repository were publicly referenced.** On 2026-07-18, a post linked the project website and GitHub repository. We track it because it directs readers to the site and source code. The post does not show whether this was a launch, a release, or a feature update.

## What changed

2026-07-18 — OpenCut was reachable at opencut.app and the OpenCut-app/OpenCut repository. The linked pages show no versioned release or feature change on that date.

## How to use this

As of 2026-07-18, start from the official OpenCut website and GitHub repository to evaluate or adopt the project.

1. Open the official site and select “Try early beta” to enter the project workspace.
  — <https://opencut.app/>
2. For rewrite development, clone the main repository, install Proto, and run `proto use` to install the tools pinned in `.prototools`.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>
3. Run the required local target: `moon run web:dev`, `moon run api:dev`, or `moon run desktop:dev`.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>

## Best practices

- Pin the toolchain with `proto use` before running Moon tasks.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>
- Treat plugins, MCP, headless mode, and scripting as planned work, not active dependencies.
  — <https://github.com/OpenCut-app/OpenCut/issues/811>
- Check architecture plans before submitting code: the project says outside contributions are closed during redesign.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>

## Superseded by this

- 2026-05-17 — Contribution guidance for opencut-classic is obsolete: the owner archived the repository and dropped maintenance.
- 2026-05-26 — Treating the Editor API, cross-platform plugins, MCP server, headless rendering, or in-editor scripting as shipped features is obsolete: they remain rewrite targets without delivery dates.

## Still unknown

- We do not know whether 2026-07-18 marked a release, an availability change, or a reference to existing entry points.
- The site calls its entry point an early beta, but the README says opencut.app still runs the classic editor.
- We found no first-party Simplified-Chinese documentation or announcements.
- The project gives no release date for the rewrite, plugins, MCP, headless mode, scripting, desktop, or mobile builds.
- The GitHub release line ends at v0.3.0 on 2026-04-15; official sources do not say which release backs the early beta.
- Unrelated forks and mirrors use the OpenCut name; this page covers only OpenCut-app/OpenCut and opencut.app.
- We found no verified current desktop or mobile distribution channel.
- The legacy repository and rewrite repository follow different contracts, with no documented feature parity.
- The early beta renders via JavaScript, leaving the editing workflow undocumented in text.
- We found no first-party changelog entry after the rewrite announcement.
- Early beta storage, export, and privacy match only what the project self-reports.
- Non-developer users have no confirmed way to access planned automation tools today.
- Official sources do not list supported browsers, operating systems, GPUs, or video codecs for the beta.
- Release notes for v0.3.0 describe the desktop app as early and bare, with no dated change since.
- We do not know if projects created in the early beta open in the archived classic editor.
- We found no official package manager, installer, or signed desktop release.
- The “Try early beta” button opens a workspace, but documents do not describe account rules or project storage.
- The planned MCP server, plugin host, headless mode, and scripting tab have no release notes.
- The repository rejects outside pull requests while architecture documentation is prepared, with no end date given.
- There is no published service-level commitment or support policy for the early beta.
- A Rust core is a stated rewrite direction, not proof that current editor features use it.
- We found no first-party Chinese-language source to verify terms, support, or regional availability.
- The old release feature list does not prove feature parity with the web workspace.
- Linked pages establish identity, but not the private context of the 2026-07-18 post.

## Sources

| source | title | read |
|---|---|---|
| https://opencut.app/ | OpenCut | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut | OpenCut-app/OpenCut repository | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut/blob/main/README.md | OpenCut README | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut/releases | OpenCut releases | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut/issues/811 | Tracking: OpenCut rewrite | 2026-09-05 |
| https://github.com/OpenCut-app/opencut-classic | OpenCut legacy repository | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:opencut`, thread `opencut-development`, 1 dated events 2026-07-18 → 2026-07-18.
- **Practical note:** As of 2026-07-18, practitioners should use the official OpenCut website and GitHub repository as the starting points for evaluating or adopting the project, pending review of the linked content.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
