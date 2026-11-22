---
title: "Thinking Machines: thinking-machines-inkling-2-small-release — Thinking Machines Inkling 2 Small Release"
category: "organizations"
date: 2026-11-21
tags: ["organization", "thinking-machines", "thinking-machines-inkling-2-small-release"]
aliases: ["Thinking Machines: thinking-machines-inkling-2-small-release"]
---

# Thinking Machines: thinking-machines-inkling-2-small-release — Thinking Machines Inkling 2 Small Release

**Development line:** organization:thinking-machines · thread thinking-machines-inkling-2-small-release  
**Last event:** 2026-11-21 · 2 dated since 2026-11-21 · **Researched:** 2026-11-21 · confidence: high

## What it is

Inkling 2 Mini is an open-weights multimodal model from Thinking Machines Lab. It runs locally on a developer workstation and competes with Qwen2.5-Coder and Qwen3.8-27B.

What it does:

- text generation
- image comprehension
- agentic tool invocation
- automated software repair

It has 26.4B total parameters and 3.4B active per step. It has 24 physical layers, and the middle blocks run three times, giving 48 layer applications in about 20 GB of memory. That brings developer-tier coding to 32 GB Apple Silicon and single GPUs, with no hosted inference needed.

## Development line

- **2026-11-21 — Thinking Machines releases Inkling 2 Mini for laptops.** Thinking Machines released Inkling 2 Mini, a 26.4-billion-parameter model that needs about 20 GB of memory. Weights are on Hugging Face. Tinker pricing is 15 cents per million input tokens and 50 cents per million output tokens. In a demo, the model ran offline on a 48 GB MacBook Pro during a flight and generated a playable flight simulator.
- **2026-11-21 — Thinking Machines releases Inkling 2 Mini looped transformer.** Thinking Machines released Inkling 2 Mini, a small looped transformer for local deployment. It has about 26.4B total parameters and about 3.4B active. Its 24 layers sit in four blocks of six, and the middle two blocks run three times each. That gives 48 layer applications per token. The release describes its benchmark results as comparable to Qwen3.8-27B. Talk of using the architecture in other models is unverified and is not part of this event.
- **2026-11-21 — further details from the same date.**
  - The release carries an Apache 2.0 license and a 1-million-token context window. It scores 79.2% on SWE-bench Verified and 77.9% on SWEBench Pro v2 Hard. (2026-11-21) — <https://thinkingmachines.ai/news/inkling-2-mini/>
  - The architecture uses decoder-only sparse mixture-of-experts blocks with mixed NVFP4/MXFP8 quantization, which fits it into the 20 GB footprint. The TML-d24-varloop-research checkpoint supports 1 to 5 variable loop passes. (2026-11-21) — <https://huggingface.co/thinkingmachines/Inkling-2-Mini>

## What changed

Thinking Machines released Inkling 2 Mini as open weights, with public weights on Hugging Face and hosted Tinker inference endpoints. Depth now comes from looping middle blocks, not from stacking more physical layers. An open research variant lets the loop count be configured.

## How to use this

1. Download the weights from the Hugging Face repository, or pull the model in Ollama with ollama run thinkingmachines/inkling-2-mini.
  — <https://huggingface.co/thinkingmachines/Inkling-2-Mini>
2. Run it locally with vLLM or Ollama on hardware with at least 20 GB to 32 GB of memory, such as an Apple Silicon Mac or a 24 GB GPU.
  — <https://thinkingmachines.ai/news/inkling-2-mini/>
3. Or query it through the hosted Tinker API at 15 cents per million input tokens and 50 cents per million output tokens.
  — <https://thinkingmachines.ai/news/inkling-2-mini/>

## Best practices

- Allocate at least 24 GB to 32 GB of unified memory when running locally, so the ~20 GB of weights fit alongside the KV cache for long context.
  — <https://thinkingmachines.ai/news/inkling-2-mini/>
- Use the 1M token context window for large codebases and agentic tool-use loops, not a truncated window.
  — <https://thinkingmachines.ai/news/inkling-2-mini/>

## Superseded by this

- Local coding models needed full 27B\+ parameter linear-depth architectures to reach SWE-bench scores in the 70-80% range.
  — <https://thinkingmachines.ai/news/inkling-2-mini/>

## Still unknown

- Community sentiment and third-party postmortems from developer forums were not found in the search results.
- Throughput and latency of the 3-loop transformer passes on non-Apple hardware are unbenchmarked in the vendor's release documentation.

## Sources

| source | title | read |
|---|---|---|
| https://thinkingmachines.ai/news/inkling-2-mini/ | Thinking Machines - Inkling 2 Mini | 2026-11-21 |
| https://huggingface.co/thinkingmachines/Inkling-2-Mini | thinkingmachines/Inkling-2-Mini · Hugging Face | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** organization:thinking-machines, thread thinking-machines-inkling-2-small-release, 2 dated events 2026-11-21 → 2026-11-21.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
