---
title: Comfy Desktop — ComfyUI
category: projects

tags: [comfy-desktop, comfyui, project]
aliases: ["Comfy Desktop"]
---

# Comfy Desktop — ComfyUI

**Development line:** `project:comfy-desktop` · thread `comfyui`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-07 · confidence: medium

## What it is

Comfy Desktop is an official launcher and multi-instance manager for people who want local ComfyUI without separately maintaining each Python environment.

- Instance management: installs, launches, updates, and tracks independent ComfyUI instances.
- Environment isolation: separates versions, custom nodes, and settings while allowing shared model storage.
- Snapshots: records snapshots for rollback and reproducible instance setups.

Current docs support Windows 10+ and macOS 13+ on Apple Silicon, with 4.85 GB per standalone install and 8 GB RAM minimum. Linux guidance conflicts between official docs and the repository. We use it to isolate experimental and production node stacks. Do not assume a tracked legacy install has snapshot support.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-06-04 — Comfy Desktop — a rebuilt multi-instance manager began phased rollout, replacing the older bundled-desktop model.
- 2026-06-09 — Comfy Desktop — the recorded link points to an original post displayed as June 8; it describes a rebuilt app that keeps existing workflows, custom nodes, models, and settings.
- 2026-06-16 — Comfy Desktop — documentation corrected snapshot guidance: snapshots were then Standalone-only, not available to tracked Portable or Git installs.
- 2026-06-23 — Comfy Desktop — ComfyUI v0.26.0 release notes updated the link to the new desktop repository and product references to “Comfy Desktop.”
- 2026-06-26 — Comfy Desktop — the legacy `desktop` repository was archived and explicitly superseded by `Comfy-Desktop`.
- 2026-08-28 — Comfy Desktop — v1.0.46 shipped on the stable channel; the observed release page marked it Latest.
- 2026-09-03 — Comfy Desktop — v1.0.47-rc.1 shipped as an RC pre-release, not the default stable channel.

## How to use this

1. 1. Check the documented platform and storage requirements, then download the supported installer path for Windows or macOS.
  — <https://docs.comfy.org/installation/desktop/overview>
2. 2. Create a Standalone instance for a fresh isolated setup, or add an existing Portable/Git installation when its current environment must remain intact.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
3. 3. Launch the provisioned instance, choose a workflow template, and use Manage to set paths, launch arguments, and per-instance configuration.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
4. 4. Before an update or custom-node change, inspect or create a snapshot; use Stable unless deliberately testing master-branch changes.
  — <https://docs.comfy.org/installation/desktop/usage/manage>

## Best practices

- Use a separate Standalone instance for an experimental node or dependency stack; snapshots capture the ComfyUI commit, custom-node versions, and Python packages.
  — <https://docs.comfy.org/installation/desktop/usage/snapshots>
- Keep the instance update channel on Stable by default; Latest on GitHub is for deliberate testing.
  — <https://docs.comfy.org/installation/desktop/usage/manage>
- Treat tracked Portable and Git installs as manually updated and without snapshot support.
  — <https://docs.comfy.org/installation/desktop/usage/instance-management>
- Keep ComfyUI-Manager on Standard policy; only allow unregistered node sources under a consciously local-only setup.
  — <https://docs.comfy.org/installation/desktop/usage/manage>

## Superseded by this

- 2026-06-04 — Desktop is no longer a single bundled ComfyUI installation; the rebuilt product manages independently configured instances.
- 2026-06-16 — Tracked Portable or Git instances do not support snapshots; the documented scope is Standalone only.
- 2026-06-26 — Treat `Comfy-Org/desktop` as historical evidence, not the current source repository; its own README points to `Comfy-Org/Comfy-Desktop`.

## Still unknown

- Direct retrieval of the X URL returned HTTP 403. We did not capture its full text or media from X; the June 8 correction relies on an accessible secondary rendering.
- The record date is 2026-06-09, while the accessible rendering labels the post June 8. Source-timezone normalization is unverified.
- First-party sources conflict on Linux: official documentation reports no installer, while the Comfy-Desktop README advertises Linux `.deb` and AppImage paths. Verify a current downloadable artifact before treating Linux as supported or unsupported.
- No first-party Simplified-Chinese Desktop guide was verified in this pass; secondary Chinese mirrors were not used for operational claims.
- The legacy repository explicitly names Comfy-Desktop as its successor, so these are not two unrelated subjects. Pre-transition instructions and binaries still need separate attribution.

## Sources

| source | title | read |
|---|---|---|
| https://x.com/ComfyUI/status/2064093003590111314 | ComfyUI status 2064093003590111314 | 2026-09-07 |
| https://easyvibecoding.app/curated/1843-comfy-desktop-launches-multi-instance-management | Comfy Desktop 推出實現多執行個體管理 — EasyVibeCoding | 2026-09-07 |
| https://www.reddit.com/r/comfyui/comments/1tx4qn7/announcing_comfy_desktop_one_app_for_every_comfy/ | Announcing Comfy Desktop: One App for every Comfy | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/overview | Comfy Desktop Overview - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/overview | Using Comfy Desktop - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/instance-management | Instance Management - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/snapshots | Snapshots - ComfyUI | 2026-09-07 |
| https://docs.comfy.org/installation/desktop/usage/manage | Managing Installations - ComfyUI | 2026-09-07 |
| https://github.com/Comfy-Org/docs/discussions/1141 | installation/desktop/usage/instance-management #1141 | 2026-09-07 |
| https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.26.0 | Release v0.26.0 · Comfy-Org/ComfyUI | 2026-09-07 |
| https://github.com/Comfy-Org/desktop | Comfy-Org/desktop: archived and superseded by Comfy-Desktop | 2026-09-07 |
| https://github.com/Comfy-Org/Comfy-Desktop | Comfy-Org/Comfy-Desktop | 2026-09-07 |
| https://github.com/Comfy-Org/Comfy-Desktop/releases | Releases · Comfy-Org/Comfy-Desktop | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfy-desktop`, thread `comfyui`, 0 dated events - → -.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
