---
title: Krea 2 Anygles Camera-View Adapter
description: "Krea 2 Anygles re-renders one clear person from a new camera yaw, elevation or distance through a Control-LoRA driven by a SAM 3D Body normal map; it needs its own loader and a gated, pickle-based preparation step. Includes our 80-frame orbit test with an open image-to-3D mesh in place of SAM 3D Body."
category: models
tags: [krea-2, anygles, camera-control, novel-view, control-lora, comfyui, sam-3d-body, normal-map]
aliases: ["krea2-anygles", "Anygles", "Krea 2 camera angle LoRA"]
---

# Krea 2 Anygles Camera-View Adapter

Community adapter for Krea 2 Turbo: from one image of one person it generates the same person and scene from a new camera position. A rank-32 Control-LoRA plus 4 ComfyUI nodes; the target view is given as a rendered normal map, not only as words. Reviewed 2026-09-30 against the model card, node README and node code.

> **Status:** tested by us with the real adapter, but with a substitute normal source: an open image-to-3D mesh (TripoSG) instead of the gated SAM 3D Body. See [Our orbit test](#our-orbit-test). Numbers are small-sample.

## What it controls

| Control | Node range | Author demos | Meaning |
|---|---|---|---|
| Yaw | -180 to +180 degrees | full orbit | negative moves the camera left, positive right |
| Elevation | -60 to +60 degrees | -45 to +45 | negative moves the camera down, positive up |
| Distance | 0.6x to 1.8x | 0.78x to 1.35x | below 1 closer, above 1 farther |

- Scope: **one clear human subject.** Not for animals, general objects, crowds, or exact 3D reconstruction. Hidden sides and background are generated, not recovered.
- The card calls elevation and distance "useful controls, not calibrated scene reconstruction"; treat the numbers as directions.

## How it works

1. **Camera node.** SAM 3D Body recovers the body mesh; MoGe estimates the camera field of view. The mesh is rotated around the pelvis and rendered as a target normal map inside the source-aspect-ratio canvas. The node also writes the camera sentence the model was trained on.
2. **Encode node.** Sends the photo to Qwen3-VL and to a clean reference path (max edge 384 px), and VAE-encodes the full-canvas target normal.
3. **Load LoRA node.** Applies the LoRA pairs **and** the extra projection tensor `transformer.first_control.weight`. An ordinary LoRA loader skips that tensor, so the spatial control is silently lost.
4. **Model patch node.** Injects the normal tokens at the noisy-image input and caches the reference K/V once per run.

The weights file `krea2_anygles_rank32.safetensors` is 229 MB in BF16: 256 rank-32 LoRA pairs across the 32 transformer blocks (attention q, k, v, out and gate, plus the MLP) and the one control projection, shape [6144, 64] (our inspection of the file; it matched the author's published checksum).

### Camera sentence

The model was trained on left-only yaw wording. The node converts signed yaw with `left_angle = (-yaw) mod 360`, so a right turn of +50 degrees becomes:

```text
Same figure. Move the camera 310 degrees to the left relative to the input view.
```

Elevation and distance clauses are added only when requested; optional user text is appended unchanged. Write extra text as scene detail ("soft afternoon light"), not as a new camera instruction that contradicts the normal map.

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

ComfyUI: clone the nodes into `custom_nodes`, install `requirements.txt`, download the SAM 3D Body checkpoint after accepting its license, put the LoRA in `models/loras`, and load the shipped `krea2_anygles_workflow.json`. Portable Python, from the model card:

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

Our code review before installing found that the diffusion half of the nodes loads safetensors only, with no network calls, subprocesses, `eval` or `exec`. The normal-preparation half is heavier:

- two pickle checkpoints, loaded with `torch.load(weights_only=False)` and `torch.jit.load`;
- a pickle MoGe model;
- a runtime `torch.hub` fetch of DINOv3 code from GitHub;
- about 20 extra packages (pyrender, pytorch-lightning, MoGe from git);
- the gated `facebook/sam-3d-body-dinov3` repo (separate SAM License).

The gated repo returned HTTP 403 for our accounts (access is approved by hand), and we do not unpickle third-party checkpoints in a shared runtime, so we did not use this path.

**Isolation pattern:** run normal preparation in a separate environment that only writes `target_normal.png`, then feed that PNG and the camera sentence to the Encode node. The shared ComfyUI never unpickles anything.

## Our orbit test

We replaced only the mesh source and kept everything else from the author:

- **Mesh:** [TripoSG](https://github.com/VAST-AI-Research/TripoSG) (MIT, ungated, all weights `.safetensors`) on a [BiRefNet](https://huggingface.co/ZhengPeng7/BiRefNet) person matte of the source, in a separate environment. TripoSG settings: 50 steps, guidance 7.0, seed 42.
- **Normals:** the author's own normal renderer, called unchanged with our mesh, with the author's camera sentences. Focal fixed at 1680 px (SAM 3D Body's default when it has no FOV estimate), because the MoGe checkpoint is pickle-only.
- **Diffusion:** only the Encode, Load LoRA and Model patch nodes in ComfyUI. Settings as above: fp8 Turbo, 8 steps, euler/simple, cfg 1, strength 1.0, 384 px reference, 1008x1344, one fixed seed.
- **Matrix:** 4 one-person subjects (one from an identity LoRA, three photoreal scenes) x 20 views. That is a full yaw circle in 22.5-degree steps (16 views), elevation +-20 and distance 0.78 / 1.35. 80 frames in total.

Measured (face similarity = OpenCV SFace cosine against the source face; 0.363 or more counts as the same person):

| Signal | Result |
|---|---|
| Person silhouette vs target normal (IoU, median per subject) | 0.83-0.91 (the seated subject fits worst) |
| Face similarity, near-front views (median per subject) | 0.47-0.61 |
| Face similarity at +-90 degrees (profiles) | 0.07-0.53, strongly subject-dependent |
| Back views (about +-135 to 180 degrees) | the detector usually finds no face, as expected |
| Detected faces at or above the same-person line | 43 of 60 |

What differs from the author's setup: TripoSG gives the clothed outline (coat, skirt, hair, objects in hand), while SAM 3D Body gives a bare parametric body, which is what the adapter was trained on. A seated pose fit the open mesh worst. Treat these numbers as a lower bound for the original pipeline, not a measurement of it.

## Gotchas

- **Issue:** Loading the file with a standard LoRA loader. -> **Fix:** Use the Anygles Load LoRA node; a plain loader drops `transformer.first_control.weight` and the view control with it.
- **Issue:** The normal map and the output canvas differ in size. -> **Fix:** Render the normal at exactly the output size and aspect ratio; a mismatched normal gives wrong control.
- **Issue:** Several people or a small figure in the source. -> **Fix:** The adapter is built for one clear, reasonably large person; crop first.
- **Issue:** Expecting a faithful back view. -> **Fix:** Hidden sides and background are invented; check identity and clothing on large yaw.
- **Issue:** Swapping the checkpoint precision. -> **Fix:** The ComfyUI graph was validated on an int8 ConvRot Turbo checkpoint and the card warns quantized runtimes differ at pixel level from BF16; re-check on fp8.
- **Issue:** Running the preparation step in a shared server. -> **Fix:** It unpickles checkpoints and fetches code at runtime; isolate it.

## Open questions

- The same orbit with the original SAM 3D Body normals (bare body instead of a clothed mesh).
- The effect of strengths other than 1.0.
- Whether fp8 Turbo behaves like the author's int8 ConvRot checkpoint.

## See Also

- [[krea-2-prompting]] - settings, guidance conventions and prompt form for Krea 2
- [[krea-2]] - Krea 2 release history
- [[flux-klein-capability-map]] - the same "attest the exact variant and runtime" discipline

## Sources

- Model card (settings, ranges, portable usage, license): https://huggingface.co/yijunwang2/krea2-anygles
- ComfyUI nodes, README and workflow: https://github.com/alexw5702-afk/krea2-anygles
- Node widget ranges: https://github.com/alexw5702-afk/krea2-anygles/blob/main/nodes.py
- Pixel budget (`MAX_PIXELS = 2 * 1024 * 1024`): https://github.com/alexw5702-afk/krea2-anygles/blob/main/anygles.py
- Demo Space: https://huggingface.co/spaces/yijunwang2/krea2-anygles
- SAM 3D Body source: https://github.com/facebookresearch/sam-3d-body
- SAM 3D Body checkpoint (gated): https://huggingface.co/facebook/sam-3d-body-dinov3
- TripoSG (image-to-3D, MIT): https://github.com/VAST-AI-Research/TripoSG and weights https://huggingface.co/VAST-AI/TripoSG
- BiRefNet (matting): https://huggingface.co/ZhengPeng7/BiRefNet
- OpenCV face recognition (SFace, 0.363 cosine threshold): https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html
