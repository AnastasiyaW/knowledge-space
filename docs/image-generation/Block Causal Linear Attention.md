---
title: Block Causal Linear Attention
category: architectures
tags: [sana-video, causal, kv-cache, temporal, linear-attention, constant-memory, tiling]
aliases: ["BCLA", "Causal Linear Attention", "SANA-Video Attention"]
---

# Block Causal Linear Attention

Temporal extension of [[SANA]]'s linear attention for sequential processing (video frames or image tiles). Enables constant-memory O(D^2) processing regardless of sequence length.

## How Standard Linear Attention Works

SANA uses ReLU kernel linear attention:
```
O_i = phi(Q_i) * S / (phi(Q_i) * Z)
where:
  S = sum_j phi(K_j)^T * V_j   # running sum, shape [D x D]
  Z = sum_j phi(K_j)^T          # normalizer, shape [D x 1]
  phi(x) = ReLU(x)
```

Key insight: S and Z are **cumulative sums** shared across all queries. Computed once = O(N*D^2) instead of O(N^2*D).

## Extension to Causal (Temporal) Processing

For video or tile-sequence, enforce causality - frame/tile N can only attend to frames/tiles 0..N:

```
For tile t:
  S_t = S_{t-1} + sum_{j in tile_t} phi(K_j)^T * V_j
  Z_t = Z_{t-1} + sum_{j in tile_t} phi(K_j)^T

  O_i = phi(Q_i) * S_t / (phi(Q_i) * Z_t)   # for queries in tile t
```

### Memory: O(D^2) Constant

- S is a D x D matrix (~2240 x 2240 = 5M params for SANA 1.6B)
- Z is a D x 1 vector
- Does NOT grow with number of tiles/frames
- Compare: standard KV cache is O(N * D) and grows linearly

## Application to [[Temporal Tiling]]

Instead of video frames, treat image tiles as the temporal sequence:

1. **Raster-scan order** - top-left to bottom-right
2. Each tile: encode via [[DC-AE]] → 32x32x32 latent (for 1024px tile)
3. Process tile through SANA DiT with causal linear attention
4. Update running sums S and Z
5. Next tile inherits global context from all previous tiles

### Overlap Handling

For overlapping tiles:
- Tokens from overlap zone appear in both tile latents
- Use position encoding to distinguish: RoPE with `(tile_row, tile_col, local_h, local_w)`
- Blend overlap latents with linear weights before VAE decode

## From SANA-Video Implementation

SANA-Video specs:
- 2B params, 720p, up to 1 minute, 16 FPS
- **36s latency** for 5s 720p (vs 1897s for Wan-2.1-14B = 52x faster)
- **Causal Mix-FFN**: caches last frame for temporal convolution causality
- LTX-VAE for video encoding

The same mechanism applied to tiles enables:
- Process 4K image (4096x4096) as ~16 tiles of 1024x1024
- Each tile sees context from all previous tiles
- No seam artifacts on smooth gradients (metal, skin)
- Memory: same as single tile + small S, Z cache

## Comparison with Other Temporal Approaches

| Approach | Memory | Quality | Speed |
|----------|--------|---------|-------|
| Independent tiles + overlap avg | O(1) | Poor (seams) | Fast (parallel) |
| Full self-attention across tiles | O(N^2) | Best | Very slow |
| AnimateDiff temporal modules | O(N) KV cache | Good | Medium |
| **Block Causal Linear Attention** | **O(D^2) constant** | **Good** | **Fast (linear)** |
| SyncDiffusion (gradient sync) | O(1) + grad cost | Good | Slow |

## Implementation Notes

```python
# Pseudocode for causal tile processing
S = torch.zeros(D, D)  # running KV sum
Z = torch.zeros(D, 1)  # running K sum

for tile in raster_scan(image):
    tile_latent = dc_ae.encode(tile)          # [1, 32, 32, 32]
    noise = torch.randn_like(tile_latent)

    # Denoise with causal context
    for step in scheduler.timesteps:
        x_t = scheduler.add_noise(tile_latent, noise, step)
        # Linear attention uses S, Z as accumulated context
        pred = model(x_t, step, text, causal_state=(S, Z))

    # Update running sums with this tile's K, V
    S += phi(K_tile).T @ V_tile
    Z += phi(K_tile).T.sum(dim=-1, keepdim=True)

    denoised_tiles.append(pred)

# Stitch and decode
full_latent = stitch_with_blending(denoised_tiles)
output = dc_ae.decode(full_latent)
```
