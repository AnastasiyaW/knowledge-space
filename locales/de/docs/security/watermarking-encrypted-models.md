---
level: 3
source_sha256: 480cc86eb403f957b1067273798c28c0d95bf891f7239ba0cf8d66eee50017df
translation: machine
translated_at: '2026-10-24'
---
# Watermarking neuronaler Netzausgaben + .hmod-Format für verschlüsselte Modelle {#watermarking-neural-network-outputs-hmod-encrypted-model-format}

Datum: 2026-04-03
Kontext: C++-Desktop-Retusche-App. Unsichtbares Wasserzeichen pro Ausgabebild; Modelle werden im verschlüsselten .hmod-Format gespeichert, mit AES-256-GCM pro Tensor und Ed25519-Signatur des Headers.

---

## Unsichtbares Watermarking {#invisible-watermarking}

### StegaStamp (CVPR 2020) {#stegastamp-cvpr-2020}

Quelle: Matthew Tancik et al. (UC Berkeley). Repo: https://github.com/tancik/StegaStamp

**Encoder-Architektur:**
- Eingabe: 400×400×3 RGB + 100-Bit-Nachricht
- Nachricht → FC-Schicht → 50×50×3 → Upsampling → 400×400×3
- Verkettung mit dem Bild → 400×400×4
- U-Net → Residual 400×400×3
- Ausgabe: Original + geklipptes Residual

**Decoder:**
- Eingabe: codiertes Bild (möglicherweise verzerrt)
- Spatial Transformer Network (STN) zur Perspektivkorrektur
- Conv-Schichten + FC → Sigmoid → 100-Bit-Wahrscheinlichkeiten

**Fehlerkorrektur:** BCH(100, 56): 100 Bit insgesamt = 56 Nutzdatenbits + 44 ECC-Bits.

**C++ über ONNX Runtime:**

```text
tf2onnx: TF 1.13 checkpoint → freeze_graph → tf2onnx → .onnx
```

Zentrale ONNX-Runtime-API: `CreateSessionFromArray()` lädt das Modell aus dem entschlüsselten In-Memory-Puffer. Ein Klartextmodell wird niemals auf die Festplatte geschrieben.

**Execution Provider:**
- Windows: DirectML EP (jede DX12-GPU: NVIDIA/AMD/Intel)
- macOS: CoreML EP (Apple Neural Engine)

**Performance:**

| Auflösung | CPU (i7-12700) | GPU (RTX 3060) |
|-----------|----------------|----------------|
| 400×400 (nativ) | 15-30 ms | 3-8 ms |
| 1024×1024 | 100-200 ms | 15-30 ms |
| 2048×2048 | 200-400 ms | 25-50 ms |

StegaStamp arbeitet mit fester Auflösung 400×400. Optionen für größere Bilder:
- A: skalieren → einbetten → zurückskalieren (schnell, etwas Detailverlust im Wasserzeichen)
- B: kachelbasiert (in jede Kachel einbetten, redundant, robust gegen Zuschnitt)
- C: TrustMark verwenden (beliebige Auflösung)

**Speicherbedarf:** ca. 100-150 MB (Modell ca. 30 MB + ONNX-Runtime-Puffer).

### TrustMark (Adobe, ICCV 2025) {#trustmark-adobe-iccv-2025}

Repo: https://github.com/adobe/trustmark

**Vorteile gegenüber StegaStamp:**
- Beliebige Auflösung (keine 400×400-Beschränkung)
- 100-Bit-Nutzlast mit konfigurierbarer ECC (BCH_SUPER, BCH_5, BCH_4, BCH_3)
- ONNX-Modelle bereits verfügbar (in der JS-Implementierung verwendet)
- PSNR ca. 50 dB (Artefakte nahezu unsichtbar)
- Entwickelt für C2PA (Content Authenticity Initiative)
- Rust-Implementierung für FFI verfügbar

**EMPFEHLUNG: TrustMark statt StegaStamp** für neue Implementierungen. Keine Skalierung nötig, bereits ONNX, aktiv gepflegt (2025).

### DCT Spread Spectrum (Alternative ohne Modell) {#dct-spread-spectrum-no-model-alternative}

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

**DCT vs. neuronal:**

| Kriterium | DCT Spread Spectrum | Neuronal (StegaStamp/TrustMark) |
|-----------|--------------------|-----------------------------|
| Modellgröße | 0 MB | 15-30 MB |
| Geschwindigkeit | <5 ms | 15-200 ms |
| JPEG Q=90 | 85-95 % der Bits | 98 %+ der Bits |
| JPEG Q=70 | 60-80 % der Bits | 95 %+ der Bits |
| Zuschnitt 20 % | 30-50 % der Bits | 90 %+ der Bits |
| Druck-Scan | ca. 50 % | 95 %+ der Bits |

**Neuronal ist für Anti-Piraterie zwingend.** DCT lässt sich durch Zuschnitt + JPEG zu leicht brechen.

### Robustheit (WAVES Benchmark, NeurIPS 2024) {#robustness-waves-benchmark-neurips-2024}

Robustheit von StegaStamp:

| Angriff | Bitgenauigkeit |
|---------|----------------|
| JPEG Q=90 | ca. 99 % |
| JPEG Q=70 | ca. 96-98 % |
| JPEG Q=50 | ca. 92-95 % (BCH korrigiert) |
| Skalieren 50 %+ zurück | ca. 96 % |
| Screenshot | ca. 94-97 % |
| Unschärfe/Rauschen | ca. 95-99 % |
| Druck + Scan | ca. 95 % (Hauptanwendungsfall!) |
| Diffusions-Neugenerierung | ca. 70-85 % (verwundbar) |
| Adversarieller Angriff | ca. 60-80 % |

### Nutzlast-Design (64 Bit empfohlen) {#payload-design-64-bit-recommended}

```text
[32 bits: license_id hash]
[16 bits: timestamp - days since 2025-01-01] = 180 years coverage
[8 bits: app_version + model_version]
[8 bits: CRC-8 or additional ECC]
```

Bei TrustMark (100 Bit): 64 Nutzdatenbits + 36 ECC-Bits.
Bei StegaStamp BCH(100,56): 48 Nutzdatenbits passen bequem in die 56-Bit-Nutzlast.

**Testwasserzeichen:** `license_id = 0x00000000` (reserviert). Unsichtbares Tracking + sichtbares Overlay (zwei Ebenen).

### Decoder-Tool {#decoder-tool}

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

Falsch-positiv-Rate: ca. 1 zu 10^6 bei Schwellwert 0,8. Empfohlener Schwellwert: 0,85.

---

## .hmod-Format für verschlüsselte Modelle {#hmod-encrypted-model-format}

### Warum AES-256-GCM {#why-aes-256-gcm}

- **GCM = Verschlüsselung + Authentifizierung in einem Durchlauf.** CBC benötigt zusätzlich HMAC.
- GCM erkennt Manipulationen automatisch (Auth-Tag).
- GCM ist parallelisierbar (Counter-Modus); CBC nicht (hängt vom vorherigen Block ab).
- AES-NI-Durchsatz: GCM ca. 2,2 GB/s, CBC ca. 1,5 GB/s.

**Nonce pro Tensor (12 Byte):** muss bei gleichem Schlüssel für jede Verschlüsselung eindeutig sein.
- Zufälliger IV: `crypto_random_bytes(12)`. Einfach, sicher für weniger als 2^48 Operationen.
- Abgeleiteter IV: `HKDF(key, tensor_name + counter)`. Deterministisch.

**Empfehlung: zufälliger IV.** Da die Verschlüsselung einmalig zur Build-Zeit erfolgt, ist eine Nonce-Wiederverwendung konstruktionsbedingt ausgeschlossen.

### HKDF-Schlüsselableitung {#hkdf-key-derivation}

```text
HKDF-SHA256(
  input_key_material = device_fingerprint || license_key,
  salt = random_salt (32 bytes, stored in file header),
  info = "hmod-v1-tensor-decryption",
  output_length = 32
)
```

### Dateiformat-Spezifikation {#file-format-specification}

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

**Vergleich mit SafeTensors:**
1. Binärer Header (kein JSON). Netron und Python können ihn ohne unseren Code nicht parsen.
2. Eigene Magic-Bytes. Wird nicht als bekanntes Format erkannt.
3. Verschlüsselte Tensordaten: ohne Schlüssel bedeutungslose Bytes.
4. Keine Lücken erlaubt. Verhindert Polyglot-Dateien.

**Vergleich mit CryptoTensors (arxiv:2512.04580):**

| Aspekt | CryptoTensors | .hmod |
|--------|--------------|-------|
| Basisformat | SafeTensors-Erweiterung | Vollständig eigenes Format |
| AES-GCM-256 pro Tensor | Ja | Ja |
| DEK pro Tensor | Ja | Ja |
| Schlüsselquelle | JWK, KBS, HTTP | HKDF(device_fp + license) |
| Richtlinien | Rego OPA | Keine (Desktop) |
| Mit Netron lesbar | Teilweise | Nein (eigene Magic-Bytes) |
| Ladeaufwand | 2-8x | Ziel: <2x |

### Hybrides Schlüsselmanagement (Envelope Encryption) {#hybrid-key-management-envelope-encryption}

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

**Verteilungsmodell:**
- Eine `.hmod`-Datei auf dem CDN (ca. 200 MB), für alle Nutzer gleich
- Pro Nutzer ein `license_blob` (ca. 1 KB), ausgestellt bei der Aktivierung
- Widerruf: Für diesen Nutzer kein neues license_blob mehr ausstellen
- Kompromittierung: neuen MCK erzeugen, .hmod neu verschlüsseln, alle Nutzer erhalten ein neues license_blob

### Ladeleistung (AES-NI) {#loading-performance-aes-ni}

| Operation | Zeit |
|-----------|------|
| AES-256-GCM-Entschlüsselung 1 MB | ca. 0,5 ms |
| AES-256-GCM-Entschlüsselung 10 MB | ca. 4,5 ms |
| AES-256-GCM-Entschlüsselung 200 MB | ca. 90 ms |
| HKDF-Schlüsselableitung | <1 ms |
| Ed25519-Header-Verifikation | <1 ms |

Ein 200-MB-Modell wird in ca. 90 ms entschlüsselt, für Nutzer nicht wahrnehmbar.

**Hardware-Unterstützung:**
- Windows x64: AES-NI auf allen Intel- (Westmere 2010+) und AMD-CPUs (Bulldozer 2011+)
- macOS Intel: AES-NI; Apple Silicon: ARM-Crypto-Erweiterungen
- libsodium: Prüfung mit `crypto_aead_aes256gcm_is_available()` erforderlich

### Toolchain {#toolchain}

**hmod_packer:**
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

**key_weight_analyzer (Sensitivitätsanalyse):**
```toml
For each tensor: replace with random → measure output degradation
Top 5-10% most impactful = "critical tensors" → must encrypt
Remaining = "non-critical" → optional (speed tradeoff)
```

**hmod_validator:**
```text
1. Check magic + version
2. Parse header (no corruption)
3. Verify Ed25519 signature
4. Per tensor: decrypt + auth tag verify
5. Shape/dtype consistency check
```

---

## SEAL: Watermarking für LoRA-Gewichte {#seal-watermarking-for-lora-weights}

LoRA-Adapter stellen besondere Herausforderungen dar: kleine Delta-Gewichte (Rang 4-64), die entweder in das Basismodell gemergt oder eigenständig verwendet werden können.

**SEAL-Ansatz (Signed Efficient Adaptation for LLMs):**
- Wasserzeichen während des LoRA-Trainings einbetten (nicht nachträglich)
- Das Wasserzeichen übersteht Fine-Tuning, Merging und Quantisierung
- Erkennung über einen statistischen Hypothesentest am verdächtigen Modell
- Einschränkung: erfordert erneutes Training des LoRA mit Watermark-Zielfunktion

**Praktische Alternative zur Erkennung gestohlener LoRAs:**
- Kleine Sentinel-Muster in die Trainingsdaten einbetten (bestimmte Prompts → bestimmte Ausgaben)
- „Canary-Ausgaben“, prüfbar ohne Zugriff auf die Originalgewichte
- Funktioniert auch nach dem Merge: Das gemergte Modell reagiert weiterhin auf die Sentinel-Prompts

**LoRA-spezifische Bedrohungen:**
- StolenLoRA: Extraktion der LoRA-Deltas über wiederholte API-Anfragen (in der Regel reichen 30-100 Anfragen für einen LoRA mit Rang 4)
- Merge-Angriff: LoRA in das Basismodell mergen, Wasserzeichen wird verwässert
- Quantisierung: INT4/INT8 zerstört häufig subtile Wasserzeichenmuster

## Verteilung pro Nutzer (.hmod) {#per-user-hmod-distribution}

**Eine CDN-Datei + ein Lizenz-Blob pro Nutzer (1 KB)** ist die richtige Architektur:
- `.hmod` (ca. 200 MB): für alle Nutzer gleich, auf dem CDN (Cloudflare R2: 5-10 $/Monat)
- `license_blob` (ca. 1 KB): pro Nutzer, bei der Aktivierung ausgestellt
  - Enthält: verschlüsselten MCK-Wrapper + Material zur nutzerspezifischen Schlüsselableitung
  - Widerruf: keine neuen `license_blob` mehr ausstellen, bestehende laufen per TTL ab
- Kompromittierung: neuen MCK erzeugen, `.hmod` neu verschlüsseln, allen Nutzern ein neues `license_blob` ausstellen

**Ablauf der Schlüsselrotation:**
1. Neuen MCK (Model Content Key) erzeugen
2. Alle Tensoren mit neuen DEKs neu verschlüsseln, die unter dem neuen MCK eingepackt werden
3. Modellversion/Epoche im HKDF-Ableitungskontext erhöhen
4. Neue `.hmod` auf das CDN hochladen
5. Alle Nutzer laden beim nächsten Phone-Home ein neues `license_blob`

## Fallstricke {#gotchas}

- **Wiederverwendung einer AES-GCM-Nonce ist katastrophal.** Gleiche Nonce + gleicher Schlüssel bedeutet: XOR der Klartexte wird offengelegt und der Authentifizierungsschlüssel wiederherstellbar. Bei .hmod erfolgt die Verschlüsselung einmalig zur Build-Zeit mit zufälliger Nonce, daher ist Wiederverwendung konstruktionsbedingt ausgeschlossen. Falls du eine erneute Verschlüsselung hinzufügst (z. B. Personalisierung zur Laufzeit), sei äußerst vorsichtig.
- **AES-GCM-Limit von 64 GB pro Nonce.** Ein einzelner Tensor darf 64 GB nicht überschreiten. Modelle sind typischerweise insgesamt 200 MB groß, das ist kein Problem.
- **Teilweiser Entschlüsselungsfehler = sofort abbrechen.** Schlägt das Auth-Tag eines einzelnen Tensors fehl, das Modell nicht laden. Entweder liegt eine beschädigte Datei vor (neu herunterladen) oder eine Manipulation (verweigern).
- **`CreateSessionFromArray` in ONNX Runtime** erlaubt das Laden eines Modells aus einem RAM-Puffer ohne Zugriff auf die Festplatte. Kritisch: diese Funktion statt des Ladens aus einer entschlüsselten temporären Datei verwenden.
- **StegaStamp verwendet TF 1.13.** Für Training/Konvertierung wird eine alte TensorFlow-Umgebung benötigt. Mit tf2onnx ein ONNX-Modell erzeugen, für die Inferenz reicht dann ONNX Runtime.
- **TrustMark-Konfidenzschwelle 0,85** ist der empfohlene Ausgleich. Eine Senkung auf 0,7 erhöht die Falsch-positiv-Rate von 1:10^6 auf ungefähr 1:1000.
- **Diffusions-Neugenerierungsangriffe** (DALL-E, Midjourney „Rinsing“) senken die Genauigkeit von StegaStamp auf 70-85 %. Gegenmaßnahme: kurzlebigere Wasserzeichen verwenden oder dieses Bedrohungsmodell für forensische Zwecke (nicht zur Authentifizierung) akzeptieren.
- **Binärer Header (kein JSON) in .hmod** bedeutet keine kostenlose Kompatibilität mit vorhandenen Tools. Eine Validator-CLI bereitstellen, um Dateien in der Build-Pipeline zu prüfen.
- **Testwasserzeichen:** `license_id = 0x00000000` reservieren. Sichtbares Overlay hinzufügen (zwei Ebenen: unsichtbare forensische Markierung + sichtbarer Testhinweis). Beide werden von derselben Encoder-Pipeline verwaltet.
- **Nutzlast-Design (100-Bit-TrustMark):** 32 Bit license_id-Hash + 16 Bit Tage seit Epoche (reicht für 180 Jahre) + 8 Bit App-/Modellversion + 8 Bit CRC-8 = 64 Nutzdatenbits + 36 ECC-Bits.

## Siehe auch {#see-also}
- [[hkdf-personalized-weights]]
- [[output-scrambling-antipiracy]]
- [[remote-kill-switch]]
- [[licensing-implementation-cpp]]
