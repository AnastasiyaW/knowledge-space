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

AutoDesign is an MIT project for researchers and teams who need editable materials from a paper PDF using a coding agent and a chosen LLM provider.

- Generation: produces an HTML poster, slides, landing page, and subtitled video.
- Local storage: saves manifests, run events, candidates, and outputs locally.
- Harness optimization: tunes the surrounding agent harness rather than base model weights.

PosterBench formal evaluation covers only academic posters; slides, web pages, and video remain pilot tracks.
We can use it for a reproducible paper-to-poster workflow; test other formats on your own examples.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-08-13 — Paper introduced AutoDesign as a meta-harness for paper-to-poster and PosterBench: 100 papers in the main set and 10 in the controlled mini-set; authors reported 78.32 points on Main Track and 253 tool calls across 40 minutes of autonomous execution.
- 2026-08-14 — First public repository release published.
- 2026-08-16 — AutoDesign became available as a public project with source code and a web interface; confirmed scope is converting multimodal sources into academic posters, not a general UI generator.
- 2026-08-17 — Standalone Agent Skills became available for posters, presentations, web pages, and video.
- 2026-08-18 — Poster Skill moved to agent-first v2: direct PDF handling, revision-bound attempts, and read-only DOM QA.
- 2026-08-19 — Web UI added poster canvas controls: templates, aspect ratios, exact dimensions, and academic presets.

## How to use this

As of 2026-08-16, practitioners may treat the linked AutoDesign website and repository as sources to investigate, but should not infer a verified release, capability, or workflow change from this link-only record.

1. Install Node.js 22+ and ffmpeg/ffprobe, run the local launcher, and check the environment with `autodesign doctor`.
  — <https://github.com/Yaxin9Luo/AutoDesign>
2. For running from source, install dependencies with `uv sync`, install Playwright browsers, and configure video runtime and web client dependencies.
  — <https://github.com/Yaxin9Luo/AutoDesign>
3. Upload a PDF and run Paper All-in-One, or call `python -m autodesign run` with the PDF and poster template.
  — <https://github.com/Yaxin9Luo/AutoDesign>
4. Check `final/poster.html`, preview, final manifest, and `run_events.jsonl`; file presence alone does not guarantee validation success.
  — <https://github.com/Yaxin9Luo/AutoDesign>

## Best practices

- Use reference posters only for the visual system: their text, logos, QR codes, tables, and links must not become evidence for new work.
  — <https://github.com/Yaxin9Luo/AutoDesign>
- Inspect terminal status and manifest feedback instead of treating a generated file as proof of success.
  — <https://github.com/Yaxin9Luo/AutoDesign>
- Use `autodesign` and `AUTODESIGN_*` variables for new automation: legacy names `design_anything` and `DESIGN_ANYTHING_*` are deprecated aliases.
  — <https://github.com/Yaxin9Luo/AutoDesign>

## Superseded by this

- 2026-08-17 — Monolithic server-only usage is no longer required: standalone installable Agent Skills are available.
- 2026-08-18 — Previous Poster Skill replaced by agent-first v2 for PDF-oriented workflows and DOM QA.
- Current documentation marks `design_anything`, `design-anything`, `designanything`, and `DESIGN_ANYTHING_*` as deprecated compatibility aliases; new setups use `autodesign` and `AUTODESIGN_*`.

## Still unknown

- Reported benchmark results and human evaluation scores are published by the authors but were not reproduced independently in this review.
- Stability of the hosted demo and production readiness of bundled integrations remain unverified.
- The 2026-08-16 event has no separate dated primary source; details rely on the 2026-08-13 paper and the 2026-08-14 public release.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Yaxin9Luo/AutoDesign | Yaxin9Luo/AutoDesign | 2026-09-05 |
| https://arxiv.org/abs/2608.13560 | AutoDesign: Meta-Harness Optimization for Long-Horizon Agentic Design | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:autodesign`, thread `autodesign-development`, 0 dated events - → -.
- **Practical note:** As of 2026-08-16, practitioners may treat the linked AutoDesign website and repository as sources to investigate, but should not infer a verified release, capability, or workflow change from this link-only record.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
