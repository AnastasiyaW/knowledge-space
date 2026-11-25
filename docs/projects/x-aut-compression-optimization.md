---
title: "X-AuT"
category: "projects"
date: 2026-09-14
tags: ["project", "x-aut-compression-optimization"]
aliases: ["X Aut Compression Optimization: x-aut-compression-optimization"]
---

# X-AuT

**Development line:** project:x-aut-compression-optimization · thread x-aut-compression-optimization  
**Last event:** 2026-09-14 · 2 dated since 2026-09-10 · **Researched:** 2026-11-25 · confidence: high

## What it is

X-AuT is an open XPeng method that compresses the Qwen3-ASR-0.6B audio encoder for speech LLMs on automotive PPUs.

- **Audio-tower pruning**: cuts whole Transformer blocks from the Qwen3-ASR-0.6B audio encoder.
- **Quality recovery**: aligns representations and distills from a frozen Qwen3-ASR-1.7B teacher under scheduled student-policy supervision and LoRA finetuning.
- **Full title**: Progressive Audio-Encoder Compression for Speech LLMs with Cross-Scale Distillation.

## Development line

- **2026-09-10 — X-AuT repository update.** XPENG-AI published the X-AuT model repository on Hugging Face with a 14-layer safetensors checkpoint under cc-by-nc-4.0, based on Qwen/Qwen3-ASR-0.6B.
- **2026-09-14 — X-AuT Audio Encoder Compression Optimization for Speech LLMs.** XPeng published a compression method for automotive speech LLMs. It removes 4 of 18 encoder slots in Qwen3-ASR-0.6B and restores quality by distilling from a 1.7B model. This cuts parameters by 21% and automotive PPU latency by 21%, with a 2.5% error increase.
  - Compression runs progressively: 18 to 16 layers by dropping original layers {1, 18}, then 16 to 14 by dropping {5, 6}. Candidate layers are picked through short-budget behavioral recovery probes rather than single-layer rankings. The 21% parameter drop applies only to the audio tower, where the exact cut is 20.70%. The 14-layer model achieves 5.75% macro error against the 5.61% Full-18 baseline (+2.5% relative). The 16-layer operating point improves to 5.27% (−6.1% relative). — <https://xpeng-ai.github.io/x-aut/>
  - Comparing the 14-layer model to Full-18 on in-vehicle PPU versus NVIDIA H800: encoder latency −21.4% / −11.4%, end-to-end latency −4.7% / −2.6%, and peak memory −4.4% / −2.8%. These are descriptive single-run measurements from one model family, without repeated seeds or confidence intervals. — <https://xpeng-ai.github.io/x-aut/>
  - Cross-scale supervision changes the result: at the matched 16-layer Stage 1 checkpoint, the 1.7B teacher gives 5.55% macro error versus 8.45% for same-scale self-distillation. The teacher uses learned 2048-to-1024 projections and is discarded at inference. The repository notes this is a single-run comparison rather than causal proof. Removal touches only audio-tower Transformer blocks: ConvStem, Bridge, and ln_post stay intact, and language-model weights are not pruned. — <https://github.com/XPENG-AI/X-AuT>

## What changed

The release provides a 14-layer checkpoint with 20.70% fewer audio-tower parameters (186.376M to 147.794M). Macro error across ten public Chinese-English benchmarks is 5.75% against the 5.61% baseline (+2.5% relative). Encoder latency on the in-vehicle PPU falls 21.4%. End-to-end latency falls only 4.7% there, so the headline figure applies strictly to the encoder.

## How to use this

1. Download the complete 14-layer safetensors checkpoint with tokenizer and preprocessor from the XPENG-AI/X-AuT model page. Run infer_xaut.py from the repository to transcribe local audio.
  — <https://xpeng-ai.github.io/x-aut/>
2. Adapt the model using the minimal LoRA finetuning recipe and example manifests in the xaut-ft-simple folder. This is a Stage-2-style recipe, not the private training pipeline.
  — <https://github.com/XPENG-AI/X-AuT>

## Best practices

- Test candidate layer pairs directly with short recovery runs on a fixed development set. Pair interactions are non-additive, so single-layer rankings and assumptions about adjacent layers fail.
  — <https://github.com/XPENG-AI/X-AuT>
- Prune progressively (18 to 16 to 14) instead of in one step. Under the same recovery budget, progressive pruning gave 5.75% macro error against 6.73% for direct pruning.
  — <https://xpeng-ai.github.io/x-aut/>
- Monitor for deletion errors and early end-of-sequence predictions after removing layers. Dropping layers shifts decoder embeddings, so recovery training must target that interface.
  — <https://xpeng-ai.github.io/x-aut/>
- Check the license before deployment: the Hugging Face weights are tagged cc-by-nc-4.0, which forbids commercial use.
  — <https://huggingface.co/XPENG-AI/X-AuT>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Measurements come from single runs on one model family, without repeated seeds, confidence intervals, or latency variance.
- The public release provides only a Stage-2-style LoRA recipe; the private three-stage training and data pipeline remains unreleased.
- The project page and paper lack public release dates beyond the initial repository creation.

## Sources

| source | title | read |
|---|---|---|
| https://xpeng-ai.github.io/x-aut/ | X-AuT \| XPENG AI \(project page\) | 2026-09-14 |
| https://github.com/XPENG-AI/X-AuT | GitHub - XPENG-AI/X-AuT | 2026-09-14 |
| https://huggingface.co/XPENG-AI/X-AuT | XPENG-AI/X-AuT · Hugging Face | 2026-09-14 |

## Agent brief {#agent-brief}

- **Subject:** project:x-aut-compression-optimization, thread x-aut-compression-optimization, 2 dated events 2026-09-10 → 2026-09-14.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
