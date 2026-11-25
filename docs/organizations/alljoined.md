---
title: "Alljoined: alljoined-bci-eeg-research — Alljoined Bci Eeg Research"
category: "organizations"
date: 2026-11-20
tags: ["alljoined", "alljoined-bci-eeg-research", "organization"]
aliases: ["Alljoined: alljoined-bci-eeg-research"]
---

# Alljoined: alljoined-bci-eeg-research — Alljoined Bci Eeg Research

Alljoined is an open research project on non-invasive EEG decoding, an alternative to Neuralink and lab fMRI image pipelines.

**Development line:** organization:alljoined · thread alljoined-bci-eeg-research  
**Last event:** 2026-11-20 · 1 dated since 2026-11-20 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Alljoined is a brain-computer interface research project. It builds open non-invasive neural decoding models and datasets for researchers and consumer neurotech developers. It competes with invasive neural interfaces like Neuralink and with laboratory fMRI-to-image pipelines.

Abilities:

- Reconstruct seen images from non-invasive EEG signals with the ENIGMA multi-subject model
- Adapt visual decoding to unseen subjects with a brief calibration protocol
- Map EEG signals to visual latent representations with a unified spatio-temporal backbone and subject alignment layers
- Train and test decoding models on large consumer-grade EEG data, including the Alljoined-1.6M image-response dataset and the NOVA emotion dataset

Limit: decoding is evaluated mainly on 32-channel wet-electrode EEG setups and needs at least fifteen minutes of calibration per user. Spatial resolution is lower than with invasive cortical arrays or functional MRI.

Conclusion: multi-subject pre-training and lightweight architectures give semantic visual decoding from non-invasive EEG. They need neither hours of single-subject training nor large compute clusters.

## Development line

- **2026-11-20 — Alljoined advances non-invasive EEG brain-computer interface work.** Alljoined is developing non-invasive EEG-based brain-computer interfaces. Its ENIGMA model recognizes what a person sees from brain signals and adapts to new users quickly. The team built the Alljoined-1.6M dataset of over 1.6 million EEG brain responses to images. It is now exploring emotion and state detection from brain activity.
  - The ENIGMA \(EEG Neural Image Generator for Multi-subject Applications\) decoding model cuts user calibration to 15 minutes by learning a shared visual representation across subjects. It uses about 120 times fewer trainable parameters than prior state-of-the-art models, through a unified spatio-temporal backbone with latent alignment. It is benchmarked on the 20-subject, 32-channel Alljoined-1.6M dataset. The NOVA video-evoked EEG emotion decoding dataset comes with it. (2026-11-20) — <https://www.alljoined.com/>

## What changed

Work moved from collecting large EEG benchmark datasets to training lightweight multi-subject foundation models. First came the Alljoined-1.6M dataset, gathered across many participants with consumer-grade wet-electrode hardware. Then came affective neural decoding with the NOVA dataset. The architecture then moved from heavy individual-specific decoding pipelines to the unified ENIGMA spatio-temporal model. That cut the parameter count and shortened subject calibration.

## How to use this

1. Record multi-channel EEG from subjects viewing visual stimuli. Use consumer-grade or laboratory hardware, such as a 32-channel wet-electrode cap.
  — <https://www.alljoined.com/>
2. Collect about 15 minutes of EEG calibration data per user, so ENIGMA's shared multi-subject representation adapts to that person's brain patterns.
  — <https://www.alljoined.com/>
3. Pass the raw EEG through the spatio-temporal backbone and the multi-subject latent alignment layers. This projects the signals into the visual latent space for image reconstruction.
  — <https://www.alljoined.com/>

## Best practices

- Pre-train decoding backbones across a pool of subjects to learn general visual representations. Do not train separate individual models from scratch.
  — <https://www.alljoined.com/>
- Use lightweight unified spatio-temporal backbones with latent alignment layers, so the parameter count stays low and inference runs locally without large compute clusters.
  — <https://www.alljoined.com/>

## Superseded by this

- The older assumption that non-invasive EEG visual decoding needs hours of single-subject calibration and bulky, high-parameter individual models.
  — <https://www.alljoined.com/>

## Still unknown

- Exact publication paths and identifiers on arXiv, NeurIPS, OpenReview and Hugging Face could not be verified without direct URL inspection tools, so they are left out of the citations.
- Commercial availability, licensing and pricing of proprietary hardware or hosted inference endpoints for Alljoined tools are not documented in the available summaries.

## Sources

| source | title | read |
|---|---|---|
| https://www.alljoined.com/ | Alljoined: Non-invasive EEG Brain-Computer Interfaces | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** organization:alljoined, thread alljoined-bci-eeg-research, 1 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** medium. The dated entries under "Superseded by this" say what is obsolete.
