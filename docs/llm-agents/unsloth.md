---
title: "Unsloth"
description: "Artifact-aware reference for Unsloth Core, Studio, Desktop, and version-bound fine-tuning guidance."
---

# Unsloth

Unsloth is a family of local fine-tuning and inference surfaces. Core/library recipes, Studio, and Desktop are related products but not interchangeable runtimes. Status verified against first-party English and Chinese sources on **2026-08-27**.

## Current Surface Map

| Surface | Role | Current boundary |
|---|---|---|
| Unsloth Core/library | Python training and inference integration | Use for script/notebook workflows and pin package plus model recipe |
| Unsloth Studio | Local UI/workflow surface | Do not assume the same install, feature set, or release cadence as Core |
| Unsloth Desktop | Desktop installers for Windows, macOS, and Linux | Introduced in the 2026-08-13 release line; current releases must be checked separately |
| Model-specific guides | Fine-tuning settings and compatibility | Settings apply only to the named model family and guide revision |

The official releases surface showed `v0.1.803-beta` on 2026-08-25. The repository documents CPU and multi-GPU paths across NVIDIA, AMD, Intel, and Mac, but support depth varies by operating system, backend, model, and workflow.

## Development History

| Date | Thread | Event | Temporal status |
|---|---|---|---|
| 2025-08-11 | model-training guides | GPT-OSS fine-tuning guidance reported | Historical; retrieve current guide before use |
| 2026-03-11 | model-training guides | Qwen3.5 fine-tuning guidance reported | Current family guide, settings remain model-size specific |
| 2026-04-08 | local UI | Studio/Gemma-related local workflow report | Historical product branch |
| 2026-08-13 | local UI | Unsloth Desktop introduced | Current product branch |
| 2026-08-25 | release line | `v0.1.803-beta` observed | Current release at verification time |

Model-training guides form one history. Studio/Desktop form a separate local-UI history. Do not make a Studio article the predecessor of an unrelated model recipe.

## Qwen3.5 Fine-Tuning Bounds

The official guide reports approximate bf16 LoRA memory by model size:

| Qwen3.5 size | Reported bf16 LoRA memory |
|---|---:|
| 0.8B | 3 GB |
| 2B | 5 GB |
| 4B | 10 GB |
| 9B | 22 GB |
| 27B | 56 GB |
| 35B-A3B | 74 GB |

The commonly repeated “5 GB” claim belongs specifically to the **2B bf16 LoRA** recipe. It is not a universal Qwen3.5 or Unsloth memory requirement.

The guide requires Transformers v5 for this model family. It also advises against 4-bit QLoRA for Qwen3.5 because its quantization behavior differs from recipes where 4-bit QLoRA is the normal low-memory default.

## Reproducible Run Record

```yaml
unsloth_surface: core-or-studio-or-desktop
unsloth_version: <exact-release-or-package-version>
model_id: <exact-model-and-size>
model_revision: <immutable-revision>
transformers_version: <exact-version>
training_mode: bf16-lora-or-other
quantization: none-or-exact-format
gpu_backend: nvidia-or-amd-or-intel-or-mps-or-cpu
gpu_and_vram: <exact-device>
sequence_length: <integer>
batch_and_accumulation: <values>
measured_peak_memory: <value>
```

Use measured peak memory as the deployment fact. Guide tables are planning bounds, not guarantees across sequence lengths, batch sizes, optimizer state, and offload settings.

## Platform Selection

- Use Core when scripts, notebooks, CI, or exact dependency pinning are required.
- Use Desktop when a local packaged UI is the requirement and its current installer supports the target OS/backend.
- Use Studio only when its current feature surface matches the task; do not call it Desktop.
- Prefer the model-specific guide over a generic community recipe.
- Re-run a minimal training step after any package, Transformers, CUDA/backend, model, or quantization change.

## Community Reports

- [Issue #7506](https://github.com/unslothai/unsloth/issues/7506) records a Qwen3.5-0.8B BF16 training crash on Tesla T4. A community suggestion to switch trainer flags to FP16 did not fully resolve it because the reporter still observed BF16-loaded weights. Treat T4 Qwen3.5 training as an unresolved mixed-dtype compatibility case, not a one-flag fix.
- [Issue #9549](https://github.com/unslothai/unsloth/issues/9549) records Unsloth Studio/Desktop `v0.1.801-beta` on Windows 10 with AMD W7900/W7500 loading a model into system RAM despite VRAM-related options. The report post-dates Desktop launch and remains open; verify the behavior again on the current release before relying on those toggles.
- These reports reinforce that cross-platform support is not backend parity and that UI memory labels are not measured allocation receipts.

## Gotchas

- **Issue:** Repeating “Qwen3.5 trains in 5 GB” without a model size -> **Fix:** bind the claim to 2B bf16 LoRA and record sequence/batch settings.
- **Issue:** Applying generic 4-bit QLoRA guidance to Qwen3.5 -> **Fix:** follow the current family guide; it does not recommend that path.
- **Issue:** Treating Core, Studio, and Desktop as one versioned application -> **Fix:** record the exact surface and its own release/install contract.
- **Issue:** Reading cross-platform support as feature parity -> **Fix:** verify the exact OS, accelerator backend, model, quantization, and workflow.
- **Issue:** Treating `fp16=True` as a proven T4 repair for Qwen3.5 -> **Fix:** reproduce a training step; issue #7506 remained mixed-dtype after that change.

## Temporal Status

- **Current:** Desktop product branch; `v0.1.803-beta` at verification time; Qwen3.5 Transformers v5 and model-size-specific bf16 LoRA guidance.
- **Superseded or revision-sensitive:** older GPT-OSS and early Qwen3.5 recipe copies.
- **Unknown until tested:** exact Desktop hardware/format parity and measured memory for a user's sequence/batch configuration.

## Agent Brief

Resolve the requested surface (`Core`, `Studio`, or `Desktop`) and exact model before giving instructions. Retrieve the current first-party guide in the requested language, pin all versions, and keep reported planning memory separate from measured peak memory. Never generalize the Qwen3.5 2B/5 GB figure or recommend 4-bit QLoRA for that family without newer first-party evidence.

## Sources

- Official repository: https://github.com/unslothai/unsloth
- Official releases: https://github.com/unslothai/unsloth/releases
- English documentation: https://unsloth.ai/docs
- Chinese documentation: https://unsloth.ai/docs/zh/
- T4/Qwen3.5 mixed-dtype report: https://github.com/unslothai/unsloth/issues/7506
- Desktop/Studio system-RAM report: https://github.com/unslothai/unsloth/issues/9549
