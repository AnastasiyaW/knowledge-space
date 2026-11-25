---
title: ComfyUI Skill Public — Public repository
category: projects
date: 2026-05-14
tags: [comfyui-skill-public, comfyui_skill_public, project, public-repository]
aliases: ["ComfyUI Skill Public", "comfyui-skill-public"]
---

# ComfyUI Skill Public — Public repository

**Development line:** `project:comfyui-skill-public` · thread `public-repository`  
**Last event:** 2026-05-14 · 1 dated since 2026-05-14 · **Researched:** 2026-09-05 · confidence: medium

## What it is

comfyui-skill-public: a portable ComfyUI skill for agents and operators working across unfamiliar local, remote, or cloud installs.

- Discovers node classes and model values before building a workflow.
- Covers FLUX 2 image work, LTX 2.3 and WAN 2.2 video, JoyCaption prompting, LoRA training, batches, and recovery.
- Uses REST plus WebSocket job tracking rather than a GUI.

## Development line

- **2026-05-14 — ComfyUI Skill Public GitHub repository referenced.** On 2026-05-14, the record recorded a link to the GitHub repository for ComfyUI Skill Public. The available evidence establishes the repository reference, but does not establish a specific release, feature, or code change.

## What changed

2026-03-28 — comfyui-skill-public: the initial public portable package separated trigger/routing guidance from machine-specific setup. 2026-04-11 — Added LTX 2.3 guidance, batch state/recovery, reference implementations, dependency guidance, demo workflows, and a LoRA-training path. 2026-04-12 — Added FLUX 2 and WAN 2.2 prompting guides plus a first-time setup decision flow. 2026-04-25 — Added a batch monitoring and recovery SOP. 2026-04-26 — Aligned setup and cron documentation. 2026-05-14 — A documented public mention described natural-language OpenClaw control; no GitHub implementation change is visible for that date. 2026-06-03 — v1.4.0 added a portable API helper, batch starter, JoyCaption convention, cold-start agent instructions, and more node maps; v1.4.1 explicitly broadened support beyond OpenClaw and replaced demo-as-drop-in guidance with bring-your-own API workflows.

## How to use this

As of 2026-05-14, practitioners can use the linked GitHub repository as a candidate public reference for the ComfyUI skill, while inspecting its contents before relying on any specific capability or release.

1. Clone the repository, then have an AI agent read AGENTS.md or read SKILL.md as an operator; install the listed Python dependencies if using its helper code.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md>
2. For an unknown ComfyUI target, collect its URL, version, node packs, model family, hardware limits, and output rules; verify system_stats, object_info, queue, WebSocket, and a tiny completed prompt first.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/setup.md>
3. Export an existing workflow in ComfyUI API format, then inspect its required nodes, models, encoders, and VAEs through object_info.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md>
4. Deep-copy the workflow, patch only per-job inputs, submit it to prompt, retain the prompt ID, wait for WebSocket completion, and verify outputs through history.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/api.md>
5. For a batch, reuse one client ID and WebSocket connection, persist each job's state, and resume only jobs without verified output.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/batch-operations.md>

## Best practices

- Discover node classes, model filenames, and install-specific values at runtime; do not treat examples as target-machine facts.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/SKILL.md>
- Do not edit a base workflow in place; deep-copy it and patch the copy.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md>
- Do not fire-and-forget batch prompts: block on WebSocket completion and verify every prompt ID with history.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/batch-operations.md>
- Treat bundled demo graphs as examples only; prefer a workflow exported from the target ComfyUI install.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/commit/755d3f66f4ebb1072a75fc7d8d616489c97bacce>

## Superseded by this

- 2026-06-03 — Demo workflows as installation-ready drop-ins: superseded by v1.4.1 guidance to export and adapt the user's own API-format workflow.
- 2026-06-03 — OpenClaw- and Discord-specific, hard-coded controller assumptions: superseded by v1.4.0's scheduler-neutral, environment-configured guidance.

## Still unknown

- No first-party commit or GitHub Release is visible for 2026-05-14; the event is supported as a same-day public mention, not a proven code release.
- The original URL now redirects to ComfyUI-Agent-Toolkit, but the rename date and rationale are not exposed.
- GitHub has no published Releases; changelog version labels are documentation, not release-asset proof.
- The GitHub API was unreachable during this check, so repository created_at and pushed_at were not independently verified.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Zambav/comfyui-skill-public | GitHub - Zambav/ComfyUI-Agent-Toolkit | 2026-09-05 |
| https://nnets.ru/news/openclaw-skill-upravlenie-comfyui-komandami-na-estestvennom-yazyke | OpenClaw Skill: управление ComfyUI командами на естественном языке. | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/commits/main | Commits · Zambav/ComfyUI-Agent-Toolkit | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/commit/95fe0bc5ee9cdf9b64db983ea8983d68905dbc9c | v1.4.0: port controller improvements + new hero README | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/commit/755d3f66f4ebb1072a75fc7d8d616489c97bacce | v1.4.1: broaden README to 'any agent' + 'bring your own workflows' | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md | README.md | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/SKILL.md | SKILL.md | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/setup.md | setup.md | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/api.md | ComfyUI-Agent-Toolkit/api.md at main | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/batch-operations.md | ComfyUI-Agent-Toolkit/batch-operations.md at main | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/changelog.md | changelog.md | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/releases | Releases · Zambav/ComfyUI-Agent-Toolkit | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-skill-public`, thread `public-repository`, 1 dated events 2026-05-14 → 2026-05-14.
- **Practical note:** As of 2026-05-14, practitioners can use the linked GitHub repository as a candidate public reference for the ComfyUI skill, while inspecting its contents before relying on any specific capability or release.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
