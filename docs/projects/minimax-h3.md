---
title: MiniMax H3
category: projects
date: 2026-07-31
tags: [minimax, minimax-h3, project]
aliases: ["MiniMax H3"]
---

# MiniMax H3

**Development line:** `project:minimax-h3` · thread `minimax-h3`  
**Last event:** 2026-07-31 · 1 dated since 2026-07-31 · **Researched:** 2026-09-04 · confidence: high

## What it is

MiniMax H3 is a 33B open-weight audiovisual video base model for creators and developers choosing local 768p generation or an API-backed 2K workflow.

- Inputs: text, first/last frames, or image, video, and audio references.
- Output: synchronized video with native stereo audio; FL2VA covers text/keyframe work and Ref2VA covers multimodal reference work.
- Limit: 4–15 seconds; Context-IR and H3-Regenerate-2K remain hosted in the official full-2K workflow.

## Development line

- **2026-07-31 — MiniMax publishes an official MiniMax H3 blog entry.** MiniMax launched H3 with multimodal context and native-stereo video up to 2K/15 seconds; weights were promised for a later release.

## What changed

- 2026-07-31: MiniMax launched H3 with multimodal context and native-stereo video up to 2K/15 seconds; weights were promised for a later release.
- 2026-08-03: MiniMax opened H3 Base weights, with FL2VA and Ref2VA checkpoints while Context-IR and 2K regeneration stayed in the hosted pipeline.
- 2026-08-10: A linked AMA clarified prompt/workflow guidance and future local-release plans; it was not a new versioned model release.
- 2026-08-27: fal released H3 Max, a post-trained MiniMax H3 derivative offered through fal.

## How to use this

From 2026-07-31, start with the official MiniMax H3 page to evaluate the project. Do not infer features or deployment readiness from early materials alone.

1. For the hosted path, create an API key and POST an application/json request with Bearer authentication to the H3 video-generation endpoint.
  — <https://platform.minimax.io/docs/api-reference/video-generation-v2-create>
2. Choose MiniMax-H3, include one non-empty text item, then add either first/last frames or reference image, video, and audio inputs; the two input modes cannot be mixed in one request.
  — <https://platform.minimax.io/docs/api-reference/video-generation-v2-create>
3. Set H3 resolution to 768P or 2K and duration from 4 to 15 seconds, then poll the task or register a callback for queued, running, succeeded, failed, or cancelled states.
  — <https://platform.minimax.io/docs/api-reference/video-generation-v2-create>
4. For local 768p, download FL2VA for text/first-last-frame work or Ref2VA for multimodal reference work, then serve the matching H3-Base checkpoint with a supported framework.
  — <https://www.minimax.io/news/minimax-h3-open-source>
5. For a hosted post-trained derivative instead of the open Base, use fal's H3 Max through its Playground or API.
  — <https://blog.fal.ai/introducing-h3-max-by-fal/>

## Best practices

- Use Context-IR as a planning/preprocessing stage, or reproduce its structure from the provider prompt guidance, before sending work to H3 Base.
  — <https://www.minimax.io/news/minimax-h3-open-source>
- For first/last-frame work, follow the Base guide's frame-alignment instruction and describe a continuous path to the final frame; keep later shot cut times strictly increasing.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md>
- For full reference, define each Subject, Picture, Video, and Audio label once and preserve its meaning; state whether audio is copied or only referenced.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md>
- Treat local H3 Base output as 768p; use the declared full 2K workflow instead of assuming Context-IR or H3-Regenerate-2K ships with the weights.
  — <https://www.minimax.io/news/minimax-h3-open-source>
- Review the Community License before commercial or hosted deployment: it excludes several territories and requires separate authorization above US$20 million annual revenue.
  — <https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE>

## Superseded by this

- 2026-08-03: the 2026-07-31 state in which MiniMax H3 weights were only planned for release in the coming days.

## Still unknown

- Whether MiniMax-H3-Max on the MiniMax API and H3 Max on fal share the same checkpoint.
- Whether MiniMax released H3-Context-IR, H3-Regenerate-2K, or their sparse-attention implementation for local use.
- Minimum GPU or VRAM requirements for local serving; the SGLang command is an example with four GPUs, not a minimum specification.

## Sources

| source | title | read |
|---|---|---|
| https://www.minimax.io/blog/minimax-h3 | MiniMax H3: An Open Model Breaking the Boundaries Between Tasks and Modalities - MiniMax Research | MiniMax | 2026-09-04 |
| https://www.minimax.io/news/minimax-h3-open-source | Open General Intelligence: MiniMax H3 Is Now Open Source - MiniMax News | MiniMax | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/1vh9rtw/ama_minimax_h3_team_ask_us_anything_about_our/ | AMA: MiniMax H3 Team — Ask us anything about our open video generation model, training, and future plans : r/StableDiffusion | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/video-generation-v2-create | Create Video Generation Task - MiniMax API Docs | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md | docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md · MiniMaxAI/MiniMax-H3 at main | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md | docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md · MiniMaxAI/MiniMax-H3 at main | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE | LICENSE · MiniMaxAI/MiniMax-H3 at main | 2026-09-04 |
| https://blog.fal.ai/introducing-h3-max-by-fal/ | Introducing H3 Max by fal | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:minimax-h3`, thread `minimax-h3`, 1 dated events 2026-07-31 → 2026-07-31.
- **Practical note:** From 2026-07-31, start with the official MiniMax H3 page to evaluate the project. Do not infer features or deployment readiness from early materials alone.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:d336eed43fa2789e79635be365c8a2a0bb09b0d8651d55809dfa1659a5457423 -->
## 2026-09-05 — MiniMax H3 Semantic Bridge adds an adapter for H3's FL2VA text path

MiniMax H3 Semantic Bridge is a ComfyUI conditioning adapter for the standard MiniMax H3 FL2VA text-conditioned workflow. It is a community project, not an official MiniMax or SenseNova release. Ref2VA support was not released because author tests degraded singing and lip-sync.

### Usage and practices

- Install the released custom-node archive under ComfyUI/custom_nodes/. Place MiniMaxH3_SemanticBridge_v1.safetensors under ComfyUI/models/semantic_bridge/, restart ComfyUI, and start from the supplied workflow reference. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)
- Use v1 only with the standard MiniMax H3 FL2VA/text-conditioned route. Do not put it into Ref2VA or another reference-conditioned workflow. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)
- Begin at alpha 0.10 with per-token magnitude matching. Compare native H3 and bridge-enabled output using the same prompt, seed, and generation settings. Treat the published alpha 0.15 comparisons as examples rather than a universal preset. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)
- Keep the author's representation-space cosine measurements separate from video-quality claims. The release says they measure agreement with a teacher-derived representation, not perceptual quality or universal prompt-adherence improvement. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/blob/8c2d9b0edb844d6002864a9addd61458dbe81c22/README.md)

### Additional evidence

- 2026-09-05: The public repository is speach1sdef178/MiniMax-H3-Semantic-Bridge at revision 8c2d9b0edb844d6002864a9addd61458dbe81c22. Public files include the v1 adapter, custom-node archive, workflow examples, checksums, README, research material, NOTICE, and licenses. This is a community project, not an official MiniMax or SenseNova release. [Source](https://huggingface.co/speach1sdef178/MiniMax-H3-Semantic-Bridge/tree/8c2d9b0edb844d6002864a9addd61458dbe81c22)
- 2026-09-05: The author reports that v1 belongs only on the standard MiniMax H3 FL2VA/text-conditioned route. Ref2VA/reference-audio experiments degraded singing and lip-sync, so no Ref2VA node was released. Alpha 0.10 is the author's starting point. The alpha 0.15 A/B examples are qualitative illustrations, not proof of general gains. [Source](https://www.reddit.com/r/StableDiffusion/comments/1w7wtco/i_tried_transferring_semantic_representations/)

### Limits and open questions

- No independent reproduction, standardized human-preference benchmark, or separate third-party performance validation was found for this exact adapter as of 2026-09-05.
- The 5-6M parameter count, representation metrics, training split, and compatibility claims are author-published release claims, not independently audited here.
- Chinese queries found no exact zh-CN announcement, tutorial, or independent reproduction for MiniMax H3 Semantic Bridge. The examined MiniMaxH3 CondBridge Qwen3.5-4B result is a different project and must not be merged into this event.
- We did not download or run the package. Runtime compatibility, artifact integrity beyond the named revision, license interpretation, and practical video gains remain unverified.

<!-- Retained base: 10a35259638c923851e915e3b979bbd355ddaf2b; article blob: 3d4f380ad8d34d47f874ef8a5bfdcd7a04126e47 -->

<!-- live-update:71f37afc1afa7b9771cd1a16db8d14948463f58af1f1b5584133448d4f1ef68b -->
## 2026-11-18 — MiniMax H3 community tools add face-swap, sampling, and node optimizations

Community releases for MiniMax H3 add a four-stage ComfyUI face-swap pipeline, Spectrum v0.2.30 integration, DenoMix tiled-sampler workflows and FastDerope rotary embedding patches.

### Usage and practices

- Clone the four-stage face-swap pipeline and install it as a custom node in the ComfyUI custom\_nodes directory. [Source](https://github.com/neohh/minimax-h3-faceswap-pipeline)
- Install ComfyUI-Spectrum-MiniMax-H3 to get the spectrum schedule nodes and calibrate the attention layers. [Source](https://github.com/xmarre/ComfyUI-Spectrum-MiniMax-H3)
- Load the DenoMix tiled-sampler workflow and checkpoints for high-resolution latent upscaling. [Source](https://hf.co/Deno2026/MiniMax-H3-DenoMix)
- Apply the FastDerope node patch to the rotary positional embedding layer. It speeds up attention processing during frame generation. [Source](https://github.com/tazmannner/ComfyUI-H3-FastDerope)
- Run subject tracking and facial mask generation as a first pass, before the latent composite replacement, so the boundary stays stable. [Source](https://github.com/neohh/minimax-h3-faceswap-pipeline)
- In DenoMix, keep the overlap margins between tiles consistent on high-resolution video frames, so tile boundaries do not show breaks. [Source](https://hf.co/Deno2026/MiniMax-H3-DenoMix)
- In FastDerope, check that the rotary embedding dimension parameters match the exact MiniMax H3 model variant, so attention does not diverge. [Source](https://github.com/tazmannner/ComfyUI-H3-FastDerope)

### Additional evidence

- 2026-11-18: The four-stage face-swap repository splits replacement into segmentation masking, reference feature extraction, latent blending and composite post-refinement. [Source](https://github.com/neohh/minimax-h3-faceswap-pipeline)
- 2026-11-18: ComfyUI-Spectrum-MiniMax-H3 v0.2.30 adds adaptive noise scheduling and parameter sweeping, calibrated for MiniMax H3 attention maps. [Source](https://github.com/xmarre/ComfyUI-Spectrum-MiniMax-H3)
- 2026-11-18: The DenoMix release ships tiled-sampler workflows built to remove seam artifacts in high-resolution latent diffusion passes. [Source](https://hf.co/Deno2026/MiniMax-H3-DenoMix)
- 2026-11-18: The ComfyUI-H3-FastDerope node patches rotary positional embeddings to speed up inference and fix sequence distortion at extended frame counts. [Source](https://github.com/tazmannner/ComfyUI-H3-FastDerope)

### Superseded guidance (retained for history)

- 2026-11-18: Unpatched rotary embedding implementations and un-tiled latent sampling, which caused frame seams and positional drift in long sequences. [Source](https://github.com/tazmannner/ComfyUI-H3-FastDerope)

### Limits and open questions

- Benchmarks for the Turbo multi-GPU execution and the audio retake studio could not be verified from the primary repository documentation.
- Direct links to community discussions on Reddit and forums could not be verified.

<!-- Retained base: 2b6b5eee14d533d859230f73d69fabb93305e572; article blob: c1148c23f3104a2f6a1590eda5a318d2fd4c8c8b -->

<!-- live-update:4946e4366fd8dc73bb2e2865c7f67c91751e9bd6735b3f9a57834850637995ac -->
## 2026-11-21 — MiniMax-H3 ref2va pruned INT8 checkpoint released

Comfy-Org published the pruned INT8 convrot ref2va diffusion model for MiniMax-H3. It generates synchronized video and stereo audio.

### Usage and practices

- Download minimax\_h3\_ref2va\_pruned\_int8\_convrot.safetensors from the Comfy-Org/MiniMax-H3 repository into the ComfyUI models/diffusion\_models directory. [Source](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors)
- Put the MiniMax-H3 text encoder and the dual video and audio VAE checkpoints into their own ComfyUI model directories. [Source](https://huggingface.co/Comfy-Org/MiniMax-H3)
- In ComfyUI, import the reference-to-video workflow JSON, connect the ref2va diffusion loader node, set the sampler steps and resolution, then queue the generation. [Source](https://huggingface.co/Comfy-Org/MiniMax-H3)
- Use the pruned INT8 convrot variant to keep the diffusion model's memory footprint workable on consumer GPUs. The audio stays synchronized. [Source](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors)
- Map both the video VAE node and the stereo audio VAE node in the ComfyUI pipeline, so the output does not come out silent or corrupted. [Source](https://huggingface.co/Comfy-Org/MiniMax-H3)

### Additional evidence

- 2026-11-21: The Comfy-Org MiniMax-H3 repository holds the exact ref2va checkpoint, minimax\_h3\_ref2va\_pruned\_int8\_convrot.safetensors, under diffusion\_models. It uses pruned INT8 convolution-rotation quantization and is packaged for synchronized reference-to-video-audio generation. [Source](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors)

### Superseded guidance (retained for history)

- 2026-11-21: Direct reference-to-video generation needed full-precision weights until the pruned INT8 convolution-rotation checkpoints became available. [Source](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors)

### Limits and open questions

- The upstream primary training repository and the complete training logs from MiniMax/Hailuo remain proprietary. Open weights and quantization wrappers are mainly maintained and repackaged by Comfy-Org and community repositories on Hugging Face.


<!-- Retained base: 220fcf56fb877799e9f79a6a0605e627689377dc; article blob: 788ff9bfb1a78451e5b5c9ba0f2b627eb87d5e88 -->
