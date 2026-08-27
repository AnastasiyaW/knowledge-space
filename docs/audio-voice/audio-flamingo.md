---
title: "Audio Flamingo"
description: "Version-aware reference for Audio Flamingo 3, Music Flamingo, and Audio Flamingo Next understanding checkpoints."
---

# Audio Flamingo

Audio Flamingo is an NVIDIA audio-understanding research family. Audio Flamingo 3 (AF3), Music Flamingo, and Audio Flamingo Next (AF-Next) are related but distinct branches. Status verified against first-party project, paper, repository, and model-card sources on **2026-08-27**.

## Current Family Map

| Branch | Purpose | Current artifact boundary |
|---|---|---|
| Audio Flamingo 3 | General audio-language understanding | Earlier released research branch |
| Music Flamingo | Music-focused understanding/reasoning | Separate music branch; do not treat as an AF3 point release |
| Audio Flamingo Next | Current long-audio understanding family | 8B BF16 Hugging Face checkpoints: instruction, thinking, and captioning variants |

The official `nvidia/audio-flamingo-next-hf` model card is the artifact authority for AF-Next inference. The older `NVIDIA/audio-flamingo` repository predates AF-Next and should not be used to infer all current features or installation details.

## AF-Next Input Contract

| Property | Verified model-card value |
|---|---|
| Checkpoint family | 8B BF16 |
| Variants | instruction, thinking, captioner |
| Audio format | 16 kHz mono |
| Processing window | 30 seconds |
| Maximum documented duration | 1,800 seconds / 30 minutes |
| Runtime surface | Transformers model-card example |
| Hosted inference provider | None shown at verification time |
| License | Non-commercial; inspect the exact model-card license before use |

Long-audio support is implemented through windowed processing. “Supports 30 minutes” does not mean a single unbounded context tensor, real-time streaming, or low-memory inference.

The released AF-Next checkpoint is an audio-understanding model. The broader research project discusses streaming TTS and voice-to-voice capabilities, but those capabilities are **not included in the released Hugging Face checkpoint**.

## Development History

| Date | Thread | Event | Temporal status |
|---|---|---|---|
| 2025-10-27 | general audio language | Audio Flamingo 3 reported | Historical foundation |
| 2025-11-15 | music understanding | Music Flamingo reported | Current separate branch |
| 2026-04-15 | general audio language | Audio Flamingo Next reported | Current successor branch |

AF3 can be a predecessor of AF-Next in the general audio-language thread. Music Flamingo remains a separate project branch because its specialization and artifacts differ.

## Practical Use

Choose the AF-Next variant by output behavior:

- **Instruction checkpoint:** direct instruction-following audio analysis.
- **Thinking checkpoint:** reasoning-oriented tasks where the model-card contract explicitly supports that mode.
- **Captioner:** dense or structured audio captioning.

Normalize input before evaluation:

```yaml
sample_rate_hz: 16000
channels: 1
duration_seconds: <0-to-1800>
checkpoint: nvidia/audio-flamingo-next-hf
checkpoint_revision: <immutable-revision>
variant: instruction-or-thinking-or-captioner
dtype: bfloat16
device: <exact-gpu>
transformers_version: <exact-version>
```

For long recordings, retain time offsets for each 30-second window so answers can be traced back to source audio. Test overlap/aggregation behavior on the target task instead of assuming window boundaries are semantically neutral.

## When to Use

- Audio question answering, captioning, and semantic analysis under the model-card task contract.
- Long recordings where a documented 30-minute windowed path is useful.
- Research evaluation where the non-commercial license is acceptable.

Do not use the released AF-Next checkpoint as proof of streaming speech synthesis, voice conversion, or commercial deployment rights.

## Community Evidence Boundary

No qualified Chinese source or reproducible consumer-hardware memory recipe was accepted in the bounded pass. One exact implementation gap was retained:

- [Issue #104](https://github.com/NVIDIA/audio-flamingo/issues/104) shows `audio-flamingo-3-hf` under Transformers rejecting a multi-turn/two-audio conversation with a 1:1 text/audio-count `ValueError`. The issue is open with no maintainer reply. It concerns AF3, not AF-Next, and makes the high-level “multi-audio dialogue” claim unsafe as a generic Transformers recipe.
- [Issue #106](https://github.com/NVIDIA/audio-flamingo/issues/106) documents unresolved LongAudio dataset-timeline ambiguities (1 second versus 10 ms stitching gaps and out-of-order segments). This affects reproduction of temporal QA results, not ordinary checkpoint inference.

## Gotchas

- **Issue:** Combining AF3, Music Flamingo, and AF-Next results -> **Fix:** name the branch and checkpoint variant in every claim.
- **Issue:** Reading “30-minute support” as streaming or one-shot context -> **Fix:** preserve the documented 30-second windowing contract and test aggregation.
- **Issue:** Claiming TTS/voice-to-voice from the AF-Next HF checkpoint -> **Fix:** restrict checkpoint claims to released audio-understanding capabilities.
- **Issue:** Ignoring the non-commercial license -> **Fix:** inspect and record the exact checkpoint license before product use.
- **Issue:** Assuming multi-audio research results map directly to the AF3 Transformers chat template -> **Fix:** test the exact processor contract; issue #104 reports a current 1:1 mismatch failure.

## Temporal Status

- **Current:** AF-Next 8B BF16 model-card variants and their 16 kHz mono, 30-second-window, 30-minute maximum contract.
- **Historical:** AF3 general-audio branch.
- **Parallel:** Music Flamingo music-understanding branch.
- **Unreleased in the cited checkpoint:** streaming TTS and voice-to-voice features.

## Agent Brief

Resolve `AF3`, `Music Flamingo`, or `AF-Next` before answering. For AF-Next, retrieve the current model card and identify the exact variant. Preserve audio format, duration/windowing, dtype, hardware, revision, and license. Never turn broader research demonstrations into released-checkpoint capabilities, and label community observations separately from first-party artifact facts.

## Sources

- Audio Flamingo repository: https://github.com/NVIDIA/audio-flamingo
- Audio Flamingo 3 project: https://research.nvidia.com/labs/adlr/AF3/
- Audio Flamingo Next checkpoint: https://huggingface.co/nvidia/audio-flamingo-next-hf
- Audio Flamingo Next paper: https://arxiv.org/abs/2604.10905
- AF3 multi-audio Transformers gap: https://github.com/NVIDIA/audio-flamingo/issues/104
- LongAudio timeline-reproduction gap: https://github.com/NVIDIA/audio-flamingo/issues/106
