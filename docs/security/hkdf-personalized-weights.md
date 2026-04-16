# HKDF + ChaCha20 Personalized Neural Network Weights

Date: 2026-04-03
Context: Desktop C++ app, ONNX Runtime inference. Per-user unique weights via HKDF-derived seed + ChaCha20 stream. Functionally equivalent models - permutation symmetry ensures identical output.

---

## Core Concept

Server holds `master_secret`. Per-user HKDF derivation → seeds for 3 operations:
- **Permutation** - neuron index shuffling (lossless, mathematically equivalent)
- **Scale** - multiplicative weight perturbation (~±3%)
- **Offset** - additive weight perturbation (~±0.5% of weight magnitude)

Each user's model weights are unique while producing identical outputs (within floating point tolerance).

---

## HKDF + ChaCha20 Implementation

### Why This Combination

**HKDF alone:** limited to 255 × HashLen = 8160 bytes for SHA-256. Insufficient for 100M+ parameter models.

**Solution:** HKDF generates 32-byte seeds → ChaCha20 expands into arbitrary-length stream.

```bash
master_secret (32 bytes, on server)
    │
HKDF-Extract(salt=epoch_bytes, ikm=master_secret) → PRK
    │
HKDF-Expand(PRK, info="user:{account_id}:perm")   → seed_perm  (32 bytes)
HKDF-Expand(PRK, info="user:{account_id}:scale")  → seed_scale (32 bytes)
HKDF-Expand(PRK, info="user:{account_id}:offset") → seed_offset (32 bytes)
    │
ChaCha20(key=seed_perm,   nonce=0) → stream for permutations
ChaCha20(key=seed_scale,  nonce=0) → stream for scale factors
ChaCha20(key=seed_offset, nonce=0) → stream for offsets
```

### Library Choice

| Library | HKDF | Speed | API |
|---------|------|-------|-----|
| OpenSSL 3.x | EVP_KDF | Best (HW SHA-256) | Verbose boilerplate |
| libsodium 1.0.19+ | `crypto_kdf_hkdf_sha256_*` | ~20% slower | Simple, misuse-resistant |
| Standalone (RFC 5869) | Custom | Depends on HMAC | Full control |

**Recommendation: libsodium.** Already needed for other crypto ops. ChaCha20 at ~1705 MiB/s without AES-NI (important for weak GPU machines).

**ChaCha12 vs ChaCha20:** 12 rounds ~1.6× faster. Sufficient for this threat model (PRNG, not encryption). Estimated total personalization time for 100M-parameter model: <500ms on slow CPU.

### Code (libsodium)

```cpp
#include <sodium.h>
#include <vector>
#include <cstring>

struct PersonalizationSeeds {
    uint8_t perm[32];
    uint8_t scale[32];
    uint8_t offset[32];
};

// Step 1: Derive per-user seeds from master secret
PersonalizationSeeds derive_seeds(
    const uint8_t master_secret[32],
    const char* account_id,
    uint32_t epoch)
{
    PersonalizationSeeds seeds;
    uint8_t salt[4] = {
        (uint8_t)(epoch >> 24), (uint8_t)(epoch >> 16),
        (uint8_t)(epoch >> 8),  (uint8_t)(epoch)
    };

    uint8_t prk[crypto_kdf_hkdf_sha256_KEYBYTES];
    crypto_kdf_hkdf_sha256_extract(prk, salt, sizeof(salt),
                                    master_secret, 32);

    char info_perm[128], info_scale[128], info_offset[128];
    snprintf(info_perm,   sizeof(info_perm),   "user:%s:perm",   account_id);
    snprintf(info_scale,  sizeof(info_scale),  "user:%s:scale",  account_id);
    snprintf(info_offset, sizeof(info_offset), "user:%s:offset", account_id);

    crypto_kdf_hkdf_sha256_expand(seeds.perm,   32, info_perm,   strlen(info_perm),   prk);
    crypto_kdf_hkdf_sha256_expand(seeds.scale,  32, info_scale,  strlen(info_scale),  prk);
    crypto_kdf_hkdf_sha256_expand(seeds.offset, 32, info_offset, strlen(info_offset), prk);
    return seeds;
}

// Step 2: Generate float stream from ChaCha20 seed
std::vector<float> generate_float_stream(
    const uint8_t seed[32], size_t count, float min_val, float max_val)
{
    std::vector<float> result(count);
    uint8_t nonce[crypto_stream_chacha20_NONCEBYTES] = {0};
    size_t byte_count = count * sizeof(uint32_t);
    std::vector<uint8_t> stream(byte_count);
    crypto_stream_chacha20(stream.data(), byte_count, nonce, seed);

    float range = max_val - min_val;
    for (size_t i = 0; i < count; i++) {
        uint32_t raw;
        memcpy(&raw, &stream[i * 4], 4);
        float u = (float)(raw >> 8) / (float)(1 << 24); // uniform [0, 1)
        result[i] = min_val + u * range;
    }
    return result;
}

// Step 3: Generate permutation (Fisher-Yates with deterministic PRNG)
std::vector<uint32_t> generate_permutation(const uint8_t seed[32], uint32_t n)
{
    std::vector<uint32_t> perm(n);
    for (uint32_t i = 0; i < n; i++) perm[i] = i;

    uint8_t nonce[crypto_stream_chacha20_NONCEBYTES] = {0};
    std::vector<uint8_t> stream(n * sizeof(uint32_t));
    crypto_stream_chacha20(stream.data(), n * sizeof(uint32_t), nonce, seed);

    for (uint32_t i = n - 1; i > 0; i--) {
        uint32_t raw;
        memcpy(&raw, &stream[i * 4], 4);
        uint32_t j = raw % (i + 1); // negligible bias for n < 2^24
        std::swap(perm[i], perm[j]);
    }
    return perm;
}
```

### OpenSSL 3.x Alternative

```cpp
EVP_KDF *kdf = EVP_KDF_fetch(NULL, "HKDF", NULL);
EVP_KDF_CTX *kctx = EVP_KDF_CTX_new(kdf);
OSSL_PARAM params[5], *p = params;
*p++ = OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_DIGEST,
       SN_sha256, strlen(SN_sha256));
*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_KEY,
       master_secret, 32);
*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_INFO,
       info, info_len);
*p++ = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SALT,
       salt, salt_len);
*p = OSSL_PARAM_construct_end();
EVP_KDF_derive(kctx, out, 32, params);
EVP_KDF_CTX_free(kctx);
EVP_KDF_free(kdf);
```

More boilerplate, heavier dependency, no convenient ChaCha20 stream API.

---

## Permutation Symmetry: Which Layers Can Be Permuted

### Theory

**Permutation symmetry** (arxiv:2506.13018, arxiv:2502.17391): For a FC layer with n neurons, n! equivalent parameterizations exist giving **identical output**. Permuting neuron i→j requires:
1. Permute row i→j in output weight matrix of this layer
2. Permute column i→j in input weight matrix of **next** layer
3. Permute corresponding biases

**Papers confirming quality preservation:**
- NeuPerm (arxiv:2510.20367): permuting hidden layers of LLM = <0.01% accuracy drop
- Git Re-Basin (arxiv:2209.04836): exploits same symmetry for model merging

### Layer-by-Layer Rules

| Layer Type | Safe to Permute? | What to Permute | Constraints |
|------------|-----------------|-----------------|-------------|
| **Fully Connected** | YES | W_out rows + W_in columns + bias | Classic permutation symmetry |
| **Conv2d (hidden)** | YES | Output channels = "neurons". Permute output ch of current + input ch of next + bias | Same as FC |
| **Grouped Conv** | PARTIAL | Only within each group | Groups cannot be swapped |
| **Depthwise Conv** | NO | 1 filter = 1 channel, permutation meaningless | |
| **Attention Q/K/V** | PARTIAL | Permute attention heads as whole units | Cannot permute neurons within a head without consistent Q,K,V permutation |

### Layers That CANNOT Be Permuted Independently

| Layer | Why | Consequence |
|-------|-----|-------------|
| **BatchNorm** | Stores per-channel running_mean/var | Must permute BN params together with preceding conv |
| **LayerNorm** | gamma/beta tied to feature positions | Same - permute with preceding layer |
| **Skip connections (residual)** | Input and output must share order | Permutation in block must be cancelled at output (P_out = P_in^(-1)) |
| **Input layer** | Channels tied to RGB | Never permute input channels |
| **Output layer** | Channels tied to task (RGB output) | Never permute output channels |

### U-Net Specifics

U-Net with skip connections is the most complex case:

```yaml
Encoder:              Decoder:
conv1 → pool ----skip---→ upconv4 + concat
conv2 → pool ----skip---→ upconv3 + concat
conv4 (bottleneck)  ---→ upconv1
```

Rules:
1. **Bottleneck (conv4):** SAFE. No skip connection; channels are self-contained.
2. **Encoder conv within block:** SAFE if permutation propagates through block and cancels before skip.
   - Permute output channels of conv1 → permute BN1 → permute input channels of conv2
   - Do NOT touch output channels of conv2 (they go into skip)
3. **Skip connection channels:** Must match decoder input after concat. Permuting encoder output requires matching decoder permutation.
4. **Attention heads (Stable Diffusion U-Net):** Permute entire heads (8 heads = 8! = 40320 variants - too few for security).

### Practical Strategy for Retouching Model

**Permute only: bottleneck + internal conv layers within residual blocks.**

Security gains:
- Bottleneck with 512 channels: 512! ~ 10^1166 permutations
- Each conv-block with 256 channels: 256! ~ 10^507
- Combined: astronomically large search space

Do NOT touch: input/output layers, skip connection boundaries.

---

## Scale/Offset Injection

### Safe Perturbation Ranges

| Layer Type | Scale Range | Offset Range | Notes |
|------------|-------------|--------------|-------|
| Conv2d (hidden) - conservative | 0.97 - 1.03 | ±0.005 | **Recommended** |
| Conv2d (hidden) - standard | 0.95 - 1.05 | ±0.02 | Risk of visible degradation |
| Linear (hidden) | 0.95 - 1.05 | ±0.01 | FC weights usually larger, less sensitive |
| BatchNorm gamma/beta | 0.98 - 1.02 | ±0.01 | BN sensitive - small perturbations only |
| Attention Q/K/V | 0.97 - 1.03 | ±0.005 | Dot product amplifies errors quadratically |
| First/last layer | **DO NOT TOUCH** | **DO NOT TOUCH** | Direct impact on input/output mapping |

### Why Offset is More Dangerous Than Scale

Scale 0.97-1.03 = ±3% deviation. For typical conv weight ~0.05 this is ±0.0015 (small).

Offset ±0.02 for same weight = ±40% of value (catastrophic for small weights).

**Better approach: relative offset proportional to weight magnitude:**

```cpp
// w' = w * scale + offset * |w|
// offset here is a coefficient, not absolute value
float perturbed = weight * scale + offset_coeff * fabsf(weight);
```

This keeps perturbations proportional to weight magnitude.

### Functional Equivalence Verification

After personalization, verify output matches reference:

```cpp
// Run original and personalized model on same input
// Maximum acceptable per-pixel difference: ~0.001 (float32)
// PSNR should remain > 50 dB
float max_diff = 0.0f;
for (size_t i = 0; i < output_size; i++)
    max_diff = std::max(max_diff, fabsf(orig[i] - personalized[i]));
assert(max_diff < 1e-3f); // permutation must be lossless
```

Permutation should be **exactly** lossless (max_diff ≈ FP32 epsilon). Scale/offset will introduce small perturbations.

---

## Epoch Rotation

Epoch field in HKDF derivation allows periodic key rotation without weight regeneration:

```cpp
// info = "user:{account_id}:perm:epoch:{epoch_num}"
// Each epoch produces completely different permutation for same account
// Leaked weights from epoch N are useless after epoch increment
snprintf(info_perm, sizeof(info_perm),
    "user:%s:perm:epoch:%u", account_id, epoch);
```

Epoch update triggers:
- Model update (every 2-4 weeks)
- Suspected compromise of specific account(s)
- Scheduled rotation (e.g. every 90 days)

Server stores only: `{account_id, epoch, master_secret}` (~300 bytes/user). All personalized weights computed on-demand. 1M users = ~12 req/sec at typical usage = fits on $20/month VPS.

## INT8 Quantization Constraints

Scale/offset perturbations must survive INT8 quantization if used:

```
INT8 range: [-128, 127] → float range ≈ [-1.0, 1.0] (typical scale ~0.0078)
Minimum distinguishable delta: 1 LSB = 0.0078

Safe perturbation for INT8:
  scale: 0.998 - 1.002 (not 0.95-1.05 - these cause LSB collapse)
  offset: ±0.001 * abs(w) (relative)
```

FP16 is more permissive: 1 LSB ≈ 6e-5 (half exponent range). Scale 0.97-1.03 safe for FP16.

## ONNX Weight Swap

Load base model, apply permutation in-memory, run inference - no model file modification needed:

```python
import onnx
import numpy as np

def apply_permutation_to_session(model_bytes: bytes, perm: list[int],
                                  layer_name: str) -> bytes:
    model = onnx.load_from_string(model_bytes)
    for init in model.graph.initializer:
        if init.name == layer_name + ".weight":
            w = np.frombuffer(init.raw_data, dtype=np.float32).reshape(init.dims)
            # Permute output channels (rows)
            w_perm = w[perm, ...]
            init.raw_data = w_perm.tobytes()
    return model.SerializeToString()
```

For C++ via ONNX C API: modify `OrtValue` tensors before session creation using `CreateTensorWithDataAsOrtValue` with permuted buffer.

## Gotchas

- **HKDF-Expand info strings must be unique per purpose.** Using the same info for perm and scale seeds produces the same key - completely breaking the purpose. Always use distinct labels.
- **Fisher-Yates modulo bias:** `raw % (i+1)` is slightly biased when i+1 is not a power of 2. For permutations of n < 2^24 this bias is negligible (< 10^-7). For cryptographic quality shuffle, use rejection sampling.
- **ChaCha20 nonce=0 is safe here** because each seed is a unique 256-bit key (derived from different HKDF info strings). Different key = different stream regardless of nonce.
- **Permuting BatchNorm separately from conv corrupts the model.** Always co-permute: `{conv.weight, conv.bias, bn.weight, bn.bias, bn.running_mean, bn.running_var}`.
- **Skip connections in U-Net require paired permutations.** Permuting only the encoder side without matching the decoder input will produce wrong outputs at skip-concat points.
- **Attention head permutation gives only n_heads! variants** (e.g., 8! = 40320 for 8 heads). Not enough for security. Permute neurons within heads in a consistent Q,K,V manner instead.
- **Scale/offset perturbations accumulate across layers.** In deep networks (50+ layers), even 0.3% perturbation per layer compounds. Always test final output PSNR, not just per-layer metrics.
- **Master secret leakage = all users compromised.** Store master_secret in HSM or secure enclave on server. Never ship it to clients.
- **INT8 quantization collapses large perturbations.** Scale 0.95-1.05 maps to same INT8 bucket → personalization disappears. Use scale 0.998-1.002 for quantization-compatible models.
- **Weight averaging attack:** adversary averages K users' personalized weights hoping permutation cancels. Permutation prevents this (neurons in different positions), but scale/offset does not - additional defense needed if averaging is realistic threat.

## See Also
- [[watermarking-encrypted-models]]
- [[output-scrambling-antipiracy]]
- [[licensing-implementation-cpp]]
