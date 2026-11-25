---
title: DMX
category: projects
date: 2026-04-09
tags: [dmx, dmx-format-release, dmx_format_release, project]
aliases: ["DMX"]
---

# DMX

**Development line:** `project:dmx` · thread `dmx-format-release`  
**Last event:** 2026-04-09 · 1 dated since 2026-04-09 · **Researched:** 2026-09-05 · confidence: medium

## What it is

DMX is a Python package for teams distributing safetensors models: lossless `.dmx` archives, base-relative `.dmxd` deltas, round-trip verification, and embedded lineage metadata. Limit: every PyPI release listed through 1.5.3 is yanked, so it is not a safe unpinned production dependency.

## Development line

- **2026-04-09 — DMX was publicly presented as an AI model-weight compression format.** On 2026-04-09, DMX was publicly presented through a ComfyUI community post linking a GitHub repository and a Hugging Face profile. The linked materials identify the project as concerning compression of AI model weights. The available evidence does not establish its technical specifications, release maturity, or supported integrations.

## What changed

2026-04-09 — DMX launched as a CLI-oriented compressor for model storage and transfer; the release-day package history records versions 0.4.0 and 0.5.0, later yanked. The original workflow required decompression back to safetensors before ComfyUI use; the launch cited 9.1 GB to 1.8 GB, 7.2 GB to 1.5 GB, and +0.16% perplexity on Llama 3 8B. 2026-04-10 — PyPI version 0.6.0 was released and later yanked. 2026-04-11 — PyPI version 0.7.0 was released and later yanked. 2026-04-19 — PyPI versions 1.0.0 and 1.1.0 were released and later yanked; the later package documentation describes lossless archives, deltas, provenance, and a GPU runtime. 2026-04-20 to 2026-04-25 — versions 1.2.0 through 1.5.3 were released and all later yanked. A Qwen2.5-3B-Instruct delta demonstrates the newer distribution path: 2.88 GB int16 delta versus a 13.59 GB full model, but it requires the exact Qwen2.5-3B base and a merged single-file export.

## How to use this

As of 2026-04-09, practitioners evaluating model-weight storage or transfer can treat DMX as a newly announced compression-format project, but should verify implementation details and compatibility in its repository before adopting it.

1. Do not install an unpinned current release: first select and audit a specific wheel because the listed releases are yanked.
  — <https://pypi.org/project/dmx-compress/>
2. For a lossless archive, run `dmx compress model.safetensors model.dmx`, then prove it with `dmx verify model.safetensors model.dmx`.
  — <https://pypi.org/project/dmx-compress/>
3. Restore a portable checkpoint with `dmx decompress model.dmx restored.safetensors`; use the restored safetensors in tools that do not natively load DMX.
  — <https://pypi.org/project/dmx-compress/>
4. For the published Qwen delta, obtain the exact Qwen/Qwen2.5-3B base, apply `dmx delta-reconstruct`, then load the reconstructed safetensors in the target framework.
  — <https://huggingface.co/Senat1/dmx-qwen2.5-3b-instruct-delta>

## Best practices

- Keep the original checkpoint and run a round-trip verification before deleting or distributing a DMX artifact.
  — <https://pypi.org/project/dmx-compress/>
- Treat a delta as bound to its stated base checkpoint; reconstruction is expected to fail with a different base.
  — <https://huggingface.co/Senat1/dmx-qwen2.5-3b-instruct-delta>
- For the April 9 workflow, budget DMX as disk and download compression, not ComfyUI VRAM reduction; native ComfyUI loading was only a roadmap item then.
  — <https://www.reddit.com/r/comfyui/comments/1saeezm/i_built_a_compression_format_for_ai_model_weights/>

## Superseded by this

- 2026-04-09 — Guidance that DMX was only an external storage compressor is outdated relative to later package claims of compressed-residency runtime support, but those claims remain insufficiently reproducible for production adoption.
- 2026-04-09 — Guidance to expect a native ComfyUI node is obsolete as a current instruction: use restored safetensors unless a separately verified integration is available.

## Still unknown

- The requested response schema has no `event_findings` or `new_events` fields; the event-specific additions and later dated events are therefore represented in `what_changed`.
- The original GitHub repository URL returned 404 when checked, so repository code, changelog, and current maintainership could not be independently audited.
- The PyPI README reports runtime benchmarks and support claims, but its public technical and benchmark documentation is marked as forthcoming; treat those measurements as maintainer claims rather than independently reproduced results.

## Sources

| source | title | read |
|---|---|---|
| https://www.reddit.com/r/comfyui/comments/1saeezm/i_built_a_compression_format_for_ai_model_weights/ | I built a compression format for AI model weights — 60-80% smaller, need help testing | 2026-09-05 |
| https://github.com/willjriley/dmx | willjriley/dmx repository (returned 404 when observed) | 2026-09-05 |
| https://huggingface.co/Senat1/dmx-qwen2.5-3b-instruct-delta | DMX Delta for Qwen2.5-3B-Instruct | 2026-09-05 |
| https://pypi.org/project/dmx-compress/ | dmx-compress on PyPI | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:dmx`, thread `dmx-format-release`, 1 dated events 2026-04-09 → 2026-04-09.
- **Practical note:** As of 2026-04-09, practitioners evaluating model-weight storage or transfer can treat DMX as a newly announced compression-format project, but should verify implementation details and compatibility in its repository before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
