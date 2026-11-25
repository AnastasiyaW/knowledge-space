---
title: "Tufazip: tufazip-lossless-neural-compressor — Tufazip Lossless Neural Compressor"
category: "projects"
date: 2026-11-20
tags: ["project", "tufazip", "tufazip-lossless-neural-compressor"]
aliases: ["Tufazip: tufazip-lossless-neural-compressor"]
---

# Tufazip: tufazip-lossless-neural-compressor — Tufazip Lossless Neural Compressor

**Development line:** project:tufazip · thread tufazip-lossless-neural-compressor  
**Last event:** 2026-11-20 · 1 dated since 2026-11-20 · **Researched:** 2026-11-22 · confidence: medium

## What it is

TufaZip is an open-source lossless text compressor for machine learning practitioners and compression researchers. It uses neural sequence modeling alone, with no hybrid heuristic compressor like PPM.

- Prediction: a decoder-only Transformer predicts the next token online.
- Adaptation: per-token backpropagation updates the parameters deterministically.
- Coding: an arithmetic coder does the entropy compression.

It needs roughly 74 GB of memory and multiple days of compute on accelerator clusters to process benchmark corpora. It is an experimental baseline for pure neural prediction, not a general-purpose tool for low-latency archiving.

## Development line

- **2026-11-20 — Tufa Labs releases TufaZip, a single-transformer lossless text compressor.** Tufa Labs released TufaZip, a lossless text compressor in which one transformer model learns during compression. On the enwik9 benchmark (1 GB of English Wikipedia) it compressed the data to 105.4 MB, 13th on the leaderboard. Compression takes about a week and roughly 74 GB of memory.
  - Tufa Labs specified a 12-layer, 163-million-parameter decoder-only Transformer. It starts from an offline-trained 4.33 MB quantized prior model. Weights are updated deterministically on each token by online backpropagation, during both compression and decompression. With arithmetic coding the result on the 1 GB enwik9 benchmark is 105.39 MB. (2026-11-20) — <https://tufalabs.ai/research/tufazip/>

## What changed

A single transformer now keeps adapting its weights while it compresses. It does not use a frozen model or heuristic fallbacks. The result checks pure sequence prediction on a standard benchmark.

## How to use this

1. Start compression from the pre-trained compact base prior model and the token dictionary.
  — <https://tufalabs.ai/research/tufazip/>
2. Stream the input text through the 12-layer Transformer to get next-token probability distributions.
  — <https://tufalabs.ai/research/tufazip/>
3. Encode those distributions into the compressed bitstream with the arithmetic coder.
  — <https://tufalabs.ai/research/tufazip/>
4. Apply per-token deterministic backpropagation online, so the weights update in step during encoding and decoding.
  — <https://tufalabs.ai/research/tufazip/>

## Best practices

- Use high-memory hardware with at least 74 GB of available system memory, so the online model state fits during benchmark runs.
  — <https://tufalabs.ai/research/tufazip/>
- Keep floating-point operations deterministic across encoder and decoder environments, so the weights do not drift during online gradient descent.
  — <https://tufalabs.ai/research/tufazip/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Commit history and a non-redirect code repository URL could not be verified from the first public search results.
- No independent, non-redirect Chinese documentation or community post URL could be fetched to check first-hand.

## Sources

| source | title | read |
|---|---|---|
| https://tufalabs.ai/research/tufazip/ | TufaZip: Lossless Compression with Online Learning Transformers | 2026-11-22 |

## Agent brief {#agent-brief}

- **Subject:** project:tufazip, thread tufazip-lossless-neural-compressor, 1 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
