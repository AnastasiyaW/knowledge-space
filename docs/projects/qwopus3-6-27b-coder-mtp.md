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

- Code generation for local repositories.
- Debugging and patching across files.
- Structured tool calls for local agents.

Available GGUF quants range from 13.5 GB Q3_K_M to 29 GB Q8_0. The stated SWE-bench result is 335/500 in a Q5_K_M thinking-off run, with other suites pending. We use it as an experimental local coding model, not as an independently validated production authority.

## Development line

- **2026-06-18 — Qwopus3.6-27B-Coder-MTP GGUF artifact linked.** Qwopus3.6-27B-Coder-MTP-GGUF, its Qwopus3.6-27B-v2 base, and the Qwen MTP-to-GGUF conversion workflow were linked as one local speculative-decoding path.

## What changed

2026-06-18: Qwopus3.6-27B-Coder-MTP-GGUF, its Qwopus3.6-27B-v2 base, and the Qwen MTP-to-GGUF conversion workflow were linked as one local speculative-decoding path.

## How to use this

We treat the linked GGUF artifact from 2026-06-18 as a candidate Coder-MTP deployment format. Verify provenance, runtime compatibility, licence, and performance against the linked v2 model before use.

1. Choose a GGUF quantization for available storage and memory; the repository lists Q3_K_M through Q8_0 builds.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/tree/main>
2. Run the GGUF with a llama.cpp-compatible local application; the model card names llama.cpp, Ollama and LM Studio as compatible targets.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF>
3. For agent use, keep tool definitions and the system prompt consistent with the training format, and handle text inside <think> tags in the client.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md>

## Best practices

- Treat the reported 67.0% SWE-bench result as a single disclosed setup, not a cross-harness ranking; the card labels the release experimental and leaves other suites pending.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md>
- When creating or repackaging an MTP GGUF, run the preflight before downloading weights so configuration mismatches or full disks do not block the run.
  — <https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md>
- Smoke-test the GGUF before upload or deployment, and use a matching MTP-head source model rather than assuming heads transfer across variants.
  — <https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md>

## Superseded by this

- 2026-07-09: a super-squashed GGUF cleanup commit replaced the prior granular repository history; this does not indicate a new model capability.

## Still unknown

- No dated primary source proves the model card's benchmark, throughput, or MTP speed claims were true on 2026-06-18; we do not attach those claims to that event.
- Hugging Face metadata labels the GGUF as image-text-to-text, Transformers, and a 0.5B CLIP architecture while the README describes a 27B coder GGUF; this conflict makes generic Transformers, vLLM, and image examples unverified for deployment.
- No independent benchmark reproduction, compatibility matrix, or release changelog exists for the 2026-06-18 release.

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
- **Practical note:** We treat the linked GGUF artifact from 2026-06-18 as a candidate Coder-MTP deployment format; verify provenance, runtime compatibility, licence, and performance against the linked v2 model before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
