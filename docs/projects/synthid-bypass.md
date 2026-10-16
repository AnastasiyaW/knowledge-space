---
title: SynthID-Bypass
category: projects
date: 2026-03-13
tags: [project, synthid-bypass, synthid_bypass]
aliases: ["SynthID-Bypass"]
---

# SynthID-Bypass

**Development line:** `project:synthid-bypass` · thread `synthid-bypass`  
**Last event:** 2026-03-13 · 1 dated since 2026-03-13 · **Researched:** 2026-09-06 · confidence: medium

## What it is

SynthID-Bypass is a community ComfyUI workflow for authorized robustness tests of Google’s image SynthID watermark, not a Google product.

- Current V2 runs as one graph: Qwen Image GGUF handles global reconstruction, and Z-Image Turbo handles face-specific cleanup.
- It is an image pipeline; Google documents separate SynthID modalities for text, audio, and video.

## Development line

- **2026-03-13 — SynthID-Bypass v2.0 workflow artifact was linked.** SynthID-Bypass and its v2.0 JSON were linked. No dated primary release note or immutable revision establishes a further project change on that day.

## What changed

2026-03-08: A V2 announcement described one ComfyUI graph replacing V1’s separate workflow branches. It added resolution-aware denoise, a bundled custom-node pack, and a face-reconstruction path. 2026-03-13: SynthID-Bypass and its v2.0 JSON were linked. No dated primary release note or immutable revision establishes a further project change on that day.

## How to use this

1. Define an authorized image-watermark robustness experiment. Retain source assets, outputs, and provenance together, because the project disclaimer forbids copyright circumvention and misrepresenting origin.
  — <https://github.com/00quebec/Synthid-Bypass>
2. For a disposable local evaluation setup, prepare a current ComfyUI installation, resolve listed V2 dependencies, and load the graph. Treat it as a workflow with external nodes and models, not a packaged application.
  — <https://github.com/00quebec/Synthid-Bypass>
3. Read a SynthID result as a likelihood signal: detected, not detected, or possibly detected. Preserve complementary provenance metadata, because non-detection does not prove human origin.
  — <https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/>

## Best practices

- Use only media we own or are explicitly authorized to test, and keep disclosure and provenance intact. The project disclaimer rejects copyright circumvention and misrepresentation of origin.
  — <https://github.com/00quebec/Synthid-Bypass>
- Treat V1 as history rather than current guidance. The repository marks the V1 folder as archived and keeps the active release at the root.
  — <https://github.com/cebeuq/Synthid-Bypass/tree/main/V1>
- Separate visual quality assessment from watermark detection. Google describes SynthID as a likelihood-based signal that complements metadata, and notes limits under extreme image manipulation.
  — <https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/>

## Superseded by this

- 2026-03-08: The V1 split into separate general, portrait, and GGUF workflows is legacy guidance. V2 was announced as the main single workflow and V1 as an archive.

## Still unknown

- No immutable Git revision, release tag, or dated primary note was found for 2026-03-13. Current main-branch contents cannot prove the exact state on that day.
- No independent test discloses detector version, input source, resolution, before/after artifacts, and reproducible settings. Available repository and secondary examples do not establish a bypass rate.
- The Simplified-Chinese source produced a secondary synopsis with only a relative publication label. No first-party Chinese material or independently reproducible Chinese test was found.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/00quebec/Synthid-Bypass | SynthID-Bypass repository, current main branch redirected to cebeuq | 2026-09-06 |
| https://github.com/00quebec/Synthid-Bypass/blob/main/Synthid-Bypass-v2.0.json | Synthid-Bypass-v2.0.json, current mutable main-branch workflow | 2026-09-06 |
| https://www.reddit.com/r/comfyui/comments/1rnz3ar/i_created_an_open_source_synthid_remover_that/.json | V2 announcement record with created_utc timestamp | 2026-09-06 |
| https://github.com/cebeuq/Synthid-Bypass/tree/main/V1 | V1 Archive in the current repository | 2026-09-06 |
| https://deepmind.google/models/synthid/ | Google DeepMind SynthID overview | 2026-09-06 |
| https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/ | Google DeepMind: Identifying AI-generated images with SynthID | 2026-09-06 |
| https://sd114.wiki/21871.html | Simplified-Chinese community synopsis of SynthID-Bypass | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:synthid-bypass`, thread `synthid-bypass`, 1 dated events 2026-03-13 → 2026-03-13.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
