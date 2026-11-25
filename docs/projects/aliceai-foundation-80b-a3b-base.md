---
title: "Aliceai Foundation 80B A3B Base: aliceai-foundation-80b-a3b-base — Aliceai Foundation 80B A3B Base"
category: "projects"
date: 2026-09-29
tags: ["aliceai-foundation-80b-a3b-base", "project"]
aliases: ["Aliceai Foundation 80B A3B Base: aliceai-foundation-80b-a3b-base"]
---

# Aliceai Foundation 80B A3B Base: aliceai-foundation-80b-a3b-base — Aliceai Foundation 80B A3B Base

**Development line:** project:aliceai-foundation-80b-a3b-base · thread aliceai-foundation-80b-a3b-base  
**Last event:** 2026-09-29 · 7 dated since 2026-09-21 · **Researched:** 2026-11-25 · confidence: high

## What it is

AliceAI-Foundation-80B-A3B-Base is a pretrained hybrid MoE language model for researchers and developers who need an open foundation checkpoint.

- Russian and English support.
- Released evaluation assets.

80B total parameters, 3B activated per token, 262,144-token context. The model has no post-training or alignment, so it is not a ready chat assistant or direct production replacement.

Use it for controlled fine-tuning, continued training, or raw-completion research after task-specific evaluation.

## Development line

- **2026-09-21 — Yandex opens AliceAI-Foundation-80B-A3B-Base language model weights.** Yandex released weights for AliceAI-Foundation-80B-A3B-Base, a model trained from scratch. Benchmark scores beat DeepSeek-V4-Flash-Base and Nemotron-3-Super. The release fits Yandex's unified reasoning model \(ЕРМ\) strategy. A technical report and dataset updates came out alongside the weights.
- **2026-09-21 — Yandex opens AliceAI-Foundation-80B-A3B-Base language model weights.** Yandex published the AliceAI-Foundation-80B-A3B-Base model weights under an Apache 2.0 license. Yandex trained the model from scratch to outperform larger open models on benchmarks. The technical report details data pipelines, evaluation protocols, and scaling laws.
- **2026-09-21 — Yandex releases AliceAI-Foundation-80B-A3B-Base model.** Yandex released the AliceAI-Foundation-80B-A3B-Base model. The strategic shift toward training models from scratch directly affects Sber's GigaChat positioning in the government sector.
- **2026-09-21 — Yandex open-sources AliceAI-Foundation-80B-A3B-Base large language model.** Yandex open-sourced the AliceAI-Foundation-80B-A3B-Base model. The release provides Hugging Face access to weights, associated datasets \(WikiWebFacts, HardMultiQA\), and evaluation protocols.
- **2026-09-21 — Yandex releases AliceAI-Foundation-80B-A3B-Base model on Hugging Face.** Yandex released the AliceAI-Foundation-80B-A3B-Base model, framed against pre-training and architectures from European labs. Only the base version is available. SFT and RL require buying GPU hardware.
- **2026-09-21 — other reporting on this date.**
  - The official release defines the model as a pretrained checkpoint trained from scratch under Apache 2.0 for research and commercial work. It tests architectural choices for a future unified reasoning model. (2026-09-21) — <https://ir.yandex/press-releases?id=2026-09-21&year=2026>
  - The official release confirms Apache-2.0 licensing and states main pre-training is complete. The checkpoint serves as a base for downstream projects rather than a finished assistant product. (2026-09-21) — <https://ir.yandex/press-releases?id=2026-09-21&year=2026>
  - The upstream README specifies a hybrid MoE architecture with 80B total parameters, 3B activated per token, and up to 262,144 tokens of context. (2026-09-21) — <https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base/blob/main/README_en.md>
  - The official release notes public availability of WikiWebFacts, HardMultiQA, reference answers, and full evaluation protocols. The benchmarks evaluate Russian factual contexts. (2026-09-21) — <https://ir.yandex/press-releases?id=2026-09-21&year=2026>
  - Upstream documentation notes the checkpoint lacks post-training or alignment. It targets research, experiments, and further development. (2026-09-21) — <https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base>
- **2026-09-25 — Release of AliceAI-Foundation-80B-A3B-Base model and technical report.** Yandex AI published model weights for AliceAI-Foundation-80B-A3B-Base under an Apache 2.0 license. The report details the training pipeline, scaling laws experiments, MoE stabilization, and Muon optimizer improvements.
  - Upstream documentation records 512 routed experts, top-10 routing plus one shared expert, and a one-layer multi-token-prediction component. (2026-09-21) — <https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base/blob/main/README_en.md>
- **2026-09-29 — Yandex releases AliceAI-Foundation-80B-A3B-Base, a 80B parameter model trained from scratch.** Yandex published open weights for AliceAI-Foundation-80B-A3B-Base with 80B parameters, trained from scratch. The model has 3B active parameters per token and accepts fine-tuning immediately. Turing Post covered it in a weekly roundup, and DeepMind's Aamir Chadha noted the industry shift toward efficiency over scale.
  - The community MLX conversion is an unofficial experimental mixed-precision port. It preserves BF16 router weights, excludes MTP support, and is not instruction-tuned or production-ready. (2026-09-29) — <https://huggingface.co/Yamada114514/AliceAI-Foundation-80B-A3B-Base-MLX-4bit/blob/main/README.md?code=true>

## What changed

The project moved from an internal model effort to a public Apache-2.0 pretrained checkpoint. Yandex published technical documentation and reproducible Russian factual benchmarks. Community MLX and GGUF conversions allow local testing, but remain separate third-party artifacts that leave the upstream base-model status unchanged.

## How to use this

1. Read the model card and upstream README to select an integration path compatible with a base model rather than a chat template.
  — <https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base>
2. For Transformers, install the documented reference stack, then load tokenizer and causal-LM weights with remote code enabled, BF16 precision, and an automatic device map.
  — <https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base>
3. For serving, use a supported vLLM or SGLang setup and send completion requests. Test output behavior on target prompts before attaching a user-facing interface.
  — <https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base>
4. For Apple-silicon experiments, download the separate MLX conversion into an isolated environment, inspect custom code, and test its bounded inference example first.
  — <https://huggingface.co/Yamada114514/AliceAI-Foundation-80B-A3B-Base-MLX-4bit/blob/main/README.md?code=true>

## Best practices

- Treat output as raw base-model completions: add post-training and behavioral controls for the target task, then test them before production use.
  — <https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base>
- Use the released WikiWebFacts and HardMultiQA protocols as reproducible Russian factual-evaluation inputs, but run independent evaluation for the target domain.
  — <https://ir.yandex/press-releases?id=2026-09-21&year=2026>
- Pin community conversion revisions apart from upstream weights. The MLX conversion runs local custom model code and omits MTP support.
  — <https://huggingface.co/Yamada114514/AliceAI-Foundation-80B-A3B-Base-MLX-4bit/blob/main/README.md?code=true>

## What practitioners say

- A LocalLLaMA discussion noted that the release is a custom architecture rather than a Qwen fine-tune, but reported no llama.cpp support at the time. (2026-09-21)
  — <https://www.reddit.com/r/LocalLLaMA/comments/1wmmnrt/yandexaliceaifoundation80ba3bbase/>
- A Chinese technical review found the base checkpoint unsuitable for direct chat use and recommended checking tokenizer and runtime fit for Chinese workloads. (2026-09-24)
  — <https://blog.mushroom.cv/blog/yandex-aliceai-foundation-80b-a3b-base-moe-teardown/>
- The author of the MLX conversion describes it as experimental, with limited local validation rather than a comprehensive benchmark. (2026-09-29)
  — <https://huggingface.co/Yamada114514/AliceAI-Foundation-80B-A3B-Base-MLX-4bit/blob/main/README.md?code=true>

## Superseded by this

- Guidance to use the released upstream checkpoint as a ready instruction-following assistant is obsolete. Upstream model documentation states it is pretrained and has no post-training or alignment.
  — <https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base>

## Still unknown

- Records live-0c6cdf5c3b07 and live-4cdfc9dd45a4 refer to the same release date and event; public research did not establish that they are distinct developments.
- Benchmark comparisons are vendor-run evaluations. They confirm that Yandex reported the results, not an independent performance conclusion.
- No official post-release instruction-tuned AliceAI-Foundation-80B-A3B derivative was verified in the sources used.

## Sources

| source | title | read |
|---|---|---|
| https://ir.yandex/press-releases?id=2026-09-21&year=2026 | Yandex Open-Sources New AI Model Trained from Scratch | 2026-11-25 |
| https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base | yandex/AliceAI-Foundation-80B-A3B-Base | 2026-11-25 |
| https://huggingface.co/yandex/AliceAI-Foundation-80B-A3B-Base/blob/main/README_en.md | README\_en.md — yandex/AliceAI-Foundation-80B-A3B-Base | 2026-11-25 |
| https://huggingface.co/Yamada114514/AliceAI-Foundation-80B-A3B-Base-MLX-4bit/blob/main/README.md?code=true | README.md — Yamada114514/AliceAI-Foundation-80B-A3B-Base-MLX-4bit | 2026-11-25 |
| https://www.reddit.com/r/LocalLLaMA/comments/1wmmnrt/yandexaliceaifoundation80ba3bbase/ | yandex/AliceAI-Foundation-80B-A3B-Base: Russian-developed competitor to Qwen 35B and DeepSeek V4 Flash | 2026-11-25 |
| https://blog.mushroom.cv/blog/yandex-aliceai-foundation-80b-a3b-base-moe-teardown/ | Yandex 开源 AliceAI-Foundation-80B-A3B 基座模型：Apache-2.0 属实，俄语强，中文分词比 Qwen 多耗 58% | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:aliceai-foundation-80b-a3b-base, thread aliceai-foundation-80b-a3b-base, 7 dated events 2026-09-21 → 2026-09-29.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. The dated supersessions above identify obsolete guidance.
