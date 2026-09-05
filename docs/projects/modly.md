---
title: Modly
category: projects
date: 2026-03-20
tags: [modly, modly-development, project]
aliases: ["Modly"]
---

# Modly

**Development line:** `project:modly` · thread `modly-development`  
**Last event:** 2026-03-20 · 1 dated since 2026-03-20 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Modly is a local alternative to cloud image-to-3D tools such as Meshy for creators who run models on their own hardware.

- 3D mesh generation from an image or text prompt.
- Model and process extensions, including Hunyuan3D 2, TripoSG, and Trellis.
- Desktop app with node workflows, mesh export, and a local CLI.

## Development line

- **2026-03-20 — Modly GitHub repository reference.** On 2026-03-20, Modly’s development line linked to the public GitHub repository github.com/lightningpixel/modly. The link establishes a dated repository reference without identifying a particular release, commit, feature, or operational change.

## What changed

- 2026-03-20 — Modly was recorded at its public GitHub repository; no first-party dated artifact for that exact day's feature scope was retrieved.
- 2026-03-26 — Modly Beta v0.2.1 revised the extension system, trusted-extension handling, and updater.
- 2026-04-03 — Modly Beta v0.3.0 moved the product toward node-based workflows and an extension-centered Models page.
- 2026-04-21 — Modly Beta v0.3.2 added headless `/workflow-runs` execution and embedded Python.
- 2026-04-22 — Modly Beta v0.3.3 added a remesh workflow node.
- 2026-06-21 — Modly Beta v0.4.0 added the agent CLI, local-extension installation, Apple Silicon work, transform controls, and Gaussian-splat viewing.
- 2026-07-16 — Modly Beta v0.4.1 added workflow iteration nodes, audio process outputs, a workflow browser, and Apple Silicon packaging.
- 2026-08-28 — Modly Beta v0.4.2 became the latest tagged beta, fixing extension validation and picker behavior, CLI JSON arguments, Windows UTF-8 subprocess I/O, and workflow-run collection placement.

## How to use this

From 2026-03-20, use the referenced GitHub repository as the starting point for source-level verification of Modly; do not infer releases, capabilities, or usage instructions from this link alone.

1. Check that the target model and platform fit the machine; the official site recommends an NVIDIA CUDA GPU with at least 6 GB VRAM, then download the current beta installer.
  — <https://modly3d.app/>
2. Install an official model extension from the Models page by using “Install from GitHub,” then download its model variant.
  — <https://github.com/lightningpixel/modly>
3. Build a basic graph: Image → Generate Mesh → Add to Scene; select it in Generate, run it, and inspect Settings/Logs/Errors if it fails.
  — <https://github.com/lightningpixel/modly>
4. Preview the mesh and export GLB, OBJ, STL, or PLY for the target DCC, engine, or slicer.
  — <https://modly3d.app/>
5. For automation, launch the desktop app, run `python tools/modly-cli/agent.py health`, inspect models, then use `generate --image ... --output ...` and retain the returned run ID for status or cancellation.
  — <https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md>

## Best practices

- Start with the smallest connected workflow and verify every edge before generating; preserve the mesh view and read the inline error/log panel instead of rebuilding the graph after a failed run.
  — <https://github.com/lightningpixel/modly>
- Use a clean, isolated input image or a specific prompt, then select the installed model variant for speed or fidelity rather than assuming one model fits every task.
  — <https://modly3d.app/>
- For scripted use, prefer the canonical `health`, `model`, and `workflow-run` commands; treat `/generate/*` and experimental ComfyUI helpers as compatibility or experimental paths, not a silent fallback.
  — <https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md>
- Do not treat the desktop installers or stock extension setup as Jetson support: the Jetson guide documents an unsupported path requiring a Jetson-native PyTorch build, NumPy pinning, and a background-removal workaround.
  — <https://github.com/lightningpixel/modly/blob/main/docs/running-on-jetson.md>

## Superseded by this

- The pre-v0.3 model-page-centered workflow is superseded by the node workflow and extension architecture from 2026-04-03.
- The old `/generate/*` automation surface is compatibility-only; canonical automation is the workflow-run contract introduced by the v0.4 line, 2026-06-21.
- Modly Beta v0.4.1 is no longer the latest tagged beta; v0.4.2 superseded it on 2026-08-28.

## Still unknown

- No retrieved first-party release note, tag, or archived repository snapshot fixes the exact Modly feature set on 2026-03-20, so later releases are kept as separate events.
- First-party hardware guidance is not yet a single support matrix: the product site recommends NVIDIA CUDA with 6 GB VRAM, the repository lists Apple Silicon macOS, and the Jetson guide explicitly describes an unsupported workaround.
- A targeted Chinese-language search found secondary coverage but no official Chinese Modly documentation or release record.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/lightningpixel/modly | GitHub - lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/releases | Releases · lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/releases/tag/v0.2.1 | Release Modly Beta v0.2.1 · lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/tags | Tags · lightningpixel/modly | 2026-09-05 |
| https://github.com/lightningpixel/modly/blob/main/tools/modly-cli/SKILL.md | Modly CLI SKILL.md | 2026-09-05 |
| https://modly3d.app/ | Modly — Free Local AI 3D Model Generator | 2026-09-05 |
| https://github.com/lightningpixel/modly/blob/main/docs/running-on-jetson.md | Running Modly headless on an NVIDIA Jetson | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:modly`, thread `modly-development`, 1 dated events 2026-03-20 → 2026-03-20.
- **Practical note:** From 2026-03-20, use the referenced GitHub repository as the starting point for source-level verification of Modly; do not infer releases, capabilities, or usage instructions from this link alone.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
