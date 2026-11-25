---
title: Gemini
category: projects
date: 2026-07-22
tags: [gemini, gemini-app, gemini-gems, gemini-product-development, google-gemini, project]
aliases: ["Gemini", "Google Gemini"]
---

# Gemini

**Development line:** `project:google-gemini` · thread `gemini-product-development`  
**Last event:** 2026-07-22 · 1 dated since 2026-07-22 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Gemini is Google's product family for chat, files, code, and model integration into apps.
- Gemini Apps: conversation, attachments, and model selection.
- Gems: saved instructions for repeated tasks.
- Gemini API and AI Studio: multimodal calls, structured output, and tools.

Available model IDs and statuses change; the current catalog includes `gemini-3.8-flash`, while `gemini-3.6-flash` remains listed. Use a Gem for personal routines, and the API with an explicit model choice and response checks for products.

## Development line

- **2026-07-22 — Gemini 3.6 Flash was linked with updated Flash model variants.** A linked Google page from 2026-07-21 introduced Gemini 3.6 Flash, 3.5 Flash-Lite, and a limited pilot of 3.5 Flash Cyber; 3.6 and 3.5 Flash-Lite became available through Gemini API and AI Studio.

## What changed

- 2024-05-14 — Gemini Apps: Gemini Advanced received Gemini 1.5 Pro with a 1 million token context window and file uploads.
- 2024-05-14 — Gems: Google previewed customizable versions of Gemini, marked "soon" rather than a confirmed public launch.
- 2024-05-14 — Gemini API: Google introduced Gemini 1.5 Flash for high-frequency tasks, while Gemini 1.5 Pro gained context up to 2 million tokens and audio processing in API and AI Studio.
- 2024-12-20 — AI Studio: a new chat URL appeared without disclosing model, version, or release, leaving the specific change unconfirmed.
- 2026-07-22 — Flash lineup: a linked Google page from 2026-07-21 introduced Gemini 3.6 Flash, 3.5 Flash-Lite, and a limited pilot of 3.5 Flash Cyber; 3.6 and 3.5 Flash-Lite became available through Gemini API and AI Studio.
- 2026-09-04 — Current catalog: Gemini API lists `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash`, and `gemini-3.5-flash-lite`; 3.6 is no longer the only current choice.

3.5 Flash Cyber did not become a public API model; Google describes a pilot for governments and trusted partners through CodeMender. Pick a version from the current catalog for new integrations, not from an old AI Studio link.

## How to use this

From 2026-07-22, treat Gemini 3.6 Flash as an AI Studio model candidate, and verify its capabilities, rollout, and pricing in the linked official model update before adopting it.

1. For personal tasks, open Gemini Apps, sign in, pick a model, attach a file or image if needed, and send the prompt.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
2. For repeated roles, open Explore Gems → New Gem. Set the name, add instructions covering role, task, context, and format, test in preview, and save.
  — <https://support.google.com/gemini/answer/15235603>
3. For integrations, create a project and an API key in AI Studio. Store the key in an environment variable, install the SDK, and make the first Interactions API call from Python, JavaScript, or REST.
  — <https://ai.google.dev/gemini-api/docs/get-started>
4. Before release, pin an exact model ID from the live catalog in configuration. Current documentation starts with `gemini-3.8-flash`.
  — <https://ai.google.dev/gemini-api/docs/models?hl=en>
5. When answers require fresh data, connect Google Search. When calling internal systems, declare a function, run it in the app, and return the result to the model.
  — <https://ai.google.dev/gemini-api/docs/tools>

## Best practices

- State goal, constraints, format, and context explicitly; use several consistent examples when style or classification matters.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- For Gemini 3.x, keep temperature, top-p, and top-k at default values first; document and test every change, because tuning can degrade complex reasoning or trigger loops.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Use Structured Outputs for fixed final formats, and Function Calling for actions; check schema JSON for semantics and business rules.
  — <https://ai.google.dev/gemini-api/docs/structured-output>
- Verify Gemini Apps responses before professional decisions; help docs explicitly warn that the app can make mistakes.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
- Select a tier before sending work data; Google states Free content trains products while Paid does not, so verify team and contract terms.
  — <https://ai.google.dev/gemini-api/docs/pricing>

## Superseded by this

- 2024-05-14: "Gems coming soon" is obsolete; current help docs explain how to create, test, and save Gems.
- 2024-05-14: Starting a new API integration with Gemini 1.5 Flash or 1.5 Pro is obsolete; the current Gemini API catalog focuses on 3.x and lists Gemini 3.8 Flash.
- 2026-07-22: Gemini 3.6 Flash and 3.5 Flash-Lite remain available, but 3.6 Flash is no longer the newest Flash model; the catalog also contains 3.7 and 3.8 Flash.
- 2024-12-20: The new AI Studio chat URL is an entry point, not a stable model version recommendation.

## Still unknown

- Exact wording for the two 2024-05-14 entries is unavailable; official announcements from that day confirm the direction, not the full text.
- The 2024-12-20 entry gives only a new AI Studio chat URL, without specifying a model, version, or release.
- Gemini Apps, Gems, and Gemini API are different surfaces of one family, not separate projects; availability depends on account, tier, region, and model.

## Sources

| source | title | read |
|---|---|---|
| https://blog.google/products-and-platforms/products/gemini/google-gemini-update-may-2024/ | Get more done with Gemini: Try 1.5 Pro and more intelligent features | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/google-gemini-update-flash-ai-assistant-io-2024/ | Gemini breaks new ground with a faster model, longer context, AI agents and more | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ | Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models?hl=en | Models | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/get-started | Getting started | Gemini API | Google AI for Developers | 2026-09-04 |
| https://support.google.com/gemini/answer/13275745?hl=en | Use Gemini Apps | 2026-09-04 |
| https://support.google.com/gemini/answer/15235603 | Tips for creating custom Gems | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt design strategies | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/tools | Using tools with Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/structured-output | Structured outputs | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/pricing | Gemini Developer API pricing | Gemini API | Google AI for Developers | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:google-gemini`, thread `gemini-product-development`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** From 2026-07-22, practitioners should treat Gemini 3.6 Flash as an AI Studio model-selection candidate and verify its capabilities, rollout, and pricing in the linked official model update before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
