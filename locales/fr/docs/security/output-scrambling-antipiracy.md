---
level: 4
source_sha256: 69f916eb4c022cbedfc7931c035d5fd911dbe4959a63a967c5b94b93a75e9430
translation: machine
translated_at: '2026-10-24'
---
# Brouillage des sorties de réseaux de neurones : protection anti-piratage pour moteurs d'inférence {#neural-network-output-scrambling-anti-piracy-for-inference-engines}

Date : 2026-04-03
Contexte : application C++ de bureau avec inférence ONNX. Le modèle produit un tenseur brouillé ; un processus convertisseur séparé et obfusqué applique une formule dérivée de la clé de session secrète pour produire une image normale.

---

## Approche d'entraînement {#training-approach}

### Approche A : intégrer le brouillage à l'entraînement {#approach-a-bake-scramble-into-training}

Perte = MSE(sortie_modèle, brouillage(vérité_terrain)). Le modèle apprend à prédire la représentation brouillée.

**Avantages :** l'image normale n'existe jamais dans la mémoire GPU, pas même de façon transitoire.
**Inconvénients :** nécessite un réentraînement. La fonction de brouillage doit être différentiable :
- Permutation de canaux ou spatiale : différentiable (réordonnancement d'indices)
- XOR avec la clé : NON différentiable directement (utiliser un straight-through estimator)
- LUT : NON différentiables
- Perte de qualité de 1 à 3 % en PSNR pour un brouillage non linéaire

### Approche B : post-traitement (sans réentraînement) - RECOMMANDÉE {#approach-b-post-processing-no-retraining-recommended}

Entraînement normal. Ajouter le brouillage comme opérateur personnalisé ONNX (dernier nœud du graphe). Le brouillage s'exécute sur le GPU ; la sortie est déjà brouillée lorsqu'elle est copiée vers le CPU.

```cpp
// Register ONNX Runtime custom op
struct ScrambleOp : Ort::CustomOpBase<ScrambleOp, ScrambleKernel> {
    const char* GetName() const { return "Scramble"; }
    size_t GetInputTypeCount() const { return 2; } // tensor + key
    size_t GetOutputTypeCount() const { return 1; }
    ONNXTensorElementDataType GetInputType(size_t) const {
        return ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT;
    }
    ONNXTensorElementDataType GetOutputType(size_t) const {
        return ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT;
    }
};
```

Insérer le nœud de brouillage dans le modèle exporté existant via la manipulation de graphe ONNX (aucun réentraînement requis).
Surcoût de performance : environ 0,1 à 0,5 ms de noyau CUDA supplémentaire. Négligeable face à une inférence de 50 à 200 ms.

---

## Techniques de brouillage {#scrambling-techniques}

### Permutation de canaux {#channel-permutation}

Pour du RGB (3 canaux) : seulement 3! = 6 permutations. Testables par force brute en quelques microsecondes.

**Solution :** permuter les canaux intermédiaires (64 canaux dans l'avant-dernière couche). 64! ≈ 10^89 variantes. Implémentation par permutation des lignes ou colonnes de la matrice de poids de la dernière convolution : aucune modification du modèle n'est nécessaire.

### Brouillage spatial {#spatial-scrambling}

| Niveau | Espace de recherche | Résistance à l'attaque par puzzle | Surcoût |
|-------|-------------|--------------------------|---------|
| Niveau bloc (16x16) | (64×64)! ≈ 10^9000+ | **Faible** : un solveur de puzzle retrouve l'ordre par correspondance des bords de blocs | Minimal |
| Niveau pixel | (1024×1024)! | **Moyenne** : histogramme préservé au sein des canaux | Moyen |
| Niveau pixel + mélange de canaux | Astronomique | **Élevée** : détruit les corrélations spatiales ET chromatiques | Moyen |
| Domaine DCT | Dépend de l'implémentation | **Élevée** : détruit la cohérence spatiale | Important |

**Recommandation : permutation au niveau pixel + mélange de canaux.** Le niveau bloc est vulnérable aux attaques par puzzle (voir arxiv:2308.02227, arxiv:2211.02369).

### Transformations de valeurs {#value-transformations}

**Affine (y = w*x + b) :** seulement 2 paramètres par canal. Cassée avec 2 paires connues. Trop faible comme défense principale.

**LUT par canal (8 bits) :** 256! ≈ 10^507 tables possibles. Cassée avec 1 paire connue (brouillée, originale) si elle est indépendante de la position. La renforcer avec une LUT dépendant de la position (PDLUT) : `out[i] = LUT[x,y][in[i]]`.

**Polynomiale (dérivée de la clé de session) :**
```sql
y = a0 + a1*x + a2*x^2 + ... + an*x^n  (n=4-8)
Coefficients derived from session_key via HKDF
```
Nécessite n+1 paires connues pour être cassée, mais les coefficients changent à chaque session.

**Matrice de couleur dépendant de la clé :**
```text
[R', G', B'] = M(key) × [R, G, B]
```
M est dérivée de session_key via HMAC/KDF. Linéaire, donc vulnérable à l'analyse statistique.

### Pile multicouche recommandée {#recommended-multi-layer-stack}

```bash
Input tensor (HWC, float32)
  ↓
[1] Channel permutation on intermediate channels (64ch)
  ↓
[2] Custom conv layer (scrambled weights from session_key)
  ↓
[3] Pixel-level spatial permutation (seed = HMAC(session_key, "spatial"))
  ↓
[4] Position-dependent polynomial transform (coefficients from session_key)
  ↓
[5] XOR with key-derived pseudorandom stream (AES-CTR)
  ↓
Scrambled output (HWC, float32)
```

L'attaquant doit casser TOUTES les couches, dans le bon ordre.

---

## Formule dépendant de la clé de session {#session-key-dependent-formula}

### Inversion paramétrée (RECOMMANDÉE) {#parameterized-inversion-recommended}

```text
session_key → HKDF-SHA256 → scramble parameters:
  - spatial_permutation_seed  (32 bytes)
  - channel_permutation_seed  (32 bytes)
  - polynomial_coefficients   (N * float64)
  - xor_stream_key            (32 bytes)
  - affine_scale              (per channel)
  - affine_offset             (per channel)
```

Le serveur émet `session_key` lors de l'authentification (échange de clés ECDH). La clé tourne toutes les 1 h à 1 j. Le convertisseur dérive les mêmes paramètres et calcule l'inverse.

Sécurité : même si l'attaquant extrait le binaire du convertisseur, sans session_key la formule est inutilisable. Une compromission n'expose qu'une seule session.

### Flux XOR (CSPRNG AES-CTR) {#xor-stream-aes-ctr-csprng}

```cpp
void generate_scramble_stream(const uint8_t* session_key, size_t key_len,
                              float* stream, size_t num_pixels) {
    AES_CTR_Context ctx;
    aes_ctr_init(&ctx, session_key, initial_counter);
    for (size_t i = 0; i < num_pixels * 3; i++) {
        uint32_t rand_bits;
        aes_ctr_next(&ctx, &rand_bits, 4);
        stream[i] = (float)(rand_bits) / UINT32_MAX * 2.0f - 1.0f;
    }
}
// Scramble: output[i] = clamp(model_output[i] + stream[i] * strength)
// Unscramble: original[i] = output[i] - stream[i] * strength
```

Un flux purement additif est faible à lui seul : il s'inverse trivialement avec une paire connue. À utiliser uniquement comme couche 5 par-dessus un brouillage non linéaire.

---

## Obfuscation du binaire du convertisseur {#converter-binary-obfuscation}

Le convertisseur est la cible d'attaque critique. S'il est compromis, tout le schéma l'est.

### Obfuscation LLVM (référence : obligatoire) {#llvm-obfuscation-baseline-required}

Outils : Obfuscator-LLVM (o-LLVM), Hikari (fork d'o-LLVM), solutions commerciales : IRDETO Cloakware, Arxan, Promon.

Techniques :
1. **Aplatissement du flot de contrôle (CFF)** : tous les blocs de base dans un switch unique dans une boucle ; une variable d'état contrôle l'ordre
2. **Flot de contrôle factice** : fausses branches avec des prédicats opaques (toujours vrais ou faux, difficiles à analyser statiquement)
3. **Substitution d'instructions** : `a+b` → `a-(-b)`, `x^y` → `(x&~y)|(~x&y)`
4. **Chiffrement des chaînes** : déchiffrement des chaînes à l'exécution
5. **Encodage des constantes** : remplacement des constantes numériques par des équivalents calculés

Face à cela : SATURN (désobfuscation de l'IR LLVM), Triton (exécution symbolique). L'aplatissement du flot de contrôle n'est pas une solution miracle.

### Protection par machine virtuelle (pour les fonctions critiques) {#vm-protection-for-critical-functions}

VMProtect / Themida : la fonction critique est compilée en bytecode propriétaire, interprété par un interpréteur sur mesure. L'attaquant ne voit que l'interpréteur et un blob de bytecode. État actuel (2025-2026) : aucun dévirtualiseur public universel pour les versions récentes de VMProtect. Il faut plusieurs semaines à plusieurs mois à un ingénieur inverse qualifié.

**Pile recommandée :**
```text
Required (baseline):
├── LLVM obfuscation (CFF + bogus flow + string encryption)
├── Anti-debug checks (IsDebuggerPresent, ptrace, timing)
├── Integrity checks (code signing + self-checksumming)
└── Stripped symbols

Recommended (serious protection):
├── VMProtect for inverse-scramble function
├── White-box crypto for key derivation
└── Junk/dead code injection

Optional (maximum):
├── NN as one unscramble layer
├── Split into 2 processes (GPU unscramble + CPU finalize)
└── Custom VM for key management
```

**Réalité de la cryptographie en boîte blanche :** l'AES en boîte blanche a été cassé à plusieurs reprises dans la recherche académique (DCA : Differential Computation Analysis). Les implémentations commerciales de boîte blanche tiennent mieux grâce à la sécurité par l'obscurité. Utile comme **une couche**, pas comme défense unique.

### Séparation en processus {#process-split}

```text
Process A: inverse_step_1(scrambled) → intermediate_1
Process B: inverse_step_2(intermediate_1) → normal_image
```

Deux processus maximum : la surcharge et la complexité de l'IPC croissent très vite.

---

## Sécurité de l'IPC (moteur → convertisseur) {#ipc-security-engine-converter}

### Mémoire partagée + chiffrement (RECOMMANDÉ) {#shared-memory-encryption-recommended}

```cpp
// Windows: random GUID segment name
std::wstring segName = L"Global\\" + generate_uuid();
HANDLE hMap = CreateFileMappingW(INVALID_HANDLE_VALUE, NULL,
    PAGE_READWRITE, 0, tensor_size, segName.c_str());
void* ptr = MapViewOfFile(hMap, FILE_MAP_ALL_ACCESS, 0, 0, tensor_size);
VirtualLock(ptr, tensor_size); // prevent swap to disk

// macOS/Linux: anonymous, unlinked immediately
int fd = shm_open("/tensor_temp", O_CREAT | O_RDWR, 0600);
ftruncate(fd, tensor_size);
void* ptr = mmap(NULL, tensor_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
shm_unlink("/tensor_temp"); // name removed, segment lives while fd open
```

Chiffrer les données en mémoire partagée avec ChaCha20-Poly1305 (environ 0,3 ms pour 12 Mo sur un CPU moderne avec SIMD). Noms de segments aléatoires par session.

**Tubes nommés :** environ 5 à 15 ms pour 12 Mo, trop lent. Un débogueur sur le convertisseur voit toujours les données déchiffrées.
**DLL dans le processus :** le plus faible. Un débogueur sur le processus principal voit tout.

---

## Benchmarks de performance {#performance-benchmarks}

**CPU (Intel i5-10400, 6 cœurs, 2,9 GHz) :**

| Opération | 1024×1024 | 2048×2048 | Parallélisable |
|-----------|-----------|-----------|----------------|
| Permutation de canaux (3 canaux) | ~0,01 ms | ~0,04 ms | Trivialement (memcpy) |
| Permutation de canaux (64 canaux) | ~0,05 ms | ~0,2 ms | Par canal |
| Permutation spatiale de pixels | ~0,5 ms | ~2 ms | Par ligne |
| Transformation affine (par pixel) | ~0,1 ms | ~0,4 ms | SIMD AVX2 |
| Polynomiale (degré 4) | ~0,3 ms | ~1,2 ms | SIMD AVX2 |
| LUT par canal | ~0,2 ms | ~0,8 ms | Favorable au cache |
| Flux XOR (AES-CTR) | ~0,3 ms | ~1,2 ms | AES-NI |
| **Brouillage multicouche complet** | **~2-3 ms** | **~8-12 ms** | |

**GPU (CUDA) :**

| Opération | 1024×1024 | 2048×2048 |
|-----------|-----------|-----------|
| Brouillage complet | ~0,1-0,3 ms | ~0,3-0,8 ms |
| + copie GPU→CPU | ~0,5 ms | ~2 ms |

Surcoût total : environ 3 à 5 ms pour du 1024×1024 typique. Face à une inférence de 50 à 200 ms, cela représente moins de 5 %.

---

## Attaques connues {#known-attacks}

### Résolution de puzzle (jigsaw) {#jigsaw-puzzle-solving}
Le brouillage par blocs équivaut à un puzzle. Les algorithmes exploitent les statistiques des bords de blocs.
- Blocs 16×16 : 70 à 90 % de l'ordre retrouvé avec suffisamment de blocs
- Blocs 8×8 : 40 à 60 %
- **Niveau pixel : immunisé** (pas de bords de blocs)

### Attaque à texte clair connu (KPA) : la plus dangereuse {#known-plaintext-attack-kpa-most-dangerous}
L'attaquant obtient une paire (sortie_brouillée, image_originale).

Résultats de recherche :
- Tous les chiffrements par permutation seule ont été cassés à partir de O(log2(N)) paires (arxiv, 2017)
- Permutation de pixels 1024×1024 : environ 20 paires pour une récupération complète
- Transformation affine : 2 paires par canal
- LUT (indépendante de la position) : 1 paire

**Critique : si session_key ne change pas entre deux exécutions**, une seule paire interceptée peut suffire à une cassure complète.

### Analyse statistique {#statistical-analysis}
- La permutation de canaux préserve l'histogramme de chaque canal
- La permutation spatiale préserve l'histogramme global
- **Défense :** une transformation non linéaire des valeurs (LUT/polynôme) modifie l'histogramme

---

## Sel par image (obligatoire) {#per-image-salt-mandatory}

L'attaque à texte clair connu avec environ 20 paires brise le brouillage par permutation seule. Contre-mesure : un sel par image introduit une aléa unique dans chaque opération de brouillage.

```cpp
// Per-image salt derivation
uint8_t image_salt[16];
crypto_random_bytes(image_salt, 16); // unique per image
// embed in output (first 16 bytes of scrambled tensor, or separate channel)

// Scramble key for this image
uint8_t image_key[32];
crypto_kdf_hkdf_sha256_expand(image_key, 32,
    "image-scramble", 14,
    session_key_derived_prk); // XOR image_salt into derivation
// feed image_key into spatial permutation seed, polynomial coefficients, etc.
```

Effet : chaque image obtient une permutation ou une transformation différente, même avec la même session_key. Les 20 paires (brouillée, originale) issues d'images différentes donnent 20 instances de brouillage distinctes, donc aucune clé commune à extraire.

**Où placer le sel :** préfixer le tenseur brouillé par un nonce de 16 octets, ou le stocker dans un canal supplémentaire dédié. Le convertisseur lit le sel avant d'inverser le brouillage.

## Brouillage dans l'espace latent (modèles basés sur VAE) {#latent-space-scrambling-vae-based-models}

Pour les architectures basées sur un VAE (Stable Diffusion, etc.) : brouiller dans l'espace latent plutôt que dans l'espace des pixels.

**Avantages :**
- Tenseur latent : typiquement 4 canaux × H/8 × W/8 (beaucoup plus petit que la sortie en pixels)
- Environ 64 canaux latents (sortie de l'encodeur) : 64! ≈ 10^89 permutations disponibles
- Pas de statistiques spatiales naturelles dans l'espace latent : les attaques statistiques sont affaiblies
- Surcoût de brouillage et de débrouillage : environ 0,05 ms (tenseur minuscule)

**Implémentation :** ajouter un opérateur ONNX personnalisé après la sortie de l'encodeur VAE, avant le décodeur.

## Sécurité de l'IPC : moteur → convertisseur {#ipc-security-engine-converter_1}

Mémoire partagée chiffrée (recommandée) :

```cpp
// Windows: random GUID name per session
std::wstring seg_name = L"Global\\" + generate_uuid();
HANDLE hMap = CreateFileMappingW(INVALID_HANDLE_VALUE, NULL,
    PAGE_READWRITE, 0, tensor_size, seg_name.c_str());
void* ptr = MapViewOfFile(hMap, FILE_MAP_ALL_ACCESS, 0, 0, tensor_size);
VirtualLock(ptr, tensor_size); // prevent swap to disk

// macOS: anonymous, unlinked immediately
int fd = shm_open("/t", O_CREAT | O_RDWR, 0600);
void* ptr = mmap(NULL, tensor_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
shm_unlink("/t"); // name removed, segment lives while fd open
```

Chiffrer les données en mémoire partagée : ChaCha20-Poly1305 environ 0,3 ms pour 12 Mo sur un CPU moderne avec SIMD. Noms de segments aléatoires par session. Tubes nommés : environ 5 à 15 ms pour 12 Mo, trop lent.

## Pièges {#gotchas}

- **Un brouillage par permutation seule se brise avec 20 paires à texte clair connu**, quelle que soit la taille de la permutation. Toujours le combiner avec une transformation des valeurs.
- **Le sel par image est obligatoire.** Sans lui, 20 paires (brouillée, originale) brisent la clé de session partagée. Un sel par image rend chaque instance indépendante.
- **La clé de session doit changer à chaque session**, et non par utilisateur ni par jour. Une session = une clé. Clé compromise = une seule session exposée, pas toutes.
- **Le flux AES-CTR seul est trivialement inversible** dès que l'attaquant dispose d'une paire (brouillée, originale). À utiliser uniquement comme couche finale après les transformations non linéaires.
- **Le brouillage GPU dans un opérateur ONNX personnalisé** exige que l'opérateur soit enregistré avant la création de la session. Si la session a déjà été créée sans l'opérateur, il faut la recréer.
- **Le brouillage au niveau bloc est inutile contre le piratage** : les solveurs de puzzle modernes (2022-2023) retrouvent plus de 70 % du contenu à partir de blocs 16x16. Utiliser uniquement le niveau pixel.
- **Les têtes de brouillage apprises (NN)** sont théoriquement élégantes, mais avec pertes (erreurs d'environ 0,1 à 0,5 LSB) et vulnérables à l'approximation si l'attaquant dispose de suffisamment de paires avec clés connues.
- **VMProtect ralentit fortement la fonction protégée** : surcoût de 10 à 50 fois. Profiler avant de protéger les chemins chauds.
- **3 canaux RGB = 6 permutations = testées par force brute en quelques microsecondes.** Le brouillage doit intervenir AVANT la dernière couche convolutive, là où existent 64 canaux intermédiaires ou plus.
- **Processus convertisseur avec VirtualLock** : empêche le tenseur brouillé d'être déplacé vers le fichier d'échange sur disque. Sans cela, la mise en veille prolongée ou la veille peut faire fuir le tenseur vers pagefile.sys.

## Voir aussi {#see-also}
- [[hkdf-personalized-weights]]
- [[watermarking-encrypted-models]]
- [[remote-kill-switch]]
- [[licensing-implementation-cpp]]
