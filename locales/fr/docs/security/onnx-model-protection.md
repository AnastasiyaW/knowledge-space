---
level: 4
source_sha256: f916fd89855d6cdb2fff95f70331c704b1f688267ad353e9401da63916c8a3af
translation: machine
translated_at: '2026-10-24'
---
# Protection des modèles ONNX : chargement chiffré et obfuscation de l'architecture {#onnx-model-protection-encrypted-loading-and-architecture-obfuscation}

Date : 2026-04-03
Contexte : application C++ de bureau (Mac + Windows), inférence avec ONNX Runtime, protection des poids du modèle contre l'extraction.

---

## Chargement chiffré via CreateSessionFromArray {#encrypted-loading-via-createsessionfromarray}

Microsoft ne prévoit pas officiellement d'intégrer le chiffrement à ONNX Runtime (Issue #3556). Le chiffrement relève de la responsabilité du développeur ; ONNX Runtime fournit l'API de chargement depuis la mémoire.

```cpp
#include <onnxruntime_cxx_api.h>

std::vector<uint8_t> encrypted_data = read_file("model.onnx.enc");
std::vector<uint8_t> decrypted = decrypt_aes256_gcm(encrypted_data, key);

Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "app");
Ort::SessionOptions opts;
Ort::Session session(env, decrypted.data(), decrypted.size(), opts);

// Zero buffer immediately after session creation
sodium_memzero(decrypted.data(), decrypted.size());
```

```python
import onnxruntime as ort

with open("model.onnx.enc", "rb") as f:
    encrypted = f.read()
decrypted = decrypt_aes_gcm(encrypted, key, nonce)
session = ort.InferenceSession(decrypted)
# decrypted goes out of scope → GC (Python); explicitly zero in C++
```

### Optimisation de la mémoire pour les grands modèles {#memory-optimization-for-large-models}

`CreateSessionFromArray` double l'empreinte mémoire : tampon + modèle parsé. Pour un modèle de 500 Mo, cela représente environ 1 Go de RAM pendant l'initialisation (Issue #23775).

Options :
```cpp
// Use model bytes directly (no copy), buffer must stay alive for session lifetime
session_options.AddConfigEntry("session.use_ort_model_bytes_directly", "1");
// Initializers (weights) read from buffer directly
session_options.AddConfigEntry("session.use_ort_model_bytes_for_initializers", "1");
```

Les deux options offrent une économie de mémoire maximale pour les modèles au format `.ort`. Pour le format `.onnx` standard, le gain n'est que partiel.

**Déchiffrement par blocs pour les grands modèles (>1 Go) :**
```cpp
constexpr size_t CHUNK = 64 * 1024;
std::vector<uint8_t> out;
out.reserve(file_size);
for (size_t off = 0; off < file_size; off += CHUNK) {
    size_t chunk_sz = std::min(CHUNK, file_size - off);
    auto chunk = decrypt_chunk(mapped_ptr + off, chunk_sz, &ctx);
    out.insert(out.end(), chunk.begin(), chunk.end());
}
// ONNX Runtime does NOT support streaming model load - full buffer required
```

---

## DirectML / WinML (Windows) {#directml-winml-windows}

DirectML est passé en mode maintenance (2025). Microsoft recommande **Windows ML (WinML)**, une couche d'abstraction au-dessus d'ONNX Runtime qui sélectionne automatiquement l'execution provider :
- NVIDIA RTX → TensorRT EP
- GPU AMD → DirectML EP
- GPU/NPU Intel → DirectML ou Intel EP
- NPU Qualcomm → QNN EP
- Repli → XNNPACK EP

```cpp
// Force DirectML EP
Ort::SessionOptions opts;
OrtSessionOptionsAppendExecutionProvider_DML(opts, 0); // device_id = 0

// Memory limits for weak GPUs
opts.SetGraphOptimizationLevel(ORT_ENABLE_ALL);
opts.SetExecutionMode(ORT_SEQUENTIAL); // less memory vs parallel
```

**Réalité de la mémoire GPU sur le matériel modeste :**

| GPU | VRAM | UNet ~100 Mo | FPS en 1024×1024 |
|-----|------|--------------|------------------|
| Intel UHD 630 | Partagée 2-4 Go | Possible | 0,5-2 |
| Intel Iris Xe | Partagée 4-8 Go | OK | 2-5 |
| NVIDIA GTX 1650 | 4 Go | OK | 5-15 |
| Intel Arc A380 | 6 Go | OK | 8-20 |

Un modèle ONNX de 1,77 Go en FP16 nécessite environ 2,5 Go de VRAM au chargement, soit un pic d'environ 5 Go à la première inférence (tampons intermédiaires). Sur un GPU à 2 Go de VRAM, la taille de modèle sûre maximale est d'environ 300 Mo.

**Repli lorsque la VRAM est épuisée :** DirectML utilise alors la mémoire système partagée, ce qui entraîne un ralentissement de 10 à 100 fois. Vérifiez toujours l'utilisation réelle de la mémoire, et non uniquement la taille du fichier modèle.

---

## Chiffrement CoreML (macOS) {#coreml-encryption-macos}

Apple fournit un chiffrement natif des modèles CoreML, intégré à la Secure Enclave.

```bash
# Generate key (coremltools)
python -c "import coremltools as ct; print(ct.models.utils.generate_model_encryption_key())"
```

```swift
// Encrypt at compile time
let key = try MLModelEncryptionKey(url: keyURL)
try MLModel.compileModel(at: modelURL, configuration: config, encryptionKey: key)

// Load encrypted (CoreML handles decryption transparently)
let model = try MLModel(contentsOf: compiledModelURL, configuration: config)
```

**Intégration avec la Secure Enclave :** la clé de chiffrement ne quitte jamais la SE. Le déchiffrement s'effectue à l'intérieur de la puce. La clé est liée à l'appareil (non exportable).

**Robustesse de la protection :**
- Apple Silicon + SIP activé + pas de jailbreak : **très forte**
- Mac Intel sans SIP : **moyenne** (un vidage mémoire est possible)
- Sans SE (Hackintosh, VM) : clés dans un trousseau logiciel → **faible**

**Contournement connu :** `.mlmodelc` contient `model.espresso.weights`, qui se parse facilement une fois déchiffré. Sur un appareil jailbreaké, le modèle peut être intercepté en RAM après déchiffrement.

---

## Performances comparées CoreML et ONNX Runtime (Mac) {#coreml-vs-onnx-runtime-performance-mac}

| Modèle | CoreML (ANE) | CoreML (Metal) | ONNX CPU | ONNX + CoreML EP |
|--------|--------------|----------------|----------|------------------|
| MobileNetV2 (M1) | ~1,5 ms | ~5 ms | ~15 ms | ~6 ms |
| UNet 1024×1024 (M2) | ~30 ms | ~80 ms | ~300 ms | ~90 ms |
| ViT-Base (M3) | ~4 ms | ~12 ms | ~40 ms | ~15 ms |

Le Neural Engine d'Apple est 3 à 5 fois plus rapide que Metal pour les modèles compatibles.

**Quand utiliser chaque solution :**
- CoreML natif : besoin de l'ANE, besoin de chiffrement, formes statiques, Apple uniquement
- ONNX + CoreML EP : code multiplateforme, formes dynamiques, opérations complexes non prises en charge par CoreML

---

## Obfuscation de l'architecture via des opérations personnalisées {#architecture-obfuscation-via-custom-ops}

Remplacez les opérations standard (Conv, MatMul) par des opérations personnalisées dont les noms n'ont pas de signification. Netron et onnx-inspector ne peuvent pas déterminer l'architecture réelle.

```cpp
struct HiddenConv2dOp : Ort::CustomOpBase<HiddenConv2dOp, HiddenConv2dKernel> {
    const char* GetName() const { return "XProcessor_v3"; } // obfuscated name
    size_t GetInputTypeCount() const { return 2; }
    size_t GetOutputTypeCount() const { return 1; }
    ONNXTensorElementDataType GetInputType(size_t) const {
        return ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT;
    }
    // ...
};

Ort::CustomOpDomain domain("com.myapp.internal");
domain.Add(&hiddenConvOp);
session_options.Add(domain);
```

**Limites de cette approche :**
- Les poids (initializers) restent dans le protobuf : ils restent extractibles même si les noms d'opérations sont masqués
- Les formes des tenseurs restent visibles : l'architecture peut être devinée à partir des tailles
- Les opérations personnalisées désactivent les optimisations de transformation du graphe (perte de performance)

**Approche par enveloppe :** une opération personnalisée qui exécute une session interne chiffrée :
```cpp
struct EncryptedModelOp {
    void Compute(OrtKernelContext* context) {
        // inner_session_ holds real model, decrypted at init
        inner_session_->Run(run_options, names, tensors, ...);
    }
    std::unique_ptr<Ort::Session> inner_session_;
};
```

Le fichier `.onnx` externe ne contient qu'une seule opération personnalisée. Le modèle réel, chiffré, se trouve dans le binaire de cette opération.

---

## Export du modèle : réduire les fuites de métadonnées {#model-export-minimizing-metadata-leakage}

```python
torch.onnx.export(
    model, dummy_input, "model.onnx",
    opset_version=17,
    strip_doc_string=True,    # removes Python stack traces
    do_constant_folding=True,
    input_names=["input"],    # anonymized names
    output_names=["output"],
)
```

**Ce qui subsiste dans le fichier ONNX après l'export :**
- Le graphe de calcul complet (noms d'opérations, connexions)
- Tous les poids sous forme d'initializers (en clair, sauf s'ils sont chiffrés)
- Les formes et types de données des tenseurs
- La version de l'opset

`strip_doc_string=True` supprime les chemins des sources Python, mais pas l'architecture. Le chiffrement du fichier `.onnx` est nécessaire pour protéger les poids ; l'obfuscation des noms d'opérations ne protège que l'architecture.

---

## Recommandation à deux backends (application de bureau) {#dual-backend-recommendation-desktop-app}

```text
Mac:     CoreML native
         - Built-in encryption (Secure Enclave)
         - Apple Neural Engine performance
         - Compile: torch → coremltools → .mlpackage

Windows: ONNX Runtime + WinML
         - AES-256-GCM encrypted .onnx / .hmod
         - WinML auto-selects best EP
         - Compile: torch → torch.onnx.export → encrypt
```

Convertissez le modèle PyTorch vers les deux formats au moment de la compilation. Le chiffrement CoreML passe par l'API Apple, et celui d'ONNX par un AES-256-GCM personnalisé.

---

## Pièges courants {#gotchas}

- **`CreateSessionFromArray` double la consommation de RAM.** Un modèle de 200 Mo nécessite environ 400 Mo pendant le chargement. Sur des machines à 4 Go de RAM avec GPU partagé, planifiez soigneusement.
- **ONNX Runtime ne propose pas de chargement de modèle en flux.** Le tampon déchiffré complet doit exister avant `CreateSessionFromArray`. Il n'existe aucun moyen de le lui fournir par blocs.
- **DirectML est passé en mode maintenance.** Utilisez l'API WinML pour le nouveau code. L'EP DirectML fonctionne toujours, mais n'évolue plus.
- **Le CoreML EP d'ONNX Runtime convertit silencieusement en FP16.** Utilisez CoreML natif pour les modèles sensibles à la précision. ONNX + CoreML EP peut répartir le graphe entre CoreML et CPU, ce qui peut parfois être plus lent que le CPU seul.
- **Une opération personnalisée désactive les optimisations du graphe.** Si un chemin critique se trouve dans une opération personnalisée, ONNX Runtime ne peut pas la fusionner avec les opérations adjacentes. Profilez avant de protéger les chemins critiques.
- **Effacer les données sensibles après déchiffrement.** Utilisez `sodium_memzero` ou `SecureZeroMemory` : le compilateur peut supprimer un `memset(ptr, 0, ...)` qu'il juge « écriture inutile ».
- **Vérification de la disponibilité d'AES-NI obligatoire.** `crypto_aead_aes256gcm_is_available()` renvoie 0 sur certains processeurs ARM ou x86 anciens dépourvus d'AES-NI. Prévoyez un repli vers ChaCha20-Poly1305.

## Voir aussi {#see-also}
- [[watermarking-encrypted-models]]
- [[hkdf-personalized-weights]]
- [[output-scrambling-antipiracy]]
- [[licensing-implementation-cpp]]
