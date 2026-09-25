---
title: Qwen-MM-Plugins — Development
category: projects
date: 2026-08-10
tags: [development, project, qwen, qwen-mm-plugins]
aliases: ["Qwen-MM-Plugins"]
---

# Qwen-MM-Plugins — Development

**Development line:** `project:qwen-mm-plugins` · thread `development`  
**Last event:** 2026-08-10 · 1 dated since 2026-08-10 · **Researched:** 2026-09-08 · confidence: medium

## What it is

Qwen-MM-Plugins packages capability-specific Skills and optional MCP servers for agent harnesses. It connects an existing agent to visual, audio, document, search, and 3D/CAD tasks.

- `core`: local reading and visualization for images, video, documents, data, 3D files, and NIfTI.
- `api` and `search`: model and API vision, OCR, grounding, audio, web, and reverse-image tasks.
- `video-memory`, `video-edit`, `blender`, `freecad`, `edu-agent`, and `omni-memory`: long-video, media-editing, application-control, education, and audio-visual-memory workflows.

`core` needs no API key in default native-image mode. Cloud, search, text-only captioning, and memory paths require credentials or system dependencies. Native Windows is not validated. Start with `core` on a multimodal harness. Add capabilities only when data-egress and runtime requirements demand them.

## Development line

- **2026-08-10 — Qwen-MM-Plugins repository referenced.** On 2026-08-10, the Qwen thread referenced the Qwen-MM-Plugins GitHub repository. The source provides only the date and repository link, without asserting a release, feature, or model change.

## What changed

- 2026-08-10 — Qwen-MM-Plugins was referenced in a dated source; the reachable first-party repository does not establish a launch, creation, or first-commit date.
- 2026-08-11 — An opt-in raw-Base64 audio mode for OpenAI-compatible endpoints was merged, while the DashScope default remained unchanged.
- 2026-08-18 — `video-memory` v1.0.2 normalized local file URIs across capabilities as part of cross-platform path fixes.
- 2026-08-20 — Tagged capability updates added text fallback for MCP image results.
- 2026-08-24 — `core` v1.0.5 added NIfTI volume visualization and 4D volume selection.
- 2026-09-03 — `omni-memory` v1.0.0 added audio-visual memory for long-video work.

## How to use this

1. Choose one capability for the task, then use the guided installer for the target harness. On Windows, use Ubuntu WSL2 and keep the checkout in the Linux home directory.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
2. Configure only required credentials and system tools. Run the installer Verify action or test the MCP entry with `--check-system`.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
3. Reference a file in the harness and state the task in plain language. The installed Skill selects the relevant MCP tool.
  — <https://github.com/QwenLM/Qwen-MM-Plugins>
4. On a text-only host, set `QWEN_MM_NATIVE_MODE=0` only after configuring a VL endpoint and approving image uploads.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md>
5. For an `omni-memory` video workflow, query `get_memory_status` first. Build or resume memory only when clip duration and status warrant it.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/cookbooks/omni-memory/usage.md>

## Best practices

- Pin durable installs to immutable per-capability tags. Reserve `main` and local-checkout mode for development.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
- Update a capability's Skill and MCP registration together, then reload or restart the harness.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
- Keep native image output for a multimodal host. Text-only fallback sends returned images and screenshots to the configured VL endpoint.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md>
- Pin `QWEN_MM_SEARCH_BACKEND` when provider selection must stay reproducible. Auto mode chooses the first configured backend.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md>
- Enable `QWEN_MM_AUDIO_RAW_B64` only for OpenAI-spec Omni endpoints that require raw Base64. Leave DashScope on its default format.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/pull/9>
- After an interrupted omni-memory build, verify clip coverage with `get_memory_status`. Resume rather than trusting a partial memory.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/cookbooks/omni-memory/usage.md>

## Superseded by this

- 2026-08-11 — Assuming every OpenAI-compatible endpoint accepts DashScope data-URL audio. The opt-in raw-Base64 path covers endpoints like vLLM while DashScope keeps the default.
- 2026-08-18 — Unnormalized local-file URIs across capabilities. `video-memory` v1.0.2 normalized URIs and fixed cross-platform paths.
- 2026-08-20 — Native MCP image blocks as the only documented format for text-only hosts. Updates added text fallback.
- 2026-08-24 — Core without NIfTI visualization or 4D volume selection. `core` v1.0.5 added both.

## Still unknown

- The official Qwen post for August 10 returned HTTP 403 during research. Event details rely on secondary archives rather than a first-party repository receipt.
- GitHub repository and Releases pages do not establish a creation date, first commit, or a GitHub Release on 2026-08-10.
- The broader Qwen development line includes separate projects. We found no technical lineage, compatibility, or ownership ties to Qwen-MM-Plugins.
- We found no primary compatibility matrix across OpenAI-compatible providers. Test the selected endpoint and capability before relying on it.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/QwenLM/Qwen-MM-Plugins | QwenLM/Qwen-MM-Plugins repository README | 2026-09-08 |
| https://easyvibecoding.app/curated/2887-alibaba-qwen-shares-qwen-mm-plugins-native-multimodal-agent | EasyVibeCoding archive of Qwen's Qwen-MM-Plugins post | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/pull/9 | PR #9: opt-in raw Base64 input audio for OpenAI-spec servers | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/tags | Qwen-MM-Plugins capability tags | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md | Qwen-MM-Plugins installation guide | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md | Qwen-MM-Plugins configuration reference | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/cookbooks/omni-memory/usage.md | Qwen-MM-Plugins omni-memory usage cookbook | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/releases | Qwen-MM-Plugins GitHub Releases page | 2026-09-08 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen-mm-plugins`, thread `development`, 1 dated events 2026-08-10 → 2026-08-10.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
