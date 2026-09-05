---
title: Qwopus3.6-27B-Coder-MTP
category: projects
date: 2026-06-18
tags: [project, qwopus3-6-27b-coder-mtp, qwopus3-6-27b-coder-mtp-development, qwopus3_6]
aliases: ["Qwopus3.6-27B-Coder-MTP"]
---

# Qwopus3.6-27B-Coder-MTP

**Development line:** `project:qwopus3-6-27b-coder-mtp` · thread `qwopus3-6-27b-coder-mtp-development`  
**Last event:** 2026-06-18 · 1 dated since 2026-06-18 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Qwopus3.6-27B-Coder-MTP is a Qwopus3.6-27B-v2 coding fine-tune with MTP draft heads for local repository work.

- Code generation for repositories.
- Debugging and patching code.
- Structured tool calls.

Available GGUF quants range from 13.5 GB Q3_K_M to 29 GB Q8_0. The community-reported SWE-bench score is 335/500 in a Q5_K_M thinking-off run, with other suites pending. We use it as an experimental local coding model, not as an independently validated production authority.

## Development line

- **2026-06-18 — Qwopus3.6-27B-Coder-MTP GGUF artifact linked.** We linked Qwopus3.6-27B-Coder-MTP-GGUF, its Qwopus3.6-27B-v2 base, and the Qwen MTP-to-GGUF conversion workflow as one local speculative-decoding path.

## What changed

2026-06-18: Qwopus3.6-27B-Coder-MTP-GGUF, its Qwopus3.6-27B-v2 base, and the Qwen MTP-to-GGUF conversion workflow were linked as one local speculative-decoding path.

## How to use this

From 2026-06-18, treat the linked GGUF artifact as a candidate Coder-MTP deployment format. Verify provenance, runtime compatibility, licence, and performance against the linked v2 model before use.

1. Choose a GGUF quantization to fit storage and memory. The repository lists Q3_K_M through Q8_0 builds.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/tree/main>
2. Run the GGUF in a llama.cpp-compatible local application. The model card names llama.cpp, Ollama and LM Studio as compatible targets.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF>
3. Keep tool definitions and the system prompt aligned with the training format for agents. Handle text inside <think> tags in the client.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md>

## Best practices

- Treat the reported 67.0% SWE-bench score as a single setup, not a cross-harness ranking. The card marks the release experimental and leaves other suites pending.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md>
- Run the preflight before downloading weights when creating or repackaging an MTP GGUF. A source/target configuration mismatch or insufficient disk blocks the build.
  — <https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md>
- Smoke-test the GGUF before upload or deployment. Use a matching MTP-head source model rather than assuming heads transfer across variants.
  — <https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md>

## Superseded by this

- 2026-07-09: a super-squashed GGUF cleanup commit replaced the prior granular repository history. It shows no new model capability.

## Still unknown

- No dated primary source proves the benchmark, throughput, or MTP speed claims held on 2026-06-18. We do not attach those claims to that event.
- Hugging Face metadata labels the GGUF as image-text-to-text, Transformers and a 0.5B CLIP architecture, but the README describes a 27B coder GGUF. This conflict makes the Transformers, vLLM and image examples unverified for deployment.
- No independent benchmark reproduction, compatibility matrix, or release changelog exists for the 2026-06-18 release point.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF | Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF model card | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md | Qwopus3.6-27B-Coder-MTP-GGUF README | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/tree/main | Qwopus3.6-27B-Coder-MTP-GGUF file tree | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-v2 | Jackrong/Qwopus3.6-27B-v2 model card | 2026-09-05 |
| https://github.com/R6410418/Jackrong-llm-finetuning-guide/tree/main/qwen-mtp-gguf | Qwen MTP GGUF Conversion Skill repository directory | 2026-09-05 |
| https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md | Qwen MTP GGUF Conversion Skill README | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/commits/main | Qwopus3.6-27B-Coder-MTP-GGUF commit history | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwopus3-6-27b-coder-mtp`, thread `qwopus3-6-27b-coder-mtp-development`, 1 dated events 2026-06-18 → 2026-06-18.
- **Practical note:** From 2026-06-18, treat the linked GGUF artifact as a candidate Coder-MTP deployment format. Verify provenance, runtime compatibility, licence, and performance against the linked v2 model before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.