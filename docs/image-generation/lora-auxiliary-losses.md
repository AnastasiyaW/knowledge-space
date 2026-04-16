---
title: LoRA Auxiliary Losses
category: techniques
tags: [lora, training, loss, arcface, dreambooth, masked-loss, b-lora, identity]
aliases: ["Auxiliary Training Losses", "LoRA Loss Functions"]
---

# LoRA Auxiliary Losses

Additional loss terms beyond standard diffusion denoising loss. Use these when the main diffusion loss alone fails to preserve specific properties (identity, structure, spatial separation).

## Standard Diffusion Loss (Baseline)

```python
# Predict noise at timestep t, minimize MSE to real noise
noise_pred = unet(noisy_latent, t, text_embedding)
loss = F.mse_loss(noise_pred, real_noise)
```

All auxiliary losses are additive weighted terms on top of this.

## ArcFace Identity Loss

Preserves facial identity during edit LoRA training. Penalizes identity drift between generated face and reference.

```python
from insightface.app import FaceAnalysis
import torch.nn.functional as F

face_app = FaceAnalysis(providers=['CUDAExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

def arcface_loss(generated_img, target_img, weight=0.1):
    gen_faces = face_app.get(generated_img)
    tgt_faces = face_app.get(target_img)

    if not gen_faces or not tgt_faces:
        return torch.tensor(0.0)

    gen_emb = torch.tensor(gen_faces[0].embedding)
    tgt_emb = torch.tensor(tgt_faces[0].embedding)
    cos_sim = F.cosine_similarity(gen_emb.unsqueeze(0), tgt_emb.unsqueeze(0))
    return weight * (1 - cos_sim)

# Combined loss
total_loss = diffusion_loss + arcface_loss(generated, target)
```

**When to use**: edit LoRA (before/after pairs), face swap LoRA, beautify LoRA. Any task where generated face must match a reference identity.

**Weight tuning**: start at 0.05-0.1. Too high → face becomes static/stiff. Too low → no identity preservation.

## DreamBooth Prior Preservation Loss

Prevents language drift: model forgets what the class concept is while learning the specific instance.

```python
# During training: generate class images using base model
# class_prompt = "a person" (generic version of the subject)
# prior_images = model.generate(class_prompt, n=200)

# Loss includes:
# 1. Main loss on instance images (specific subject)
# 2. Prior loss on class images (generic concept)

instance_loss = diffusion_loss(instance_batch)
prior_loss = diffusion_loss(prior_batch)
total_loss = instance_loss + prior_weight * prior_loss
```

**In ai-toolkit:**
```yaml
train:
  prior_preservation: true
  prior_preservation_weight: 1.0
  class_prompt: "a person"
  num_class_images: 200
  prior_loss_weight: 1.0
```

**When to use**: DreamBooth-style training (single subject, few images). Less critical for large datasets.

## Masked Loss (diffusion-pipe)

Train only on specific image regions — essential for face LoRA where background should not influence weights.

```toml
# diffusion-pipe dataset config
[[dataset.image_config]]
path = "data/faces/"
masks_path = "data/masks/"
masked_loss = true
```

```
data/faces/
  ├── img001.jpg
  └── img002.jpg
data/masks/
  ├── img001.png   # white = train, black = ignore
  └── img002.png
```

**Mask generation pipeline:**
```python
# SAM2 for mask generation
from sam2.sam2_image_predictor import SAM2ImagePredictor

predictor = SAM2ImagePredictor.from_pretrained("facebook/sam2-hiera-large")
predictor.set_image(image)
masks, _, _ = predictor.predict(point_coords=[[cx, cy]], point_labels=[1])

# Erode slightly to avoid edge artifacts
import cv2
mask = cv2.erode(masks[0].astype(np.uint8) * 255, kernel=np.ones((10,10)))
```

**When to use**: face-only LoRA training, object-specific LoRA (jewelry, product). Prevents background texture, lighting, and other scene elements from leaking into LoRA weights.

## Face-Masked Diffusion Loss

Variant of masked loss focused on the face region specifically:

```python
def face_masked_loss(noise_pred, real_noise, face_mask):
    """
    face_mask: binary tensor (H, W), 1 = face region
    """
    # Standard loss everywhere
    base_loss = F.mse_loss(noise_pred, real_noise)

    # Upweight loss in face region
    face_weight = 1.0 + face_mask_weight * face_mask
    weighted_loss = (F.mse_loss(noise_pred, real_noise, reduction='none') * face_weight).mean()

    return weighted_loss
```

## B-LoRA: Content / Style Disentanglement

Train different LoRA portions on different transformer block groups to separate content (structure) from style.

```python
# Klein 9B block targeting
# double_transformer_blocks = joint image+text attention (style influence)
# single_transformer_blocks = image-only refinement (structure/content)

# Style-only LoRA: target only double blocks
style_lora_target = [
    f"transformer.double_transformer_blocks.{i}"
    for i in range(8)  # all 8 double blocks
]

# Content/identity LoRA: target only single blocks
content_lora_target = [
    f"transformer.single_transformer_blocks.{i}"
    for i in range(0, 12)  # first 12 of 24 single blocks
]
```

**When to use**: when you need to merge multiple LoRAs at inference and prevent style from corrupting structure or vice versa.

## Concept Sliders

Train on contrast pairs to create a directional attribute slider:

```python
# Dataset: image pairs with/without attribute
# positive_pair: ["detailed_texture.jpg", "smooth_texture.jpg"]
# negative_pair: ["smooth_texture.jpg", "detailed_texture.jpg"]

# Loss: maximize difference along attribute direction
# Result: LoRA weight at -2.0 = very smooth, at +2.0 = very textured
```

```yaml
# Inference: apply slider at inference
lora_weight: 1.5   # positive = more detail
lora_weight: -1.5  # negative = less detail
```

**In ComfyUI**: load as LoRA with strength slider. The sign and magnitude directly control the attribute direction.

**Available pre-trained sliders** (compatible with FLUX/Klein):
- `klein_slider_anatomy v1.5` — anatomy correction, use weight 2-4 (NOT 0-1 scale)

## Combining Multiple Auxiliary Losses

```python
def combined_training_loss(
    noise_pred, real_noise,
    generated_img=None, target_img=None,
    face_mask=None,
    prior_pred=None, prior_noise=None
):
    # Base diffusion loss
    diff_loss = F.mse_loss(noise_pred, real_noise)

    # Identity preservation
    id_loss = arcface_loss(generated_img, target_img) if generated_img else 0

    # Prior preservation
    prior = F.mse_loss(prior_pred, prior_noise) if prior_pred else 0

    # Face region upweighting
    face = face_masked_loss(noise_pred, real_noise, face_mask) if face_mask else 0

    return diff_loss + 0.1 * id_loss + 1.0 * prior + 0.5 * face
```

**Warning**: stacking too many auxiliary losses can destabilize training. Start with 1-2 at a time and verify convergence before adding more.

## Gotchas

- **ArcFace requires face detection at every step**: InsightFace runs on every training batch which adds significant overhead (2-5× slower). Use only when identity preservation is critical and dataset is small.
- **Prior preservation for large datasets**: with 50+ training images, language drift is minimal and prior preservation loss rarely helps. The extra inference cost for generating prior images is not justified.
- **Masked loss requires aligned masks**: masks must correspond 1:1 with training images. If augmentation (crop, flip) is applied, masks must undergo the same transforms. diffusion-pipe handles this automatically if masks are in parallel directory.
- **B-LoRA block targeting is model-specific**: block indices for Klein 9B (8 double + 24 single) differ from FLUX.1. Always verify block names via `model.named_modules()` before setting targets.
- **Concept Slider weights are NOT standard LoRA strength**: `klein_slider_anatomy v1.5` uses weight 2-4 (documented range), not 0-1. Using standard 0-1 range produces no visible effect.

## See Also

- [[diffusion-lora-training]] - general training pipeline, optimizer choices
- [[flux-klein-character-lora]] - character LoRA with ArcFace and masked loss
- [[lora-fine-tuning-for-editing-models]] - edit LoRA with paired data
- [[anatomy-correction-diffusion]] - anatomy correction sliders and tools
