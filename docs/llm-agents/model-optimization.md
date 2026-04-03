---
title: Model Optimization
category: techniques
tags: [llm-agents, quantization, distillation, pruning, inference, optimization]
---

# Model Optimization

Three complementary techniques for reducing model size and inference cost: distillation (train a smaller model), quantization (reduce numeric precision), and pruning (remove unnecessary weights). These can be combined to achieve 10-50x size reduction with acceptable quality loss.

## Key Facts
- Quantization is the most practical optimization - reduces memory and speeds inference with minimal setup
- Distillation preserves the most quality for a given size reduction
- Pruning can remove 40%+ of attention heads with minimal quality loss
- Combined approach: distill -> prune -> quantize for maximum compression
- GGUF format (llama.cpp/Ollama) is the standard for quantized local inference

## Knowledge Distillation

Large "teacher" model trains smaller "student" model to mimic outputs.

### Types
- **Offline**: teacher pre-trained and fixed, only student trains (most common)
- **Online**: teacher and student train simultaneously
- **Self-distillation**: same network serves as both teacher and student

### Notable Examples
- **DistilBERT**: 6 layers (vs 12), retains 97% of BERT performance at 60% size
- **TinyBERT**: 4 layers, uses attention + hidden state distillation
- **FastBERT**: self-distillation with early exit for simpler inputs

Student learns from teacher's softmax probability distributions (soft labels carry more information than hard labels - the teacher's uncertainty distribution encodes knowledge about class relationships).

## Quantization

Reduces bits per weight to compress models and speed inference.

### Precision Levels

| Precision | Bits/Weight | Memory (7B) | Quality |
|-----------|------------|-------------|---------|
| FP32 | 32 | ~28 GB | Original |
| FP16 | 16 | ~14 GB | Near-original |
| INT8 (Q8) | 8 | ~7 GB | Minimal loss |
| INT4 (Q4) | 4 | ~3.5 GB | Noticeable on complex tasks |
| INT2 (Q2) | 2 | ~1.75 GB | Significant degradation |

### Training Approaches
- **QAT (Quantization Aware Training)**: simulate quantization during training. Higher accuracy but slower.
- **PTQ (Post-Training Quantization)**: quantize after training. Faster but usually lower quality.

### Formats

| Format | Target | Description |
|--------|--------|-------------|
| **GGUF** | CPU | llama.cpp/Ollama format. Standard for consumer hardware |
| **GPTQ** | GPU | Post-training quantization. Fast GPU inference |
| **AWQ** | GPU | Activation-aware. Balances accuracy and speed |

### Practical Usage (Ollama)
```bash
ollama run llama3.1:8b-instruct-q4_0  # Q4 quantized (~4GB)
ollama run llama3.1:8b-instruct-q8_0  # Q8 quantized (~8GB)
```

## Pruning

Remove unnecessary weights or structures to reduce model size.

### Unstructured Pruning
Remove individual weights based on magnitude, gradient, etc. Creates sparse matrices. Requires sparse computation support for actual speedup.

### Structured Pruning
Remove entire blocks - neurons, attention heads, or layers:
- Some BERT attention heads are redundant - can remove up to 40% with minimal quality loss
- Middle layers tend to be most redundant
- FFN neurons can be pruned by contribution magnitude

### Challenges
- Choosing what to prune requires careful analysis
- Often needs additional fine-tuning after pruning
- Finding optimal pruning ratio per layer is non-trivial

## Inference Optimizations

Beyond model compression:
- **KV-cache**: cache key-value pairs for previously seen tokens
- **Continuous batching**: process multiple requests simultaneously
- **Speculative decoding**: small model drafts, large model verifies
- **FlashAttention**: GPU-efficient attention computation (2-4x faster)

## Combined Pipeline

1. **Distill** large model into smaller architecture
2. **Prune** redundant weights/heads from the student
3. **Quantize** remaining weights to lower precision

This cascade enables deployment on edge devices and consumer hardware.

## Gotchas
- Q4 quantization significantly degrades complex reasoning and code generation
- Different quantization methods (GGUF vs GPTQ vs AWQ) are NOT interchangeable - match to your inference runtime
- Pruning benefits are hardware-dependent - sparse matrices need sparse compute support
- Distillation requires access to a powerful teacher model and training infrastructure
- Always benchmark quantized model on YOUR specific task - generic benchmarks don't predict domain performance
- Quantized models may fail at function calling where the full model succeeds

## See Also
- [[ollama-local-llms]] - Running quantized models locally
- [[frontier-models]] - Models available for optimization
- [[fine-tuning]] - LoRA/QLoRA as parameter-efficient alternatives
- [[transformer-architecture]] - Architecture bottlenecks that optimization targets
