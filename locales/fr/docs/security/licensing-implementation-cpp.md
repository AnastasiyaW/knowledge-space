---
level: 4
source_sha256: 5c53340eb34f204786bbeec7ad1f5dad9c729296adbea422a55a90789e250919
translation: machine
translated_at: '2026-10-24'
---
# Implémentation de licence en C++ : Ed25519 + empreinte matérielle + HKDF {#licensing-implementation-in-c-ed25519-device-fingerprinting-hkdf}

Date : 2026-04-03
Contexte : application de bureau C++ (Mac + Windows), serveur de licences auto-hébergé, modèles ONNX en tant qu'actif protégé.

---

## Choix de la bibliothèque Ed25519 {#ed25519-library-selection}

| Critère | libsodium | OpenSSL 3.x | TweetNaCl |
|-----------|-----------|-------------|-----------|
| Taille | ~300 Ko | ~3 Mo+ | <50 Ko |
| API | `crypto_sign_*` simple | EVP_PKEY_*, verbeuse | C minimal |
| Audit | Complet | Complet | Complet (article « 100 tweets ») |
| Extras | AEAD, KDF, hachage | Tout | Sous-ensemble NaCl uniquement |
| CMake | vcpkg/conan | Bibliothèque système | Un seul fichier .c |
| Résistant aux attaques temporelles | Oui | Oui | Oui |

**Recommandation : libsodium.** OpenSSL est déjà présent via curl/TLS, mais l'API EVP pour Ed25519 est verbeuse. TweetNaCl sert de solution de repli pour un binaire minimal.

### libsodium : signature et vérification {#libsodium-signverify}

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

### OpenSSL 3.x : API EVP {#openssl-3x-evp-api}

Ed25519 dans OpenSSL utilise une **API en un seul appel** : pas de couple Update+Final en flux comme pour RSA.

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

### Protéger la clé publique dans le binaire {#protecting-the-public-key-in-binary}

Un attaquant peut remplacer la clé publique intégrée par la sienne et signer de fausses licences.

Défenses (en couches) :
1. **Signature de code** : Apple codesign / Windows Authenticode. Un remplacement d'octets casse la signature du système d'exploitation.
2. **Distribution de la clé** : XOR de la clé répartie sur plusieurs sections du binaire (pas cryptographiquement robuste, mais complique l'automatisation) :
   ```cpp
   const uint8_t pk_part1[16] = {...}; // in .rodata
   const uint8_t pk_xor_mask[32] = {...}; // in .data
   // Reconstruct: pk = pk_part1 || pk_part2; pk ^= pk_xor_mask;
   ```
3. **Clé comme entrée HKDF** : la clé publique participe à la dérivation de la clé de déchiffrement du modèle. Remplacer la clé revient à obtenir une mauvaise clé de déchiffrement, et le modèle devient inutilisable. **Mécanisme principal.**
4. **Obfuscation LLVM** : Hikari, OLLVM, VMProtect/Themida (500 à 5 000 $). N'obfusquer que les fonctions critiques.

---

## JWT avec Ed25519 {#jwt-with-ed25519}

### Bibliothèque : jwt-cpp {#library-jwt-cpp}

`github.com/Thalhammer/jwt-cpp` : header-only, C++11, EdDSA/Ed25519 via OpenSSL >= 1.1.1.

**Création du JWT côté serveur (Python) :**

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

**Vérification du JWT côté client (C++) :**

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

**Taille du JWT par rapport aux poids du modèle :** le JWT ne contient qu'un hash (`kw_hash`) ; les poids chiffrés sont dans un fichier séparé :
```text
JWT payload:
  kw_hash: "sha256:<hash>"
  kw_version: 3

model_weights.enc (AES-256-GCM encrypted)
  Key = HKDF(jwt_signature, device_fp, "model_key_v3")
```
Taille du JWT : ~500 à 800 octets (la signature Ed25519 fait 64 octets).

---

## Empreinte matérielle {#device-fingerprint}

### Composants Windows {#windows-components}

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

### Composants macOS {#macos-components}

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

### Correspondance floue : 3 sur 5 {#fuzzy-matching-3-of-5}

Approche pragmatique : énumérer les C(5,3)=10 combinaisons :

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

**Flux de réactivation** lorsque tout le matériel a changé :
1. L'application constate qu'aucun blob ne se déchiffre
2. Elle affiche « Nouvel appareil détecté. Réactivation requise. »
3. Elle envoie `{license_key, new_fp, old_fp_hash}` au serveur
4. Le serveur vérifie : la licence est-elle valide ? Le nombre d'appareils est-il inférieur à max_devices ?
5. Il renvoie de nouveaux blobs chiffrés
6. Limite : 3 réactivations par mois

---

## Épinglage de certificat {#certificate-pinning}

### libcurl : CURLOPT_PINNEDPUBLICKEY {#libcurl-curlopt_pinnedpublickey}

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

**Obtenir le hash d'épinglage à partir du certificat :**
```bash
openssl x509 -in server.crt -pubkey -noout | \
openssl pkey -pubin -outform der | \
openssl dgst -sha256 -binary | \
openssl enc -base64
```

**Épingler la clé publique, et non le certificat** : cela fonctionne lors des renouvellements Let's Encrypt (la clé reste identique). Inclure une épingle de secours pour permettre la rotation.

**Procédure de rotation des clés :**
1. Générer une nouvelle clé (son hash = BACKUP_PIN)
2. Livrer une mise à jour de l'application contenant les deux épingles
3. Après 30 jours (95 % et plus mis à jour), basculer le serveur sur la nouvelle clé
4. Mise à jour suivante : la nouvelle clé devient PRIMARY, et générer un nouveau BACKUP

**Gestion des proxys d'entreprise** (Zscaler, Bluecoat interceptent le TLS) :
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

## La licence comme ingrédient de déchiffrement (et non comme simple verrou booléen) {#license-as-decryption-ingredient-not-boolean-gate}

**Incorrect (verrou booléen) :**
```cpp
if (verify_license()) {
    load_model(); // Attacker: jmp load_model, skip check
}
```

**Correct (ingrédient de déchiffrement) :**
```cpp
auto key_material = verify_license(); // returns data, not bool
auto model_key = derive_key(key_material, device_fp);
auto model = decrypt_model(encrypted_model, model_key);
// Wrong key_material = model garbage, not "blocked"
```

### Architecture de dérivation des clés {#key-derivation-architecture}

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

### Implémentation de HKDF (libsodium) {#hkdf-implementation-libsodium}

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

## Esquisse du serveur de licences en Go {#go-license-server-sketch}

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

## Pièges à éviter {#gotchas}

- **Ed25519 dans OpenSSL n'accepte qu'un appel unique.** Appeler `EVP_DigestSignUpdate` sur un contexte Ed25519 provoque un plantage ou une erreur. Utiliser systématiquement l'appel unique `EVP_DigestSign`.
- **Extraction de la signature jwt à partir de jwt-cpp** : la bibliothèque n'expose pas directement les octets bruts de la signature. Découper le jeton sur `.` et décoder en base64url la troisième partie.
- **Taille maximale de sortie de HKDF-Expand** : 255 × HashLen = 8160 octets pour SHA-256. Pour des données plus volumineuses (clés de modèles), générer une graine de 32 octets, puis utiliser ChaCha20 comme chiffrement en flux.
- **`crypto_aead_aes256gcm` de libsodium nécessite AES-NI.** Vérifier avec `crypto_aead_aes256gcm_is_available()`. Solution de repli : `crypto_aead_chacha20poly1305_ietf`.
- **La correspondance 3 sur 5 de sous-clés est en O(100)**, et non en O(1) : 10 sous-clés × 10 blobs. Acceptable au démarrage, à éviter sur le chemin critique.
- **CRED_PERSIST_LOCAL_MACHINE** (Gestionnaire d'identification Windows) survit à la déconnexion, mais pas à la suppression du profil utilisateur ni à la réinstallation du système. Toujours recouper avec le compteur du serveur.
- **Les proxys HTTPS d'entreprise cassent l'épinglage de certificat** : implémenter la signature des réponses comme deuxième couche de défense, afin qu'un MITM ne puisse pas forger les réponses du serveur même sans épinglage.
- **L'epoch dans le JWT** permet au serveur de révoquer d'anciennes clés de modèle sans réémettre les licences : incrémenter l'epoch, livrer le nouveau modèle chiffré, et l'ancien key_material dérive une mauvaise clé.
