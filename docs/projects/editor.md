---
title: Pascal Editor
category: projects
date: 2026-07-27
tags: [editor, pascal-editor-development, pascal_editor, project]
aliases: ["Pascal Editor"]
---

# Pascal Editor

**Development line:** `project:editor` · thread `pascal-editor-development`  
**Last event:** 2026-07-27 · 1 dated since 2026-07-27 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Pascal Editor is an open-source 3D building editor with a semantic scene graph.

- Runs as a hosted editor or a persistent local CLI runtime.
- Exposes MCP tools for project and scene editing, validation, and saving.
- Publishes reusable React packages for embedding.

## Development line

- **2026-07-27 — Pascal Editor GitHub repository linked.** On 2026-07-27, we linked the project's GitHub repository. This gives a public project reference, but documents no release, feature, ownership change, or repository state.

## What changed

- 2026-04-09 — Hosted Pascal v1.0.0 launched with a semantic scene graph for people and AI agents.
- 2026-04-14 — Hosted v1.1.0 added AI layout generation and a photorealistic rendering tab.
- 2026-05-05 — Hosted v1.2.0 added agent-driven editing and SAM3D image-to-3D.
- 2026-06-09 — Hosted v1.3.0 added presets, room templates, and improved manipulation.
- 2026-06-10 — Open-source v0.9.1 published core, viewer, and editor packages at 0.9.1; the announced v0.9.0 packages never reached npm.
- 2026-06-21 — Hosted v1.4.0 added materials, first-person walkthroughs, and MEP tools.
- 2026-07-08 — Hosted v1.5.0 added a rebuilt Studio, the first editor plugin, and lingo unit input.
- 2026-07-27 — No retrieved first-party release or changelog entry identifies a shipped change on this date; the repository reference is an identity pointer, not a release boundary.
- 2026-07-30 — Hosted v1.6.0 added terrain and vertical-construction workflows; the related open-source packages shipped separately as v1.0.0-beta.1.
- 2026-08-03 — Hosted v1.7.0 added team editing, shared cursors and cameras, shared AI chat, and Material Studio.
- 2026-08-11 — Hosted v1.8.0 added the Pascal CLI and agent accounts.
- 2026-08-26 — Hosted v1.9.0 added Bones, Pascal Capture mesh scanning, and block modeling.

## How to use this

As of 2026-07-27, use the linked Pascal Editor GitHub repository as the project's reference point, and verify its capabilities and release status directly before relying on it.

1. Choose a project store first: use hosted MCP for Pascal account or organization projects, or the local CLI for local SQLite projects; they do not share data.
  — <https://editor.pascal.app/docs/developers/mcp>
2. For a local editor, install Node.js 22.13+ and run `npx @pascal-app/cli editor`.
  — <https://editor.pascal.app/docs/developers/local-editor>
3. Connect a local agent with `pascal mcp setup <codex|claude>` or `pascal mcp connect`; configure the hosted endpoint only for hosted projects.
  — <https://editor.pascal.app/docs/developers/mcp>
4. For an existing scene, use `list_scenes` then `load_scene`, make semantic edits, run `validate_scene` and `verify_scene`, then `save_scene` and `get_project_status`.
  — <https://editor.pascal.app/docs/developers/mcp>
5. To embed the editor, install the published packages and load the built-in plugin before mounting the viewer.
  — <https://github.com/pascalorg/editor>

## Best practices

- Do not adopt `v1.0.0-beta.1` accidentally: it is a prerelease on npm's `beta` tag, while `latest` remains on the 0.x line.
  — <https://github.com/pascalorg/editor/releases/tag/v1.0.0-beta.1>
- For a local-runtime failure, run `doctor`, then `status`, then inspect logs before using a forced stop.
  — <https://editor.pascal.app/docs/developers/local-editor>
- Prefer semantic scene tools over raw patches and finish every agent edit with validation, verification, saving, and a project-status check.
  — <https://editor.pascal.app/docs/developers/mcp>
- For source contributions, run `bun check` and `bun run test`; bare `bun test` does not run the workspace test script.
  — <https://github.com/pascalorg/editor/blob/main/CONTRIBUTING.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No first-party release or changelog entry was found for 2026-07-27, so no capability or version can safely be assigned to that date.
- The hosted product changelog and open-source package releases use different version numbers; the July 30 release explains that distinction, but no complete later cross-version compatibility matrix was found.
- No official Chinese-language documentation or independently reproducible Chinese operating report was found, so no Chinese practice is included.
- The local CLI documentation still describes Linux and Windows support as unverified in its initial release; a current platform support matrix was not found.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/pascalorg/editor | Pascal Editor — GitHub repository | 2026-09-06 |
| https://editor.pascal.app/changelog | Changelog | Pascal Editor | 2026-09-06 |
| https://github.com/pascalorg/editor/releases/tag/v0.9.1 | Release v0.9.1 — Preset System, Rooms & Templates, Building Manipulation | 2026-09-06 |
| https://editor.pascal.app/changelog/2026-07-30-terrain-and-community | Shape the ground, then build on it | Changelog | Pascal Editor | 2026-09-06 |
| https://github.com/pascalorg/editor/releases/tag/v1.0.0-beta.1 | Release Pascal Editor 1.0.0-beta.1 | 2026-09-06 |
| https://editor.pascal.app/docs/developers/local-editor | Run Pascal locally - Pascal | 2026-09-06 |
| https://editor.pascal.app/docs/developers/mcp | Connect an AI agent - Pascal | 2026-09-06 |
| https://github.com/pascalorg/editor/blob/main/CONTRIBUTING.md | Contributing to Pascal Editor | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:editor`, thread `pascal-editor-development`, 1 dated events 2026-07-27 → 2026-07-27.
- **Practical note:** As of 2026-07-27, use the linked Pascal Editor GitHub repository as the project's reference point, and verify its capabilities and release status directly before relying on it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.