---
title: ComfyUI Setup Manager
category: projects
date: 2026-07-23
tags: [comfyui-setup-manager, comfyui-setup-manager-development, comfyui_setup_manager, project]
aliases: ["ComfyUI Setup Manager"]
---

# ComfyUI Setup Manager

**Development line:** `project:comfyui-setup-manager` · thread `comfyui-setup-manager-development`  
**Last event:** 2026-07-23 · 1 dated since 2026-07-23 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ComfyUI Setup Manager is a terminal TUI and CLI for managing isolated ComfyUI installations.

- Installation lifecycle: installs, launches, inspects, updates, repairs, exports and recreates ComfyUI checkouts.
- Environment isolation: separates the checkout, virtual environment and custom nodes for each install.
- Shared asset libraries: shares model and workflow directories across checkouts to prevent duplicate files.
- Setup profiles: exports and rebuilds installations using portable `.comfyuisetup` reconstruction files.

Current README version: 0.8.8.

Use it for reproducible multi-install ComfyUI maintenance, not as a replacement for ComfyUI Desktop or a guarantee that incompatible nodes can coexist.

## Development line

- **2026-07-23 — ComfyUI Setup Manager repository was publicly referenced.** On 2026-07-23, a public reference linked to the GitHub repository for ComfyUI Setup Manager. This establishes a dated public reference to the project, but does not by itself establish a release, feature change, or repository activity.

## What changed

2026-07-23 — ComfyUI Setup Manager appeared as a standalone GitHub project for reconstructing and maintaining ComfyUI installations; the linked repository is now at version 0.8.8.

## How to use this

As of 2026-07-23, evaluate the repository when testing ComfyUI tooling; its capabilities and safety remain unverified.

1. Check prerequisites: Python 3.10+, Git, internet access and write permissions; on Windows, verify WinGet if Python or Git may be missing.
  — <https://github.com/badgids/comfyui-setup-manager/blob/main/docs/getting-started.md>
2. Install with `install.ps1` on Windows, `install.cmd` in Command Prompt, or `./install.sh` on Linux, WSL2 and macOS.
  — <https://github.com/badgids/comfyui-setup-manager>
3. Run `./comfyui-setup-manager`, select Setup & Install, choose a profile and review the installation; CLI equivalent: `install run --profile vanilla-comfyui --target /path/to/ComfyUI --repository-mode official`.
  — <https://github.com/badgids/comfyui-setup-manager/blob/main/docs/getting-started.md>
4. Before creating multiple installs, configure one external models directory and one workflows directory, then apply them to each managed checkout.
  — <https://github.com/badgids/comfyui-setup-manager>
5. Before an update, run `updates check`; use `updates run --strategy safe` only after reviewing the preflight report.
  — <https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/automation-and-agents.md>

## Best practices

- Treat an exact `.comfyuisetup` export as a reconstruction manifest, not a backup of models, virtual environments or the whole checkout; verify its Python, accelerator and PyTorch ABI before reuse on another machine.
  — <https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/setup-profiles.md>
- Use one shared external model and workflow library to avoid duplicating large checkpoints across stable, experimental and development installations.
  — <https://github.com/badgids/comfyui-setup-manager>
- For unattended use, request JSON or YAML output, create a plan before mutation, inspect exit codes and do not parse the TUI.
  — <https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/automation-and-agents.md>
- Start with a non-critical installation: genuinely incompatible custom-node requirements can still require separate ComfyUI installs.
  — <https://www.reddit.com/r/comfyui/comments/1uzgm6o/i_built_a_setup_manager_because_backing_up_entire/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No dated first-party release or commit confirms what changed specifically on 2026-07-23; later capabilities cannot be assigned to that date without evidence.
- The release notes document feature sets from 0.8.0 through 0.8.7 but omit release dates.
- The project repository describes version 0.8.8, but the release notes page provides no dated release evidence for 0.8.8.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/badgids/comfyui-setup-manager | ComfyUI Setup Manager README | 2026-09-05 |
| https://github.com/badgids/comfyui-setup-manager/blob/main/docs/getting-started.md | Getting started | 2026-09-05 |
| https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/automation-and-agents.md | Automation and AI agent use | 2026-09-05 |
| https://git.hubp.de/badgids/comfyui-setup-manager/blob/main/docs/setup-profiles.md | Portable setup profiles | 2026-09-05 |
| https://github.com/badgids/comfyui-setup-manager/blob/main/RELEASE_NOTES.md | Release notes | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1uzgm6o/i_built_a_setup_manager_because_backing_up_entire/ | I built a setup manager because backing up entire ComfyUI installs was getting ridiculous | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-setup-manager`, thread `comfyui-setup-manager-development`, 1 dated events 2026-07-23 → 2026-07-23.
- **Practical note:** As of 2026-07-23, evaluate the repository when testing ComfyUI setup tooling; its capabilities and safety remain unverified.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
