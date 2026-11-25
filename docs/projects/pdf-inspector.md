---
title: pdf-inspector
category: projects
date: 2026-08-03
tags: [firecrawl, pdf-inspector, pdf-inspector-development, project]
aliases: ["pdf-inspector"]
---

# pdf-inspector

**Development line:** `project:pdf-inspector` · thread `pdf-inspector-development`  
**Last event:** 2026-08-03 · 1 dated since 2026-08-03 · **Researched:** 2026-09-05 · confidence: medium

## What it is

pdf-inspector — a local Rust library and CLI for PDF-processing developers: it classifies native-text, scanned, image-based, and mixed PDFs, then returns structured Markdown and page-level routing data. — Rust, Python, Node.js, CLI, and browser WebAssembly entry points. — Position-aware text, reading order, table detection, and optional OCR with provenance. classification is documented at about 10–50 ms; routed OCR needs external PDFium, ONNX Runtime, and a roughly 31 MB model set. use it as a local classification-and-extraction layer, but validate the document shapes that matter to your workflow.

## Development line

- **2026-08-03 — pdf-inspector repository linked in the Firecrawl thread.** On 2026-08-03, the pdf-inspector GitHub repository was linked in the Firecrawl thread. This is a material historical reference because it identifies the project’s source repository at that date. The available evidence does not establish a release, feature change, or project maturity.

## What changed

2026-08-03 — pdf-inspector’s Python package was already public as 0.2.6; same-day reports exposed malformed-xref and sparse-table failures, so the date is not a verified launch. 2026-08-06 — pdf-inspector was documented as Firecrawl’s separate open-source PDF engine and as part of hosted document endpoints. 2026-08-10 — pdf-inspector received a verified packages-2026-08-10 tag consolidating package versions beyond the 0.2.6 Python line. 2026-08-13 — pdf-inspector v1.14.2 added resource bounds for pathological PDFs and Form XObject/layout fixes. 2026-08-17 — pdf-inspector v1.15.0 added selective OCR through PDFium, ONNX Runtime, and PP-OCRv6 Small. 2026-08-21 — PyPI published pdf-inspector 1.17.0, the current public Python package line. 2026-09-03 — pdf-inspector main gained rotated-text geometry and visible-page coordinate changes; these source changes remain unreleased.

## How to use this

As of 2026-08-03, practitioners can use the linked pdf-inspector repository as the dated source reference when evaluating PDF-inspection work related to Firecrawl.

1. Install the Python binding with `pip install pdf-inspector`, then call `detect_pdf()` on each input before committing to a processing path.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
2. For a native-text result, call `process_pdf()` to obtain Markdown plus type, confidence, page count, pages needing OCR, layout signals, and encoding-issue flags.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
3. For scanned or mixed documents, call `process_pdf_with_ocr()` in auto mode and retain each page's native, OCR, or fused provenance.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
4. When OCR is routed, install the documented PDFium and ONNX Runtime builds, set their library paths, and preseed a model directory with offline mode where network access is disallowed.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/ocr-runtime.md>
5. In a Node server, use asynchronous `processPdfWithOcr()` and inspect `pagesRoutedToOcr` and `pagesRecommendingHosted`.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md>

## Best practices

- Treat classification as routing, not a blanket OCR decision: preserve type, confidence, per-page reasons, and page provenance with extracted content.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md>
- Pin PDFium 153.0.7988.0, ONNX Runtime 1.27.0, and the PP-OCRv6 Small artifact revision for reproducible OCR; preseed and use offline mode for hermetic deployments.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/ocr-runtime.md>
- Benchmark representative PDFs rather than generalizing from the published 200-document, OCR-disabled Apple M4 Pro comparison.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
- Keep malformed-startxref PDFs in the regression record; an Aug. 3 report showed classification and extraction could both fail on them in 0.2.6.
  — <https://github.com/firecrawl/pdf-inspector/issues/228>
- Validate sparse and grouped tables against source pages, because an Aug. 3 report showed well-formed but structurally wrong Markdown with collapsed rows in 0.2.6.
  — <https://github.com/firecrawl/pdf-inspector/issues/229>
- Normalize page-number conventions at your boundary: classification and region extraction use 0-based page lists while OCR selectors and several result types use 1-based page numbers.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>

## Superseded by this

- 2026-08-03 — treating the repository link as proof that pdf-inspector launched that day.
- Before 2026-08-17 — manually handing every scanned or mixed page to another OCR system as the only supported route.

## Still unknown

- The exact release or intent associated with 2026-08-03 is unverified: the repository link carries no version or release note, while same-day issue reports identify an already-public 0.2.6 package.
- GitHub Releases still marks 1.15.0 as latest, while the current source manifest and PyPI show 1.17.0; no GitHub Release page for 1.16.0 or 1.17.0 was found.
- The 2026-09-03 coordinate and rotated-text changes are in current source and the changelog's Unreleased section, so their first packaged version is unverified.
- Firecrawl states that hosted /parse and /scrape use pdf-inspector, but this research did not independently execute either endpoint.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/firecrawl/pdf-inspector | firecrawl/pdf-inspector | 2026-09-05 |
| https://raw.githubusercontent.com/firecrawl/pdf-inspector/main/README.md | pdf-inspector README | 2026-09-05 |
| https://raw.githubusercontent.com/firecrawl/pdf-inspector/main/Cargo.toml | pdf-inspector Cargo.toml | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/issues/228 | Issue #228: No xref recovery | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/issues/229 | Issue #229: Sparse/grouped table rows collapse | 2026-09-05 |
| https://www.firecrawl.dev/blog/anydoc-and-pdf-inspector | Introducing AnyDoc and pdf-inspector | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/tags | pdf-inspector tags | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/releases/tag/v1.14.2 | Release 1.14.2 — Hardened parsing for pathological PDFs | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/releases/tag/v1.15.0 | Release 1.15.0 — Selective OCR for scanned and mixed PDFs | 2026-09-05 |
| https://pypi.org/project/pdf-inspector/ | pdf-inspector on PyPI | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/commit/636ca1a58bdc1af4cd3fc20b8c1f549a1121cca7 | Commit 636ca1a: rotated text geometry | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/CHANGELOG.md | pdf-inspector changelog | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md | pdf-inspector Python API | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md | pdf-inspector Node.js API | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/docs/ocr-runtime.md | pdf-inspector OCR runtime setup | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:pdf-inspector`, thread `pdf-inspector-development`, 1 dated events 2026-08-03 → 2026-08-03.
- **Practical note:** As of 2026-08-03, practitioners can use the linked pdf-inspector repository as the dated source reference when evaluating PDF-inspection work related to Firecrawl.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
