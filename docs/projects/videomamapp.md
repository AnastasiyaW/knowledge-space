---
title: "VideoMaMa++: videomamapp-release-line — Videomamapp Release Line"
category: "projects"
date: 2026-10-20
tags: ["project", "videomamapp", "videomamapp-release-line"]
aliases: ["VideoMaMa++: videomamapp-release-line"]
---

# VideoMaMa\+\+: videomamapp-release-line — Videomamapp Release Line

**Development line:** project:videomamapp · thread videomamapp-release-line  
**Last event:** 2026-10-20 · 1 dated since 2026-10-20 · **Researched:** 2026-11-28 · confidence: medium

## What it is

VideoMaMa\+\+ \(NeurIPS 2026\) is a mask-guided diffusion video-matting model from Korea University, Adobe Research and KAIST AI. It turns a video plus a coarse mask track into an alpha matte. It is built on Wan 2.1 \(1.3B\) adapted with LoRA \(rank 512\) and uses one denoising step at inference. It is a follow-up to VideoMaMa \(CVPR 2026\).

## Development line

- **2026-10-20 — VideoMaMa\+\+ video alpha-matting model announced for NeurIPS 2026.** The KAIST cvlab team announced VideoMaMa\+\+, a model that generates alpha mattes from a video and a mask, including hair and fine edges. It uses joint spatio-temporal attention over RGB and mask tokens, preserve/refine learned frame tokens, and a sliding window that carries mattes across chunks. The post reports best results on three benchmarks and says no long-video fine-tuning is needed; code is linked as forthcoming.
  - The project page names the paper 'VideoMaMa\+\+: Temporally Consistent Video Matting via Preserve-and-Refine Tokens' \(Sangbeom Lim, Seoung Wug Oh, Heeji Yoon, Seungryong Kim, Joon-Young Lee; Korea University, Adobe Research, KAIST AI\). RGB and mask conditioning are separate token streams combined by full spatio-temporal self-attention, not channel concatenation. Two learnable per-frame embeddings, preserve \(keep this matte as a reference\) and refine \(turn the coarse mask into a fine matte\), enable sliding-window inference: overlap frames carry the previous chunk's matte under the preserve token, and a global reference anchor is supplied to every chunk. Training used 3-frame clips at 1024x1024 for about 2.5 days on 8xH100, and RoPE lets this generalize to 6-frame chunks at test time. The authors chose explicit alpha-matte propagation over reusing an auto-regressive key-value cache, because the cache would let hidden state rather than each chunk's own mask drive the result. Evaluation covers VideoMatte and YouTubeMatte at 1920x1080 and V-HIM60 \(Hard\), with every mask-guided method given the identical SAM3 mask track. The abstract says the method outperforms prior diffusion-based methods in fine-detail accuracy and temporal consistency. (undated project page) — <https://cvlab-kaist.github.io/VideoMaMa-PlusPlus/>

## What changed

Video diffusion backbones only process 6-24 frames at a time, so video is matted in chunks. When each chunk refines its coarse mask independently, edges flicker and transparency jumps at the seams. VideoMaMa\+\+ passes the matte the previous chunk already produced into the next chunk, and adds a shared global reference anchor so errors do not build up on long sequences. The authors say this needs no additional training.

## How to use this

1. Prepare the input video and a coarse mask track for the subject; the model takes RGB frames and the mask as separate token streams and outputs an alpha matte, which can also be composited onto a greenscreen.
  — <https://cvlab-kaist.github.io/VideoMaMa-PlusPlus/>
2. For long videos, run sliding-window inference. Overlap frames carry the previous chunk's matte under the preserve token, and a shared reference anchor is supplied to every chunk. No extra fine-tuning is required.
  — <https://cvlab-kaist.github.io/VideoMaMa-PlusPlus/>

## Best practices

- Propagate finished mattes across chunk boundaries and keep a global reference anchor for every chunk, so errors do not accumulate over long sequences.
  — <https://cvlab-kaist.github.io/VideoMaMa-PlusPlus/>
- When comparing matting methods, give all mask-guided methods the same mask track \(the authors use the identical SAM3 mask track\) so no method gets a privileged mask.
  — <https://cvlab-kaist.github.io/VideoMaMa-PlusPlus/>

## Superseded by this

- Matting each diffusion chunk independently from its own coarse mask is sufficient for video; the authors say it causes flickering edges and discontinuous transparency at chunk boundaries.
  — <https://cvlab-kaist.github.io/VideoMaMa-PlusPlus/>

## Still unknown

- The excerpt of the results table is cut off before the VideoMaMa\+\+ row, so the claim of best results on all metrics across three benchmarks could not be checked. In the visible rows some baselines, such as MaGGIe and MatAnyone 2, post strong numbers.
- The code release date is not stated; the code link is announced as forthcoming.
- The page carries no publication date.

## Sources

| source | title | read |
|---|---|---|
| https://cvlab-kaist.github.io/VideoMaMa-PlusPlus/ | VideoMaMa\+\+: Temporally Consistent Video Matting via Preserve-and-Refine Tokens | 2026-10-20 |

## Agent brief {#agent-brief}

- **Subject:** project:videomamapp, thread videomamapp-release-line, 1 dated events 2026-10-20 → 2026-10-20.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
