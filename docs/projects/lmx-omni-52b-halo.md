---
title: LMX-Omni-52B-Halo
category: projects
date: 2026-06-12
tags: [lmx-omni-52b-halo, project]
aliases: ["LMX-Omni-52B-Halo"]
---

# LMX-Omni-52B-Halo

**Development line:** `project:lmx-omni-52b-halo` · thread `lmx-omni-52b-halo`  
**Last event:** 2026-06-12 · 1 dated since 2026-06-12 · **Researched:** 2026-09-05 · confidence: high

## What it is

LMX-Omni-52B-Halo bundles Qwen3.6-35B-A3B-MTP, Flux-2-Klein-9B, Whisper-Large-v3-Turbo and kokoro-v1 for local multimodal applications.

- Chat and image analysis
- Image generation and editing
- Audio transcription
- Speech synthesis

Component downloads take about 44,8 GB, and the Halo class targets Strix Halo hardware.
Choose it for local any-to-any prototypes when the download size and internal tool-calling latency are justified.

## Development line

- **2026-06-12 — LMX-Omni-52B-Halo was linked to its Hugging Face model repository.** On 2026-06-12, a link connected LMX-Omni-52B-Halo to its Hugging Face repository. That establishes the repository as a project artifact by that date. It does not establish its release status, capabilities, licensing, or intended use.

## What changed

- 2026-06-12 — The model card described LMX-Omni-52B-Halo as a unified OpenAI-compatible omni bundle. The initial repository was created on 2026-06-03, and on 2026-06-04 its manifest switched to the unified format while deleting `collection.json`.
- 2026-06-23 — The published manifest added a configurable collection system prompt.
- 2026-08-08 — An open issue reported that the collection does not stream planner `reasoning_content` to Open WebUI. That remains a limitation for interfaces requiring visible reasoning.

## How to use this

As of 2026-06-12, verify LMX-Omni-52B-Halo artifacts and documentation in the linked Hugging Face repository before relying on the project.

1. Install Lemonade, download all components with `lemonade pull LMX-Omni-52B-Halo`, and launch the model with `lemonade run LMX-Omni-52B-Halo`.
  — <https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo>
2. Point an OpenAI-compatible client to `/chat/completions` using the model name; the server dispatches components and returns images and audio in the response message.
  — <https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo>
3. Pass `model: "LMX-Omni-52B-Halo"` to `lemonade_omni` in an MCP client for a single multimodal turn with images and audio.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>

## Best practices

- Specify Halo explicitly only on supported hardware; MCP defaults to the smaller and faster LMX-Omni-5.5B-Lite.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>
- Set `output_dir` for MCP artifacts: that creates unique file names and supports clients that do not render audio content blocks.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>
- Do not expect streaming reasoning in Open WebUI: the filed issue for Omni collections remains open.
  — <https://github.com/lemonade-sdk/lemonade/issues/2990>

## Superseded by this

- 2026-05-21 — The old guide for legacy collections is obsolete: Lemonade v10.6.0 replaced them with LMX-Omni-52B-Halo and LMX-Omni-5.5B-Lite.
- 2026-06-04 — The legacy `collection.json` manifest for this model was replaced with unified `LMX-Omni-52B-Halo.json`.

## Still unknown

- The primary source does not date 2026-06-12 with a release or change. It confirms page state, but records no distinct event on that day.
- The response schema omits the requested `event_findings` and `new_events` fields. Their additions appear in `what_changed` and `unknowns` instead.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo | LMX-Omni-52B-Halo model card | 2026-09-05 |
| https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo/commits/main | LMX-Omni-52B-Halo commit history | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/blob/main/docs/dev/lemonade-omni.md | Lemonade Omni Models documentation | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md | Lemonade MCP API documentation | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/releases/tag/v10.6.0 | Lemonade v10.6.0 release | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/issues/2990 | Omni collections do not stream planner reasoning_content | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:lmx-omni-52b-halo`, thread `lmx-omni-52b-halo`, 1 dated events 2026-06-12 → 2026-06-12.
- **Practical note:** As of 2026-06-12, verify LMX-Omni-52B-Halo artifacts and documentation in the linked Hugging Face repository before relying on the project.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
