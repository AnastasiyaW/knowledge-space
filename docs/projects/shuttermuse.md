---
title: ShutterMuse
category: projects
date: 2026-07-03
tags: [project, shuttermuse]
aliases: ["ShutterMuse"]
---

# ShutterMuse

**Development line:** `project:shuttermuse` · thread `shuttermuse`  
**Last event:** 2026-07-03 · 1 dated since 2026-07-03 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ShutterMuse is a capture-time photography assistant for photographers and portrait subjects.

- Framing assessment: assesses framing.
- Composition-box refinement: refines composition boxes.
- COCO-17 pose guidance: guides portrait poses.

The released checkpoint is 9B parameters in BF16, and the project has no declared source-code license. It suits local research and evaluation, not a production-ready hosted service.

## Development line

- **2026-07-03 — ShutterMuse public project links were shared.** On 2026-07-03, ShutterMuse shared links to a project website, a GitHub repository, and a Hugging Face page. These links establish a public presence across a site, source repository, and model venue. They do not establish a specific release, version, capability, or technical result.

## What changed

- 2026-06-24 — ShutterMuse introduced CaptureGuide-Bench, a 130K-sample development dataset, and a unified MLLM trained with supervised and reinforcement fine-tuning.
- 2026-07-03 — ShutterMuse documentation linked the project page, code, and model. The README dates the code, benchmark, and weight release only to 2026-06, so a distinct July version is unverified.

## How to use this

As of 2026-07-03, treat ShutterMuse as a project with public site, source, and model references. Verify exact capabilities and versions from those sources before use.

1. Clone the repository, create its Python 3.10 Conda environment, and install the declared requirements.
  — <https://github.com/lijayuTnT/ShutterMuse>
2. Prepare the base or merged Qwen-VL checkpoint plus the ShutterMuse LoRA/checkpoint. Leave the LoRA path empty only for a fully merged checkpoint.
  — <https://github.com/lijayuTnT/ShutterMuse>
3. Run quick_start.sh with --side photographer for framing guidance or --side subject for pose guidance. Inspect the JSON prediction and WebP visualization.
  — <https://github.com/lijayuTnT/ShutterMuse>
4. For evaluation, download CaptureGuide-Bench into Benchmark/ and run one official evaluation target at a time.
  — <https://huggingface.co/datasets/ShutterMuse/CaptureGuide-Bench>

## Best practices

- Choose the photographer or subject workflow deliberately: they produce different guidance and require different inputs.
  — <https://github.com/lijayuTnT/ShutterMuse>
- Treat the training scripts as launch templates. Set local model, dataset, GPU, and output paths explicitly before running them.
  — <https://github.com/lijayuTnT/ShutterMuse>
- Pin the repository and weight revisions for experiments. The repository currently has commits but no versioned release.
  — <https://github.com/lijayuTnT/ShutterMuse>
- Confirm rights before commercial deployment or redistribution. The benchmark is research-use and the repository license section remains unfinished.
  — <https://huggingface.co/datasets/ShutterMuse/CaptureGuide-Bench>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No exact changelog or tagged release identifies a model, repository, or benchmark revision released specifically on 2026-07-03. The first-party README dates the asset release only to 2026-06.
- The repository license section says it is still to be added. Commercial and redistribution rights for the code and weights are not established here.
- No hosted inference provider is listed for the model at the observed time.

## Sources

| source | title | read |
|---|---|---|
| https://lijayutnt.github.io/ShutterMuse/ | ShutterMuse: Capture-Time Photography Guidance with MLLMs | 2026-09-05 |
| https://github.com/lijayuTnT/ShutterMuse | GitHub - lijayuTnT/ShutterMuse | 2026-09-05 |
| https://huggingface.co/ShutterMuse/ShutterMuse | ShutterMuse/ShutterMuse · Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2606.25763 | ShutterMuse: Capture-Time Photography Guidance with MLLMs | 2026-09-05 |
| https://huggingface.co/datasets/ShutterMuse/CaptureGuide-Bench | ShutterMuse/CaptureGuide-Bench | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:shuttermuse`, thread `shuttermuse`, 1 dated events 2026-07-03 → 2026-07-03.
- **Practical note:** As of 2026-07-03, practitioners can treat ShutterMuse as a project with public site, source, and model-distribution references, while verifying its exact capabilities and versions from those sources before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
