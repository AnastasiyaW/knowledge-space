---
title: ComfyUI Mobile Frontend
category: projects
date: 2026-08-12
tags: [comfyui-mobile-frontend, comfyui_mobile_frontend, project]
aliases: ["ComfyUI Mobile Frontend"]
---

# ComfyUI Mobile Frontend

**Development line:** `project:comfyui-mobile-frontend` · thread `comfyui-mobile-frontend`  
**Last event:** 2026-08-12 · 1 dated since 2026-08-12 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ComfyUI Mobile Frontend is a custom node for people who run ComfyUI and want to edit workflows, monitor queues, and manage outputs from a phone or tablet.

- Browser UI served at `/mobile`.
- Workflow editor for touch devices.
- Queue and history monitoring.
- Output and media viewer.

Custom-node support is incomplete, and the project labels itself experimental. Latest published release found is v3.2.5 from 2026-08-25. Use it on a trusted personal ComfyUI server after testing the workflows and nodes you need.

## Development line

- **2026-08-12 — ComfyUI Mobile Frontend public references were shared.** On 2026-08-12, the ComfyUI Mobile Frontend development line was linked to its GitHub repository and the CueForge website. This creates a dated public reference point for the project, though the shared links do not document a release, a feature set, or another specific milestone.

## What changed

2026-08-12 — v3.1.3 improved output browsing, workflow controls, and wildcard handling.

## How to use this

From 2026-08-12, practitioners could use the linked GitHub repository and CueForge website as starting references when evaluating ComfyUI Mobile Frontend; take no specific capability, version, or release status from this event alone.

1. Install it through ComfyUI-Manager under author `cosmicbuffalo`, or clone the repository into ComfyUI’s `custom_nodes` directory.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend>
2. Restart ComfyUI, then open `http://<server-ip>:8188/mobile`; use ComfyUI’s `--listen` option when accessing it from another device on the LAN.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend>
3. Load a workflow; when nodes are missing, use the dialog to open the Custom Nodes Manager filtered to the missing node types.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/USER_GUIDE.md>

## Best practices

- Test the exact custom-node workflows you need before relying on the mobile interface, because automatic support for all custom nodes is not available.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend>
- Do not expose a ComfyUI server to untrusted clients; place it behind authentication, a VPN, or a reverse proxy. Disable CueForge pairing with `COMFYUI_MOBILE_APP_PUSH=0` if it is not wanted.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/CUEFORGE_PRIVACY.md>

## Superseded by this

- 2026-08-16 — v3.2.0 superseded English-only interface guidance by adding Simplified Chinese, Traditional Chinese, Japanese, and Korean.
- 2026-08-25 — v3.2.5 superseded v3.2.4 as the latest published release, adding client-paced progress-socket support and a subgraph-combo fix.

## Still unknown

- CueForge is a separate iOS client, not a version of the custom node. Its retrieved official page says it is coming soon to the App Store, but no dated first-party launch record was found.
- The retrieved main-branch changelog labels v3.2.5 “Unreleased” while the official Releases page lists v3.2.5 as the latest published release dated 2026-08-25; use the release page for published-version selection.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend | ComfyUI Mobile Frontend repository | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/releases | ComfyUI Mobile Frontend releases | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/releases/tag/v3.0.0 | Release v3.0.0 | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/releases/tag/v3.1.0 | Release v3.1.0 — Another big UX release | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/USER_GUIDE.md | ComfyUI Mobile User Guide | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/CUEFORGE_PRIVACY.md | What this custom node sends to CueForge | 2026-09-05 |
| https://cueforge.dev/ | CueForge — ComfyUI on iPhone | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-mobile-frontend`, thread `comfyui-mobile-frontend`, 1 dated events 2026-08-12 → 2026-08-12.
- **Practical note:** From 2026-08-12, practitioners could use the linked GitHub repository and Cueforge website as starting references when evaluating ComfyUI Mobile Frontend; no specific capability, version, or release status should be inferred from this event alone.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
