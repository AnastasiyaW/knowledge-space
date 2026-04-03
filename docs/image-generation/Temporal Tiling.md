---
title: Temporal Tiling (Tiles as Temporal Sequence)
category: techniques
tags: [tiling, temporal-attention, tiles-as-frames, animatediff, sliding-window, context-propagation, high-resolution, nuwa-infinity, multidiffusion]
aliases: ["Tiles-as-Frames", "Temporal Tile Processing"]
---

# Temporal Tiling: Treating Image Tiles as a Temporal Sequence

The idea: instead of processing tiles independently (standard tiling), treat them as a **temporal sequence** where each tile knows the context of previously generated tiles — like frames in a video. This eliminates seam artifacts and maintains global coherence.

## The Problem with Standard Tiling

Standard tiled diffusion (MultiDiffusion, [[Tiled Inference]]) processes tiles independently and blends overlaps by averaging. This causes:
- Seam artifacts on smooth gradients (metal surfaces, skin)
- Inconsistent lighting/color across tiles
- Duplicated objects (same prompt, different tiles → same content repeated)

## Approaches — From Simple to Full

### Level 0: Overlap Averaging (MultiDiffusion)

```
Tile A [====overlap====] Tile B
       averaged in overlap zone
```
Fast, parallel, but quality limited. Averaging smears details.

### Level 1: Gradient Sync (SyncDiffusion, NeurIPS 2023)

At each denoising step, compute perceptual loss between overlapping predicted images → backprop gradients → nudge tiles toward consistency. 66% preference over MultiDiffusion. No retraining. Slow (gradient computation per step).

### Level 2: Global + Local (DemoFusion, AccDiffusion)

Generate low-res global image first → use as structural guide for high-res tiles:
- **DemoFusion**: skip-residual from low-res + dilated sampling for global paths
- **AccDiffusion v2**: ControlNet from low-res + patch-content-aware prompts (avoids object duplication)
- **FreeScale**: Scale Fusion separates self-attention into global (low-freq) and local (high-freq)

### Level 3: Cross-Attention to Previous Tile (IP-Adapter Pattern)

After generating tile N, encode its latent. When generating tile N+1, inject previous tile features via cross-attention (like [[PixelSmile|IP-Adapter]]).

~22M extra params. Fast. But only sees immediate predecessor — error accumulates.

### Level 4: Temporal Attention Modules (AnimateDiff Pattern)

**Treat tiles as video frames.** Insert temporal self-attention after each spatial block:

```
Spatial layers: each tile processed independently
                (temporal axis → batch dimension)
                          ↓
Temporal attention: process ACROSS tiles
                (spatial axes → batch dimension)
                          ↓
Each spatial position attends to same position in all tiles
```

Zero-initialized output projection → identity at start → pretrained spatial model protected.

**Pros**: bidirectional attention, learned consistency
**Cons**: O(N^2) in number of tiles, requires training temporal modules

### Level 5: Causal Temporal Attention (SANA-Video / GPDiT Pattern)

Generate tiles sequentially with causal masking — each tile attends only to previously generated tiles:

```
Tile 0 (top-left): generated normally
Tile 1: attends to Tile 0
Tile 2: attends to Tiles 0, 1
...
```

**GPDiT variant**: each noisy tile attends to previous CLEAN tiles (already denoised). Ablating clean-clean attention saves ~50% FLOPs.

**Sparse causal** (Tune-A-Video): each tile attends only to first tile + immediate neighbor. Efficient.

### Level 6: NUWA-Infinity Pattern (Autoregressive Patches)

Microsoft's system — **closest prior art** to tiles-as-sequence:
- **Nearby Context Pool (NCP)**: caches previously generated patches as context for current patch
- **Arbitrary Direction Controller**: learns optimal generation order
- Global patch-level autoregressive model for inter-patch dependencies
- Local token-level generation within each patch
- "Render-and-optimize": each patch optimized immediately, hidden states saved as context

### Level 7: Hybrid (Best of All Worlds)

Combine global guidance + neighbor cross-attention:
1. Generate low-res global image (DemoFusion)
2. For each tile: inject global context via skip-residual AND inject neighbor tile features via MVDiffusion-style Correspondence-Aware Attention (CAA)
3. Parallelizable (tiles depend on global + overlap, not on each other sequentially)

## For [[SANA]] Specifically

SANA's linear attention makes temporal tiling uniquely practical:

1. **Linear complexity O(N)** — extending token sequence with neighbor tiles costs linearly, not quadratically
2. **32× DC-AE compression** — tile latents are extremely compact (32×32 for 1024px tile)
3. **SANA-Video already exists** — Block Causal Linear Attention with constant-memory KV cache. **Same mechanism directly applicable to tiles.**
4. **Causal Mix-FFN** in SANA-Video caches last frame of previous block for temporal convolution — maps to last row of previous tile for spatial tiling

**Minimum viable approach for SANA:**
Extend RoPE position encoding to include 2D tile position. When generating a tile, concatenate its tokens with tokens from overlapping regions of adjacent (already generated) tiles. Linear attention handles cross-tile consistency at O(N) cost.

**Full approach:**
Port SANA-Video's Block Causal Linear Attention to 2D spatial tiling. Each tile = one "frame". KV cache stores cumulative statistics from previous tiles (O(D^2) memory regardless of tile count).

## Key Papers

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| MultiDiffusion | 2023 | Overlap averaging baseline |
| SyncDiffusion | NeurIPS 2023 | Gradient-based sync |
| MVDiffusion | NeurIPS 2023 | Correspondence-Aware Attention |
| DemoFusion | CVPR 2024 | Progressive upscale + skip residual |
| ScaleCrafter | ICLR 2024 | Re-dilation of convolutions |
| AccDiffusion v2 | 2024 | Content-aware tile prompts + ControlNet |
| FreeScale | ICCV 2025 | Scale Fusion, 8K generation |
| Sliding Tile Attention | 2025 | Tile-granularity sliding window, 7× faster |
| NUWA-Infinity | NeurIPS 2022 | Autoregressive tile generation |
| Hierarchical Patch Diffusion | CVPR 2024 | Deep Context Fusion coarse→fine |
| SANA-Video | ICLR 2026 | Block Causal Linear Attention for video |

## Memory Comparison

| Approach | VRAM per tile | Consistency | Speed |
|----------|-------------|-------------|-------|
| MultiDiffusion | ~baseline | Poor | Fast (parallel) |
| SyncDiffusion | ~1.5× | Good | Slow (gradients) |
| DemoFusion | ~1.2× | Good | Slow (progressive) |
| Temporal attention (all) | ~N× | Excellent | Slow (O(N^2)) |
| Causal (sequential) | ~1.5× + KV | Very good | Medium |
| **SANA causal linear** | ~1.2× + O(D^2) KV | Very good | **Fast (O(N))** |
| Hybrid (global + CAA) | ~2-3× | Very good | Medium (parallel) |
