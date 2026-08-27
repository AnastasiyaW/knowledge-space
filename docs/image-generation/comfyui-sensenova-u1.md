---
title: "SenseNova U1 and ComfyUI"
description: "Boundary-aware reference for official SenseNova U1/U1.5 artifacts, official ComfyUI nodes, and the third-party ComfyUI_SenseNova_U1 wrapper."
---

# SenseNova U1 and ComfyUI

SenseNova U1 is an official image-generation/editing family. `smthemex/ComfyUI_SenseNova_U1` is a separate third-party wrapper. Official nodes, official model capabilities, and wrapper capabilities must be attributed independently. Status verified against first-party English/Chinese sources and the wrapper repository on **2026-08-27**.

## Current Artifact Map

| Surface | Verified state |
|---|---|
| Official repository | `OpenSenseNova/SenseNova-U1`, Apache-2.0 |
| Official verified revision | `022fa663d3f1a3c6822ec0b534e336a991bb7b0b` |
| Official ComfyUI nodes | Available through the ComfyUI registry according to the official FAQ |
| Third-party wrapper | `smthemex/ComfyUI_SenseNova_U1`, Apache-2.0 |
| Wrapper verified revision | `35f930a349aa38a94100529fd1ec7dd8b31f9ec9` |
| Wrapper formats | U1.5 preview/formal plus GGUF, INT8, FP8, and BF16 paths described by its current README |
| Older 8-step LoRA path | Struck through in the wrapper README; retain as history, not a current default |

Do not attribute every official U1/U1.5 feature to the third-party wrapper. Do not treat the wrapper's quantized path as evidence that the official full-precision model fits the same hardware.

## Development History

| Date | Thread | Event | Temporal status |
|---|---|---|---|
| 2026-05-05 | third-party wrapper | Initial ComfyUI wrapper report | Historical foundation |
| 2026-05-21 | official project | Full fine-tuning code released | Current official capability |
| 2026-06-19 | wrapper/adapter | Eight-step infographic LoRA report | Superseded/struck-through in current wrapper docs |
| 2026-08-26 | wrapper | Verified current wrapper revision | Current wrapper endpoint |
| 2026-08-27 | official project | Verified current official revision | Current official endpoint |

Official model development and third-party wrapper development are connected by integration, not ownership. Represent them as separate subjects/threads with explicit `integrates_with` links rather than one false predecessor chain.

## Hardware Selection

The official Chinese FAQ reports approximately 36 GB for full BF16 and requires more than 36 GB VRAM for that path. For constrained devices, it recommends lower/balanced GGUF choices.

The same FAQ warns that a full Q6 path on 8 GB is unsafe and can OOM. Do not convert “GGUF available” into “every GGUF tier fits 8 GB.”

```yaml
surface: official-nodes-or-third-party-wrapper
official_revision: 022fa663d3f1a3c6822ec0b534e336a991bb7b0b
wrapper_revision: 35f930a349aa38a94100529fd1ec7dd8b31f9ec9
model: U1-or-exact-U1.5-artifact
format: BF16-or-FP8-or-INT8-or-exact-GGUF
adapter: <exact-hash-or-none>
comfyui_revision: <exact-revision>
gpu_and_vram: <exact-device>
steps: <integer>
resolution: <width>x<height>
peak_vram: <measured-value>
```

## Practical Selection

- Prefer official registry nodes when the official artifact/runtime contract meets the task.
- Use the third-party wrapper only when its exact quantization/model path is required and pin both wrapper and model.
- Use full BF16 only with measured headroom above the documented requirement.
- On 8 GB, start from a documented low/balanced quantization and validate a minimal workflow; do not select full Q6 by name alone.
- For infographic generation, record language, repeated-text failures, background behavior, adapter hash, steps, and resolution.

## Training Boundary

The official project released full fine-tuning code on 2026-05-21. The official FAQ describes LoRA training code as planned, not equivalent to the already released full fine-tuning path. Re-check this status before claiming LoRA training support because it is temporally unstable.

Local and API surfaces can expose different models, defaults, limits, and output behavior. Keep API results out of local workflow benchmarks unless the exact endpoint is the subject.

## Community Evidence Boundary

The older eight-step infographic LoRA report is useful project history but is not a current default: its own wrapper documentation now strikes that path through. Exact wrapper issues add context:

- [Issue #12](https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/12) reports an 18.6 GB `SenseNova-U1-8B-MoT-8step-Q8_0.gguf` edit on a 16 GB NVIDIA card: 4.92 GB GPU allocation was logged and the eight-step prompt took 42.19 seconds, indicating heavy offload/under-utilization. Another reporter measured 37 GB combined GPU/shared memory for a 2K run on RTX 4090 and suggested testing `prefetch_count=0`. These are workflow-specific observations, not a capacity guarantee.
- [Issue #17](https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/17) reports burned-out results for Interleaved/Infographic fine-tunes under Q4 while the same reporter found Q6 acceptable. Preserve the exact GGUF quantization before diagnosing adapter quality.
- A community [U1.5 GGUF model card](https://huggingface.co/realrebelai/SenseNova-U1.5-8B_GGUFs) exists, but it is not an official model card and cannot override the official >36 GB BF16/8 GB Q6 warning.

## Gotchas

- **Issue:** Calling the third-party wrapper “official SenseNova ComfyUI” -> **Fix:** name the repository owner and keep official registry nodes separate.
- **Issue:** Assuming Q6 fits an 8 GB GPU -> **Fix:** follow the official warning and select/test a lower documented quantization.
- **Issue:** Recommending the old eight-step LoRA because a historical post did -> **Fix:** mark it superseded/struck-through and verify the current adapter path.
- **Issue:** Claiming official LoRA training from released full fine-tuning code -> **Fix:** treat them as distinct capabilities and re-check the FAQ.
- **Issue:** Diagnosing infographic quality without the GGUF tier -> **Fix:** record Q4/Q6/Q8 and adapter revision; issue #17 reports materially different results between Q4 and Q6.

## Temporal Status

- **Current:** official U1 repository and registry nodes; current U1.5/quantization wrapper surface; released full fine-tuning code.
- **Superseded but retained:** historical wrapper eight-step infographic LoRA instructions now struck through.
- **Planned/unstable:** official LoRA training-code status.
- **Unsafe generalization:** full Q6 on 8 GB.

## Agent Brief

First resolve official nodes versus `smthemex` wrapper, then U1 versus exact U1.5 artifact and quantization. Pin both repositories when the wrapper is used. Treat historical adapter instructions as superseded when current docs strike them through. Preserve official-versus-community attribution and never promise 8 GB compatibility without an exact measured configuration.

## Sources

- Official repository: https://github.com/OpenSenseNova/SenseNova-U1
- Official Chinese FAQ: https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/FAQ_CN.md
- Third-party wrapper: https://github.com/smthemex/ComfyUI_SenseNova_U1
- Official project surface: https://www.sensenova.cn/
- Paper: https://arxiv.org/abs/2605.12500
- Chinese VRAM/offload report: https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/12
- Q4 versus Q6 artifact report: https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/17
