---
title: MiniMax-H3 x Z-Image
category: projects
date: 2026-08-24
tags: [minimax-h3-x-z-image, minimax_h3_x_z_image, project]
aliases: ["MiniMax-H3 x Z-Image"]
---

# MiniMax-H3 x Z-Image

**Development line:** `project:minimax-h3-x-z-image` · thread `minimax-h3-x-z-image`  
**Last event:** 2026-08-24 · 1 dated since 2026-08-24 · **Researched:** 2026-11-21 · confidence: medium

## What it is

MiniMax-H3 x Z-Image is a community graft of Z-Image attention statistics onto the open MiniMax-H3 video model, shipped as ComfyUI weights.

- Base: MiniMax-H3 (MiniMaxAI). The official card describes H3-Base, which generates 768p video with audio, 4 to 15 seconds, 24 FPS, 32 kHz stereo. The H3-Omni-Transformer is 33B parameters.
- Derivative: native and GGUF weights by one community author. The GGUF card says the files are "drop-in replacements" that keep identity, voices, speed and VRAM while adding surface detail. These are the author's claims.
- Users: ComfyUI users who already run MiniMax-H3 workflows. The card says the files work with existing MiniMax-H3 workflows, including Multishot canvases.
- Limits: the license is "minimax-h3-community-license" and its text is not on the page. The GGUF card lists 20B parameters, which does not match the official 33B; the page does not explain why.

As of 2026-11, the derivative has no verified independent quality comparison. Check the graft on your own prompts before use.

## Development line

- **2026-08-24 — MiniMax-H3 x Z-Image native and GGUF repositories were linked.** On 2026-08-24, native and GGUF repositories for MiniMax-H3 x Z-Image appeared on Hugging Face. These give two model-format access points, but do not establish release status, contents, or compatibility.

## What changed

- No dated release of the derivative is verified. The native repository page (read 2026-11-21) shows 18 commits, the latest about three months old, without exact dates.
- The official MiniMax-H3 collection page shows "Updated Aug 9" with no release date and no year. It is an update marker, not a release date.

## How to use this

1. Start from the official base card. It defines the open H3-Base checkpoints (FL2VA and Ref2VA), the full-attention-only initial release, and the license reference.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3>
2. Choose a GGUF file by VRAM. The card recommends curve-zs05 files: Q8_0 for about 32 GB, Q5_1 for 24 to 32 GB, Q4_0 for 16 to 24 GB.
  — <https://huggingface.co/joeygambino/MiniMax-H3-x-Z-Image-GGUF>
3. For ComfyUI, use the native repository's variants. The fl2va set lists fp8, int8, mxfp8, nvfp4 and w4a8. The card corrects one label: mxfp8 is 8-bit microscaling, not 4-bit.
  — <https://huggingface.co/joeygambino/MiniMax-H3-x-Z-Image-native/tree/main>
4. Before any commercial use, read the full license. The official card links an application form marked for USA, EU, UK and South Korea, and does not explain its scope.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3>
5. Compare stock MiniMax-H3 and the graft with the same seed and prompt, because the detail and identity claims are the author's measurements.
  — <https://huggingface.co/joeygambino/MiniMax-H3-x-Z-Image-GGUF>

## Best practices

- Run a same-seed A/B test against the stock checkpoint before choosing a graft. The card's figures (high-band ratio 0.99 over three joins versus 1.11 on stock) are self-reported.
  — <https://huggingface.co/joeygambino/MiniMax-H3-x-Z-Image-GGUF>
- Use prompt processing close to the official recommendation. The official card recommends H3-Context-IR or a comparable system for best quality; Context-IR is API-only, not open.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3>
- Match the file to the hardware. The card says mxfp8 is Blackwell-specialized, so use other variants elsewhere.
  — <https://huggingface.co/joeygambino/MiniMax-H3-x-Z-Image-native/tree/main>

## Superseded by this

- Nothing verified as obsolete. The official MiniMax-H3 checkpoints remain the base; this derivative does not replace them.

## Still unknown

- The author's identity and whether MiniMax endorses the derivative: not stated.
- Z-Image upstream: the card calls Z-Image "Lumina2, a 6B image model" and links no upstream page. Not confirmed as the same model as the Z-Image-Turbo listed by ComfyUI-Qlip.
- Parameter count conflict: 20B on the GGUF card versus 33B on the official card.
- The license text was not read. A secondary article reports revenue and jurisdiction terms; that article was not verified against the license file.
- The companion comfy-native repository and the linked Space were not checked.
- Exact release date of the derivative. The stub date 2026-08-24 is kept as recorded.
- Official H3-Regenerate-2K is not yet released, and sparse-attention inference is not in the initial release.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/MiniMaxAI/MiniMax-H3 | MiniMaxAI/MiniMax-H3 — model card | 2026-11-21 |
| https://huggingface.co/joeygambino/MiniMax-H3-x-Z-Image-GGUF | MiniMax-H3 x Z-Image GGUF — model card | 2026-11-21 |
| https://huggingface.co/joeygambino/MiniMax-H3-x-Z-Image-native/tree/main | MiniMax-H3 x Z-Image native — file listing | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:minimax-h3-x-z-image`, thread `minimax-h3-x-z-image`, 1 dated events 2026-08-24 → 2026-08-24.
- **Practical note:** A third-party ComfyUI graft of the open MiniMax-H3 base (official 33B; derivative card says 20B). Quality and identity claims are the author's; verify with same-seed A/B tests, and check the license before commercial use.
- **Confidence:** medium. Official base facts are verified; derivative claims are self-reported. Dated supersedes above are the authority for what is obsolete.
