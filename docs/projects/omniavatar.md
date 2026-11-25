---
title: OmniAvatar — Public release and demo availability
category: projects
date: 2025-08-05
tags: [omniavatar, project, public-release-and-demo]
aliases: ["OmniAvatar"]
---

# OmniAvatar — Public release and demo availability

**Development line:** `project:omniavatar` · thread `public-release-and-demo`  
**Last event:** 2025-08-05 · 2 dated since 2025-07-04 · **Researched:** 2026-09-04 · confidence: high

## What it is

OmniAvatar is an open research system for talking avatar video generation from an image, audio, and text prompt.

- Lip-sync to speech audio.
- Facial expressions and body motion matched to audio.
- Text control over character action, background, and emotion.

The models are LoRA and audio-condition checkpoints over Wan2.1 T2V in 14B and 1.3B variants. Output resolution is limited to 480p. For local experiments, this is a working Wan2.1 stack. The public Space is third-party, so we do not rely on it as the only launch path.

## Development line

- **2025-07-04 — OmniAvatar public project and source repository were linked.** The official repository dates the release of these weights to 2025-07-02.
- **2025-08-05 — OmniAvatar Hugging Face Space was linked.** On 2025-08-05, a Hugging Face Space named OmniAvatar appeared and referenced the earlier July project announcement. This adds a hosted demo surface, but the links alone do not establish its exact functionality, availability, or relation to a specific repository revision.

## What changed

2025-07-04 — the public project included code, weights, and the 1.3B variant for Wan2.1. The official repository dates the release of these weights to 2025-07-02. 2025-08-05 — the third-party Hugging Face Space alexnasa/OmniAvatar appeared. On 2025-08-06, the OmniAvatar author team publicly confirmed the demo was successful, but it did not become an official inference API. 2025-06-23 — the OmniAvatar paper was published (arXiv:2506.18866). 2025-06-24 — the authors released inference code and initial weights.

## How to use this

As of 2025-08-05, practitioners could locate OmniAvatar through its public repository and the linked Hugging Face Space; they should validate the current repository revision, Space behavior, and usage instructions before relying on either.

1. Clone the repository and install the pinned dependencies: PyTorch 2.4.0 with CUDA 12.4 and requirements.txt.
  — <https://github.com/Omni-Avatar/OmniAvatar>
2. Download compatible Wan2.1 T2V, the official OmniAvatar LoRA/audio-condition checkpoint, and wav2vec2-base-960h into the pretrained_models structure.
  — <https://huggingface.co/OmniAvatar/OmniAvatar-14B>
3. Prepare the input string formatted as [prompt]@@[img_path]@@[audio_path] and run scripts/inference.py with the 14B or 1.3B configuration.
  — <https://github.com/Omni-Avatar/OmniAvatar>
4. Open the Space for a brief preliminary check, but expect intermittent availability and replicate any critical result locally.
  — <https://huggingface.co/spaces/alexnasa/OmniAvatar>

## Best practices

- Start with 480p and prompt/audio CFG in the 4–6 range; increase audio CFG if lip-sync is not stable enough.
  — <https://github.com/Omni-Avatar/OmniAvatar>
- Compose the prompt from the first-frame description, person behavior, and background as needed.
  — <https://github.com/Omni-Avatar/OmniAvatar>
- Plan VRAM ahead for 14B: the authors report 36 GB without memory management, 21 GB with 7B persistent parameters, and 8 GB with zero persistent parameters on a single GPU.
  — <https://github.com/Omni-Avatar/OmniAvatar>
- Do not use the Space as a production endpoint: user discussions report blank screens and issues during local cloning; run official code when reproducibility is required.
  — <https://huggingface.co/spaces/alexnasa/OmniAvatar/discussions/1>

## Superseded by this

- 2025-06-24 — the paper-only or examples-only status is obsolete: the authors released inference code and weights.
- 2025-07-02 — the 14B-only status is obsolete: the authors released OmniAvatar weights for Wan2.1 T2V-1.3B.

## Still unknown

- The response schema does not contain event_findings and new_events fields; their confirmed facts sit in what_changed rather than separate structured objects.
- Space SLA and stable interactive uptime remain unconfirmed: the page shows Running on Zero, and later user messages report a blank screen.
- The official repository sets no production API, commercial support, or complete set of verified GPU configurations.

## Sources

| source | title | read |
|---|---|---|
| https://omni-avatar.github.io/ | OmniAvatar: Efficient Audio-Driven Avatar Video Generation with Adaptive Body Animation | 2026-09-05 |
| https://github.com/Omni-Avatar/OmniAvatar | Omni-Avatar/OmniAvatar | 2026-09-05 |
| https://huggingface.co/OmniAvatar/OmniAvatar-14B | OmniAvatar/OmniAvatar-14B | 2026-09-05 |
| https://huggingface.co/spaces/alexnasa/OmniAvatar | alexnasa/OmniAvatar | 2026-09-05 |
| https://huggingface.co/spaces/alexnasa/OmniAvatar/discussions/1 | alexnasa/OmniAvatar discussion: Is it working? | 2026-09-05 |
| https://huggingface.co/spaces/alexnasa/OmniAvatar/discussions/2 | alexnasa/OmniAvatar discussion: It works. Very excellent Demo Space. | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:omniavatar`, thread `public-release-and-demo`, 2 dated events 2025-07-04 → 2025-08-05.
- **Practical note:** As of 2025-08-05, practitioners could locate OmniAvatar through its public repository and the linked Hugging Face Space; they should validate the current repository revision, Space behavior, and usage instructions before relying on either.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.