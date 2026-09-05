---
title: Nemotron 3.5 Lightning
category: projects
date: 2026-08-12
tags: [nemotron-3-5-lightning, nvidia-nemotron, nvidia_nemotron, project]
aliases: ["Nemotron 3.5 Lightning"]
---

# Nemotron 3.5 Lightning

**Development line:** `project:nvidia-nemotron` · thread `nemotron-3-5-lightning`  
**Last event:** 2026-08-12 · 1 dated since 2026-08-12 · **Researched:** 2026-09-05 · confidence: high

## What it is

Nemotron 3.5 Lightning is a text hybrid MoE model with 30B total and 3B active parameters. It targets developers of agent systems, chat bots, and RAG.

- Reasoning with a thinking switch.
- Tool use.
- Code generation.
- Long context up to 1M tokens.
- Speculative decoding.
- NVFP4 and BF16 release checkpoints.

The NVFP4 checkpoint takes about 22 GB of memory; NVIDIA specifies running it on one DGX Spark or H100. This is an execution model for frequent agent calls, not a replacement for a larger model for complex planning.

## Development line

- **2026-08-12 — Nemotron 3.5 Lightning public model and playground resources surfaced.** NVIDIA released NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4, a commercially usable 30B/3B-active Mamba-2/MoE/attention hybrid with context up to 1M tokens. NVIDIA also presented BF16, NVFP4, DSpark/DFlash for speculative decoding, and routing through NeMo Switchyard. The primary model card dates the release to 2026-08-11, so the 2026-08-12 event reflects the distribution day rather than a separate model.

## What changed

2026-08-12: NVIDIA released NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4, a commercially usable 30B/3B-active Mamba-2/MoE/attention hybrid with context up to 1M tokens. The release includes BF16, NVFP4, DSpark/DFlash for speculative decoding, and routing through NeMo Switchyard. The primary model card dates the release to 2026-08-11, so the 2026-08-12 event reflects the distribution day rather than a separate model.

2026-08-17: NVIDIA published a breakdown of the QAD recipe for NVFP4. The checkpoint shrinks from about 66 GB in BF16 to 22 GB. This post documents the existing checkpoint and is not a new base model release.

## How to use this

From 2026-08-12, practitioners should treat Nemotron 3.5 Lightning as a line with public model artifacts, a hosted playground, and related Switchyard tooling; select the specific published model or deployment path from those resources rather than relying on an unverified repost.

1. Call the NVIDIA Build API for fast prototypes through an OpenAI-compatible client using model name `nvidia/nemotron-3.5-lightning-30b-a3b`. Set `enable_thinking` and cap the reasoning budget for the task.
  — <https://build.nvidia.com/nvidia/nemotron-3.5-lightning-30b-a3b>
2. Run the NVFP4 checkpoint through vLLM or SGLang for self-hosting. Use the returned `/v1/models` name in an OpenAI-compatible client.
  — <https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4>
3. Route high-frequency steps to Lightning in agent systems: tool calls, result checks, and formatting. Reserve complex planning for a stronger model.
  — <https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/>

## Best practices

- Measure the baseline NVFP4 or BF16 path on internal workloads first. Choose speculative decoding by concurrency: DSpark fits DGX Spark and low concurrency, while MTP fits medium and high concurrency.
  — <https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/>
- Set explicit routing rules for Lightning instead of using implicit fallbacks. Validate route quality and cost in Switchyard.
  — <https://github.com/NVIDIA-NeMo/Switchyard>
- Use NVFP4 under strict memory limits. NVIDIA designed the QAD recipe to recover quality after aggressive quantization, but verify it on target agent benchmarks.
  — <https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/>

## Superseded by this

- 2026-08-17: the official Lightning NVFP4 checkpoint is not simple post-training quantization. NVIDIA applies QAD distillation on top of PTQ.
- 2026-08-12: routine agent steps no longer require the same large reasoning model for every call. Strong models now handle planning, while Lightning handles execution.

## Still unknown

- Primary sources do not record the exact publication time for all five links on 2026-08-12. The model card lists a 2026-08-11 release date, so the one-day difference may reflect time zones or publication schedules.
- NVIDIA claims on speed and benchmarks do not replace testing on local hardware, server versions, concurrency, and agent harnesses.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 | NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 model card | 2026-09-05 |
| https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/ | NVIDIA Nemotron 3.5 Lightning Delivers Fast, Accurate Specialized Task Execution for Long-Running Agents | 2026-09-05 |
| https://build.nvidia.com/nvidia/nemotron-3.5-lightning-30b-a3b | nvidia/nemotron-3.5-lightning-30b-a3b on NVIDIA Build | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Switchyard | NVIDIA-NeMo/Switchyard | 2026-09-05 |
| https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/ | Developing Nemotron 3.5 Lightning NVFP4 with QAD Using NVIDIA Model Optimizer | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:nvidia-nemotron`, thread `nemotron-3-5-lightning`, 1 dated events 2026-08-12 → 2026-08-12.
- **Practical note:** From 2026-08-12, practitioners should treat Nemotron 3.5 Lightning as a line with public model artifacts, a hosted playground, and related Switchyard tooling; select the specific published model or deployment path from those resources rather than relying on an unverified repost.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
