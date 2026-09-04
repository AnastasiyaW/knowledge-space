---
title: ComfyUI Desktop — ComfyUI Desktop development
category: projects
tags: [comfyui-desktop, project]
aliases: ["ComfyUI Desktop"]
---

# ComfyUI Desktop — ComfyUI Desktop development

**Development line:** `project:comfyui-desktop` · thread `comfyui-desktop`  
**Events:** 2 dated, 2024-11-27 → 2026-01-06 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ComfyUI Desktop, now succeeded by Comfy Desktop, is a local launcher for practitioners who need separate ComfyUI environments instead of maintaining one manual Python installation. - Creates, launches, and manages independent ComfyUI instances. - Keeps each instance’s version, custom nodes, settings, and Python environment separate. - Supports templates, migration from legacy or existing installs, update channels, snapshots, and rollback. Limit: allow at least 4.85 GB per standalone install and 8 GB RAM; 16 GB is recommended. Windows 10+ and macOS 13+ on Apple Silicon are documented paths, while current Linux instructions conflict. Verdict: use it for isolated local workflow stacks and recoverable updates; choose portable or manual ComfyUI when you need a platform or core revision Desktop does not clearly cover.

## Development line

- **2024-11-27 — ComfyUI Desktop became available as an open-source project.** On 2024-11-27, ComfyUI made its Desktop application available as an open-source project. The linked repository and user-guide references identify this as a public product-line milestone. The sealed links do not establish its exact feature scope, supported platforms, or release details.
- **2026-01-06 — ComfyUI added official AMD ROCm support.** On 2026-01-06, ComfyUI announced official support for AMD ROCm. This is a material platform-compatibility development for the ComfyUI Desktop line. The sealed link alone does not establish the exact Desktop versions, operating systems, hardware, or setup requirements.

## What changed

ComfyUI Desktop development line: - 2024-11-27 — v1 Desktop was open-sourced. The original launch article’s detailed feature set could not be re-read today. - 2026-01-06 — Windows Desktop v0.7.0 added official AMD ROCm support; installation should select ROCm automatically. The release used ROCm 7.1.1 and recommended its preview driver. - Found today (2026-09-04) — the maintained successor is documented as Comfy Desktop: a multi-installation manager rather than the legacy single-install app. It can migrate legacy workflows, nodes, models, inputs, outputs, and settings into a fresh standalone environment. - Found today (2026-09-04) — the old Comfy-Org/desktop repository is archived and points to Comfy-Org/Comfy-Desktop. Limit: current English documentation says Linux has no official installer, while the maintained repository documents Debian/Ubuntu and AppImage installation. Verdict: treat the legacy Desktop app and repository as migration sources, not the current operational baseline.

## How to use this

From 2024-11-27, practitioners can evaluate ComfyUI Desktop through its public source repository and user-guide materials; from 2026-01-06, AMD users should also check the official ROCm-support guidance when assessing a Desktop deployment.

1. Check the documented platform and capacity before installing: Windows 10+ or macOS 13+ on Apple Silicon, with at least 4.85 GB per standalone instance and 8 GB RAM.
  — <https://docs.comfy.org/installation/desktop/overview>
2. On Windows, run the downloaded .exe, launch Comfy Desktop, and create the first installation from the Welcome screen.
  — <https://docs.comfy.org/installation/desktop/windows>
3. On macOS with Apple Silicon, open the .dmg, drag Comfy Desktop to Applications, and launch it.
  — <https://docs.comfy.org/installation/desktop/macos>
4. In the Chooser, create a named Standalone instance on an SSD, then select a workflow template after setup completes.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
5. If an existing portable, Git, or Legacy Desktop installation already contains work, add or migrate it instead of rebuilding models and workflows by hand; verify workflows, nodes, models, and the carried-over URL afterward.
  — <https://docs.comfy.org/installation/desktop/usage/migrate>
6. Use Manage → Update to keep Stable for normal work, or deliberately select Latest on GitHub when a workflow needs newest core commits.
  — <https://docs.comfy.org/installation/desktop/usage/manage>

## Best practices

- Keep incompatible projects in separate Standalone instances so their Python environments, ComfyUI revisions, and custom nodes cannot collide.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
- Use the Stable update channel by default; Latest on GitHub is for intentional testing of newer commits.
  — <https://docs.comfy.org/installation/desktop/usage/manage>
- Create a labeled manual snapshot before adding a node or updating a working stack; snapshots record the ComfyUI commit, node versions, and pip packages and can restore the prior state.
  — <https://docs.comfy.org/installation/desktop/usage/snapshots>
- Leave ComfyUI-Manager at the recommended Standard security level: it permits registered node packs and blocks arbitrary Git sources.
  — <https://docs.comfy.org/installation/desktop/usage/manage>
- If a custom node breaks startup or the interface, disable all custom nodes first, then bisect the set; back up custom_nodes before doing a manual bisect.
  — <https://docs.comfy.org/troubleshooting/custom-node-issues>

## Superseded by this

- 2024-11-27 legacy single-install ComfyUI Desktop guidance: replace it with the current multi-instance Comfy Desktop model and migrate rather than overwrite the old install.
- Pre-2026-01-06 Windows Desktop guidance that assumes NVIDIA-only hardware: v0.7.0 introduced official Windows AMD ROCm support for supported Radeon GPUs and Ryzen AI processors.
- 2026-06-26 Comfy-Org/desktop as the active source repository: it is archived and explicitly superseded by Comfy-Org/Comfy-Desktop.
- 2026-09-04 guidance that Desktop always matches the newest ComfyUI commit: Stable is the default channel; Latest must be selected deliberately.

## Still unknown

- The 2024 launch article did not render when retrieved, so its exact v1 feature set is not independently verified beyond the dated open-source event.
- The current English documentation says Linux is source-only with no official installer, while the maintained Comfy-Desktop repository documents .deb and AppImage installation. Resolve this contradiction from the release artifact before choosing Linux Desktop.
- English documentation now describes the multi-instance successor, while the Chinese Windows page still describes the earlier single-install beta and NVIDIA-only path. The public sources do not state the localization or migration cutoff date.
- The AMD announcement names supported Radeon GPUs and Ryzen AI processors but does not provide a complete current Desktop hardware matrix; validate the exact GPU and driver combination during installation.

## Sources

| source | title | read |
|---|---|---|
| https://blog.comfy.org/open-sourcing-v1-desktop/ | Open Sourcing V1 Desktop | 2026-09-04 |
| https://blog.comfy.org/p/official-amd-rocm-support-arrives | Official AMD ROCm Support Arrives on Windows for ComfyUI Desktop | 2026-09-04 |
| https://github.com/Comfy-Org/desktop | Comfy-Org/desktop — archived and superseded by Comfy-Org/Comfy-Desktop | 2026-09-04 |
| https://github.com/Comfy-Org/Comfy-Desktop | Comfy-Org/Comfy-Desktop — The desktop app for ComfyUI | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/overview | Comfy Desktop Overview | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/windows | Comfy Desktop for Windows | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/macos | Comfy Desktop for macOS | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/instance-management | Instance Management | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/manage | Managing Installations | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/snapshots | Snapshots | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/usage/migrate | Migrate from Legacy Desktop | 2026-09-04 |
| https://docs.comfy.org/troubleshooting/custom-node-issues | How to Troubleshoot and Solve ComfyUI Issues | 2026-09-04 |
| https://docs.comfy.org/zh/installation/desktop/windows | Windows Desktop — ComfyUI (Chinese) | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-desktop`, thread `comfyui-desktop`, 2 dated events 2024-11-27 → 2026-01-06.
- **Practical note:** From 2024-11-27, practitioners can evaluate ComfyUI Desktop through its public source repository and user-guide materials; from 2026-01-06, AMD users should also check the official ROCm-support guidance when assessing a Desktop deployment.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
