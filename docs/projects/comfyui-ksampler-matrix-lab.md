---
title: ComfyUI KSampler Matrix Lab — Repository reference
category: projects
date: 2026-06-05
tags: [comfyui-ksampler-matrix-lab, comfyui_ksampler_matrix_lab, project, repository-reference]
aliases: ["ComfyUI KSampler Matrix Lab"]
---

# ComfyUI KSampler Matrix Lab — Repository reference

**Development line:** `project:comfyui-ksampler-matrix-lab` · thread `repository-reference`  
**Last event:** 2026-06-05 · 1 dated since 2026-06-05 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ComfyUI KSampler Matrix Lab — two ComfyUI nodes for artists and model evaluators: KSampler Matrix Lab compares sampler/scheduler combinations, Model Matrix Lab compares installed checkpoints. Limits: up to 9 sampler slots, 9 scheduler slots and 20 model slots; generation runs sequentially. Verdict: usable for controlled visual tests, but compatibility still depends on the local ComfyUI build, models and custom nodes.

## Development line

- **2026-06-05 — ComfyUI KSampler Matrix Lab repository referenced.** On 2026-06-05, this development line was linked to the GitHub repository for ComfyUI KSampler Matrix Lab. The dated link establishes a public repository reference for the project, but the post contents, repository state, capabilities, and release status have not been researched.

## What changed

2026-06-05 — the extension was available as a custom-node package for labeled sampler/scheduler comparison grids; the creator’s public launch was dated 2026-06-04 and described same-seed, incrementing-seed, metadata-header and error-cell behavior.

## How to use this

As of 2026-06-05, practitioners should inspect the linked repository before treating ComfyUI KSampler Matrix Lab as a usable workflow component; its installation, behavior, and maturity remain unverified.

1. Clone the repository into `ComfyUI/custom_nodes`, then restart ComfyUI.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>
2. Add `KSampler Matrix Lab` or `Model Matrix Lab` from the extension category and connect it to a normal generation workflow.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>
3. Connect the node’s single `IMAGE` output to Preview Image or Save Image; optionally load the included workflow JSON.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>

## Best practices

- Keep prompt, model, latent and seed fixed when comparing sampler and scheduler settings; use increment-per-cell seed only when testing variation as well.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>
- Keep the matrix bounded with `max_combinations`; reduce selected samplers or schedulers before raising the limit.
  — <https://www.runcomfy.com/comfyui-nodes/ComfyUI-KSampler-Matrix-Lab/k-sampler-matrix-lab>
- Leave labels and the run header enabled when results will be reviewed or shared, and inspect error cells when continuation is enabled.
  — <https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The repository has no tagged releases, and the accessible first-party overview does not expose a reliable dated commit-by-commit change log after the initial June 2026 publication.
- No independent runtime test on a current local ComfyUI installation was available; current compatibility is therefore documented rather than verified in execution.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/btitkin/ComfyUI-KSampler-Matrix-Lab | GitHub — btitkin/ComfyUI-KSampler-Matrix-Lab | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1twjm31/comfyui_node_to_compare_multiple_samplers_and/ | ComfyUI node to compare multiple samplers and schedulers at once | 2026-09-05 |
| https://www.runcomfy.com/comfyui-nodes/ComfyUI-KSampler-Matrix-Lab/k-sampler-matrix-lab | KSampler Matrix Lab | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-ksampler-matrix-lab`, thread `repository-reference`, 1 dated events 2026-06-05 → 2026-06-05.
- **Practical note:** As of 2026-06-05, practitioners should inspect the linked repository before treating ComfyUI KSampler Matrix Lab as a usable workflow component; its installation, behavior, and maturity remain unverified.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
