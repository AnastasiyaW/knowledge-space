# TIPSv2: Text-Image Pretraining with Spatial Awareness

Google DeepMind model for dense spatial feature prediction (depth, surface normals, segmentation) producing per-patch embeddings that remain compatible with text embeddings.

## Architecture

- **Full name:** Text-Image Pretraining with Spatial awareness v2
- **Variant covered:** B/14 — 86M vision params + 110M text params
- **Key departure from CLIP:** CLIP produces one global vector per image; TIPSv2 produces a **per-patch feature map** (dense), enabling DPT (Dense Prediction Transformer) decoder heads
- **Backbone:** ViT-B/14 patch size, trained with spatial awareness objectives alongside contrastive text-image alignment
- **Output:** patch-level embeddings at 14×14 pixel stride → direct input to DPT heads for pixel-level tasks

## Supported Downstream Tasks

```
image → TIPSv2 backbone → patch features
                              │
                    ┌─────────┼──────────┐
                    ▼         ▼          ▼
              depth map   normals    segmentation mask
```

All three heads share the same frozen or fine-tuned backbone. Cross-task transfer is possible because the per-patch representation is not task-specific.

### Additional use cases

- **Backbone for downstream vision tasks** — patch embeddings can be treated as a general dense visual feature extractor, similar to DINOv2 but with text alignment preserved
- **Multi-modal retrieval with spatial grounding** — text embedding space compatibility means region-level text-image matching is possible without extra alignment training

## Availability Status (as of April 2026)

| Resource | Status |
|---|---|
| `google/tipsv2-b14` on HuggingFace | **404 — unavailable** (published then pulled) |
| HF Demo Space `google/tipsv2-gpu-explorer` | **Working** (Zero GPU, interactive) |
| ModelScope / Gitee mirrors | Not found |
| arxiv paper | Not found under TIPSv2; presumed CVPR 2026 submission |
| TIPS **v1** weights | **Available** — `google-deepmind/tips` on GitHub |
| TIPS v1 paper | arxiv [2410.16512] |

Likely reason for v2 unavailability: weights published ahead of CVPR 2026 camera-ready deadline, then retracted.

## TIPS v1 as Fallback

v1 paper [2410.16512] covers the same spatial-awareness pretraining concept. Use it if v2 weights remain unavailable.

```bash
# Clone v1 code and weights
git clone https://github.com/google-deepmind/tips
cd tips
pip install -r requirements.txt
```

Core inference pattern from the v1 codebase:

```python
import tips
import torch
from PIL import Image

model = tips.load_model("tips_b14")          # downloads ~350 MB checkpoint
model.eval()

img = Image.open("photo.jpg").convert("RGB")
inputs = tips.preprocess(img)                # returns dict with pixel_values tensor

with torch.no_grad():
    outputs = model(**inputs)

# patch_features: (1, num_patches, embed_dim)
patch_features = outputs.last_hidden_state
```

DPT head for depth estimation requires an additional fine-tuned decoder; v1 repo ships pre-trained heads for depth and normals.

## Comparison with Related Models

| Model | Output type | Text alignment | Depth | Normals | Segmentation |
|---|---|---|---|---|---|
| CLIP ViT-B/16 | global embedding | yes | no | no | no |
| DINOv2 ViT-B/14 | patch + global | no | via head | via head | via head |
| **TIPSv2 B/14** | **patch (dense)** | **yes** | **yes** | **yes** | **yes** |
| Depth Anything v2 | depth map | no | yes | no | no |

TIPSv2's differentiator is the combination of dense spatial features **and** text embedding compatibility. DINOv2 gives better dense features in isolation but has no text alignment.

## DPT Head Overview

Dense Prediction Transformer (DPT) heads take patch tokens from a ViT backbone and upsample them to full resolution through a multi-scale fusion scheme:

```
patch tokens (e.g., 37×37 for 518×518 input at /14 stride)
        │
  Reassemble × 4 scales  ← extracts tokens at different depths of ViT
        │
  Fusion blocks (Conv + BN + ReLU)
        │
  Final head (Conv → output channels)
        │
  Dense output (depth / normals / segmentation logits)
```

Any ViT producing patch-level tokens can drive a DPT head; TIPSv2 improves head quality by providing spatially-aware features rather than purely semantic ones.

## Gotchas

- **HF weights 404:** `google/tipsv2-b14` will raise `RepositoryNotFoundError` as of April 2026. Fall back to v1 weights (`google-deepmind/tips`) or use the live demo Space for experimentation only.
- **Global vs. patch pooling:** if you pool TIPSv2 patch features to a single vector for image retrieval, you lose spatial information. Use full patch sequences as input to DPT heads, not pooled vectors.
- **Patch stride vs. input size:** at /14 stride, a 224×224 image gives 16×16 = 256 tokens; a 518×518 image gives ~37×37 = 1369 tokens. Memory scales quadratically — batch large images carefully.
- **Text compatibility does not mean zero-shot depth:** the text-image alignment is for retrieval/grounding, not for prompting depth output. Depth estimation still requires a trained DPT head.
- **v1 vs. v2 quality gap unknown:** no published benchmark comparing v1 and v2 is available while v2 paper is under review. Treat v1 as a reasonable approximation, not a confirmed equivalent.

## Monitoring for v2 Release

```bash
# Poll HF API for model availability
python - <<'EOF'
import requests, json
r = requests.get("https://huggingface.co/api/models/google/tipsv2-b14")
print(r.status_code, json.loads(r.text).get("error", "available"))
EOF
```

When the model returns 200, download via:

```python
from transformers import AutoModel, AutoProcessor
model = AutoModel.from_pretrained("google/tipsv2-b14")
processor = AutoProcessor.from_pretrained("google/tipsv2-b14")
```

## See Also

- [[cnn-computer-vision]]
- [[transfer-learning]]
- [[generative-models]]
