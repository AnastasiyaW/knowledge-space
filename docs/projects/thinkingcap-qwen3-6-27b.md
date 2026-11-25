---
title: ThinkingCap-Qwen3.6-27B
category: projects
date: 2026-07-08
tags: [project, thinkingcap-qwen3-6-27b]
aliases: ["ThinkingCap-Qwen3.6-27B"]
---

# ThinkingCap-Qwen3.6-27B

**Development line:** `project:thinkingcap-qwen3-6-27b` · thread `thinkingcap-qwen3-6-27b`  
**Last event:** 2026-07-08 · 1 dated since 2026-07-08 · **Researched:** 2026-11-21 · confidence: high

## What it is

ThinkingCap-Qwen3.6-27B is an Apache-2.0 fine-tune of Qwen3.6-27B that aims to cut reasoning tokens while keeping accuracy close to the base.

- What: a "brevity" fine-tune, listed as an image-text-to-text model, trained on a curated set of problems across several domains.
- Users: people running a local 27B reasoning model with vLLM, SGLang, Transformers or llama.cpp GGUF builds. The card also links a hosted API.
- Key capability: on the card's out-of-domain macro average, accuracy is 80.7 versus 81.5 for the base, with 45.8 percent fewer thinking tokens. On GPQA-Diamond, accuracy is 83.8 versus 85.5 with 3,351 versus 10,777 thinking tokens.
- Limits: all results are self-reported by the developer (5 seeds, 95% CIs). HMMT (Nov 2025) drops from 88.0 to 84.7. Files are gated behind an access request.

As of 2026-11, the model page links ThinkingCap-Qwen3.8-27B as a newer version. This page does not evaluate it.

## Development line

- **2026-07-08 — ThinkingCap-Qwen3.6-27B repositories and deployment variants were linked.** On 2026-07-08, public repositories appeared for ThinkingCap-Qwen3.6-27B and several deployment formats. Linked formats include GGUF, NVFP4, and an int4 AutoRound variant. These links mark public availability of the model line and distribution options.

## What changed

- No dated version change is verified beyond the 2026-07-08 link. The model page (read 2026-11-21) links ThinkingCap-Qwen3.8-27B as newer; its date is not shown.

## How to use this

1. Accept the access conditions on the base model page and request access to the files.
  — <https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B>
2. Use the base card's sampling settings: temperature 1.0, top_p 0.95, top_k 20, min_p 0.0. The card says these match the base model.
  — <https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B>
3. For llama.cpp, run `llama-cli -hf bottlecapai/ThinkingCap-Qwen3.6-27B-GGUF:Q4_K_M`. The GGUF page calls Q4_K_M (15.7 GB) the recommended balance for most local setups. For vision, add the 0.9 GB mmproj file with `--mmproj`.
  — <https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B-GGUF>
4. For faster serving, add `--spec-type draft-mtp` on a recent llama.cpp build with MTP support.
  — <https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B-GGUF>
5. Check truncation on your own tasks. The card reports that think traces failing to close fall from 2.9 to 0.4 percent out-of-domain.
  — <https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B>

## Best practices

- Set token caps with headroom. Truncation (a think trace that never closes) is the card's main failure mode it measures.
  — <https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B>
- Re-measure accuracy in your own domain. The card's gains differ by domain: in-domain accuracy is 94.4 versus 95.4 for the base, with 57.7 percent fewer thinking tokens.
  — <https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B>
- Use the base model's recommended usage notes, which the card points to for context and sampling detail.
  — <https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B>

## Superseded by this

- Nothing verified as obsolete by this model. The page links ThinkingCap-Qwen3.8-27B as a newer version, which is not evaluated here.

## Still unknown

- Context length is not stated on the model card.
- The GGUF page shows no license text; the base card's metadata says apache-2.0.
- The NVFP4 and int4 AutoRound variants linked from the stub were not read. Their provenance and whether they match the ThinkingCap weights are unverified.
- All benchmarks come from the publisher's own harness (llama.cpp CUDA server, batch size 16, three seeds for the GGUF page).

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B | bottlecapai/ThinkingCap-Qwen3.6-27B — model card | 2026-11-21 |
| https://huggingface.co/bottlecapai/ThinkingCap-Qwen3.6-27B-GGUF | bottlecapai/ThinkingCap-Qwen3.6-27B-GGUF — GGUF model card | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:thinkingcap-qwen3-6-27b`, thread `thinkingcap-qwen3-6-27b`, 1 dated events 2026-07-08 → 2026-07-08.
- **Practical note:** Apache-2.0 brevity fine-tune of Qwen3.6-27B (gated). Use the base sampling settings and a token cap with headroom; the newer 3.8 variant is not evaluated here.
- **Confidence:** high for the cards' stated facts; benchmarks are self-reported. Dated supersedes above are the authority for what is obsolete.
