# Watermarking Neural Network Outputs + .hmod Encrypted Model Format

Date: 2026-04-03
Context: C++ desktop retouching app. Invisible watermark per output image; models stored in encrypted .hmod format with per-tensor AES-256-GCM + Ed25519 header signing.

---

## Invisible Watermarking

### StegaStamp (CVPR 2020)

Source: Matthew Tancik et al. (UC Berkeley). Repo: https://github.com/tancik/StegaStamp

**Encoder architecture:**
- Input: 400×400×3 RGB + 100-bit message
- Message → FC layer → 50×50×3 → upsample → 400×400×3
- Concat with image → 400×400×4
- U-Net → residual 400×400×3
- Output: original + clipped residual

**Decoder:**
- Input: encoded image (possibly distorted)
- Spatial Transformer Network (STN) for perspective correction
- Conv layers + FC → sigmoid → 100-bit probabilities

**Error correction:** BCH(100, 56): 100 bits total = 56 data bits + 44 ECC bits.

**C++ via ONNX Runtime:**

```
tf2onnx: TF 1.13 checkpoint → freeze_graph → tf2onnx → .onnx
```

Key ONNX Runtime API: `CreateSessionFromArray()` - load model from decrypted in-memory buffer. No plaintext model ever written to disk.

**Execution providers:**
- Windows: DirectML EP (any DX12 GPU: NVIDIA/AMD/Intel)
- macOS: CoreML EP (Apple Neural Engine)

**Performance:**

| Resolution | CPU (i7-12700) | GPU (RTX 3060) |
|------------|----------------|----------------|
| 400×400 (native) | 15-30 ms | 3-8 ms |
| 1024×1024 | 100-200 ms | 15-30 ms |
| 2048×2048 | 200-400 ms | 25-50 ms |

StegaStamp operates on fixed 400×400. Options for larger images:
- A: resize → embed → resize back (fast, some detail loss in watermark)
- B: tile-based (embed in each tile, redundant, robust to crop)
- C: use TrustMark (arbitrary resolution)

**Memory overhead:** ~100-150 MB (model ~30 MB + ONNX Runtime buffers).

### TrustMark (Adobe, ICCV 2025)

Repo: https://github.com/adobe/trustmark

**Advantages over StegaStamp:**
- Arbitrary resolution (no 400×400 constraint)
- 100-bit payload with configurable ECC (BCH_SUPER, BCH_5, BCH_4, BCH_3)
- ONNX models already available (used in JS implementation)
- PSNR ~50 dB (artifacts nearly invisible)
- Designed for C2PA (Content Authenticity Initiative)
- Rust implementation available for FFI

**RECOMMENDATION: TrustMark over StegaStamp** for new implementations - no resize, already ONNX, actively maintained (2025).

### DCT Spread Spectrum (no-model alternative)

```cpp
void embed(cv::Mat& image, uint64_t payload, const Key& key) {
    cv::Mat dct_image;
    cv::dct(image_float, dct_image);
    PRNG prng(key);
    for (int bit = 0; bit < 48; bit++) {
        auto coeffs = select_mid_freq_coeffs(dct_image, prng);
        float delta = (payload >> bit & 1) ? +strength : -strength;
        for (auto& c : coeffs) c += delta;
    }
    cv::idct(dct_image, image_float);
}
```

**DCT vs Neural:**

| Criterion | DCT Spread Spectrum | Neural (StegaStamp/TrustMark) |
|-----------|--------------------|-----------------------------|
| Model size | 0 MB | 15-30 MB |
| Speed | <5ms | 15-200ms |
| JPEG Q=90 | 85-95% bits | 98%+ bits |
| JPEG Q=70 | 60-80% bits | 95%+ bits |
| Crop 20% | 30-50% bits | 90%+ bits |
| Print-scan | ~50% | 95%+ bits |

**Neural is mandatory for anti-piracy.** DCT too easily broken by crop + JPEG.

### Robustness (WAVES Benchmark, NeurIPS 2024)

StegaStamp robustness:

| Attack | Bit Accuracy |
|--------|-------------|
| JPEG Q=90 | ~99% |
| JPEG Q=70 | ~96-98% |
| JPEG Q=50 | ~92-95% (BCH corrects) |
| Resize 50%+back | ~96% |
| Screenshot | ~94-97% |
| Blur/noise | ~95-99% |
| Print + scan | ~95% (primary use case!) |
| Diffusion regeneration | ~70-85% (vulnerable) |
| Adversarial attack | ~60-80% |

### Payload Design (64-bit recommended)

```
[32 bits: license_id hash]
[16 bits: timestamp - days since 2025-01-01] = 180 years coverage
[8 bits: app_version + model_version]
[8 bits: CRC-8 or additional ECC]
```

With TrustMark (100 bits): 64 data bits + 36 bits ECC.
With StegaStamp BCH(100,56): 48 data bits fit comfortably in 56-bit data payload.

**Trial watermark:** `license_id = 0x00000000` (reserved). Invisible tracking + visible overlay (two layers).

### Decoder Tool

```
hmod_watermark_check <image_or_dir> [--batch] [--output report.json]

Output:
{
  "file": "photo.jpg",
  "watermark_detected": true,
  "confidence": 0.97,
  "payload": {
    "license_id": "a3f8c91b",
    "timestamp": "2026-03-15",
    "version": 2
  },
  "bits_above_90pct": 45,
  "bits_above_80pct": 48
}
```

False positive rate: ~1 in 10^6 at threshold 0.8. Recommended threshold: 0.85.

---

## .hmod Encrypted Model Format

### Why AES-256-GCM

- **GCM = encrypt + authenticate in one pass.** CBC needs separate HMAC.
- GCM detects tampering automatically (auth tag).
- GCM parallelizes (counter mode); CBC doesn't (depends on previous block).
- AES-NI throughput: GCM ~2.2 GB/s, CBC ~1.5 GB/s.

**Per-tensor nonce (12 bytes):** must be unique per encryption under same key.
- Random IV: `crypto_random_bytes(12)` - simple, safe for <2^48 ops
- Derived IV: `HKDF(key, tensor_name + counter)` - deterministic

**Recommendation: random IV.** One-time encryption (at build time) means nonce reuse is impossible by construction.

### HKDF Key Derivation

```
HKDF-SHA256(
  input_key_material = device_fingerprint || license_key,
  salt = random_salt (32 bytes, stored in file header),
  info = "hmod-v1-tensor-decryption",
  output_length = 32
)
```

### File Format Specification

```
Offset    Size        Content
──────    ────        ───────
0         4           Magic: "HMOD" (0x484D4F44)
4         2           Version: uint16 LE (currently 1)
6         2           Flags: uint16 LE (bit0: all_encrypted, bit1: critical_only)
8         4           Header size: uint32 LE
12        header_size Binary header (NOT JSON):
                        - num_tensors: uint32
                        - salt: 32 bytes (for HKDF)
                        - encrypted_MCK: 32+12+16 bytes (ciphertext+IV+tag)
                        - Per tensor:
                            - name_len: uint16
                            - name: UTF-8 string
                            - dtype: uint8 (f32=0, f16=1, bf16=2...)
                            - ndim: uint8
                            - shape: ndim * uint32
                            - data_offset: uint64
                            - data_size: uint64
                            - iv: 12 bytes
                            - auth_tag: 16 bytes
                            - encrypted_dek: 32+12+16 bytes
                            - is_encrypted: uint8 (0/1)
12+hs     64          Ed25519 signature of bytes [0..12+header_size)
12+hs+64  ...         Tensor data (encrypted or plaintext per is_encrypted)
```

**vs SafeTensors:**
1. Binary header (not JSON) - Netron/Python can't parse without our code
2. Custom magic bytes - not recognized as known format
3. Encrypted tensor data - meaningless bytes without key
4. No gaps allowed - prevents polyglot files

**vs CryptoTensors (arxiv:2512.04580):**

| Aspect | CryptoTensors | .hmod |
|--------|--------------|-------|
| Base format | SafeTensors extension | Fully custom |
| Per-tensor AES-GCM-256 | Yes | Yes |
| DEK per tensor | Yes | Yes |
| Key source | JWK, KBS, HTTP | HKDF(device_fp + license) |
| Policies | Rego OPA | None (desktop) |
| Netron readable | Partial | No (custom magic) |
| Loading overhead | 2-8x | Target: <2x |

### Hybrid Key Management (Envelope Encryption)

```
Distribution (our side):
  Master Content Key (MCK) - random AES-256, generated once at model release
  DEK_i = random() per tensor
  tensor_i encrypted with DEK_i
  DEK_i wrapped with MCK → encrypted_DEK_i in header

Per-user key:
  User Key (UK) = HKDF(device_fp + license_key, salt, "hmod-v1-uk")
  encrypted_MCK = wrap(MCK, UK) → stored in license blob (~1 KB)

Client decryption:
  1. UK = HKDF(device_fp + license)
  2. MCK = unwrap(encrypted_MCK, UK)
  3. DEK_i = unwrap(encrypted_DEK_i, MCK)
  4. tensor_i = AES-GCM-decrypt(data, DEK_i, iv_i)
  5. Verify auth_tag before using data
```

**Distribution model:**
- One `.hmod` on CDN (~200 MB) - same for all users
- Per-user `license_blob` (~1 KB) - issued at activation
- Revocation: stop issuing license_blob for that user
- Compromise: generate new MCK, re-encrypt .hmod, all users get new license_blob

### Loading Performance (AES-NI)

| Operation | Time |
|-----------|------|
| AES-256-GCM decrypt 1 MB | ~0.5 ms |
| AES-256-GCM decrypt 10 MB | ~4.5 ms |
| AES-256-GCM decrypt 200 MB | ~90 ms |
| HKDF key derivation | <1 ms |
| Ed25519 header verify | <1 ms |

200 MB model decrypts in ~90 ms - imperceptible to user.

**Hardware support:**
- Windows x64: AES-NI on all Intel (Westmere 2010+) / AMD (Bulldozer 2011+)
- macOS Intel: AES-NI; Apple Silicon: ARM Crypto extensions
- libsodium: `crypto_aead_aes256gcm_is_available()` check required

### Toolchain

**hmod_packer:**
```
hmod_packer --input model.onnx \
            --output model.hmod \
            --master-key-file master.key \
            --sign-key-file signing.ed25519 \
            --encrypt-all

Steps:
1. Parse ONNX → tensor list
2. Per tensor: random DEK + random IV + AES-GCM encrypt
3. Wrap each DEK with MCK
4. Build header: metadata + encrypted DEKs + IVs + tags
5. Sign header with Ed25519
6. Write: [magic][header_size][header][signature][tensor_data...]
```

**key_weight_analyzer (sensitivity analysis):**
```
For each tensor: replace with random → measure output degradation
Top 5-10% most impactful = "critical tensors" → must encrypt
Remaining = "non-critical" → optional (speed tradeoff)
```

**hmod_validator:**
```
1. Check magic + version
2. Parse header (no corruption)
3. Verify Ed25519 signature
4. Per tensor: decrypt + auth tag verify
5. Shape/dtype consistency check
```

---

## Gotchas

- **AES-GCM nonce reuse is catastrophic.** Same nonce + same key = XOR of plaintexts revealed + auth key recoverable. In .hmod: encryption is one-time at build time, random nonce, so reuse is impossible by construction. If you add any re-encryption (e.g., on-the-fly personalization), be extremely careful.
- **AES-GCM 64 GB per-nonce limit.** One tensor cannot exceed 64 GB. Models are typically 200 MB total - not an issue.
- **Partial decryption failure = fail fast.** If one tensor auth tag fails, don't load the model. Either file corruption (re-download) or tampered (deny).
- **`CreateSessionFromArray` in ONNX Runtime** lets you load a model from a RAM buffer without touching disk. Critical: use this instead of loading from a decrypted temp file.
- **StegaStamp uses TF 1.13** - requires old TensorFlow environment for training/conversion. Use tf2onnx to get ONNX and then only need ONNX Runtime for inference.
- **TrustMark confidence threshold 0.85** is recommended balance. Lowering to 0.7 increases false positive rate from 1:10^6 to approximately 1:1000.
- **Diffusion regeneration attacks** (DALL-E, Midjourney "rinsing") reduce StegaStamp accuracy to 70-85%. Mitigation: use shorter-lived watermarks or accept this threat model for forensic (not authentication) purposes.
- **Binary header (not JSON) in .hmod** means no zero-cost compatibility with existing tools. Provide a validator CLI to verify files during build pipeline.
