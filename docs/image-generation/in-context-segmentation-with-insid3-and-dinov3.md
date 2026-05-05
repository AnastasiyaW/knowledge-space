# In-Context Segmentation with INSID3 and DINOv3

INSID3 is a training-free framework for one-shot in-context segmentation that leverages dense features from a frozen DINOv3 backbone. It identifies semantic correspondences between a reference image/mask pair and a target image to generate high-resolution binary masks.

## Core Architecture and Backbone
The system utilizes a Vision Transformer (ViT) encoder to extract spatial features. While the original implementation expects Meta-style model weights, native support in `transformers 5.5.0` allows the use of Hugging Face compatible `DINOv3ViTModel` via a thin adapter.

- **Backbone:** ViT-L/16 (DINOv3)
- **Parameters:** ~303M (backbone)
- **Input Resolution:** 1024x1024 px
- **Output:** `(H, W) torch.bool` segmentation mask
- **Peak VRAM:** ~2.45 GB during inference

## Hugging Face Adapter
To bridge the gap between the `transformers` library and the expected Meta-style API, a wrapper is used to implement the `get_intermediate_layers` method. This method is the primary interface INSID3 uses to extract multi-scale or single-layer features.

### Adapter Implementation
```python
import torch
import torch.nn as nn
from transformers import AutoModel

class HFDinoV3Adapter(nn.Module):
    def __init__(self, hf_model_path: str, dtype=torch.float32):
        super().__init__()
        self.model = AutoModel.from_pretrained(hf_model_path, dtype=dtype)
        self.model.eval()
        cfg = self.model.config
        self.patch_size = cfg.patch_size
        self.embed_dim = cfg.hidden_size
        self.num_register_tokens = cfg.num_register_tokens
        self.num_prefix = 1 + self.num_register_tokens # 1 CLS + N registers

    @torch.no_grad()
    def get_intermediate_layers(self, x, n=1, reshape=False, return_class_token=False, norm=True):
        B, C, H, W = x.shape
        Hp, Wp = H // self.patch_size, W // self.patch_size
        out = self.model(x, output_hidden_states=True)
        
        # Meta implementation applies norm to intermediate layers.
        # HF out.last_hidden_state is already normalized.
        if n == 1 and norm:
            layers = [out.last_hidden_state]
        else:
            layers = list(out.hidden_states[-n:])
            
        results = []
        for feat in layers:
            cls_tok = feat[:, 0, :]
            patch = feat[:, self.num_prefix:, :] # Strip CLS and Register tokens
            if reshape:
                patch = patch.transpose(1, 2).reshape(B, self.embed_dim, Hp, Wp)
            results.append((patch, cls_tok) if return_class_token else patch)
        return tuple(results)
```

## Inference Pipeline
The inference process involves setting a reference image with its corresponding binary mask and then passing the target image. The internal similarity computation and SVD-based positional subspace projection handle the correspondence mapping.

### Production Wrapper
```python
from models import build_insid3

def run_segmentation(ref_img, ref_mask, tgt_img, size=1024):
    """
    Performs one-shot segmentation.
    ref_img/ref_mask: Tensors or PIL images.
    """
    # Requires monkey-patching models._build_encoder to use HFDinoV3Adapter
    model = build_insid3(model_size='large', image_size=size).to('cuda').eval()
    
    model.set_reference(ref_img, ref_mask)
    model.set_target(tgt_img)
    
    with torch.no_grad():
        mask = model.segment() # Returns (size, size) torch.bool
    return mask
```

## Performance Benchmarks
Tested on NVIDIA H200 (140GB VRAM), though applicable to consumer hardware with >= 4GB VRAM.

| Step | Duration |
| :--- | :--- |
| **Model Initialization** | ~1.7 s |
| **Reference Encoding** | ~0.35 s |
| **Target Segmentation** | ~0.76 s |
| **Cold Start Total** | ~2.8 s |

## Gotchas
- **Normalization Mismatch:** The adapter uses `last_hidden_state` for `n=1` which includes the final LayerNorm. If requesting `n > 1` layers from `hidden_states`, the intermediate outputs are pre-norm, potentially causing feature scale shifts compared to the original Meta implementation.
- **Register Tokens:** DINOv3 uses register tokens (typically 4). These must be explicitly stripped from the feature map before reshaping, or the spatial dimensions will not match the expected `(H/16, W/16)` grid.
- **Positional Subspace:** If segmenting very small objects (e.g., skin lesions or micro-defects), the default SVD components (`--svd-comps 500`) may be insufficient. Increasing this value or decreasing the similarity threshold `--tau` (default 0.6) may be necessary.
- **RoPE Embedding Periods:** In the Meta architecture, `rope_embed.periods` is a buffer generated during initialization. It is missing from standard Hugging Face `safetensors` state dicts and must be handled by the adapter or the base model class.

## See Also
- [[in-context-segmentation]]
- [[face-detection-filtering-pipeline]]
- [[flow-matching]]
- [[defect-detection-small-objects]]

