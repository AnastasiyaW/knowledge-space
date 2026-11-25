---
title: SANA-Streaming — SANA Streaming
category: projects
date: 2026-06-03
tags: [project, sana-streaming, sana_streaming]
aliases: ["SANA-Streaming"]
---

# SANA-Streaming — SANA Streaming

**Development line:** `project:sana-streaming` · thread `sana-streaming`  
**Last event:** 2026-06-03 · 1 dated since 2026-06-03 · **Researched:** 2026-09-05 · confidence: high

## What it is

SANA-Streaming is a 2B video-to-video editor for creators who need text-guided edits while retaining source motion and unedited regions.

- Long streaming editing: edits continuous video streams frame by frame.
- Short bidirectional editing: edits clips using both forward and backward context.

The reported real-time configuration runs 1280×704 at 24 end-to-end FPS on one RTX 5090. The public inference path uses BF16 checkpoints, not the paper’s MPQ deployment recipe. We use it for local long-form V2V work when its NVIDIA-oriented runtime and fixed 720p workflow fit the job.

## Development line

- **2026-06-03 — SANA Streaming project page referenced.** We linked the SANA Streaming development line to NVIDIA's SANA Streaming project page on 2026-06-03. This is a material reference point for the project's public development history. Available evidence does not establish a specific release, capability, or performance claim.

## What changed

- **2026-06-03** — NVIDIA introduced SANA-Streaming as a 2B, 720p, minute-scale streaming video-to-video editor. The accompanying paper, dated 2026-05-28, reported 24 end-to-end FPS and 58 DiT FPS at 1280×704 on an RTX 5090.
- **2026-07** — NVIDIA released training support for bidirectional and distillation paths. This extended the initial inference-and-checkpoint release.

## How to use this

As of 2026-06-03, start from the SANA Streaming project page to check official materials before relying on secondary summaries.

1. Install the repository environment, activate the `sana` Conda environment, and keep the documented pinned runtime versions for reproducible bidirectional inference.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>
2. Run `long_streaming` with the released `sana_streaming_ar.pth` checkpoint for a source video, text instruction, and up to 969 decoded frames. Documented defaults use four denoising steps, CFG 1.0, two cached blocks, and sink-token caching.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>
3. Use `bidirectional_short` with `sana_bidirectional_short.pth` when a five-second, 81-frame edit is sufficient. Documented defaults use 50 steps and CFG 6.0.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>

## Best practices

- Keep the mode-specific repository configuration and pinned package versions. Fused GDN kernels and the LTX-2 VAE path are version-sensitive.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>
- Treat the RTX 5090 24-FPS figure as a system-co-designed MPQ result. It is not a guarantee for the released BF16 inference command.
  — <https://arxiv.org/abs/2605.30409>
- Use long streaming for sequence length and bidirectional mode for short edits. Released checkpoints, frame counts, sampling settings, and temporal assumptions differ between them.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>

## Superseded by this

- **2026-07** — The June inference-only understanding is incomplete. NVIDIA later released bidirectional and distillation training paths.

## Still unknown

- The dated June event names no release commit and no day-specific announcement. We cannot independently pin the exact 2026-06-03 release scope beyond the June release notice and the 2026-05-28 paper date.
- The supplied response schema lacks `event_findings` and `new_events` fields. We represent their verified content in `what_changed` and `supersedes`.

## Sources

| source | title | read |
|---|---|---|
| https://nvlabs.github.io/Sana/Streaming/ | SANA-Streaming | Real-time Streaming Video Editing | 2026-09-05 |
| https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md | SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer | 2026-09-05 |
| https://github.com/NVlabs/Sana | NVlabs/Sana | 2026-09-05 |
| https://arxiv.org/abs/2605.30409 | SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:sana-streaming`, thread `sana-streaming`, 1 dated events 2026-06-03 → 2026-06-03.
- **Practical note:** As of 2026-06-03, practitioners should use the SANA Streaming project page as the primary starting point for identifying the project's public materials before relying on secondary summaries.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.