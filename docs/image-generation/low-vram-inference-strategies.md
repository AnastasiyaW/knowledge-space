---
title: Low-VRAM Inference Strategies
category: techniques
tags: [low-vram, memory, offloading, quantization, tiling, attention-slicing, onnx, directml, coreml, inference]
aliases: ["Memory-Efficient Inference", "GPU Memory Optimization"]
---

# Low-VRAM Inference Strategies

Techniques for running image generation and processing models on GPUs with limited VRAM (2-8 GB). Covers quantization, offloading, tiling, and platform-specific optimizations.

## GPU Landscape for Desktop Applications

| Tier | Example GPUs | VRAM | Strategy |
|------|-------------|------|----------|
| Must work | Intel UHD 630, AMD Vega 8 | 1-2 GB shared | CPU fallback |
| Must work | Apple M1/M2 8 GB | 8 GB unified | CoreML |
| Should work | GT 1030, MX250 | 2 GB | Tiling + INT8 |
| Good | GTX 1050/1650 | 4 GB | FP16 + tiling |
| Great | RTX 3060+ | 6-12 GB | Full speed |

Key insight: photographer/retoucher audience skews toward good monitors over powerful GPUs. The 2-4 GB bracket is larger in this demographic than Steam surveys suggest.

## Model Quantization

### Precision Ladder

| Format | Model Size | VRAM at Inference | Quality Impact |
|--------|-----------|-------------------|---------------|
| FP32 | 100% | 100% | Baseline |
| FP16/BF16 | ~50% | ~55-60% | Imperceptible |
| INT8 | ~25% | ~30-35% | Minimal with calibration |
| INT4 | ~12.5% | ~20% | Noticeable on fine detail |

### ONNX Quantization

```bash
# Static INT8 quantization (best quality - requires calibration data)
python -m onnxruntime.quantization.quantize \
    --input model_fp32.onnx \
    --output model_int8.onnx \
    --calibration_data_reader calibration_reader \
    --quant_format QDQ \
    --per_channel

# Dynamic INT8 quantization (simpler, slightly worse)
python -m onnxruntime.quantization.quantize \
    --input model_fp32.onnx \
    --output model_int8_dynamic.onnx \
    --quant_format QDQ
```

### Mixed Precision

Sensitive layers (first convolution, last convolution, normalization) kept at FP16 while the bulk runs INT8. This preserves input/output fidelity while getting most of the memory savings.

### Diffusion Model Quantization

For diffusion transformers, [[diffusion-inference-acceleration|Nunchaku]] provides FP8/NVFP4:

| Model | bf16 | FP8 | NVFP4 |
|-------|------|-----|-------|
| FLUX Klein 9B | ~18 GB | ~10 GB | ~8 GB |
| SANA 1.6B | ~16 GB | ~8 GB | ~6 GB |

## CPU/GPU Offloading

### Model Offloading (diffusers)

```python
# Sequential offload - moves entire model CPU<->GPU
pipe.enable_sequential_cpu_offload()

# Model offload - keeps model on CPU, moves submodules to GPU on demand
pipe.enable_model_cpu_offload()

# For SANA/FLUX training and inference
pipe.vae.enable_tiling()  # decode high-res without OOM
```

`enable_model_cpu_offload()` is preferred - finer granularity, less GPU peak usage. Sequential offload has lower peak but more transfer overhead.

### ONNX Runtime Memory Management

```cpp
Ort::SessionOptions session_options;

// Disable memory pre-allocation patterns
session_options.DisableMemPattern();

// Disable CPU memory arena (don't hoard freed memory)
session_options.DisableCpuMemArena();

// Sequential execution reduces parallel memory pressure
session_options.SetExecutionMode(ExecutionMode::ORT_SEQUENTIAL);

// Full graph optimization (fuses ops, reduces intermediates)
session_options.SetGraphOptimizationLevel(
    GraphOptimizationLevel::ORT_ENABLE_ALL
);

// Limit thread count
session_options.SetIntraOpNumThreads(2);
session_options.SetInterOpNumThreads(1);
```

### Arena Configuration (Fine-Grained)

```cpp
OrtArenaCfg arena_cfg;
arena_cfg.arena_extend_strategy = 1;  // kSameAsRequested (no power-of-2 rounding)
arena_cfg.initial_chunk_size_bytes = 1024 * 1024;  // 1 MB initial
arena_cfg.max_dead_bytes_per_chunk = 0;  // no dead block retention
```

Multiple models (skin, eyes, hair) can share a single allocator via C API to reduce per-session overhead.

## Tile-Based Processing for Memory

### VRAM Per Tile (Typical U-Net Restoration Model, FP16)

| Tile Size | Model (20 MB) | Activations | Total VRAM |
|-----------|--------------|-------------|------------|
| 128x128 | 20 MB | ~30 MB | ~60 MB |
| 256x256 | 20 MB | ~100 MB | ~140 MB |
| 512x512 | 20 MB | ~400 MB | ~450 MB |
| 1024x1024 | 20 MB | ~1.5 GB | ~1.6 GB |

### Adaptive Tile Size Selection

```cpp
size_t available_vram = getAvailableVRAM();
size_t model_size = getModelSize();
size_t overhead = 100 * 1024 * 1024;  // 100 MB safety margin

size_t budget = available_vram - model_size - overhead;

// Empirical: activations ~ tile_pixels * channels * bytes * depth_factor
// FP16 U-Net, 64 channels, 4 levels -> depth_factor ~ 8
int max_tile_side = (int)sqrt(budget / (64 * 2 * 8));
max_tile_side = std::clamp(max_tile_side, 128, 1024);
max_tile_side = (max_tile_side / 32) * 32;  // align to 32
```

### Overlap Strategy

Minimum overlap = receptive_field / 2. For U-Net with 4 downsampling levels: receptive field ~128px, overlap = 64px.

```cpp
// Linear blending in overlap zone
for (int i = 0; i < overlap; i++) {
    float alpha = (float)i / overlap;
    output[x] = tile_left[x] * (1.0f - alpha) + tile_right[x] * alpha;
}
```

**BatchNorm hazard**: BN computes statistics per-tile, not per-image. This causes tile boundary artifacts that overlap cannot fix. Solutions: use LayerNorm/InstanceNorm, or train on tiles matching inference size.

### Multi-Model Pipeline Strategy

For sequential model pipeline (skin -> eyes -> hair -> color):

1. **Sequential load/unload**: one model at a time. Minimum VRAM, maximum latency.
2. **Shared I/O buffers**: all models same input/output size - reuse buffers.
3. **Model fusion**: shared encoder, multiple heads. One load, multiple outputs.
4. **Unified model**: single model does everything. Most memory-efficient but least flexible.

## TensorRT Acceleration (NVIDIA-only)

TensorRT outperforms DirectML and CUDA baseline significantly for ONNX models:

| Backend | Relative Speed | Notes |
|---------|---------------|-------|
| DirectML | 1.0× (baseline) | Any DirectX 12 GPU |
| CUDA (default) | 1.5-2.0× | NVIDIA only |
| TensorRT-RTX EP | **3-5× over DirectML** | NVIDIA RTX/Turing+ required |

**ONNX Runtime TensorRT execution provider:**

```cpp
// C++ API
OrtTensorRTProviderOptions trt_options{};
trt_options.device_id = 0;
trt_options.trt_fp16_enable = 1;          // FP16 for speed
trt_options.trt_engine_cache_enable = 1;  // cache compiled engines
trt_options.trt_engine_cache_path = "./trt_cache/";
trt_options.trt_max_workspace_size = (size_t)2 * 1024 * 1024 * 1024; // 2 GB

session_options.AppendExecutionProvider_TensorRT(trt_options);
session_options.AppendExecutionProvider_CUDA(cuda_options);  // fallback
```

```python
# Python API
import onnxruntime as ort

providers = [
    ('TensorrtExecutionProvider', {
        'device_id': 0,
        'trt_fp16_enable': True,
        'trt_engine_cache_enable': True,
        'trt_engine_cache_path': './trt_cache/',
    }),
    ('CUDAExecutionProvider', {'device_id': 0}),  # fallback
    'CPUExecutionProvider',
]
session = ort.InferenceSession("model.onnx", providers=providers)
```

**FP16 conversion pipeline** (1.5-2× speedup, 10-minute conversion):

```python
from onnxconverter_common import float16

model = onnx.load("model_fp32.onnx")
model_fp16 = float16.convert_float_to_float16(model, keep_io_types=True)
onnx.save(model_fp16, "model_fp16.onnx")
```

## IOBinding: Eliminate GPU-CPU Memory Copies

IOBinding keeps tensors on GPU throughout the pipeline, eliminating redundant copy overhead:

```python
# Without IOBinding: input copied CPU→GPU, output copied GPU→CPU every call
# With IOBinding: tensors stay on GPU; 1.2-1.5× speedup

io_binding = session.io_binding()

# Bind input tensor (already on GPU as numpy/torch)
io_binding.bind_input(
    name='input',
    device_type='cuda',
    device_id=0,
    element_type=np.float32,
    shape=input_tensor.shape,
    buffer_ptr=input_tensor.data_ptr(),  # GPU pointer
)

# Bind output (pre-allocated GPU buffer)
output_tensor = torch.empty(output_shape, dtype=torch.float32, device='cuda')
io_binding.bind_output(
    name='output',
    device_type='cuda',
    device_id=0,
    element_type=np.float32,
    shape=output_shape,
    buffer_ptr=output_tensor.data_ptr(),
)

session.run_with_iobinding(io_binding)
# output_tensor now contains result, still on GPU
```

## ONNX Session Reuse (Cold Start Elimination)

Loading an ONNX session has 200-500ms cold-start cost. Keep sessions loaded between calls:

```python
# BAD: Creates session every call
def process_image(img):
    session = ort.InferenceSession("model.onnx")  # 200-500ms
    return session.run(...)

# GOOD: Session created once, reused
class ModelRunner:
    def __init__(self, model_path):
        self._session = ort.InferenceSession(model_path, providers=providers)

    def process(self, img):
        return self._session.run(...)  # <5ms
```

For multi-model pipelines: keep all sessions loaded even when not processing. Memory cost (~20-50MB per session) is worth eliminating 200-500ms per switch.

## Platform-Specific Paths

### Windows + DirectML

Works with any DirectX 12 GPU (NVIDIA, AMD, Intel). One binary for all vendors.

```cpp
OrtSessionOptionsAppendExecutionProvider_DML(options, 0);
```

DirectML is in maintenance mode (2026) - stable API, no new features. Falls back to shared system memory when dedicated VRAM is exhausted, with significant performance degradation.

### Windows + CUDA (NVIDIA only)

Best performance on NVIDIA. `cudaMallocManaged` enables automatic page migration between CPU and GPU RAM (supported on Pascal+ including GT 1030). Page faults are expensive but transparent.

### macOS + CoreML

Apple Silicon unified memory eliminates the "low VRAM" problem entirely - GPU uses system RAM directly. M1 8 GB has ~5-6 GB available for ML.

```cpp
uint32_t coreml_flags = COREML_FLAG_ENABLE_ON_SUBGRAPH;
OrtSessionOptionsAppendExecutionProvider_CoreML(options, coreml_flags);
```

Neural Engine offloading provides 11+ TOPS on M1. Bandwidth advantage: 68.25 GB/s (M1) vs 12.8 GB/s (GT 1030).

### CPU Fallback (All Platforms)

Always-available fallback. Performance benchmarks (2048x2048 lightweight model):

| CPU | Time |
|-----|------|
| Apple M1 | 0.5-1.5s |
| Ryzen 5 5600 | 1.5-3s |
| i5-10400 | 2-4s |
| i5-7400 | 5-8s |

Acceptable for non-realtime use. For preview: downscale input first.

## Adaptive Runtime Strategy

```cpp
class AdaptiveInference {
    void process(const cv::Mat& image) {
        size_t free_vram = queryFreeVRAM();

        if (free_vram > 2048 * MB)
            processFullImage(image);          // plenty of VRAM
        else if (free_vram > 512 * MB)
            processTiled(image, 512);         // medium tiles
        else if (free_vram > 200 * MB)
            processTiled(image, 256);         // small tiles
        else
            processCPU(image);                // CPU fallback
    }
};
```

## Knowledge Distillation for Lightweight Models

For creating purpose-built small models:

- **SLKD framework**: 85.4% FLOPs reduction, 85.8% parameter reduction, -2.6% PSNR / -0.9% SSIM
- Train full-size teacher model, distill to 5-10x smaller student
- Works for image-to-image tasks (denoising, deblurring, restoration)
- Best long-term strategy: purpose-built small models outperform quantized large models

## Model Architecture Selection for Low VRAM

| Architecture | Params | FP16 Size | VRAM at 512x512 | PSNR | Fits 2GB? |
|-------------|--------|-----------|-----------------|------|-----------|
| Lightweight U-Net | 1-5M | 2-10 MB | ~50-150 MB | 30-33 dB | Yes |
| NAFNet-width32 | ~5M | ~10 MB | ~100-200 MB | 33.7 dB | Yes |
| NAFNet-width64 | ~17M | ~34 MB | ~200-500 MB | Higher | Tiled |
| MobileNet-based | 0.5-3M | 1-6 MB | ~30-100 MB | 28-31 dB | Yes |
| Real-ESRGAN x4v3 | 1.2M | 2.3 MB | ~50-100 MB | Good SR | Yes |
| Real-ESRGAN x4plus | 16.7M | 32 MB | ~300-800 MB | Best SR | Tiled |
| SwinIR | 11.8M | ~24 MB | ~400-1000 MB | 32-34 dB | Tiled only |
| Restormer | ~26M | ~52 MB | ~1-3 GB | SOTA | No |
| INRetouch | 11K | <1 MB | <50 MB | Excellent | Yes |

**Best quality/VRAM ratio:** NAFNet-width32 - uses LayerNorm (no tiling artifacts from BatchNorm), no nonlinear activations (easier INT8 quantization), modular width scaling, clean ONNX export.

**INRetouch** is an outlier - only 11K parameters via implicit neural representation, 70ms on 4K images. Specialized for photography retouching, not general-purpose.

## Progressive Quality (Preview to Full)

```cpp
// Fast preview on any hardware, full quality when user commits
void processAdaptive(const cv::Mat& input) {
    // Preview: downscale 4x, run model, upscale bilinear
    // ~50ms even on CPU at 512x512 from 2048x2048
    cv::Mat preview;
    cv::resize(input, preview, input.size() / 4);
    cv::Mat result = runModel(preview);
    cv::resize(result, result, input.size());  // fast preview

    // Full quality: triggered on user action
    // Use tiled processing at native resolution
}
```

Preview at 1/4 resolution takes ~50ms even on CPU. Apply full resolution only when user confirms the edit.

## Competitor VRAM Requirements

| Application | GPU Minimum | GPU Recommended | Notes |
|------------|------------|-----------------|-------|
| Topaz Photo AI | Integrated (16GB RAM) | 8 GB VRAM | Generative models need 8GB |
| Retouch4me | 4 GB GPU or CPU+OpenCL | - | CPU fallback works |
| Luminar Neo | Integrated | Dedicated GPU | No specific VRAM min |
| Adobe Neural Filters | 4 GB VRAM DX12 | 8 GB+ VRAM | AI Denoise 70% slower at 4GB |

## Gotchas

- **DirectML memory leak**: each ONNX Runtime inference run allocates ~517 MB that is not freed until session destruction. For iterative processing (multiple tiles), destroy and recreate session periodically, or accept growing memory usage
- **Shared memory fallback is deceptive**: DirectML reports "success" when falling back to shared system memory, but performance drops to CPU-equivalent levels. Monitor actual execution time, not just whether the call succeeded
- **INT8 calibration data matters**: dynamic quantization (no calibration) is easy but ~1-2 dB worse PSNR than static quantization with representative calibration images. For production models, always use static quantization
- **ONNX graph optimization level ALL can change memory layout**: this may break assumptions about tensor contiguity. Test thoroughly with your specific model before deploying
- **BatchNorm causes tiling artifacts that overlap cannot fix**: BN computes statistics per-tile, not per-image. Use LayerNorm/InstanceNorm or train on tiles matching inference size. NAFNet uses LayerNorm specifically for this reason
- **Intel iGPU via DirectML can be slower than CPU**: integrated graphics with shared memory + DirectML overhead sometimes runs slower than pure CPU with OpenMP SIMD. Always benchmark both paths and pick the faster one at runtime
- **TensorRT engine cache is device-specific**: a cached engine compiled for RTX 3080 will fail (or produce wrong results) on RTX 3090. Cache key must include device ID and driver version. Set `trt_engine_cache_path` to a device-specific subdirectory.
- **TensorRT first-run compilation**: first inference with TRT EP triggers engine compilation (30s-3min depending on model complexity). Use `trt_engine_cache_enable=1` to cache; subsequent loads are instant.
- **IOBinding and dynamic shapes**: ORT IOBinding requires pre-allocated output buffers with known shapes. For dynamic-output models, fall back to standard `session.run()` for those outputs.

## See Also

- [[diffusion-inference-acceleration]] - Spectrum, TriAttention, sampling speedups
- [[tiled-inference]] - spatial tiling techniques and blending
- [[DC-AE]] - 32x compression reducing memory requirements
- [[SANA]] - efficient architecture with linear attention
