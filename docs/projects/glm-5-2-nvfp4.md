---
title: GLM-5.2-NVFP4
category: projects
date: 2026-06-26
tags: [glm-5-2-nvfp4, project]
aliases: ["GLM-5.2-NVFP4"]
---

# GLM-5.2-NVFP4

**Development line:** `project:glm-5-2-nvfp4` · thread `glm-5-2-nvfp4`  
**Last event:** 2026-06-26 · 1 dated since 2026-06-26 · **Researched:** 2026-09-06 · confidence: high

## What it is

GLM-5.2-NVFP4 is NVIDIA Model Optimizer’s NVFP4 checkpoint of Z.AI GLM-5.2 for self-hosting agents, chatbots, RAG, coding, and reasoning.

- Sparse-MoE text generation and reasoning.
- Coding and long-context requests.
- Tool calling through the supplied SGLang and vLLM parser settings.

753B total parameters, 40B active, and up to 1M context on Blackwell and Linux.
Serve it on Blackwell after workload validation; this evidence does not establish a general local, non-NVIDIA, or managed-inference route.

## Development line

- **2026-06-26 — GLM-5.2-NVFP4 linked to NVIDIA's Hugging Face model page.** On 2026-06-26, the GLM-5.2-NVFP4 development line linked to a Hugging Face model page under NVIDIA's account. This is a material reference point for the project's public distribution trail, although the dated link alone does not establish a release date, model revision, or technical specifications.

## What changed

- 2026-06-26 — GLM-5.2-NVFP4 was documented as an NVFP4 1.0 Model Optimizer checkpoint of Z.AI GLM-5.2; the linked card is dated 2026-06-25.
- 2026-07-09 — NVIDIA NGC added `nim-aec724e-nvfp4`, a 432.95 GB NIM staging artifact; its FP8 description creates a package-identity caveat.
- 2026-07-20 — NVIDIA Dynamo recorded a GLM-5.2 dev-only SGLang runtime with un-upstreamed stability, configuration-parsing, and model-support patches.
- 2026-08-14 — NVIDIA Dynamo v1.4.0 added aggregated and disaggregated GLM-5.2 SGLang recipes for B200 NVFP4 and H200 FP8 deployments.

## How to use this

1. Confirm a Blackwell/Linux deployment target. The published checkpoint is tested on B200/B300 and lists SGLang and vLLM as supported engines.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
2. For direct serving, start from the official SGLang or vLLM configuration: SGLang needs `transformers>=5.3.0` and `modelopt_fp4`; the vLLM example uses `vllm/vllm-openai:v0.23.0`, tensor parallelism 8, expert parallelism, the GLM parsers, and an FP8 KV cache.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
3. For a Dynamo cluster, select the B200 NVFP4 target for this checkpoint, provision the shared model cache and Hugging Face token, deploy the matching aggregated or disaggregated recipe, then run its OpenAI-compatible smoke test.
  — <https://docs.nvidia.com/dynamo/dev/recipes/glm-5-2>
4. Validate accuracy, safety, and system behavior on use-case-specific data before production use.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>

## Best practices

- Treat the supplied runtime versions and parser flags as the starting contract rather than a generic GLM-5.2 launch command.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
- For NVIDIA Dynamo, do not substitute a stock SGLang image for the documented GLM-5.2 dev-only image while its required patches remain outside a stable release.
  — <https://docs.nvidia.com/dynamo/v1.4.2/reference/model-early-access-builds>
- Plan capacity against the deployment recipe, not the 1M checkpoint limit: the documented B200 NVFP4 path supports up to 500K context with HiCache CPU offload; the H200 FP8 path supports up to 250K.
  — <https://docs.nvidia.com/dynamo/dev/recipes/glm-5-2>
- Do not infer full-model quantization: NVIDIA says only linear operators within MoE expert transformer blocks are NVFP4-quantized, while the shared expert remains unquantized.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
- Before using the NIM artifact, verify its manifest and precision rather than relying on the catalog label alone.
  — <https://catalog.ngc.nvidia.com/orgs/nim/zai-org/models/glm-52/nim-aec724e-nvfp4>

## Superseded by this

- 2026-07-20 — For the NVIDIA Dynamo SGLang route, generic stable-runtime guidance is superseded by the documented GLM-5.2 dev-only image until its required patches are available in a stable SGLang release.

## Still unknown

- NVIDIA NGC labels `nim-aec724e-nvfp4` as NVFP4 but describes the staging model as FP8; its public page does not resolve the artifact’s exact precision contract.
- The Hugging Face UI shows 381B parameters while the model card reports 753B total and 40B active; the page does not explain the difference, so the UI number should not be used to derive memory requirements.
- The card’s 1M context declaration is not an end-to-end deployment guarantee: the current Dynamo recipes document 500K on B200 and 250K on H200.
- No Simplified-Chinese primary source specific to NVIDIA GLM-5.2-NVFP4 was retrieved; Chinese-language maintenance or deployment guidance remains unverified.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/nvidia/GLM-5.2-NVFP4 | nvidia/GLM-5.2-NVFP4 · Hugging Face | 2026-09-06 |
| https://catalog.ngc.nvidia.com/orgs/nim/zai-org/models/glm-52/nim-aec724e-nvfp4 | zai-org GLM-5.2 | NVIDIA NGC | 2026-09-06 |
| https://docs.nvidia.com/dynamo/v1.4.2/reference/model-early-access-builds | Model Early Access Builds | NVIDIA Dynamo Documentation | 2026-09-06 |
| https://docs.nvidia.com/dynamo/dev/reference/releases/v1-4-0 | Dynamo v1.4.0 | NVIDIA Dynamo Documentation | 2026-09-06 |
| https://docs.nvidia.com/dynamo/dev/recipes/glm-5-2 | GLM-5.3/5.2 | NVIDIA Dynamo Documentation | 2026-09-06 |