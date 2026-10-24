---
level: 3
source_sha256: 2aaf366802e80ca6615437250800d3a7faf74f9a0bb5ba96e8298d2f25866aad
translation: machine
translated_at: '2026-10-24'
---
# HKDF + ChaCha20 personalisierte Gewichte neuronaler Netze {#hkdf-chacha20-personalized-neural-network-weights}

Datum: 2026-04-03
Kontext: Desktop-C++-Anwendung, ONNX-Runtime-Inferenz. Pro Benutzer eindeutige Gewichte über einen aus HKDF abgeleiteten Seed und einen ChaCha20-Strom. Funktional äquivalente Modelle: Die Permutationssymmetrie garantiert identische Ausgaben.

---

## Kernkonzept {#core-concept}

Der Server hält das `master_secret`. Die HKDF-Ableitung pro Benutzer liefert Seeds für drei Operationen:
- **Permutation**: Umordnung der Neuronenindizes (verlustfrei, mathematisch äquivalent)
- **Skalierung**: multiplikative Gewichtsstörung (~±3 %)
- **Offset**: additive Gewichtsstörung (~±0,5 % des Gewichtsbetrags)

Die Modellgewichte jedes Benutzers sind eindeutig, liefern aber identische Ausgaben (innerhalb der Toleranz der Gleitkommaarithmetik).

---

## HKDF + ChaCha20 Implementierung {#hkdf-chacha20-implementation}

### Warum diese Kombination {#why-this-combination}

**HKDF allein:** Bei SHA-256 auf 255 × HashLen = 8160 Byte begrenzt. Für Modelle mit über 100 Mio. Parametern nicht ausreichend.

**Lösung:** HKDF erzeugt 32-Byte-Seeds, ChaCha20 expandiert sie zu einem Strom beliebiger Länge.

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

### Wahl der Bibliothek {#library-choice}

| Bibliothek | HKDF | Geschwindigkeit | API |
|---------|------|-------|-----|
| OpenSSL 3.x | EVP_KDF | Am schnellsten (HW-SHA-256) | Ausführlicher Boilerplate-Code |
| libsodium 1.0.19+ | `crypto_kdf_hkdf_sha256_*` | ~20 % langsamer | Einfach, fehlertolerant gegenüber Fehlbedienung |
| Eigenständig (RFC 5869) | Selbst implementiert | Abhängig von HMAC | Volle Kontrolle |

**Empfehlung: libsodium.** Wird ohnehin für andere Kryptooperationen benötigt. ChaCha20 erreicht ~1705 MiB/s ohne AES-NI (wichtig für schwache GPU-Rechner).

**ChaCha12 vs. ChaCha20:** 12 Runden sind ~1,6× schneller. Für dieses Bedrohungsmodell (PRNG, keine Verschlüsselung) ausreichend. Geschätzte Gesamtzeit für die Personalisierung eines Modells mit 100 Mio. Parametern: <500 ms auf einer langsamen CPU.

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

### Alternative mit OpenSSL 3.x {#openssl-3x-alternative}

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

Mehr Boilerplate-Code, größere Abhängigkeit, keine praktische ChaCha20-Stream-API.

---

## Permutationssymmetrie: Welche Schichten sich permutieren lassen {#permutation-symmetry-which-layers-can-be-permuted}

### Theorie {#theory}

**Permutationssymmetrie** (arxiv:2506.13018, arxiv:2502.17391): Für eine FC-Schicht mit n Neuronen existieren n! äquivalente Parametrisierungen mit **identischer Ausgabe**. Die Permutation von Neuron i→j erfordert:
1. Permutation der Zeile i→j in der Ausgabe-Gewichtsmatrix dieser Schicht
2. Permutation der Spalte i→j in der Eingabe-Gewichtsmatrix der **nächsten** Schicht
3. Permutation der entsprechenden Bias-Werte

**Arbeiten, die die Qualitätserhaltung bestätigen:**
- NeuPerm (arxiv:2510.20367): Permutation verborgener Schichten eines LLM bewirkt einen Genauigkeitsverlust von <0,01 %
- Git Re-Basin (arxiv:2209.04836): nutzt dieselbe Symmetrie für Model Merging

### Regeln pro Schichttyp {#layer-by-layer-rules}

| Schichttyp | Permutation sicher? | Was permutiert wird | Einschränkungen |
|------------|-----------------|-----------------|-------------|
| **Fully Connected** | JA | W_out-Zeilen + W_in-Spalten + Bias | Klassische Permutationssymmetrie |
| **Conv2d (verborgen)** | JA | Ausgabekanäle = „Neuronen“. Ausgabekanäle der aktuellen + Eingabekanäle der nächsten Schicht + Bias permutieren | Wie FC |
| **Gruppierte Conv** | TEILWEISE | Nur innerhalb jeder Gruppe | Gruppen können nicht vertauscht werden |
| **Depthwise Conv** | NEIN | 1 Filter = 1 Kanal, Permutation bedeutungslos | |
| **Attention Q/K/V** | TEILWEISE | Attention-Heads als Ganzes permutieren | Neuronen innerhalb eines Heads nicht ohne konsistente Q-, K-, V-Permutation permutierbar |

### Schichten, die NICHT unabhängig permutiert werden können {#layers-that-cannot-be-permuted-independently}

| Schicht | Warum | Konsequenz |
|-------|-----|-------------|
| **BatchNorm** | Speichert running_mean/var pro Kanal | BN-Parameter müssen zusammen mit der vorangehenden Conv permutiert werden |
| **LayerNorm** | gamma/beta sind an Merkmalspositionen gebunden | Ebenfalls zusammen mit der vorangehenden Schicht permutieren |
| **Skip-Verbindungen (Residual)** | Ein- und Ausgabe müssen dieselbe Reihenfolge haben | Die Permutation im Block muss am Ausgang aufgehoben werden (P_out = P_in^(-1)) |
| **Eingabeschicht** | Kanäle sind an RGB gebunden | Eingabekanäle niemals permutieren |
| **Ausgabeschicht** | Kanäle sind an die Aufgabe gebunden (RGB-Ausgabe) | Ausgabekanäle niemals permutieren |

### Besonderheiten bei U-Net {#u-net-specifics}

Ein U-Net mit Skip-Verbindungen ist der komplexeste Fall:

```yaml
Encoder:              Decoder:
conv1 → pool ----skip---→ upconv4 + concat
conv2 → pool ----skip---→ upconv3 + concat
conv4 (bottleneck)  ---→ upconv1
```

Regeln:
1. **Bottleneck (conv4):** SICHER. Keine Skip-Verbindung; die Kanäle sind in sich abgeschlossen.
2. **Encoder-Conv innerhalb eines Blocks:** SICHER, wenn sich die Permutation durch den Block fortsetzt und vor der Skip-Verbindung aufgehoben wird.
   - Ausgabekanäle von conv1 permutieren → BN1 permutieren → Eingabekanäle von conv2 permutieren
   - Ausgabekanäle von conv2 NICHT anfassen (sie fließen in die Skip-Verbindung)
3. **Kanäle der Skip-Verbindung:** Müssen nach dem Concat der Decoder-Eingabe entsprechen. Die Permutation des Encoder-Ausgangs erfordert eine passende Decoder-Permutation.
4. **Attention-Heads (Stable-Diffusion-U-Net):** Ganze Heads permutieren (8 Heads = 8! = 40320 Varianten, zu wenig für Sicherheit).

### Praktische Strategie für das Retouching-Modell {#practical-strategy-for-retouching-model}

**Nur permutieren: Bottleneck + interne Conv-Schichten innerhalb der Residualblöcke.**

Sicherheitsgewinn:
- Bottleneck mit 512 Kanälen: 512! ~ 10^1166 Permutationen
- Jeder Conv-Block mit 256 Kanälen: 256! ~ 10^507
- Zusammen: astronomisch großer Suchraum

NICHT anfassen: Ein- und Ausgabeschichten, Grenzen der Skip-Verbindungen.

---

## Injektion von Skalierung und Offset {#scaleoffset-injection}

### Sichere Störbereiche {#safe-perturbation-ranges}

| Schichttyp | Skalierungsbereich | Offset-Bereich | Hinweise |
|------------|-------------|--------------|-------|
| Conv2d (verborgen), konservativ | 0,97 – 1,03 | ±0,005 | **Empfohlen** |
| Conv2d (verborgen), standard | 0,95 – 1,05 | ±0,02 | Gefahr sichtbarer Verschlechterung |
| Linear (verborgen) | 0,95 – 1,05 | ±0,01 | FC-Gewichte sind meist größer und weniger empfindlich |
| BatchNorm gamma/beta | 0,98 – 1,02 | ±0,01 | BN ist empfindlich, nur kleine Störungen |
| Attention Q/K/V | 0,97 – 1,03 | ±0,005 | Skalarprodukt verstärkt Fehler quadratisch |
| Erste/letzte Schicht | **NICHT ANFASSEN** | **NICHT ANFASSEN** | Direkter Einfluss auf die Abbildung von Ein- und Ausgabe |

### Warum der Offset gefährlicher ist als die Skalierung {#why-offset-is-more-dangerous-than-scale}

Skalierung 0,97–1,03 entspricht einer Abweichung von ±3 %. Bei einem typischen Conv-Gewicht von ~0,05 sind das ±0,0015 (klein).

Ein Offset von ±0,02 bei demselben Gewicht entspricht ±40 % des Werts (katastrophal bei kleinen Gewichten).

**Besser: relativer Offset proportional zum Gewichtsbetrag:**

```cpp
// w' = w * scale + offset * |w|
// offset here is a coefficient, not absolute value
float perturbed = weight * scale + offset_coeff * fabsf(weight);
```

Damit bleiben die Störungen proportional zum Betrag des Gewichts.

### Verifikation der funktionalen Äquivalenz {#functional-equivalence-verification}

Nach der Personalisierung prüfen, ob die Ausgabe mit der Referenz übereinstimmt:

```cpp
// Run original and personalized model on same input
// Maximum acceptable per-pixel difference: ~0.001 (float32)
// PSNR should remain > 50 dB
float max_diff = 0.0f;
for (size_t i = 0; i < output_size; i++)
    max_diff = std::max(max_diff, fabsf(orig[i] - personalized[i]));
assert(max_diff < 1e-3f); // permutation must be lossless
```

Die Permutation sollte **exakt** verlustfrei sein (max_diff ≈ FP32-Epsilon). Skalierung und Offset führen zu kleinen Störungen.

---

## Epochenrotation {#epoch-rotation}

Das Epochenfeld in der HKDF-Ableitung erlaubt eine periodische Schlüsselrotation ohne Neuerzeugung der Gewichte:

```cpp
// info = "user:{account_id}:perm:epoch:{epoch_num}"
// Each epoch produces completely different permutation for same account
// Leaked weights from epoch N are useless after epoch increment
snprintf(info_perm, sizeof(info_perm),
    "user:%s:perm:epoch:%u", account_id, epoch);
```

Auslöser für eine Epochenaktualisierung:
- Modellaktualisierung (alle 2–4 Wochen)
- Verdacht auf Kompromittierung einzelner Konten
- Planmäßige Rotation (z. B. alle 90 Tage)

Der Server speichert nur: `{account_id, epoch, master_secret}` (~300 Byte pro Benutzer). Alle personalisierten Gewichte werden bei Bedarf berechnet. 1 Mio. Benutzer ergeben bei typischer Nutzung ~12 Anfragen/s und passen auf einen VPS für 20 $ pro Monat.

## Einschränkungen bei INT8-Quantisierung {#int8-quantization-constraints}

Skalierungs- und Offset-Störungen müssen die INT8-Quantisierung überstehen, sofern sie verwendet wird:

```text
INT8 range: [-128, 127] → float range ≈ [-1.0, 1.0] (typical scale ~0.0078)
Minimum distinguishable delta: 1 LSB = 0.0078

Safe perturbation for INT8:
  scale: 0.998 - 1.002 (not 0.95-1.05 - these cause LSB collapse)
  offset: ±0.001 * abs(w) (relative)
```

FP16 ist nachsichtiger: 1 LSB ≈ 6e-5 (halber Exponentenbereich). Skalierung 0,97–1,03 ist für FP16 sicher.

## ONNX-Gewichtstausch {#onnx-weight-swap}

Basismodell laden, Permutation im Speicher anwenden, Inferenz ausführen. Eine Änderung der Modelldatei ist nicht nötig:

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

Für C++ über die ONNX-C-API: `OrtValue`-Tensoren vor der Session-Erzeugung mit `CreateTensorWithDataAsOrtValue` und dem permutierten Puffer ändern.

## Fallstricke {#gotchas}

- **HKDF-Expand-Info-Strings müssen pro Zweck eindeutig sein.** Wenn für Permutations- und Skalierungs-Seeds dieselbe Info verwendet wird, entsteht derselbe Schlüssel, und die Trennung der Zwecke ist vollständig aufgehoben. Immer unterschiedliche Labels verwenden.
- **Modulo-Bias bei Fisher-Yates:** `raw % (i+1)` ist leicht verzerrt, wenn i+1 keine Zweierpotenz ist. Bei Permutationen mit n < 2^24 ist diese Verzerrung vernachlässigbar (< 10^-7). Für kryptografisch belastbare Mischung Rejection Sampling verwenden.
- **ChaCha20 mit nonce=0 ist hier sicher,** weil jeder Seed ein eindeutiger 256-Bit-Schlüssel ist (abgeleitet aus unterschiedlichen HKDF-Info-Strings). Ein anderer Schlüssel ergibt unabhängig vom Nonce einen anderen Strom.
- **BatchNorm getrennt von der Conv zu permutieren beschädigt das Modell.** Immer gemeinsam permutieren: `{conv.weight, conv.bias, bn.weight, bn.bias, bn.running_mean, bn.running_var}`.
- **Skip-Verbindungen im U-Net erfordern gepaarte Permutationen.** Wird nur die Encoder-Seite permutiert, ohne den Decoder-Eingang anzupassen, entstehen an den Skip-Concat-Stellen falsche Ausgaben.
- **Attention-Head-Permutation liefert nur n_heads!-Varianten** (z. B. 8! = 40320 für 8 Heads). Das reicht für Sicherheit nicht aus. Stattdessen Neuronen innerhalb der Heads konsistent in Q, K, V permutieren.
- **Skalierungs- und Offset-Störungen akkumulieren sich über die Schichten.** Bei tiefen Netzen (50+ Schichten) summiert sich schon eine Störung von 0,3 % pro Schicht. Immer das endgültige Ausgabe-PSNR testen, nicht nur Metriken pro Schicht.
- **Leck des Master Secret = alle Benutzer kompromittiert.** Das master_secret in einem HSM oder einer sicheren Enklave auf dem Server speichern. Niemals an Clients ausliefern.
- **INT8-Quantisierung hebt große Störungen auf.** Skalierung 0,95–1,05 fällt in denselben INT8-Bereich, und die Personalisierung verschwindet. Für quantisierungskompatible Modelle Skalierung 0,998–1,002 verwenden.
- **Angriff durch Mittelung der Gewichte:** Ein Angreifer mittelt die personalisierten Gewichte von K Benutzern in der Hoffnung, dass sich die Permutation aufhebt. Die Permutation verhindert dies (Neuronen stehen an unterschiedlichen Positionen), die Skalierung und der Offset aber nicht. Wenn solche Mittelung eine realistische Bedrohung ist, ist eine zusätzliche Absicherung nötig.

## Siehe auch {#see-also}
- [[watermarking-encrypted-models]]
- [[output-scrambling-antipiracy]]
- [[licensing-implementation-cpp]]
