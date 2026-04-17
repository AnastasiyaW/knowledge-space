---
title: TTS Fine-Tuning Infrastructure and GPU Platforms
category: reference
tags: [tts, fine-tuning, lora, gpu-rental, runpod, vast-ai, lambda-labs, modal, nebius, vllm, voice-safety]
---

# TTS Fine-Tuning Infrastructure and GPU Platforms

GPU rental platform comparison and deployment patterns for fine-tuning and serving 2B-4B TTS models. Based on April 2026 pricing; rates change frequently — verify before committing.

## GPU Rental Platform Comparison

### On-Demand Pods

| Provider | GPU | USD/hr | Billing | Notes |
|----------|-----|--------|---------|-------|
| RunPod Community | H100 80GB PCIe | $1.99 | per-second | Best price/stability for fine-tune |
| RunPod Community | H100 SXM 80GB | $2.69 | per-second | NVLink for multi-GPU |
| RunPod Community | A100 80GB | $1.19-1.59 | per-second | Base option |
| RunPod Secure | H100 80GB | +$0.10-0.40/hr | per-second | SOC2 compliance |
| Vast.ai | H100 80GB (spot) | $0.90-1.65 | per-minute | Interruptible — risky for long runs |
| Vast.ai | RTX 4090 24GB (spot) | $0.29-0.59 | per-minute | Cost-optimal for LoRA 2B models |
| Lambda Labs | H100 SXM 80GB | $3.78 | per-hour | Zero interruptions, guaranteed |
| Lambda Labs | A100 80GB | $1.48 | per-hour | Most stable A100 option |
| Nebius | H100 80GB | $2.95 | per-hour | Up to 35% commit discount |
| Nebius | L40S 48GB | $1.55-1.82 | per-hour | 48GB covers all 2B-4B TTS models |

### Serverless / Scale-to-Zero

| Provider | GPU | USD/hr effective | Cold Start | Notes |
|----------|-----|-----------------|-----------|-------|
| RunPod Serverless Flex | H100 80GB | $2.72 | 1-2s (FlashBoot) | Best DX/cost for inference |
| RunPod Serverless Active | H100 80GB | $3.35 | ~0 | When >25% uptime expected |
| Modal | H100 | $3.95 | <5s | Clean Python API, no Docker/YAML |
| Modal | A100 80GB | $2.50 | <5s | Sufficient for VoxCPM2 inference |
| Modal | A100 40GB | $2.10 | <5s | Min for 2B model inference |

### Selection Guide

| Scenario | Recommended | Reason |
|----------|------------|--------|
| First LoRA run, 2B model | RunPod Community H100 | $1.99/hr, per-second, no interruption risk |
| Cheapest LoRA (established pipeline) | Vast.ai spot RTX 4090 | $0.30-0.60/hr, save checkpoints every N steps |
| Guaranteed compute for full fine-tune | Lambda Labs A100 | Zero interruption SLA |
| Production inference (moderate traffic) | RunPod Serverless Flex | Scale-to-zero + FlashBoot |
| Rapid prototype inference | Modal A100 40GB | Clean Python, per-second billing |
| Cost-optimized inference (48GB needed) | Nebius L40S | $1.55/hr, underrated tier |

## Fine-Tune Cost Estimates

### VoxCPM2 (2B, tokenizer-free diffusion autoregressive)

LoRA adds <1% parameters. GPU requirements: ≥8GB VRAM minimum, 24GB for normal batch sizes.

**Dataset scale:** 60-120 min clean speech = solid LoRA tier (2-4× recommended minimum of 5-30 min). Full fine-tune is overkill for single-speaker.

| Scenario | GPU | Steps | Time | Cost |
|----------|-----|-------|------|------|
| LoRA, 60 min dataset | RTX 4090 (Vast spot) | 6-8K | 4-6h | $2-4 |
| LoRA, 120 min dataset | RTX 4090 (Vast spot) | 10-15K | 6-10h | $2-6 |
| LoRA, 120 min | H100 RunPod | 10-15K | 2-4h | $4-8 |
| Full fine-tune, 120 min | H100 RunPod | 20-30K | 10-18h | $20-36 |

### Fish-Speech S2 Pro (4B)

+50-80% time vs VoxCPM2. H100 80GB recommended for LoRA; A100 80GB with gradient accumulation.

| Scenario | GPU | Time | Cost |
|----------|-----|------|------|
| LoRA, 120 min | H100 | 4-7h | $8-14 |
| Full fine-tune, 120 min | H100 | 18-30h | $36-60 |

## Inference Real-Time Factor (RTF)

RTF = inference time / audio duration. RTF < 1 = faster than real-time.

| System | GPU | RTF | Notes |
|--------|-----|-----|-------|
| NVIDIA Riva (TensorRT compiled) | A100 | 61.4× | Compiled TRT engines, not general |
| NVIDIA Riva | V100 | 33.7× | |
| Qwen3-TTS (StaticCache + CUDAGraph) | RTX 4090 | 5.6× | Streaming |
| Qwen3-TTS | H100 | 4.2× | |
| Typical 2B-4B model (no deep optimization) | A100/H100 | 2-8× | 125-500ms per second of audio |

**Cost per 1M characters** (rough, ~18.5 hours of audio):

| GPU | RTF | GPU-hours | Cost (RunPod H100) |
|-----|-----|-----------|-------------------|
| H100 | 5× | ~3.7h | ~$7.3 |
| A100 80GB | 3× | ~6.2h | — |

With batching and LoRA hot-swap, effective cost 2-3× lower.

## Multi-LoRA Serving

### vLLM Multi-LoRA

For TTS models with compatible architectures:

```bash
# Enable runtime LoRA loading
VLLM_ALLOW_RUNTIME_LORA_UPDATING=True python -m vllm.entrypoints.openai.api_server \
    --model base_tts_model \
    --enable-lora \
    --max-lora-rank 32

# Load adapter per request via lora_request parameter
```

**Limitation:** vLLM targets LLM architectures. Diffusion AR (VoxCPM2) and dual-AR (Fish S2 Pro) may not be compatible out of the box — verify per model.

### PEFT Manual Switching

For non-vLLM-compatible TTS architectures:

```python
from peft import PeftModel
import time

base_model = load_base_model()  # loaded once, stays in VRAM
adapter_cache = {}

def get_model_for_teacher(teacher_id: str):
    if teacher_id not in adapter_cache:
        path = f"adapters/{teacher_id}"
        adapter_cache[teacher_id] = path
    
    base_model.load_adapter(adapter_cache[teacher_id], adapter_name=teacher_id)
    base_model.set_adapter(teacher_id)
    return base_model
    # Switch time: ~50-200ms depending on adapter size
```

### Storage per Adapter

LoRA rank 16-32 for TTS → 20-100 MB per adapter (compressible). 100 adapters ≈ 5 GB on network volume ≈ $0.35/month on RunPod. Negligible at scale.

## Deployment Patterns

### Pattern A: Persistent Pod (first production version)

```python
# RunPod Pod with custom FastAPI inference server
# Persistent network volume: $0.07/GB/mo
# Structure:
# /volume/
#   base_model/          # Base TTS weights (~10-20 GB)
#   adapters/            # LoRA adapters (100 × 50MB = 5 GB)
#   datasets/            # Training data (optional)

# HTTP endpoint via pod's public URL
# One H100 handles 10-30 parallel audio generation streams
```

### Pattern B: Serverless Flex (scale-to-zero)

```python
# RunPod Serverless: custom Docker image
# - Base model + adapters mounted from network volume
# - Handler returns base64-encoded audio or file URL
# - FlashBoot: 1-2s cold start with cached image
# - Active workers: add N always-on workers when traffic is regular
```

### Pattern C: Modal

```python
import modal

app = modal.App("tts-inference")
volume = modal.Volume.from_name("tts-models")

@app.function(
    gpu="A100",
    volumes={"/models": volume},
    timeout=120,
)
def synthesize(text: str, lora_id: str) -> bytes:
    model = load_with_adapter(f"/models/adapters/{lora_id}")
    return model.synthesize(text)
```

## Voice Safety Infrastructure

Non-optional controls for voice cloning systems:

### Consent Gate

```python
# At dataset upload time:
# 1. Server generates random phrase with 60s TTL
# 2. User reads phrase aloud (microphone, not file upload)
# 3. ASR verifies phrase content
# 4. Speaker verification confirms same voice as training data
# 5. Log consent event with timestamp, user ID, audio hash
```

### Audio Watermarking

Embed imperceptible watermark in every synthesized audio output:
- **AudioSeal** (Meta, open-source): neural watermark, verifiable via API
- **Resemble Neural Watermarking**: commercial, traceable to account
- ElevenLabs embeds watermarks in all generation by default

Embed at vocoder output stage — zero perceptible quality degradation.

### Audit Trail

```python
# Every synthesis request:
audit_log.append({
    "timestamp": datetime.utcnow(),
    "account_id": user_id,
    "lora_id": adapter_id,
    "text_hash": sha256(text),
    "audio_hash": sha256(audio_output),
    "duration_seconds": len(audio) / sample_rate,
})
# Retain for 30-90 days for forensic attribution
```

## Gotchas

- **Vast.ai spot interruption risk**: interruptible instances lose all non-checkpointed work without warning. Never start a 6-hour fine-tune on spot without checkpoint-every-N-steps configured. Use Vast.ai only after the pipeline is validated on non-interruptible hardware.
- **vLLM incompatibility with non-LLM TTS**: vLLM's Multi-LoRA is designed for decoder-only transformer LLMs. VoxCPM2 (tokenizer-free diffusion AR) and Fish-Speech S2 Pro (dual-AR) architectures may require custom serving code. Test explicitly before assuming vLLM will work.
- **60-120 min clean speech = LoRA, not full fine-tune**: with this dataset size, full fine-tune overfits and does not improve over LoRA. Full fine-tune requires 1-5 hours of clean single-speaker audio. Using full fine-tune on a 60-min dataset wastes 2-4× compute with worse results.
- **ConTree microVMs have no confirmed GPU access**: Nebius ConTree is a code execution sandbox for agents, not a GPU compute service. The separate Nebius cloud has H100 and L40S instances. Do not confuse the two when planning compute budget.

## See Also

- [[tts-models]] - TTS architecture families, model comparison
- [[voice-cloning]] - zero-shot cloning vs. fine-tuning approaches
- [[lora-fine-tuning-for-editing-models]] - LoRA training patterns (image domain, partially applicable)
- [[agent-deployment]] - infrastructure patterns for agent-serving backends
