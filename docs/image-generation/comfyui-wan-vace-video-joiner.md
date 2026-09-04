---
title: ComfyUI Wan VACE Video Joiner: Release-Bound Workflow Contract
description: "A ComfyUI Wan VACE video join is a release-bound community workflow, not a generic transition node; pin its workflow revision, ComfyUI/custom-node/model dependencies, input frame/timestamp/color contracts, generated bridge and loop policy, intermediate artifacts, and visual/audio review before publishing a joined clip."
category: workflows
tags: [comfyui, wan-vace, video, transitions, provenance, review]
aliases: ["ComfyUI Wan VACE Video Joiner", "Wan VACE Video Joiner"]
---

# ComfyUI Wan VACE Video Joiner: Release-Bound Workflow Contract

A Wan VACE join should be treated as a particular ComfyUI workflow release,
not as a generic transition node. The community-maintained
[ComfyUI Wan VACE Video Joiner repository](https://github.com/stuttlepress/ComfyUI-Wan-VACE-Video-Joiner)
publishes workflows that generate bridge frames from context on both sides of
a clip boundary. It also documents version-sensitive dependencies and known
failure modes. That is a useful starting point, not a guarantee that every
pair of source clips will join smoothly.

## Pin the executable workflow

For each run, record:

- workflow file and repository revision, plus every local modification;
- ComfyUI backend and frontend version, custom-node revisions, and their
  installation source;
- exact VACE-compatible model/weight/precision and sampler subgraph used;
- input clips, ordering rule, container/codec, frame count, timestamps, frame
  rate, dimensions, color interpretation, alpha policy, and any resampling;
- transition context, replacement/generation policy, loop policy, seed, and
  queue/run identifiers; and
- intermediate frames/files and their digests, final encode settings, and
  output digest.

The upstream workflow currently identifies Wan 2.1 VACE and Wan 2.2 Fun VACE
as its compatible diffusion-model path. Do not infer that a non-VACE model,
another workflow JSON, or an unpinned ComfyUI installation has the same
contract.

## Treat generated bridge frames as derived content

Record which frames are retained source frames and which are generated,
replaced, blended, interpolated, color-matched, or re-encoded. A transition
that looks continuous may still alter exposure, color, geometry, text, motion,
or factual detail. If looping is requested, evaluate the final-to-first
boundary separately; a loop toggle is not evidence of a seamless loop.

Keep source rights and permitted-edit scope with the clip record. Review audio
timing and continuity independently from visual frames, because visual
alignment does not establish audio correctness.

## Validate the target delivery condition

Run a small representative join in the pinned environment before processing a
batch. Review every boundary at delivery frame rate and resolution for dropped
or repeated frames, ghosting, motion discontinuity, brightness/color shifts,
changed subjects or objects, and encode/container errors. Keep a rerun path
for a single failed boundary rather than replacing a batch without evidence.

If a required dependency, model, input shape, or workflow validation fails,
stop visibly with the captured environment and error. Do not substitute a
cross-fade, different model, changed frame rate, or another node as an
equivalent result.

## Related pages

- [[temporal-tiling]]
- [[tiled-inference]]
- [[diffusion-inference-acceleration]]
- [[flow-matching]]
