---
title: Modality Forcing — Depth Prediction
category: projects
date: 2026-06-15
tags: [depth-prediction, depth_prediction, modality-forcing, project]
aliases: ["Modality Forcing"]
---

# Modality Forcing — Depth Prediction

**Development line:** `project:modality-forcing` · thread `depth-prediction`  
**Last event:** 2026-06-15 · 1 dated since 2026-06-15 · **Researched:** 2026-09-08 · confidence: medium

## What it is

Modality Forcing is a post-training recipe and released BF16 FluxRGBD checkpoint for people who need one model for text-to-RGB-D, image-to-relative-depth, or depth-to-image work.

- Text-to-RGB, depth, and point cloud generation: joint generation in one pass.
- Image-to-depth: relative depth prediction from an image.
- Depth-to-image: RGB generation from depth and text.

The released checkpoint is flux_rgbd_9b_v2, 12B total with a separate Qwen3-8B encoder; its depth is relative rather than calibrated metric depth. Use it for RGB-D experiments and asset workflows, not metrology or commercial deployment under the public weights license.

## Development line

- **2026-06-15 — Modality Forcing depth-prediction resources were linked.** On 2026-06-15, a dated reference connected Modality Forcing's project site, source repository, Hugging Face Space, and Hugging Face model page. This is a material public reference point for the project's depth-prediction development line, although the supplied links do not establish a specific release, version, or technical result.

## What changed

- 2026-06-11 — arXiv v1 introduced the Modality Forcing post-training recipe: one DiT with independently noised RGB and depth streams for joint RGB-D, image-to-depth, and depth-to-image inference.
- 2026-06-12 — bartduis/modality_forcing made the public flux_rgbd_9b_v2 weights, FLUX.2 autoencoder files, model card, and usage path available in its initial public release.
- 2026-06-15 — the available first-party records date the paper and initial public model artifact to 11–12 June and do not identify a separate technical release on this date.

## How to use this

1. Check the checkpoint and license first: bartduis/modality_forcing is the default model; the released weights are CC BY-NC 4.0.
  — <https://huggingface.co/bartduis/modality_forcing>
2. Clone the repository, use Python 3.10+ and a CUDA GPU with at least 48 GB memory, install exactly one uv CUDA extra that matches the driver, then verify torch.cuda.is_available().
  — <https://github.com/Duisterhof/modality-forcing>
3. Run uv run scripts/joint.py --prompt "..." to write an RGB image, depth map, and colored point cloud to outputs.
  — <https://github.com/Duisterhof/modality-forcing>
4. Use scripts/i2d.py with an image for relative depth, or scripts/d2i.py with a .npy or 16-bit single-channel depth map plus text to generate RGB.
  — <https://github.com/Duisterhof/modality-forcing>
5. Treat depth_raw.npy and the exported cloud as relative-scale output; use the depth map for composition or visualization, not calibrated measurement.
  — <https://github.com/Duisterhof/modality-forcing>

## Best practices

- Pick one driver-compatible PyTorch extra and verify GPU visibility; a bare uv sync omits PyTorch.
  — <https://github.com/Duisterhof/modality-forcing>
- Keep the released checkpoint at its 512-pixel training resolution; avoid non-square local image-to-depth input when stretching would change the geometry.
  — <https://github.com/Duisterhof/modality-forcing>
- Use torch.compile only for repeated local sampling: it has a first-run compilation cost and then reuses cached kernels.
  — <https://github.com/Duisterhof/modality-forcing>
- Treat image-to-depth and depth-to-image depth as relative scale; do not infer metric distances from their raw values or point clouds.
  — <https://github.com/Duisterhof/modality-forcing>
- For custom denoising trajectories, prioritize RGB before depth when depth consistency is the goal; the paper reports better depth quality for that direction.
  — <https://arxiv.org/html/2606.13676v1>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The private text of the 2026-06-15 event is unavailable, so its intended claim cannot be reconstructed as a paper announcement versus an artifact-release reference.
- The current repository README rounds the controlled scaling span to 300M–3B, while arXiv v1 lists 370M–3.3B; neither source explains whether this is rounding or a revision.
- The accuracy claims are from the authors' arXiv v1 evaluation; no independent production, metric-depth, video-consistency, or throughput validation was found.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/html/2606.13676v1 | Modality Forcing for Scalable Spatial Generation (arXiv v1) | 2026-09-08 |
| https://huggingface.co/bartduis/modality_forcing/commit/1da410587ea9f76d3b56602af625cd77b0e650ba | Initial public release · bartduis/modality_forcing at 1da4105 | 2026-09-08 |
| https://huggingface.co/bartduis/modality_forcing | bartduis/modality_forcing · Hugging Face | 2026-09-08 |
| https://github.com/Duisterhof/modality-forcing | Duisterhof/modality-forcing · GitHub | 2026-09-08 |

## Agent brief {#agent-brief}

- **Subject:** `project:modality-forcing`, thread `depth-prediction`, 1 dated events 2026-06-15 → 2026-06-15.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.