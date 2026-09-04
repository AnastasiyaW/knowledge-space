---
title: Tencent — Tencent AI research releases
category: organizations
tags: [ai-research-releases, organization, tencent, tencent_arc]
aliases: ["Tencent"]
---

# Tencent — Tencent AI research releases

**Development line:** `organization:tencent` · thread `ai-research-releases`  
**Events:** 1 dated, 2025-12-29 → 2025-12-29 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Tencent is a technology company for consumer platforms and enterprises using cloud, marketing, payments and digital services. - Consumer and enterprise product lines are separate. - TencentARC’s DSR Suite is an Apache-2.0, Qwen2.5-VL-7B-derived VLM package for reasoning about object geometry and relationships over time in video. - It includes a 50K-QA training set, a 1,484-QA benchmark, a 9B BF16 model and a Geometry Selection Module. Limit: the checked model card lists no deployed inference provider. Verdict: select a named Tencent product for production work; treat DSR Suite as self-hosted research tooling, not as a current Tencent Cloud avatar-service replacement.

## Development line

- **2025-12-29 — Tencent ARC published the DSR Suite model and code repositories.** On 2025-12-29, Tencent ARC made DSR Suite available through a Hugging Face model repository and a linked GitHub source repository. This created identifiable model and code entry points for practitioners to assess the release. The supplied links alone do not establish its capabilities, licensing, or deployment requirements.

## What changed

Tencent development line: - 2023-05-02 — Tencent Cloud’s low-sample digital-human production platform was reported as a self-service avatar workflow; the report said it could use a three-minute speaking video and 100 voice sentences. This is a Tencent Cloud product report, not DSR Suite documentation. - 2025-12-29 — TencentARC DSR Suite entered the line as an open research release: code and weights for dynamic spatial reasoning in video, with DSR-Train, DSR-Bench and GSM on a Qwen2.5-VL-7B base. - Found today in the current project source — the repository dates the paper-and-code release to 2025-12-25 and records CVPR 2026 acceptance on 2026-02-21. This changes the work’s research status, not its availability as a managed Tencent product.

## How to use this

As of 2025-12-29, practitioners evaluating Tencent ARC work should begin with the published DSR Suite model and source repositories, then independently verify its capabilities and licensing before adoption.

1. Choose the named Tencent product line first; Tencent itself is not one developer endpoint, and its public catalog separates consumer services, Tencent Cloud and marketing products.
  — <https://www.tencent.com/what-we-create/>
2. For DSR Suite local inference, follow the model card’s Transformers loader for AutoProcessor and Qwen2_5_VLForConditionalGeneration_Spatial, loading TencentARC/DSR_Suite-Model with device_map="auto".
  — <https://huggingface.co/TencentARC/DSR_Suite-Model>
3. For a reproducible check, download DSR-Bench as benchmark.parquet, set local video and parquet paths in VLMEvalKit, then run its Spatial-Reasoning task.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md>
4. For fine-tuning, create the separate Python 3.11 model environment, install model requirements, obtain video/caption data and optional DSR-Train, convert QA pairs, set the QA, video and Pi3 checkpoint paths, then run train.sh.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/model/README.md>

## Best practices

- Keep data generation and model training in separate environments; the project says their package requirements differ.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md>
- Plan for local hosting of 9B BF16 weights rather than assuming a hosted endpoint; the checked model card listed no inference provider.
  — <https://huggingface.co/TencentARC/DSR_Suite-Model>
- Evaluate with DSR-Bench only after obtaining the referenced videos and setting both local paths; the benchmark parquet does not itself supply a local video record.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md>
- For custom QA generation, remove static scenes before generation and account for API access: the supplied curation scripts require the operator’s own endpoint and token.
  — <https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/data/README.md>

## Superseded by this

- No verified product supersession: the 2025-12-29 DSR Suite release is not documented as a successor to the 2023-05-02 Tencent Cloud low-sample digital-human platform.
- 2026-02-21: the project’s CVPR 2026 acceptance supersedes describing the 2025 paper only as a pre-acceptance release; it does not establish a new managed service.

## Still unknown

- The 2023 Tencent Cloud digital-human report and the 2025 TencentARC DSR Suite release are different products and teams; no checked source establishes a shared API, product lineage or replacement relationship.
- No current first-party public page was verified for access, price, regional availability or support status of the 2023 digital-human platform.
- The checked DSR Suite sources do not state a tested Transformers version, GPU-memory requirement or Tencent Cloud deployment path.

## Sources

| source | title | read |
|---|---|---|
| https://www.tencent.com/who-we-are/ | Who we are - Tencent | 2026-09-04 |
| https://www.tencent.com/what-we-create/ | What we create - Tencent | 2026-09-04 |
| https://m.jiemian.com/article/9312569.html | 腾讯云公布小样本数智人生产平台，花费千元即可自行制作数字人 | 2026-09-04 |
| https://huggingface.co/TencentARC/DSR_Suite-Model | TencentARC/DSR_Suite-Model | 2026-09-04 |
| https://github.com/TencentARC/DSR_Suite | TencentARC/DSR_Suite | 2026-09-04 |
| https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/README.md | DSR_Suite README | 2026-09-04 |
| https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/model/README.md | DSR_Suite model training README | 2026-09-04 |
| https://raw.githubusercontent.com/TencentARC/DSR_Suite/main/data/README.md | DSR_Suite data generation README | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:tencent`, thread `ai-research-releases`, 1 dated events 2025-12-29 → 2025-12-29.
- **Practical note:** As of 2025-12-29, practitioners evaluating Tencent ARC work should begin with the published DSR Suite model and source repositories, then independently verify its capabilities and licensing before adoption.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
