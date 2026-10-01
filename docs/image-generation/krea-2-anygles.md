---
title: Krea 2 Anygles Camera-View Adapter
description: "Krea 2 Anygles re-renders one clear person from a new camera yaw, elevation or distance through a Control-LoRA driven by a SAM 3D Body normal map; it needs its own loader and a gated, pickle-based preparation step. Includes our 80-frame orbit test with an open image-to-3D mesh in place of SAM 3D Body."
category: models
tags: [krea-2, anygles, camera-control, novel-view, control-lora, comfyui, sam-3d-body, normal-map]
aliases: ["krea2-anygles", "Anygles", "Krea 2 camera angle LoRA"]
---

# Krea 2 Anygles Camera-View Adapter

Krea 2 Anygles is a community adapter for Krea 2 Turbo. From one image of one person, it generates the same person and scene from a new camera angle. It pairs a rank-32 Control-LoRA with 4 ComfyUI nodes. The target view is a rendered normal map rather than text prompts alone. We reviewed it on 2026-09-30 against the model card, node README and node code.

We ran the real adapter with an open image-to-3D mesh (TripoSG) in place of the gated SAM 3D Body; the small-sample results are in [Our orbit test](#our-orbit-test).

## What it controls

| Control | Node range | Author demos | Meaning |
|---|---|---|---|
| Yaw | -180 to +180 degrees | full orbit | negative moves the camera left, positive right |
| Elevation | -60 to +60 degrees | -45 to +45 | negative moves the camera down, positive up |
| Distance | 0.6x to 1.8x | 0.78x to 1.35x | below 1 closer, above 1 farther |

- Scope: **one clear human subject.** It does not handle animals, general objects, crowds, or exact 3D reconstruction. The model generates hidden sides and background instead of recovering them.
- Elevation and distance are useful controls rather than calibrated scene reconstruction. Treat the numbers as directions.

## How it works

1. **Camera node.** SAM 3D Body extracts the body mesh, and MoGe estimates camera field of view. The node rotates the mesh around the pelvis and renders a target normal map in the source aspect ratio. It also generates the training camera sentence.
2. **Encode node.** This node routes the image to Qwen3-VL and a clean reference path at max edge 384 px. It then VAE-encodes the full-canvas target normal.
3. **Load LoRA node.** This node loads the LoRA pairs and the projection tensor `transformer.first_control.weight`. Standard loaders omit this tensor and lose spatial control silently.
4. **Model patch node.** This injects normal tokens at the noisy-image input and caches reference K/V once per run.

The weights file `krea2_anygles_rank32.safetensors` takes 229 MB in BF16. It contains 256 rank-32 LoRA pairs across the 32 transformer blocks (attention q, k, v, out, gate, and the MLP) plus the one control projection with shape [6144, 64]. We inspected the file and confirmed the author's published checksum.

### Camera sentence

Training used left-only yaw phrasing. The node converts signed yaw through `left_angle = (-yaw) mod 360`. A right turn of +50 degrees becomes:

```text
Same figure. Move the camera 310 degrees to the left relative to the input view.
```

The node appends elevation and distance clauses only when requested, and passes user text through unchanged. Put scene details in extra text ("soft afternoon light"). Do not write camera instructions that clash with the normal map.

## Settings (author's card and README)

```yaml
inference_base: krea/Krea-2-Turbo      # ComfyUI graph validated with krea2_turbo_int8_convrot
steps: 8
sampler: euler
scheduler: simple
guidance: 0.0 in diffusers / cfg 1.0 in ComfyUI
lora_strength: 1.0                     # node allows 0-2; no other value is documented
reference_max_edge: 384                # px; Qwen3-VL image input on
reference_kv_cache: on
output: source aspect ratio, sides multiple of 16, at most 2 * 1024 * 1024 px
validated_size: 1008x1344
```

For guidance conventions (Krea 0.0 = ComfyUI 1.0) see [[krea-2-prompting]].

## Running it

For ComfyUI, clone the repository into `custom_nodes`, install `requirements.txt`, accept the license to download the SAM 3D Body checkpoint, copy the LoRA into `models/loras`, and load `krea2_anygles_workflow.json`. 

The model card provides a standalone Python workflow:

```bash
python prepare_normal.py --source person.webp --output target_normal.png \
  --yaw 50 --elevation 0 --distance 1.0 \
  --sam3d-root ./sam-3d-body \
  --checkpoint ./checkpoints/sam-3d-body-dinov3/model.ckpt \
  --mhr-model ./checkpoints/sam-3d-body-dinov3/assets/mhr_model.pt

python example.py --source person.webp --normal target_normal.png --output result.webp \
  --yaw 50 --elevation 0 --distance 1.0 --prompt "soft afternoon light" --steps 8 --seed 42
```

### What the normal-preparation step pulls in

Our pre-install code audit showed the diffusion nodes load safetensors files directly without network calls, subprocesses, `eval`, or `exec`. The normal-preparation pipeline carries heavy dependencies:

- two pickle checkpoints loaded through `torch.load(weights_only=False)` and `torch.jit.load`
- a pickle MoGe model
- a runtime `torch.hub` download of DINOv3 code from GitHub
- about 20 extra packages, including pyrender, pytorch-lightning, and MoGe from git
- the gated `facebook/sam-3d-body-dinov3` repository.

The gated repository returned HTTP 403 for us, and we do not unpickle third-party checkpoints in a shared runtime, so we did not use this path.

Run normal preparation in a dedicated container or machine that outputs only `target_normal.png`. Pass that file and the camera sentence to the Encode node so the main ComfyUI environment never touches pickle files.

## Our orbit test

We substituted the mesh generator and retained the rest of the author's pipeline:

- **Mesh:** [TripoSG](https://github.com/VAST-AI-Research/TripoSG) (MIT license, ungated, `.safetensors` weights) run on a [BiRefNet](https://huggingface.co/ZhengPeng7/BiRefNet) person matte in an isolated environment. TripoSG ran with 50 steps, guidance 7.0, and seed 42.
- **Normals:** The author's normal renderer executed unchanged on our mesh using the author's camera sentences. We fixed focal length at 1680 px (SAM 3D Body default without FOV estimation) to avoid the pickle-based MoGe checkpoint.
- **Diffusion:** We ran only Encode, Load LoRA, and Model patch nodes in ComfyUI: fp8 Turbo, 8 steps, euler/simple, cfg 1, strength 1.0, reference edge 384 px, resolution 1008x1344, and one fixed seed.
- **Matrix:** 4 one-person subjects (one identity LoRA subject and three photoreal scenes) across 20 camera angles. This covered a full yaw circle in 22.5-degree steps (16 views), elevation +-20, and distances 0.78 / 1.35, producing 80 frames total.

Face similarity uses OpenCV SFace cosine distance against the source face; values of 0.363 or higher indicate the same identity:

| Signal | Result |
|---|---|
| Person silhouette vs target normal (IoU, median per subject) | 0.83-0.91 (the seated subject fits worst) |
| Face similarity, near-front views (median per subject) | 0.47-0.61 |
| Face similarity at +-90 degrees (profiles) | 0.07-0.53, strongly subject-dependent |
| Back views (about +-135 to 180 degrees) | the detector usually finds no face, as expected |
| Detected faces at or above the same-person line | 43 of 60 |

TripoSG gives a clothed outline. SAM 3D Body generates a bare parametric body mesh, which matches the adapter's training data. Seated poses fit our open mesh worst. These numbers describe this substitute setup, not the original SAM 3D Body pipeline.

## Gotchas

- **Do not load the weights with a standard LoRA loader.** Use the Anygles Load LoRA node. Generic loaders drop `transformer.first_control.weight`, which silently removes view control.
- **Match normal map dimensions to the canvas.** Render normals at the exact output resolution and aspect ratio so spatial steering stays accurate.
- **Crop down to one clear person.** The adapter cannot handle groups or distant figures; crop the frame first.
- **Check identity on rear views.** The model invents unseen angles and backgrounds rather than reconstructing them. Verify face and wardrobe consistency across wide yaw turns.
- **Test quantized checkpoints.** The ComfyUI graph was validated with an int8 ConvRot Turbo checkpoint. Whether fp8 behaves the same is untested, so check the output when switching.
- **Run normal preparation in its own environment.** The preparation scripts unpickle third-party checkpoints and download code at runtime.

## Open questions

- Orbit results using native SAM 3D Body bare-mesh normals instead of clothed meshes.
- Adapter behavior across LoRA strengths other than 1.0.
- Parity between fp8 Turbo and the author's validated int8 ConvRot checkpoint.

## See Also

- [[krea-2-prompting]] - Settings, guidance conventions, and prompt structure for Krea 2
- [[krea-2]] - Krea 2 release milestones
- [[flux-klein-capability-map]] - Variant and runtime verification rules

## Sources

- Model card (settings, ranges, portable usage, license): https://huggingface.co/yijunwang2/krea2-anygles
- ComfyUI nodes, README and workflow: https://github.com/alexw5702-afk/krea2-anygles
- Node widget ranges: https://github.com/alexw5702-afk/krea2-anygles/blob/main/nodes.py
- Pixel budget (`MAX_PIXELS = 2 * 1024 * 1024`): https://github.com/alexw5702-afk/krea2-anygles/blob/main/anygles.py
- Demo Space: https://huggingface.co/spaces/yijunwang2/krea2-anygles
- SAM 3D Body repository: https://github.com/facebookresearch/sam-3d-body
- SAM 3D Body checkpoint (gated): https://huggingface.co/facebook/sam-3d-body-dinov3
- TripoSG (image-to-3D, MIT): https://github.com/VAST-AI-Research/TripoSG and weights https://huggingface.co/VAST-AI/TripoSG
- BiRefNet (matting): https://huggingface.co/ZhengPeng7/BiRefNet
- OpenCV face recognition (SFace, 0.363 cosine threshold): https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html
