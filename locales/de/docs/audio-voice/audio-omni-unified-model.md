---
level: 3
source_sha256: b44a0f31126dfe84f2c8583253be3175affe626e426f162451747656240c14ac
translation: machine
translated_at: '2026-10-24'
---
# Audio-Omni: Einheitliches Verstehen, Generieren und Bearbeiten von Audio {#audio-omni-unified-audio-understanding-generation-and-editing}

Ein einziges Modell für das Verstehen, Generieren und Bearbeiten von Audio, bestehend aus einem eingefrorenen LLM für das Schlussfolgern und einer trainierbaren Diffusion Transformer (DiT) für die hochwertige Audiosynthese. [arxiv 2604.10708] SIGGRAPH 2026.

## Architektur {#architecture}

Das Design besteht aus zwei Komponenten: Ein eingefrorenes multimodales LLM übernimmt das Schlussfolgern und die Konditionierung, ein trainierbarer DiT die hochwertige Audiosynthese.

```text
Text / Audio / Video input
         ↓
  ┌─────────────────────────────────────┐
  │  FROZEN Qwen2.5-Omni (multimodal)   │  ← reasoning, context, knowledge
  │  - Audio encoder                    │
  │  - Text encoder                     │
  │  - Cross-modal reasoning            │
  └─────────────────────────────────────┘
         ↓  semantic conditioning
  ┌─────────────────────────────────────┐
  │  TRAINABLE Diffusion Transformer    │  ← high-fidelity synthesis
  │  - Audio latent diffusion           │
  │  - Conditioned on LLM embeddings    │
  └─────────────────────────────────────┘
         ↓
  Generated / edited audio
```

**Warum das LLM eingefroren wird:** Es bleibt das allgemeine Wissen erhalten, der Trainingsaufwand sinkt, und eine Anpassung an neue Aufgaben erfolgt zero-shot über Prompts statt über Fine-Tuning für jede Aufgabe.

Für Video-zu-Audio-Aufgaben wird zusätzlich ein Synchformer-Checkpoint für die zeitliche Ausrichtung von Bild und Audio verwendet.

## Funktionsumfang {#capabilities}

### Verstehen {#understanding}
- Audio-Captioning und Frage-Antwort
- Sprachanalyse: Geschlecht, Anzahl der Sprecher, Erkennung von Sarkasmus
- Klassifikation von Geräuschen und Identifikation von Schallquellen
- Erkennung der Hintergrundszene

### Generieren {#generation}
- Text-zu-Audio (Umgebungsgeräusche, Foley)
- Text-zu-Musik (aus Video oder Text)
- Video-zu-Audio
- Video-zu-Musik (Soundtrack)
- Text-zu-Sprache
- Zero-shot-Stimmkonvertierung

### Bearbeiten (auf Wort- und Segmentebene) {#editing-wordsegment-level}
Die Audiobearbeitung ist die entscheidende Fähigkeit. Kein vergleichbares offenes Modell bietet alle vier Operationen:

```python
# Add a sound element to existing audio
model.edit("Add", "input.wav", desc="skateboarding sounds")

# Remove a specific element
model.edit("Remove", "input.mp3", desc="female singing")

# Extract a specific element
model.edit("Extract", "input.wav", desc="piano melody")

# Apply style transfer
model.edit("Style", "input.wav", desc="lo-fi hip hop")

# Replace a word/phrase in speech
model.edit("Speech", "input.wav", desc="replace 'hello' with 'goodbye'")
```

## Technische Spezifikationen {#technical-specs}

| Parameter | Wert |
|---|---|
| Basis-LLM | Qwen2.5-Omni (eingefroren) |
| Checkpoint-Größe | ca. 21 GB |
| Geschätzte Parameter | ca. 8–14B (bf16) |
| Lizenz | **CC-BY-NC-4.0** (nicht kommerziell) |
| Sprachen | EN, CN, JA, FR, DE |
| Russisch | Nicht unterstützt |
| VRAM (Inferenz) | mindestens 24 GB; empfohlen 40+ GB |
| Python | 3.11 |
| Referenzaudio (Stimmklonen) | Zero-shot (keine Mindestlänge angegeben) |
| Fine-Tuning- / LoRA-Rezept | Nicht bereitgestellt |
| Kommerzielle Lizenz | Nur auf Anfrage |

## Trainingsdaten {#training-data}

**AudioEdit**-Datensatz: über 1 Mio. kuratierte Bearbeitungspaare, speziell für Audiobearbeitungsaufgaben erstellt. Ob er als eigenständiger offener Datensatz verfügbar sein wird, ist zum Zeitpunkt der Erstellung nicht bestätigt. Sollte er veröffentlicht werden, wäre er wertvoll, um Bearbeitungsfähigkeiten auf Basis kommerziell lizenzierter TTS-Modelle zu trainieren.

## Vergleich: Audio-Omni vs. spezialisierte TTS-Modelle {#comparison-audio-omni-vs-specialized-tts}

| Aspekt | Audio-Omni | VoxCPM2 | OmniVoice | Fish S2 Pro |
|---|---|---|---|---|
| Architektur | Eingefrorenes LLM + DiT | Tokenizer-freie Diffusion-AR | Attention-basiert | Dual-AR + RLHF |
| Parameter | ca. 8–14B | 2B | Nicht angegeben | 4,4B |
| Sprachen | 5 | 30+ | 600+ | 80+ |
| Russisch | Nein | Ja | Ja | Ja |
| Stimmklonen | Zero-shot | Zero-shot + Fine-Tuning | Zero-shot sprachübergreifend | 10–30 s Referenz |
| Bearbeitung auf Wortebene | **Ja** | Nein | Nein | Nein |
| Audioverständnis | **Ja** | Nein | Nein | Nein |
| Fine-Tuning / LoRA | Kein Rezept | Ja | Unklar | Ja |
| Lizenz | CC-BY-NC-4.0 | Apache 2.0 | Offen | Offene Gewichte |
| Kommerzielle Nutzung | Nein (ohne Vereinbarung) | Ja | Ja | Ja |

Audio-Omni tauscht Sprachabdeckung und kommerzielle Nutzbarkeit gegen Breite der Funktionen. Spezialisierte TTS-Modelle sind bei der TTS-Qualität für einzelne Sprachen und bei der Mehrsprachigkeit überlegen.

## Architekturmuster: Eingefrorenes Schlussfolgern + trainierbare Synthese {#architectural-pattern-frozen-reasoning-trainable-synthesis}

Dieses Designmuster, bei dem ein gemeinsames eingefrorenes LLM als Schlussfolgerungsbasis über einem trainierbaren Synthesemodul dient, lässt sich über dieses Modell hinaus verallgemeinern:

- Neue Aufgaben = neue Prompts an das eingefrorene LLM, kein Neutraining
- Schlussfolgern und Generieren können unabhängig voneinander aktualisiert werden
- Das eingefrorene LLM liefert fundiertes didaktisches Feedback (z. B. Erklärung von Fehlern auf Phonemebene bei Sprache)

**Alternativen zur Implementierung der Sprachbearbeitung auf Wortebene** (für kommerziell lizenzierte Systeme):
1. Diffusionsbasiertes Inpainting mit einem Prompt (erfordert eine Diffusionsarchitektur wie VoxCPM2)
2. Phonemausrichtung + AudioSep-Extraktion → TTS-Inpainting in der Zielstimme → erneutes Einfügen
3. Training eines Bearbeitungs-LoRA auf einer kommerziell offenen Basis mit dem AudioEdit-Datensatz (falls veröffentlicht)

## Einheitliches API-Muster {#unified-api-pattern}

```python
# Demonstrates clean interface separation between tasks
model.understand("transcribe", audio_path)          # understanding
model.generate("tts", text="Hello world", ref=ref_audio)  # generation
model.edit("Add", audio_path, desc="rain sounds")  # editing
```

Dieses API-Design mit drei Namensräumen (verstehen / generieren / bearbeiten) trennt die Absichten sauber und lohnt sich für die Nachbildung in Audio-Worker-Diensten.

## Stolperfallen {#gotchas}

- **Problem:** Der 21-GB-Checkpoint benötigt für die Inferenz mindestens 24 GB VRAM → **Lösung:** A100 80GB oder H100 verwenden; Consumer-Karten mit 24 GB (RTX 4090/3090) stoßen an die absolute Grenze und haben keinen Spielraum für Batching
- **Problem:** CC-BY-NC-4.0 schließt die kommerzielle Nutzung aus → **Lösung:** Die Autoren wegen einer kommerziellen Lizenz kontaktieren (`ztianad@connect.ust.hk`); für kommerzielle Produktivsysteme Apache-2.0-Alternativen verwenden (VoxCPM2, Fish S2 Pro)
- **Problem:** Keine Unterstützung für Russisch, obwohl Alternativen mit 600 Sprachen existieren → **Lösung:** Für russischsprachige Produktivsysteme OmniVoice (600+ Sprachen) oder Fish S2 Pro mit Fine-Tuning verwenden
- **Problem:** Kein LoRA- / Fine-Tuning-Rezept bereitgestellt → **Lösung:** Anpassung an eigene Stimmen oder Domänen ist nur mit einer eigenen Trainingspipeline möglich; spezialisierte Modelle (Fish S2 Pro, VoxCPM2) bieten dokumentierte Fine-Tuning-Wege

## Siehe auch {#see-also}

- [[tts-models]]
- [[voice-cloning]]
- [[voice-conversion]]
