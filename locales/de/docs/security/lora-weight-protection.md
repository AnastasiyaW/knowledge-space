---
level: 3
source_sha256: b56a3b7484b2b1b0c1a8c77ce6be8762ff7745ee0000db3c94605b10f7d7e97a
translation: machine
translated_at: '2026-10-24'
---
# LoRA-Gewichtsschutz: Wasserzeichen, Extraktionsangriffe und Lizenzierung {#lora-weight-protection-watermarking-extraction-attacks-and-licensing}

Datum: 2026-04-03
Kontext: Desktop-/Server-Bildgenerierung mit proprietären LoRA-Adaptern auf Open-Source-Basismodellen (FLUX, SD). Behandelt den Schutz von Adaptergewichten vor Diebstahl, forensischen Eigentumsnachweis und die Abwehr von Extraktionsangriffen.

---

## Bedrohungsmodell {#threat-model}

LoRA-Adapter (delta_W = B × A, gespeichert als `.safetensors`, 10-200 MB) haben vier inhärente Schwachstellen:

1. **Portabilität** - eine Datei, funktioniert mit jeder Kopie desselben Basismodells
2. **Kompakter Format** - trivial per E-Mail, USB oder Cloud-Speicher weiterzugeben
3. **Extrahierbarkeit** - ist das Basismodell öffentlich, lässt sich delta_W rekonstruieren: `delta_W = merged_model - base_model`
4. **Abfragebasierte Extraktion** - selbst bei reinem API-Zugriff sind Distillationsangriffe möglich

---

## LoRA-spezifische Wasserzeichenverfahren {#lora-specific-watermarking-methods}

### SEAL (Verschränkte White-Box-Wasserzeichen) {#seal-entangled-white-box-watermarks}

**Paper:** arxiv:2501.09284 (Jan 2025)

Bettet während des Trainings eine geheime, nicht trainierbare Matrix zwischen die trainierbaren LoRA-Gewichtsmatrizen ein. Das Wasserzeichen ist mit den trainierten Gewichten „verschränkt“ - das Extrahieren des SEAL-Wasserzeichens erfordert die Lösung eines gemeinsamen Optimierungsproblems.

**Eigenschaften:**
- Keine Qualitätsverschlechterung bei Text-zu-Bild- oder Instruction-Tuning-Aufgaben
- Resistent gegen: Entfernungsangriffe, Verschleierung, Mehrdeutigkeitsangriffe
- Verifikation erfolgt White-Box (erfordert Zugriff auf das Modell)

**Integration ins Training:**
```python
# Pseudo-code: SEAL inserts a fixed passport matrix P
# between LoRA A and B matrices during forward pass
def forward(x, A, B, P, alpha):
    # Standard LoRA: output = x + alpha * (B @ A @ x)
    # SEAL: output = x + alpha * (B @ P @ A @ x)
    # P is non-trainable, randomly initialized at training start
    return x + alpha * (B @ P @ A @ x)
```

### AquaLoRA (White-Box, SD-spezifisch) {#aqualora-white-box-sd-specific}

**Paper:** arxiv:2405.11135 (ICML 2024) | [GitHub](https://github.com/Georgefwt/AquaLoRA)

Zweistufig: (1) Vortraining von Wasserzeichen-Encoder/Decoder im Latent Space; (2) Einbettung des Wasserzeichens in das SD-U-Net via LoRA während des Fine-Tunings.

- **Kapazität:** 48 Bit pro Modell
- **Skalierungsmatrix:** ermöglicht die Änderung der Wasserzeichen-Nutzlast ohne vollständiges Neutraining
- Resistent gegen: LoRA-Merge, Entfernungsversuche

### LoRAGuard (Black-Box, Yin-Yang-Verfahren) {#loraguard-black-box-yin-yang-method}

**Paper:** arxiv:2501.15478 (Jan 2025)

Erkennt Eigentum ohne Zugriff auf interne Gewichte:
- **Yin** (Pfad mit negativem Gewicht): detektierbar über die Negationsoperation auf Modellausgaben
- **Yang** (Pfad mit positivem Gewicht): detektierbar über die Additionsoperation

Löst das zentrale Problem, dass bisherige Wasserzeichen bei LoRA-Kombination (Zusammenführen mehrerer Adapter) oder Negation brechen. Nahezu 100 % Verifikationserfolgsrate.

### AuthenLoRA (Output-propagierendes Wasserzeichen) {#authenlora-output-propagating-watermark}

**Paper:** arxiv:2511.21216 (Nov 2025) | [GitHub](https://github.com/ShiFangming0823/AuthenLoRA)

Das Wasserzeichen wandert in jedes generierte Bild, nicht nur in die Gewichte:
- Duale Zielfunktion: optimiert Stiltransfer und Wasserzeicheneinbettung gemeinsam
- Ein leichtgewichtiger Mapper ermöglicht die Änderung der Wasserzeichen-Nutzlast ohne vollständiges Neutraining
- Detektion funktioniert auf Bildausgaben - nützlich auch dann, wenn die Gewichte gestohlen wurden

### Vergleichstabelle {#comparison-table}

| Verfahren | Jahr | Box | Resistent gegen Merge | Resistent gegen Quantisierung | Kapazität |
|-----------|------|-----|-----------------------|-------------------------------|-----------|
| AquaLoRA | 2024 | White | Ja | Teilweise | 48 Bit |
| SEAL | 2025 | White | Ja | Ja | Eingebettet |
| LoRAGuard | 2025 | Black | Ja | Ja | Binär |
| AuthenLoRA | 2025 | Output | k. A. (pro Bild) | k. A. | Pro Bild |
| MOLM | 2024 | Routing | Ja | Ja | >0,98 Genauigkeit |

**Empfehlung für den Produktivbetrieb:** SEAL für den Eigentumsnachweis auf Gewichtsebene, zusätzlich AuthenLoRA oder ein Standard-Ausgabewasserzeichen für forensische Analysen auf Bildebene. Beides kombinieren: den Besitz der Gewichte UND die Herkunft bestimmter Bilder aus dem eigenen Modell nachweisen.

---

## Extraktionsangriffe {#extraction-attacks}

### StolenLoRA (Abfragebasierte Distillation) {#stolenlora-query-based-distillation}

**Paper:** arxiv:2509.23594 (ICCV 2025)

Angriff, der die LoRA-Funktionalität mithilfe synthetischer Anfragen rekonstruiert:

- **Methode:** Der Angreifer erzeugt synthetische Daten über ein LLM und Diffusion, fragt die Ziel-API ab und trainiert aus den Antworten einen Student-LoRA mittels Disagreement-based Semi-supervised Learning (DSL)
- **Kosten:** ca. 10.000 Anfragen, von einem Nutzer an einem Tag machbar
- **Erfolgsrate:** 96,6 % funktionale Replikation
- **Backbone-übergreifend:** funktioniert auch, wenn der Angreifer ein anderes Basismodell als das Opfer verwendet

**Folgerung:** Reiner API-Schutz (Gewichte werden nie ausgeliefert) ist NICHT ausreichend. 10.000 Anfragen von einem Nutzer = Ihr LoRA ist rekonstruiert.

### Merge-and-Subtract (Gewichtsextraktion aus dem zusammengeführten Modell) {#merge-and-subtract-weight-extraction-from-merged-model}

Ist das Basismodell öffentlich (FLUX, SD):
```python
# Attacker recovers delta_W exactly
import torch
merged = load_state_dict("your_product_model.safetensors")
base = load_state_dict("FLUX.1-dev.safetensors")  # public
delta_W = {k: merged[k] - base[k] for k in merged}
# delta_W ≈ your LoRA (full-rank, functionally equivalent)
```

`unfuse_lora()` in Diffusers verwendet genau diese Mathematik. Das Zusammenführen mit einem Open-Source-Basismodell bietet **keinen Schutz**, wenn der Angreifer das Basismodell kennt - und das tut er, da es öffentlich ist.

**Teilweise Gegenmaßnahmen (geringere Wirksamkeit):**
- INT4/INT8-Quantisierung nach dem Merge (verschlechtert die Präzision der Rekonstruktion)
- Fine-Tuning auf Rauschen für einige Schritte nach dem Merge (verwischt die Delta-Grenze)
- Mehrere LoRAs zusammenführen (schwieriger, einen einzelnen herauszurechnen)

**Wirksamkeit des Merge als Schutz: 2/10**

### Membership Inference auf LoRA {#membership-inference-on-lora}

**Paper:** arxiv:2507.18302 (Jul 2025)

Membership-Inference-Angriffe (MIA) können bestimmen, ob bestimmte Bilder im Trainingsdatensatz enthalten waren, indem das LoRA abgefragt wird. Relevant für Betriebsgeheimnisse und DSGVO-Konformität: Die Zugehörigkeit zu Trainingsdaten kann aus dem Modellverhalten abgeleitet werden.

---

## Verteidigungsstrategien {#defense-strategies}

### Gegen abfragebasierte Extraktion (StolenLoRA) {#against-query-based-extraction-stolenlora}

```python
# Server-side: detect extraction patterns
def detect_extraction_query(user_id: str, request: dict) -> float:
    """Returns extraction suspicion score 0-100"""
    history = get_request_history(user_id, hours=24)
    
    score = 0
    # High volume from single user
    if len(history) > 500: score += 30
    if len(history) > 2000: score += 50
    
    # Uniform/grid-like inputs (systematic sampling)
    if _is_systematic_sampling(history): score += 40
    
    # Inputs similar to known synthetic datasets
    if _resembles_synthetic_grid(request): score += 20
    
    return min(score, 100)
```

**Gegenmaßnahmen:**
- Ratenbegrenzung pro Lizenz (weiche Obergrenze 50-100 Inferenzen/Tag, harte Obergrenze 500/Tag)
- Ausgabeverzerrung: minimales, unsichtbares Rauschen hinzufügen, das das Training des Student-Modells verschlechtert, ohne die Nutzerqualität zu beeinträchtigen
- API-Fingerprinting: nutzerspezifisches Wasserzeichen in alle API-Ausgaben einbetten (nach AuthenLoRA-Muster)
- Anomalieerkennung bei Abfragemustern (systematische Eingaben = Rastersampling = Extraktion)

### Gegen Speicherabbild entschlüsselter Gewichte {#against-memory-dump-of-decrypted-weights}

Sobald die Gewichte für die Inferenz entschlüsselt sind, liegen sie im RAM. Gegenmaßnahmen:

- `VirtualLock()` (Windows) bzw. `mlock()` (macOS/Linux) auf Gewichtspuffern verwenden, um das Auslagern auf die Festplatte zu verhindern
- Gewichtspuffer unmittelbar nach Sitzungsende leeren (`sodium_memzero()`)
- CORELOCKER-Muster: kritische Tensoren nur vom Server ausliefern, niemals lokal speichern

```cpp
// Lock weight buffer in RAM, prevent swap to pagefile
VirtualLock(tensor_buffer, tensor_size);
// ... run inference ...
sodium_memzero(tensor_buffer, tensor_size);
VirtualUnlock(tensor_buffer, tensor_size);
```

---

## Laufzeitverschlüsselung in ComfyUI (ComfyUI-LMCQ) {#comfyui-runtime-encryption-comfyui-lmcq}

**GitHub:** [github.com/sebord/ComfyUI-LMCQ](https://github.com/sebord/ComfyUI-LMCQ)

Praktische, hardwaregebundene Verschlüsselung für ComfyUI-Deployments:

**Erzeugung des Maschinencodes:**
```text
GPU ID + CPU serial + MAC address + disk serial + motherboard ID
-> HMAC-SHA256 -> machine_code
```

**Workflow:**
1. `machine_code` auf der Zielmaschine erzeugen
2. LoRA-Datei an die Liste autorisierter `machine_code`-Werte gebunden verschlüsseln
3. Runtime-Entschlüsselungsknoten verifiziert `machine_code` vor dem Laden
4. Das Modell existiert nur im Speicher - keine entschlüsselte Datei wird auf die Festplatte geschrieben

**Einschränkungen:**
- Hardware-Spoofing umgeht die Maschinenbindung
- VMs haben instabile Hardware-IDs (brechen bei Snapshot-Wiederherstellung)
- Cloud-GPU-Instanzen wechseln Hardware-IDs beim Austausch der Instanz
- Nach der Entschlüsselung liegen die Gewichte im RAM - ein Speicherabbild ist weiterhin möglich

---

## Lizenzbeschränkungen von FLUX {#flux-license-constraints}

| Modell | Lizenz | Kommerzielle Nutzung |
|--------|--------|----------------------|
| FLUX.1 [dev] | Non-Commercial v2.0 | Nicht zulässig ohne Vereinbarung mit BFL |
| FLUX.2 Klein 4B | Apache 2.0 | Vollständig zulässig |
| FLUX.2 Klein 9B | Non-Commercial | Erfordert kommerzielle Lizenz von BFL |
| Stable Diffusion 1.5/SDXL | CreativeML Open RAIL-M | Zulässig mit Nutzungsbeschränkungen |

**LoRA-Derivate übernehmen die nutzungsbasierten Beschränkungen** der Basismodell-Lizenz, müssen aber nicht als Open Source veröffentlicht werden. Ein auf FLUX.1 [dev] trainiertes LoRA darf kommerziell nicht ohne BFL-Lizenz genutzt werden, unabhängig davon, ob Sie das LoRA besitzen.

Für produktive Retusche-Anwendungen: Klein 4B verwenden (Apache 2.0, keine Einschränkungen) oder eine kommerzielle BFL-Lizenz für Klein 9B einholen.

---

## Fingerprinting für den rechtlichen Eigentumsnachweis {#fingerprinting-for-legal-ownership-proof}

### Chain & Hash (arxiv:2407.10887) {#chain-hash-arxiv240710887}

Bindet Fingerprint-Prompts kryptografisch an die Antworten. Der Eigentümer speichert Paare (Prompt, erwartete_Antwort) - dies zeigt, dass die Ausgabe nur von seinem Modell deterministisch erzeugt werden kann. Dient im Streitfall als Eigentumsnachweis.

### LoRA-FP-Framework (arxiv:2509.00820) {#lora-fp-framework-arxiv250900820}

Plug-and-play-Einbettung von Fingerprints über constrained Fine-Tuning:
- Der Fingerprint überträgt sich über Parameter-Fusion auf abgeleitete Modelle
- Geringerer Rechenaufwand als Verfahren mit vollständiger Parameteranpassung
- Übersteht inkrementelles Fine-Tuning

### RoFL (arxiv:2505.12682) {#rofl-arxiv250512682}

Fingerprint über statistische Ausgabemuster:
- Resistent gegen Fine-Tuning, Pruning und Quantisierung
- Nutzt kryptografische Commitments (vor dem Deployment veröffentlichter Hash = Vorregistrierung)
- Liefert gerichtsverwertbare Beweise: „Wir haben Fingerprint X registriert, bevor Ihr Modell erschien“

---

## Stolpersteine {#gotchas}

- **Merge-and-Subtract hebelt jede Gewichtsverschlüsselung aus, wenn das Basismodell öffentlich ist.** Das Verschlüsseln der zusammengeführten Modelldatei ist nutzlos, wenn das Basismodell öffentlich verfügbar ist und der Angreifer weiß, welches Basismodell verwendet wurde. Schützen Sie nur eigenständige LoRA-Dateien oder verwenden Sie ein privates Basismodell.
- **StolenLoRA macht „nur API“ zu einer falschen Sicherheit.** 10.000 Anfragen an einem Tag sind für einen professionellen Fotografen normale Nutzung. Ratenbegrenzung muss mit verhaltensbasierter Erkennung kombiniert werden (Rastersampling-Muster, einheitliche Bildmerkmale), nicht nur mit einer Anfragezählung.
- **FHE (homomorphe Verschlüsselung) für die Inferenz ist etwa 1000-mal langsamer.** PrivTuner und ähnliche Arbeiten zeigen, dass FHE-Inferenz auf LoRA theoretisch möglich ist, aber um Größenordnungen zu langsam für interaktive Bildgenerierung. Stand 2026 nicht praktikabel.
- **Ein AuthenLoRA-Wasserzeichen in den Ausgaben kann von Angreifern geprüft werden.** Kann der Angreifer erkennen, ob seine extrahierte Kopie dasselbe Wasserzeichenmuster ausgibt, kann er überprüfen, ob seine Extraktion erfolgreich war. Den Wasserzeichen-Decoder ausschließlich serverseitig betreiben.
- **Das ComfyUI-Format `.ckpt`/`.pt` erlaubt über Pickle die Ausführung beliebigen Codes.** Für Verteilung und Laden von LoRAs immer `.safetensors` verwenden. `.safetensors` wurde sicherheitsgeprüft; Pickle nicht.
- **Das Yin-Yang-Verfahren von LoRAGuard erfordert ein spezifisches Inferenz-Setup.** Die Detektion setzt voraus, dass das Modell mit Negations- oder Additionsoperationen ausgeführt wird, die nicht Teil der normalen Inferenz sind. Wird das Verifikationsprotokoll nicht beibehalten, geht die Möglichkeit verloren, später einen Eigentumsnachweis zu führen.

## Siehe auch {#see-also}
- [[watermarking-encrypted-models]]
- [[hkdf-personalized-weights]]
- [[model-weight-encryption]]
- [[output-scrambling-antipiracy]]
- [[anti-piracy-legal]]
