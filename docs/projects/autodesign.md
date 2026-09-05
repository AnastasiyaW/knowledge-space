---
title: AutoDesign
category: projects

tags: [autodesign, autodesign-development, project, yaxin9luo/autodesign]
aliases: ["AutoDesign"]
---

# AutoDesign

**Development line:** `project:autodesign` · thread `autodesign-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

AutoDesign is an MIT-licensed project for researchers and teams who generate editable presentation assets from a paper PDF using a coding agent and a chosen LLM provider.

- Generates HTML posters, slides, landing pages, and subtitled videos.
- Stores manifests, run events, candidates, and outputs locally.
- Optimizes the agent harness around the run instead of fine-tuning model weights.

PosterBench formal evaluation covers academic posters only; slides, web pages, and video remain pilot tracks.

The system works for a reproducible paper-to-poster workflow; test the other formats on your own examples.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-08-13 — The paper introduced AutoDesign as a meta-harness for paper-to-poster workflows and PosterBench: 100 papers in the main set and 10 in the controlled mini-set; reported 78.32 points on Main Track and 253 tool calls across 40 minutes in autonomous execution.
- 2026-08-14 — The repository published its first public release.
- 2026-08-16 — AutoDesign became available as a public project with code and a web interface; its confirmed initial scope is converting multimodal sources into academic posters rather than general UI generation.
- 2026-08-17 — Modular Agent Skills became available for posters, presentations, web pages, and video.
- 2026-08-18 — Poster Skill switched to agent-first v2 with direct PDF processing, revision-bound attempts, and read-only DOM QA.
- 2026-08-19 — Web UI added poster canvas controls for templates, aspect ratios, exact dimensions, and academic presets.

## How to use this

As of 2026-08-16, treat the linked AutoDesign website and repository as sources to investigate, but verify any release, capability, or workflow change before relying on it.

1. Install Node.js 22+ and ffmpeg/ffprobe, start the local launcher, and verify the environment with `autodesign doctor`.
  — <https://github.com/Yaxin9Luo/AutoDesign>
2. For source setups, install dependencies with `uv sync`, install Playwright browsers, and fetch video runtime and web client dependencies.
  — <https://github.com/Yaxin9Luo/AutoDesign>
3. Upload a PDF and run Paper All-in-One, or call `python -m autodesign run` with the PDF and poster template.
  — <https://github.com/Yaxin9Luo/AutoDesign>
4. Inspect `final/poster.html`, preview, final manifest, and `run_events.jsonl`; generating a file does not guarantee a valid run.
  — <https://github.com/Yaxin9Luo/AutoDesign>

## Best practices

- Use reference posters only for visual structure so text, logos, QR codes, tables, and links do not bleed into new work.
  — <https://github.com/Yaxin9Luo/AutoDesign>
- Check the terminal status and manifest feedback; do not treat file creation as proof of success.
  — <https://github.com/Yaxin9Luo/AutoDesign>
- Use `autodesign` and `AUTODESIGN_*` variables for new automations; `design_anything` and `DESIGN_ANYTHING_*` are deprecated aliases.
  — <https://github.com/Yaxin9Luo/AutoDesign>

## Superseded by this

- 2026-08-17 — Server-only monolithic execution was replaced as the only route: modular Agent Skills are now installable separately.
- 2026-08-18 — The previous Poster Skill was replaced by agent-first v2 for PDF-first runs and DOM QA.
- Documentation marks `design_anything`, `design-anything`, `designanything`, and `DESIGN_ANYTHING_*` as obsolete compatibility aliases; configure new setups with `autodesign` and `AUTODESIGN_*`.

## Still unknown

- Benchmark results and human evaluation scores come from the authors and have not been independently reproduced here.
- Stability for the hosted demo and fitness of bundled integrations for production remain unverified.
- The 2026-08-16 entry lacks a distinct dated primary source; details rely on the 2026-08-13 paper and the 2026-08-14 public release.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Yaxin9Luo/AutoDesign | Yaxin9Luo/AutoDesign | 2026-09-05 |
| https://arxiv.org/abs/2608.13560 | AutoDesign: Meta-Harness Optimization for Long-Horizon Agentic Design | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:autodesign`, thread `autodesign-development`, 0 dated events - → -.
- **Practical note:** As of 2026-08-16, treat the linked AutoDesign website and repository as sources to investigate, but verify any release, capability, or workflow change before relying on it.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
