---
title: OmniStream
category: projects
date: 2026-03-13
tags: [omnistream, omnistream-development, project]
aliases: ["OmniStream"]
---

# OmniStream

**Development line:** `project:omnistream` · thread `omnistream-development`  
**Last event:** 2026-03-13 · 1 dated since 2026-03-13 · **Researched:** 2026-09-05 · confidence: high

## What it is

OmniStream is a 0.3B-parameter DINOv3 ViT-L-derived visual backbone for continuous video feature extraction. It uses causal spatiotemporal attention, 3D-RoPE and a persistent KV cache.

- processes frames online without recomputing prior attention;
- transfers a frozen backbone to perception, reconstruction, VLM and VLA tasks;
- ships as a 1.21 GB F32 Hugging Face checkpoint and an official inference repository.

The public checkpoint is an image-feature extractor. The repository still lists pre-training and VLM/VLA code as unreleased. It is usable now for CUDA feature-extraction experiments, not yet as a turnkey VLM or robot-control stack.

## Development line

- **2026-03-13 — OmniStream was publicly linked through its project, code, and model resources.** On 2026-03-13, links appeared for the OmniStream project page, GitHub source repository, and Hugging Face resource. This gives a dated public reference point for the web, code, and model presence, without fixing a specific version, capability, or release status.

## What changed

2026-03-12 — the technical report (arXiv:2603.12265) was submitted. It specified the unified causal streaming backbone, training across 29 datasets, and the evaluation scope.

2026-03-13 — project materials, code, and the StreamFormer/OmniStream checkpoint were published or updated. The release made the 0.3B F32 feature extractor available. Commits that day updated the repository README and arXiv reference.

2026-03-15 — the repository removed environment-specific DINOv3 paths and bundled DINO-text code. A configurable placeholder replaced the hard-coded local path. This supersedes guidance that assumes the authors' original filesystem layout.

The 13 March step adds two practical limits absent from the event links alone: the released checkpoint is 0.3B parameters, and the repository has not released its pre-training or VLM/VLA code.

## How to use this

From 2026-03-13, use the linked OmniStream project page, source repository, and Hugging Face resource as the starting point for evaluation. Verify the exact model version, license, and usage instructions independently.

1. Clone the official repository, create a Python 3.10 Conda environment, then install the pinned PyTorch 2.6.0 CUDA 12.4 stack and Transformers 4.56.1.
  — <https://github.com/Go2Heart/OmniStream>
2. Load `AutoImageProcessor` and `OmnistreamMultiFrameTransformer` from `StreamFormer/OmniStream`, move both tensors and model to CUDA, call `eval()`, and run inference under `torch.no_grad()`.
  — <https://huggingface.co/StreamFormer/OmniStream>
3. Treat the output as visual features (`last_hidden_state`, `hidden_states`, `pooler_output`, and patch indices); supply an integration layer yourself for a downstream task.
  — <https://github.com/Go2Heart/OmniStream>

## Best practices

- Use the repository’s pinned CUDA/PyTorch and Transformers versions for the documented inference path. The checkpoint is not served by a Hugging Face Inference Provider.
  — <https://github.com/Go2Heart/OmniStream>
- Keep the official `model.py` in the environment. The model card says it is required for the sample feature-extraction workflow.
  — <https://huggingface.co/StreamFormer/OmniStream>
- Do not rely on the former author-local DINOv3 paths. Configure the DINOv3 weights location for your own environment.
  — <https://github.com/Go2Heart/OmniStream/commit/780e5d7d60ea7788e9ee62395dc0d465d02dc873>

## Superseded by this

- 2026-03-15 — environment-specific DINOv3 paths and bundled DINO-text source were removed. Do not reproduce the prior local-path setup.
- 2026-03-15 — do not describe the available implementation as a released end-to-end VLM/VLA stack. Those code releases remain listed as TODO items.

## Still unknown

- The primary sources do not expose a dated Hugging Face checkpoint publication timestamp. The exact time the weights became downloadable cannot be separated from the 2026-03-13 project and code update.
- The project page reports results for VLM and VLA transfers, but public VLM and VLA implementation code remains unreleased. Production readiness for those paths is unverified.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2603.12265 | OmniStream: Mastering Perception, Reconstruction and Action in Continuous Streams | 2026-09-05 |
| https://go2heart.github.io/omnistream/ | OmniStream project page | 2026-09-05 |
| https://github.com/Go2Heart/OmniStream | Go2Heart/OmniStream | 2026-09-05 |
| https://github.com/Go2Heart/OmniStream/commits/main | OmniStream commit history | 2026-09-05 |
| https://github.com/Go2Heart/OmniStream/commit/780e5d7d60ea7788e9ee62395dc0d465d02dc873 | fix: hard code and dino.txt | 2026-09-05 |
| https://huggingface.co/StreamFormer/OmniStream | StreamFormer/OmniStream model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:omnistream`, thread `omnistream-development`, 1 dated events 2026-03-13 → 2026-03-13.
- **Practical note:** From 2026-03-13, use the linked OmniStream project page, source repository, and Hugging Face resource as the starting point for evaluation. Verify the exact model version, license, and usage instructions independently.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.