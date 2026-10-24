---
level: 4
source_sha256: 69f916eb4c022cbedfc7931c035d5fd911dbe4959a63a967c5b94b93a75e9430
translation: machine
translated_at: '2026-10-24'
---
# Neural-Network-Output-Scrambling: Anti-Piracy für Inference-Engines {#neural-network-output-scrambling-anti-piracy-for-inference-engines}

Datum: 2026-04-03
Kontext: Desktop-C++-Anwendung mit ONNX-Inferenz. Das Modell gibt einen verwürfelten Tensor aus. Ein separater, obfuskierter Konverter-Prozess wendet eine geheime, aus dem Session-Key abgeleitete Formel an und erzeugt daraus ein normales Bild.

---

## Trainingsansatz {#training-approach}

### Ansatz A: Scrambling in das Training einbetten {#approach-a-bake-scramble-into-training}

Loss = MSE(model_output, scramble(ground_truth)). Das Modell lernt, eine verwürfelte Darstellung vorherzusagen.

**Vorteile:** Das normale Bild existiert nie im GPU-Speicher (nicht einmal transient).
**Nachteile:** Erfordert Neutraining. Die Scramble-Funktion muss differenzierbar sein:
- Kanal- und räumliche Permutation: differenzierbar (Index-Umordnung)
- XOR mit Schlüssel: NICHT direkt differenzierbar (Straight-Through-Estimator verwenden)
- LUTs: NICHT differenzierbar
- Qualitätsverlust von 1–3 % PSNR bei nichtlinearem Scrambling

### Ansatz B: Nachverarbeitung (ohne Neutraining) – EMPFOHLEN {#approach-b-post-processing-no-retraining-recommended}

Normales Training. Scrambling wird als ONNX-Custom-Operator hinzugefügt (letzter Knoten im Graph). Das Scrambling läuft auf der GPU, die Ausgabe ist bereits verwürfelt, wenn sie auf die CPU kopiert wird.

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

Scramble-Knoten per ONNX Graph Surgery in das bestehende exportierte Modell einfügen (kein Neutraining erforderlich).
Performance-Overhead: ~0.1–0.5ms zusätzlicher CUDA-Kernel. Vernachlässigbar gegenüber 50–200ms Inferenz.

---

## Scrambling-Techniken {#scrambling-techniques}

### Kanal-Permutation {#channel-permutation}

Für RGB (3 Kanäle) gibt es nur 3! = 6 Permutationen. Diese sind per Brute-Force in Mikrosekunden lösbar.

**Lösung:** Zwischenkanäle permutieren (64 Kanäle in der vorletzten Schicht). 64! ~ 10^89 Varianten. Umsetzung durch Permutation der Zeilen/Spalten der Gewichtsmatrix der letzten Conv-Schicht. Keine Modelländerungen nötig.

### Räumliches Scrambling {#spatial-scrambling}

| Level | Suchraum | Jigsaw-Angriffsresistenz | Overhead |
|-------|-------------|--------------------------|---------|
| Block-Level (16x16) | (64×64)! ~ 10^9000+ | **Gering** – Jigsaw-Solver rekonstruiert über Abgleich der Blockgrenzen | Minimal |
| Pixel-Level | (1024×1024)! | **Mittel** – Histogramm innerhalb der Kanäle bleibt erhalten | Mittel |
| Pixel-Level + Kanalmischung | Astronomisch | **Hoch** – zerstört räumliche UND Farbkorrelationen | Mittel |
| DCT-Domäne | Implementierungsabhängig | **Hoch** – zerstört räumliche Kohärenz | Erheblich |

**Empfehlung: Pixel-Level-Permutation + Kanalmischung.** Block-Level ist anfällig für Jigsaw-Angriffe (siehe arxiv:2308.02227, arxiv:2211.02369).

### Wertetransformationen {#value-transformations}

**Affin (y = w*x + b):** Nur 2 Parameter pro Kanal. Mit 2 bekannten Paaren gebrochen. Als primäre Verteidigung zu schwach.

**LUT pro Kanal (8-bit):** 256! ~ 10^507 mögliche Tabellen. Mit 1 bekanntem (verwürfelt, original)-Paar gebrochen, falls positionsunabhängig. Stärken durch eine positionsabhängige LUT (PDLUT): `out[i] = LUT[x,y][in[i]]`.

**Polynom (aus Session-Key abgeleitet):**
```sql
y = a0 + a1*x + a2*x^2 + ... + an*x^n  (n=4-8)
Coefficients derived from session_key via HKDF
```
Benötigt n+1 bekannte Paare zum Brechen, aber die Koeffizienten rotieren mit der Session.

**Schlüsselabhängige Farbmatrix:**
```text
[R', G', B'] = M(key) × [R, G, B]
```
M wird aus `session_key` über HMAC/KDF abgeleitet. Linear, daher anfällig für statistische Analyse.

### Empfohlener mehrschichtiger Stack {#recommended-multi-layer-stack}

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

Der Angreifer muss ALLE Schichten in der richtigen Reihenfolge brechen.

---

## Session-Key-abhängige Formel {#session-key-dependent-formula}

### Parametrisierte Inversion (EMPFOHLEN) {#parameterized-inversion-recommended}

```text
session_key → HKDF-SHA256 → scramble parameters:
  - spatial_permutation_seed  (32 bytes)
  - channel_permutation_seed  (32 bytes)
  - polynomial_coefficients   (N * float64)
  - xor_stream_key            (32 bytes)
  - affine_scale              (per channel)
  - affine_offset             (per channel)
```

Der Server stellt `session_key` bei der Authentifizierung aus (ECDH-Schlüsselaustausch). Der Schlüssel rotiert alle 1h–1d. Der Konverter leitet dieselben Parameter ab und berechnet die Inverse.

Sicherheit: Selbst wenn ein Angreifer das Konverter-Binary extrahiert, ist die Formel ohne `session_key` nutzlos. Eine Kompromittierung betrifft nur eine einzelne Session.

### XOR-Stream (AES-CTR-CSPRNG) {#xor-stream-aes-ctr-csprng}

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

Ein reiner additiver Stream ist allein schwach und mit einem bekannten Paar trivial invertierbar. Nur als Schicht 5 über einem nichtlinearen Scrambling verwenden.

---

## Obfuskation des Konverter-Binaries {#converter-binary-obfuscation}

Der Konverter ist das kritische Angriffsziel. Wird er gebrochen, ist das gesamte Schema kompromittiert.

### LLVM-Obfuskation (Baseline, Pflicht) {#llvm-obfuscation-baseline-required}

Werkzeuge: Obfuscator-LLVM (o-LLVM), Hikari (o-LLVM-Fork). Kommerziell: IRDETO Cloakware, Arxan, Promon.

Techniken:
1. **Control Flow Flattening (CFF)**: Alle Basisblöcke liegen in einem `switch` innerhalb einer Schleife. Eine Zustandsvariable steuert die Reihenfolge.
2. **Bogus Control Flow**: Gefälschte Verzweigungen mit opaquen Prädikaten (immer wahr bzw. falsch, statisch schwer zu analysieren)
3. **Instruction Substitution**: `a+b` → `a-(-b)`, `x^y` → `(x&~y)|(~x&y)`
4. **String-Verschlüsselung**: Strings zur Laufzeit entschlüsseln
5. **Konstanten-Kodierung**: Numerische Konstanten durch berechnete Äquivalente ersetzen

Dagegen helfen: SATURN (LLVM-IR-Deobfuskation), Triton (symbolische Ausführung). CFF ist kein Allheilmittel.

### VM-Schutz (für kritische Funktionen) {#vm-protection-for-critical-functions}

VMProtect / Themida: Die kritische Funktion wird in einen eigenen Bytecode für einen eigenen Interpreter kompiliert. Der Angreifer sieht nur Interpreter und Bytecode-Blob. Aktueller Stand (2025–2026): Es gibt keinen öffentlich verfügbaren universellen Devirtualisierer für aktuelles VMProtect. Für einen qualifizierten Reverser dauert es Wochen bis Monate.

**Empfohlener Stack:**
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

**Realität von White-Box-Kryptografie:** White-Box-AES wurde akademisch mehrfach gebrochen (DCA – Differential Computation Analysis). Kommerzielle WBC-Implementierungen halten besser, vor allem durch Security-through-Obscurity. Nützlich als **eine Schicht**, nicht als alleinige Verteidigung.

### Prozesstrennung {#process-split}

```text
Process A: inverse_step_1(scrambled) → intermediate_1
Process B: inverse_step_2(intermediate_1) → normal_image
```

Maximal 2 Prozesse, da IPC-Overhead und Komplexität schnell wachsen.

---

## IPC-Sicherheit (Engine → Konverter) {#ipc-security-engine-converter}

### Shared Memory + Verschlüsselung (EMPFOHLEN) {#shared-memory-encryption-recommended}

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

Daten im Shared Memory mit ChaCha20-Poly1305 verschlüsseln (~0.3ms für 12MB auf moderner CPU mit SIMD). Zufällige Segmentnamen pro Session.

**Named Pipes:** ~5–15ms für 12MB, zu langsam. Ein Debugger am Konverter sieht weiterhin die entschlüsselten Daten.
**In-Process-DLL:** am schwächsten. Ein Debugger am Hauptprozess sieht alles.

---

## Performance-Benchmarks {#performance-benchmarks}

**CPU (Intel i5-10400, 6-Core, 2.9 GHz):**

| Operation | 1024×1024 | 2048×2048 | Parallelisierbar |
|-----------|-----------|-----------|----------------|
| Kanal-Permutation (3 Kanäle) | ~0.01ms | ~0.04ms | Trivial (memcpy) |
| Kanal-Permutation (64 Kanäle) | ~0.05ms | ~0.2ms | Pro Kanal |
| Räumliche Pixel-Permutation | ~0.5ms | ~2ms | Pro Zeile |
| Affine Transformation (pro Pixel) | ~0.1ms | ~0.4ms | SIMD AVX2 |
| Polynom (Grad 4) | ~0.3ms | ~1.2ms | SIMD AVX2 |
| LUT pro Kanal | ~0.2ms | ~0.8ms | Cache-freundlich |
| XOR-Schlüsselstrom (AES-CTR) | ~0.3ms | ~1.2ms | AES-NI |
| **Vollständiges mehrschichtiges Scrambling** | **~2–3ms** | **~8–12ms** | |

**GPU (CUDA):**

| Operation | 1024×1024 | 2048×2048 |
|-----------|-----------|-----------|
| Vollständiges Scrambling | ~0.1–0.3ms | ~0.3–0.8ms |
| + GPU→CPU-Kopie | ~0.5ms | ~2ms |

Gesamt-Overhead: ~3–5ms für typisches 1024×1024. Gegenüber 50–200ms Inferenz entspricht das <5 %.

---

## Bekannte Angriffe {#known-attacks}

### Jigsaw-Puzzle-Lösung {#jigsaw-puzzle-solving}
Block-Level-Scrambling ist ein Jigsaw-Puzzle. Algorithmen nutzen Statistiken der Blockgrenzen aus.
- 16×16-Blöcke: 70–90 % Reihenfolgerekonstruktion bei ausreichend Blöcken
- 8×8-Blöcke: 40–60 %
- **Pixel-Level: immun** (keine Blockgrenzen)

### Known-Plaintext-Angriff (KPA): am gefährlichsten {#known-plaintext-attack-kpa-most-dangerous}
Der Angreifer erhält ein Paar (scrambled_output, Originalbild).

Forschungsergebnisse:
- Alle reinen Permutations-Chiffren sind ab O(log2(N)) Paaren gebrochen (arxiv, 2017)
- Pixel-Permutation 1024×1024: ~20 Paare für vollständige Rekonstruktion
- Affine Transformation: 2 Paare pro Kanal
- LUT (positionsunabhängig): 1 Paar

**Kritisch: Wenn `session_key` zwischen Läufen nicht rotiert**, kann ein abgefangenes Paar für einen vollständigen Bruch genügen.

### Statistische Analyse {#statistical-analysis}
- Kanal-Permutation erhält das Histogramm pro Kanal
- Räumliche Permutation erhält das globale Histogramm
- **Verteidigung:** Nichtlineare Wertetransformation (LUT/Polynom) verändert das Histogramm

---

## Per-Image-Salt (Pflicht) {#per-image-salt-mandatory}

Ein Known-Plaintext-Angriff mit ~20 Paaren bricht reines Permutations-Scrambling. Gegenmaßnahme: Ein Per-Image-Salt mischt in jede Scrambling-Operation eine eindeutige Zufallskomponente ein.

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

Wirkung: Jedes Bild erhält eine andere Permutation bzw. Transformation, auch bei gleichem `session_key`. 20 (scrambled, original)-Paare aus verschiedenen Bildern ergeben 20 verschiedene Scrambling-Instanzen, also keinen gemeinsamen Schlüssel, der extrahiert werden könnte.

**Wo der Salt eingebettet wird:** 16-Byte-Nonce dem verwürfelten Tensor voranstellen oder in einem eigenen Zusatzkanal speichern. Der Konverter liest den Salt, bevor er invertiert.

## Latent-Space-Scrambling (VAE-basierte Modelle) {#latent-space-scrambling-vae-based-models}

Für VAE-basierte Architekturen (Stable Diffusion etc.): Scrambling im latenten Raum statt im Pixelraum.

**Vorteile:**
- Latenter Tensor: typischerweise 4 Kanäle × H/8 × W/8 (deutlich kleiner als die Pixelausgabe)
- ~64 latente Kanäle (Encoder-Ausgabe): 64! ~ 10^89 Permutationen verfügbar
- Kein natürliches räumliches Statistikprofil im latenten Raum, daher statistische Angriffe geschwächt
- Scramble-/Unscramble-Overhead: ~0.05ms (winziger Tensor)

**Umsetzung:** Custom-ONNX-Op nach der VAE-Encoder-Ausgabe und vor dem Decoder hinzufügen.

## IPC-Sicherheit: Engine → Konverter {#ipc-security-engine-converter_1}

Verschlüsseltes Shared Memory (empfohlen):

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

Daten im Shared Memory verschlüsseln: ChaCha20-Poly1305 ~0.3ms für 12MB auf moderner CPU mit SIMD. Zufällige Segmentnamen pro Session. Named Pipes: ~5–15ms für 12MB, zu langsam.

---

## Gotchas {#gotchas}

- **Reines Permutations-Scrambling bricht mit 20 Known-Plaintext-Paaren**, unabhängig von der Permutationsgröße. Immer mit einer Wertetransformation kombinieren.
- **Per-Image-Salt ist Pflicht.** Ohne ihn brechen 20 (scrambled, original)-Paare den gemeinsamen Session-Key. Ein Salt pro Bild macht jede Instanz unabhängig.
- **Der Session-Key muss pro Session rotieren**, nicht pro Benutzer und nicht pro Tag. Eine Session entspricht einem Schlüssel. Ein kompromittierter Schlüssel legt nur eine Session offen, nicht alle.
- **Der AES-CTR-Strom allein ist trivial invertierbar**, sobald der Angreifer ein (scrambled, original)-Paar hat. Nur als letzte Schicht nach nichtlinearen Transformationen verwenden.
- **GPU-Scrambling als ONNX-Custom-Op** erfordert, dass der Op vor der Session-Erstellung registriert wird. Wurde die Session bereits ohne den Custom-Op erstellt, muss sie neu erstellt werden.
- **Block-Level-Scrambling ist für Anti-Piracy nutzlos.** Moderne Jigsaw-Solver (2022–2023) rekonstruieren 70 %+ der Inhalte aus 16×16-Blöcken. Nur Pixel-Level verwenden.
- **Gelernte Scrambling-Heads (NN)** sind theoretisch elegant, aber verlustbehaftet (~0.1–0.5 LSB-Fehler) und anfällig für Approximation, wenn der Angreifer genügend Paare mit bekannten Schlüsseln hat.
- **VMProtect verlangsamt die geschützte Funktion deutlich**, mit 10–50-fachem Overhead. Hot Paths vor dem Schutz profilieren.
- **3 RGB-Kanäle = 6 Permutationen = in Mikrosekunden per Brute-Force.** Das Scrambling muss VOR der letzten Conv-Schicht erfolgen, wo 64+ Zwischenkanäle existieren.
- **Konverter-Prozess mit VirtualLock** verhindert, dass der verwürfelte Tensor auf die Auslagerungsdatei geschrieben wird. Ohne dies können Ruhezustand bzw. Sleep den Tensor nach pagefile.sys leaken.

## Siehe auch {#see-also}
- [[hkdf-personalized-weights]]
- [[watermarking-encrypted-models]]
- [[remote-kill-switch]]
- [[licensing-implementation-cpp]]
