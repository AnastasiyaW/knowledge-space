---
title: "Q.ANT: llm-inference-on-photonic-hardware — Llm Inference On Photonic Hardware"
category: "organizations"
date: 2026-11-18
tags: ["llm-inference-on-photonic-hardware", "organization", "q-ant"]
aliases: ["Q.ANT: llm-inference-on-photonic-hardware"]
---

# Q.ANT: llm-inference-on-photonic-hardware — Llm Inference On Photonic Hardware

Q.ANT NPU Gen 2\+ is a PCIe photonic co-processor that runs Fourier transforms next to a GPU for hybrid LLM inference.

**Development line:** organization:q-ant · thread llm-inference-on-photonic-hardware  
**Last event:** 2026-11-18 · 2 dated since 2026-11-18 · **Researched:** 2026-11-19 · confidence: medium

## What it is

Q.ANT NPU Gen 2\+ is a PCIe photonic co-processor built on thin-film lithium niobate. It accelerates discrete Fourier transforms for hybrid neural network inference next to host electronic GPUs.

- Optical DFT: computes a discrete Fourier transform in a single pass of light.
- Attention offload: takes token-mixing attention operations off the electronic accelerators.
- PCIe: connects through standard server slots.
- SDK: C and Python simulation tools for model development.

It targets hybrid execution of language models of about one billion parameters. A host GPU still runs the remaining network layers. It is an optical math block, not a standalone general-purpose processor.

## Development line

- **2026-11-18 — Q.ANT demonstrates hybrid LLM inference with photonic NPU at SC26.** At SC26 in Chicago, Germany's Q.ANT moved part of a language model's layers from an AMD GPU to its photonic NPU Gen 2\+, which does a discrete Fourier transform optically. The company's press release called it the first in the world. UK startup Lumai had already run a full LLM on optical hardware in April 2026, using 3D free-space optics, and reported about 90% energy savings on Llama 70B-class models.
- **2026-11-18 — Q.ANT demonstrates hybrid LLM inference on photonic NPU at SC26.** At SC26 in Chicago, Q.ANT showed hybrid LLM inference. Some layers of a language model moved from an AMD GPU to its photonic NPU Gen 2\+, which computes a discrete Fourier transform optically. The company's press release called it the world's first. British startup Lumai had already run a full LLM on optical hardware in April 2026.
- **2026-11-18 — other reporting on this date.**
  - The demonstration paired the NPU Gen 2\+ with an AMD Instinct MI210 GPU over PCIe and ran a language model of about one billion parameters. The NPU uses thin-film lithium niobate \(TFLN\) photonic integrated circuits to run discrete Fourier transforms in a single optical pass. These replace the electronic attention-layer calculations. Q.ANT also released an updated SDK with C/Python simulation environments. (2026-11-18) — <https://habr.com/ru/companies/selectel/articles/1109180/>
  - The same details hold on the technical side. The hybrid system offloaded attention layers using optical discrete Fourier transforms \(DFT\) on a ~1B parameter model with an AMD Instinct GPU. It relies on thin-film lithium niobate \(TFLN\) photonics. Q.ANT's C and Python SDK now has native Fourier simulation support. (2026-11-18) — <https://habr.com/ru/companies/selectel/articles/1109180/>

## What changed

Q.ANT moved from basic optical matrix multiplication and non-linear operations to dedicated, native optical discrete Fourier transform hardware. The pipeline moved from standalone optical math blocks to co-processing with electronic accelerators such as AMD Instinct GPUs over PCIe. In transformer layers, optical transforms now replace standard attention calculations, so the work is split between optics and electronics. The SDK gained CPU simulation tooling.

## How to use this

1. Simulate optical discrete Fourier transform operations locally with Q.ANT's open-source SDK in Python or C, before moving to physical photonic hardware.
  — <https://habr.com/ru/companies/selectel/articles/1109180/>
2. Install the Q.ANT NPU Gen 2\+ co-processor in a standard PCIe slot of a server with an AMD Instinct host GPU.
  — <https://habr.com/ru/companies/selectel/articles/1109180/>
3. Split the model: map the Fourier-transformable attention layers to the photonic NPU, and keep the dense and memory-bound layers on the host GPU.
  — <https://habr.com/ru/companies/selectel/articles/1109180/>

## Best practices

- Compare the Fourier-transformed layers with baseline attention in CPU simulation first, so accuracy loss is measured before any physical offload.
  — <https://habr.com/ru/companies/selectel/articles/1109180/>
- Pick models where sequence length is the bottleneck. A single optical Fourier pass should give the largest latency and energy gain over electronic quadratic attention.
  — <https://habr.com/ru/companies/selectel/articles/1109180/>

## Superseded by this

- The claim that photonic processors are limited to basic optical matrix multiplication, with no native single-pass discrete Fourier transform acceleration for generative models.
  — <https://habr.com/ru/companies/selectel/articles/1109180/>

## Still unknown

- Benchmarked inference speedup and power reduction for the NPU Gen 2\+ demo were not disclosed in detail. Lumai's 90% figure is the only number cited.
- Links to technical articles on picmagazine.net and thequantuminsider.com came back as search-engine redirects, not canonical paths. They could not be fetched directly or verified.
- Availability dates, unit pricing and compatibility beyond the AMD Instinct MI210 PCIe testbed are unconfirmed.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/companies/selectel/articles/1109180/ | Фотонные вычисления в ИИ: демонстрация гибридного инференса Q.ANT на SC26 | 2026-11-19 |

## Agent brief {#agent-brief}

- **Subject:** organization:q-ant, thread llm-inference-on-photonic-hardware, 2 dated events 2026-11-18 → 2026-11-18.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
