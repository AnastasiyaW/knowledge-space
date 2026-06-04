---
title: Pixel Art Generation
category: image-generation
tags: [pixel-art, lora, sdxl, flux, conversion, dithering, quantization, pyxelate, retrodiffusion, spritesheet]
aliases: ["Pixel Art Pipeline", "Raster to Pixel Art"]
---

# Pixel Art Generation

Algorithms and models for converting raster images to pixel art, generating pixel art via diffusion LoRAs, and training custom pixel-art style LoRAs. For LoRA training fundamentals see [[diffusion-lora-training]].

## Key Facts

- **pyxelate** last stable: v2.1.1 (2022); Python 3.10 venv required — numba incompatible on 3.12+
- **nerijs/pixel-art-xl**: SDXL LoRA with LCM scheduler, 8-step inference, last updated April 2026
- **fal/flux-2-klein-4b-spritesheet-lora**: FLUX.2 Klein 4B LoRA generating 2×2 multi-angle sprite sheets
- **Shakker-Labs/FLUX.1-Kontext-dev-LoRA-Pixel-Style**: img2img pixel conversion via [[flux-kontext]] pipeline, 24 steps, CFG 2.5
- **RetroDiffusion**: purpose-trained model (not SD LoRA); true grid-aligned output; REST API at `api.retrodiffusion.ai/v1/inferences`; also on Replicate `retro-diffusion/rd-fast`
- **PixelLab**: Python SDK `pip install pixellab`; MCP server available; sprite rotation + animation endpoints
- **SD-piXL**: ETH Zurich SIGGRAPH Asia 2024 (arxiv 2410.06236); score distillation with hard H×W + N-color constraints; research-grade, no pip package
- **libimagequant** (pngquant's quantizer): available as `imagequant` PyPI package (released Oct 2025) or via Pillow 10+ `Image.Quantize.LIBIMAGEQUANT`
- **hitherdither**: no PyPI release; install from GitHub; dithering-only (no palette extraction)

## Conversion Algorithms

### pyxelate — Bayesian GMM + Atkinson dithering

Best for clean/cartoon sources. Struggles with JPEG compression artifacts.

```python
from pyxelate import Pyx, Pal
from skimage import io

img = io.imread("source.jpg")
pyx = Pyx(factor=8, palette=24, dithering="atkinson")
pyx.fit(img)
result = pyx.transform(img)
io.imsave("output.png", result)
```

`factor=8`: each output pixel = 8×8 source pixels. For 512px source → 64px output.
Speed: ~2–60s per image CPU (slow; `factor` is the main lever). License: MIT.

### Pillow NEAREST + libimagequant

Production batch pipeline. Best palette fidelity; ~0.5s/image CPU.

```python
from PIL import Image

def to_pixel_art(src: str, dst: str, scale: int = 8, n_colors: int = 32) -> None:
    img = Image.open(src).convert("RGBA")
    pw = max(16, img.width // scale)
    ph = max(16, img.height // scale)
    small = img.resize((pw, ph), Image.NEAREST)
    quantized = small.quantize(
        colors=n_colors,
        method=Image.Quantize.LIBIMAGEQUANT,
        dither=1,
    )
    quantized.save(dst)
```

`LIBIMAGEQUANT` uses perceptual LAB weighting; `MEDIANCUT` is the fallback if not compiled in.

### hitherdither — ordered dithering pass

Apply after palette selection (Pillow or imagequant) for crispier ordered patterns.

```python
# pip install git+https://github.com/hbldh/hitherdither
import hitherdither
from PIL import Image

img = Image.open("source.jpg").convert("RGB").resize((64, 64), Image.NEAREST)
palette = hitherdither.palette.Palette.create_by_median_cut(img, n=32)
dithered = hitherdither.ordered.bayer.bayer_dithering(
    img, palette, [256/4, 256/4, 256/4], order=8
)
dithered.save("output.png")
```

Bayer order=8 gives crisper results than Floyd-Steinberg; Yliluoma's algorithm is highest-quality but slower. License: MIT.

### AI post-process — downsample AI output to pixel grid

```python
from PIL import Image

def ai_to_pixelart(
    src: str,
    dst: str,
    target_w: int = 320,
    target_h: int = 480,
    n_colors: int = 48,
) -> None:
    img = Image.open(src).convert("RGB")
    # Two-step: LANCZOS first, NEAREST final (preserves hard edges)
    mid = img.resize((target_w * 2, target_h * 2), Image.LANCZOS)
    small = mid.resize((target_w, target_h), Image.NEAREST)
    quantized = small.quantize(
        colors=n_colors,
        method=Image.Quantize.LIBIMAGEQUANT,
        dither=Image.Dither.FLOYDSTEINBERG,
    )
    quantized.convert("RGB").save(dst)
```

### rembg — background removal preprocessing

Removes noisy backgrounds before conversion; prevents palette confusion from JPEG artifacts. `pip install rembg[gpu]`; RMBG-2.0 model; ~1–3s GPU / ~5–10s CPU.

```python
from rembg import remove
from PIL import Image
import io

with open("source.jpg", "rb") as f:
    img = Image.open(io.BytesIO(remove(f.read())))  # RGBA PNG with alpha
```

### GCD-based pixel grid size detection

Infer the logical block size from run-length GCD before choosing scale factor.

```python
from math import gcd
from functools import reduce
import numpy as np
from PIL import Image

def detect_pixel_grid_size(img: Image.Image) -> int:
    arr = np.array(img.convert("RGB"))
    runs = []
    for row in arr[::4]:  # sample every 4 rows for speed
        cur, count = row[0].tobytes(), 1
        for px in row[1:]:
            if px.tobytes() == cur: count += 1
            else: runs.append(count); cur, count = px.tobytes(), 1
        runs.append(count)
    cands = [r for r in runs if 1 < r <= 32]
    return max(1, min(reduce(gcd, cands), 16)) if cands else 1
```

## Generative / LoRA Approaches

### nerijs/pixel-art-xl — SDXL + LCM (8-step)

```python
from diffusers import DiffusionPipeline, LCMScheduler
import torch

pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda")
pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl", adapter_name="lcm")
pipe.load_lora_weights(
    "nerijs/pixel-art-xl",
    weight_name="pixel-art-xl.safetensors",
    adapter_name="pixel",
)
pipe.set_adapters(["lcm", "pixel"], adapter_weights=[1.0, 1.2])

image = pipe(
    prompt="pixel art castle, 8-bit style",
    num_inference_steps=8,
    guidance_scale=1.5,
    height=512,
    width=512,
).images[0]

# Snap to true pixel grid
w, h = image.size
image.resize((w // 8, h // 8), Image.NEAREST).resize((w, h), Image.NEAREST).save("out.png")
```

Requires 8+ GB VRAM. License: CreativeML OpenRAIL-M.
For img2img: use `StableDiffusionXLImg2ImgPipeline` with `strength=0.6–0.75`.

### FLUX.1-dev + atmospheric pixel art LoRAs

Notable FLUX.1-dev LoRAs for high-detail pixel art (CivitAI/HF):
- `UmeAiRT/FLUX.1-dev-LoRA-Modern_Pixel_art` — trigger: `umempart`; 100-image training set
- CivitAI #683579 "Pixel Art Illustrations FLUX" — V1 trained on 4×4-pixel-block art; best for atmospheric landscapes
- CivitAI #629354 "Pixel Art Styles FluxV3" — trained on MidJourney output; best for compositional depth

```python
from diffusers import FluxPipeline
import torch

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16,
).to("cuda")
pipe.load_lora_weights(
    "UmeAiRT/FLUX.1-dev-LoRA-Modern_Pixel_art",
    weight_name="FLUX.1-dev-LoRA-Modern_Pixel_art.safetensors",
)
pipe.set_adapters(["default"], adapter_weights=[0.85])

image = pipe(
    prompt="umempart, atmospheric pixel art, mountain fortress, pine forest mist, warm window light",
    height=1024,
    width=640,
    num_inference_steps=28,
    guidance_scale=3.5,
).images[0]
image.save("cover_draft.png")
# Then run ai_to_pixelart() above for palette quantization
```

### FLUX.1-Kontext img2img pixel conversion

`Shakker-Labs/FLUX.1-Kontext-dev-LoRA-Pixel-Style`: preserves source composition while applying pixel style.

```python
from diffusers import FluxKontextPipeline
import torch
from PIL import Image

pipe = FluxKontextPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype=torch.bfloat16,
).to("cuda")
pipe.load_lora_weights(
    "Shakker-Labs/FLUX.1-Kontext-dev-LoRA-Pixel-Style",
    weight_name="FLUX1-Kontext-dev-LoRA-Pixel-Style.safetensors",
)

image = pipe(
    image=Image.open("source.png"),
    prompt="convert to atmospheric pixel art, crisp pixel edges, 50+ color palette",
    num_inference_steps=24,
    guidance_scale=2.5,
).images[0]
```

See [[flux-kontext]] for pipeline setup details.

### fal spritesheet LoRA — multi-angle sprites

`fal/flux-2-klein-4b-spritesheet-lora`: generates 2×2 spritesheet (isometric front-right, front-left, side, top-down). Available via fal.ai API without local GPU:

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/flux-2-klein/4b/base/edit/lora",
    arguments={
        "prompt": "red dragon character, pixel art sprite, 2x2 spritesheet",
        "loras": [{"path": "fal/flux-2-klein-4b-spritesheet-lora", "scale": 1.0}],
    },
)
```

Base model: FLUX.2 Klein 4B. **4B LoRA not compatible with 9B** — see [[flux-klein-9b-inference]].

### RetroDiffusion — purpose-trained API

Purpose-trained on pixel art data (not SD adapter). True grid-aligned output. Models: `rd_plus__low_res` (16–128px), `rd_plus__default`, `rd_plus__mc_item`, `rd_plus__topdown_item`.

```python
import requests

response = requests.post(
    "https://api.retrodiffusion.ai/v1/inferences",
    headers={"X-RD-Token": "YOUR_KEY"},
    json={
        "width": 128,
        "height": 128,
        "prompt": "stone castle tower, fog, pixel art",
        "prompt_style": "rd_plus__default",
        "num_images": 1,
    },
)
# Also: replicate.run("retro-diffusion/rd-fast", input={...})
```

50 free credits on signup; ~$0.02–0.05/image on Replicate.

### PixelLab SDK — game sprites and animation

```python
from pixellab import PixelLab

client = PixelLab(api_key="YOUR_KEY")
result = client.generate_image_pixflux(
    description="knight character, dark fantasy, pixel art",
    image_size={"width": 64, "height": 64},
)
result.image.save("sprite.png")
```

Supports sprite rotation (4/8 directional), skeleton animation, inpainting. MCP server: `github.com/pixellab-code/pixellab-mcp`.

## LoRA Training for Pixel Art Style

> For training tool comparison, hyperparameters, and dataset guidelines see [[diffusion-lora-training]].

**Dataset size:** 50–200 curated images is the effective range. 1000 mixed-style images train a noisier LoRA than 200 consistent ones. Pre-process with the `Pillow + libimagequant` pipeline first to produce clean indexed PNGs.

**Pixel-art-specific params:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| Rank / alpha | 16–32 / rank/2 | Higher rank captures more detail but slower |
| LR (FLUX) | 1e-4 | FLUX is LR-sensitive; see [[diffusion-lora-training]] |
| Steps (100-img dataset) | 1000–2000 | Fewer steps than portrait LoRA |
| Augmentation | **Disabled** | Hard pixel edges blur under standard augmentation |
| Captions | Dense scene descriptions | Not short prompts; describe palette, grid style |
| Augment text | "pixel art", "8-bit style", pixel size | Reinforce style in every caption |

**Dataset prep:** batch-convert with the `to_pixel_art()` function in the Conversion Algorithms section above. Produces clean indexed PNGs as training data.

**Cloud training (fal.ai):** `fal-ai/flux-lora-fast-training` — ~$8 / 1000 steps, returns hosted endpoint. `fal-ai/flux-2-trainer` for FLUX.2 Klein base.

## Collection-Level Learning

For extracting style profiles and scene grammar from a large image collection:

**Embedding + clustering** — DINOv2 for visual style clustering (texture/palette); SigLIP-2 for semantic text-to-image search. Cluster with UMAP (20D) + HDBSCAN → 15–40 style groups. Use `mlxtend.frequent_patterns.fpgrowth` for scene grammar (element co-occurrence). See [[synthetic-dataset-pipeline]] for full pipeline patterns.

```python
from transformers import AutoImageProcessor, AutoModel
import torch, numpy as np
from PIL import Image

def embed_batch(paths: list[str], model_name="facebook/dinov2-large") -> np.ndarray:
    proc = AutoImageProcessor.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).cuda().eval()
    imgs = [Image.open(p).convert("RGB").resize((224, 224)) for p in paths]
    inp = proc(images=imgs, return_tensors="pt").to("cuda")
    with torch.no_grad():
        return model(**inp).last_hidden_state[:, 0].cpu().numpy()  # (N, 1024)
```

**Public pixel art datasets (HuggingFace):**

| Dataset | Size | License |
|---------|------|---------|
| `bghira/free-to-use-pixelart` | ~2K | Permissive for training |
| `jainr3/diffusiondb-pixelart` | ~16K | Research |
| `VatsaDev/pixel-art` | ~5K | Mixed |
| `carlosuperb/lpc-4view-pixel-art-diffusion` | ~8K | LPC (CC-BY-SA 3.0) |
| `UmeAiRT/Ume-Modern_Pixel_Art` | ~100 | Per-model card |

OpenGameArt.org for CC0 game assets; Lospec Gallery for reference (check ToS before scraping).

## Tools Landscape

| Tool | Type | API/Python | License | Best For |
|------|------|------------|---------|----------|
| pyxelate | Library | Python | MIT | Retro look, clean sources |
| Pillow + libimagequant | Library | Python | HPND | Production batch |
| hitherdither | Library | Python | MIT | Ordered dithering step |
| rembg | Library | Python | MIT | Background removal pre-step |
| ImageGoNord | Library | Python | MIT | Palette-snapping to fixed palette |
| nerijs/pixel-art-xl | SDXL LoRA | diffusers | OpenRAIL-M | 8-step pixel generation/img2img |
| FLUX.1-Kontext Pixel LoRA | FLUX LoRA | diffusers | Apache-2.0 | Structure-preserving pixel conversion |
| fal spritesheet LoRA | FLUX.2 LoRA | fal.ai / diffusers | Custom | Multi-angle sprite sheets |
| SD-piXL | Research model | Python (GitHub) | Research | Hard-constrained grid + palette |
| RetroDiffusion | Commercial API | REST + Replicate | Proprietary | True pixel art, game assets |
| PixelLab | Commercial API | Python SDK + MCP | Proprietary | Sprites, animation, rotation |
| PixelOver | Desktop app | None (UI only) | Paid (~$10) | Visual exploration |
| Pixelmash | Desktop app | None (UI only) | Paid (~$40) | Non-destructive pixel layer |
| Aseprite | Desktop app | Lua scripting | Paid ($20) | Manual pixel editing |
| Pixelit | JS Library | JavaScript only | MIT | Browser/Node pipelines |
| ComfyUI-PixelArt-Detector | ComfyUI nodes | ComfyUI | MIT | Palette + downscale in workflow |

## Gotchas

- **Issue:** pyxelate fails to install on Python 3.12+ due to numba version coupling (`numba >= 0.59` required for 3.12, but pyxelate pins older numba). -> **Fix:** Use a `python3.10 -m venv` environment, or skip pyxelate and use `Pillow + libimagequant` instead. Verify with `python -c "import numba; import pyxelate"` before batch runs.

- **Issue:** `Image.Quantize.LIBIMAGEQUANT` raises `ImportError` or silently falls back to MEDIANCUT on some Pillow builds (pre-compiled wheels without libimagequant). -> **Fix:** Install `imagequant` PyPI package (Oct 2025 release) separately: `pip install imagequant`, then use `imagequant.quantize_pil_image()` directly instead of `Image.quantize()`.

- **Issue:** nerijs/pixel-art-xl and most FLUX LoRAs produce anti-aliased output (fractional-pixel rendering) — output does not snap to a clean integer grid. -> **Fix:** Always follow with the two-step downsample: `img.resize((w//N, h//N), NEAREST).resize((w, h), NEAREST)`. Do not use LANCZOS for the final snap.

- **Issue:** FLUX.2 Klein 4B spritesheet LoRA (`fal/flux-2-klein-4b-spritesheet-lora`) cannot be loaded on Klein 9B — architecture mismatch (text encoder shape). -> **Fix:** The LoRA was trained on Klein 4B; 4B and 9B LoRAs are incompatible (different Qwen text encoder sizes). Use fal.ai API or run the 4B base model locally. See [[flux-klein-9b-inference]] for model variant details.

- **Issue:** Training pixel art LoRA on raw JPEG sources produces inconsistent palette noise; standard augmentation (flip, rotation, color jitter) blurs hard pixel edges. -> **Fix:** (a) Pre-process all training images through `Pillow + libimagequant` before training to normalize palette. (b) Disable all augmentation — hard edges are the defining characteristic and any interpolation destroys them.

- **Issue:** Grid-size mismatch: converting a 512px image with `scale=8` gives 64px output, but the source image's internal pixel grid may be 2px, 4px, or 8px blocks — resulting in blurry sub-pixel output. -> **Fix:** Use `detect_pixel_grid_size()` (GCD of run lengths) to infer the logical block size before choosing the scale factor.

## See Also

- [[diffusion-lora-training]] - full LoRA training guide (tools, hyperparameters, dataset prep)
- [[flux-kontext]] - FLUX.1-Kontext img2img pipeline
- [[flux-klein-9b-inference]] - Klein 9B inference settings, compatible LoRA formats
- [[lora-fine-tuning-for-editing-models]] - edit LoRA patterns (Step1X-Edit, paired data)
- [[synthetic-dataset-pipeline]] - collection decomposition, embedding, clustering
- [[low-vram-inference-strategies]] - running FLUX LoRAs on limited VRAM

**Source URLs:**
- https://github.com/sedthh/pyxelate
- https://github.com/hbldh/hitherdither
- https://huggingface.co/nerijs/pixel-art-xl
- https://github.com/AlexandreBinninger/SD-piXL (arxiv 2410.06236)
- https://huggingface.co/fal/flux-2-klein-4b-spritesheet-lora
- https://huggingface.co/Shakker-Labs/FLUX.1-Kontext-dev-LoRA-Pixel-Style
- https://huggingface.co/UmeAiRT/FLUX.1-dev-LoRA-Modern_Pixel_art
- https://retrodiffusion.ai / https://replicate.com/retro-diffusion/rd-fast
- https://github.com/pixellab-code/pixellab-python
- https://github.com/cocktailpeanut/fluxgym
- https://fal.ai/models/fal-ai/flux-lora-fast-training
- https://huggingface.co/datasets/bghira/free-to-use-pixelart
- https://pypi.org/project/imagequant/
