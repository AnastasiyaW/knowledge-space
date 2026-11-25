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

Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF is a set of static GGUF quants of a 39B multimodal fine-tuned model for llama.cpp, Ollama, and local OpenAI-compatible servers.

- Text and image processing when paired with an mmproj file.
- Local CLI and local server execution.
- Quant selection based on available memory and quality.

Q4_K_M takes 24.0 GB, Q8_0 takes 41.6 GB, and standalone mmproj files take 0.7–1.0 GB.

We get a practical local release, but uncensored claims and fine-tune quality require separate testing against your own tasks and risks.

## Development line

- **2026-03-25 — Hugging Face reference recorded for the GGUF model line.** Files range from Q2_K (14.5 GB) to Q8_0 (41.6 GB), plus two multimodal-projector files; the model card links directly to the upstream DavidAU repository and a separate i1/imatrix variant.

## What changed

2026-03-25 — Static GGUF quants of the base 39B model are out: from Q2_K (14.5 GB) to Q8_0 (41.6 GB), plus two multimodal-projector files; the card points directly to the upstream DavidAU repository and a separate i1/imatrix variant.

2026-03-25 — The quant index also lists a separate mradermacher i1-GGUF release; this is a parallel weighted imatrix build of the same checkpoint rather than an update to the static GGUF line.

## How to use this

As of 2026-03-25, practitioners can use the linked Hugging Face page as a lead for this GGUF model line, while independently verifying its files, provenance, licence, and runtime compatibility before use.

1. Pick a quant by available memory; the card suggests Q4_K_M for an initial local run, and marks Q4_K_S as a fast recommended option.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
2. Run the model through llama.cpp: `llama serve -hf mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF:Q4_K_M`; the server provides an OpenAI-compatible local endpoint.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
3. For Ollama, run `ollama run hf.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF:Q4_K_M`; download a matching mmproj from the static repository to process images.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>

## Best practices

- Do not pick a quant by file size alone: the author notes the list is sorted by size, and IQ quants often beat non-IQ variants of similar size.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
- Pull mmproj from the static GGUF repository for vision tasks; the i1/imatrix repository notes its mmproj lives there.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF>
- Test the model against your own tasks and safety requirements before deployment: the card describes provenance and claimed traits, but provides no independent benchmark or behavioral guarantee.
  — <https://huggingface.co/DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The requested event_findings and new_events fields are absent from the response schema; facts belonging to 2026-03-25 appear in what_changed.
- The exact release date of the upstream DavidAU model and independent quality metrics remain unconfirmed by the cited sources.
- The model card calls it a vision model and provides mmproj, but runtime compatibility with images depends on runtime version and configuration.

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
