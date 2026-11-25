---
title: Fooocus
category: projects
date: 2023-09-12
tags: [fooocus, fooocus-development, fooocus_v2, project]
aliases: ["Fooocus"]
---

# Fooocus

**Development line:** `project:fooocus` · thread `fooocus-development`  
**Last event:** 2023-09-12 · 2 dated since 2023-08-13 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Fooocus is a local, offline SDXL image generator for creators who want a simpler prompt-first workflow than ComfyUI.

- Text-to-image with styles and prompt expansion.
- Variations, upscale, inpaint/outpaint, Image Prompt, and face swap.
- General, realistic, and anime presets.

## Development line

- **2023-08-13 — Fooocus repository and Windows release artifact linked.** On 2023-08-13, we linked Fooocus to its GitHub repository and Windows 64-bit release archive. This records a public distributable artifact in the Fooocus development line.
- **2023-09-12 — Fooocus development discussion linked.** On 2023-09-12, we linked the Fooocus development line to GitHub Discussion #347. This links the thread to the Fooocus v2-era history, though we have not researched the discussion content itself.

## What changed

2023-08-13 — Fooocus entered its public v1 state. The update log marks v1.0.15 as publicly available.

2023-09-12 — Fooocus 2.0.0 replaced the text-processing engine, added multi-style prompting, and renamed Prompt Expansion and Raw Mode to Fooocus V2. The maintainer reported V2 beating V1 in 87/100 default results and 81/100 prompt-understanding tests, judged by two people.

2026-09-04 (found today, not a release date) — upstream describes Fooocus as SDXL-only, limited LTS, and bug-fix-only. Release v2.5.5 is currently marked Latest and contains a Colab inpaint fix.

## How to use this

From 2023-08-13, use the public GitHub repository and Windows distribution artifact. From 2023-09-12, consult the linked development discussion before relying on v2-era behavior.

1. Confirm that an SDXL workflow fits the task; Fooocus is not the maintained path for Flux or other newer architectures.
  — <https://github.com/lllyasviel/Fooocus>
2. On Windows, use the official download, extract it, and run `run.bat`. On Linux, clone the repository, install pinned requirements in Conda or a Python 3.10 venv, then run `entry_with_update.py`.
  — <https://github.com/lllyasviel/Fooocus>
3. Let the first launch download selected models, then use the default, anime, or realistic preset in the UI or with `--preset anime` / `--preset realistic`.
  — <https://github.com/lllyasviel/Fooocus>
4. Write a prompt, choose styles or Advanced settings as needed, and use Input Image for variation, upscale, inpaint/outpaint, or Image Prompt workflows.
  — <https://github.com/lllyasviel/Fooocus>
5. Keep the UI local unless remote access is needed. For `--listen` or `--share`, add an `auth.json` because access is unauthenticated by default.
  — <https://github.com/lllyasviel/Fooocus>

## Best practices

- Install only from the official GitHub repository or its linked downloads; upstream warns that similarly named Fooocus websites are fake.
  — <https://github.com/lllyasviel/Fooocus>
- Treat Fooocus as a stable SDXL tool. For Flux or newer-model work, follow upstream’s recommendation to use WebUI Forge, ComfyUI, or SwarmUI instead.
  — <https://github.com/lllyasviel/Fooocus>
- When switching presets, let required models finish downloading. Use `--always-download-new-model` if a preset must fetch its missing model rather than silently falling back to an older one.
  — <https://github.com/lllyasviel/Fooocus>
- Protect any network-exposed UI with `auth.json`. Neither `--listen` nor `--share` enables authentication by default.
  — <https://github.com/lllyasviel/Fooocus>
- Prefer supplied aspect ratios over arbitrary custom resolutions unless SDXL positional encoding is understood.
  — <https://github.com/lllyasviel/Fooocus/blob/main/update_log.md>

## Superseded by this

- 2023-08-13 — the v2.5.5 release currently marked Latest supersedes the public v1 state.
- 2023-09-12 — Fooocus 2.0 and its `Fooocus V2` style supersede V1 text-processing guidance and the UI label “Prompt Expansion and Raw Mode”; disable that style when attempting to reproduce V1 output.
- 2026-09-04 (found today) — waiting for official Fooocus support for Flux or another new architecture is obsolete today: upstream is LTS with bug fixes only and directs Flux users elsewhere.

## Still unknown

- We did not inspect the direct Windows archive at https://github.com/lllyasviel/Fooocus/releases/download/release/Fooocus_win64_1-1-10.7z; its contents, checksum, and exact packaging version remain unconfirmed.
- The upstream update log marks v1.0.15 as publicly available without a calendar date, so its exact release timestamp remains unconfirmed.
- No separate product exists behind `fooocus` and `fooocus_v2`: the official discussion identifies the latter as Fooocus 2.0.0, not a different subject.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/lllyasviel/Fooocus | Fooocus repository and README | 2026-09-04 |
| https://github.com/lllyasviel/Fooocus/discussions/347 | [Major Update] Fooocus 2.0.0 — Discussion #347 | 2026-09-04 |
| https://github.com/lllyasviel/Fooocus/blob/main/update_log.md | Fooocus update log | 2026-09-04 |
| https://github.com/lllyasviel/Fooocus/releases/tag/v2.5.5 | Fooocus v2.5.5 release | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:fooocus`, thread `fooocus-development`, 2 dated events 2023-08-13 → 2023-09-12.
- **Practical note:** From 2023-08-13, practitioners could treat Fooocus as having a publicly linked GitHub source location and Windows distribution artifact; from 2023-09-12, they should consult the linked development discussion before relying on v2-era behavior.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
