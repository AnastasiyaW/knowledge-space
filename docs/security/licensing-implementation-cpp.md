# Licensing Implementation in C++: Ed25519 + Device Fingerprinting + HKDF

Date: 2026-04-03
Context: Desktop C++ app (Mac + Windows), self-hosted license server, ONNX models as protected asset.

---

## Ed25519 Library Selection

| Criterion | libsodium | OpenSSL 3.x | TweetNaCl |
|-----------|-----------|-------------|-----------|
| Size | ~300KB | ~3MB+ | <50KB |
| API | Simple `crypto_sign_*` | EVP_PKEY_*, verbose | Minimal C |
| Audit | Full | Full | Full (100 tweets paper) |
| Extra | AEAD, KDF, hashing | Everything | NaCl subset only |
| CMake | vcpkg/conan | System lib | Single .c file |
| Timing-safe | Yes | Yes | Yes |

**Recommendation: libsodium.** OpenSSL already pulled in via curl/TLS but Ed25519 EVP API is verbose. TweetNaCl is fallback for minimal binary.

### libsodium: Sign/Verify

```cpp
#include <sodium.h>

// Key generation (server)
if (sodium_init() < 0) { /* fatal */ }
unsigned char pk[crypto_sign_PUBLICKEYBYTES]; // 32 bytes
unsigned char sk[crypto_sign_SECRETKEYBYTES]; // 64 bytes
crypto_sign_keypair(pk, sk);

// Sign (server, detached)
unsigned char sig[crypto_sign_BYTES]; // 64 bytes
crypto_sign_detached(sig, NULL, message, message_len, sk);

// Verify (client, detached)
if (crypto_sign_verify_detached(sig, message, message_len, pk) != 0) {
    // Invalid signature
}
```

### OpenSSL 3.x: EVP API

Ed25519 in OpenSSL uses **one-shot API** - no streaming Update+Final like RSA.

```cpp
#include <openssl/evp.h>

// Key generation
EVP_PKEY *pkey = NULL;
EVP_PKEY_CTX *pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_ED25519, NULL);
EVP_PKEY_keygen_init(pctx);
EVP_PKEY_keygen(pctx, &pkey);
EVP_PKEY_CTX_free(pctx);

// Sign (one-shot)
EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
EVP_DigestSignInit(mdctx, NULL, NULL, NULL, pkey); // NULL md for Ed25519
size_t siglen;
EVP_DigestSign(mdctx, NULL, &siglen, msg, msg_len); // get size
unsigned char *sig = (unsigned char*)OPENSSL_malloc(siglen);
EVP_DigestSign(mdctx, sig, &siglen, msg, msg_len);
EVP_MD_CTX_free(mdctx);

// Verify
EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
EVP_DigestVerifyInit(mdctx, NULL, NULL, NULL, pkey);
int rc = EVP_DigestVerify(mdctx, sig, siglen, msg, msg_len);
// rc == 1 = valid, 0 = invalid, <0 = error
EVP_MD_CTX_free(mdctx);

// Load raw 32-byte public key
EVP_PKEY *pkey = EVP_PKEY_new_raw_public_key(EVP_PKEY_ED25519, NULL, raw_pk, 32);
```

### Protecting the Public Key in Binary

The attacker can replace the embedded public key with their own and sign fake licenses.

Defenses (layered):
1. **Code signing** - Apple codesign/Windows Authenticode. Byte replacement breaks OS signature.
2. **Key distribution** - XOR key across multiple binary sections (not cryptographically strong, but hinders automation):
   ```cpp
   const uint8_t pk_part1[16] = {...}; // in .rodata
   const uint8_t pk_xor_mask[32] = {...}; // in .data
   // Reconstruct: pk = pk_part1 || pk_part2; pk ^= pk_xor_mask;
   ```
3. **Key as HKDF input** - public key participates in model decryption key derivation. Replacing key = wrong decryption key = model garbage. **Primary mechanism.**
4. **LLVM obfuscation** - Hikari, OLLVM, VMProtect/Themida ($500-5000). Obfuscate only critical functions.

---

## JWT with Ed25519

### Library: jwt-cpp

`github.com/Thalhammer/jwt-cpp` - header-only, C++11, EdDSA/Ed25519 via OpenSSL >= 1.1.1.

**Server-side JWT creation (Python):**

```python
import jwt  # PyJWT
payload = {
    "sub": "user_12345",
    "iss": "license.ourapp.com",
    "iat": int(datetime.utcnow().timestamp()),
    "exp": int((datetime.utcnow() + timedelta(days=30)).timestamp()),
    "device_fp": "sha256:a1b2c3...",
    "tier": "pro",
    "key_id": "LK-2026-00042",
    "max_devices": 2,
    "epoch": 7,          # server epoch counter (anti clock rollback)
    "kw_hash": "sha256:of_encrypted_key_weights_blob"
}
token = jwt.encode(payload, private_key, algorithm="EdDSA")
```

**Client-side JWT verification (C++):**

```cpp
#include <jwt-cpp/jwt.h>

const std::string ed25519_pub_pem = R"(
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEA<base64_32_bytes>
-----END PUBLIC KEY-----
)";

try {
    auto decoded = jwt::decode(token_string);
    auto verifier = jwt::verify()
        .allow_algorithm(jwt::algorithm::ed25519(ed25519_pub_pem, "", "", ""))
        .with_issuer("license.ourapp.com")
        .with_claim("device_fp", jwt::claim(std::string(local_device_fp)))
        .leeway(60); // 60s tolerance for clock skew
    verifier.verify(decoded);

    auto tier = decoded.get_payload_claim("tier").as_string();
    auto epoch = decoded.get_payload_claim("epoch").as_integer();
} catch (const jwt::error::token_verification_exception& e) {
    // Invalid token
}
```

**JWT size vs model weights:** JWT contains only a hash (`kw_hash`); encrypted weights are a separate file:
```
JWT payload:
  kw_hash: "sha256:<hash>"
  kw_version: 3

model_weights.enc (AES-256-GCM encrypted)
  Key = HKDF(jwt_signature, device_fp, "model_key_v3")
```
JWT size: ~500-800 bytes (Ed25519 signature is 64 bytes).

---

## Device Fingerprint

### Windows Components

```cpp
#include <windows.h>
#include <intrin.h>
#include <Wbemidl.h>
#pragma comment(lib, "wbemuuid.lib")

// 1. CPU ID
std::string getCpuId() {
    int cpuInfo[4] = {0};
    __cpuid(cpuInfo, 1);
    char buf[64];
    snprintf(buf, sizeof(buf), "%08X%08X", cpuInfo[3], cpuInfo[0]);
    return buf;
}

// 2. BIOS Serial via GetSystemFirmwareTable('RSMB', ...) -> parse SMBIOS Type 1
// 3. Disk Serial via WMI: SELECT SerialNumber FROM Win32_DiskDrive WHERE Index=0
// 4. Machine GUID from registry
std::string getMachineGuid() {
    HKEY hKey;
    RegOpenKeyExA(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Cryptography",
                  0, KEY_READ, &hKey);
    char guid[256]; DWORD size = sizeof(guid);
    RegQueryValueExA(hKey, "MachineGuid", NULL, NULL, (LPBYTE)guid, &size);
    RegCloseKey(hKey);
    return guid;
}
// 5. OS Install Date via HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\InstallDate
```

### macOS Components

```cpp
#include <CoreFoundation/CoreFoundation.h>
#include <IOKit/IOKitLib.h>

// Hardware UUID
std::string getHardwareUUID() {
    io_service_t pe = IOServiceGetMatchingService(kIOMasterPortDefault,
        IOServiceMatching("IOPlatformExpertDevice"));
    CFStringRef uuid = (CFStringRef)IORegistryEntryCreateCFProperty(
        pe, CFSTR("IOPlatformUUID"), kCFAllocatorDefault, 0);
    char buf[256];
    CFStringGetCString(uuid, buf, sizeof(buf), kCFStringEncodingUTF8);
    CFRelease(uuid); IOObjectRelease(pe);
    return buf;
}
// Also: kIOPlatformSerialNumberKey, MAC address (en0), hw.model sysctl
// Link: -framework IOKit -framework CoreFoundation
```

### Fuzzy Matching: 3-of-5

Practical approach - enumerate all C(5,3)=10 combinations:

```cpp
std::vector<std::string> components = {
    getCpuId(), getBiosSerial(), getDiskSerial(), getMachineGuid(), getOsInstallDate()
};

// Generate 10 subkeys (all 3-of-5 combinations)
int indices[10][3] = {
    {0,1,2},{0,1,3},{0,1,4},{0,2,3},{0,2,4},
    {0,3,4},{1,2,3},{1,2,4},{1,3,4},{2,3,4}
};
for (auto& combo : indices) {
    std::string combined = components[combo[0]] + "|" +
                           components[combo[1]] + "|" + components[combo[2]];
    uint8_t hash[32];
    crypto_hash_sha256(hash, (const uint8_t*)combined.c_str(), combined.size());
    subkeys.push_back(hash);
}

// At activation: server encrypts key_material with each of 10 subkeys
// At use: client tries all 10 subkeys against all 10 blobs
// Match = at least 3 of 5 components identical
struct EncryptedKeyMaterial {
    uint8_t nonce[24];
    uint8_t ciphertext[48]; // 32 bytes key_material + 16 bytes auth tag
};
// 10 blobs * 72 bytes = 720 bytes overhead (negligible)
```

**Re-activation flow** when all hardware changed:
1. App detects no blob decrypts successfully
2. Shows "New device detected. Re-activation required."
3. Sends `{license_key, new_fp, old_fp_hash}` to server
4. Server verifies: license valid? device count < max_devices?
5. Returns new encrypted blobs
6. Limit: 3 re-activations per month

---

## Certificate Pinning

### libcurl: CURLOPT_PINNEDPUBLICKEY

```cpp
#include <curl/curl.h>

CURL *curl = curl_easy_init();
curl_easy_setopt(curl, CURLOPT_URL, "https://license.ourapp.com/v1/activate");
// SHA-256 hash of server's public key; semicolon for primary + backup
curl_easy_setopt(curl, CURLOPT_PINNEDPUBLICKEY,
    "sha256//YhKJKSzoTt2b5FP18fvpHo7fJYqQCjAa3HWY3tvRMwE=;"
    "sha256//backup_pin_hash_for_key_rotation=");

CURLcode res = curl_easy_perform(curl);
if (res == CURLE_SSL_PINNEDPUBKEYNOTMATCH) {
    // Server cert didn't match pin - possible MITM or corporate proxy
}
```

**Get pin hash from certificate:**
```bash
openssl x509 -in server.crt -pubkey -noout | \
openssl pkey -pubin -outform der | \
openssl dgst -sha256 -binary | \
openssl enc -base64
```

**Pin public key, not certificate** - works across Let's Encrypt renewals (key stays same). Include backup pin for rotation.

**Key rotation procedure:**
1. Generate new key (its hash = BACKUP_PIN)
2. Ship app update with both pins
3. After 30 days (95%+ updated) - switch server to new key
4. Next update: new key = PRIMARY, generate new BACKUP

**Corporate proxy handling** (Zscaler, Bluecoat intercept TLS):
```cpp
CURLcode res = curl_easy_perform(curl);
if (res == CURLE_SSL_PINNEDPUBKEYNOTMATCH) {
    // Fallback: disable pinning but verify Ed25519 response signature
    curl_easy_setopt(curl, CURLOPT_PINNEDPUBLICKEY, NULL);
    res = curl_easy_perform(curl);
    // MUST verify server response signature
}
```

---

## License as Decryption Ingredient (not Boolean Gate)

**Wrong (boolean gate):**
```cpp
if (verify_license()) {
    load_model(); // Attacker: jmp load_model, skip check
}
```

**Correct (decryption ingredient):**
```cpp
auto key_material = verify_license(); // returns data, not bool
auto model_key = derive_key(key_material, device_fp);
auto model = decrypt_model(encrypted_model, model_key);
// Wrong key_material = model garbage, not "blocked"
```

### Key Derivation Architecture

```
JWT (from server)
     |
Ed25519 verify
     |
jwt_signature (64 bytes)
     |
+----+----+
|         |
device_fp  public_key
(matched   (32 bytes)
 subkey)   |
+----+----+
     |
HKDF-SHA256
  salt = jwt_signature
  IKM  = matched_subkey (from 3-of-5)
  info = public_key || "model_v3" || epoch
     |
model_decryption_key (32 bytes)
     |
AES-256-GCM decrypt
     |
ONNX model weights
```

### HKDF Implementation (libsodium)

```cpp
// HKDF-Extract: PRK = HMAC-SHA256(salt=jwt_signature, IKM=matched_subkey)
uint8_t prk[32];
crypto_auth_hmacsha256(prk,
    lr.matched_subkey.data(), lr.matched_subkey.size(),
    lr.jwt_signature.data()); // salt = jwt_signature

// HKDF-Expand (manual RFC 5869 or use OpenSSL EVP_KDF)
// info = public_key || "model_v" || epoch
std::string info_str = std::string((char*)public_key, 32) +
                       "model_v" + std::to_string(lr.epoch);
// ... standard HKDF-Expand implementation ...

// AES-256-GCM decrypt
// First 12 bytes = nonce, last 16 bytes = auth tag
// crypto_aead_aes256gcm_decrypt (libsodium, requires AES-NI)
// or EVP_aes_256_gcm (OpenSSL)
```

---

## Go License Server Sketch

```go
package main

import (
    "crypto/ed25519"
    "github.com/golang-jwt/jwt/v5"
    "golang.org/x/crypto/hkdf"
    "crypto/sha256"
    "io"
)

type LicenseClaims struct {
    DeviceFP    string `json:"device_fp"`
    Tier        string `json:"tier"`
    KeyID       string `json:"key_id"`
    MaxDevices  int    `json:"max_devices"`
    Epoch       int    `json:"epoch"`
    KWHash      string `json:"kw_hash"`
    jwt.RegisteredClaims
}

func issueLicense(privateKey ed25519.PrivateKey, claims LicenseClaims) (string, error) {
    token := jwt.NewWithClaims(jwt.SigningMethodEdDSA, claims)
    return token.SignedString(privateKey)
}

func deriveModelKey(jwtSig, matchedSubkey, pubKey []byte, epoch int) []byte {
    info := append(pubKey, []byte("model_v"+strconv.Itoa(epoch))...)
    r := hkdf.New(sha256.New, matchedSubkey, jwtSig, info)
    key := make([]byte, 32)
    io.ReadFull(r, key)
    return key
}
```

---

## Gotchas

- **Ed25519 in OpenSSL is one-shot only.** Calling `EVP_DigestSignUpdate` on an Ed25519 context crashes or returns error. Always use the single `EVP_DigestSign` call.
- **jwt_signature extraction from jwt-cpp** - the library doesn't expose raw signature bytes directly. Split token on `.`, base64url-decode the third part.
- **HKDF-Expand max output** is 255 * HashLen = 8160 bytes for SHA-256. For larger data (model keys), generate a 32-byte seed then use ChaCha20 as stream cipher.
- **libsodium `crypto_aead_aes256gcm` requires AES-NI.** Check with `crypto_aead_aes256gcm_is_available()`. Fallback: `crypto_aead_chacha20poly1305_ietf`.
- **3-of-5 subkey matching is O(100)** not O(1) - 10 subkeys × 10 blobs. Fine for startup, not for hot path.
- **CRED_PERSIST_LOCAL_MACHINE** (Windows Credential Manager) survives logoff but not user profile deletion or OS reinstall. Always cross-validate with server counter.
- **Corporate HTTPS proxies break cert pinning** - implement response signing as second defense layer so MITM can't forge server responses even without pinning.
- **Epoch in JWT** allows server to revoke old model keys without reissuing licenses - increment epoch, ship new encrypted model, old key_material derives wrong key.
