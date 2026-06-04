# CDM — Continuous-Time Distribution Matching Distillation

[[flow-matching]] distillation to 4 NFE without GAN or reward model. Covers SD3-Medium and Longcat-Image; porting matrix for SD3.5, SANA, and FLUX.1-dev included.

## Key Facts

| Property | Value |
|---|---|
| Full name | Continuous-Time Distribution Matching |
| arxiv | [2605.06376](https://arxiv.org/abs/2605.06376) |
| Code | [github.com/byliutao/cdm](https://github.com/byliutao/cdm) |
| Tested on | SD3-Medium, Longcat-Image (4-NFE turbo) |
| NFE target | 4 |
| Loss type | Distribution matching — no GAN, no reward model |
| Noise formulation | `xt = (1 - σ) * x0 + σ * noise` (flow-matching, sigma-based) |
| Sigma schedule | `[1.0, 0.75, 0.5, 0.25]` (SD3 convention) |
| Sigma sampling | Logit-normal (CDM branch); uniform / uniform-capped (CFG / DDM branches) |
| Minimum GPUs | 8 (FSDP2 hard minimum in training code) |
| Relation to DMD | Evolution of DMD — continuous-time rather than discrete anchor points |

**Three loss branches**: CFG, DDM, CDM — each with independent sigma sampling strategy. Student/fake-teacher architecture; no discriminator network.

**Published HF checkpoints**: [SD3-Medium-Turbo](https://huggingface.co/byliutao/stable-diffusion-3-medium-turbo), [Longcat-Image-Turbo](https://huggingface.co/byliutao/Longcat-Image-Turbo).

**Cross-references**: [[diffusion-inference-acceleration]] (runtime speedups — orthogonal to distillation), [[flow-matching]] (theoretical basis), [[MMDiT]] (target architecture family), [[SANA]] (competing 1-step baseline via adversarial sCM+LADD).

## Method

**Distribution matching objective**: student is trained to match the output distribution of the teacher across the full continuous-time sigma trajectory, not at fixed discrete anchors. This avoids the mode collapse that adversarial losses (LADD, GAN-D) produce when the discriminator overpowers the generator.

**Adapter pattern** — CDM uses `create_model_adapter(base_model_type, config)`. Each supported backbone is a separate adapter class:

```python
# Adapter interface — methods required per new backbone
class NewModelAdapter:
    def load_pipeline(self, model_name, **kwargs): ...    # via diffusers
    def get_lora_target_modules(self) -> list[str]: ...
    def get_text_encoders(self) -> list: ...
    def get_tokenizers(self) -> list: ...
    def student_forward(self, *args, **kwargs): ...
    def teacher_forward(self, *args, **kwargs): ...
```

Adding a new backbone also requires:
1. Config function in `config/config.py` (alongside existing `sd3()` / `longcat()`)
2. Optionally `wrap_*_for_fsdp()` if the model has non-standard layer types

Core training loop is **not modified** when porting — adapter layer absorbs all architecture differences.

**Reference training config (SD3-Medium)**:

```yaml
batch_size: 16          # SD3 / 8 for Longcat
lr_student: 1.0e-5
lr_fake_teacher: 5.0e-6
epochs: 4001            # 2001 for Longcat
student_update_ratio: 2
parallelism: FSDP2, 8 processes
```

## Porting Matrix

| Target | Effort | Key blocker | Compute estimate | Notes |
|---|---|---|---|---|
| **SD3.5 Medium** | Lowest | None — same [[MMDiT]] family as SD3-Medium | ~12-24 h on 8×H100 (~$480-670) | Best first validation target |
| **SD3.5 Large** | Low | Checkpoint swap only | ~24-48 h on 8×H100 | Scale up after Medium validates |
| **PixArt-Σ** | Low | DiT + flow-matching, 0.6 B | Cheap; good cross-validation | Useful sanity check before Sana |
| **SANA 0.6B / 1.6B** | Medium | Adapter class for linear-attention [[SANA]] arch | ~0.5-2 h on 8×A100 (SiD-DiT ref) | SANA-Sprint already exists (1-step); use CDM only if non-adversarial stability needed |
| **FLUX.1-dev** | High | Distilled guidance embedding — no explicit unconditional branch for CFG loss; DMD-family convergence instability on FLUX | ~140 GPU-h on 8×B200 192 GB (SiD-DiT ref for 1024²) | Requires SenseFlow-style IDA + ISG patches; consider SenseFlow first |
| **FLUX.1-schnell** | N/A | Already distilled (4 steps) | — | Distilling a distilled model yields negligible gain |
| **SDXL / SD 1.5** | Not applicable | Epsilon-prediction, not flow-matching — sigma schedule requires full rewrite | — | Different parametrization family |
| **Video (Wan2.x, CogVideo)** | Not applicable | Temporal axis not handled by current objective | — | Requires new temporal CDM formulation |
| **3D generation** | Not applicable | Different parametrization | — | — |

**FLUX.1-dev detail**: `FLUX-dev` encodes guidance via a distilled embedding rather than an explicit CFG branch. CDM's CFG loss requires an unconditional branch. Options: disable the CFG loss branch (degrades stability), or apply SenseFlow-style IDA (Implicit Denoising Alignment) + ISG (Implicit Score Guidance) patches — see [SenseFlow arxiv 2506.00523](https://arxiv.org/html/2506.00523) / [github.com/XingtongGe/SenseFlow](https://github.com/XingtongGe/SenseFlow).

**FLUX sigma convention**: SenseFlow uses shifted sigmas `[0.512, 0.759, 0.904, 1.0]` instead of the SD3 default `[1.0, 0.75, 0.5, 0.25]`. Adjust before training.

**SANA vs SANA-Sprint trade-off**: SANA-Sprint achieves 1-step generation (0.1 s on H100, 64.7× faster than FLUX-schnell) using sCM + LADD (adversarial). CDM gives 4-step non-adversarial generation — worse step count but potentially more distribution coverage stability on diverse prompts.

**Recommended porting order** (risk-ascending):

```text
1. SD3.5 Medium    → validate pipeline, cheapest
2. PixArt-Σ        → cross-validate on different small backbone
3. SANA 1.6B       → only if SANA-Sprint shows mode collapse
4. FLUX.1-dev      → only after 1-3 done; consider SenseFlow as alternative
```

## Gotchas

- **Issue:** FSDP2 initialization fails with fewer than 8 processes -> **Fix:** CDM training code hard-codes 8-process FSDP2 sharding. There is no single-GPU or 4-GPU mode; minimum viable setup is 8 GPUs. Do not attempt to patch FSDP2 group size without rewriting the sharding strategy.

- **Issue:** Applying CDM to FLUX.1-dev produces diverging loss or NaN after warmup -> **Fix:** Vanilla DMD2 (CDM's ancestor) is explicitly documented in the SenseFlow paper as having "difficulty converging" on FLUX. Apply SenseFlow's IDA and ISG patches before training. These patches stabilize the implicit score matching term when the model lacks an explicit unconditional branch.

- **Issue:** Sigma schedule mismatch when porting from SD3 to FLUX causes quality degradation at inference -> **Fix:** FLUX and SD3 use different sigma conventions. SD3 default `[1.0, 0.75, 0.5, 0.25]`; FLUX uses shifted sigmas (SenseFlow: `[0.512, 0.759, 0.904, 1.0]`). Update the adapter's sigma schedule before distillation, not just at inference.

- **Issue:** Running distillation as a serverless job times out or loses state mid-training -> **Fix:** CDM distillation is a multi-hour to multi-day training run (SD3.5 ~12-24 h; FLUX ~140 h). Serverless containers with `idleTimeout` will be killed. Use persistent Pod mode with SSH access and checkpoint resume enabled.

- **Issue:** Distilling FLUX.1-schnell produces negligible improvement -> **Fix:** FLUX-schnell is already a 4-step distilled model. CDM's target NFE is also 4. Distilling an already-distilled model at the same step count yields near-zero quality gain for significant compute cost. Use FLUX.1-dev as the teacher instead.

## See Also

- [[diffusion-inference-acceleration]] — runtime inference speedups (Spectrum, Nunchaku quantization, sampler optimization) — orthogonal to distillation
- [[flow-matching]] — continuous-time flow matching formulation underlying CDM's noise trajectory
- [[MMDiT]] — transformer architecture used by SD3/SD3.5 (lowest-effort CDM targets)
- [[SANA]] — SANA-Sprint 1-step adversarial baseline; use CDM when non-adversarial stability matters
- [[flux-klein-9b-architecture]] — FLUX.2 Klein 9B architecture context; CDM applicable to FLUX.1-dev (not schnell)
- [[diffusion-lora-training]] — LoRA target modules referenced in CDM adapter interface
- [SenseFlow (arxiv 2506.00523)](https://arxiv.org/html/2506.00523) — FLUX/SD3.5-specific DMD patches (IDA + ISG); prerequisite for stable FLUX CDM porting
- [SiD-DiT (arxiv 2509.25127)](https://arxiv.org/html/2509.25127) — score identity distillation covering FLUX, Sana, SD3-Medium, SD3.5 explicitly; compute reference for FLUX 1024²
- [SANA-Sprint (arxiv 2503.09641)](https://arxiv.org/html/2503.09641v1) — 1-step sCM+LADD baseline for SANA
