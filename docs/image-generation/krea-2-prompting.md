---
title: Krea 2 Prompting
description: "Krea 2 open-weights prompting reference: one English paragraph with the medium early and the light described, guidance converted between conventions, no negative prompt on Turbo, a 507-token cap outside ComfyUI, and adapter-specific prompts for edits and box layouts."
category: techniques
tags: [krea-2, prompting, text-to-image, comfyui, diffusers, cfg, lora, inpainting, bbox]
aliases: ["Krea 2 prompts", "Krea-2-Turbo prompting", "Krea 2 CFG", "Krea 2 negative prompt"]
---

# Krea 2 Prompting

Open-weights Krea 2 has two variants: Krea-2-Turbo for images and Krea-2-Raw for LoRA training. Krea-2-Turbo is an 8-step distilled model. Krea-2-Raw is the undistilled base. A 12B DiT reads prompts through a Qwen3-VL-4B-Instruct text encoder per the Turbo card, so it responds to plain descriptive English rather than tag soup. Sources reviewed 2026-09-30, including the diffusers Krea2 pipeline and native Krea 2 support in ComfyUI. Hosted Krea 2 Medium/Large on the krea.ai app and API is a separate surface; see [[krea-2]] for the release history.

Facts from code, cards and docs link to the source. Our own runs are marked *in our tests*; they use small samples, one to three seeds per cell. Treat them as direction, not as benchmarks.

## Settings before any prompt matters

Wrong guidance breaks the image before wording does. Krea reference code and diffusers use their own guidance convention. ComfyUI, SGLang and DiffSynth use standard CFG.

| | Turbo (run images) | Raw (base; not for final images) |
|---|---|---|
| Steps | 8 | 52 (README, card) |
| Guidance, Krea / diffusers convention | **0.0** | 3.5 |
| Same in ComfyUI / SGLang / DiffSynth | **cfg 1.0** | cfg 4.5 |
| ComfyUI sampler | `euler`, `simple`, denoise 1 | `euler` |
| Timestep shift | mu 1.15, built into ComfyUI's model config | resolution-dependent |
| Size | 1K to 2K | up to about 1K |
| Negative prompt | never evaluated | used |

**Conversion rule:** standard CFG = 1 + Krea g. Krea computes `cond + g * (cond - uncond)`; ComfyUI computes `uncond + cfg * (cond - uncond)`. The diffusers docstring states the equivalence directly ("the usual CFG formulation with scale `1 + guidance_scale`").

- Krea/diffusers `0.0` = ComfyUI `1.0`; Krea `3.5` = ComfyUI `4.5`.
- **ComfyUI cfg 0 = unconditional sampling.** The sampler ignores the prompt. At least one community ComfyUI guide gives cfg 0.0 by copying Krea's convention.
- diffusers and Krea's `inference.py` CLI default to 28 steps / guidance 4.5 (Krea convention): base-checkpoint defaults, not Turbo values. Pass Turbo values explicitly.
- Beyond 8 steps and cfg 1.0 on Turbo is untested territory: we found no controlled comparison of more steps or of ComfyUI cfg 1.2 to 1.5.

### diffusers (Turbo)

```python
import torch
from diffusers import Krea2Pipeline

# Gated repo: accept the Krea 2 Community License on the model page and log in first.
pipe = Krea2Pipeline.from_pretrained("krea/Krea-2-Turbo", torch_dtype=torch.bfloat16).to("cuda")

image = pipe(
    prompt,
    num_inference_steps=8,
    guidance_scale=0.0,      # Krea convention; equals ComfyUI cfg 1.0
    width=1248, height=832,  # multiples of 16
).images[0]
image.save("krea2_turbo.png")
```

### ComfyUI (Turbo)

```yaml
# Official template image_krea2_turbo_t2i: files and KSampler values
diffusion_model: krea2_turbo_fp8_scaled.safetensors
text_encoder: qwen3vl_4b_fp8_scaled.safetensors   # CLIP type: krea2
vae: qwen_image_vae.safetensors
KSampler: {steps: 8, cfg: 1.0, sampler_name: euler, scheduler: simple, denoise: 1.0}
negative: ConditioningZeroOut   # never computed at cfg 1.0 anyway
model_sampling_node: none       # shift 1.15 is in the model config
```

## Size and aspect ratio

- **Sides in multiples of 16.** Krea's `sampling.py` pads up and prints a notice; diffusers rounds up with a logged warning; the AnyPaint edit adapter requires a multiple-of-16 canvas.
- **Turbo 1K to 2K, Raw up to about 1K.** Pretraining ran at 256/512/1024 px in same-aspect-ratio batches.
- **1K ladder** (Krea's hosted size list, all multiples of 16): 1024x1024, 1184x896, 1248x832, 1376x768, 928x1152, 832x1248, 768x1376.
- For 2K on Turbo, scale a 1K size by about 1.41 and round to 16. This is derived, not published by Krea.

```python
def krea_2k(w: int, h: int, scale: float = 2 ** 0.5) -> tuple[int, int]:
    """Scale a 1K ladder size to ~2 MP and snap both sides to multiples of 16."""
    return (int(round(w * scale / 16)) * 16, int(round(h * scale / 16)) * 16)

krea_2k(1248, 832)  # (1760, 1184)
```

## Text-to-image prompt form

Krea sets the rule in `docs/prompting.md` and the LLM expansion prompt `docs/expansion.txt`: use natural language in one cohesive paragraph. Longer and specific descriptions work better, though short ones still run.

- **One paragraph, no bullets, headings, JSON or markdown.** The bbox LoRA block below is the one exception.
- **Name the medium early.** Write "An editorial portrait photograph of..." or "A macro photograph of...". The expansion prompt treats "photo of" as a medium to keep.
- **Keep each subject together with its own attributes and actions.** Use concrete spatial words: left, right, foreground, behind, holding.
- **Describe the light, always.** State quality and direction ("soft window light from the left", "harsh noon sun", "warm low sunlight from the right"). Every official photo example does this.
- **Photorealism.** Specify concrete surface detail and small imperfections (skin pores, faint freckles, flyaway hairs, scuffed shoes, worn vinyl seats), shot type and depth of field (medium close-up, shallow depth of field), film grain or motion blur where wanted. The technical report says motion blur and softness were kept in the data on purpose. Lens numbers ("85mm at f/2") appear in one provider guide and are unproven either way.
- **Text in the image.** Put exact words in double quotes and keep them short. Incidental background text is unreliable; distorted text is a named failure mode.
- **Descriptive comma lists are in distribution.** 8 of the 20 official Turbo examples are comma-separated descriptor lists, and several card widget prompts end with a `, <style tag>`.
- **No quality boilerplate, no weights.** "masterpiece, best quality, 8k" appears in no official example; `(word:1.2)` weighting is reported not to work reliably (one community source).
- **Say what is there instead of "no X".** Write "an unlit torch", not "a torch without flame"; "an empty courtyard at dawn", not "a courtyard, no people".
- **English only is documented.** The card declares `language: en`. Keep non-English words only as text to render, inside quotes, and treat even that as untested.

### Example prompts

```text
A candid street photograph of a young woman standing on a cracked asphalt sidewalk in a courtyard
of five-storey panel apartment blocks, gray facades with uneven glazed balconies, laundry drying on
a line, old poplar trees behind her. She wears a white t-shirt and a denim jacket and squints
slightly in the late afternoon sun, a few flyaway hairs catching the light. Warm low sunlight from
the right, soft shadows, slightly faded colors, eye-level medium shot, everyday documentary feel,
realistic film photograph.
```

```text
A close-up photograph of a hand-painted wooden shop sign reading "OPEN" hanging on a brass hook
beside a green door with chipped paint, morning sun raking from the left across the wood grain,
shallow depth of field, the street behind softly out of focus.
```

### Rewrites

| Instead of | Write |
|---|---|
| `masterpiece, best quality, 8k, (sharp:1.3)` | concrete detail: "fine skin pores, crisp fabric weave, sharp focus on the eyes" |
| "a Paris street, no people" | a scene without a crowd: "a quiet cobbled side street at dawn, shutters closed" |
| "torch without flame" | "an unlit torch" |
| negative prompt "blurry, deformed" on Turbo | nothing: it is not evaluated; describe the wanted focus positively |
| Russian or mixed-language description | English description; quoted words only for rendered text |

### Rejected folklore

- **"The official Krea caption order"** (Subject -> Appearance -> Props -> Composition -> Environment -> Lighting -> Aesthetic, often "in two paragraphs"). It comes from a community post in the model's discussion tab and was repackaged by a ComfyUI node as "the official system prompt". Krea's actual system prompt asks for one paragraph with no fixed section order. The order is a harmless habit, not a trained format.
- **"CFG 0.0 in ComfyUI"** for Turbo: see the conversion rule above.
- **Negative prompts on Turbo:** see the next section.
- **Hosted controls on open weights:** creativity levels, sliders, moodboards and style references exist only in hosted Medium/Large. fal's "Krea 2 Prompting Guide" predates the open release and targets hosted models.
- **"Both variants were trained at 2048":** Raw is documented up to 1K; pretraining stages stopped at 1024.

## Token budget and language

The encoder wraps the prompt in a fixed system template ("Describe the image by detailing the color, shape, size, texture, quantity, text, spatial relationships of the objects and background"). Krea's reference code, diffusers and DiffSynth pad or truncate to 512 positions after stripping the 34-token system prefix; a 5-token assistant suffix follows the prompt.

- **User-prompt cap: about 507 tokens** in Krea's reference code, diffusers and DiffSynth. The tail beyond it is cut silently.
- **ComfyUI does not truncate** (its Qwen3-VL tokenizer has no 512 cap). The same long prompt behaves differently across runtimes.
- Keep prompts under about 500 tokens and put the essentials first.
- Rates measured with the Qwen tokenizer: English about 1.3 to 1.4 tokens per word (about 360 to 390 words fit the cap); the longest official example is 252 tokens. The 84-word official "mouse" example is 108 tokens in English; a Russian translation took 215 tokens, 2.0x.

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-VL-4B-Instruct")  # the encoder Krea 2 uses
n = len(tok(prompt)["input_ids"])
print(n, "tokens;", "over the 507 cap" if n > 507 else "fits")
```

## Negative prompts and suppression

- **Turbo at its settings never evaluates the negative.** Krea's sampler skips the unconditional branch at guidance 0; ComfyUI skips it at cfg 1.0 (`uncond + 1 * (cond - uncond) = cond`); diffusers ignores `negative_prompt` when `guidance_scale <= 0`; fal's Turbo API has no negative field. Negative lists copied from Raw-era LoRA cards ("airbrushed, plastic skin, waxy") do nothing on Turbo.
- **Raw with real CFG (ComfyUI cfg > 1) does use the negative.** Default is the empty string.
- **Negation inside the positive prompt is unreliable.** In our tests a street background with "an empty ... street, no people, no passers-by" gave 16 extra faces against 13 without the phrase (one comparison, one seed per cell): it did not remove people, and one comparison cannot show it adds them.

To suppress something on Turbo:

1. Rephrase positively ("unlit torch", "empty courtyard at dawn").
2. Pick a scene that does not invite the unwanted thing: a sunlit city street brings passers-by (remedy not A/B-tested).
3. Use the community NAG node (Normalized Attention Guidance), which gives negative control at cfg 1.0 through attention; defaults phi 4.0, tau 2.5, alpha 0.25.
4. Use Raw with real CFG, accepting that Raw is slower and not tuned for final images.

## LoRA triggers

**Put the trigger where that LoRA's training captions had it.** Train LoRAs on Raw, run them on Turbo.

- **Official Krea style LoRAs:** a descriptive phrase at the **end** of the prompt, strength 1.0 on the cards (the ComfyUI template ships 0.8 and appends the trigger with `", "`).

| Repo | Trigger (append at the end) |
|---|---|
| `krea/Krea-2-LoRA-darkbrush` | `monochrome ink wash style` |
| `krea/Krea-2-LoRA-dotmatrix` | `monochrome stippling style` |
| `krea/Krea-2-LoRA-kidsdrawing` | `naive expressive sketch style` |
| `krea/Krea-2-LoRA-neondrip` | `textured abstract style` |
| `krea/Krea-2-LoRA-rainywindow` | `rainy window style` |
| `krea/Krea-2-LoRA-retroanime` | `purple retro anime style` |
| `krea/Krea-2-LoRA-softwatercolor` | `Art Deco watercolor style` |
| `krea/Krea-2-LoRA-sunsetblur` | `ethereal motion blur style` |
| `krea/Krea-2-LoRA-vintagetarot` | `vintage tarot style` |

- **Character LoRAs** trained with a name-like token: token first, used as the subject, then stable traits, then the scene. Our prefix shape: `character_<id>_person, woman, in her twenties, dark hair, long hair, <scene prose>`.
- **Community realism LoRAs** differ: some take no trigger, some a prefix, some a suffix. Take the position from that LoRA's own card, not from blog tables.
- Do not stack style words that fight a style LoRA. fal allows at most 3 LoRAs per call, scale 0 to 4.
- **Captions for your own LoRAs** (diffusers Krea 2 DreamBooth guide): for a style, describe the content you do not want baked in and add a descriptive trigger phrase; for a character, a trigger word is fine if captions name the class, clothing, pose, setting and light, but not the face.

## Edits need an adapter

Stock Krea 2 has **no reference-conditioned edit path**. The DiT has no reference-latent or inpaint input, so a VAE reference fed through plain `CLIPTextEncode` or the Qwen-Image-Edit encode node is silently discarded. The edit routes we know are an adapter LoRA plus its patch node.

| Task | Adapter | Prompt |
|---|---|---|
| Replace the background, keep the person | AnyPaint (K/V cache on) | Only the new background plus "matching the existing light". Never the kept person |
| Paint an object into a region | AnyPaint, region = white mask | The object in plain prose plus light to match |
| Instruction edit (recolor, restyle) | `ComfyUI-Krea2-Ostris-Edit` edit LoRAs, `comfyui-krea2edit` | Imperative instruction: "recolor the car to matte black" |
| Fill a blacked-out region | `krea2-inpaint-edit` LoRA on the Ostris edit nodes | What fills the region; sample at the reference size (see below) |
| Lay out a new picture by boxes | Coordinates in the prompt; bbox LoRA optional | JSON boxes, see next section |

- **Mask convention:** white = regenerate, black = keep. Canvas in multiples of 16.
- **With the Krea2Edit adapter keep output at or below about 2 MP** (its README, single source): above its trained range source content can bleed in. AnyPaint states no such limit.
- **Removals:** the same notes say distilled Turbo at cfg 1 tends to re-render the subject and recommend Raw, cfg 3 (standard convention), about 20 steps (single source).

### Background replacement: describe only the new background

```text
A rain-washed evening street in an old European city, warm shop windows and wet cobblestones
reflecting orange light, soft haze in the distance, matching the existing light.
```

- Write the new background and ask for the light to match. Do not mention the kept person at all: not the character token, not "the woman in front", not "behind her". People in the background are fine when you want them.
- The AnyPaint card itself asks for "a prompt describing the complete desired output image". Background-only is our practice; a controlled A/B between the two has not been run.
- *In our tests* (3 renders x 2 backgrounds x 5 edit adapters, face count outside the kept-person mask; originals with the same masks: 0): a second, smaller copy of the person came mainly from sampling scale, not from the prompt. Removing the person from the prompt and dropping the character LoRA moved extra faces only from 30 to 24/25.
- *In our tests* the main cause looked like scale: the Ostris edit encoder shrinks the reference to about 1 MP (`REF_LATENT_MAX_PIXELS = 1024*1024`), and sampling a 2048 canvas redrew the person at reference scale: the face at (1092, 726), 940 px wide, reappeared at (546, 366), about 460 px wide. Sampling at the reference size and upscaling the new background removed the copy; extra faces went from 28 to 12, nearly all of them passers-by the street prompt asked for.
- In the same runs AnyPaint kept the person in place every time, so it is the adapter we use for background replacement.

### Region inpaint

- Mark the region with the mask and name the object in plain prose plus the light. The mask is the location; the prompt needs no coordinates.
- *In our tests* (AnyPaint, 2 pictures x 3 objects x 2 box shapes x 3 seeds = 72): mean absolute change outside the box stayed at or below 1.06, inside 15 to 49. Adding the bbox LoRA changed nothing measurable (bicycle 33.6 vs 33.8, dog 40.5 vs 40.9, plant 35.5 vs 34.5).
- In the same tests, a wide low strip along the bottom of a 9:16 picture drew the weakest change (15 to 26) for two of three objects; treat such boxes as suspect until checked by eye or a detector.

## Box layout (bbox LoRA)

The krea2 bbox LoRA (Civitai model 2897864) takes object boxes as JSON in 0..1000 normalised coordinates, `[x1, y1, x2, y2]`, with no trigger word. The card's Format block puts one sentence before the JSON:

```text
The all objects uses the following bbox.
{"objects": {"a golden retriever sitting": [40, 500, 420, 1000], "a red bicycle": [560, 450, 980, 1000]}}
A sunny city park with a gravel path and tall linden trees, soft afternoon light, photograph.
```

- The card's author calls the format loose ("can just write the coordinates"); the embedded example prompts vary the order, sometimes put the JSON last, and sometimes omit the sentence. A valid JSON block with sane boxes (x1 < x2, y1 < y2) is what matters.
- Author example strength 0.75. The card notes subjects tend to render large and centred, and base Krea 2 follows coordinates only sometimes and may print them as text.
- The official expansion rules forbid JSON in prompts; this block is adapter-specific. Do not add it to ordinary prompts.
- *In our tests* (6 mirrored layouts x 4 variants x 2 seeds; hit = the character's face centre inside its box): plain words 0/12, JSON coordinates without the LoRA 5/12, LoRA 0.75 3/12, LoRA 1.0 5/12. Small figures failed in every variant. Coordinates in the text alone already move the subject toward its box; the LoRA added nothing measurable at this sample size. Placement is approximate.

## Camera-angle adapter (krea2-anygles)

A Control-LoRA plus 4 ComfyUI nodes that re-render one person from a new yaw, elevation or distance, driven by a SAM 3D Body normal map and a fixed camera sentence ("Same figure. Move the camera 310 degrees to the left relative to the input view."). Author settings: 8 steps, cfg 1, strength 1.0, 384 px reference, at most about 2 MP. A plain LoRA loader drops its control projection. Details, run steps and our orbit test: [[krea-2-anygles]].

## Gotchas

- **Issue:** A Turbo image ignores the prompt entirely in ComfyUI. -> **Fix:** cfg is 0 (Krea's "0.0" copied). Set cfg 1.0.
- **Issue:** The negative prompt has no effect. -> **Fix:** Turbo at cfg 1 never computes it. Rephrase positively, use the NAG node, or switch to Raw with real CFG.
- **Issue:** The tail of a long prompt is ignored in diffusers but not in ComfyUI. -> **Fix:** The reference encoder truncates at about 507 tokens and ComfyUI does not. Shorten to under about 500 and keep essentials first.
- **Issue:** A second, smaller copy of the person appears after background replacement with an inpaint-edit adapter. -> **Fix:** The Ostris edit encoder caps the reference at about 1 MP; in our tests sampling at that size and upscaling removed the copy. Or use AnyPaint.
- **Issue:** "no people" still gives passers-by. -> **Fix:** In our one comparison negation did not remove them. Pick a place or time of day without a crowd (remedy not A/B-tested).
- **Issue:** A style LoRA looks weak. -> **Fix:** Official style triggers go at the end of the prompt; check the card for community LoRAs.
- **Issue:** Hosted Krea docs say to avoid "Turbo" for final photoreal work. -> **Fix:** That page describes hosted Medium Turbo; the open Turbo card shows photoreal outputs. Hosted and open checkpoints are not publicly mapped one to one.
- **Issue:** A size like 1250x830 runs in one tool and fails the edit adapter. -> **Fix:** Snap sides to multiples of 16 yourself before any run.

## See Also

- [[krea-2]] - release history, hosted vs open surfaces
- [[krea2-realism]] - community realism LoRA line for Krea 2
- [[krea-2-outpaint]] - outpaint adapter for Krea 2
- [[krea-2-anygles]] - camera-view adapter for one person
- [[flux-klein-9b-inference]] - the same "pin the checkpoint and runtime" discipline for FLUX.2 [klein]
- [[diffusion-lora-training]] - LoRA training as a version-bound experiment
- [[object-removal-inpainting]] - removal and inpainting outside Krea
- [[flow-matching]] - the sampler family behind Krea 2

## Sources

Official:

- Krea 2 repository, README (Turbo/Raw settings, multiples of 16): https://github.com/krea-ai/krea-2
- Prompting guide: https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md
- LLM expansion system prompt: https://github.com/krea-ai/krea-2/blob/main/docs/expansion.txt
- Encoder (template, 512 positions, truncation): https://github.com/krea-ai/krea-2/blob/main/encoder.py
- Sampler (guidance formula, padding to 16): https://github.com/krea-ai/krea-2/blob/main/sampling.py
- Turbo model card: https://huggingface.co/krea/Krea-2-Turbo
- Raw model card: https://huggingface.co/krea/Krea-2-Raw
- Technical report: https://www.krea.ai/blog/krea-2-technical-report
- Official style LoRA card (same pattern for all nine): https://huggingface.co/krea/Krea-2-LoRA-softwatercolor
- Hosted Krea 2 docs (hosted-only controls, size list): https://www.krea.ai/docs/user-guide/features/krea-2

Serving code and docs:

- diffusers Krea 2 pipeline docs: https://huggingface.co/docs/diffusers/en/api/pipelines/krea2
- diffusers pipeline source (guidance convention, 16-rounding, 512 length): https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/krea2/pipeline_krea2.py
- diffusers Krea 2 LoRA training guide: https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/README_krea2.md
- ComfyUI Krea 2 tutorial (files, official LoRA triggers): https://docs.comfy.org/tutorials/image/krea/krea-2
- ComfyUI official Turbo template: https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_krea2_turbo_t2i.json
- ComfyUI Krea 2 text encoder (template, prefix stripping): https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/text_encoders/krea2.py
- ComfyUI Qwen3-VL tokenizer (no 512 cap): https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/text_encoders/qwen3vl.py
- ComfyUI sampler (cfg 1.0 skips uncond): https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/samplers.py
- SGLang Krea 2 cookbook: https://docs.sglang.io/cookbook/diffusion/Krea/Krea-2
- DiffSynth-Studio Krea 2: https://diffsynth-studio-doc.readthedocs.io/en/latest/Model_Details/Krea-2.html
- Qwen3-VL-4B-Instruct (tokenizer for counting): https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct

Providers:

- fal, open-weights guide: https://fal.ai/learn/tools/how-to-use-krea-2-open-source
- fal, hosted-model prompting guide (predates the open release): https://fal.ai/learn/tools/krea-2-prompting-guide
- fal Turbo endpoint (no steps, guidance or negative field; the LoRA variant takes up to 3 LoRAs): https://fal.ai/models/fal-ai/krea-2/turbo
- Scenario, Krea 2 essentials: https://help.scenario.com/articles/1463593157-krea-2-the-essentials

Adapters and community:

- AnyPaint card: https://huggingface.co/yijunwang2/krea2-anypaint
- AnyPaint ComfyUI nodes: https://github.com/alexw5702-afk/krea2-anypaint
- krea2-inpaint-edit LoRA: https://huggingface.co/Cierpliwy/krea2-inpaint-edit
- Ostris edit nodes (reference at about 1 MP): https://github.com/ostris/ComfyUI-Krea2-Ostris-Edit
- Krea2Edit nodes (instructions, 2 MP, removals on Raw): https://github.com/lbouaraba/comfyui-krea2edit
- bbox LoRA card: https://civitai.com/models/2897864
- Code analysis of the missing reference path: https://github.com/ethanfel/ComfyUI-Krea2TextEncoder
- NAG node for Krea 2: https://github.com/iljung1106/ComfyUI-Krea2-NAG
- Origin of the "official caption order": https://huggingface.co/krea/Krea-2-Turbo/discussions/4
- The node that repackages it: https://github.com/WaitWut/krea2-structured-prompt
- Negation failure ("torch without flame"): https://huggingface.co/krea/Krea-2-Turbo/discussions/13
- Community ComfyUI guide (useful, but gives cfg 0.0 for ComfyUI): https://www.instasd.com/post/krea-2-prompt-and-style-guide-comfyui
- Raw-era realism LoRA with a negative list: https://huggingface.co/inlineresearch/skin-lora-krea-2-raw
- krea2-anygles nodes: https://github.com/alexw5702-afk/krea2-anygles
- krea2-anygles card: https://huggingface.co/yijunwang2/krea2-anygles
