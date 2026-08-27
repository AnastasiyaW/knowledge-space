---
title: "Qwen-Image"
description: "Version-aware reference for Qwen-Image generation, editing, 2511/2512 checkpoints, and the separate Qwen-Image 2.0 service surface."
---

# Qwen-Image

Qwen-Image is a project family with separate generation and editing checkpoints. This page distinguishes open local artifacts from later hosted-product announcements. Status verified against first-party sources on **2026-08-27**.

## Current Artifact Map

| Artifact | First-party status | Use |
|---|---|---|
| Qwen-Image | Released in the official repository on 2025-08-04 | Base text-to-image generation |
| Qwen-Image-Edit | Released on 2025-08-18 | Instruction-based image editing |
| Qwen-Image-Edit-2511 | Weights announced on 2025-12-23 | Later editing checkpoint |
| Qwen-Image-2512 | Weights announced on 2025-12-31 | Later generation checkpoint |
| Qwen-Image 2.0 | Announced on 2026-02-10 through the official blog/Qwen Chat surface | Hosted/current product generation; no open 2.0 weights identified in the official repository |
| Qwen-Image 2.0 Pro | Hosted product/news label observed later in 2026 | Do not treat as an alias for open 2512 weights |

The safe default for a local open generation workflow is the official **2512** example. The safe default for a local open editing workflow is the official **Edit-2511** example. Re-check the repository before assuming Qwen-Image 2.0 is downloadable.

## Development History

| Date | Thread | Event | Temporal status |
|---|---|---|---|
| 2025-08-04 | generation | Initial Qwen-Image release | Superseded by 2512 for current local examples |
| 2025-08-18 | editing | Qwen-Image-Edit release | Superseded by Edit-2511 for current local examples |
| 2025-12-23 | editing | Edit-2511 weights released | Current open editing checkpoint in official examples |
| 2025-12-31 | generation | 2512 weights released | Current open generation checkpoint in official examples |
| 2026-02-10 | generation/product | Qwen-Image 2.0 announced | Current hosted-product branch; open-artifact status unverified |
| 2026-04-26 | generation/product | Qwen-Image 2.0 Pro report observed | Later product event, not evidence of open weights |

Generation and editing are related project branches, not one predecessor chain. Preserve both histories and connect only events inside the same branch when constructing a news graph.

## Practical Use

### Local generation

```bash
git clone https://github.com/QwenLM/Qwen-Image.git
cd Qwen-Image
git rev-parse HEAD
```

Then use the 2512 generation example from that pinned revision. Record the model ID, repository revision, Diffusers/runtime versions, dtype, GPU, seed, dimensions, steps, and any quantization or offload.

### Local editing

Use the Edit-2511 example from the same pinned repository. Keep the source image and edit instruction together in the run record. For multi-image editing, also record input order because positional references can affect interpretation.

### Hosted 2.0

Use the current first-party Qwen Chat/API documentation and name the exact endpoint/model. Do not present hosted latency, limits, or output behavior as properties of the 2512 local checkpoint.

## Runtime and Integration Surface

The official repository records integration paths for Diffusers and references support in LightX2V, vLLM-Omni, and SGLang. These are separate runtimes with different batching, quantization, and API contracts.

For every deployment record:

```yaml
artifact: Qwen-Image-2512-or-Qwen-Image-Edit-2511
source_revision: <40-character-commit>
runtime: <diffusers-or-serving-runtime>
runtime_version: <exact-version>
dtype: <bf16-fp16-fp8-int8-other>
gpu: <exact-model-and-vram>
resolution: <width>x<height>
steps: <integer>
seed: <integer>
```

No current first-party, versioned VRAM/latency matrix was accepted in the bounded research pass. Measure local resource use instead of copying a community number.

## Evidence Boundaries

- The official repository is authoritative for downloadable artifacts and local examples.
- The official 2.0 blog is authoritative for the announcement, but does not by itself prove an open checkpoint.
- Chinese first-party API documentation is useful for hosted editing behavior; it does not prove local 2512 compatibility.
- Community examples are useful for failure discovery, not for artifact identity or universal settings.

## Community Reports

- [Issue #26](https://github.com/QwenLM/Qwen-Image/issues/26) documents an initial Qwen-Image Diffusers run consuming 44.24 GiB and failing on a nominal 48 GB card. Community replies report `enable_model_cpu_offload()` as a working memory reduction with a speed cost; VAE tiling alone still exceeded 50 GB for one reporter. These measurements are from the 2025 base artifact, not 2512/Edit-2511.
- [Issue #54](https://github.com/QwenLM/Qwen-Image/issues/54) compares an official infographic prompt across hosted Qwen, Diffusers, and ComfyUI BF16. Multiple users reported that ComfyUI's 20-step default underperformed the repository's 50-step example; 50 steps improved readability but did not guarantee prompt-perfect text. Diffusers and ComfyUI outputs were not interchangeable even with nominally similar weights.
- The operational lesson is to preserve runtime and step count in comparisons. Do not present a hosted example as a local checkpoint guarantee.

## Gotchas

- **Issue:** Calling every artifact “Qwen-Image 2.0” -> **Fix:** preserve the exact model ID: base, Edit, Edit-2511, 2512, or hosted 2.0/2.0 Pro.
- **Issue:** Assuming a blog or Qwen Chat launch means open weights -> **Fix:** require a first-party repository/model-card artifact before describing 2.0 as locally downloadable.
- **Issue:** Linking editing events as predecessors of generation events -> **Fix:** keep separate `generation` and `editing` development threads.
- **Issue:** Publishing community VRAM or speed as universal -> **Fix:** pin runtime, dtype, quantization, dimensions, steps, and GPU, then measure.
- **Issue:** Comparing a 20-step ComfyUI run with the repository's 50-step Diffusers example -> **Fix:** align runtime controls first and still expect backend-specific output differences.

## Temporal Status

- **Current:** 2512 local generation example; Edit-2511 local editing example; hosted Qwen-Image 2.0 product surface.
- **Superseded but retained:** initial 2025 base generation/edit examples where later official checkpoints exist.
- **Unknown:** availability, license, and local runtime contract of a Qwen-Image 2.0 open checkpoint.

## Agent Brief

Resolve the user's intent to `local generation`, `local editing`, or `hosted 2.0` before recommending anything. For local work, retrieve the current official repository and cite an immutable revision plus exact model ID. For hosted work, cite the current endpoint documentation. Never map “2.0 Pro” onto `2512` without primary evidence. Return old events with their temporal status rather than deleting them.

## Sources

- Official repository: https://github.com/QwenLM/Qwen-Image
- Qwen-Image 2.0 announcement: https://qwen.ai/blog?id=qwen-image-2.0
- Chinese hosted editing documentation: https://docs.qwencloud.com/developer-guides/image-generation/image-editing
- Research paper: https://arxiv.org/abs/2605.10730
- Base-model memory discussion (zh-CN/EN): https://github.com/QwenLM/Qwen-Image/issues/26
- Hosted/Diffusers/ComfyUI reproduction discussion: https://github.com/QwenLM/Qwen-Image/issues/54
