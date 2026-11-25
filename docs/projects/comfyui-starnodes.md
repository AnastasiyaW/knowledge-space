---
title: ComfyUI_StarNodes
category: projects
date: 2026-07-18
tags: [comfyui-starnodes, project]
aliases: ["ComfyUI_StarNodes"]
---

# ComfyUI_StarNodes

**Development line:** `project:comfyui-starnodes` · thread `comfyui-starnodes`  
**Last event:** 2026-07-18 · 1 dated since 2026-07-18 · **Researched:** 2026-09-06 · confidence: medium

## What it is

ComfyUI_StarNodes is an MIT-licensed custom node suite for ComfyUI practitioners who need starter workflows, sampling, image processing, and video in one extension.

- Starter settings for Flux, SDXL, and Qwen
- Samplers, LoRAs, inpainting, upscaling, PSD saving, wildcards, and debugging tools
- Video tools, including LTX workflows

The README claims 100 nodes, `pyproject.toml` lists version 2.7.1, and GitHub Releases has no releases. The package covers broad ground, but reproducible workflows require pinning a revision and testing individual nodes separately.

## Development line

- **2026-07-18 — ComfyUI_StarNodes GitHub repository was referenced.** On 2026-07-18, we referenced the link to the ComfyUI_StarNodes GitHub repository. The available evidence identifies the project repository, but does not establish a release, feature change, version, or installation status. This history entry notes the dated repository reference only.

## What changed

- **2024-11-20** — v1.7.0 moved verified StarBetaNodes into the main package, including Qwen/WAN editing and utilities.
- **2026-04-10** — v2.0.0 added nine integrated nodes for LTX video and ACE Step, removed eight legacy nodes, and trimmed dependencies.
- **2026-07-10** — A public post claimed v2.1.1 with a 360-degree panorama viewer and an updated workflow; commit or registry artifacts are missing.
- **2026-07-18** — Only the repository link is documented for this date, with no confirmed change, version, or SHA.
- **2026-07-19** — A public post claimed updates v2.3.6 and v2.3.7 with performance improvements, new nodes, UI updates, and compatibility fixes; primary release artifacts are missing.

## How to use this

Treat the linked ComfyUI_StarNodes repository as a project source to inspect as of 2026-07-18, not as proof of a verified release or installation procedure.

1. Search for `Starnodes` in ComfyUI Manager, install the package, and restart ComfyUI. If the package is not listed, proceed to manual installation.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>
2. For manual installation, clone the repository into `ComfyUI/custom_nodes`, install `requirements.txt`, and restart ComfyUI.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>
3. Install dependencies directly into the Python environment of the active ComfyUI setup, then check the startup log for import errors after restart.
  — <https://docs.comfy.org/installation/install_custom_node>
4. Search nodes by `star` and begin with a relevant example: Start(t) Settings to start a graph, Save Image+ or PSD Saver for output, and Star Wildcards Advanced for prompt data.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>

## Best practices

- Review the repository and its requirements before installation. ComfyUI recommends installing custom nodes only from trusted sources and understanding what they do.
  — <https://docs.comfy.org/installation/install_custom_node>
- Save a snapshot before updating, so Manager can restore the node setup after the next launch.
  — <https://docs.comfy.org/manager/legacy-ui>
- Choose a packaged version over nightly for production graphs, because Manager documentation marks nightly as less stable.
  — <https://docs.comfy.org/manager/legacy-ui>
- Start with the bundled JSON example for the target task instead of moving the entire production graph at once.
  — <https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md>

## Superseded by this

- :{
- claim
- obsolete_since
- source_url
- claim

## Still unknown

- No second dated primary source links 2026-07-18 to a specific change, commit, tag, or version.
- The 2.7.1 value in `pyproject.toml` is a manifest version, not a confirmed GitHub Release or verified registry publication.
- Accessible GitHub history ends with an April 2026 snapshot while current repository files carry later metadata; exact commit chronology after April is not confirmed.
- Posts from July 10 and 19 point to the same repository, but independent primary artifacts do not confirm their authorship or claimed versions.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Starnodes2024/ComfyUI_StarNodes | ComfyUI_StarNodes repository | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/README.md | ComfyUI_StarNodes README | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/pyproject.toml | ComfyUI_StarNodes pyproject.toml | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/blob/main/CHANGELOG.md | ComfyUI_StarNodes changelog | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/commits/main | ComfyUI_StarNodes commit history | 2026-09-06 |
| https://github.com/Starnodes2024/ComfyUI_StarNodes/releases | ComfyUI_StarNodes releases | 2026-09-06 |
| https://www.reddit.com/r/comfyui/comments/1usx5f3/starnodes_211_panorama_update/ | Starnodes 2.1.1 Panorama Update | 2026-09-06 |
| https://www.reddit.com/r/comfyui/comments/1v0u5mt/starnodes_double_feature_updates_v236_v237_are/ | STARNODES Double Feature: Updates v2.3.6 & v2.3.7 are LIVE! | 2026-09-06 |
| https://docs.comfy.org/installation/install_custom_node | How to Install Custom Nodes in ComfyUI | 2026-09-06 |
| https://docs.comfy.org/manager/legacy-ui | Managing custom nodes with ComfyUI-Manager (legacy UI) | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-starnodes`, thread `comfyui-starnodes`, 1 dated events 2026-07-18 → 2026-07-18.
- **Practical note:** As of 2026-07-18, practitioners should treat the linked ComfyUI_StarNodes repository as the project source to investigate, not as evidence of a verified release or installation procedure.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
