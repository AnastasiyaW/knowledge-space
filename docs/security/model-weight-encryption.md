# ML Model Weight Encryption: At-Rest and In-Transit Protection

Date: 2026-04-03
Context: Desktop C++ app (Mac + Windows). Protecting neural network weights from extraction. Covers algorithm selection, key management, OS integration, and format comparison.

---

## Algorithm Selection

| Algorithm | Use case | Throughput (AES-NI) | Auth tag | Notes |
|-----------|----------|---------------------|----------|-------|
| AES-256-GCM | Primary: at-rest weights | ~2.2 GB/s | 16 bytes | Encrypt + authenticate in one pass |
| ChaCha20-Poly1305 | Fallback: no AES-NI | ~1.7 GB/s | 16 bytes | libsodium `crypto_aead_chacha20poly1305_ietf` |
| AES-256-CBC | Legacy: avoid for new code | ~1.5 GB/s | Needs separate HMAC | Sequential blocks, no auth |

**AES-256-GCM vs CBC:**
- GCM = encrypt + authenticate in one pass. CBC needs separate HMAC → two-pass.
- GCM parallelizes (counter mode). CBC is sequential (each block depends on previous).
- GCM detects tampering automatically via 16-byte auth tag.
- AES-GCM 64 GB per-nonce limit: one tensor cannot exceed 64 GB (models are typically 200 MB - not a concern).

**Nonce generation:** random 12-byte IV per encryption. One-time encryption at build time makes reuse impossible by construction. Derived IV (`HKDF(key, tensor_name)`) for deterministic builds.

---

## Key Storage: OS Credential Stores

### Windows DPAPI

DPAPI derives encryption key from user's logon credentials. Bound to user + machine.

```cpp
#include <windows.h>
#include <wincrypt.h>
#pragma comment(lib, "crypt32.lib")

// Encrypt key material with DPAPI (local machine scope)
bool dpapi_protect(const std::vector<uint8_t>& plaintext,
                   std::vector<uint8_t>& ciphertext) {
    DATA_BLOB in = { (DWORD)plaintext.size(),
                     (BYTE*)plaintext.data() };
    DATA_BLOB out = {};
    if (!CryptProtectData(&in, nullptr, nullptr, nullptr, nullptr,
                          CRYPTPROTECT_LOCAL_MACHINE, &out))
        return false;
    ciphertext.assign(out.pbData, out.pbData + out.cbData);
    LocalFree(out.pbData);
    return true;
}

bool dpapi_unprotect(const std::vector<uint8_t>& ciphertext,
                     std::vector<uint8_t>& plaintext) {
    DATA_BLOB in = { (DWORD)ciphertext.size(),
                     (BYTE*)ciphertext.data() };
    DATA_BLOB out = {};
    if (!CryptUnprotectData(&in, nullptr, nullptr, nullptr, nullptr,
                            CRYPTPROTECT_LOCAL_MACHINE, &out))
        return false;
    plaintext.assign(out.pbData, out.pbData + out.cbData);
    LocalFree(out.pbData);
    return true;
}
```

**DPAPI properties:**
- `CRYPTPROTECT_LOCAL_MACHINE`: any user on same machine can decrypt. For per-user protection use `CRYPTPROTECT_CURRENT_USER` (default - no flag).
- MasterKey stored in `%APPDATA%\Microsoft\Protect\{SID}` encrypted with user password + optional domain key.
- Survives: reboot, OS updates. Does NOT survive: OS reinstall, user profile deletion.
- Same user can always decrypt; other users on same machine cannot (per-user mode).

### macOS Keychain

```objc
#import <Security/Security.h>

bool keychain_store(const char* service, const char* account,
                    const void* data, size_t len) {
    NSDictionary* q = @{
        (__bridge id)kSecClass: (__bridge id)kSecClassGenericPassword,
        (__bridge id)kSecAttrService: @(service),
        (__bridge id)kSecAttrAccount: @(account),
        (__bridge id)kSecValueData: [NSData dataWithBytes:data length:len],
        (__bridge id)kSecAttrAccessible:
            (__bridge id)kSecAttrAccessibleAfterFirstUnlock,
    };
    OSStatus s = SecItemAdd((__bridge CFDictionaryRef)q, NULL);
    if (s == errSecDuplicateItem) {
        NSDictionary* attrs = @{
            (__bridge id)kSecValueData:
                [NSData dataWithBytes:data length:len]
        };
        SecItemUpdate((__bridge CFDictionaryRef)@{
            (__bridge id)kSecClass: (__bridge id)kSecClassGenericPassword,
            (__bridge id)kSecAttrService: @(service),
            (__bridge id)kSecAttrAccount: @(account),
        }, (__bridge CFDictionaryRef)attrs);
    }
    return s == errSecSuccess || s == errSecDuplicateItem;
}
```

**Secure Enclave option:** generate P256 key in SE, use for ECDH-derived symmetric key. Key never extractable from hardware.

---

## Envelope Encryption (Hybrid Key Architecture)

One encrypted model file for all users + small per-user key material:

```text
Build time (developer side):
  Master Content Key (MCK) = random AES-256, generated once per model version
  DEK_i = random AES-256 per tensor
  tensor_i = AES-GCM-256-encrypt(tensor_data, DEK_i, IV_i)
  encrypted_DEK_i = AES-GCM-encrypt(DEK_i, MCK)

Activation time (per user):
  User Key (UK) = HKDF(device_fp + license_key, salt, "model-v1-uk")
  encrypted_MCK = AES-GCM-encrypt(MCK, UK)  → stored in license_blob (~1 KB)

Client decryption:
  UK = HKDF(device_fp + license_key, salt, "model-v1-uk")
  MCK = AES-GCM-decrypt(encrypted_MCK, UK)
  DEK_i = AES-GCM-decrypt(encrypted_DEK_i, MCK)
  tensor_i = AES-GCM-decrypt(cipher_i, DEK_i, IV_i)
  verify auth_tag_i before using
```

**Benefits:**
- One `.hmod` on CDN (200 MB) - same for all users
- Per-user `license_blob` (~1 KB) issued at activation
- Model revocation: stop issuing new `license_blob`
- Model key rotation: generate new MCK, re-encrypt tensors, push new CDN file

---

## Key Derivation (HKDF)

```cpp
#include <sodium.h>

// HKDF-SHA256: Extract + Expand
bool derive_model_key(
    const uint8_t* device_fp, size_t fp_len,
    const uint8_t* license_key, size_t lk_len,
    const uint8_t* salt, size_t salt_len,
    uint8_t out_key[32])
{
    // Concatenate IKM
    std::vector<uint8_t> ikm(fp_len + lk_len);
    memcpy(ikm.data(), device_fp, fp_len);
    memcpy(ikm.data() + fp_len, license_key, lk_len);

    // HKDF-Extract: PRK = HMAC-SHA256(salt, IKM)
    uint8_t prk[crypto_kdf_hkdf_sha256_KEYBYTES];
    if (crypto_kdf_hkdf_sha256_extract(prk, salt, salt_len,
                                        ikm.data(), ikm.size()) != 0)
        return false;

    // HKDF-Expand
    const char* info = "hmod-v1-tensor-decryption";
    return crypto_kdf_hkdf_sha256_expand(out_key, 32,
               info, strlen(info), prk) == 0;
}
```

---

## Decryption Performance (AES-NI, x86-64)

| Data size | AES-256-GCM | ChaCha20-Poly1305 |
|-----------|-------------|-------------------|
| 1 MB | ~0.5 ms | ~0.6 ms |
| 10 MB | ~4.5 ms | ~5.5 ms |
| 100 MB | ~45 ms | ~55 ms |
| 200 MB | ~90 ms | ~110 ms |
| HKDF derive | <1 ms | - |

200 MB model decrypts in ~90 ms - imperceptible to user at startup.

**Hardware support:**
- Windows x64: AES-NI on Intel (Westmere 2010+), AMD (Bulldozer 2011+)
- macOS Intel: AES-NI; Apple Silicon: ARM Crypto extensions (equivalent speed)
- Always check: `crypto_aead_aes256gcm_is_available()` before using AES-GCM

---

## CryptoTensors Format (arxiv:2512.04580)

Extension of SafeTensors with tensor-level encryption:
- Per-tensor DEK (data encryption key) + unique IV
- Header in plaintext but Ed25519 signed
- Policy support: Rego/OPA for access control
- Compatible with HuggingFace Transformers, vLLM

**CryptoTensors vs .hmod (custom format):**

| Aspect | CryptoTensors | .hmod |
|--------|--------------|-------|
| Base format | SafeTensors extension | Fully custom binary |
| Per-tensor AES-GCM | Yes | Yes |
| Netron readable | Partial (open header) | No (custom magic) |
| Key source | JWK, KBS, HTTP | HKDF(device_fp + license) |
| Desktop use case | Cloud/server | Desktop anti-piracy |

Custom format recommendation: `.hmod` with binary (non-JSON) header. SafeTensors-based formats are parseable by standard Python tooling even without keys (headers expose tensor names/shapes).

---

## Selective Encryption (Critical Tensors Only)

Full model encryption: all weights protected but slowest decryption.
Selective: encrypt only critical tensors (5-10% by count, >90% of quality impact).

```python
# Sensitivity analysis: replace each tensor with random, measure PSNR drop
def find_critical_tensors(model_path, test_input, threshold_psnr_drop=3.0):
    critical = []
    baseline = run_inference(model_path, test_input)
    for name in get_tensor_names(model_path):
        perturbed = randomize_tensor(model_path, name)
        output = run_inference(perturbed, test_input)
        psnr_drop = baseline_psnr - compute_psnr(baseline, output)
        if psnr_drop > threshold_psnr_drop:
            critical.append(name)
    return critical  # typically 5-10% of all tensors
```

CORELOCKER (IEEE S&P 2024, arxiv:2303.12397): encrypt only critical tensors, serve them from server (never on disk). Non-critical tensors in plaintext - model degrades gracefully without key weights but doesn't fully function.

---

## Gotchas

- **AES-GCM nonce reuse is catastrophic.** Same key + same nonce = XOR of plaintexts revealed + authentication key recoverable. Use random 12-byte nonce per encryption. One-time build-time encryption makes accidental reuse impossible.
- **DPAPI `CRYPTPROTECT_LOCAL_MACHINE` = any user on machine can decrypt.** For key material binding to current user only, use per-user mode (default, no flag needed).
- **Secure zero after decryption.** `memset` can be optimized away. Use `sodium_memzero()` or `SecureZeroMemory()` (Windows).
- **macOS App Store sandbox:** Keychain access is sandboxed per-app container. Container deleted on app uninstall → Keychain entry deleted too. For non-App-Store distribution, Keychain entries survive uninstall.
- **HKDF-Expand max output = 255 × HashLen = 8160 bytes** for SHA-256. For larger key material, use ChaCha20 stream keyed by HKDF output.
- **Partial authentication failure = reject entire model.** If one tensor auth tag fails, do not load any tensors. Either file corruption (re-download) or tampering (deny and log).
- **Intel's AES-NI AESNI instruction present but disabled by BIOS** on some older systems. Always call `crypto_aead_aes256gcm_is_available()` and provide ChaCha20 fallback.

## See Also
- [[watermarking-encrypted-models]]
- [[hkdf-personalized-weights]]
- [[onnx-model-protection]]
- [[licensing-implementation-cpp]]
