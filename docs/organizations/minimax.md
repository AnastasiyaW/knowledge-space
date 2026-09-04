---
title: MiniMax — MiniMax models and products
category: organizations
tags: [minimax, minimax-models-and-products, minimax_models, organization]
aliases: ["MiniMax"]
---

# MiniMax — MiniMax models and products

**Development line:** `organization:minimax` · thread `minimax-models-and-products`  
**Events:** 3 dated, 2025-06-18 → 2025-12-27 · **Researched:** 2026-09-04 · confidence: medium

## What it is

MiniMax is an AI provider for developers who want an Anthropic-SDK-compatible model API plus video and speech services, and for creators using separate Hailuo and Audio products. - M3: language, tool use, image/video input, and a 1M-token context window. - H3: text, image, first/last-frame, and multimodal-reference video generation. - Speech 2.8: synthesis, cloning, and voice design. Measure: H3 outputs 4–15-second, 24-fps video up to 2K; new users cannot start paid Music APIs after 2026-08-20, and free Music APIs were discontinued. Verdict: choose the current product line for the modality; M2.1 and Hailuo 02 are compatibility or self-hosting choices, not defaults for a new build.

## Development line

- **2025-06-18 — MiniMax surfaced MiniMax-M1 model resources.** On 2025-06-18, MiniMax linked a Hugging Face collection for MiniMax-M1 and a GitHub repository for the model. The same dated link set also pointed to Hailuo Create and MiniMax Agent, placing the model alongside MiniMax's video-creation and agent product surfaces.
- **2025-06-22 — MiniMax publicly surfaced its Audio product.** On 2025-06-22, MiniMax linked its Audio product page at minimax.io/audio. This establishes MiniMax Audio as a public product surface in this development line on that date.
- **2025-12-27 — MiniMax surfaced M2.1 through hosted and local access routes.** On 2025-12-27, MiniMax linked its MiniMax-M2.1 news page and Hugging Face model repository. The dated resource set also pointed to MiniMax Agent, an Anthropic-compatible text API reference, OpenRouter, and Ollama, showing multiple listed access routes for M2.1.

## What changed

2024-10-10 — A MiniMax event is recorded without retained text or URL, so it creates no source-backed historical claim. Found today: MiniMax’s closest primary baseline is Video-01, released 2024-08-31 with text-to-video and image-to-video at 720p/25 fps for up to six seconds; this is context, not confirmation of the 10 October change. 2025-06-18 — MiniMax M1 and Hailuo 02 entered the record. M1 was an open-weight hybrid-attention reasoning model with 456B total parameters, 45.9B active parameters, and 1M context; Hailuo 02 added native 1080p video options. 2025-06-20 — Hailuo Video Agent entered beta with prebuilt video templates as Stage One; its more autonomous stages were a roadmap, not a verified current capability. 2025-06-22 — A MiniMax Audio endpoint was recorded, but its retained page exposes no dated release details. Found today: speech remains a distinct API line with synthesis, cloning, and voice design; music access has since changed materially. 2025-12-27 — M2.1 entered the record as an open-weight, agent-oriented M2 model for multilingual coding, tool use, instruction following, and long-horizon work. MiniMax’s release note is dated 2025-12-23, while its model release notes say 2025-12-22. Found today — M3 released on 2026-06-01 as the current 1M-context language model; H3 was open-sourced on 2026-08-03 as the current multimodal video line; and music API access changed on 2026-08-20 for new users.

## How to use this

As of 2025-12-27, practitioners should evaluate MiniMax model use by the explicitly listed route—MiniMax Agent, the text API, OpenRouter, or Ollama—rather than assuming one interface covers all MiniMax products.

1. Choose the current surface first: M3 for new language, coding, tool-use, or multimodal API work; H3 for video; Speech 2.8 for voice. Do not start from a historical M2.1 or Hailuo model name.
  — <https://platform.minimax.io/docs/guides/models-intro>
2. Create a pay-as-you-go API key in the MiniMax Platform; it covers language, video, speech, and image models.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
3. For a new language integration, configure the Anthropic SDK with `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic`, use the MiniMax API key, and select `MiniMax-M3`.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
4. For a tool-calling conversation, append the complete assistant response—including thinking, text, and tool-use blocks—to history before sending tool results and the next turn.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
5. For H3 video, create an asynchronous task, persist its `task_id`, query status, and retrieve the output URL only after success. Select inputs and duration within the documented 4–15-second range.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
6. For speech, choose synchronous T2A for short interactive output or asynchronous synthesis for long text. Do not begin a new Music API integration; use MiniMax Audio or the open Music 3 model instead.
  — <https://platform.minimax.io/docs/api-reference/api-overview>

## Best practices

- Treat Anthropic compatibility as a documented subset: `top_k`, stop sequences, MCP servers, context management, and containers are ignored rather than emulated.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Use M3’s adaptive thinking for complex reasoning and disable it for latency-sensitive work; preserve thinking blocks unchanged across tool-use turns.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Use M3—not M2.x—when the request needs image or video input, and estimate tokens before large multimodal requests.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Keep M2.1, Hailuo 02/2.3, and older Speech models behind an explicit compatibility or migration decision: MiniMax classifies them as legacy.
  — <https://platform.minimax.io/docs/guides/models-intro>
- Treat video creation as a job workflow, not a synchronous call: retain task identifiers, query results, and handle cancellation or deletion deliberately.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
- If an existing deployment requires local M2.1 weights, use the vendor-recommended SGLang or vLLM serving paths and review the Modified MIT license before shipping.
  — <https://huggingface.co/MiniMaxAI/MiniMax-M2.1>
- For music, verify account eligibility before designing a workflow: new users no longer receive paid Music API access and the free endpoints are discontinued.
  — <https://platform.minimax.io/docs/api-reference/api-overview>

## Superseded by this

- 2024-08-31 / 2024-10-10 — Video-01-era guidance of 720p, 25-fps, up-to-six-second text/image-to-video is legacy. H3 now covers multimodal inputs, 4–15-second output, 24 fps, and up to 2K.
- 2025-06-18 — M1 as the default hosted 1M-context model is historical. For a new hosted build, MiniMax now documents M3 as the current 1M-context language model; M1 remains an archival or self-hosted open-weight option.
- 2025-06-20 — Hailuo Video Agent Stage One beta and its Stage Two/Three roadmap are historical. Verify current delivery against H3 and API documentation rather than assuming the roadmap shipped.
- 2025-12-27 — Choosing M2.1 as MiniMax’s flagship for a new build is obsolete. It remains API-compatible and downloadable, but MiniMax lists it under Legacy Models.
- 2025-06-22 — Starting a new Music API workflow from earlier MiniMax Audio guidance is obsolete: from 2026-08-20, paid Music APIs are unavailable to new users and free Music endpoints are discontinued.

## Still unknown

- The 2024-10-10 event has no retained link or text. The 2024-08-31 Video-01 page is nearby primary context, not proof of the exact October change.
- The supplied `https://hailuoai.video/create`, `https://agent.minimax.io/`, and `https://www.minimax.io/audio` pages were JavaScript shells during current retrieval, so their present consumer UX and availability are not verified here.
- The supplied 2025-06-20 X post was not independently readable. A same-day first-party Hailuo Video Agent announcement is verified, but the exact correspondence cannot be proven.
- The M2.1 date differs across the record: 2025-12-27 in the dated event, 2025-12-23 on the release article, and 2025-12-22 in release notes.
- `minimax` and `minimax_models` combine company/product history with a model-version lineage. They are related but should not be treated as one single-product lifecycle in a knowledge base.

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
