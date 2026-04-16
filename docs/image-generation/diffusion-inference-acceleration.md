---
title: Diffusion Inference Acceleration
category: techniques
tags: [inference, acceleration, spectrum, triattention, kv-cache, quantization, nunchaku, sampling, spectral-forecasting]
aliases: ["Spectrum", "TriAttention", "Inference Speedup"]
---

# Diffusion Inference Acceleration

Techniques for accelerating diffusion model inference without quality loss. Covers spectral forecasting, KV cache compression, quantization, and sampling optimization.

## Spectrum - Spectral Forecasting

Accelerates diffusion sampling by 3.5-4.8x through frequency-domain analysis. Instead of running the full denoiser at every timestep, Spectrum identifies which frequency components actually change between adjacent steps and only recomputes those.

### How It Works

1. **Analyze frequency spectrum** of denoiser output at each step via FFT
2. **Identify static frequencies** - many high-frequency components stabilize early in the denoising process
3. **Forecast static components** from previous step, only run the model on changing frequencies
4. **Reconstruct** full output by combining forecasted + computed components

The key insight: during diffusion sampling, low-frequency structure (composition, color) settles first, while high-frequency detail (texture, edges) continues evolving. But even high-frequency components become predictable in later steps.

### Performance

| Model | Speedup | Quality Impact |
|-------|---------|---------------|
| FLUX.1 | 3.5-4.79x | No measurable degradation |
| HunyuanVideo + FLUX.1 | 3.5x | No measurable degradation |
| Wan 2.1-14B | 4.67x | No measurable degradation |
| SDXL | Supported | No measurable degradation |

### ComfyUI Integration

Available as `ComfyUI-Spectrum-Proper` nodes. Supports FLUX, WAN, and SDXL architectures. Drop-in replacement for standard sampling - no workflow restructuring needed.

```python
# Conceptual usage (diffusers)
from spectrum import SpectralForecaster

forecaster = SpectralForecaster(
    model=pipe.transformer,
    threshold=0.1,  # frequency change threshold
)

# During sampling loop, forecaster decides per-step
# which frequency bands need full model evaluation
```

## TriAttention - KV Cache Compression

Compresses KV cache memory by 10.7x through trigonometric representation of attention matrices. Primarily targets LLM inference but applicable to any transformer with KV caching.

### Mechanism

Standard KV cache stores full K and V tensors for all previous tokens. TriAttention represents these via trigonometric decomposition:

- Encode K/V vectors into compact trigonometric coefficients
- Reconstruct attention weights from coefficients on-the-fly
- 10.7x memory reduction with 2.5x generation speed improvement

### Practical Integration

Available as a vLLM plugin. For diffusion transformers (DiT, [[MMDiT]]), KV cache compression matters most during:

- Tiled inference with cross-tile attention (see [[temporal-tiling]])
- Long-context conditioning (multiple reference images)
- Video generation with temporal attention

## TurboQuant - Extreme KV Cache Quantization

Compresses KV cache to 3 bits per element without model retraining. Uses random rotation of vectors + scalar quantization.

### Algorithm

```text
1. Apply random orthogonal rotation R to K/V vectors
2. Quantize rotated vectors to 3-bit scalars (table lookup)
3. At attention time: dequantize, apply R^T, compute attention normally
```

~5-6x memory compression at 99.5% attention fidelity.

### Implementation Status

```bash
# llama.cpp fork (working)
git clone https://github.com/TheTom/llama-cpp-turboquant
cd llama-cpp-turboquant && make -j
./llama-server -m model.gguf --cache-type-k turbo3 --cache-type-v turbo3
```

| Runtime | Status |
|---------|--------|
| llama.cpp fork | Working, CPU, all tests pass |
| llama.cpp mainline | Merge pending |
| vLLM | Feature request open |
| Apple Silicon | 4.6x compression, matches q8_0 speed |

### Practical Notes

- Best gains on long contexts (128K+). At 4K context, difference is minimal
- Base weight quantization affects quality: Q8_0+ gives best results, Q4_K_M degrades more
- QJL correction (second stage) can worsen quality through standard attention - use TurboQuant_mse variant
- The rotation trick is simple (table lookup), which is why implementations appeared within hours of publication

## Nunchaku - Weight Quantization for DiT

NVFP4 and INT8 quantization specifically optimized for diffusion transformers.

### FLUX Klein 9B Quantization

```python
# Nunchaku quantized Klein inference
# 40-55% VRAM reduction vs bf16
from nunchaku import load_quantized_model

model = load_quantized_model(
    "flux2-klein-9b-nunchaku",
    dtype="nvfp4"  # or "int8"
)
```

| Precision | VRAM (9B) | Quality | Speed |
|-----------|-----------|---------|-------|
| bf16 | ~18 GB | Baseline | 1.0x |
| FP8 | ~10 GB | Near-identical | ~1.1x |
| NVFP4 | ~8 GB | Slight softening | ~1.3x |
| INT8 (W8A8) | ~9 GB | Near-identical | ~1.2x |

FP8 Klein maintains desirable grain structure (16mm film look). Non-FP8 produces cleaner output (35mm film character).

## Sampling Optimization

### Step Reduction for Distilled Models

Distilled models (FLUX Klein distilled, [[SANA]]-Sprint) are step-optimized:

| Model | Design Steps | Usable Range | Quality Cliff |
|-------|-------------|-------------|---------------|
| Klein 9B distilled | 4 | 4-8 | >8 degrades |
| SANA-Sprint | 1-4 | 1-4 | N/A (designed for 1-step) |
| FLUX.1-schnell | 4 | 4-8 | >8 degrades |

Using 50+ steps on a 4-step distilled model wastes compute and can actively degrade quality.

### Sampler Compute Efficiency

Different samplers have different compute cost per step:

| Sampler | Compute/Step | Notes |
|---------|-------------|-------|
| euler | 1x | Baseline, most stable |
| res_2s | ~2x | Effectively doubles work per step |
| dpmpp_2m | ~1.5x | Good quality/speed balance |
| euler_ancestral | ~1x | Adds stochasticity |

`res_2s` at 4 steps is computationally equivalent to `euler` at 8 steps. Useful for fixing anatomy issues without increasing step count.

### Combined Acceleration Stack

For maximum throughput:

```text
1. Spectrum spectral forecasting     (3-5x speedup)
2. Nunchaku FP8/NVFP4 quantization  (1.1-1.3x speedup)
3. Optimal step count                (no wasted steps)
4. VAE tiling for decode             (enables high-res)
```

These stack multiplicatively. FLUX.1 with Spectrum + FP8 achieves ~4-6x total acceleration.

## Gotchas

- **Spectrum + LoRA interaction**: spectral forecasting assumes stable frequency patterns. Heavy LoRA influence can shift which frequencies change per step, potentially requiring threshold tuning. Test with your specific LoRA before production use.
- **Quantization + fine detail**: NVFP4 quantization slightly softens fine textures (hair strands, fabric weave). For product photography where texture detail is critical, FP8 is the safe choice over NVFP4.
- **Distilled model CFG**: distilled models have guidance baked in. Setting CFG above 1.0-1.5 produces "deep-fried" artifacts. Klein 9B distilled requires CFG=1.0 specifically.
- **TurboQuant on short contexts**: at 4K tokens or fewer, the overhead of rotation/dequantization can negate memory savings. Only beneficial for 32K+ contexts.

## See Also

- [[SANA]] - linear attention + 32x compression for native efficiency
- [[flow-matching]] - fewer steps needed vs DDPM
- [[tiled-inference]] - spatial tiling for high-res
- [[temporal-tiling]] - cross-tile context propagation
- [[DC-AE]] - 32x VAE compression reducing token count
