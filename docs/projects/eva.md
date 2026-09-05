---
title: EVA
category: projects
date: 2026-03-26
tags: [eva, eva-public-resources, project]
aliases: ["EVA"]
---

# EVA

**Development line:** `project:eva` · thread `eva-public-resources`  
**Last event:** 2026-03-26 · 1 dated since 2026-03-26 · **Researched:** 2026-09-05 · confidence: medium

## What it is

EVA (Efficient Video Agent) is a video agent built on Qwen2.5-VL for researchers and engineers.

- Agent loop that runs summary, plan, action, and reflection steps.
- Frame extractor that selects and retrieves video frames by query.
- Planner that adjusts subsequent actions based on observation results.

Weights are available as `WRHC/EfficientVideoAgent`, and the code evaluates on six video datasets. The published code runs evaluation through vLLM across multiple GPUs without a ready user interface. It suits reproducible evaluation of query-driven video understanding, but practical inference requires a separate pipeline around the model.

## Development line

- **2026-03-26 — EVA source code and model weights were published.** On 2026-03-26, EVA linked to a GitHub source repository and a Hugging Face model page. These links mark public access for the project. They do not establish a version, capabilities, evaluation results, or whether either resource was first published that day.

## What changed

2026-03-26 — Official evaluation code and weights for EVA were published. The system switched from passive uniform frame sampling to an agent loop that decides what to inspect and when.

## How to use this

As of 2026-03-26, verify setup and model details directly from the repository and model page before use.

1. Download the `WRHC/EfficientVideoAgent` weights and install repository dependencies with FFmpeg.
  — <https://github.com/wangruohui/EfficientVideoAgent>
2. Prepare one of the six supported video datasets for evaluation and set the local `video_root` in `DATASET_CONFIG`.
  — <https://github.com/wangruohui/EfficientVideoAgent>
3. Serve the weights through a vLLM OpenAI-compatible endpoint, then set its URL, tokenizer path, and allowed media paths in `eval-eva.py`.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
4. Run the target dataset with `eval-eva.py`. For interrupted runs, rerun the same command to resume from the cache file.
  — <https://github.com/wangruohui/EfficientVideoAgent>

## Best practices

- Keep `ffprobe` in `PATH` and FFmpeg libraries in `LD_LIBRARY_PATH` so standard frame extraction works during evaluation.
  — <https://github.com/wangruohui/EfficientVideoAgent>
- Verify vLLM access to local videos through `--allowed-local-media-path`, or the agent cannot pass extracted frames to the model.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
- Fix `--max-visual-tokens` across runs. Exceeding the visual token budget reduces resolution and frame count, which skews comparisons.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
- Do not treat a single run as an exact reproduction. The authors report final accuracy varies by fractions of a percent even at `temperature=0`.
  — <https://github.com/wangruohui/EfficientVideoAgent>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No dated first-party changelog exists after the initial release. We cannot confirm whether subsequent repository or model updates changed EVA capabilities.
- Public documentation covers only the benchmark evaluation workflow. No supported production inference, standalone API, or user interface is confirmed.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/wangruohui/EfficientVideoAgent | EVA: Efficient Reinforcement Learning for End-to-End Video Agent — official evaluation code | 2026-09-05 |
| https://huggingface.co/WRHC/EfficientVideoAgent | WRHC/EfficientVideoAgent — model card and weights | 2026-09-05 |
| https://arxiv.org/abs/2603.22918 | EVA: Efficient Reinforcement Learning for End-to-End Video Agent | 2026-09-05 |
| https://huggingface.co/papers/2603.22918 | Paper page — EVA: Efficient Reinforcement Learning for End-to-End Video Agent | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:eva`, thread `eva-public-resources`, 1 dated events 2026-03-26 → 2026-03-26.
- **Practical note:** As of 2026-03-26, practitioners should treat EVA as having both a source-code reference and a model-hosting reference, then verify setup and model details directly from those resources before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
