---
level: 4
source_sha256: 5c53340eb34f204786bbeec7ad1f5dad9c729296adbea422a55a90789e250919
translation: machine
translated_at: '2026-10-24'
---
# Lizenzierung in C++: Ed25519 + Geräte-Fingerprinting + HKDF {#licensing-implementation-in-c-ed25519-device-fingerprinting-hkdf}

Datum: 2026-04-03
Kontext: Desktop-C++-App (Mac + Windows), selbst gehosteter Lizenzserver, ONNX-Modelle als geschütztes Asset.

---

## Auswahl der Ed25519-Bibliothek {#ed25519-library-selection}

| Kriterium | libsodium | OpenSSL 3.x | TweetNaCl |
|-----------|-----------|-------------|-----------|
| Größe | ~300KB | ~3MB+ | <50KB |
| API | Einfach `crypto_sign_*` | EVP_PKEY_*, ausführlich | Minimal C |
| Audit | Vollständig | Vollständig | Vollständig (100-Tweets-Paper) |
| Extras | AEAD, KDF, Hashing | Alles | Nur NaCl-Teilmenge |
| CMake | vcpkg/conan | Systembibliothek | Einzelne .c-Datei |
| Timing-sicher | Ja | Ja | Ja |

**Empfehlung: libsodium.** OpenSSL wird ohnehin über curl/TLS eingebunden, aber die Ed25519-EVP-API ist ausführlich. TweetNaCl dient als Fallback für ein minimales Binary.

### libsodium: Signieren/Verifizieren {#libsodium-signverify}

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

### OpenSSL 3.x: EVP-API {#openssl-3x-evp-api}

Ed25519 in OpenSSL verwendet eine **One-Shot-API** – kein Streaming mit Update+Final wie bei RSA.

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

### Schutz des öffentlichen Schlüssels im Binary {#protecting-the-public-key-in-binary}

Ein Angreifer kann den eingebetteten öffentlichen Schlüssel durch seinen eigenen ersetzen und gefälschte Lizenzen signieren.

Verteidigung in Schichten:
1. **Code-Signierung** – Apple codesign/Windows Authenticode. Byte-Ersetzung bricht die Betriebssystem-Signatur.
2. **Schlüsselverteilung** – XOR-Verschlüsselung des Schlüssels über mehrere Binary-Sektionen (kryptografisch nicht stark, erschwert aber Automatisierung):
   ```cpp
   const uint8_t pk_part1[16] = {...}; // in .rodata
   const uint8_t pk_xor_mask[32] = {...}; // in .data
   // Reconstruct: pk = pk_part1 || pk_part2; pk ^= pk_xor_mask;
   ```
3. **Schlüssel als HKDF-Eingabe** – Der öffentliche Schlüssel fließt in die Ableitung des Modell-Entschlüsselungsschlüssels ein. Ersetzen des Schlüssels = falscher Entschlüsselungsschlüssel = unbrauchbares Modell. **Primärer Mechanismus.**
4. **LLVM-Obfuskation** – Hikari, OLLVM, VMProtect/Themida ($500–5000). Nur kritische Funktionen obfuskieren.

---

## JWT mit Ed25519 {#jwt-with-ed25519}

### Bibliothek: jwt-cpp {#library-jwt-cpp}

`github.com/Thalhammer/jwt-cpp` – nur Header, C++11, EdDSA/Ed25519 über OpenSSL >= 1.1.1.

**Serverseitige JWT-Erstellung (Python):**

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

**Clientseitige JWT-Verifikation (C++):**

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

**JWT-Größe vs. Modellgewichte:** Das JWT enthält nur einen Hash (`kw_hash`); die verschlüsselten Gewichte liegen in einer separaten Datei:
```text
JWT payload:
  kw_hash: "sha256:<hash>"
  kw_version: 3

model_weights.enc (AES-256-GCM encrypted)
  Key = HKDF(jwt_signature, device_fp, "model_key_v3")
```
Größe des JWT: ~500–800 Bytes (die Ed25519-Signatur hat 64 Bytes).

---

## Geräte-Fingerprint {#device-fingerprint}

### Windows-Komponenten {#windows-components}

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

### macOS-Komponenten {#macos-components}

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

### Unscharfer Abgleich: 3 aus 5 {#fuzzy-matching-3-of-5}

Praktischer Ansatz – alle C(5,3)=10 Kombinationen durchzählen:

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

**Reaktivierungsablauf**, wenn die gesamte Hardware gewechselt wurde:
1. Die App stellt fest, dass kein Blob erfolgreich entschlüsselt werden kann.
2. Zeigt „Neues Gerät erkannt. Reaktivierung erforderlich.“ an.
3. Sendet `{license_key, new_fp, old_fp_hash}` an den Server.
4. Der Server prüft: Ist die Lizenz gültig? Ist die Geräteanzahl < max_devices?
5. Liefert neue verschlüsselte Blobs zurück.
6. Limit: 3 Reaktivierungen pro Monat.

---

## Certificate Pinning {#certificate-pinning}

### libcurl: CURLOPT_PINNEDPUBLICKEY {#libcurl-curlopt_pinnedpublickey}

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

**Pin-Hash aus dem Zertifikat ermitteln:**
```bash
openssl x509 -in server.crt -pubkey -noout | \
openssl pkey -pubin -outform der | \
openssl dgst -sha256 -binary | \
openssl enc -base64
```

**Den öffentlichen Schlüssel pinnen, nicht das Zertifikat** – das funktioniert auch über Let's-Encrypt-Erneuerungen hinweg (der Schlüssel bleibt gleich). Einen Backup-Pin für die Rotation mitliefern.

**Ablauf der Schlüsselrotation:**
1. Neuen Schlüssel erzeugen (dessen Hash = BACKUP_PIN).
2. App-Update mit beiden Pins ausliefern.
3. Nach 30 Tagen (95 %+ aktualisiert) den Server auf den neuen Schlüssel umstellen.
4. Beim nächsten Update: neuer Schlüssel = PRIMARY, neuen BACKUP erzeugen.

**Umgang mit Unternehmens-Proxys** (Zscaler, Bluecoat fangen TLS ab):
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

## Lizenz als Entschlüsselungsbestandteil (kein boolesches Gate) {#license-as-decryption-ingredient-not-boolean-gate}

**Falsch (boolesches Gate):**
```cpp
if (verify_license()) {
    load_model(); // Attacker: jmp load_model, skip check
}
```

**Richtig (Entschlüsselungsbestandteil):**
```cpp
auto key_material = verify_license(); // returns data, not bool
auto model_key = derive_key(key_material, device_fp);
auto model = decrypt_model(encrypted_model, model_key);
// Wrong key_material = model garbage, not "blocked"
```

### Architektur der Schlüsselableitung {#key-derivation-architecture}

```sql
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

### HKDF-Implementierung (libsodium) {#hkdf-implementation-libsodium}

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

## Skizze des Go-Lizenzservers {#go-license-server-sketch}

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

## Stolperfallen {#gotchas}

- **Ed25519 in OpenSSL ist nur One-Shot.** Ein Aufruf von `EVP_DigestSignUpdate` auf einem Ed25519-Kontext führt zum Absturz oder liefert einen Fehler. Immer den einzelnen Aufruf von `EVP_DigestSign` verwenden.
- **jwt_signature aus jwt-cpp extrahieren** – die Bibliothek stellt die rohen Signaturbytes nicht direkt bereit. Den Token an `.` aufteilen und den dritten Teil base64url-dekodieren.
- **Maximale Ausgabelänge von HKDF-Expand** ist 255 * HashLen = 8160 Bytes für SHA-256. Für größere Daten (Modellschlüssel) einen 32-Byte-Seed erzeugen und anschließend ChaCha20 als Stromchiffre verwenden.
- **libsodium `crypto_aead_aes256gcm` erfordert AES-NI.** Prüfung mit `crypto_aead_aes256gcm_is_available()`. Fallback: `crypto_aead_chacha20poly1305_ietf`.
- **Der Abgleich von 3 aus 5 Subschlüsseln ist O(100)**, nicht O(1) – 10 Subschlüssel × 10 Blobs. Für den Start unproblematisch, nicht für den Hot Path geeignet.
- **CRED_PERSIST_LOCAL_MACHINE** (Windows-Anmeldeinformationsverwaltung) übersteht Abmeldung, aber nicht das Löschen des Benutzerprofils oder eine Neuinstallation des Betriebssystems. Immer mit dem Serverzähler gegenprüfen.
- **Unternehmens-HTTPS-Proxys brechen Certificate Pinning** – als zweite Verteidigungsschicht eine Antwortsignatur implementieren, damit ein MITM Serverantworten auch ohne Pinning nicht fälschen kann.
- **Die Epoche im JWT** erlaubt dem Server, alte Modellschlüssel zu widerrufen, ohne Lizenzen neu auszustellen: Epoche erhöhen, neues verschlüsseltes Modell ausliefern – der alte key_material leitet dann den falschen Schlüssel ab.
