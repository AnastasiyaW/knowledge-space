---
level: 3
source_sha256: c28b637f63700b9c95f4e15d0aa8a990cc20b28438ec1a02f394232075e94c33
translation: machine
translated_at: '2026-10-24'
---
# Chiffrement des poids de modèles ML : protection au repos et en transit {#ml-model-weight-encryption-at-rest-and-in-transit-protection}

Date : 2026-04-03
Contexte : Application C++ de bureau (Mac + Windows). Protection des poids de réseaux de neurones contre l'extraction. Couvre la sélection des algorithmes, la gestion des clés, l'intégration au système d'exploitation et la comparaison des formats.

---

## Sélection de l'algorithme {#algorithm-selection}

| Algorithme | Cas d'usage | Débit (AES-NI) | Tag d'authentification | Remarques |
|-----------|----------|---------------------|----------|-------|
| AES-256-GCM | Principal : poids au repos | ~2,2 Go/s | 16 octets | Chiffrement et authentification en une seule passe |
| ChaCha20-Poly1305 | Repli : sans AES-NI | ~1,7 Go/s | 16 octets | `crypto_aead_chacha20poly1305_ietf` de libsodium |
| AES-256-CBC | Historique : à éviter pour le nouveau code | ~1,5 Go/s | Nécessite un HMAC séparé | Blocs séquentiels, sans authentification |

**AES-256-GCM vs CBC :**
- GCM = chiffrement et authentification en une seule passe. CBC nécessite un HMAC séparé, soit deux passes.
- GCM se parallélise (mode compteur). CBC est séquentiel (chaque bloc dépend du précédent).
- GCM détecte automatiquement toute altération grâce au tag d'authentification de 16 octets.
- Limite AES-GCM de 64 Go par nonce : un tenseur ne peut pas dépasser 64 Go (les modèles font typiquement 200 Mo, donc ce n'est pas un problème).

**Génération du nonce :** IV aléatoire de 12 octets pour chaque chiffrement. Le chiffrement unique au moment du build rend la réutilisation impossible par construction. IV dérivé (`HKDF(key, tensor_name)`) pour des builds déterministes.

---

## Stockage des clés : magasins d'identifiants du système d'exploitation {#key-storage-os-credential-stores}

### DPAPI Windows {#windows-dpapi}

DPAPI dérive la clé de chiffrement à partir des identifiants de session de l'utilisateur. Elle est liée à l'utilisateur et à la machine.

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

**Propriétés de DPAPI :**
- `CRYPTPROTECT_LOCAL_MACHINE` : tout utilisateur de la même machine peut déchiffrer. Pour une protection par utilisateur, utiliser `CRYPTPROTECT_CURRENT_USER` (par défaut, sans drapeau).
- MasterKey stockée dans `%APPDATA%\Microsoft\Protect\{SID}`, chiffrée avec le mot de passe utilisateur et, optionnellement, une clé de domaine.
- Survit au redémarrage et aux mises à jour du système. Ne survit pas à la réinstallation du système ni à la suppression du profil utilisateur.
- Le même utilisateur peut toujours déchiffrer ; les autres utilisateurs de la machine ne le peuvent pas (mode par utilisateur).

### Trousseau macOS (Keychain) {#macos-keychain}

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

**Option Secure Enclave :** générer une clé P256 dans la SE et l'utiliser pour une clé symétrique dérivée par ECDH. La clé n'est jamais extractible du matériel.

---

## Chiffrement par enveloppe (architecture de clés hybride) {#envelope-encryption-hybrid-key-architecture}

Un seul fichier de modèle chiffré pour tous les utilisateurs, plus un petit matériel de clé par utilisateur :

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

**Avantages :**
- Un seul `.hmod` sur le CDN (200 Mo), identique pour tous les utilisateurs
- `license_blob` par utilisateur (~1 Ko), émis lors de l'activation
- Révocation du modèle : cesser d'émettre de nouveaux `license_blob`
- Rotation de la clé du modèle : générer une nouvelle MCK, rechiffrer les tenseurs, publier un nouveau fichier sur le CDN

---

## Dérivation de clés (HKDF) {#key-derivation-hkdf}

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

## Performance de déchiffrement (AES-NI, x86-64) {#decryption-performance-aes-ni-x86-64}

| Taille des données | AES-256-GCM | ChaCha20-Poly1305 |
|-----------|-------------|-------------------|
| 1 Mo | ~0,5 ms | ~0,6 ms |
| 10 Mo | ~4,5 ms | ~5,5 ms |
| 100 Mo | ~45 ms | ~55 ms |
| 200 Mo | ~90 ms | ~110 ms |
| Dérivation HKDF | <1 ms | - |

Un modèle de 200 Mo se déchiffre en ~90 ms, imperceptible pour l'utilisateur au démarrage.

**Support matériel :**
- Windows x64 : AES-NI sur Intel (Westmere, 2010 et après), AMD (Bulldozer, 2011 et après)
- macOS Intel : AES-NI ; Apple Silicon : extensions cryptographiques ARM (vitesse équivalente)
- Toujours vérifier `crypto_aead_aes256gcm_is_available()` avant d'utiliser AES-GCM

---

## Format CryptoTensors (arxiv:2512.04580) {#cryptotensors-format-arxiv251204580}

Extension de SafeTensors avec chiffrement au niveau des tenseurs :
- DEK (clé de chiffrement des données) par tenseur + IV unique
- En-tête en clair, mais signé en Ed25519
- Prise en charge des politiques via Rego/OPA pour le contrôle d'accès
- Compatible avec HuggingFace Transformers et vLLM

**CryptoTensors vs .hmod (format maison) :**

| Aspect | CryptoTensors | .hmod |
|--------|--------------|-------|
| Format de base | Extension de SafeTensors | Binaire entièrement personnalisé |
| AES-GCM par tenseur | Oui | Oui |
| Lisible dans Netron | Partiellement (en-tête ouvert) | Non (magic personnalisé) |
| Source des clés | JWK, KBS, HTTP | HKDF(device_fp + license) |
| Cas d'usage desktop | Cloud/serveur | Anti-piratage desktop |

Recommandation pour le format maison : `.hmod` avec un en-tête binaire (non JSON). Les formats basés sur SafeTensors restent analysables avec les outils Python standard même sans clés (les en-têtes exposent les noms et les formes des tenseurs).

---

## Chiffrement sélectif (tenseurs critiques uniquement) {#selective-encryption-critical-tensors-only}

Chiffrement complet du modèle : tous les poids sont protégés, mais le déchiffrement est le plus lent.
Sélectif : chiffrer uniquement les tenseurs critiques (5 à 10 % en nombre, plus de 90 % de l'impact sur la qualité).

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

CORELOCKER (IEEE S&P 2024, arxiv:2303.12397) : chiffrer uniquement les tenseurs critiques et les servir depuis un serveur (jamais sur le disque). Les tenseurs non critiques restent en clair : le modèle se dégrade progressivement sans les poids clés, mais ne fonctionne pas pleinement.

---

## Pièges à éviter {#gotchas}

- **La réutilisation d'un nonce AES-GCM est catastrophique.** Même clé + même nonce = XOR des textes en clair révélé + clé d'authentification récupérable. Utiliser un nonce aléatoire de 12 octets par chiffrement. Le chiffrement unique au moment du build rend la réutilisation accidentelle impossible.
- **DPAPI `CRYPTPROTECT_LOCAL_MACHINE` = tout utilisateur de la machine peut déchiffrer.** Pour lier le matériel de clé au seul utilisateur courant, utiliser le mode par utilisateur (par défaut, aucun drapeau nécessaire).
- **Effacer les données sensibles après déchiffrement.** `memset` peut être supprimé par l'optimiseur. Utiliser `sodium_memzero()` ou `SecureZeroMemory()` (Windows).
- **Sandbox du Mac App Store :** l'accès au Trousseau est cloisonné par conteneur d'application. Le conteneur est supprimé à la désinstallation de l'application, et l'entrée du Trousseau avec lui. Pour une distribution hors App Store, les entrées du Trousseau survivent à la désinstallation.
- **Sortie maximale de HKDF-Expand = 255 × HashLen = 8160 octets** pour SHA-256. Pour un matériel de clé plus grand, utiliser un flux ChaCha20 initialisé avec la sortie de HKDF.
- **Échec partiel d'authentification = rejeter le modèle entier.** Si le tag d'authentification d'un seul tenseur échoue, ne charger aucun tenseur. Il s'agit soit d'une corruption du fichier (retélécharger), soit d'une altération (refuser et journaliser).
- **L'instruction AES-NI d'Intel peut être présente mais désactivée par le BIOS** sur certains systèmes anciens. Toujours appeler `crypto_aead_aes256gcm_is_available()` et prévoir un repli vers ChaCha20.

## Voir aussi {#see-also}
- [[watermarking-encrypted-models]]
- [[hkdf-personalized-weights]]
- [[onnx-model-protection]]
- [[licensing-implementation-cpp]]
