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

FreeToken is an open-source inference server to run large open Mixture-of-Experts models on consumer PCs, built as an alternative to vLLM and SGLang for local MoE serving.

- OpenAI, Anthropic, and Responses APIs for serving requests.
- CPU–GPU offload, expert cache, and FTW weight format to manage memory.
- CLI, Desktop app, and integrations for coding agents.

Official support requires x86_64, NVIDIA Ampere/RTX 30 or newer, and driver r580+; MoE requires free system RAM for experts.

The project changes quickly, so we test it on each target GPU and model.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-08-19 — GitHub release v0.1.2 shipped with tag `9db1a39`, seven assets, and a fixed PyPI publication. 2026-08-23 — maintainers published an FAQ and roadmap: support targets NVIDIA/x86_64, while macOS, AMD, aarch64, tensor parallelism, vision, and expanded GGUF support remain planned.

## How to use this

As of 2026-08-19, no practitioner workflow change can be supported from the dated links alone; research the project page and repository before relying on FreeToken.

1. Check requirements: Linux x86_64, NVIDIA GPU, driver r580+, and Python 3.10+; then create an environment and install `freetoken[accel]` with uv.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md>
2. Run `ft serve --model <local-path-or-HF-id>`; the server listens on `127.0.0.1:1919` by default.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>
3. Verify the installation with `ft --version` and a request to `/v1/chat/completions`, then connect a compatible client to the OpenAI-compatible API.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/install.md>

## Best practices

- Measure CPU and PCIe bandwidth with `ft bench bw` before choosing backend and offload settings, to calibrate the MoE backend.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>
- Plan free RAM around the size of expert weights for MoE; the FAQ notes about 70 GB for bf16 Qwen3.6-35B-A3B.
  — <https://github.com/FlashML-org/FreeToken/issues/84>
- Do not expose the server to the network without custom configuration: default bind is `127.0.0.1`; verify responses locally first.
  — <https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact feature set and maturity of the Windows Desktop build are not confirmed by primary release assets in this research; official pip install instructions cover Linux.
- The paper's claims on performance and hardware support lack independent benchmarks for any specific model, GPU, or workload.
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
