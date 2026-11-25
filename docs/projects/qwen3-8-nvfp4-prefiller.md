---
title: "Qwen3.8 NVFP4 prefiller (disaggregated quantization): qwen3-8-nvfp4-prefiller-disaggregated-quantization — Qwen3 8 Nvfp4 Prefiller Disaggregated Quantization"
category: "projects"
date: 2026-09-30
tags: ["project", "qwen3-8-nvfp4-prefiller", "qwen3-8-nvfp4-prefiller-disaggregated-quantization"]
aliases: ["Qwen3.8 NVFP4 prefiller (disaggregated quantization): qwen3-8-nvfp4-prefiller-disaggregated-quantization"]
---

# Qwen3.8 NVFP4 prefiller \(disaggregated quantization\): qwen3-8-nvfp4-prefiller-disaggregated-quantization — Qwen3 8 Nvfp4 Prefiller Disaggregated Quantization

**Development line:** project:qwen3-8-nvfp4-prefiller · thread qwen3-8-nvfp4-prefiller-disaggregated-quantization  
**Last event:** 2026-09-30 · 1 dated since 2026-09-30 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Qwen3.8 NVFP4 prefiller streams NVFP4 blocks from SSD during prefill while a low-bit GGUF decoder runs on a Blackwell GPU.

Disaggregated quantization runs prefill and decode with different quantizations of the same model. The Qwen3.8-27B NVFP4 prefiller repository holds NVFP4 transformer blocks streamed off the SSD one layer at a time. They pair with a low-bit GGUF decoder \(IQ1\_S, IQ1\_M, IQ2\_XXS or IQ2\_S\). Decode is memory-bound and benefits from small weights. Prefill is compute-bound, so it gains little from compression below NVFP4 as long as it does not occupy much device memory.

## Development line

- **2026-09-30 — Disaggregated quantization splits prefill and decode across different quantizations.** On 2026-09-30, disaggregated quantization ran prefill under NVFP4 while decode used 1–3-bit weights, with the prefill checkpoint loaded from SSD. The method is reported as working on Qwen3 and Gemma 3, and a Qwen3.8 NVFP4 prefiller checkpoint is listed on HuggingFace.
  - The model card describes the Qwen3.8-27B prefiller. Its checkpoint is 12.8 GiB and never becomes resident. It is read through a two-slot ring carved out of the output head's memory, so the ring adds no device memory. Only the transformer stack's linear projections are disaggregated. Embedding, output head, norms and gated-DeltaNet parameters come from the decoder GGUF. Variants are available for IQ1\_S, IQ1\_M, IQ2\_XXS and IQ2\_S decoders. The card says the released kernels reach speedups closer to 1.3x, because the faster custom FlashInfer integration is not yet released. The card mentions Qwen3.8-27B only, not Gemma 3. It requires a Blackwell consumer GPU \(GB10 or RTX 50-series\). The paper is Panferov et al., 'Disaggregated Quantization: Specializing LLM Prefill and Decode' \(arXiv 2609.26333\). (undated) — <https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller>

## What changed

A Qwen3.8-27B NVFP4 prefiller checkpoint set is published on Hugging Face. A llama.cpp fork runs it alongside a low-bit decoder. The model card says auxiliary prefillers recover about 50% of the accuracy lost to aggressive quantization, at close to no extra memory cost. It also says streaming costs hide under compute once prompts exceed a few thousand tokens.

## How to use this

1. Use a Blackwell consumer GPU \(GB10, sm\_121, or RTX 50-series, sm\_120\). Clone the fork with \`git clone https://github.com/IST-DASLab/disaggregated-llama.cpp.git llama.cpp && cd llama.cpp\`.
  — <https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller>
2. Build with CUDA: \`cmake -B build -DLLAMA\_BUILD\_BORINGSSL=ON -DGGML\_CUDA=ON -DCMAKE\_BUILD\_TYPE=Release\` then \`cmake --build build -j\`.
  — <https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller>
3. Start the server with a decoder and the prefill repo: \`./build/bin/llama-server -ngl 99 -hf unsloth/Qwen3.8-27B-GGUF:IQ1\_S --odp-blocks ISTA-DASLab/Qwen3.8-27B-disaggregated-NVFP4-prefill\`. Both halves download from the Hub, and the prefill variant is chosen from the decoder. For a local decoder, replace \`-hf ...\` with \`-m path/to/decoder.gguf\`.
  — <https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller>

## Best practices

- Pair each prefiller variant with the decoder GGUF it was trained against, because each prefiller complements one specific decode checkpoint. Check the server log line 'odp: prefill variant ...' to confirm which variant was picked.
  — <https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller>
- Leave the micro-batch \(-ub\) alone. It is raised to 8192 so the checkpoint streams once per batch; a lower batch forces more SSD loads.
  — <https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller>
- Pass \`-cram 0 -ctxcp 0\` for benchmarking. Otherwise the server splits prompts to snapshot recurrent state, and each split re-streams the full checkpoint from SSD.
  — <https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller>
- If you pin a CUDA architecture, use 120a or 121a. Plain 120/121 or the 120f family target fail to assemble the block-scaled FP4 MMA.
  — <https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller>

## Superseded by this

- The method makes LLM inference about twice as fast.
  — <https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller>

## Still unknown

- The model card does not mention Gemma 3 or other Qwen3 sizes, so the claim that the method works on them is not confirmed by the linked page.
- The headline 'twice as fast and cheaper' figure comes from unreleased custom kernels. The released code is said to reach about 1.3x.
- The card gives no accuracy benchmark tables beyond the statement that about 50% of the quantization loss is recovered.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller | ISTA-DASLab/Qwen3.8-27B-NVFP4-prefiller · Hugging Face | 2026-09-30 |

## Agent brief {#agent-brief}

- **Subject:** project:qwen3-8-nvfp4-prefiller, thread qwen3-8-nvfp4-prefiller-disaggregated-quantization, 1 dated events 2026-09-30 → 2026-09-30.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
