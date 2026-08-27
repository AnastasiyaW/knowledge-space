---
title: "ComfyUI Flux2Klein Enhancer"
description: "Pinned-workflow reference for reference conditioning and identity/detail enhancement with FLUX.2 Klein in ComfyUI."
---

# ComfyUI Flux2Klein Enhancer

`ComfyUI-Flux2Klein-Enhancer` is a third-party ComfyUI custom-node package for reference conditioning and identity/detail transfer. It targets FLUX.2 Klein 9B behavior and is not an official FLUX model release. Status verified against the project repository on **2026-08-27**.

## Current Status

| Property | Verified state |
|---|---|
| Repository | `capitan01R/ComfyUI-Flux2Klein-Enhancer` |
| Verified default-branch revision | `6804643bff9a20926106427ff08d5b1bd2e49861` |
| License | MIT |
| Primary target | FLUX.2 Klein 9B |
| Reference count | Up to eight references in the current workflow |
| Neutral controls | Exact neutral values are intended as pass-through |
| Independent identity benchmark | Not available in the bounded research pass |

The package grew beyond the two-node form described in the initial news item. Current workflow concepts include reference encoding, `Multi ReferenceLatent`, `Identity Feature Transfer Final`, and optional masks.

## Development History

| Date | Event | Temporal status |
|---|---|---|
| 2026-04-07 | Initial enhancer package/report | Historical foundation |
| 2026-06-24 | Expanded workflow/package reported | Current successor event |
| 2026-07-11 | Verified repository revision date | Current repository snapshot used here |

Keep the original news text unchanged. Attach later package expansion and current repository state as successor nodes.

## Installation and Pinning

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer.git
cd ComfyUI-Flux2Klein-Enhancer
git checkout 6804643bff9a20926106427ff08d5b1bd2e49861
git rev-parse HEAD
```

Restart ComfyUI and load a workflow that matches the pinned revision. Preserve the workflow JSON with the run receipt; node names and sockets may drift across revisions.

## Evaluation Protocol

Run a same-seed comparison:

```yaml
comfyui_revision: <exact-revision>
plugin_revision: 6804643bff9a20926106427ff08d5b1bd2e49861
model: <exact-flux2-klein-artifact>
reference_count: <1-to-8>
reference_order: <ordered-list>
masks: <file-hashes-or-none>
seed: <integer>
dimensions: <width>x<height>
steps: <integer>
enhancer_controls: <all-values>
gpu_and_vram: <exact-device>
```

Compare a baseline workflow and an enhancer workflow while holding model, prompt, seed, steps, dimensions, and sampler fixed. Record identity similarity, unwanted detail transfer, prompt adherence, and peak VRAM. Neutral settings should be tested as an exact pass-through invariant.

## Evidence Boundaries

- The repository proves implementation identity, node surface, target model, and license.
- “No LoRA needed,” exact identity preservation, quality gains, and low-VRAM behavior are author/community claims until independently measured.
- Smaller conditioning models may be recognized by the implementation, but the hook schedules and documented target center on Klein 9B.
- No qualified Chinese community source was retained in the initial bounded pass.

## Community and Issue Evidence

- [Issue #35](https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/35) found that `Identity Feature Transfer Final` returned `NaN` from `IS_CHANGED`, forcing fixed-seed downstream reruns. The owner merged a fix on 2026-06-12. This is a historical bug; revisions after that merge should not inherit the workaround.
- [Issue #41](https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/41) reports identity changes after ComfyUI `v0.28.0` with two masked references. The reporter isolated `zero_unmasked_tokens` and used `focus_only` as a workaround; the issue remained open. Preserve ComfyUI version, mask wiring, preset, and plugin revision when reproducing.
- The exact [community showcase thread](https://www.reddit.com/r/StableDiffusion/comments/1t1mvyh/flux2klein_exact_preservation_no_lora_needed/) is useful for discovering the method, but “exact preservation” remains an author/community claim without an independent metric.

## Gotchas

- **Issue:** Treating the plugin as an official FLUX feature -> **Fix:** identify it as a third-party ComfyUI package and pin its commit.
- **Issue:** Claiming identity preservation from a showcase -> **Fix:** run same-seed baseline/enhancer comparisons with an explicit review metric.
- **Issue:** Loading an old two-node workflow against the expanded package -> **Fix:** match workflow JSON to the exact plugin revision.
- **Issue:** Assuming smaller conditioning support equals full 9B parity -> **Fix:** verify the exact model path and schedules locally.
- **Issue:** Reusing `zero_unmasked_tokens` across ComfyUI versions -> **Fix:** reproduce with the pinned mask/preset setup; `focus_only` is a reported v0.28 workaround, not a universal default.

## Temporal Status

- **Current:** expanded multi-reference workflow at the pinned July 2026 revision.
- **Historical:** initial April two-node description.
- **Reported, not independently verified:** exact preservation, no-LoRA replacement, quality gain, and low-memory performance.

## Agent Brief

Pin the plugin, ComfyUI, workflow JSON, and model before troubleshooting. Separate repository facts from showcase/community efficacy claims. Require a controlled baseline for identity or detail claims. Preserve the initial news as history and attach current package state as the endpoint rather than rewriting it.

## Sources

- Project repository: https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer
- Community discussion lane: https://www.reddit.com/r/StableDiffusion/comments/1t1mvyh/flux2klein_exact_preservation_no_lora_needed/
- Fixed cache-invalidation bug: https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/35
- Open ComfyUI v0.28 mask behavior: https://github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer/issues/41
