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

Gemini is Google's product family for chat, files, code, and model integration into applications.

- Gemini Apps: conversation, attachments, and model selection.
- Gems: saved instructions for repeatable tasks.
- Gemini API and AI Studio: multimodal calls, structured output, and tools.

Available model IDs and statuses change; the current directory already lists `gemini-3.8-flash`, while `gemini-3.6-flash` remains on the list. For personal routines we use a Gem; for a product we use the API with explicit model selection and response verification.

## Development line

- **2026-07-22 — Gemini 3.6 Flash was linked with updated Flash model variants.** A linked Google page from 2026-07-21 introduced Gemini 3.6 Flash, 3.5 Flash-Lite, and a limited pilot of 3.5 Flash Cyber; 3.6 and 3.5 Flash-Lite became available through the Gemini API and AI Studio.

## What changed

- 2024-05-14 — Gemini Apps: Gemini Advanced received Gemini 1.5 Pro with a 1 million token context and file uploads; source found today.
- 2024-05-14 — Gems: Google showed customizable versions of Gemini, but on that day marked them "soon" rather than confirming a public launch; source found today.
- 2024-05-14, found today — Gemini API: Google introduced Gemini 1.5 Flash for high-frequency tasks, and Gemini 1.5 Pro received context up to 2 million tokens and audio processing in the API and AI Studio.
- 2024-12-20 — AI Studio: a new chat URL is given; it reveals no model, version, or release, so no specific change is confirmed.
- 2026-07-22 — Flash line: a linked Google page from 2026-07-21 introduced Gemini 3.6 Flash, 3.5 Flash-Lite, and a limited pilot of 3.5 Flash Cyber; 3.6 and 3.5 Flash-Lite became available through the Gemini API and AI Studio.
- 2026-09-04, found today — the current Gemini API catalog lists `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash`, and `gemini-3.5-flash-lite`; 3.6 is no longer the only current choice.
- 3.5 Flash Cyber did not become a public API model: Google describes a pilot for governments and trusted partners through CodeMender.
- For a new integration, take a version from the current catalog rather than an old AI Studio link.

## How to use this

From 2026-07-22, practitioners should treat Gemini 3.6 Flash as a recorded AI Studio model-selection candidate and verify its capabilities, rollout, and pricing in the linked official model update before adopting it.

1. For personal tasks, open Gemini Apps, sign in, pick a model, attach a file or image if needed, and send the prompt.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
2. For a repeated role, open Explore Gems → New Gem; set a name and instructions with role, task, context, and format, test in preview, and save.
  — <https://support.google.com/gemini/answer/15235603>
3. For integration, create a project and key in AI Studio, store the key in an environment variable, install the SDK, and make the first Interactions API call from Python, JavaScript, or REST.
  — <https://ai.google.dev/gemini-api/docs/get-started>
4. Before release, pick an exact model ID from the live catalog and pin it in configuration; current documentation starts with `gemini-3.8-flash`.
  — <https://ai.google.dev/gemini-api/docs/models?hl=en>
5. When an answer needs fresh data, connect Google Search; when calling an internal system, declare a function, run it in the application, and pass the result back to the model.
  — <https://ai.google.dev/gemini-api/docs/tools>

## Best practices

- State the goal, constraints, format, and context explicitly; use several consistent examples when style or classification matters.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- For Gemini 3.x, leave temperature, top-p, and top-k at default at first; document and verify each change, because tuning can degrade complex reasoning or cause loops.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Use Structured Outputs for a fixed final format, and Function Calling for actions; still verify schema-valid JSON for semantics and business rules.
  — <https://ai.google.dev/gemini-api/docs/structured-output>
- Check Gemini Apps responses before professional decisions: documentation explicitly warns that the app can make mistakes.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
- Choose a tier before sending work data: for Free, Google specifies content is used to improve products; for Paid, it is not; check this against team and contract requirements.
  — <https://ai.google.dev/gemini-api/docs/pricing>

## Superseded by this

- 2024-05-14: "Gems coming soon" status is obsolete — current documentation describes creating, previewing, and saving Gems.
- 2024-05-14: the recommendation to start a new API integration on Gemini 1.5 Flash or 1.5 Pro is obsolete; the current Gemini API catalog leads with 3.x and lists Gemini 3.8 Flash.
- 2026-07-22: Gemini 3.6 Flash and 3.5 Flash-Lite remain available, but we cannot treat 3.6 Flash as automatically the newest Flash: the current catalog also contains 3.7 and 3.8 Flash.
- 2024-12-20: the new AI Studio chat URL is an entry point, not a stable model version recommendation.

## Still unknown

- Exact wording of the two entries from 2024-05-14 is unavailable: official announcements from that day confirm the direction, but not the text of each entry.
- The 2024-12-20 entry gives only a new AI Studio chat URL; we cannot reliably deduce the model, version, or release from it.
- Gemini Apps, Gems, and the Gemini API are different surfaces of one family rather than separate projects; availability depends on account, tier, region, and model.

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
- **Practical note:** From 2026-07-22, practitioners should treat Gemini 3.6 Flash as a recorded AI Studio model-selection candidate and verify its capabilities, rollout, and pricing in the linked official model update before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
