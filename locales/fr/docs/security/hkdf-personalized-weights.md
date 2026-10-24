---
level: 3
source_sha256: 2aaf366802e80ca6615437250800d3a7faf74f9a0bb5ba96e8298d2f25866aad
translation: machine
translated_at: '2026-10-24'
---
# HKDF + ChaCha20 : poids de réseaux de neurones personnalisés {#hkdf-chacha20-personalized-neural-network-weights}

Date : 2026-04-03
Contexte : application C++ de bureau, inférence avec ONNX Runtime. Poids uniques par utilisateur grâce à une graine dérivée par HKDF et à un flux ChaCha20. Modèles fonctionnellement équivalents : la symétrie de permutation garantit des sorties identiques.

---

## Concept central {#core-concept}

Le serveur détient le `master_secret`. Une dérivation HKDF par utilisateur produit les graines de 3 opérations :
- **Permutation** : mélange des indices de neurones (sans perte, mathématiquement équivalent)
- **Échelle** : perturbation multiplicative des poids (~±3 %)
- **Décalage** : perturbation additive des poids (~±0,5 % de la magnitude du poids)

Les poids du modèle de chaque utilisateur sont uniques, tout en produisant des sorties identiques (à la tolérance des calculs en virgule flottante près).

---

## Implémentation HKDF + ChaCha20 {#hkdf-chacha20-implementation}

### Pourquoi cette combinaison {#why-this-combination}

**HKDF seul :** limité à 255 × HashLen = 8160 octets pour SHA-256. Insuffisant pour des modèles de plus de 100 M de paramètres.

**Solution :** HKDF génère des graines de 32 octets, et ChaCha20 les étend en un flux de longueur arbitraire.

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

### Choix de la bibliothèque {#library-choice}

| Bibliothèque | HKDF | Vitesse | API |
|--------------|------|---------|-----|
| OpenSSL 3.x | EVP_KDF | Meilleure (SHA-256 matériel) | Code de service verbeux |
| libsodium 1.0.19+ | `crypto_kdf_hkdf_sha256_*` | ~20 % plus lent | Simple, résistant aux mauvaises utilisations |
| Autonome (RFC 5869) | Personnalisé | Dépend de HMAC | Contrôle total |

**Recommandation : libsodium.** Déjà nécessaire pour d'autres opérations cryptographiques. ChaCha20 atteint ~1705 MiB/s sans AES-NI (important pour les machines dotées d'un GPU faible).

**ChaCha12 vs ChaCha20 :** 12 tours sont ~1,6× plus rapides. Suffisant pour ce modèle de menace (PRNG, pas de chiffrement). Temps total estimé de personnalisation pour un modèle de 100 M de paramètres : <500 ms sur un CPU lent.

### Code (libsodium) {#code-libsodium}

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

### Alternative OpenSSL 3.x {#openssl-3x-alternative}

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

Davantage de code de service, dépendance plus lourde, et aucune API pratique de flux ChaCha20.

---

## Symétrie de permutation : quelles couches peuvent être permutées {#permutation-symmetry-which-layers-can-be-permuted}

### Théorie {#theory}

**Symétrie de permutation** (arxiv:2506.13018, arxiv:2502.17391) : pour une couche FC à n neurones, il existe n! paramétrisations équivalentes produisant **la même sortie**. Permuter le neurone i→j implique :
1. Permuter la ligne i→j dans la matrice de poids de sortie de cette couche
2. Permuter la colonne i→j dans la matrice de poids d'entrée de la **couche suivante**
3. Permuter les biais correspondants

**Articles confirmant la préservation de la qualité :**
- NeuPerm (arxiv:2510.20367) : permuter les couches cachées d'un LLM = baisse de précision <0,01 %
- Git Re-Basin (arxiv:2209.04836) : exploite la même symétrie pour la fusion de modèles

### Règles par couche {#layer-by-layer-rules}

| Type de couche | Permutation sûre ? | Quoi permuter | Contraintes |
|----------------|--------------------|---------------|-------------|
| **Entièrement connectée** | OUI | Lignes de W_out + colonnes de W_in + biais | Symétrie de permutation classique |
| **Conv2d (cachée)** | OUI | Canaux de sortie = « neurones ». Permuter les canaux de sortie de la couche courante + les canaux d'entrée de la suivante + biais | Identique à FC |
| **Convolution groupée** | PARTIEL | Uniquement au sein de chaque groupe | Les groupes ne peuvent pas être échangés |
| **Convolution depthwise** | NON | 1 filtre = 1 canal, la permutation n'a pas de sens | |
| **Attention Q/K/V** | PARTIEL | Permuter les têtes d'attention comme unités entières | Impossible de permuter des neurones au sein d'une tête sans une permutation cohérente de Q, K et V |

### Couches qui NE PEUVENT PAS être permutées indépendamment {#layers-that-cannot-be-permuted-independently}

| Couche | Raison | Conséquence |
|--------|--------|-------------|
| **BatchNorm** | Stocke running_mean/var par canal | Doit être permutée avec la convolution qui la précède |
| **LayerNorm** | gamma/beta liés aux positions des caractéristiques | Identique : permuter avec la couche précédente |
| **Connexions résiduelles (skip)** | L'entrée et la sortie doivent partager le même ordre | La permutation dans un bloc doit être annulée en sortie (P_out = P_in^(-1)) |
| **Couche d'entrée** | Canaux liés à RGB | Ne jamais permuter les canaux d'entrée |
| **Couche de sortie** | Canaux liés à la tâche (sortie RGB) | Ne jamais permuter les canaux de sortie |

### Spécificités de U-Net {#u-net-specifics}

U-Net avec connexions de saut est le cas le plus complexe :

```yaml
Encoder:              Decoder:
conv1 → pool ----skip---→ upconv4 + concat
conv2 → pool ----skip---→ upconv3 + concat
conv4 (bottleneck)  ---→ upconv1
```

Règles :
1. **Goulot d'étranglement (conv4) :** SÛR. Pas de connexion de saut ; les canaux sont autonomes.
2. **Convolution d'encodeur dans un bloc :** SÛR si la permutation se propage dans le bloc et s'annule avant le saut.
   - Permuter les canaux de sortie de conv1 → permuter BN1 → permuter les canaux d'entrée de conv2
   - NE PAS toucher aux canaux de sortie de conv2 (ils alimentent le saut)
3. **Canaux de connexion de saut :** doivent correspondre à l'entrée du décodeur après concaténation. Permuter la sortie de l'encodeur impose une permutation correspondante du décodeur.
4. **Têtes d'attention (U-Net de Stable Diffusion) :** permuter les têtes entières (8 têtes = 8! = 40320 variantes, trop peu pour la sécurité).

### Stratégie pratique pour le modèle de retouche {#practical-strategy-for-retouching-model}

**Permuter uniquement : le goulot d'étranglement + les convolutions internes des blocs résiduels.**

Gains de sécurité :
- Goulot d'étranglement à 512 canaux : 512! ~ 10^1166 permutations
- Chaque bloc convolutif à 256 canaux : 256! ~ 10^507
- Combinés : espace de recherche astronomique

NE PAS toucher : couches d'entrée/sortie, frontières des connexions de saut.

---

## Injection d'échelle et de décalage {#scaleoffset-injection}

### Plages de perturbation sûres {#safe-perturbation-ranges}

| Type de couche | Plage d'échelle | Plage de décalage | Remarques |
|----------------|-----------------|-------------------|-----------|
| Conv2d (cachée) : conservateur | 0,97 - 1,03 | ±0,005 | **Recommandé** |
| Conv2d (cachée) : standard | 0,95 - 1,05 | ±0,02 | Risque de dégradation visible |
| Linear (cachée) | 0,95 - 1,05 | ±0,01 | Poids FC souvent plus grands, moins sensibles |
| BatchNorm gamma/beta | 0,98 - 1,02 | ±0,01 | BN sensible : petites perturbations seulement |
| Attention Q/K/V | 0,97 - 1,03 | ±0,005 | Le produit scalaire amplifie les erreurs quadratiquement |
| Première/dernière couche | **NE PAS TOUCHER** | **NE PAS TOUCHER** | Impact direct sur la correspondance entrée/sortie |

### Pourquoi le décalage est plus dangereux que l'échelle {#why-offset-is-more-dangerous-than-scale}

Échelle 0,97-1,03 = écart de ±3 %. Pour un poids de convolution typique d'environ 0,05, cela représente ±0,0015 (faible).

Décalage ±0,02 pour ce même poids = ±40 % de la valeur (catastrophique pour les petits poids).

**Meilleure approche : décalage relatif proportionnel à la magnitude du poids :**

```cpp
// w' = w * scale + offset * |w|
// offset here is a coefficient, not absolute value
float perturbed = weight * scale + offset_coeff * fabsf(weight);
```

Cela maintient les perturbations proportionnelles à la magnitude du poids.

### Vérification de l'équivalence fonctionnelle {#functional-equivalence-verification}

Après personnalisation, vérifier que la sortie correspond à la référence :

```cpp
// Run original and personalized model on same input
// Maximum acceptable per-pixel difference: ~0.001 (float32)
// PSNR should remain > 50 dB
float max_diff = 0.0f;
for (size_t i = 0; i < output_size; i++)
    max_diff = std::max(max_diff, fabsf(orig[i] - personalized[i]));
assert(max_diff < 1e-3f); // permutation must be lossless
```

La permutation doit être **exactement** sans perte (max_diff ≈ epsilon FP32). L'échelle et le décalage introduiront de petites perturbations.

---

## Rotation des époques {#epoch-rotation}

Le champ d'époque dans la dérivation HKDF permet une rotation périodique des clés sans régénérer les poids :

```cpp
// info = "user:{account_id}:perm:epoch:{epoch_num}"
// Each epoch produces completely different permutation for same account
// Leaked weights from epoch N are useless after epoch increment
snprintf(info_perm, sizeof(info_perm),
    "user:%s:perm:epoch:%u", account_id, epoch);
```

Déclencheurs de mise à jour de l'époque :
- Mise à jour du modèle (toutes les 2 à 4 semaines)
- Soupçon de compromission d'un ou de plusieurs comptes spécifiques
- Rotation planifiée (par exemple tous les 90 jours)

Le serveur ne stocke que : `{account_id, epoch, master_secret}` (~300 octets par utilisateur). Tous les poids personnalisés sont calculés à la demande. 1 M d'utilisateurs = ~12 requêtes/s pour un usage typique = tient sur un VPS à 20 $/mois.

## Contraintes de quantification INT8 {#int8-quantization-constraints}

Les perturbations d'échelle et de décalage doivent survivre à la quantification INT8 si elle est utilisée :

```text
INT8 range: [-128, 127] → float range ≈ [-1.0, 1.0] (typical scale ~0.0078)
Minimum distinguishable delta: 1 LSB = 0.0078

Safe perturbation for INT8:
  scale: 0.998 - 1.002 (not 0.95-1.05 - these cause LSB collapse)
  offset: ±0.001 * abs(w) (relative)
```

FP16 est plus permissif : 1 LSB ≈ 6e-5 (moitié de la plage d'exposant). Une échelle de 0,97-1,03 est sûre pour FP16.

## Remplacement des poids ONNX {#onnx-weight-swap}

Charger le modèle de base, appliquer la permutation en mémoire, puis exécuter l'inférence : aucune modification du fichier de modèle n'est nécessaire :

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

Pour le C++ via l'API C d'ONNX : modifier les tenseurs `OrtValue` avant la création de la session, en utilisant `CreateTensorWithDataAsOrtValue` avec le tampon permuté.

## Pièges {#gotchas}

- **Les chaînes d'information de HKDF-Expand doivent être uniques par usage.** Utiliser la même info pour les graines de permutation et d'échelle produit la même clé, ce qui annule complètement la séparation des usages. Toujours utiliser des étiquettes distinctes.
- **Biais de modulo dans Fisher-Yates :** `raw % (i+1)` est légèrement biaisé lorsque i+1 n'est pas une puissance de 2. Pour des permutations de n < 2^24, ce biais est négligeable (< 10^-7). Pour un mélange de qualité cryptographique, utiliser un échantillonnage par rejet.
- **nonce=0 avec ChaCha20 est sûr ici** car chaque graine est une clé unique de 256 bits (dérivée de chaînes d'information HKDF différentes). Une clé différente produit un flux différent, quel que soit le nonce.
- **Permuter BatchNorm séparément de la convolution corrompt le modèle.** Toujours co-permuter : `{conv.weight, conv.bias, bn.weight, bn.bias, bn.running_mean, bn.running_var}`.
- **Les connexions de saut dans U-Net exigent des permutations appariées.** Permuter uniquement le côté encodeur sans faire correspondre l'entrée du décodeur produira des sorties erronées aux points de concaténation des sauts.
- **La permutation des têtes d'attention ne donne que n_heads! variantes** (par exemple 8! = 40320 pour 8 têtes). Insuffisant pour la sécurité. Permuter plutôt les neurones au sein des têtes, de manière cohérente pour Q, K et V.
- **Les perturbations d'échelle et de décalage s'accumulent d'une couche à l'autre.** Dans les réseaux profonds (50 couches et plus), même une perturbation de 0,3 % par couche se cumule. Toujours tester le PSNR de la sortie finale, et pas seulement les métriques par couche.
- **La fuite du master secret compromet tous les utilisateurs.** Stocker le master_secret dans un HSM ou une enclave sécurisée côté serveur. Ne jamais l'envoyer aux clients.
- **La quantification INT8 écrase les grandes perturbations.** Une échelle de 0,95-1,05 tombe dans le même intervalle INT8 : la personnalisation disparaît. Utiliser une échelle de 0,998-1,002 pour les modèles compatibles avec la quantification.
- **Attaque par moyenne des poids :** un adversaire moyenne les poids personnalisés de K utilisateurs en espérant que la permutation s'annule. La permutation l'en empêche (les neurones sont à des positions différentes), mais ce n'est pas le cas de l'échelle et du décalage : une défense supplémentaire est nécessaire si cette menace est réaliste.

## Voir aussi {#see-also}
- [[watermarking-encrypted-models]]
- [[output-scrambling-antipiracy]]
- [[licensing-implementation-cpp]]
