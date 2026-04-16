---
title: Text-to-LoRA
category: models
tags: [hypernetwork, lora-generation, zero-shot, sakana-ai, llm-adaptation, meta-learning, apache-2.0]
aliases: ["T2L", "Doc-to-LoRA"]
---

# Text-to-LoRA (Sakana AI)

Hypernetwork that generates LoRA adapter weights from a natural language task description in a **single forward pass**. No training data needed for downstream tasks. Sub-second adapter generation.

Paper: arXiv:2506.06105 (June 2025, ICML 2025). Follow-up: Doc-to-LoRA (arXiv:2602.15902, Feb 2026). Authors: Sakana AI, Tokyo (Google Brain alumni).

> **Note:** company is **Sakana AI**, not "Cakana". Founded by David Ha and Llion Jones.

## Architecture

```
Task description (text) → Text encoder → embedding
                                            ↓
Concat with: module-type embedding (q_proj, v_proj, etc.)
           + layer-index embedding (which transformer layer)
                                            ↓
MLP blocks → LoRA matrices A and B
             (repeated for all target modules/layers)
```

Generated LoRAs: **q_proj and v_proj, rank 8, ~3.4M adapter params**.

### Hypernetwork Sizes

| Size | Parameters |
|------|-----------|
| Large | 55M |
| Medium | 34M |
| Small | 5M |

Doc-to-LoRA extension: Perceiver-based (~309M params), consumes variable-length documents.

## Training

Two approaches:
1. **LoRA Reconstruction:** train T2L to reconstruct pre-trained oracle LoRAs from task descriptions
2. **SFT:** end-to-end optimization through downstream task loss (better generalization)

Training data: 479 diverse tasks from Lots-of-LoRAs dataset. Scaling 16→479 tasks substantially improved zero-shot.

## Supported Base Models

Mistral-7B (67%), Llama-3.1-8B (77%), Gemma-2-2b (66%).

## Key Innovation

Eliminates training data + compute bottleneck for LoRA fine-tuning. Describe task in text → get working adapter instantly.

Even with random/meaningless descriptions, SFT-trained T2L generates "reasonable" LoRAs — it learns task patterns beyond just text.

## Limitations

- **LLM only** — does NOT generate LoRAs for image/video diffusion models
- Fixed rank-8 LoRAs (bottleneck for complex tasks)
- Meta-training expensive (days on multi-GPU), inference is sub-second
- Out-of-distribution tasks remain difficult

## License

**Apache 2.0** — fully commercial.

## Relevance for [[lora-fine-tuning-for-editing-models|Editing Model LoRAs]]

Currently LLM-only, but the principle of hypernetwork-generated LoRAs could extend to diffusion models. If adapted for [[MMDiT]], could enable instant task-specific editing adapters from text descriptions — e.g., "remove jewelry scratches" → LoRA weights.

## Key Links

- GitHub: github.com/SakanaAI/text-to-lora
- GitHub (D2L): github.com/SakanaAI/doc-to-lora
