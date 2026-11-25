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

- Agent cycle: runs a summary → plan → action → reflection loop.
- Frame selection: picks and extracts video frames, then updates the next step from the result.
- Model weights: hosted at `WRHC/EfficientVideoAgent` for evaluation across six video datasets.

The published repository covers multi-GPU evaluation through vLLM rather than an interactive interface. The setup works for reproducible query-driven video evaluation, but practical serving requires a separate inference pipeline.

## Development line

- **2026-03-26 — EVA source and model resources were recorded.** On 2026-03-26, EVA appeared with a GitHub source repository and a Hugging Face model page. Both links mark public access for the project. The dated links alone do not confirm a version, capabilities, evaluation results, or whether either resource was first published that day.

## What changed

2026-03-26 — Official evaluation code and EVA weights are public. The model replaces passive uniform frame sampling with an agent loop that chooses what to inspect and when.

## How to use this

As of 2026-03-26, practitioners should treat EVA as having both a source-code reference and a model-hosting reference, then verify setup and model details directly from those resources before use.

1. Download weights for `WRHC/EfficientVideoAgent` and install the repository dependencies with FFmpeg.
  — <https://github.com/wangruohui/EfficientVideoAgent>
2. Prepare one of the six supported video datasets for evaluation and set the local `video_root` in `DATASET_CONFIG`.
  — <https://github.com/wangruohui/EfficientVideoAgent>
3. Serve the weights with a vLLM OpenAI-compatible endpoint, then set its URL, tokenizer path, and allowed media paths in `eval-eva.py`.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
4. Run the chosen dataset with `eval-eva.py`. Re-run the same command to resume an interrupted run from the cache file.
  — <https://github.com/wangruohui/EfficientVideoAgent>

## Best practices

- Keep `ffprobe` in `PATH` and FFmpeg libraries in `LD_LIBRARY_PATH` because frame extraction runs during evaluation.
  — <https://github.com/wangruohui/EfficientVideoAgent>
- Grant vLLM access to local video files with `--allowed-local-media-path` so the agent can pass extracted frames to the model.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
- Lock `--max-visual-tokens` across runs because exceeding the token budget lowers resolution and drops frames.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
- Do not treat a single run as an exact reproduction because accuracy varies by fractions of a percent even at `temperature=0`.
  — <https://github.com/wangruohui/EfficientVideoAgent>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No dated first-party changelog exists after the initial release. We cannot confirm whether later commits or model updates changed EVA's capabilities.
- Public documentation covers only the benchmark evaluation workflow. We find no confirmed production inference setup, standalone API, or user interface.

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
