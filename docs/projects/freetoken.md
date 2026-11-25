---
title: FreeToken
category: projects

tags: [freetoken, freetoken-development, project]
aliases: ["FreeToken"]
---

# FreeToken

**Development line:** `project:freetoken` · thread `freetoken-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: medium

## What it is

FreeToken is an open-source inference server for running large Mixture-of-Experts models on consumer PCs as an alternative to vLLM and SGLang.

- OpenAI, Anthropic, and Responses APIs for client compatibility.
- CPU-GPU offload, expert cache, and FTW weight format to fit models in memory.
- CLI, Desktop app, and coding-agent connections for local workflows.

The official setup requires x86_64, NVIDIA Ampere/RTX 30 or newer, driver r580+, and free system RAM for experts. The project changes rapidly, so test your specific GPU and model before relying on it.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-08-19: GitHub release v0.1.2 shipped under tag `9db1a39` with seven assets and a fixed PyPI publication.
- 2026-08-23: Maintainers published an FAQ and roadmap; official support targets NVIDIA/x86_64, while macOS, AMD, aarch64, tensor parallelism, vision, and expanded GGUF support remain planned.

## How to use this

As of 2026-08-19, no practitioner workflow change can be supported from the dated links alone; research the project page and repository before relying on FreeToken.

1. Check requirements for Linux x86_64, NVIDIA GPU, driver r580+, and Python 3.10+, then create an environment and install `freetoken[accel]` with uv.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md>
2. Run `ft serve --model <local-path-or-HF-id>`; by default the server listens on `127.0.0.1:1919`.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>
3. Verify the installation with `ft --version` and a request to `/v1/chat/completions`, then connect an OpenAI-compatible client.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md>

## Best practices

- Test CPU and PCIe bandwidth with `ft bench bw` before choosing a backend to calibrate MoE offloading.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>
- Plan free RAM around expert weight size for MoE models; for bf16 Qwen3.6-35B-A3B, the FAQ states about 70 GB.
  — <https://github.com/FlashML-org/FreeToken/issues/84>
- Do not expose the server to the network without explicit configuration; default bind is `127.0.0.1`. Confirm the response locally first.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Primary release assets do not confirm the feature set or maturity of the Windows Desktop build; official pip instructions cover Linux.
- Paper claims about performance and hardware support lack independent benchmarks for specific models, GPUs, or workloads.
- event_findings_placeholder

## Sources

| source | title | read |
|---|---|---|
| https://github.com/FlashML-org/FreeToken/releases | FreeToken releases | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken | FlashML-org/FreeToken README | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md | FreeToken installation guide | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md | FreeToken CLI reference | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/issues/84 | FreeToken FAQ | 2026-09-05 |
| https://github.com/FlashML-org/FreeToken/issues/79 | FreeToken Roadmap (2026) | 2026-09-05 |
| https://arxiv.org/abs/2608.16157 | FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:freetoken`, thread `freetoken-development`, 0 dated events - → -.
- **Practical note:** As of 2026-08-19, no practitioner workflow change can be supported from the dated links alone; research the project page and repository before relying on FreeToken.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.