---
level: 3
source_sha256: 480cc86eb403f957b1067273798c28c0d95bf891f7239ba0cf8d66eee50017df
translation: machine
translated_at: '2026-10-24'
---
# Filigrane des sorties de réseaux de neurones + format de modèle chiffré .hmod {#watermarking-neural-network-outputs-hmod-encrypted-model-format}

Date: 2026-04-03
Contexte : application de retouche d'images de bureau en C++ ; filigrane invisible sur chaque image de sortie ; modèles stockés dans le format chiffré .hmod, avec AES-256-GCM par tenseur et signature Ed25519 de l'en-tête.

---

## Filigrane invisible {#invisible-watermarking}

### StegaStamp (CVPR 2020) {#stegastamp-cvpr-2020}

Source : Matthew Tancik et al. (UC Berkeley). Dépôt : https://github.com/tancik/StegaStamp

**Architecture de l'encodeur :**
- Entrée : RGB 400×400×3 + message de 100 bits
- Message → couche FC → 50×50×3 → suréchantillonnage → 400×400×3
- Concaténation avec l'image → 400×400×4
- U-Net → résiduel 400×400×3
- Sortie : original + résiduel écrêté

**Décodeur :**
- Entrée : image encodée (potentiellement altérée)
- Spatial Transformer Network (STN) pour la correction de perspective
- Couches conv + FC → sigmoïde → probabilités sur 100 bits

**Correction d'erreurs :** BCH(100, 56) : 100 bits au total = 56 bits de données + 44 bits ECC.

**C++ via ONNX Runtime :**

```text
tf2onnx: TF 1.13 checkpoint → freeze_graph → tf2onnx → .onnx
```

API clé d'ONNX Runtime : `CreateSessionFromArray()` - charge le modèle depuis un tampon en mémoire déchiffré. Aucun modèle en clair n'est jamais écrit sur le disque.

**Fournisseurs d'exécution (execution providers) :**
- Windows : DirectML EP (tout GPU DX12 : NVIDIA/AMD/Intel)
- macOS : CoreML EP (Apple Neural Engine)

**Performances :**

| Résolution | CPU (i7-12700) | GPU (RTX 3060) |
|------------|----------------|----------------|
| 400×400 (natif) | 15-30 ms | 3-8 ms |
| 1024×1024 | 100-200 ms | 15-30 ms |
| 2048×2048 | 200-400 ms | 25-50 ms |

StegaStamp opère sur une taille fixe de 400×400. Options pour les images plus grandes :
- A : redimensionner → intégrer → redimensionner en retour (rapide, perte de détail dans le filigrane)
- B : par tuiles (intégrer dans chaque tuile, redondant, robuste au recadrage)
- C : utiliser TrustMark (résolution arbitraire)

**Surcharge mémoire :** ~100-150 Mo (modèle ~30 Mo + tampons ONNX Runtime).

### TrustMark (Adobe, ICCV 2025) {#trustmark-adobe-iccv-2025}

Dépôt : https://github.com/adobe/trustmark

**Avantages par rapport à StegaStamp :**
- Résolution arbitraire (pas de contrainte 400×400)
- Charge utile de 100 bits avec ECC configurable (BCH_SUPER, BCH_5, BCH_4, BCH_3)
- Modèles ONNX déjà disponibles (utilisés dans l'implémentation JS)
- PSNR ~50 dB (artefacts quasi invisibles)
- Conçu pour C2PA (Content Authenticity Initiative)
- Implémentation Rust disponible pour FFI

**RECOMMANDATION : TrustMark plutôt que StegaStamp** pour les nouvelles implémentations - pas de redimensionnement, déjà au format ONNX, activement maintenu (2025).

### Étalement de spectre DCT (alternative sans modèle) {#dct-spread-spectrum-no-model-alternative}

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

**DCT vs neuronal :**

| Critère | Étalement de spectre DCT | Neuronal (StegaStamp/TrustMark) |
|-----------|--------------------|-----------------------------|
| Taille du modèle | 0 Mo | 15-30 Mo |
| Vitesse | <5 ms | 15-200 ms |
| JPEG Q=90 | 85-95 % des bits | 98 %+ des bits |
| JPEG Q=70 | 60-80 % des bits | 95 %+ des bits |
| Recadrage 20 % | 30-50 % des bits | 90 %+ des bits |
| Impression-numérisation | ~50 % | 95 %+ des bits |

**L'approche neuronale est indispensable pour la lutte contre le piratage.** La DCT est trop facilement cassée par le recadrage combiné à la compression JPEG.

### Robustesse (benchmark WAVES, NeurIPS 2024) {#robustness-waves-benchmark-neurips-2024}

Robustesse de StegaStamp :

| Attaque | Précision des bits |
|--------|-------------|
| JPEG Q=90 | ~99 % |
| JPEG Q=70 | ~96-98 % |
| JPEG Q=50 | ~92-95 % (BCH corrige) |
| Redimensionnement à 50 %+ retour | ~96 % |
| Capture d'écran | ~94-97 % |
| Flou/bruit | ~95-99 % |
| Impression + numérisation | ~95 % (cas d'usage principal !) |
| Régénération par diffusion | ~70-85 % (vulnérable) |
| Attaque adversariale | ~60-80 % |

### Conception de la charge utile (64 bits recommandés) {#payload-design-64-bit-recommended}

```text
[32 bits: license_id hash]
[16 bits: timestamp - days since 2025-01-01] = 180 years coverage
[8 bits: app_version + model_version]
[8 bits: CRC-8 or additional ECC]
```

Avec TrustMark (100 bits) : 64 bits de données + 36 bits d'ECC.
Avec BCH(100,56) de StegaStamp : 48 bits de données tiennent confortablement dans la charge utile de 56 bits.

**Filigrane d'essai :** `license_id = 0x00000000` (réservé). Suivi invisible + superposition visible (deux couches).

### Outil de décodage {#decoder-tool}

```yaml
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

Taux de faux positifs : ~1 sur 10^6 au seuil 0,8. Seuil recommandé : 0,85.

---

## Format de modèle chiffré .hmod {#hmod-encrypted-model-format}

### Pourquoi AES-256-GCM {#why-aes-256-gcm}

- **GCM = chiffrement + authentification en une seule passe.** CBC nécessite un HMAC séparé.
- GCM détecte automatiquement les altérations (tag d'authentification).
- GCM se parallélise (mode compteur) ; CBC ne le peut pas (dépend du bloc précédent).
- Débit AES-NI : GCM ~2,2 Go/s, CBC ~1,5 Go/s.

**Nonce par tenseur (12 octets) :** doit être unique à chaque chiffrement sous une même clé.
- IV aléatoire : `crypto_random_bytes(12)` - simple, sûr pour moins de 2^48 opérations
- IV dérivé : `HKDF(key, tensor_name + counter)` - déterministe

**Recommandation : IV aléatoire.** Le chiffrement étant unique (à la compilation), la réutilisation d'un nonce est impossible par construction.

### Dérivation de clé HKDF {#hkdf-key-derivation}

```text
HKDF-SHA256(
  input_key_material = device_fingerprint || license_key,
  salt = random_salt (32 bytes, stored in file header),
  info = "hmod-v1-tensor-decryption",
  output_length = 32
)
```

### Spécification du format de fichier {#file-format-specification}

```yaml
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

**Par rapport à SafeTensors :**
1. En-tête binaire (et non JSON) - Netron/Python ne peuvent pas le lire sans notre code
2. Octets magiques personnalisés - non reconnu comme format connu
3. Données de tenseurs chiffrées - octets dénués de sens sans la clé
4. Aucun espace autorisé - empêche les fichiers polyglottes

**Par rapport à CryptoTensors (arxiv:2512.04580) :**

| Aspect | CryptoTensors | .hmod |
|--------|--------------|-------|
| Format de base | Extension de SafeTensors | Entièrement personnalisé |
| AES-GCM-256 par tenseur | Oui | Oui |
| DEK par tenseur | Oui | Oui |
| Source de clé | JWK, KBS, HTTP | HKDF(device_fp + license) |
| Politiques | Rego OPA | Aucune (bureau) |
| Lisible par Netron | Partiellement | Non (magic personnalisé) |
| Surcharge au chargement | 2-8x | Cible : <2x |

### Gestion hybride des clés (chiffrement d'enveloppe) {#hybrid-key-management-envelope-encryption}

```text
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

**Modèle de distribution :**
- Un `.hmod` sur CDN (~200 Mo) - identique pour tous les utilisateurs
- `license_blob` par utilisateur (~1 Ko) - émis à l'activation
- Révocation : cesser d'émettre le `license_blob` de l'utilisateur concerné
- Compromission : générer une nouvelle MCK, re-chiffrer le `.hmod`, tous les utilisateurs reçoivent un nouveau `license_blob`

### Performances de chargement (AES-NI) {#loading-performance-aes-ni}

| Opération | Durée |
|-----------|------|
| Déchiffrement AES-256-GCM 1 Mo | ~0,5 ms |
| Déchiffrement AES-256-GCM 10 Mo | ~4,5 ms |
| Déchiffrement AES-256-GCM 200 Mo | ~90 ms |
| Dérivation de clé HKDF | <1 ms |
| Vérification d'en-tête Ed25519 | <1 ms |

Un modèle de 200 Mo se déchiffre en ~90 ms, un délai imperceptible pour l'utilisateur.

**Support matériel :**
- Windows x64 : AES-NI sur tous les Intel (Westmere 2010+) / AMD (Bulldozer 2011+)
- macOS Intel : AES-NI ; Apple Silicon : extensions cryptographiques ARM
- libsodium : vérification `crypto_aead_aes256gcm_is_available()` obligatoire

### Chaîne d'outils {#toolchain}

**hmod_packer :**
```yaml
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

**key_weight_analyzer (analyse de sensibilité) :**
```toml
For each tensor: replace with random → measure output degradation
Top 5-10% most impactful = "critical tensors" → must encrypt
Remaining = "non-critical" → optional (speed tradeoff)
```

**hmod_validator :**
```text
1. Check magic + version
2. Parse header (no corruption)
3. Verify Ed25519 signature
4. Per tensor: decrypt + auth tag verify
5. Shape/dtype consistency check
```

---

## SEAL : filigrane pour les poids LoRA {#seal-watermarking-for-lora-weights}

Les adaptateurs LoRA posent des défis spécifiques : petits poids delta (rang 4-64), pouvant être fusionnés dans le modèle de base ou utilisés de manière autonome.

**Approche SEAL (Signed Efficient Adaptation for LLMs) :**
- Intégrer le filigrane pendant l'entraînement LoRA (et non a posteriori)
- Le filigrane survit au fine-tuning, à la fusion et à la quantification
- Détection par test d'hypothèse statistique sur le modèle suspect
- Limite : nécessite de réentraîner le LoRA avec l'objectif de filigrane

**Alternative pratique pour la détection de LoRA volés :**
- Intégrer de minuscules motifs sentinelles dans les données d'entraînement (prompts spécifiques → sorties spécifiques)
- « Sorties canari » vérifiables sans accès aux poids originaux
- Fonctionne même après fusion : le modèle fusionné répond toujours aux prompts sentinelles

**Menaces propres à LoRA :**
- StolenLoRA : extraction des deltas LoRA via des requêtes API répétées (30-100 requêtes suffisent généralement pour un LoRA de rang 4)
- Attaque par fusion : fusionner le LoRA dans le modèle de base dilue le filigrane
- Quantification : INT4/INT8 détruit souvent les motifs subtils du filigrane

## Distribution .hmod par utilisateur {#per-user-hmod-distribution}

**Un fichier CDN + un blob de licence par utilisateur (1 Ko)** constitue l'architecture correcte :
- `.hmod` (~200 Mo) : identique pour tous, sur CDN (Cloudflare R2 : 5-10 $/mois)
- `license_blob` (~1 Ko) : par utilisateur, émis à l'activation
  - Contient : enveloppe MCK chiffrée + matériel de dérivation de clé utilisateur
  - Révocation : cesser d'émettre de nouveaux `license_blob` ; les existants expirent selon leur TTL
- Compromission : générer une nouvelle MCK, re-chiffrer le `.hmod`, émettre un nouveau `license_blob` à tous les utilisateurs

**Procédure de rotation des clés :**
1. Générer une nouvelle MCK (clé de contenu du modèle)
2. Re-chiffrer tous les tenseurs avec de nouveaux DEK enveloppés sous la nouvelle MCK
3. Incrémenter la version/époque du modèle dans le contexte de dérivation HKDF
4. Publier le nouveau `.hmod` sur le CDN
5. Tous les utilisateurs récupèrent le nouveau `license_blob` au prochain phone-home

## Pièges {#gotchas}

- **La réutilisation d'un nonce AES-GCM est catastrophique.** Même nonce + même clé = XOR des textes clairs révélé + clé d'authentification récupérable. Dans .hmod : le chiffrement est unique à la compilation, avec un nonce aléatoire, donc la réutilisation est impossible par construction. Si vous ajoutez un re-chiffrement (par exemple une personnalisation à la volée), soyez extrêmement prudent.
- **Limite AES-GCM de 64 Go par nonce.** Un tenseur ne peut pas dépasser 64 Go. Les modèles font typiquement 200 Mo au total : pas de problème.
- **Échec partiel du déchiffrement = arrêt immédiat.** Si le tag d'authentification d'un tenseur échoue, ne chargez pas le modèle. Il s'agit soit d'un fichier corrompu (à retélécharger), soit d'un fichier altéré (à refuser).
- **`CreateSessionFromArray` dans ONNX Runtime** permet de charger un modèle depuis un tampon en RAM sans toucher au disque. Point critique : utilisez-le plutôt que de charger depuis un fichier temporaire déchiffré.
- **StegaStamp utilise TF 1.13** : il nécessite un ancien environnement TensorFlow pour l'entraînement ou la conversion. Utilisez tf2onnx pour obtenir un modèle ONNX ; il ne faut ensuite que ONNX Runtime pour l'inférence.
- **Le seuil de confiance de TrustMark à 0,85** est le compromis recommandé. Le descendre à 0,7 fait passer le taux de faux positifs de 1:10^6 à environ 1:1000.
- **Les attaques par régénération par diffusion** (DALL-E, Midjourney « rinsing ») réduisent la précision de StegaStamp à 70-85 %. Atténuation : utiliser des filigranes à durée de vie plus courte, ou accepter ce modèle de menace pour un usage forensique (et non d'authentification).
- **Un en-tête binaire (et non JSON) dans .hmod** signifie l'absence de compatibilité gratuite avec les outils existants. Fournissez une CLI de validation pour vérifier les fichiers dans la chaîne de compilation.
- **Filigrane d'essai :** réservez `license_id = 0x00000000`. Ajoutez une superposition visible (deux couches : filigrane forensique invisible + indicateur visible d'essai). Les deux sont gérés par le même pipeline d'encodage.
- **Charge utile (TrustMark 100 bits) :** 32 bits de hash de `license_id` + 16 bits de jours depuis l'époque (couvre 180 ans) + 8 bits de version app/modèle + 8 bits de CRC-8 = 64 bits de données + 36 bits d'ECC.

## Voir aussi {#see-also}
- [[hkdf-personalized-weights]]
- [[output-scrambling-antipiracy]]
- [[remote-kill-switch]]
- [[licensing-implementation-cpp]]
