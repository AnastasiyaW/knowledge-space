---
title: "Needle Automation Model"
category: "projects"
date: 2026-09-19
tags: ["needle-automation-model", "project"]
aliases: ["Needle Automation Model: needle-automation-model"]
---

# Needle 3

**Development line:** project:needle-automation-model · thread needle-automation-model  
**Last event:** 2026-09-19 · 1 dated since 2026-09-19 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Needle 3 is a foundation model from Cactus Compute for mobile, wearables, robots, smart home, automotive and microcontrollers.

- **Tool calls:** runs locally and outputs structured JSON.
- **Structured extraction:** extracts fields into structured JSON.
- **Text embeddings:** runs locally for search, matching and routing.

It ships as a single 8-29 MB binary built on a Simple Attention Network. It trades general chat capacity for tool calls, structured extraction and text embeddings that run locally.

## Development line

- **2026-09-19 — Needle 3 announcement.** Cactus Compute announced Needle 3, an automation model for small devices focused on tool calling, structured data extraction and device control. The vendor claims 4000 tokens/sec decode speed on a Raspberry Pi 5 and states it beats DeepSeek V4 Flash after fine-tuning.
  - The release page confirms the sizes: a single 8-29 MB binary, 29-121M parameters, and 2-20 layers. It lists decode speed on a Raspberry Pi 5 as 400-4k tokens/s, so the 4000 figure is the top of that range. It adds that tool calls return an empty list when no tool fits, and that a decode grammar guarantees extraction output parses. The same model returns text embeddings for local search, matching and routing. The DeepSeek V4 Flash claim is specific: a 4-layer subnetwork matches it after one epoch of tuning on downstream tasks. DeepSeek V4 Flash was reached through its cloud API in the comparison. (2026-09-19) — <https://cactuscompute.com/needle>

## What changed

Needle 3 was released as a laddered family of sub-networks, from 2 to 20 layers and 29-121M parameters. The release page says it beats models 10x its size on mobile tool calls and matches models 2-3x its size on extraction. It also says a 4-layer subnetwork can match DeepSeek V4 Flash after one epoch of fine-tuning on downstream tasks.

## How to use this

1. Install the Python package with `pip install cactus-compute`. The inference engine is fetched once from Hugging Face and cached, so nothing else needs to be built.
  — <https://cactuscompute.com/needle>
2. For tool calls, give Needle the functions your app exposes. It picks the right ones and fills each argument from what the user said. Two requests give two calls in order.
  — <https://cactuscompute.com/needle>
3. For extraction, declare a shape (invoice, booking, notification or form) and pass in messy text to get typed fields back.
  — <https://cactuscompute.com/needle>
4. Choose a model size from the 2-layer to the 20-layer subnetwork to fit the target device, and fine-tune it on your own tasks.
  — <https://cactuscompute.com/needle>

## Best practices

- Describe your tools well, because Needle reads the tool descriptions to decide what to call and how to fill arguments. The page says this is the whole game.
  — <https://cactuscompute.com/needle>
- Fine-tune the chosen subnetwork on your downstream tasks. The 4-layer version matches DeepSeek V4 Flash only after tuning.
  — <https://cactuscompute.com/needle>
- In automotive use, pin the tool set so it survives long conversations.
  — <https://cactuscompute.com/needle>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The release page's benchmark figures are the vendor's own and have not been independently verified.
- The exact license and weights hosting terms are not stated on the page excerpt.
- The page excerpt does not say whether the 4000 tokens/s peak applies to the smallest subnetwork only.

## Sources

| source | title | read |
|---|---|---|
| https://cactuscompute.com/needle | Needle 3 - 8-29 MB foundation model for tiny devices \| Cactus | 2026-09-19 |

## Agent brief {#agent-brief}

- **Subject:** project:needle-automation-model, thread needle-automation-model, 1 dated events 2026-09-19 → 2026-09-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium.
