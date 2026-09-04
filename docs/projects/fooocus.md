---
title: Fooocus — Fooocus development
category: projects
tags: [fooocus, fooocus-development, fooocus_v2, project]
aliases: ["Fooocus"]
---

# Fooocus — Fooocus development

**Development line:** `project:fooocus` · thread `fooocus-development`  
**Events:** 2 dated, 2023-08-13 → 2023-09-12 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Fooocus — a local, offline SDXL image generator for creators who want a simpler prompt-first workflow than ComfyUI. - Text-to-image with styles and prompt expansion. - Variations, upscale, inpaint/outpaint, Image Prompt, and face swap. - General, realistic, and anime presets. Limit: upstream states 4 GB NVIDIA VRAM as the minimum and does not plan new model architectures. Verdict: use it for stable local SDXL work; use Forge or ComfyUI/SwarmUI for Flux and other newer-model workflows.

## Development line

- **2023-08-13 — Fooocus repository and Windows release artifact linked.** On 2023-08-13, Fooocus was linked to its GitHub repository and to a Windows 64-bit release archive. This records a publicly distributable project artifact in the Fooocus development line.
- **2023-09-12 — Fooocus development discussion linked.** On 2023-09-12, the Fooocus development line was linked to GitHub Discussion #347. The sealed thread association identifies it as part of the Fooocus v2-era development history, although the discussion content has not been researched.

## What changed

2023-08-13 — Fooocus entered its public v1 state; the maintained update log labels v1.0.15 as publicly available. 2023-09-12 — Fooocus 2.0.0 replaced the text-processing engine, added multi-style prompting, and renamed Prompt Expansion and Raw Mode to Fooocus V2. The maintainer reported V2 outperforming V1 in 87/100 default-result comparisons and 81/100 prompt-understanding comparisons, both judged by two people. 2026-09-04 (found today, not a release date) — upstream describes Fooocus as SDXL-only, limited LTS, and bug-fix-only. v2.5.5 is the release currently marked Latest and contains a Colab inpaint fix.

## How to use this

From 2023-08-13, practitioners could treat Fooocus as having a publicly linked GitHub source location and Windows distribution artifact; from 2023-09-12, they should consult the linked development discussion before relying on v2-era behavior.

1. Confirm that an SDXL workflow fits the task; Fooocus is not the maintained path for Flux or other newer architectures.
  — <https://github.com/lllyasviel/Fooocus>
2. On Windows, use the official download, extract it, and run `run.bat`; on Linux, clone the repository, install the pinned requirements in Conda or a Python 3.10 venv, then run `entry_with_update.py`.
  — <https://github.com/lllyasviel/Fooocus>
3. Let the first launch download the selected models, then use the default, anime, or realistic preset in the UI or with `--preset anime` / `--preset realistic`.
  — <https://github.com/lllyasviel/Fooocus>
4. Write a prompt, choose styles or Advanced settings as needed, and use Input Image for variation, upscale, inpaint/outpaint, or Image Prompt workflows.
  — <https://github.com/lllyasviel/Fooocus>
5. Keep the UI local unless remote access is needed; for `--listen` or `--share`, add an `auth.json` because access is unauthenticated by default.
  — <https://github.com/lllyasviel/Fooocus>

## Best practices

- Install only from the official GitHub repository or its linked downloads; upstream warns that similarly named Fooocus websites are fake.
  — <https://github.com/lllyasviel/Fooocus>
- Treat Fooocus as a stable SDXL tool. For Flux or newer-model work, follow upstream’s recommendation to use WebUI Forge, ComfyUI, or SwarmUI instead.
  — <https://github.com/lllyasviel/Fooocus>
- When switching presets, let the required models finish downloading; use `--always-download-new-model` if a preset must fetch its missing model rather than silently falling back to an older one.
  — <https://github.com/lllyasviel/Fooocus>
- Protect any network-exposed UI with `auth.json`; neither `--listen` nor `--share` enables authentication by default.
  — <https://github.com/lllyasviel/Fooocus>
- Prefer the supplied aspect ratios over arbitrary custom resolutions unless SDXL positional encoding is understood.
  — <https://github.com/lllyasviel/Fooocus/blob/main/update_log.md>

## Superseded by this

- 2023-08-13 — the public v1 state is superseded by the v2.5.5 release currently marked Latest.
- 2023-09-12 — V1 text-processing guidance and the UI label “Prompt Expansion and Raw Mode” are superseded by Fooocus 2.0 and its `Fooocus V2` style; disable that style when attempting to reproduce V1 output.
- 2026-09-04 (found today) — advice to wait for official Fooocus support for Flux or another new architecture is obsolete today: upstream is LTS with bug fixes only and directs Flux users elsewhere.

## Still unknown

- The supplied direct Windows archive URL, https://github.com/lllyasviel/Fooocus/releases/download/release/Fooocus_win64_1-1-10.7z, could not be inspected in this pass; its contents, checksum, and exact packaging version are not claimed.
- The upstream update log marks v1.0.15 as publicly available but does not give that entry a calendar date, so its exact release timestamp remains unconfirmed.
- No separate product was found behind `fooocus` and `fooocus_v2`: the official discussion identifies the latter as Fooocus 2.0.0, not a different subject.

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
