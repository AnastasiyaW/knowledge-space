---
title: MiniMax
category: organizations
date: 2025-12-27
tags: [minimax, minimax-models-and-products, minimax_models, organization]
aliases: ["MiniMax"]
---

# MiniMax

**Development line:** `organization:minimax` · thread `minimax-models-and-products`  
**Last event:** 2025-12-27 · 3 dated since 2025-06-18 · **Researched:** 2026-09-05 · confidence: medium

## What it is

MiniMax provides AI models and services. Developers get an Anthropic-SDK-compatible API alongside video and speech services; creators get separate Hailuo and Audio products.

- M3: language, tool use, image/video input, and a 1M-token context window.
- H3: text, image, first/last-frame, and multimodal-reference video generation.
- Speech 2.8: synthesis, cloning, and voice design.

## Development line

- **2025-06-18 — MiniMax surfaced MiniMax-M1 model resources.** On 2025-06-18, MiniMax linked a Hugging Face collection for MiniMax-M1 and a GitHub repository for the model. The same dated link set pointed to Hailuo Create and MiniMax Agent, placing the model alongside video and agent surfaces.
- **2025-06-22 — MiniMax publicly surfaced its Audio product.** Speech remains a distinct API line with synthesis, cloning, and voice design; music access has changed materially.
- **2025-12-27 — MiniMax surfaced M2.1 through hosted and local access routes.** On 2025-12-27, MiniMax linked its MiniMax-M2.1 news page and Hugging Face model repository. The dated resource set also pointed to MiniMax Agent, an Anthropic-compatible text API reference, OpenRouter, and Ollama, listing multiple access routes for M2.1.

## What changed

2024-10-10 — A MiniMax event has no retained text or URL, so it makes no source-backed historical claim. MiniMax's closest primary baseline is Video-01, released 2024-08-31 with text-to-video and image-to-video at 720p/25 fps for up to six seconds. This is context, not confirmation of the 10 October change.

2025-06-18 — MiniMax M1 and Hailuo 02 entered the record. M1 was an open-weight hybrid-attention reasoning model with 456B total parameters, 45.9B active parameters, and 1M context. Hailuo 02 added native 1080p video options.

2025-06-20 — Hailuo Video Agent entered beta with prebuilt video templates as Stage One. Later autonomous stages were a roadmap, not verified capabilities.

2025-06-22 — A MiniMax Audio endpoint appeared, but the page lists no dated release details. Speech remains a separate API line with synthesis, cloning, and voice design; music access has changed materially.

2025-12-27 — M2.1 entered the record as an open-weight, agent-oriented M2 model for multilingual coding, tool use, instruction following, and long-horizon tasks. MiniMax's release note is dated 2025-12-23, while its model release notes state 2025-12-22.

Found today — M3 released on 2026-06-01 as the current 1M-context language model. H3 open-sourced on 2026-08-03 as the multimodal video line. Music API access changed on 2026-08-20 for new users.

## How to use this

As of 2025-12-27, evaluate MiniMax models by each listed route—MiniMax Agent, the text API, OpenRouter, or Ollama—rather than assuming one interface covers every product.

1. Choose the current surface first: M3 for language, coding, tool use, or multimodal API work; H3 for video; Speech 2.8 for voice. Do not start from historical M2.1 or Hailuo names.
  — <https://platform.minimax.io/docs/guides/models-intro>
2. Create a pay-as-you-go API key on the MiniMax Platform to access language, video, speech, and image models.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
3. For language integrations, set `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic` in the Anthropic SDK, use the MiniMax API key, and call `MiniMax-M3`.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
4. For tool calling, append the full assistant response—thinking, text, and tool-use blocks—to history before sending tool results and the next turn.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
5. For H3 video, create an asynchronous task, save the `task_id`, query status, and fetch the output URL after success. Pick inputs and duration within the 4–15-second range.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
6. For speech, use synchronous T2A for short interactive audio and asynchronous synthesis for long text. Do not start a new Music API integration; use MiniMax Audio or the open Music 3 model instead.
  — <https://platform.minimax.io/docs/api-reference/api-overview>

## Best practices

- Treat Anthropic compatibility as a documented subset: the API ignores `top_k`, stop sequences, MCP servers, context management, and containers rather than emulating them.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Use M3's adaptive thinking for complex reasoning and disable it for low latency; keep thinking blocks unchanged across tool-use turns.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Use M3—not M2.x—for image or video input, and estimate tokens before sending large multimodal requests.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Treat M2.1, Hailuo 02/2.3, and older Speech models as legacy, requiring an explicit compatibility or migration decision.
  — <https://platform.minimax.io/docs/guides/models-intro>
- Treat video generation as a job workflow instead of a synchronous call: keep task IDs, poll status, and handle cancellation or deletion cleanly.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
- If a deployment requires local M2.1 weights, serve via SGLang or vLLM and review the Modified MIT license before shipping.
  — <https://huggingface.co/MiniMaxAI/MiniMax-M2.1>
- Check account eligibility before building music workflows: new users cannot access paid Music APIs, and free endpoints are discontinued.
  — <https://platform.minimax.io/docs/api-reference/api-overview>

## Superseded by this

- 2024-08-31 / 2024-10-10 — Video-01 limits (720p, 25 fps, up to six seconds) are legacy. H3 covers multimodal inputs, 4–15-second outputs, 24 fps, and up to 2K.
- 2025-06-18 — M1 as default hosted 1M-context model is historical. MiniMax documents M3 as the current 1M-context language model; M1 is archival or self-hosted open weights.
- 2025-06-20 — Hailuo Video Agent Stage One beta and the Stage Two/Three roadmap are historical. Check current features against H3 and API docs rather than assuming the roadmap shipped.
- 2025-12-27 — Choosing M2.1 as a flagship model is obsolete. It remains API-compatible and downloadable, but MiniMax classifies it under Legacy Models.
- 2025-06-22 — Starting a Music API workflow from older MiniMax Audio guidance is obsolete: from 2026-08-20, paid Music APIs are closed to new users and free endpoints are discontinued.

## Still unknown

- The 2024-10-10 event has no retained link or text. The 2024-08-31 Video-01 page is context, not proof of the October change.
- The links `https://hailuoai.video/create`, `https://agent.minimax.io/`, and `https://www.minimax.io/audio` returned JavaScript shells during retrieval, leaving current consumer UX and availability unverified.
- The 2025-06-20 X post was not readable. A same-day first-party Hailuo Video Agent announcement exists, but exact correspondence is unverified.
- The M2.1 release date varies in records: 2025-12-27 in the dated event, 2025-12-23 in the release article, and 2025-12-22 in API release notes.
- `minimax` and `minimax_models` mix corporate history with model lineages. They connect, but they do not form a single-product lifecycle.

## Sources

| source | title | read |
|---|---|---|
| https://www.minimax.io/news/video-01 | MiniMax officially releases the Video-01 video generation model | 2026-09-04 |
| https://huggingface.co/collections/MiniMaxAI/minimax-m1-68502ad9634ec0eeac8cf094 | MiniMax-M1 - a MiniMaxAI Collection | 2026-09-04 |
| https://github.com/MiniMax-AI/MiniMax-M1 | MiniMax-AI/MiniMax-M1 | 2026-09-04 |
| https://www.minimax.io/news/minimax-hailuo-02 | MiniMax Hailuo 02, World-Class Quality, Record-Breaking Cost Efficiency | 2026-09-04 |
| https://www.minimax.io/news/video-agent | Introducing Hailuo Video Agent in Beta, Vibe Videoing with Zero-touch | 2026-09-04 |
| https://www.minimax.io/news/minimax-m21 | MiniMax M2.1: Significantly Enhanced Multi-Language Programming, Built for Real-World Complex Tasks | 2026-09-04 |
| https://platform.minimax.io/docs/release-notes/models | Models - MiniMax API Docs release notes | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-M2.1 | MiniMaxAI/MiniMax-M2.1 | 2026-09-04 |
| https://platform.minimax.io/docs/guides/models-intro | Models - MiniMax API Docs | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/api-overview | API Overview - MiniMax API Docs | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/text-anthropic-api | Anthropic SDK - MiniMax API Docs | 2026-09-04 |
| https://www.minimax.io/models/text/m3 | MiniMax M3 - Coding & Agentic Frontier, 1M Context, Multimodal | 2026-09-04 |
| https://www.minimax.io/news/minimax-h3-open-source | Open General Intelligence: MiniMax H3 Is Now Open Source | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:minimax`, thread `minimax-models-and-products`, 3 dated events 2025-06-18 → 2025-12-27.
- **Practical note:** As of 2025-12-27, practitioners should evaluate MiniMax model use by the explicitly listed route—MiniMax Agent, the text API, OpenRouter, or Ollama—rather than assuming one interface covers all MiniMax products.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
