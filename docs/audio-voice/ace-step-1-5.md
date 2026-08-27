---
title: "ACE-Step 1.5"
description: "Artifact- and hardware-aware reference for ACE-Step 1.5 music generation, base/SFT/turbo, and XL execution."
---

# ACE-Step 1.5

ACE-Step 1.5 is an open music-generation project with base, SFT, turbo, and XL artifacts. Step count, CFG behavior, memory, and duration limits depend on the selected artifact and runtime mode. Status verified against first-party release, model-card, tutorial, and GPU guidance on **2026-08-27**.

## Current Status

| Surface | Verified state |
|---|---|
| Current repository release | `v0.1.8`, published 2026-05-18 |
| License | MIT on the official project/model surface; verify each downloaded artifact |
| Base 1.5 low-memory claim | Can run below 4 GB in the documented base path; not an XL claim |
| Base/SFT sampling | 50 steps with CFG in the documented table |
| Turbo sampling | 8 steps without CFG in the documented table |
| XL <=12 GB | Not recommended/supported by the official GPU guide |

Do not merge “ACE-Step 1.5 runs under 4 GB” with ACE-Step 1.5 XL requirements. They refer to different artifact paths.

## Artifact Selector

| Artifact | Steps | CFG | Selection rule |
|---|---:|---|---|
| base | 50 | enabled | Baseline quality/control path |
| SFT | 50 | enabled | Select only when its fine-tuned behavior is required |
| turbo | 8 | disabled | Fast path; do not copy base CFG settings |
| XL variants | Version-specific | Version-specific | Use the exact release table and GPU preflight |

Preserve the complete model directory/revision in run receipts. A UI label such as “XL” is insufficient if multiple base/SFT/turbo files are installed.

## GPU and Memory Planning for XL

| Available VRAM | Official guidance boundary |
|---|---|
| 12 GB or less | Do not use XL |
| 12-16 GB | Limited XL path with CPU offload and INT8 |
| 16-20 GB | XL with offload |
| 20 GB or more | Full XL path |
| 24 GB or more | All LM options without offload/quantization according to the guide |

For 12-16 GB, the guide bounds maximum duration at approximately 8 minutes with LM and 10 minutes without LM. Do not restate this as “10 minutes with LM.” Duration, LM state, offload, quantization, and GPU must travel together.

## Development History

| Date | Event | Temporal status |
|---|---|---|
| 2026-02-03 | ACE-Step 1.5 initial release report | Historical foundation |
| 2026-02-04 | Demo availability recovered/reported | Supporting event; not a separate project milestone |
| 2026-04-07 | ACE-Step 1.5 XL reported | Current XL branch foundation |
| 2026-05-18 | Repository `v0.1.8` | Current release at verification time |

The demo recovery belongs as supporting evidence to the initial event, not as a new development branch.

## Reproducible Run Record

```yaml
ace_step_version: 0.1.8
artifact: base-or-sft-or-turbo-or-exact-xl-name
artifact_revision: <immutable-revision>
steps: 50-or-8
cfg_enabled: <true-or-false>
lm_enabled: <true-or-false>
duration_seconds: <integer>
dtype_or_quantization: <exact-value>
cpu_offload: <true-or-false>
gpu: <exact-model-and-vram>
peak_vram: <measured-value>
seed: <integer>
```

Validate a short sample before long-duration generation. If memory is near the hardware limit, reduce artifact size or use the documented offload/INT8 path instead of silently changing multiple controls.

## Community Evidence Boundary

Community quality and memory reports are useful only when they preserve artifact, release, duration, LM state, offload, quantization, steps, and GPU. Two current failure reports provide bounded operational guidance:

- [Issue #1274](https://github.com/ace-step/ACE-Step-1.5/issues/1274) reproduces NaN/Inf latents on a 24 GB Quadro RTX 6000 (Turing) for turbo and XL-turbo. Switching only the main DiT fallback from FP16 to FP32 resolved the reporter's case but increased VRAM; a contributor confirmed that the dtype path needs a code fix. Treat FP32 as a diagnostic workaround until a release explicitly closes the issue.
- [Issue #1271](https://github.com/ace-step/ACE-Step-1.5/issues/1271) isolates `cover_noise_strength=0.2` leaking from Cover/Remix into text-to-music and producing full-duration static. A contributor confirmed the backend path and advised resetting `cover_noise_strength` to `0` before returning to text-to-music until fixed.

## Gotchas

- **Issue:** Applying the below-4-GB base claim to XL -> **Fix:** use the XL VRAM matrix; <=12 GB is not an XL target.
- **Issue:** Enabling CFG for turbo because base uses it -> **Fix:** use 8 steps with CFG disabled for the documented turbo path.
- **Issue:** Saying 12-16 GB supports 10 minutes with LM -> **Fix:** preserve the guide's 8-minute-with-LM versus 10-minute-without-LM distinction.
- **Issue:** Reporting “ACE-Step 1.5” without artifact/release -> **Fix:** record base/SFT/turbo/XL plus exact revision.
- **Issue:** Text-to-music suddenly becomes full-duration static after Cover mode -> **Fix:** inspect the saved run parameters and reset `cover_noise_strength` to `0`; preserve issue #1271 as the version-bound evidence.

## Temporal Status

- **Current:** `v0.1.8` at verification time; artifact-specific step/CFG rules; official XL GPU matrix.
- **Historical:** initial February release and demo recovery.
- **Superseded:** generic early memory claims when applied to XL.
- **Open:** reproducible quality comparison across consumer GPUs.

## Agent Brief

Ask for the exact ACE-Step artifact and GPU before generating a recipe. Retrieve the current release and GPU guide, then keep steps, CFG, LM, duration, quantization, and offload tied to that artifact. Reject any attempt to generalize the base <4 GB claim to XL or to reuse base sampling controls for turbo.

## Sources

- Official repository/releases: https://github.com/ace-step/ACE-Step-1.5/releases
- Official model card: https://huggingface.co/ACE-Step/Ace-Step1.5
- Chinese tutorial: https://ace-step.github.io/ACE-Step-1.5/zh/Tutorial
- Paper: https://arxiv.org/abs/2602.00744
- Pre-Ampere NaN/FP32 fallback report: https://github.com/ace-step/ACE-Step-1.5/issues/1274
- Cover-parameter leakage report: https://github.com/ace-step/ACE-Step-1.5/issues/1271
