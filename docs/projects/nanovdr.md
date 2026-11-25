---
title: NanoVDR
category: projects
date: 2026-03-17
tags: [nanovdr, nanovdr-public-release, project]
aliases: ["NanoVDR"]
---

# NanoVDR

**Development line:** `project:nanovdr` · thread `nanovdr-public-release`  
**Last event:** 2026-03-17 · 1 dated since 2026-03-17 · **Researched:** 2026-09-05 · confidence: high

## What it is

NanoVDR is a visual-document retrieval system for teams searching PDF pages, reports, and page images. It acts as a query-side replacement rather than a standalone document indexer.

- Document indexer: indexes pages offline with Qwen3-VL-Embedding-2B.
- Query encoder: embeds text queries with 69–151M-parameter student models.
- Scorer: ranks compatible vectors with a dot product.

The 69M multilingual query model runs at 51 ms per CPU query and requires teacher-indexed documents.

## Development line

- **2026-03-17 — NanoVDR linked public Hugging Face resources and a demo.** On 2026-03-17, the line published a Hugging Face blog article, a project page, and a demo space. This established discoverable project and demonstration resources for the public release, though we did not research their contents for this review.

## What changed

- **2026-03-17** — NanoVDR was presented as a 69M text-only query encoder distilled from Qwen3-VL-Embedding-2B for visual-document retrieval. The first-party article is dated 2026-03-16 and reports 95.1% teacher retention for NanoVDR-S-Multi.
- **2026-08-11** — Checkpoint names changed to encode tower, teacher, and embedding width. Old links redirect.
- **2026-08-29** — The team posted arXiv v3. The project repository distinguishes the later DistilVDR document-tower work from the original NanoVDR query-tower line.

## How to use this

Check the linked Hugging Face resources and public demo before evaluation as of 2026-03-17; specific capabilities, requirements, and results remain unverified.

1. Load a compatible query checkpoint with SentenceTransformers and encode the text query.
  — <https://github.com/Ryenhails/NanoVDR>
2. For the original NanoVDR line, index pages offline with Qwen3-VL-Embedding-2B, then rank its page vectors with the query vector using a dot product.
  — <https://huggingface.co/nanovdr>
3. Use the hosted demo only for exploratory queries; it may be asleep until restarted.
  — <https://huggingface.co/spaces/nanovdr/NanoVDR-Demo>

## Best practices

- Match query and document towers by both teacher and embedding width; vectors from different teacher spaces are not interchangeable.
  — <https://github.com/Ryenhails/NanoVDR>
- Prefer the multilingual `-ML` query checkpoint unless an English-only model is specifically required.
  — <https://github.com/Ryenhails/NanoVDR>
- Use the original line for CPU query serving with teacher-built indexes; use the DistilVDR pair only when teacher-free indexing is required.
  — <https://github.com/Ryenhails/NanoVDR>

## Superseded by this

- **2026-08-11** — Checkpoint names stating tower, teacher, and vector width replace earlier names; legacy model links redirect.

## Still unknown

- The event_findings and new_events fields are absent from the response schema, so the dated additions stay in what_changed.
- A first-party article dated 2026-03-16 corroborates the 2026-03-17 event.
- The 2026-08-11 rename and 2026-08-29 arXiv v3 belong to later updates, not the 2026-03-17 event.
- The public demo was sleeping when checked, so an interactive run is unverified.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/blog/Ryenhails/nanovdr | NanoVDR: A 70M Text-Only Model That Retrieves Visual Documents as Well as a 2B VLM | 2026-09-05 |
| https://huggingface.co/nanovdr | nanovdr (NanoVDR) organization page | 2026-09-05 |
| https://huggingface.co/spaces/nanovdr/NanoVDR-Demo | NanoVDR Demo | 2026-09-05 |
| https://github.com/Ryenhails/NanoVDR | Ryenhails/NanoVDR | 2026-09-05 |
| https://arxiv.org/abs/2603.12824 | NanoVDR: Distilling a 2B Vision-Language Retriever into a 70M Text-Only Encoder for Visual Document Retrieval | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:nanovdr`, thread `nanovdr-public-release`, 1 dated events 2026-03-17 → 2026-03-17.
- **Practical note:** As of 2026-03-17, practitioners should consult NanoVDR’s linked Hugging Face project resources and public demo before evaluating it; specific capabilities, requirements, and results remain unverified.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
