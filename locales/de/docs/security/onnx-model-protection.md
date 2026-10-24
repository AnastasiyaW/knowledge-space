---
level: 4
source_sha256: f916fd89855d6cdb2fff95f70331c704b1f688267ad353e9401da63916c8a3af
translation: machine
translated_at: '2026-10-24'
---
# ONNX-Modellschutz: verschlüsseltes Laden und Architekturverschleierung {#onnx-model-protection-encrypted-loading-and-architecture-obfuscation}

Datum: 2026-04-03
Kontext: Desktop-C++-App (Mac + Windows), ONNX-Runtime-Inferenz, Schutz der Modellgewichte vor Extraktion.

---

## Verschlüsseltes Laden über CreateSessionFromArray {#encrypted-loading-via-createsessionfromarray}

Microsoft plant laut Issue #3556 offiziell keine integrierte Verschlüsselungsunterstützung in ONNX Runtime. Die Verschlüsselung liegt in der Verantwortung des Entwicklers; ONNX Runtime stellt die API zum Laden aus dem Speicher bereit.

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

### Speicheroptimierung für große Modelle {#memory-optimization-for-large-models}

`CreateSessionFromArray` verdoppelt den Speicherbedarf: Puffer + geparstes Modell. Bei einem 500-MB-Modell sind während der Initialisierung ca. 1 GB RAM nötig (Issue #23775).

Optionen:
```cpp
// Use model bytes directly (no copy), buffer must stay alive for session lifetime
session_options.AddConfigEntry("session.use_ort_model_bytes_directly", "1");
// Initializers (weights) read from buffer directly
session_options.AddConfigEntry("session.use_ort_model_bytes_for_initializers", "1");
```

Beide Flags bringen die maximale Speicherersparnis für Modelle im `.ort`-Format. Bei Modellen im Standardformat `.onnx` ist der Vorteil nur teilweise.

**Blockweise Entschlüsselung für große Modelle (>1 GB):**
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

DirectML wurde 2025 in den Wartungsmodus versetzt. Microsoft empfiehlt **Windows ML (WinML)**, eine Abstraktionsschicht über ONNX Runtime, die den Execution Provider automatisch auswählt:
- NVIDIA RTX → TensorRT EP
- AMD-GPU → DirectML EP
- Intel-GPU/NPU → DirectML- oder Intel-EP
- Qualcomm-NPU → QNN EP
- Fallback → XNNPACK EP

```cpp
// Force DirectML EP
Ort::SessionOptions opts;
OrtSessionOptionsAppendExecutionProvider_DML(opts, 0); // device_id = 0

// Memory limits for weak GPUs
opts.SetGraphOptimizationLevel(ORT_ENABLE_ALL);
opts.SetExecutionMode(ORT_SEQUENTIAL); // less memory vs parallel
```

**GPU-Speicher auf schwacher Hardware:**

| GPU | VRAM | UNet ~100 MB | 1024×1024 FPS |
|-----|------|-------------|---------------|
| Intel UHD 630 | geteilt, 2-4 GB | möglich | 0,5-2 |
| Intel Iris Xe | geteilt, 4-8 GB | OK | 2-5 |
| NVIDIA GTX 1650 | 4 GB | OK | 5-15 |
| Intel Arc A380 | 6 GB | OK | 8-20 |

Ein ONNX-Modell mit 1,77 GB in FP16 benötigt beim Laden ca. 2,5 GB VRAM und beim ersten Inferenzlauf wegen der Zwischenpuffer bis zu 5 GB Spitzenbedarf. Auf einer GPU mit 2 GB VRAM liegt die sichere Obergrenze der Modellgröße bei etwa 300 MB.

**Fallback bei erschöpftem VRAM:** DirectML nutzt dann den gemeinsam genutzten Systemspeicher, was zu einer 10- bis 100-fachen Verlangsamung führt. Den tatsächlichen Speicherverbrauch prüfen, nicht nur die Größe der Modelldatei.

---

## CoreML-Verschlüsselung (macOS) {#coreml-encryption-macos}

Apple bietet eine native Verschlüsselung für CoreML-Modelle mit Integration der Secure Enclave.

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

**Integration der Secure Enclave:** Der Verschlüsselungsschlüssel verlässt die SE nie. Die Entschlüsselung findet im Chip statt. Der Schlüssel ist gerätegebunden (nicht exportierbar).

**Schutzstärke:**
- Apple Silicon, SIP aktiviert, kein Jailbreak: **sehr stark**
- Intel-Mac ohne SIP: **mittel** (Speicherabbild möglich)
- Ohne SE (Hackintosh, VM): Schlüssel im Software-Keychain → **schwach**

**Bekannte Umgehung:** `.mlmodelc` enthält `model.espresso.weights`. Wenn diese Datei entschlüsselt ist, lässt sie sich leicht parsen. Auf einem gejailbreakten Gerät lässt sich das Modell nach der Entschlüsselung im RAM abfangen.

---

## CoreML vs. ONNX Runtime: Performance (Mac) {#coreml-vs-onnx-runtime-performance-mac}

| Modell | CoreML (ANE) | CoreML (Metal) | ONNX CPU | ONNX+CoreML EP |
|-------|-------------|----------------|----------|----------------|
| MobileNetV2 (M1) | ~1,5 ms | ~5 ms | ~15 ms | ~6 ms |
| UNet 1024×1024 (M2) | ~30 ms | ~80 ms | ~300 ms | ~90 ms |
| ViT-Base (M3) | ~4 ms | ~12 ms | ~40 ms | ~15 ms |

Die Apple Neural Engine ist bei kompatiblen Modellen 3- bis 5-mal schneller als Metal.

**Wann welche Variante:**
- CoreML nativ: wenn ANE benötigt wird, Verschlüsselung nötig ist, statische Shapes vorliegen und nur Apple-Plattformen unterstützt werden müssen
- ONNX+CoreML EP: bei plattformübergreifendem Code, dynamischen Shapes oder komplexen Operatoren, die CoreML nicht unterstützt

---

## Architekturverschleierung über Custom Ops {#architecture-obfuscation-via-custom-ops}

Standardoperatoren (Conv, MatMul) werden durch Custom Ops mit sinnlosen Namen ersetzt. Netron und onnx-inspector können die reale Architektur dann nicht mehr bestimmen.

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

**Grenzen dieses Ansatzes:**
- Gewichte (Initializer) liegen weiterhin in Protobuf und sind auch dann extrahierbar, wenn die Op-Namen verborgen sind
- Tensorformen bleiben sichtbar, die Architektur lässt sich also anhand der Größen erraten
- Custom Ops deaktivieren die Graph-Transformer-Optimierungen (Performance-Verlust)

**Wrapper-Ansatz:** eine Custom Op, die eine verschlüsselte innere Session ausführt:
```cpp
struct EncryptedModelOp {
    void Compute(OrtKernelContext* context) {
        // inner_session_ holds real model, decrypted at init
        inner_session_->Run(run_options, names, tensors, ...);
    }
    std::unique_ptr<Ort::Session> inner_session_;
};
```

Die äußere `.onnx`-Datei enthält nur eine einzige Custom Op. Das eigentliche Modell ist im Binärcode dieser Custom Op verschlüsselt.

---

## Modellexport: Minimierung von Metadaten-Lecks {#model-export-minimizing-metadata-leakage}

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

**Was nach dem Export in der ONNX-Datei verbleibt:**
- vollständiger Berechnungsgraph (Op-Namen, Verbindungen)
- alle Gewichte als Initializer (im Klartext, sofern nicht verschlüsselt)
- Tensorformen und Datentypen
- Opset-Version

`strip_doc_string=True` entfernt Python-Quellpfade, nicht aber die Architektur. Die `.onnx`-Datei muss verschlüsselt werden, um die Gewichte zu schützen; die Verschleierung der Op-Namen schützt nur die Architektur.

---

## Dual-Backend-Empfehlung (Desktop-App) {#dual-backend-recommendation-desktop-app}

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

PyTorch-Modell zur Build-Zeit in beide Formate konvertieren. CoreML-Verschlüsselung über die Apple-API, ONNX über eine eigene AES-256-GCM-Verschlüsselung.

---

## Stolperfallen {#gotchas}

- **`CreateSessionFromArray` verdoppelt den RAM.** Ein 200-MB-Modell benötigt beim Laden ca. 400 MB. Auf Rechnern mit 4 GB RAM und geteilter GPU die Speichernutzung sorgfältig planen.
- **ONNX Runtime bietet kein Streaming-Laden von Modellen.** Der vollständig entschlüsselte Puffer muss vor `CreateSessionFromArray` vollständig vorliegen. Eine Übergabe in Blöcken ist nicht möglich.
- **DirectML wurde in den Wartungsmodus versetzt.** Für neuen Code die WinML-API verwenden. Der DirectML EP funktioniert weiterhin, erhält aber keine neuen Funktionen.
- **Der CoreML EP in ONNX Runtime wandelt stillschweigend nach FP16 um.** Für präzisionskritische Modelle natives CoreML verwenden. Der ONNX+CoreML EP kann den Graphen zwischen CoreML und CPU aufteilen, was mitunter langsamer ist als reine CPU-Ausführung.
- **Custom Ops deaktivieren Graph-Optimierungen.** Liegt ein Hot Path innerhalb einer Custom Op, kann ONNX Runtime ihn nicht mit benachbarten Operatoren fusionieren. Vor dem Schützen von Hot Paths unbedingt profilieren.
- **Speicher nach der Entschlüsselung sicher löschen.** `sodium_memzero` oder `SecureZeroMemory` verwenden, da der Compiler `memset(ptr, 0, ...)` als „überflüssigen Schreibzugriff“ wegoptimieren kann.
- **Verfügbarkeit von AES-NI prüfen.** `crypto_aead_aes256gcm_is_available()` gibt auf manchen ARM-Systemen oder älteren x86-CPUs ohne AES-NI den Wert 0 zurück. In diesem Fall auf ChaCha20-Poly1305 ausweichen.

## Siehe auch {#see-also}
- [[watermarking-encrypted-models]]
- [[hkdf-personalized-weights]]
- [[output-scrambling-antipiracy]]
- [[licensing-implementation-cpp]]
