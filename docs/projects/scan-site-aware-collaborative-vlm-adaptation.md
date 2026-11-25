---
title: "Scan Site Aware Collaborative Vlm Adaptation: scan-site-aware-collaborative-vlm-adaptation-research — Scan Site Aware Collaborative Vlm Adaptation Research"
category: "projects"
date: 2026-11-18
tags: ["project", "scan-site-aware-collaborative-vlm-adaptation", "scan-site-aware-collaborative-vlm-adaptation-research"]
aliases: ["Scan Site Aware Collaborative Vlm Adaptation: scan-site-aware-collaborative-vlm-adaptation-research"]
---

# Scan Site Aware Collaborative Vlm Adaptation: scan-site-aware-collaborative-vlm-adaptation-research — Scan Site Aware Collaborative Vlm Adaptation Research

SCAN adapts 3D medical vision-language models across hospitals without sharing brain MRI scans or retraining them.

**Development line:** project:scan-site-aware-collaborative-vlm-adaptation · thread scan-site-aware-collaborative-vlm-adaptation-research  
**Last event:** 2026-11-18 · 2 dated since 2026-11-18 · **Researched:** 2026-11-19 · confidence: high

## What it is

SCAN is a site-aware collaborative framework for adapting three-dimensional medical vision-language models across distributed clinical institutions. Patient brain MRI scans are not centralized, and nothing is retrained end to end. It does three things:

- Local class prototypes: built without training from hospital MRI scans, using a frozen foundation vision-language encoder.
- Site summaries: norm-bounded feature sums and sample counts, with calibrated differential privacy noise, so privacy is kept when sites share them.
- Cross-site adaptation: zero-shot and few-shot classification of Alzheimer's disease, epilepsy and stroke.

Performance depends on cross-site feature alignment. It also depends on calibrating the differential privacy noise multiplier against the prototype feature scale. For neuroimaging consortia with privacy limits, it is a practical alternative to centralized pretraining and heavy federated fine-tuning.

## Development line

- **2026-11-18 — SCAN framework proposed for privacy-preserving collaborative adaptation of brain MRI vision-language models.** An arXiv preprint (2611.21955) presented SCAN on 2026-11-18. It lets hospitals adapt a 3D medical vision-language model for neurological disease classification without sharing patient scans or retraining. The authors used 7,641 scans from 67 sites. They report gains in epilepsy and Alzheimer's AUC from local training-free prototypes. They also report near-chance membership attacks under differential privacy with epsilon 4.
- **2026-11-18 — SCAN framework proposed for privacy-preserving collaborative adaptation of medical vision-language models.** Researchers posted an arXiv preprint (2611.21955) introducing SCAN. It is a site-aware collaborative framework that lets hospitals adapt a 3D medical vision-language model for neurological disease classification without sharing patient scans or retraining. Reported results: improved local AUCs at unseen sites, and differential privacy (epsilon = 4) with limited accuracy loss at existing sites.
- **2026-11-18 — other reporting on this date.**
  - The preprint authors (Dhinagar et al.) state that the 7,641 brain MRI scans come from 67 sites across 12 countries. The adaptation is training-free prototype generation from frozen 3D vision-language representations. It pairs norm-bounded feature sums with count perturbation under calibrated differential privacy. (2026-11-18) — <https://arxiv.org/abs/2611.21955>
  - The paper covers several neurological conditions: Alzheimer's disease, epilepsy and stroke. Aggregating site prototypes improves zero-shot and few-shot classification at unseen hospital sites. It needs no raw imaging and no multi-round federated optimization. (2026-11-18) — <https://arxiv.org/abs/2611.21955>

## What changed

The project began as an academic proposal. It targets privacy barriers and scanner heterogeneity in collaborative neuroimaging. It sets up a training-free prototype sharing design: differentially private class prototype aggregation replaces raw brain MRI transfer between clinical sites. It grew from an initial multi-site evaluation across international cohorts toward standardized, privacy-preserving evaluation of medical foundation models.

## How to use this

1. At each hospital site, extract 3D brain MRI representations locally with a shared frozen medical vision-language backbone. Raw volumetric imaging stays on site.
  — <https://arxiv.org/abs/2611.21955>
2. Compute local class prototypes: normalized feature sums and patient counts for each neurological condition category.
  — <https://arxiv.org/abs/2611.21955>
3. Add calibrated differential privacy noise to the norm-bounded prototype vectors. Then broadcast the differentially private site summaries to the collaborating institutions.
  — <https://arxiv.org/abs/2611.21955>
4. Aggregate the cross-site prototype summaries to classify neurological pathology at local or unseen scanner sites, without backpropagation.
  — <https://arxiv.org/abs/2611.21955>

## Best practices

- Bound the prototype vector norms before adding noise, so the differential privacy guarantee holds and feature distortion stays low.
  — <https://arxiv.org/abs/2611.21955>
- Keep the exact, unnoised local prototypes for predictions inside the institution. Use the privatized aggregated prototypes only for cross-site generalization.
  — <https://arxiv.org/abs/2611.21955>

## Superseded by this

- Pooling raw data centrally, or running iterative federated backpropagation, to adapt medical 3D foundation models across heterogeneous hospital sites.
  — <https://arxiv.org/abs/2611.21955>

## Still unknown

- The URL of an open-source code repository, or a software library release, for SCAN. The preprint abstract and the search index metadata do not give one.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2611.21955 | SCAN: Site-Aware Collaborative Privacy-Preserving Adaptation of Vision-Language Models for Neurological Disease Classification | 2026-11-19 |

## Agent brief {#agent-brief}

- **Subject:** project:scan-site-aware-collaborative-vlm-adaptation, thread scan-site-aware-collaborative-vlm-adaptation-research, 2 dated events 2026-11-18 → 2026-11-18.
- **Practical note:** the usage and practice sections above carry their sources and limits.
- **Confidence:** high. The dated "Superseded by this" entries above are the authority on what is obsolete.
