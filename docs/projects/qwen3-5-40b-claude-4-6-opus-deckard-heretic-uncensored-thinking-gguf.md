---
title: Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF — GGUF distribution
category: projects
date: 2026-03-25
tags: [gguf-distribution, project, qwen3-5-40b-claude-4-6-opus-deckard-heretic-uncensored-thinking-gguf, qwen3_5_40b_claude_4_6_opus_deckard_heretic_uncensored_thinking_gguf]
aliases: ["Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF"]
---

# Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF — GGUF distribution

**Development line:** `project:qwen3-5-40b-claude-4-6-opus-deckard-heretic-uncensored-thinking-gguf` · thread `gguf-distribution`  
**Last event:** 2026-03-25 · 1 dated since 2026-03-25 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF is a set of static GGUF quants of a 39B multimodal fine-tuned model for users of llama.cpp, Ollama and local OpenAI-compatible servers.

- Text and images with mmproj
- Local CLI and server execution
- Quant selection by memory and quality

Q4_K_M takes 24.0 GB, Q8_0 takes 41.6 GB, and separate mmproj files take 0.7–1.0 GB.

The release is a practical local distribution, but claims of being uncensored and fine-tune quality do not replace our own assessment of tasks and risks.

## Development line

- **2026-03-25 — Hugging Face reference recorded for the GGUF model line.** Files range from Q2_K (14.5 GB) to Q8_0 (41.6 GB), plus two multimodal-projector files. The card points directly to the original DavidAU repository and a separate i1/imatrix release.

## What changed

2026-03-25 — Static GGUF quants of the original 39B model appeared, ranging from Q2_K (14.5 GB) to Q8_0 (41.6 GB), plus two multimodal-projector files. The card points directly to the original DavidAU repository and a separate i1/imatrix release.

2026-03-25 — The quant index also records a separate mradermacher i1-GGUF release. This is not an update to the static GGUF, but a parallel weighted/imatrix build of the same source checkpoint.

## How to use this

As of 2026-03-25, practitioners can use the linked Hugging Face page as a lead for this GGUF model line, while independently verifying its files, provenance, licence, and runtime compatibility before use.

1. Pick a quant by available memory; the card suggests Q4_K_M for a first run, and marks Q4_K_S as a fast recommended option.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
2. Run the model through llama.cpp: `llama serve -hf mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF:Q4_K_M`; the server provides an OpenAI-compatible local endpoint.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
3. For Ollama use `ollama run hf.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF:Q4_K_M`; download a matching mmproj from the static repository when processing images.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>

## Best practices

- Do not select a quant by file size alone: the author notes the list is sorted by size, but IQ quants often beat non-IQ options at similar sizes.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
- For vision tasks, take the mmproj from the static GGUF repository; the i1/imatrix repository states its mmproj lives there.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF>
- Test the model against your own tasks and safety requirements before deployment: the card describes provenance and claimed traits, but provides no independent benchmark or behavioural guarantee.
  — <https://huggingface.co/DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Requested fields event_findings and new_events are absent from the returned response schema; facts from 2026-03-25 appear in what_changed.
- The exact initial publication date of the source DavidAU model and independent quality metrics remain unverified by the sources used.
- The card labels the model as vision capable and publishes an mmproj, but runtime compatibility with images depends on engine version and configuration.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF | mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF | 2026-09-05 |
| https://huggingface.co/DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking | DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking | 2026-09-05 |
| https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF | mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen3-5-40b-claude-4-6-opus-deckard-heretic-uncensored-thinking-gguf`, thread `gguf-distribution`, 1 dated events 2026-03-25 → 2026-03-25.
- **Practical note:** As of 2026-03-25, practitioners can use the linked Hugging Face page as a lead for this GGUF model line, while independently verifying its files, provenance, licence, and runtime compatibility before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
