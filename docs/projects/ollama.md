---
title: Ollama — Product development
category: projects
date: 2026-01-22
tags: [ollama, product-development, project]
aliases: ["Ollama"]
---

# Ollama — Product development

**Development line:** `project:ollama` · thread `product-development`  
**Last event:** 2026-01-22 · 2 dated since 2025-05-19 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Ollama is a local runtime for developers running language, vision, and embedding models on their own hardware or through a compatible API.

- Model runner: downloads models and provides an interactive CLI, an HTTP API, and Python and JavaScript libraries.
- Vision processor: handles images alongside text prompts.

Speed, context size, and concurrency depend on available RAM and VRAM.

A practical alternative to cloud inference for local development and controlled data placement.

## Development line

- **2025-05-19 — Ollama published an update about multimodal models.** On 2025-05-19, Ollama linked to its official blog page for multimodal models and to its download page without details on specific models or hardware requirements.
- **2026-01-22 — Ollama shared a software-release update.** On 2026-01-22, Ollama directed users to the GitHub releases page without naming the version or change list.

## What changed

- 2025-05-19 — Ollama moved vision models to a new multimodal engine and added support for Llama 4, Gemma 3, Qwen 2.5 VL, and Mistral Small 3.1.
- 2026-01-22 — A link to GitHub Releases confirms the release channel, but the URL omits a version tag, so the release contents cannot be reconstructed reliably.

## How to use this

As of 2025-05-19, assess the official multimodal workflow when choosing local models. As of 2026-01-22, check the project's GitHub release notes before upgrading.

1. Install Ollama on macOS, Windows, or Linux.
  — <https://docs.ollama.com/quickstart>
2. Run a model in the terminal, such as `ollama run gemma4`, to test the first session.
  — <https://docs.ollama.com/quickstart>
3. Send requests from applications to the local API at `http://localhost:11434/api`, or use the official Python and JavaScript libraries.
  — <https://docs.ollama.com/api/introduction>
4. Pass an image alongside text in the CLI or in the `images` field of the API request for vision tasks.
  — <https://docs.ollama.com/capabilities/vision>

## Best practices

- Check model placement with `ollama ps` to verify whether it runs on GPU, CPU, or in mixed mode.
  — <https://docs.ollama.com/faq>
- Match `OLLAMA_CONTEXT_LENGTH` and concurrency to available memory: consumption grows with parallel requests multiplied by context size.
  — <https://docs.ollama.com/faq>
- Keep the service on the default loopback interface; change `OLLAMA_HOST` deliberately and use a reverse proxy when exposing it.
  — <https://docs.ollama.com/faq>
- Disable cloud features with `OLLAMA_NO_CLOUD=1` or `disable_ollama_cloud` for an entirely local setup.
  — <https://docs.ollama.com/faq>

## Superseded by this

- 2025-05-15 — The older integration built on shared multimodal code on llama.cpp was replaced by isolated model implementations in the new engine.
- 2026-01-20 — Image generation restricted to macOS was marked experimental; Windows and Linux were not supported yet.

## Still unknown

- The GitHub Releases link in the 2026-01-22 event points to a mutable release feed without a tag, so we cannot tie a specific version or changelog to that date.
- Current documentation includes cloud models, but the 2 dated links do not show whether cloud execution was part of the original announcement.

## Sources

| source | title | read |
|---|---|---|
| https://ollama.com/blog/multimodal-models | Ollama's new engine for multimodal models | 2026-09-05 |
| https://ollama.com/download | Download Ollama | 2026-09-05 |
| https://github.com/ollama/ollama/releases | Releases · ollama/ollama | 2026-09-05 |
| https://github.com/ollama/ollama/releases/tag/v0.14.3 | Release v0.14.3 · ollama/ollama | 2026-09-05 |
| https://ollama.com/blog/image-generation | Image generation (experimental) | 2026-09-05 |
| https://docs.ollama.com/quickstart | Quickstart | 2026-09-05 |
| https://docs.ollama.com/api/introduction | Introduction - Ollama API | 2026-09-05 |
| https://docs.ollama.com/capabilities/vision | Vision | 2026-09-05 |
| https://docs.ollama.com/faq | FAQ | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ollama`, thread `product-development`, 2 dated events 2025-05-19 → 2026-01-22.
- **Practical note:** As of 2025-05-19, assess Ollama's official multimodal workflow when selecting local models; as of 2026-01-22, review the project's GitHub release notes before upgrading.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
