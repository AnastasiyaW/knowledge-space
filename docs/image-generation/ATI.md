---
title: "ATI: Any Trajectory Instruction"
description: "ATI adds trajectory-conditioned object, local, and camera motion control to its Wan2.1-based image-to-video workflow; preserve the published model, checkpoint, and localhost editor boundaries."
category: models
tags: [video-generation, trajectory-control, camera-motion, object-motion, wan2.1, bytedance]
aliases: ["Any Trajectory Instruction"]
---

# ATI: Any Trajectory Instruction

**Scope checked: 2026-09-04.** ATI is ByteDance's published trajectory-control extension for image-to-video generation. It represents object, local, and camera movement as trajectories and injects the resulting motion signal into the Wan2.1 image-to-video workflow. The official implementation is a specific Wan2.1-based integration, not a generic control module for every video model.

## What It Controls

ATI uses point trajectories to express several motion intents through one interface:

- **object motion** — trajectories anchored to the subject or local region;
- **local motion** — directed movement for chosen image areas;
- **camera motion** — coordinated paths such as pan and zoom;
- **motion transfer** — extract tracks from a source video and apply them to a new first-frame image.

The result still depends on the base model, first frame, prompt, trajectory placement, and motion speed. A drawn path is an instruction, not a guarantee that occluded or ambiguous parts of an image will remain physically consistent.

## Published Runtime Boundary

The official repository is based on the Wan2.1 implementation. Its installation guide requires the original `Wan2.1-I2V-14B-480P` model, a separate ATI checkpoint, and copying the original VAE, text encoder, and other required components into the ATI checkpoint location. Keep these artifacts and their revisions together in an immutable run record.

Before use, verify:

1. the ATI repository revision and its matching Wan2.1 environment;
2. checkpoint completeness and local paths;
3. the YAML/input format used by the current example or API wrapper;
4. target GPU memory, video length, resolution, and output location;
5. a small known trajectory fixture before a larger render batch.

Community ComfyUI support exists through third-party nodes. Treat it as a separate integration with its own version, security, and output checks; it is not interchangeable proof for the upstream repository.

## Trajectory Editor Safety

The upstream project explicitly instructs operators to run its interactive trajectory editor on localhost. Do not expose that development interface directly to an untrusted network. If a remote workflow is needed, put authentication, a constrained upload surface, per-job isolation, resource limits, and retained job receipts in front of it.

## Acceptance Checks

For each output, inspect whether the intended subject moved, whether static areas stayed stable, whether the requested camera movement occurred, and whether the result produces artifacts at the final playback size. Preserve the source image, trajectory file, prompt, base and ATI revisions, settings, output, and review result. Re-run a bounded fixture after upgrading either ATI or Wan.

The ATI repository is Apache-2.0 licensed, but the Wan base model, checkpoints, and any community wrapper may have separate terms. Verify each artifact's current license and access conditions.

## References

- [ATI official repository](https://github.com/bytedance/ATI)
- [ATI paper](https://arxiv.org/abs/2505.22944)
- [ATI checkpoint collection](https://huggingface.co/bytedance-research/ATI)
- [Community ComfyUI Wan Video Wrapper](https://github.com/kijai/ComfyUI-WanVideoWrapper)
