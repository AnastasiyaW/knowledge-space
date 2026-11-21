---
title: ComfyUI-MiniMax-H3-LongMedia
category: projects
date: 2026-08-14
tags: [comfyui-minimax-h3-longmedia, comfyui-minimax-h3-longmedia-development, comfyui_minimax_h3_longmedia, project]
aliases: ["ComfyUI-MiniMax-H3-LongMedia"]
---

# ComfyUI-MiniMax-H3-LongMedia

**Development line:** `project:comfyui-minimax-h3-longmedia` · thread `comfyui-minimax-h3-longmedia-development`  
**Last event:** 2026-08-14 · 1 dated since 2026-08-14 · **Researched:** 2026-11-21 · confidence: low

## What it is

ComfyUI-MiniMax-H3-LongMedia is an Apache-2.0 community node pack for long-form MiniMax H3 video and audio generation on limited VRAM.

- Scope: a third-party pack, separate from the built-in MiniMax H3 nodes that ComfyUI ships.
- Users: ComfyUI users with the open MiniMax H3 weights who need clips longer than the base model's native duration.
- Key capability (repository About text only): streamed attention, compressed KV, adaptive VRAM guards and chunked output; the README body was not captured, so these claims are unverified.
- Limits: the MiniMax H3 license excludes the United States, European Union, United Kingdom and South Korea from its terms without a separate license; the open release is 768p and 4 to 15 seconds.

## Development line

- **2026-08-14 — ComfyUI-MiniMax-H3-LongMedia public repository reference.** A public GitHub repository reference for ComfyUI-MiniMax-H3-LongMedia appeared on 2026-08-14. This provides a dated reference point for the project. Available evidence does not establish repository contents, release status, or implementation changes on that date.

## What changed

- 2026-08-03 — ComfyUI shipped day-0 native MiniMax H3 support; it requires ComfyUI 0.30.0 or later. This is separate from the community pack.
- 2026-08-26 — MiniMax's local deployment guide was last reviewed: the open release contains H3-Base FL2VA and Ref2VA; H3-Context-IR and H3-Regenerate-2K are not in it.
- 2026-08-14 — the public repository reference recorded in the stub. The repository has a 0.4.2 release-notes file, but no release dates were visible on the page.

## How to use this

1. Obtain the H3 weights under the MiniMax H3 Community License and check the excluded territories before use.
  — <https://platform.minimax.io/docs/guides/local-deploy-h3>
2. For ordinary generation, use ComfyUI's built-in H3 templates on ComfyUI 0.30.0 or later, or on Comfy Cloud, which already includes commercial rights.
  — <https://blog.comfy.org/minimax-h3-day-0-support-in-comfyui/>
3. Use the community pack only when you need its long-sequence features; install it from its README, which was not captured on 2026-11-21, so verify the install steps there.
  — <https://github.com/vizart-vj/ComfyUI-MiniMax-H3-LongMedia>
4. Plan the output spec: H3-Base produces 1344 × 768 at 24 fps with 32 kHz stereo audio and 4 to 15 seconds per clip.
  — <https://platform.minimax.io/docs/guides/local-deploy-h3>
5. Budget VRAM with the offload recipes in the MiniMax guide; the reference configuration is 8 × B200, which the guide calls "not a minimum-hardware claim".
  — <https://platform.minimax.io/docs/guides/local-deploy-h3>

## Best practices

- Treat local commercial output as licensed only after you hold a MiniMax commercial license; ComfyUI's docs say commercial use of local outputs requires one, available through Comfy.
  — <https://docs.comfy.org/tutorials/video/minimax/minimax-h3>
- Do not quote the 2K resolution for open-weights output: 2K is a hosted-service output and needs a separate upscale pass.
  — <https://docs.comfy.org/tutorials/video/minimax/minimax-h3>

## Superseded by this

- For ordinary generation, the community pack is superseded by ComfyUI's built-in H3 nodes, which shipped on 2026-08-03 with the open weights.

## Still unknown

- Repository maintainer identity and activity: the page shows 76 commits and 15 open issues, but no last-commit date was captured.
- The README body (installation, limitations, benchmarks) was not captured; the feature claims come only from the repository About text.
- Compatibility with the built-in ComfyUI H3 nodes and with the newer template features (for example Multiframe Reference, which requires ComfyUI 0.34.0) was not tested.
- Whether the 2K and 15-second claims in ComfyUI's marketing apply to the open weights: the sources disagree, and the open release is 768p.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/vizart-vj/ComfyUI-MiniMax-H3-LongMedia | Repository overview and About text | 2026-11-21 |
| https://platform.minimax.io/docs/guides/local-deploy-h3 | MiniMax H3 local deployment guide | 2026-11-21 |
| https://blog.comfy.org/minimax-h3-day-0-support-in-comfyui/ | MiniMax H3 day-0 support in ComfyUI | 2026-11-21 |
| https://docs.comfy.org/tutorials/video/minimax/minimax-h3 | ComfyUI MiniMax H3 tutorial | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-minimax-h3-longmedia`, thread `comfyui-minimax-h3-longmedia-development`, 1 dated event 2026-08-14; the upstream model and ComfyUI support are dated 2026-08-03 to 2026-08-26.
- **Practical note:** Check the MiniMax license territories and the ComfyUI version before any use; treat the community pack's claims as unverified until its README is read.
- **Confidence:** low. The community pack's own documentation was not captured. Dated supersedes above are the authority for what is obsolete.
