# LoRA Weight Protection: Watermarking, Extraction Attacks, and Licensing

Date: 2026-04-03
Context: Desktop/server image generation with proprietary LoRA adapters on open-source base models (FLUX, SD). Covers protection of adapter weights from theft, forensic ownership proof, and extraction attack defense.

---

## Threat Model

LoRA adapters (delta_W = B × A, stored in `.safetensors`, 10-200 MB) have four inherent vulnerabilities:

1. **Portability** - one file, works with any copy of the same base model
2. **Compact format** - trivially shared via email, USB, cloud storage
3. **Extractability** - if base model is public, delta_W can be recovered: `delta_W = merged_model - base_model`
4. **Query-based extraction** - even API-only access permits distillation attacks

---

## LoRA-Specific Watermarking Methods

### SEAL (Entangled White-box Watermarks)

**Paper:** arxiv:2501.09284 (Jan 2025)

Embeds a secret non-trainable matrix between trainable LoRA weight matrices during training. The watermark is "entangled" with the trained weights - extracting SEAL watermark requires solving a joint optimization problem.

**Properties:**
- No quality degradation on text-to-image or instruction tuning tasks
- Resistant to: removal attacks, obfuscation, ambiguity attacks
- Verification is white-box (requires access to the model)

**Training integration:**
```python
# Pseudo-code: SEAL inserts a fixed passport matrix P
# between LoRA A and B matrices during forward pass
def forward(x, A, B, P, alpha):
    # Standard LoRA: output = x + alpha * (B @ A @ x)
    # SEAL: output = x + alpha * (B @ P @ A @ x)
    # P is non-trainable, randomly initialized at training start
    return x + alpha * (B @ P @ A @ x)
```

### AquaLoRA (White-box, SD-specific)

**Paper:** arxiv:2405.11135 (ICML 2024) | [GitHub](https://github.com/Georgefwt/AquaLoRA)

Two-stage: (1) pretrain watermark encoder/decoder in latent space; (2) embed watermark into SD U-Net via LoRA during fine-tuning.

- **Capacity:** 48 bits per model
- **Scaling matrix:** allows changing watermark payload without full retraining
- Resistant to: LoRA merge, removal attempts

### LoRAGuard (Black-box, Yin-Yang method)

**Paper:** arxiv:2501.15478 (Jan 2025)

Detects ownership without accessing internal weights:
- **Yin** (negative-weight path): detectable via negation operation on model outputs
- **Yang** (positive-weight path): detectable via addition operation

Solves the key problem that prior watermarks break under LoRA combination (merging multiple adapters) or negation. Near-100% verification success rate.

### AuthenLoRA (Output-Propagating Watermark)

**Paper:** arxiv:2511.21216 (Nov 2025) | [GitHub](https://github.com/ShiFangming0823/AuthenLoRA)

Watermark propagates into every generated image, not just the weights:
- Dual-objective optimization: jointly trains style transfer + watermark embedding
- Lightweight mapper lets you change the watermark payload without full retraining
- Detection works on image outputs - useful even if weights are stolen

### Comparison Table

| Method | Year | Box | Resists Merge | Resists Quant | Capacity |
|--------|------|-----|---------------|---------------|----------|
| AquaLoRA | 2024 | White | Yes | Partial | 48 bits |
| SEAL | 2025 | White | Yes | Yes | Embedded |
| LoRAGuard | 2025 | Black | Yes | Yes | Binary |
| AuthenLoRA | 2025 | Output | N/A (per-image) | N/A | Per-image |
| MOLM | 2024 | Routing | Yes | Yes | >0.98 accuracy |

**Recommendation for production:** SEAL for weight-level ownership + AuthenLoRA or standard output watermarking for image-level forensics. Layer both: prove you own the weights AND that specific images came from your model.

---

## Extraction Attacks

### StolenLoRA (Query-Based Distillation)

**Paper:** arxiv:2509.23594 (ICCV 2025)

Attack that recovers LoRA functionality using synthetic queries:

- **Method:** attacker generates synthetic data via LLM + diffusion, queries the target API, trains student LoRA from responses using Disagreement-based Semi-supervised Learning (DSL)
- **Cost:** ~10,000 queries, achievable in a single day by one user
- **Success rate:** 96.6% functional replication
- **Cross-backbone:** works even when attacker uses a different base model than the victim

**Implication:** API-only protection (never ship weights) is NOT sufficient. 10k requests from one user = your LoRA reconstructed.

### Merge-and-Subtract (Weight Extraction from Merged Model)

If base model is public (FLUX, SD):
```python
# Attacker recovers delta_W exactly
import torch
merged = load_state_dict("your_product_model.safetensors")
base = load_state_dict("FLUX.1-dev.safetensors")  # public
delta_W = {k: merged[k] - base[k] for k in merged}
# delta_W ≈ your LoRA (full-rank, functionally equivalent)
```

`unfuse_lora()` in Diffusers uses this same math. Merging with an open-source base provides **no protection** if the attacker knows the base model (and they do - it's public).

**Partial mitigations (lower effectiveness):**
- INT4/INT8 quantize after merge (degrades reconstruction precision)
- Fine-tune on noise for a few steps after merge (blurs delta boundary)
- Merge multiple LoRAs (harder to factor out one)

**Effectiveness of merge-as-protection: 2/10**

### Membership Inference on LoRA

**Paper:** arxiv:2507.18302 (Jul 2025)

Membership Inference Attacks (MIA) can determine whether specific images were in the training dataset by querying the LoRA. Relevant for trade secret and GDPR compliance: training data membership can be inferred from model behavior.

---

## Defense Strategies

### Against Query-Based Extraction (StolenLoRA)

```python
# Server-side: detect extraction patterns
def detect_extraction_query(user_id: str, request: dict) -> float:
    """Returns extraction suspicion score 0-100"""
    history = get_request_history(user_id, hours=24)
    
    score = 0
    # High volume from single user
    if len(history) > 500: score += 30
    if len(history) > 2000: score += 50
    
    # Uniform/grid-like inputs (systematic sampling)
    if _is_systematic_sampling(history): score += 40
    
    # Inputs similar to known synthetic datasets
    if _resembles_synthetic_grid(request): score += 20
    
    return min(score, 100)
```

**Countermeasures:**
- Rate limiting per license (50-100 inferences/day soft cap, 500/day hard cap)
- Output perturbation: add minimal invisible noise that degrades student training without affecting user quality
- API fingerprinting: embed per-user watermark in all API outputs (AuthenLoRA-style)
- Query pattern anomaly detection (systematic inputs = grid sampling = extraction)

### Against Memory Dump of Decrypted Weights

Once weights are decrypted for inference, they exist in RAM. Mitigation:

- Use `VirtualLock()` (Windows) / `mlock()` (macOS/Linux) on weight buffers to prevent paging to disk
- Clear weight buffers immediately after session ends (`sodium_memzero()`)
- CORELOCKER pattern: serve critical tensors from server, never store locally

```cpp
// Lock weight buffer in RAM, prevent swap to pagefile
VirtualLock(tensor_buffer, tensor_size);
// ... run inference ...
sodium_memzero(tensor_buffer, tensor_size);
VirtualUnlock(tensor_buffer, tensor_size);
```

---

## ComfyUI Runtime Encryption (ComfyUI-LMCQ)

**GitHub:** [github.com/sebord/ComfyUI-LMCQ](https://github.com/sebord/ComfyUI-LMCQ)

Practical hardware-bound encryption for ComfyUI deployments:

**Machine code generation:**
```
GPU ID + CPU serial + MAC address + disk serial + motherboard ID
-> HMAC-SHA256 -> machine_code
```

**Workflow:**
1. Generate `machine_code` on the target machine
2. Encrypt LoRA file bound to authorized `machine_code` list
3. Runtime decrypt node verifies `machine_code` before loading
4. Model lives in memory only - no decrypted file written to disk

**Limitations:**
- Hardware spoofing bypasses machine binding
- VMs have unstable hardware IDs (breaks on snapshot restore)
- Cloud GPU instances rotate hardware IDs on instance replacement
- After decryption, weights are in RAM - memory dump still possible

---

## FLUX License Constraints

| Model | License | Commercial use |
|-------|---------|----------------|
| FLUX.1 [dev] | Non-Commercial v2.0 | Not permitted without BFL agreement |
| FLUX.2 Klein 4B | Apache 2.0 | Fully permitted |
| FLUX.2 Klein 9B | Non-Commercial | Requires BFL commercial license |
| Stable Diffusion 1.5/SDXL | CreativeML Open RAIL-M | Permitted with use-restrictions |

**LoRA derivatives inherit use-based restrictions** from the base model license but do NOT need to be released as open-source. A LoRA trained on FLUX.1 [dev] cannot be used commercially without a BFL license, regardless of whether you own the LoRA.

For production retouching applications: use Klein 4B (Apache 2.0, no restrictions) or obtain a commercial BFL license for Klein 9B.

---

## Fingerprinting for Legal Ownership Proof

### Chain & Hash (arxiv:2407.10887)

Cryptographically binds fingerprint prompts to responses. Owner stores (prompt, expected_response) pairs - demonstrates output is deterministic only from their model. Serves as ownership evidence in dispute.

### LoRA-FP Framework (arxiv:2509.00820)

Plug-and-play fingerprint embedding via constrained fine-tuning:
- Fingerprint transfers to derivative models via parameter fusion
- Lower compute cost than full-parameter approaches
- Survives incremental fine-tuning

### RoFL (arxiv:2505.12682)

Fingerprint via statistical output patterns:
- Resistant to fine-tuning, pruning, quantization
- Uses cryptographic commitments (hash published before deployment = pre-registration)
- Provides court-admissible evidence: "We registered fingerprint X before your model appeared"

---

## Gotchas

- **Merge-and-subtract defeats all weight encryption if base model is public.** Encrypting the merged model file is useless if the base model is publicly available and the attacker knows which base was used. Only protect standalone LoRA files or use a private base.
- **StolenLoRA makes "API only" a false security.** 10,000 queries in a day is normal usage for a professional photographer. Rate limiting must be combined with behavioral detection (grid-sampling patterns, uniform image characteristics), not just a request count.
- **FHE (Homomorphic Encryption) for inference is ~1000x slower.** PrivTuner and similar papers show FHE inference on LoRA is theoretically possible but orders of magnitude too slow for interactive image generation. Not viable as of 2026.
- **AuthenLoRA watermark in outputs can be probed by attackers.** If the attacker can detect whether their extracted copy outputs the same watermark pattern, they can verify their extraction succeeded. Keep the watermark decoder server-side only.
- **ComfyUI `.ckpt`/`.pt` format allows arbitrary code execution via pickle.** Always use `.safetensors` for LoRA distribution and loading. `.safetensors` was security-audited; pickle is not.
- **LoRAGuard Yin-Yang method requires specific inference setup.** Detection requires running the model with negation or addition operations that are not part of normal inference. If you don't preserve the verification protocol, you lose the ability to prove ownership later.

## See Also
- [[watermarking-encrypted-models]]
- [[hkdf-personalized-weights]]
- [[model-weight-encryption]]
- [[output-scrambling-antipiracy]]
- [[anti-piracy-legal]]
