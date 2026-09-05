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

OpenMontage is an automated video production pipeline where an AI coding assistant manages research, scripting, assets, editing, and rendering.

- 11 documented pipeline types, from documentary editing to localization.
- Human approval gates, with a log recording provider choices.

Requires Python 3.10+, FFmpeg, Node.js 18+, and an AI coding assistant.
Built as a repository for controlled local production work, not a one-button cloud editor.

## Development line

- **2026-06-28 — OpenMontage GitHub repository was referenced.** On 2026-06-28, public references pointed to the OpenMontage GitHub repository. No source text, repository snapshot, release record, or description of a code change accompanied it, so this notes the public repository reference rather than a specific implementation milestone.

## What changed

- 2026-06-28 — OpenMontage was documented as a standalone project from its official repository; no dated description of a specific change was found for this day.
- 2026-06-29 — Added a native ComfyUI provider to generate images and videos through a local server.
- 2026-07-15 — Published a reproducible example of a full news video produced with OpenMontage.

## How to use this

As of 2026-06-28, practitioners can use the OpenMontage GitHub repository as the starting reference for the project's source and development context; no specific installation or workflow change can be inferred.

1. Install Python 3.10+, FFmpeg, Node.js 18+, and an AI coding assistant. Clone the official repository and run `make setup` or an equivalent manual install.  
  — <https://github.com/calesthio/OpenMontage>
2. Open the project in the coding assistant and provide a concrete brief covering duration, topic, format, and limits on assets or APIs.  
  — <https://github.com/calesthio/OpenMontage>
3. Choose a suitable pipeline first, then follow its manifest and stage skills instead of bypassing them with ad-hoc scripts.  
  — <https://github.com/calesthio/OpenMontage>
4. Review proposal, script, scene plan, and assets at approval gates before rendering; open local Backlot if needed.  
  — <https://github.com/calesthio/OpenMontage>

## Best practices

- Clone only `calesthio/OpenMontage`: a June report warned of a likely malicious lookalike repository under another owner.  
  — <https://github.com/calesthio/OpenMontage/issues/200>
- Choose the pipeline and render runtime in advance: edit decisions record the runtime choice, and changing runtimes silently breaks the workflow.  
  — <https://github.com/calesthio/OpenMontage>
- Use a custom workflow with an explicit `output_node` for custom ComfyUI setups: readiness on custom paths depends on server availability rather than bundled models.  
  — <https://github.com/calesthio/OpenMontage/pull/230>

## Superseded by this

- 2026-06-29 — PR #230 replaced obsolete PR #29: code was rebased onto current main with the .gitignore conflict resolved.

## Still unknown

- No primary dated source describes a specific functional change on 2026-06-28; event_findings remains empty.
- The reported malicious lookalike comes from a GitHub issue, not an independent antivirus finding.

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
