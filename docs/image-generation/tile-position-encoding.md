# Tile Position Encoding in Diffusion Models

Methods for injecting spatial position information into patch/tile-based image models, with emphasis on coordinate channel concatenation (proven +10.32 dB over no encoding) and global context injection strategies.

## Coordinate Channel Concatenation (PaDIS Pattern)

The most proven technique. Add 2 extra input channels encoding normalized tile coordinates.

```python
import torch
import numpy as np

def make_coord_channels(tile_h: int, tile_w: int,
                        full_h: int, full_w: int,
                        top: int, left: int) -> torch.Tensor:
    """
    Returns (2, tile_h, tile_w) coordinate channels in [-1, 1].
    top/left are pixel offsets of this tile in the full image.
    """
    ys = torch.linspace(top, top + tile_h - 1, tile_h) / (full_h - 1) * 2 - 1
    xs = torch.linspace(left, left + tile_w - 1, tile_w) / (full_w - 1) * 2 - 1
    grid_y, grid_x = torch.meshgrid(ys, xs, indexing='ij')
    return torch.stack([grid_x, grid_y], dim=0)  # (2, H, W)

def add_position_to_tile(tile_latent: torch.Tensor,
                         coord_channels: torch.Tensor) -> torch.Tensor:
    """Concat coordinate channels to tile latent along channel dim."""
    # tile_latent: (B, C, H, W) — standard 4ch latent
    # coord_channels: (2, H, W) — x/y coords
    coords = coord_channels.unsqueeze(0).expand(tile_latent.shape[0], -1, -1, -1)
    return torch.cat([tile_latent, coords], dim=1)  # (B, C+2, H, W)
```

**Ablation evidence (PaDIS, NeurIPS 2024, arxiv 2406.02462):**

| Configuration | PSNR |
|---------------|------|
| Without position encoding | 23.25 |
| With coordinate channels | **33.57** |

**+10.32 dB.** Model completely failed without position encoding.

**Architecture note:** Only the first convolution layer needs to change (4ch → 6ch input). No other changes needed.

## Global Context Injection

Tiles need to know their spatial context within the full image. Three approaches ranked by precision:

### Spatial: Downscaled Full-Image Latent

```python
def prepare_global_context(full_image: torch.Tensor,
                           vae,
                           target_res: int = 256) -> torch.Tensor:
    """
    Encode downscaled full image as spatial context.
    Returns latent (B, 4, target_res//8, target_res//8).
    """
    import torch.nn.functional as F
    downscaled = F.interpolate(full_image, size=(target_res, target_res),
                               mode='bicubic', align_corners=False)
    with torch.no_grad():
        latent = vae.encode(downscaled).latent_dist.sample()
    return latent * vae.config.scaling_factor

# Usage: concat with tile latent if same spatial size,
#        or inject via cross-attention if different size
```

**VAE latent bias:** Low frequencies reconstructed well; HF textures poorly preserved. For color/structure context this is sufficient.

### Vector: AdaLN-Zero for Global Properties

```python
class GlobalPropertyEncoder(torch.nn.Module):
    """Compress full image to low-dim vector for AdaLN conditioning."""
    def __init__(self, out_dim: int = 128):
        super().__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.AdaptiveAvgPool2d((8, 8)),
            torch.nn.Flatten(),
            torch.nn.Linear(4 * 8 * 8, 256),  # 4 = latent channels
            torch.nn.SiLU(),
            torch.nn.Linear(256, out_dim),
        )
    def forward(self, full_latent: torch.Tensor) -> torch.Tensor:
        return self.encoder(full_latent)  # (B, out_dim)
```

**DiT ablation (Peebles 2023) — conditioning method FID at 400K steps:**

| Method | FID |
|--------|-----|
| Token prepend (in-context) | ~65 |
| Cross-attention | ~47 |
| AdaLN | ~42 |
| **AdaLN-Zero** | **~35** |

AdaLN-Zero initialized with zero-scale (no modulation at init) trains most stably.

### Complete Multi-Signal Architecture

```text
For each tile:
  input = concat(tile_latent[4ch], x_coords[1ch], y_coords[1ch], global_latent[4ch])
          → 10-channel input to U-Net first conv

  At each U-Net / DiT block:
    features = AdaLN_Zero(features, global_vector[128d])   ← global color/exposure
    features = CrossAttn(features, text_embedding)          ← optional text guide
    features = SelfAttn(features)
```

## Position Encoding Method Comparison

| Method | Extra params | Resolution-independent | Tiled PSNR gain | Complexity |
|--------|-------------|----------------------|-----------------|-----------|
| **Coord channels (PaDIS)** | +2 channels | Yes | **+10.32 dB** | Trivial |
| 4-tuple scale+offset (HPDM) | +3-4 channels | Yes (relative) | FVD +18 | Low |
| 2D Sinusoidal | +2L channels | Yes | Not tested | Low |
| M-RoPE (Qwen2-VL) | In attention | Yes | Small | In attention |
| Learned 2D grid (ViT) | 1 embed/patch | No (needs interp) | Baseline | Standard |
| Token order only (LLaVA) | 0 | Yes | Implicit | None |

**Recommendation for tiled editing:**
1. Primary: coordinate channels (proven, zero architecture overhead)
2. Enhanced: sinusoidal encoding at multiple frequencies for multi-scale awareness
3. Optional flags: `is_edge_tile`, `is_corner_tile`, `distance_from_center`

## Injection Method Selection

| Conditioning signal | Recommended method | Reason |
|--------------------|--------------------|--------|
| Tile (x, y) coordinates | **Channel concat** | Spatial, aligned, proven 10dB |
| Global image features (color, exposure) | **AdaLN-Zero** | Low-dim vector, stable |
| Downscaled full image (spatial) | **Channel concat** if same res; **cross-attn** if different | Spatial alignment |
| CLIP embedding (style) | **Decoupled cross-attention** (IP-Adapter) | Variable length |
| Text prompt | **Cross-attention** | Standard |
| Structural map (edges/depth) | **ControlNet / T2I-Adapter** | Spatial, modular |
| Timestep | **AdaLN-Zero** (DiT) / **FiLM** (U-Net) | Scalar |

## Multi-Scale Position Encoding (HPDM Pattern)

```python
def cross_level_coords(scale_l: float, delta_l: tuple,
                       scale_k: float, delta_k: tuple) -> torch.Tensor:
    """
    Cross-level coordinate for hierarchical patch diffusion.
    c_hat(c_l, c_k) = [s_l/s_k; (delta_l - delta_k)/s_k]
    """
    scale_ratio = torch.tensor(scale_l / scale_k)
    offset_ratio = (torch.tensor(delta_l) - torch.tensor(delta_k)) / scale_k
    return torch.cat([scale_ratio.unsqueeze(0), offset_ratio])
```

Used in hierarchical pyramid models where tiles at different resolutions need to reference their relationship.

## Gotchas

- **Issue:** Coordinate channels normalized to [0, 1] instead of [-1, 1] — model may not center-balance the position signal. -> **Fix:** Always normalize to [-1, 1]: `x_norm = x / (W - 1) * 2 - 1`. This matches standard conv/attention initialization ranges.
- **Issue:** Global latent resolution (e.g., 32×32) doesn't match tile latent resolution (e.g., 64×64) for channel concatenation. -> **Fix:** Upsample global latent to tile latent resolution before concat, or use cross-attention instead.
- **Issue:** With SANA's NoPE (no position encoding), convolution provides implicit locality within receptive field. Copying this pattern to tiled models breaks inter-tile consistency. -> **Fix:** SANA's implicit locality works within a single pass; tiles need explicit global position to know WHERE they are in the full image. NoPE is not applicable to tiled pipelines.
- **Issue:** Coordinate channels at inference differ from training distribution when image aspect ratios vary. -> **Fix:** Always compute coordinates relative to the full image's actual H/W at inference, not a fixed assumed resolution.

## See Also

- [[tiled-inference]]
- [[temporal-tiling]]
- [[diffusion-inference-acceleration]]
- [[flux-klein-9b-inference]]
