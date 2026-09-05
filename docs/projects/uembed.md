---
title: UEmbed
category: projects
date: 2026-08-05
tags: [project, uembed]
aliases: ["UEmbed"]
---

# UEmbed

**Development line:** `project:uembed` · thread `uembed`  
**Last event:** 2026-08-05 · 1 dated since 2026-08-05 · **Researched:** 2026-09-05 · confidence: medium

## What it is

UEmbed is a Qwen3.5-based decoder-only embedding family for teams that would otherwise operate separate dense and sparse retrievers.

- Dense and sparse representations: produces normalized dense vectors and sparse lexical vectors in one causal forward pass.
- Multimodal encoding: encodes text, images, video, and mixed inputs for retrieval and visual-document search.
- Model family: ships as UEmbed-2B, UEmbed-4B, and UEmbed-9B; sparse inference requires the `sparse_info.json` and `sparse_weights.pt` sidecars.

## Development line

- **2026-08-05 — UEmbed public project, code, and UEmbed-9B resources were linked.** On 2026-08-05, we linked the official project page, its GitHub source repository, and the UEmbed-9B model page on Hugging Face. The dated links establish a public-facing project-and-model availability milestone, but do not establish a specific release version, benchmark, or capability claim.

## What changed

- 2026-08-05 — UEmbed’s initial release was documented as 2B, 4B, and 9B decoder-only multimodal checkpoints that emit dense and sparse representations.
- 2026-08-13 — Inference moved to native Transformers loading without `trust_remote_code` or processor patching, and gained a vLLM backend for dense and sparse serving.
- 2026-08-15 — The project reported MMEB-v3 leadership on text and agent tracks and second place among open models on MMEB-v2 behind Qwen3-VL-Embedding.
- 2026-08-17 — Supervised fine-tuning support with ms-swift was added.

## How to use this

From 2026-08-05, we can evaluate UEmbed through its official project documentation, inspect its source repository, and locate the UEmbed-9B model resource. Do not infer unverified performance or compatibility claims.

1. Install a current Qwen3.5/Qwen3-VL-compatible runtime: `transformers>=5.4.0`, PyTorch, qwen-vl-utils, tokenizers, Hugging Face Hub, Pillow, and NumPy.
  — <https://github.com/Alibaba-NLP/UEmbed>
2. Choose the 2B, 4B, or 9B checkpoint and download its complete repository; keep the sparse sidecar files alongside the weights.
  — <https://github.com/Alibaba-NLP/UEmbed>
3. Load `Qwen35Embedder`, pass dictionaries containing text, image, video, or mixed inputs, and supply a task instruction for retrieval queries when appropriate.
  — <https://huggingface.co/Alibaba-NLP/UEmbed-9B>
4. Select `pooling="last.normal"` for dense vectors or `pooling="splade.last"` for sparse lexical vectors, then send the chosen representation to the corresponding retrieval index.
  — <https://github.com/Alibaba-NLP/UEmbed>

## Best practices

- Download the whole checkpoint repository; sparse mode will not work without both sparse sidecar files.
  — <https://github.com/Alibaba-NLP/UEmbed>
- Instantiate only the dense or sparse pooling mode required by the retrieval path instead of assuming one output format fits both indexes.
  — <https://github.com/Alibaba-NLP/UEmbed>
- Use task-specific query instructions for retrieval, and use BF16 plus FlashAttention 2 only where the deployed GPU/runtime supports it.
  — <https://github.com/Alibaba-NLP/UEmbed>

## Superseded by this

- 2026-08-13 — Earlier inference guidance requiring `trust_remote_code` or processor patching is obsolete for the official native Transformers path.

## Still unknown

- No immutable repository or model-card snapshot was found to independently prove that all three checkpoint files were downloadable on 2026-08-05; the paper says they were released, while the dated links include the 9B card.
- The 2026-08-15 benchmark claims are project-reported and were not independently reproduced.
- The Hugging Face card labels the checkpoint UEmbed-9B but displays “Model size 8B params”; the official materials do not explain the difference.

## Sources

| source | title | read |
|---|---|---|
| https://alibaba-nlp.github.io/UEmbed/ | UEmbed: Unified Sparse and Dense Multimodal Embeddings | 2026-09-05 |
| https://github.com/Alibaba-NLP/UEmbed | Alibaba-NLP/UEmbed | 2026-09-05 |
| https://huggingface.co/Alibaba-NLP/UEmbed-9B | Alibaba-NLP/UEmbed-9B | 2026-09-05 |
| https://arxiv.org/abs/2608.02583 | UEmbed: Unified Sparse and Dense Multimodal Embeddings | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:uembed`, thread `uembed`, 1 dated events 2026-08-05 → 2026-08-05.
- **Practical note:** From 2026-08-05, we can evaluate UEmbed through its official project documentation, inspect its source repository, and locate the UEmbed-9B model resource. Do not infer unverified performance or compatibility claims.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.