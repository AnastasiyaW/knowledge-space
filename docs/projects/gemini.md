---
title: Gemini
category: projects
date: 2026-08-14
tags: [gemini, gemini-development, project]
aliases: ["Gemini", "Gemini 1.5", "Gemini 3.7 Flash"]
---

# Gemini

**Development line:** `project:gemini` · thread `gemini-development`  
**Last event:** 2026-08-14 · 6 dated since 2024-02-16 · **Researched:** 2026-09-04 · confidence: high

## What it is

Gemini is Google's model family for chat, text, code, images, audio, video, and API integrations.

- Gemini app: manual chat and everyday tasks.
- AI Studio: prompt prototyping and code generation.
- Gemini API: backend integration into applications.
- Live API: streaming voice and vision interfaces.

Access to the consumer app, API keys, pricing tiers, Live API, and macOS features is independent, and Live API remains in Preview. We prototype in AI Studio, pin a stable model ID in production, and check its pricing tier and lifecycle.

## Development line

- **2024-02-16 — Google publishes a Gemini model-development announcement.** On 2024-02-16, Google linked an official Technology & AI blog item about Gemini as a next-generation model. This is a first-party model-development announcement for Gemini. The supplied link alone does not establish its exact feature or availability scope.
- **2024-12-12 — Gemini-related Live interface appears in Google AI Studio.** On 2024-12-12, a Google AI Studio Live page was linked for the Gemini line. This indicates a Gemini-related live-interaction surface in the developer environment. The supplied URL does not establish the precise model, API, or launch status.
- **2026-03-03 — Gemini 3.1 Flash-Lite Preview appears with pricing documentation.** On 2026-03-03, Google AI Studio linked Gemini 3.1 Flash-Lite Preview alongside official pricing documentation for that named preview. This is a material availability-and-pricing step for the Gemini developer model line. The supplied links do not establish quotas, regions, or final-release status.
- **2026-04-10 — Gemini app announces 3D-model and chart capabilities.** On 2026-04-10, Google linked an official Gemini app announcement concerning 3D models and charts, together with the Gemini app. This records a product-capability step in the Gemini application surface. The URLs alone do not establish how the capability was implemented or which accounts received it.
- **2026-04-16 — Gemini gains a Mac-specific product surface.** On 2026-04-16, Google linked a Gemini page specifically for Mac. This records an expansion of the Gemini product's desktop-platform surface. The supplied URL does not establish the exact supported macOS versions, rollout scope, or feature set.
- **2026-08-14 — Google introduces Gemini 3.7 Flash for AI Studio.** On 2026-08-14, Google linked an official announcement introducing Gemini 3.7 Flash and an AI Studio prompt URL selecting that model. This is a material model-release and developer-availability step. The supplied links do not establish the model's final status, limits, or regional availability.

## What changed

- 2024-02-16: Gemini 1.5 Pro introduced MoE architecture, 128K standard context, and a limited preview up to 1M tokens through AI Studio and Vertex AI.
- 2024-12-12: Gemini 2.0 introduced the Multimodal Live API for real-time audio and video streaming; the historical AI Studio Live URL now requires sign-in, while the current Live API runs over stateful WebSocket and remains in Preview.
- 2026-03-03: Gemini 3.1 Flash-Lite entered preview for high-frequency tasks, translation, moderation, and data processing; Google later retired the preview endpoint.
- 2026-04-10: Gemini app added generation of interactive simulations and models directly in chat, with configurable visualization parameters.
- 2026-04-16: Gemini for macOS added desktop access with hotkeys and screen context; it requires an Apple Silicon machine running macOS 15+ in a supported country.
- 2026-08-14: Gemini 3.7 Flash, announced by Google on August 13, became the Flash model for coding and agent workflows.
- Found 2026-09-04: Gemini 3.8 Flash launched on September 2 and is the current stable Flash; Gemini 3.7 Flash remains fully supported, but the model list now marks it previous-generation.

## How to use this

Track Gemini by product surface as of 2026-08-14. Use AI Studio's Live interface for live workflows (2024-12-12). Price and evaluate Gemini 3.1 Flash-Lite Preview before adoption (2026-03-03). Select Gemini 3.7 Flash in AI Studio where available (2026-08-14), and treat Gemini app and Mac features as separate product surfaces.

1. Open Gemini app, sign in with a Google Account, and start a chat with text or attached files for one-off tasks.
  — <https://gemini.google.com/app>
2. Install Gemini for macOS on Mac only if the device has Apple Silicon, runs macOS Sequoia 15.0+, and the country supports Gemini app.
  — <https://gemini.google/mac/>
3. Open Google AI Studio to prototype: pick a prompt interface, test the model, adjust parameters and safety settings, and add tools.
  — <https://ai.google.dev/gemini-api/docs/ai-studio-quickstart>
4. Use Get code after prototyping, create or import a Cloud project, and generate an API auth key for backend integration.
  — <https://ai.google.dev/gemini-api/docs/api-key>
5. Select a stable endpoint from the model list before deployment; evaluate gemini-3.8-flash for new coding and agent tasks instead of defaulting to the older 3.7 endpoint.
  — <https://ai.google.dev/gemini-api/docs/models>
6. Use the separate Live API path over WebSocket for real-time voice or vision dialogue; use ephemeral tokens for client-to-server setups.
  — <https://ai.google.dev/gemini-api/docs/live-api>

## Best practices

- Pin production workloads to a specific stable model ID instead of latest or experimental aliases: latest changes automatically, and experimental endpoints carry tighter limits without contract stability.
  — <https://ai.google.dev/gemini-api/docs/models>
- Write short, direct instructions for Gemini 3; do not carry over verbose prompt engineering techniques from older models.
  — <https://ai.google.dev/gemini-api/docs/gemini-3>
- Enable Structured Output for complex JSON Schema instead of relying on "reply in JSON"; add consistent examples for repeatable formatting.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Place the question after reference material in long-context calls, omit unneeded context, and cache reused files or data.
  — <https://ai.google.dev/gemini-api/docs/long-context>
- Keep the API key out of Git and client code; route web and mobile production calls through a backend and restrict the key.
  — <https://ai.google.dev/gemini-api/docs/api-key>
- Check the pricing table before estimating costs: free and paid tiers differ in limits, features, and content handling, so launch announcement pricing is not a valid estimate.
  — <https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview>

## Superseded by this

- 2024-02-16 — Early access for Gemini 1.5 Pro with 128K base context and limited 1M preview is historical background, not current model selection guidance.
- 2026-03-03 — The `gemini-3.1-flash-lite-preview` endpoint was shut down on 2026-05-25; its direct replacement was `gemini-3.1-flash-lite`. That replacement now lists a shutdown date of 2027-05-07 with `gemini-3.5-flash-lite` as the next recommended successor.
- Found 2026-09-04 — Describing Gemini 3.7 Flash as the newest Flash is obsolete: `gemini-3.8-flash` was released on 2026-09-02. `gemini-3.7-flash` remains fully supported, but it is now the previous-generation stable option.

## Still unknown

- Gemini spans separate product surfaces: consumer app, macOS app, AI Studio, Gemini API, and Live API. Access to one does not confirm quotas, pricing tiers, or features for another.
- The historical AI Studio Live URL redirects to a login prompt. We cannot verify the exact interface or settings from December 2024 without an active session; an official announcement on December 11, 2024, and current documentation confirm the launch separately.
- The Gemini for macOS product page lists requirements and limits but gives no launch date; it does not independently verify the 2026-04-16 date.

## Sources

| source | title | read |
|---|---|---|
| https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/#sundar-note | Our next-generation model: Gemini 1.5 | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/ | Google introduces Gemini 2.0: A new AI model for the agentic era | 2026-09-04 |
| https://aistudio.google.com/live | Sign in - Google Accounts | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview | Цены на API Gemini Developer | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/ | Gemini 3.1 Flash-Lite: Built for intelligence at scale | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/gemini-app/3d-models-charts/ | The Gemini app can now generate interactive simulations and models. | 2026-09-04 |
| https://gemini.google.com/app | Google Gemini | 2026-09-04 |
| https://gemini.google/mac/ | Gemini for macOS – native AI assistant and Mac automation | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/ | Introducing Gemini 3.7 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models | Models | Gemini API | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/deprecations?hl=en | Gemini deprecations | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/latest-model | What's new in Gemini 3.8 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/ai-studio-quickstart | Google AI Studio quickstart | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/api-key | Using Gemini API keys | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt design strategies | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/long-context | Long context | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/gemini-3 | Gemini 3 developer guide | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/live-api | Gemini Live API overview | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:gemini`, thread `gemini-development`, 6 dated events 2024-02-16 → 2026-08-14.
- **Practical note:** As of 2026-08-14, practitioners should track Gemini by product surface: use AI Studio's Live interface for live workflows (2024-12-12), evaluate and price Gemini 3.1 Flash-Lite Preview before adoption (2026-03-03), and select Gemini 3.7 Flash in AI Studio where available (2026-08-14), while treating Gemini app and Mac features as separate product surfaces.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
