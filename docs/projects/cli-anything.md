---
title: CLI-Anything
category: projects
date: 2026-03-11
tags: [agent_tools, cli-anything, cli-anything-development, project]
aliases: ["CLI-Anything"]
---

# CLI-Anything

**Development line:** `project:cli-anything` · thread `cli-anything-development`  
**Last event:** 2026-03-11 · 1 dated since 2026-03-11 · **Researched:** 2026-09-05 · confidence: high

## What it is

CLI-Anything is an HKUDS project for two tasks: install an existing CLI via CLI-Hub, or generate a Python/Click harness for open-source software.

- JSON output for machine parsing
- REPL for interactive sessions
- Undo and redo for state rollback
- Tests for harness validation
- SKILL.md for agent integration

CLI-Hub requires Python 3.10+.

Use CLI-Hub for an existing tool. Run the generator when the harness is missing and the target application can be tested locally.

## Development line

- **2026-03-11 — CLI-Anything GitHub repository surfaced in the agent_tools thread.** On 2026-03-11, the HKUDS/CLI-Anything GitHub repository was linked in the agent_tools thread. The link provides a dated reference in the reviewed source. The evidence shows no release, version, feature change, or milestone.

## What changed

- **2026-03-11** — Zoom harness added as the 11th supported application. A separate post from that day reported 4,4k+ GitHub stars, 9 applications, and 1 436 tests; do not treat these early counts as a permanent catalog or current metric.
- **2026-03-12** — Codex integration added.
- **2026-03-16** — Phase 6.5 added to generate SKILL.md automatically for each harness.
- **2026-03-17** — CLI-Hub launched to search, install, and run ready-made CLIs.
- **2026-03-30** — v0.2.0 reworked HARNESS.md around progressive disclosure.
- **2026-04-18** — SKILL.md files consolidated in the root skills/ directory.
- **2026-04-24** — v0.3.0 added new harness tools, including CloudCompare, IntelWatch, VideoCaptioner, and Slay the Spire II.
- **2026-06-02** — CLI-Anything: Towards Agent-Native Computer Use paper published, defining the shift from screen GUI automation to structured CLIs.
- **2026-06-25** — v0.4.0 added CLI-Matrix, 30 new CLIs, 17 fixes, and four security hardenings.

## How to use this

As of 2026-03-11, practitioners should treat CLI-Anything as a project requiring source-level evaluation before adoption; the dated link alone provides no verified capability, release, or compatibility claim.

1. For an existing tool, install CLI-Hub with pip install cli-anything-hub. Find it with cli-hub search <query>, inspect it with cli-hub info <name>, install it with cli-hub install <name>, and run cli-hub launch <name> --help.
  — <https://clianything.cc/docs.html>
2. For software missing from the catalog, prepare Python 3.10+, source code or an accessible repository, and a supported coding agent. In Claude Code, connect the marketplace and run /cli-anything <path-or-repo>.
  — <https://github.com/HKUDS/CLI-Anything>
3. After generation, install the harness from its agent-harness directory with pip install -e .. Check commands with --help and use --json for machine parsing.
  — <https://github.com/HKUDS/CLI-Anything>

## Best practices

- Search CLI-Hub for an existing CLI first; use the generator only when the catalog lacks the needed harness.
  — <https://github.com/HKUDS/CLI-Anything>
- Do not treat a generated CLI as complete after one run: run refine for identified gaps, then validate and test before production use.
  — <https://github.com/HKUDS/CLI-Anything>
- Install and test the target application: a harness may require GIMP, Blender, LibreOffice, or other upstream software.
  — <https://github.com/HKUDS/CLI-Anything>
- In automation, use --json and exit codes instead of parsing text output.
  — <https://clianything.cc/docs.html>

## Superseded by this

- 2026-03-11: the early description of the project as 9 applications and 1 436 tests is obsolete. Official project history on that date records Zoom as the 11th harness, and v0.4.0 later added 30 more CLIs.
- 2026-03-11: generating a CLI for every request is obsolete. We now check CLI-Hub first to find and install an existing tool from the catalog.
- 2026-03-11: the lack of a Codex workflow became obsolete on 2026-03-12 with the built-in integration.

## Still unknown

- The official project log confirms the 2026-03-11 event, but lacks an immutable repository snapshot from the publication moment. Early counts from the secondary source serve only as event context.
- The output schema does not support event_findings and new_events fields; what_changed stores their contents.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/HKUDS/CLI-Anything | HKUDS/CLI-Anything repository and current README | 2026-09-05 |
| https://clianything.cc/docs.html | CLI-Anything Hub documentation | 2026-09-05 |
| https://github.com/HKUDS/CLI-Anything/releases/tag/v0.4.0 | CLI-Anything v0.4.0 release | 2026-09-05 |
| https://github.com/HKUDS/CLI-Anything/releases | CLI-Anything releases | 2026-09-05 |
| https://arxiv.org/abs/2606.03854 | CLI-Anything: Towards Agent-Native Computer Use | 2026-09-05 |
| https://linux.do/t/topic/1737269?tl=en | CLI-Anything GitHub Trending discussion | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:cli-anything`, thread `cli-anything-development`, 1 dated events 2026-03-11 → 2026-03-11.
- **Practical note:** As of 2026-03-11, practitioners should treat CLI-Anything as a project requiring source-level evaluation before adoption; the dated link alone provides no verified capability, release, or compatibility claim.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
