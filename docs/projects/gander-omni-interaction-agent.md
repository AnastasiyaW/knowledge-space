---
title: "Gander Omni Interaction Agent: gander-omni-interaction-agent — Gander Omni Interaction Agent"
category: "projects"
date: 2026-09-10
tags: ["gander-omni-interaction-agent", "project"]
aliases: ["Gander Omni Interaction Agent: gander-omni-interaction-agent"]
---

# Gander Omni Interaction Agent

**Development line:** project:gander-omni-interaction-agent · thread gander-omni-interaction-agent  
**Last event:** 2026-09-10 · 3 dated since 2026-09-09 · **Researched:** 2026-11-25 · confidence: high

## What it is

Gander Omni Interaction Agent is an Apache-2.0 interaction stack for developers building browser assistants that speak, listen, and see.

- Full-duplex audio: speaks while listening.
- Multimodal perception: continuously receives speech, video, text, and screen or camera input.
- Background execution: delegates longer tasks to a separate reasoning agent.

The documented release profile requires Linux, Conda, CUDA 12.4-compatible NVIDIA drivers, three physical GPUs, MiniCPM-o 4.5, a Gander Thinker/Talker pair, faster-whisper large-v3, and an authenticated Codex-compatible Brain.

We use it as an experimental self-hosted interaction stack, not a drop-in low-resource voice API.

## Development line

- **2026-09-09 — Gander Multi-Modal AI Agent Release.** Tencent Hunyuan and openbmb released Gander as a full-duplex agent. It sees the screen, hears audio, and interacts in real time on MiniCPM-o 4.5. It takes screen, video, and camera feeds, keeps user instructions in memory, and runs long tasks in parallel under Apache 2.0.
- **2026-09-09 — Gander Omni Interaction Agent Release.** Release of Gander, a full-duplex multimodal AI agent that can see screens, videos, and cameras; hear and speak in real-time; and run long tasks in parallel, built on MiniCPM-o 4.5 under Apache 2.0 license.
- **2026-09-09 — other reporting on this date.**
  - The accompanying report gives the release a measurable training and evaluation scope: about 2.7 million training examples; on the report’s 100-scenario Full-Duplex-Bench v3, Gander reports 100.0% timely turn-taking, 8.0% early interruption rate, and strict Pass@1 of 0.400. The report notes that this task-success figure is below the six listed baselines. (2026-09-09) — <https://omni-interaction-gander.github.io/Omni-Interaction-Agent/>
  - The public code release specifies an Apache-2.0 license and separates the streaming Cerebellum, orchestration runtime, and pluggable Back Brain; its release profile uses MiniCPM-o 4.5, matching Gander Thinker/Talker checkpoints, and faster-whisper large-v3. (2026-09-09) — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent>
- **2026-09-10 — Gander Omni Interaction Agent update.** The repository stated that the dataset was still undergoing open-source release and would be made available later; it was not available as part of the code release at that point.

## What changed

Gander provided an open implementation of continuous multimodal perception, full-duplex dialogue, and asynchronous agent execution, with code under Apache-2.0 and a MiniCPM-o 4.5-based Thinker/Talker front end.

## How to use this

1. Provision the documented Linux environment with Conda, a CUDA 12.4-compatible NVIDIA driver, three physical GPUs, and an authenticated Codex-compatible executable that supports app-server --stdio.
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent>
2. Clone the repository, create the Conda environment from environment.yml, and activate the gander environment.
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent>
3. Download MiniCPM-o 4.5, the Gander checkpoint pair, and faster-whisper large-v3; select a matching Thinker and Talker pair.
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent>
4. Copy serve.example.yaml to serve.local.yaml and replace its model, checkpoint, ASR, workspace, and Brain executable paths with absolute local paths.
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent>
5. Run ./scripts/serve.sh --check-config before loading weights, then start the service and verify runtime and ASR readiness through the documented local health endpoints.
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent>

## Best practices

- Keep the documented matching MiniCPM-o 4.5 and Gander Thinker/Talker checkpoints; direct substitution of MiniCPM-o-4\_5-awq is unsupported because the current checkpoint composition and embedding resizing are incompatible with its packed quantized layers.
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent/issues/10>
- For remote browser access, proxy both HTTP and WebSocket routes through HTTPS so browser media permissions and streaming connections work correctly.
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent>
- For extended sessions, update to the sliding-window fix, retain the documented 128-unit context settings, and configure WebSocket keepalive plus upstream proxy or load-balancer timeouts for the intended session duration.
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent/issues/5>

## What practitioners say

- One practitioner reported that tool calls and responses stopped after roughly ten minutes, and later reported a disconnect after roughly fifty minutes; the discussion points to checking the sliding-window update and WebSocket or proxy timeouts rather than assuming a supported fixed session duration. (2026-09-15)
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent/issues/5>
- One practitioner reported a CUDA device-side assertion after replacing the base model with an AWQ variant; the maintainer response says that direct replacement is not supported by the current release. (2026-09-20)
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent/issues/10>

## Superseded by this

- The technical report's statement that Gander was released together with models, code, and data.
  — <https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent>

## Still unknown

- The two reviewed model URLs disagree on the Hugging Face organization spelling: Gander-Omni versus Gander-Omi. The repository installation instructions identify Gander-Omni/Gander, but the model-card contents were not independently retrieved.
- The repository still describes the dataset as pending; a later public dataset release was not verified.
- The documented stack is coupled to a Codex-compatible Back Brain. Other provider support and production operating limits were not independently verified.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent | Gander: Multimodal Duplex Interaction Agent | 2026-11-25 |
| https://omni-interaction-gander.github.io/Omni-Interaction-Agent/ | Gander: 多模态双工交互智能体 | 2026-11-25 |
| https://arxiv.org/abs/2609.08977 | Omni Interaction Agent Technical Report | 2026-11-25 |
| https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent/issues/5 | long-running conversation is not supported · Issue \#5 | 2026-11-25 |
| https://github.com/Omni-Interaction-Gander/Omni-Interaction-Agent/issues/10 | MiniCPM-o-4\_5-awq 推理错误 · Issue \#10 | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:gander-omni-interaction-agent, thread gander-omni-interaction-agent, 3 dated events 2026-09-09 → 2026-09-10.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
