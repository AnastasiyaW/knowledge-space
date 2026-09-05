---
title: OpenMontage
category: projects
date: 2026-06-28
tags: [openmontage, openmontage-development, project]
aliases: ["OpenMontage"]
---

# OpenMontage

**Development line:** `project:openmontage` · thread `openmontage-development`  
**Last event:** 2026-06-28 · 1 dated since 2026-06-28 · **Researched:** 2026-09-05 · confidence: medium

## What it is

OpenMontage is an automated video pipeline where an AI coding assistant runs research, scripting, assets, editing, and rendering.

- 11 documented pipeline types, from documentary editing to localization.
- Human approval gates and a provider selection log to control each step.

Needs Python 3.10+, FFmpeg, Node.js 18+, and a coding assistant.

This is a local environment for controlled production work, not a one-button cloud editor.

## Development line

- **2026-06-28 — OpenMontage GitHub repository was referenced.** On 2026-06-28, a public link pointed to the OpenMontage GitHub repository. The source material includes no repository snapshot, release notes, or code diffs, marking a public repository reference instead of a code release.

## What changed

- 2026-06-28 — OpenMontage tracked as a separate project via its official repository; no dated description of a specific change exists for this day.
- 2026-06-29 — Added a native ComfyUI provider to generate images and video through a local server.
- 2026-07-15 — Published a reproducible sample of a full news clip built with OpenMontage.

## How to use this

As of 2026-06-28, we use the OpenMontage GitHub repository as the starting reference for source and development context; no installation or workflow change is documented for this date.

1. Install Python 3.10+, FFmpeg, Node.js 18+, and an AI coding assistant; clone the official repository and run `make setup` or the manual equivalent.
  — <https://github.com/calesthio/OpenMontage>
2. Open the project in a coding assistant and provide a brief with duration, topic, format, and asset or API limits.
  — <https://github.com/calesthio/OpenMontage>
3. Choose a pipeline first, then follow its manifest and stage skills instead of running arbitrary scripts.
  — <https://github.com/calesthio/OpenMontage>
4. Review the project draft, script, scene plan, and assets at approval gates before rendering; open local Backlot if needed.
  — <https://github.com/calesthio/OpenMontage>

## Best practices

- Clone only `calesthio/OpenMontage`: a report in June flagged a lookalike repository under another owner as potential malware.
  — <https://github.com/calesthio/OpenMontage/issues/200>
- Pick the pipeline and render runtime early: edit decisions log the runtime, and silent runtime changes violate the process.
  — <https://github.com/calesthio/OpenMontage>
- Use a custom workflow with an explicit `output_node` for local ComfyUI setups; server availability determines readiness on custom paths rather than bundled models.
  — <https://github.com/calesthio/OpenMontage/pull/230>

## Superseded by this

- 2026-06-29 — PR #230 replaced PR #29 by rebasing on main and resolving a .gitignore conflict.

## Still unknown

- No primary dated material describes a functional change on 2026-06-28; event_findings remains empty.
- The report of a lookalike malware repository comes from a GitHub issue, not an independent antivirus audit.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/calesthio/OpenMontage | calesthio/OpenMontage repository and README | 2026-09-05 |
| https://github.com/calesthio/OpenMontage/pull/230 | PR #230: Add native ComfyUI provider | 2026-09-05 |
| https://github.com/calesthio/OpenMontage/discussions/231 | OpenMontage now supports ComfyUI | 2026-09-05 |
| https://github.com/calesthio/OpenMontage/discussions/385 | A 7-Minute Trending-News Show for $0.24 | 2026-09-05 |
| https://github.com/calesthio/OpenMontage/issues/200 | Security warning: lookalike Open-Montage/OpenMontage release behaves like malware | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:openmontage`, thread `openmontage-development`, 1 dated events 2026-06-28 → 2026-06-28.
- **Practical note:** As of 2026-06-28, practitioners can use the OpenMontage GitHub repository as the starting reference for the project's source and development context; no specific installation or workflow change can be inferred.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
