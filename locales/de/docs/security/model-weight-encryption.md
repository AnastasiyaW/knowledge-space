---
level: 3
source_sha256: c28b637f63700b9c95f4e15d0aa8a990cc20b28438ec1a02f394232075e94c33
translation: machine
translated_at: '2026-10-24'
---
# ML-Modell-Gewichtsverschlüsselung: Schutz im Ruhezustand und bei der Übertragung {#ml-model-weight-encryption-at-rest-and-in-transit-protection}

Datum: 2026-04-03
Kontext: Desktop-C++-Anwendung (Mac + Windows). Schutz neuronaler Netzgewichte vor Extraktion. Behandelt Algorithmusauswahl, Schlüsselverwaltung, Betriebssystemintegration und Formatvergleich.

---

## Algorithmusauswahl {#algorithm-selection}

| Algorithmus | Anwendungsfall | Durchsatz (AES-NI) | Auth-Tag | Hinweise |
|-------------|----------------|--------------------|----------|----------|
| AES-256-GCM | Primär: Gewichte im Ruhezustand | ~2,2 GB/s | 16 Byte | Verschlüsseln und authentifizieren in einem Durchlauf |
| ChaCha20-Poly1305 | Fallback: kein AES-NI | ~1,7 GB/s | 16 Byte | libsodium `crypto_aead_chacha20poly1305_ietf` |
| AES-256-CBC | Legacy: für neuen Code vermeiden | ~1,5 GB/s | Separates HMAC erforderlich | Sequenzielle Blöcke, keine Authentifizierung |

**AES-256-GCM vs. CBC:**
- GCM = Verschlüsselung und Authentifizierung in einem Durchlauf. CBC benötigt ein separates HMAC → zwei Durchläufe.
- GCM ist parallelisierbar (Counter-Modus). CBC ist sequenziell (jeder Block hängt vom vorherigen ab).
- GCM erkennt Manipulationen automatisch über den 16-Byte-Auth-Tag.
- AES-GCM-Limit von 64 GB pro Nonce: Ein Tensor darf 64 GB nicht überschreiten (Modelle sind typischerweise 200 MB groß – kein Problem).

**Nonce-Erzeugung:** zufällige 12-Byte-IV pro Verschlüsselung. Einmalige Verschlüsselung zur Build-Zeit macht eine Wiederverwendung konstruktionsbedingt unmöglich. Abgeleitete IV (`HKDF(key, tensor_name)`) für deterministische Builds.

---

## Schlüsselspeicherung: Credential-Stores des Betriebssystems {#key-storage-os-credential-stores}

### Windows DPAPI {#windows-dpapi}

DPAPI leitet den Verschlüsselungsschlüssel aus den Anmeldedaten des Benutzers ab. Er ist an Benutzer und Rechner gebunden.

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

**DPAPI-Eigenschaften:**
- `CRYPTPROTECT_LOCAL_MACHINE`: Jeder Benutzer auf demselben Rechner kann entschlüsseln. Für Schutz pro Benutzer `CRYPTPROTECT_CURRENT_USER` verwenden (Standard – kein Flag).
- Der MasterKey wird unter `%APPDATA%\Microsoft\Protect\{SID}` gespeichert, verschlüsselt mit dem Benutzerpasswort und optional einem Domänenschlüssel.
- Übersteht: Neustart, Betriebssystem-Updates. Übersteht nicht: Neuinstallation des Betriebssystems, Löschen des Benutzerprofils.
- Derselbe Benutzer kann immer entschlüsseln; andere Benutzer auf demselben Rechner können es nicht (Modus pro Benutzer).

### macOS Keychain {#macos-keychain}

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

**Option Secure Enclave:** P256-Schlüssel in der SE erzeugen und für einen per ECDH abgeleiteten symmetrischen Schlüssel verwenden. Der Schlüssel ist nie aus der Hardware extrahierbar.

---

## Envelope Encryption (hybride Schlüsselarchitektur) {#envelope-encryption-hybrid-key-architecture}

Eine verschlüsselte Modelldatei für alle Benutzer plus kleines benutzerspezifisches Schlüsselmaterial:

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

**Vorteile:**
- Eine `.hmod`-Datei auf dem CDN (200 MB) – für alle Benutzer identisch
- Pro Benutzer ein `license_blob` (~1 KB), ausgestellt bei der Aktivierung
- Widerruf des Modells: keine neuen `license_blob`s mehr ausstellen
- Rotation des Modellschlüssels: neuen MCK erzeugen, Tensoren neu verschlüsseln, neue CDN-Datei bereitstellen

---

## Schlüsselableitung (HKDF) {#key-derivation-hkdf}

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

## Entschlüsselungsleistung (AES-NI, x86-64) {#decryption-performance-aes-ni-x86-64}

| Datengröße | AES-256-GCM | ChaCha20-Poly1305 |
|------------|-------------|-------------------|
| 1 MB | ~0,5 ms | ~0,6 ms |
| 10 MB | ~4,5 ms | ~5,5 ms |
| 100 MB | ~45 ms | ~55 ms |
| 200 MB | ~90 ms | ~110 ms |
| HKDF-Ableitung | <1 ms | - |

Ein 200-MB-Modell wird in ~90 ms entschlüsselt – für den Benutzer beim Start nicht wahrnehmbar.

**Hardwareunterstützung:**
- Windows x64: AES-NI auf Intel (Westmere, 2010+), AMD (Bulldozer, 2011+)
- macOS Intel: AES-NI; Apple Silicon: ARM-Crypto-Erweiterungen (gleichwertige Geschwindigkeit)
- Immer prüfen: `crypto_aead_aes256gcm_is_available()` vor der Verwendung von AES-GCM aufrufen

---

## CryptoTensors-Format (arxiv:2512.04580) {#cryptotensors-format-arxiv251204580}

Erweiterung von SafeTensors mit Verschlüsselung auf Tensorebene:
- DEK (Data Encryption Key) pro Tensor plus eindeutige IV
- Header im Klartext, aber mit Ed25519 signiert
- Policy-Unterstützung: Rego/OPA für Zugriffskontrolle
- Kompatibel mit HuggingFace Transformers und vLLM

**CryptoTensors vs. .hmod (eigenes Format):**

| Aspekt | CryptoTensors | .hmod |
|--------|---------------|-------|
| Basisformat | SafeTensors-Erweiterung | Vollständig eigenes Binärformat |
| AES-GCM pro Tensor | Ja | Ja |
| Mit Netron lesbar | Teilweise (offener Header) | Nein (eigene Magic-Bytes) |
| Schlüsselquelle | JWK, KBS, HTTP | HKDF(device_fp + license) |
| Anwendungsfall Desktop | Cloud/Server | Desktop-Schutz vor Raubkopien |

Empfehlung für das eigene Format: `.hmod` mit binärem (nicht JSON-)Header. SafeTensors-basierte Formate sind selbst ohne Schlüssel mit Standard-Python-Werkzeugen lesbar, da die Header Tensornamen und Formen offenlegen.

---

## Selektive Verschlüsselung (nur kritische Tensoren) {#selective-encryption-critical-tensors-only}

Vollständige Modellverschlüsselung: Alle Gewichte sind geschützt, die Entschlüsselung ist jedoch am langsamsten.
Selektiv: Nur kritische Tensoren verschlüsseln (5–10 % nach Anzahl, >90 % der Auswirkung auf die Qualität).

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

CORELOCKER (IEEE S&P 2024, arxiv:2303.12397): Nur kritische Tensoren verschlüsseln und vom Server bereitstellen (niemals auf der Festplatte). Nicht-kritische Tensoren liegen im Klartext vor – das Modell degradiert ohne die Schlüsselgewichte sanft, funktioniert aber nicht vollständig.

---

## Fallstricke {#gotchas}

- **Wiederverwendung einer AES-GCM-Nonce ist katastrophal.** Gleicher Schlüssel + gleiche Nonce = XOR der Klartexte wird offengelegt und der Authentifizierungsschlüssel ist rekonstruierbar. Pro Verschlüsselung eine zufällige 12-Byte-Nonce verwenden. Einmalige Verschlüsselung zur Build-Zeit macht versehentliche Wiederverwendung unmöglich.
- **DPAPI `CRYPTPROTECT_LOCAL_MACHINE` = jeder Benutzer auf dem Rechner kann entschlüsseln.** Für Schlüsselmaterial, das nur an den aktuellen Benutzer gebunden sein soll, den Modus pro Benutzer verwenden (Standard, kein Flag nötig).
- **Nach der Entschlüsselung sicher löschen.** `memset` kann wegoptimiert werden. `sodium_memzero()` oder `SecureZeroMemory()` (Windows) verwenden.
- **macOS-App-Store-Sandbox:** Der Keychain-Zugriff ist pro App-Container sandboxed. Wird der Container bei der Deinstallation der App gelöscht, wird auch der Keychain-Eintrag gelöscht. Bei Distribution außerhalb des App Stores überdauern Keychain-Einträge die Deinstallation.
- **HKDF-Expand-Maximalausgabe = 255 × HashLen = 8160 Byte** für SHA-256. Für größeres Schlüsselmaterial einen ChaCha20-Stream verwenden, der mit der HKDF-Ausgabe geschlüsselt wird.
- **Teilweiser Authentifizierungsfehler = das gesamte Modell verwerfen.** Schlägt der Auth-Tag eines einzelnen Tensors fehl, dürfen keine Tensoren geladen werden. Ursache ist entweder eine beschädigte Datei (erneut herunterladen) oder Manipulation (ablehnen und protokollieren).
- **Auf manchen älteren Systemen ist die Anweisung AES-NI vorhanden, aber im BIOS deaktiviert.** Immer `crypto_aead_aes256gcm_is_available()` aufrufen und einen ChaCha20-Fallback bereitstellen.

## Siehe auch {#see-also}
- [[watermarking-encrypted-models]]
- [[hkdf-personalized-weights]]
- [[onnx-model-protection]]
- [[licensing-implementation-cpp]]
