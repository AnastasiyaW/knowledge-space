---
title: Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF — Model publication
category: projects
date: 2026-03-24
tags: [model-publication, project, qwen3-5-27b-claude-4-6-opus-reasoning-distilled-gguf, qwen3_5_27b_claude_4_6_opus_reasoning_distilled_gguf]
aliases: ["Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF"]
---

# Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF — Model publication

**Development line:** `project:qwen3-5-27b-claude-4-6-opus-reasoning-distilled-gguf` · thread `model-publication`  
**Last event:** 2026-03-24 · 1 dated since 2026-03-24 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF is a user-published GGUF build of Qwen3.5-27B for local analysis, code, and reasoning tasks. The verified files page lists Q3_K_M at 13.3 GB, Q4_K_M at 16.5 GB, and Q8_0 at 28.6 GB. The model card claims SFT+LoRA tuning on Claude Opus 4.6 reasoning trajectories; Anthropic's verified announcement contains no such origin. The 16.5 GB figure is the Q4_K_M file size, not a verified runtime memory measurement. This is a third-party artifact, not a local version of Claude Opus 4.6.

## Development line

- **2026-03-24 — Hugging Face repository appeared for Qwen3.5-27B Claude 4.6 Opus Reasoning Distilled GGUF.** On 2026-03-24, a public repository named Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF appeared on Hugging Face. The dated link shows an artifact was available under that name. Public details do not confirm its contents, origin, or release details.

## What changed

2026-02-24 — Qwen released the official Qwen3.5-27B base model listed on the GGUF card. 2026-03-24 — Community GGUF files became available; the public card does not confirm this date as a release or weight update.

## How to use this

1. Check the target GGUF: the verified files page lists Q3_K_M at 13.3 GB, Q4_K_M at 16.5 GB, and Q8_0 at 28.6 GB; pick one file matching available disk and memory.
  — <https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF/tree/main>
2. Run `hf download <repo> <exact-file> --dry-run` before fetching files; then download the file with the full commit SHA pinned in `--revision`.
  — <https://huggingface.co/docs/huggingface_hub/en/guides/download>
3. Start the chosen quantization with `llama serve -hf Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF:Q4_K_M`; the card also lists `llama cli` for one-off runs.
  — <https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF>
4. Check `GET /health` before connecting an agent; HTTP 200 with status `ok` means the model is loaded. Then check the chat template through `/props` on the pinned revision.
  — <https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md>

## Best practices

- Pin the revision with the full commit SHA: Hugging Face requires the full hash to download a specific version; run a dry run first to avoid pulling the whole repository by mistake.
  — <https://huggingface.co/docs/huggingface_hub/en/guides/download>
- Specify the quantization explicitly (`:Q4_K_M`) or pass the exact file with `-hff`: Q4_K_M is the default for `-hf`, and without it the runtime picks the first file in the repository.
  — <https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md>
- Leave Jinja and metadata chat templates enabled on initial launch; override the template only after checking actual model properties through `/props`.
  — <https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md>
- Treat claims about quality, autonomy, VRAM, and training data as author claims: the card calls the build a preview while warning about hallucinations and incompatibilities.
  — <https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF/raw/main/README.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The public model card does not show 2026-03-24 as the creation, release, or update date; it only contains a screenshot with that date.
- The card mentions "Update (April 5)" without a year or commit timestamp, so we do not list it as a dated event.
- Independent primary sources have not confirmed the origin of the claimed Claude Opus 4.6 reasoning data, its licensing, or the stated benchmark, VRAM, and speed figures.
- The card calls the final model text-only, but the repository has a vision/multimodal tag and includes `mmproj-F32.gguf`; test image support locally on the pinned revision with a smoke run.
- Tests for compatibility with specific agents, tool calling, and output quality across quantizations have not been run.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF | Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF · Hugging Face | 2026-09-06 |
| https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF/raw/main/README.md | README.md — Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF | 2026-09-06 |
| https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF/tree/main | Files at main — Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF | 2026-09-06 |
| https://github.com/QwenLM/Qwen3.8/blob/main/README.md | Qwen3.8/README.md — QwenLM/Qwen3.8 | 2026-09-06 |
| https://www.anthropic.com/news/claude-opus-4-6 | Introducing Claude Opus 4.6 — Anthropic | 2026-09-06 |
| https://huggingface.co/docs/huggingface_hub/en/guides/download | Download files from the Hub — Hugging Face | 2026-09-06 |
| https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | LLaMA.cpp HTTP Server — ggml-org/llama.cpp | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen3-5-27b-claude-4-6-opus-reasoning-distilled-gguf`, thread `model-publication`, 1 dated events 2026-03-24 → 2026-03-24.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
