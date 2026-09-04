---
title: Llama 3.1
category: projects
date: 2024-07-23
tags: [llama-3-1, project]
aliases: ["Llama 3.1"]
---

# Llama 3.1

**Development line:** `project:llama-3-1` · thread `llama-3-1`  
**Last event:** 2024-07-23 · 1 dated since 2024-07-23 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Llama 3.1 — Meta’s static 2024 family for teams that need a downloadable, licensed alternative to a hosted text-generation API.

- 8B, 70B, and 405B pretrained and Instruct variants for text/code generation, multilingual chat, RAG, and tool-enabled systems.
- 128K context and eight supported languages.
- Text in/text out, December 2023 knowledge cutoff; 405B is a multi-GPU deployment problem.

## Development line

- **2024-07-23 — Official Llama 3.1 access resources became available.** On 2024-07-23, official Llama 3.1 resources opened paths to model downloads, Meta AI, an agentic-system repository, and a hosted chat model. This marked the line's practical availability to developers and users across those channels.

## What changed

- 2024-07-23 — Llama 3.1 released upgraded 8B and 70B models plus 405B, with 128K context, eight supported languages, tool-use support, and companion safety/system components.
- 2024-09-25 — Llama 3.2 added 1B/3B edge text models and 11B/90B vision models; Llama 3.1 remained text-only.
- 2024-12-06 — Llama 3.3 introduced a later 70B Instruct text model with 128K context.
- 2025-04-05 — Llama 4 Scout and Maverick introduced Meta’s newer native-multimodal mixture-of-experts Llama generation.

## How to use this

As of 2024-07-23, teams could evaluate Llama 3.1 through official download, chat, and developer channels; confirm the exact model variant and terms from official materials before deployment.

1. Confirm that text-only input/output, the 8B/70B/405B size range, and eight-language support fit the workload; choose an Instruct checkpoint for assistant chat.
  — <https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md>
2. Request gated access and accept the Llama 3.1 Community License before downloading model weights.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
3. Run a first local chat with Transformers 4.43+ using the official Instruct model ID and a text-generation pipeline or AutoModelForCausalLM.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
4. Send role-based messages through tokenizer.apply_chat_template before generation rather than assembling Llama control tokens yourself.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
5. Serve the checkpoint with vLLM and call /v1/chat/completions for an OpenAI-compatible local endpoint.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
6. Plan a node with 8×80GB H100 GPUs for 405B FP8; use multi-node inference for the unquantized 405B checkpoint.
  — <https://github.com/meta-llama/llama-cookbook/blob/main/getting-started/inference/local_inference/README.md>

## Best practices

- Use an Instruct model for assistant dialogue; keep the pretrained base model for adaptation or other text generation.
  — <https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md>
- Preserve the official chat template with apply_chat_template, including the generation prompt.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
- Follow the Llama 3.1 Community License as a release requirement: distributed materials and services have attribution obligations, and products above 700 million monthly active users require a separate Meta license.
  — <https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct-FP8>
- Safety-test and tune for the application, then deploy safeguards around the model and external tools; do not deploy the model alone.
  — <https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md>
- Do not budget 405B from its parameter label alone: separate FP8 single-node serving from unquantized multi-node serving.
  — <https://github.com/meta-llama/llama-cookbook/blob/main/getting-started/inference/local_inference/README.md>

## Superseded by this

- 2024-09-25 — Choosing Llama 3.1 for on-device text or image understanding is obsolete; Llama 3.2 introduced the 1B/3B edge-text and 11B/90B vision paths.
- 2024-12-06 — Comparing only Llama 3.1 70B or 405B for a new Meta 70B text service is obsolete; Llama 3.3 70B Instruct is the later 128K option.
- 2025-04-05 — Calling Llama 3.1 Meta’s newest Llama generation is obsolete; Llama 4 added native multimodality and mixture-of-experts models.

## Still unknown

- The source and X links yielded no retrievable text in this pass, so we use only their dates and URLs rather than unverified claims.
- The historical llama-agentic-system link redirects to ogx-ai/llama-stack-apps; that page lacks dated Meta provenance, so we do not treat it as current official Meta guidance.
- We found a same-day Chinese Hugging Face translation, but no separate primary Meta announcement; we make no China-specific availability or compatibility claims.
- We have no workload, hardware budget, target region, or license context, so we do not pick a specific Llama 3.1 size or later replacement.

## Sources

| source | title | read |
|---|---|---|
| https://ai.meta.com/blog/meta-llama-3-1/ | Introducing Llama 3.1: Our most capable models to date | 2026-09-04 |
| https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md | Llama 3.1 model card — meta-llama/llama-models | 2026-09-04 |
| https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct | meta-llama/Llama-3.1-8B-Instruct | 2026-09-04 |
| https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct-FP8 | meta-llama/Llama-3.1-405B-Instruct-FP8 | 2026-09-04 |
| https://github.com/meta-llama/llama-cookbook/blob/main/getting-started/inference/local_inference/README.md | Llama Cookbook — local inference guide | 2026-09-04 |
| https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/ | Llama 3.2: Revolutionizing edge AI and vision with open, customizable models | 2026-09-04 |
| https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/MODEL_CARD.md | Llama 3.3 model card — meta-llama/llama-models | 2026-09-04 |
| https://ai.meta.com/blog/llama-4-multimodal-intelligence/ | The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation | 2026-09-04 |
| https://github.com/meta-llama/llama-agentic-system | llama-agentic-system URL, currently redirected to ogx-ai/llama-stack-apps | 2026-09-04 |
| https://huggingface.co/blog/zh/llama31 | Llama 3.1：405B/70B/8B 模型的多语言与长上下文能力解析 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:llama-3-1`, thread `llama-3-1`, 1 dated events 2024-07-23 → 2024-07-23.
- **Practical note:** As of 2024-07-23, practitioners could evaluate Llama 3.1 through official download, chat, and developer-resource channels; confirm the exact model variant and applicable terms from the official materials before deployment.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
