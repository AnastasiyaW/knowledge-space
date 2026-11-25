---
title: "Stimmklonen"
category: techniques
tags: [voice-cloning, speaker-embedding, cross-lingual, zero-shot, safety, tts]
level: 3
source_sha256: 289bf673aa4ea644549c41361b9431355b10485bc7c450d1cd0a4c73cb51a704
translation: machine
translated_at: '2026-10-24'
---
# Stimmklonen {#voice-cloning}

Stimmklonen reproduziert die Stimmmerkmale eines Zielsprechers (Klangfarbe, Tonhöhe, Rhythmus) anhand eines Referenz-Audiosamples. Moderne Zero-Shot-Ansätze benötigen nur 5–30 Sekunden sauberes Audio und machen damit Stunden an Trainingsdaten pro Sprecher überflüssig.

## Kernfakten {#key-facts}

- Zero-Shot-Klonen extrahiert ein Sprecher-Embedding aus dem Referenz-Audio und konditioniert die TTS-Generierung darauf
- Sprecher-Embeddings sind typischerweise 256–512-dimensionale Vektoren aus Modellen wie ECAPA-TDNN, WavLM oder Resemblyzer
- Cross-linguales Klonen bewahrt die Stimmidentität, während Sprache in einer Sprache erzeugt wird, die der Sprecher nie aufgenommen hat
- Fine-Tuned-Klonen (Sprecheradaption) liefert höhere Qualität, erfordert aber 1–5 Stunden Zielaudio und GPU-Training
- Die Qualität hängt stark ab von: Sauberkeit des Referenz-Audios, Aufnahmebedingungen, Konsistenz des Sprechers in der Referenz

## Ansätze {#approaches}

### Zero-Shot (ohne Training) {#zero-shot-no-training}

Sprecher-Embedding aus der Referenz extrahieren und in den TTS-Decoder einspeisen. Kein Fine-Tuning erforderlich.

```text
Reference audio (5-30 sec)
  -> Speaker encoder (ECAPA-TDNN / WavLM)
  -> Speaker embedding (256-512 dim vector)
  -> TTS decoder conditioned on embedding + text
  -> Generated speech in target voice
```

**Modelle mit Unterstützung für Zero-Shot-Klonen:**
- LEMAS-TTS, F5-TTS, CosyVoice 2 (Flow Matching)
- XTTS v2, VoxCPM2, Fish Speech (autoregressiv)
- OmniVoice – über 600 Sprachen, Tag-Steuerung für Emotionen

### Sprecheradaption (Fine-Tuning) {#speaker-adaptation-fine-tuning}

Ein Basis-TTS-Modell auf Daten des Zielsprechers feinabstimmen. Höhere Qualität, erfordert aber Rechenleistung.

```text
Base TTS model + 1-5 hours of target speaker audio
  -> Fine-tune decoder layers (freeze encoder)
  -> Speaker-specific model checkpoint
  -> Generate with text input only (no reference needed at inference)
```

Typischerweise 500–2000 Trainingsschritte, 10–30 Minuten auf einer einzelnen GPU.

### Stimmgestaltung (textbasiert) {#voice-design-text-described}

Mehrere Modelle erlauben inzwischen die Erzeugung einer Stimme aus einer Textbeschreibung statt aus einer Audioreferenz.

```text
VoxCPM2 voice design:
  "A warm, deep male voice with slight British accent, age 40-50"
  -> Voice design module (built into tokenizer-free pipeline)
  -> Synthetic speaker embedding
  -> TTS generation at 48kHz studio quality

OmniVoice attribute-based design:
  Attributes: gender=male, age=40-50, pitch=low, dialect=british, style=warm
  -> Parametric attribute control (not free-text)
  -> Can specify: whisper, shouting, specific dialect
  -> Works across 600+ languages
```

**Vergleich:**
- VoxCPM2: Freitext-Beschreibung, flexibler, 30+ Sprachen
- OmniVoice: attributbasiert, vorhersagbarere Ergebnisse, über 600 Sprachen

## Cross-lingual Klonen {#cross-lingual-cloning}

Die Stimmidentität des Sprechers wird auf Sprachen übertragen, die er nie gesprochen hat. Die Qualität variiert mit der sprachlichen Distanz.

```text
Quality hierarchy for cross-lingual transfer:
  Same language family (EN -> DE):     High quality
  Same script (EN -> FR):              Good quality  
  Different family (EN -> ZH):         Moderate quality
  Low-resource target (EN -> Swahili): Lower quality
```

**Zentrale Herausforderung:** Prosodiemuster sind sprachspezifisch. Ein geklonter englischer Sprecher, der Mandarin spricht, kann im Rhythmus fremd klingen, selbst wenn die Klangfarbe perfekt ist. VoxCPM2 und OmniVoice optimieren gezielt dafür.

**Klonen aus minimaler Referenz (Stand der Technik 2026):**

| Modell | Min. Referenz | Sprachen | Cross-lingual | Hinweise |
|--------|--------------|----------|---------------|----------|
| OmniVoice | Wenige Sekunden | 600+ | Ja, Zero-Shot | Robuste Verarbeitung verrauschter Eingaben |
| VoxCPM2 | Kurzer Clip | 30+ | Ja | Diffusion-AR erhält Emotion |
| Voxtral 4B | 3 Sekunden | 9 | Eingeschränkt | Erfasst Akzent und Disfluenzen |
| Qwen3.5-Omni | Voice-Upload | 36 TTS | Ja, 20 Sprachen getestet | WER 1,87 über Sprachen, Kosinus-Ähnlichkeit 0,79 |

Qwen3.5-Omni erreicht die beste gemessene Klon-Treue (WER 1,87 über 20 Sprachen), ist aber nur über eine API verfügbar.

## Emotions- und Stilsteuerung {#emotion-and-style-control}

Moderne Klonmodelle unterstützen tag-basierte Emotionsinjektion:

```text
Tag-controlled generation (OmniVoice, Orpheus):
  Input: "I can't believe it! [surprise] This is amazing [joy]"
  Tags: [laugh], [surprise], [sadness], [whisper], [shouting]
  
  The model generates speech with corresponding emotional inflection
  at tagged positions, while maintaining target speaker's voice identity.
```

## Vorbereitung des Referenz-Audios {#reference-audio-preparation}

```text
Optimal reference characteristics:
  Duration:    10-30 seconds (sweet spot for most models)
  Content:     Natural speech, varied intonation, no music/effects
  Quality:     Clean recording, low noise floor, no reverb
  Format:      WAV 16-bit, 24kHz+ sample rate, mono
  Speaker:     Single speaker, consistent voice (no whispering then shouting)

Preprocessing pipeline:
  1. Source separation (UVR5 / Demucs) - remove background music
  2. Noise reduction (DeepFilterNet / RNNoise) - reduce ambient noise
  3. Trim silence (ffmpeg silenceremove) - remove dead air
  4. Normalize loudness (ffmpeg loudnorm) - consistent level
  5. Resample to model's expected rate (usually 24kHz)
```

## Stimmmischung: Erzeugung neuer Stimmidentitäten {#voice-mixing-creating-novel-voice-identities}

Moderne TTS-Modelle stellen Sprecher-Embeddings als Vektoren bereit. Das Mischen von Embeddings erzeugt Stimmen, die keiner realen Person entsprechen.

### Lineare Interpolation (Cartesia Sonic) {#linear-interpolation-cartesia-sonic}

Cartesia Sonic verwendet 192-dimensionale Sprecher-Embeddings (Floats von -1 bis 1):

```python
import numpy as np

def mix_voices(embedding_a: np.ndarray, embedding_b: np.ndarray, 
               weight_a: float = 0.5) -> np.ndarray:
    """Linear interpolation between two speaker embeddings."""
    weight_b = 1.0 - weight_a
    return weight_a * embedding_a + weight_b * embedding_b

# Via Cartesia API:
import requests

new_voice = requests.post("https://api.cartesia.ai/voices", json={
    "name": "Custom Mix",
    "embedding": mix_voices(voice_a_embedding, voice_b_embedding, 0.6).tolist()
}).json()
```

**Warnung:** Die Wahrnehmung ändert sich bei der Interpolation nicht linear mit dem Koeffizienten. Eine 50/50-Mischung erfordert unter Umständen ungleiche Gewichte (z. B. 0,7/0,3), um wahrnehmbar ausgewogene Ergebnisse zu erzielen. Prototyp-Embeddings (Geschwindigkeits- und Emotionsregler) helfen, Eigenschaften feinabzustimmen.

### Sphärische lineare Interpolation (Slerp) – Forschungsmethode {#spherical-linear-interpolation-slerp-research-method}

Slerp erhält die Vektorlänge auf der hochdimensionalen Hypersphäre und minimiert dadurch Artefakte im Vergleich zur linearen Interpolation. Verwendet in VoxMorph (ICASSP 2026):

```python
def slerp(a: np.ndarray, b: np.ndarray, t: float) -> np.ndarray:
    """Spherical linear interpolation between two embedding vectors."""
    a_norm = a / np.linalg.norm(a)
    b_norm = b / np.linalg.norm(b)
    
    dot = np.clip(np.dot(a_norm, b_norm), -1.0, 1.0)
    theta = np.arccos(dot)
    
    if np.abs(theta) < 1e-6:
        return a  # vectors nearly identical
    
    return (np.sin((1 - t) * theta) * a + np.sin(t * theta) * b) / np.sin(theta)
```

**Vorteil von VoxMorph:** Trennt das Prosodie-Embedding (Rhythmus, Tonhöhe) vom Timbre-Embedding (Vokaltrakt, Formanten). Sprechstil von Sprecher A und Stimmcharakter von Sprecher B können unabhängig voneinander gemischt werden. Eingabe: 5 Sekunden pro Quellsprecher, Zero-Shot.

### INSIDE-Methode (Erzeugung neuartiger Identitäten) {#inside-method-novel-identity-generation}

Wählt Paare benachbarter Sprecher-Embeddings aus und berechnet Zwischenidentitäten per Slerp. Erzeugt Stimmen, die Lücken im Embedding-Raum zwischen realen Sprechern füllen. Validiert: +5,24 % Verbesserung bei der Sprecherverifikation, +13,44 % Gewinn bei der Geschlechtsklassifikation.

## Was synthetische Stimmen unnatürlich klingen lässt {#what-makes-synthetic-voices-sound-unnatural}

Die häufigsten Natürlichkeitsprobleme und die Modelle, die sie adressieren:

| Problem | Symptom | Beste Lösungen |
|---------|---------|---------------|
| Flache Prosodie | Monoton, unabhängig vom Inhalt | Sesame CSM (kontextbewusst), Fish S2 (15K+ Tags) |
| Fehlende Mikropausen | Gleichmäßiger Wortabstand | Sesame CSM (natürliche Fülllaute), VoxCPM2 (tokenizerfrei) |
| Fehlende Atmung | Keine Atemzüge zwischen Sätzen | Orpheus TTS (`<sigh>`, natürliche Atmung) |
| Emotionale Flachheit | Gleiche Intonation für Witz und Tragödie | Fish S2 Pro (Emotion auf Subwort-Ebene), IndexTTS-2.5 (8D-Vektor) |
| Komprimierter Tonhöhenumfang | Engerer Tonhöhenbereich als beim Menschen | VoxCPM2 48kHz (kein Verlust durch Tokenisierung), CosyVoice 3 (RL) |
| Kontextblindheit | Wörter werden gelesen, nicht verstanden | Sesame CSM (Modellierung des Gesprächskontexts) |
| Roboterhafte Übergänge | „Zusammengesetzte" Wortgrenzen | RL-abgestimmte Modelle (Fish S2, CosyVoice 3) |

**Praktische Workarounds:**
- Kommas, Auslassungspunkte und Mikropausen-Marker einfügen, um die Prosodie zu steuern
- Modellspezifische Tags verwenden (`[laugh]`, `[excited]`, `[whisper]`) für den Ausdruck
- Gesprächsverlauf für kontextbewusste Modelle bereitstellen (Sesame CSM)
- RL-Nachtraining verbessert die Natürlichkeit ohne Architekturänderungen

## Natürlichkeits-Benchmarks (2026) {#naturalness-benchmarks-2026}

| Modell | MOS | Win Rate | Hinweise |
|--------|-----|----------|----------|
| Sesame CSM | 4,7 | nahezu menschlich (ohne Kontext) | nur Englisch |
| Cartesia Sonic 2 | 4,7 | — | ~90 ms TTFB |
| Orpheus TTS | 4,6 | — | Basierend auf Llama-3B |
| Fish S2 Pro (EN) | 4,50 exp / 4,21 nat | Bradley-Terry 3,07 #1 | gegenüber allen großen Wettbewerbern |
| Fish S2 Pro (ZH) | 4,94 exp / 4,40 nat | — | Stärkstes Ergebnis auf Chinesisch |
| Menschliche Sprache | ~4,5–4,8 | Referenz | variiert je nach Aufnahme |

**Zentraler Trend:** Der Qualitätsabstand zwischen den besten Open-Source- und kommerziellen TTS-Modellen schrumpfte von ~1,0 MOS (2023) auf 0,1–0,2 MOS (2026). Fish S2 Pro schlägt gpt-4o-mini-tts auf EmergentTTS-Eval (81,88 % Win Rate). Voxtral schlägt ElevenLabs Flash v2.5 in Blindtests.

## Sicherheit und Ethik {#safety-and-ethics}

- **Einwilligung**: Stimmklonen ohne Einwilligung des Sprechers ist in vielen Rechtsordnungen illegal
- **Deepfake-Erkennung**: Generierte Sprache lässt sich durch Spektralanalyse, Wasserzeichen (AudioSeal von Meta) oder Artefakterkennung identifizieren
- **Wasserzeichen**: Einige Modelle (LEMAS, CosyVoice) betten nicht hörbare Wasserzeichen in das erzeugte Audio ein
- **Ratenbegrenzung**: Produktivsysteme sollten Klonanfragen pro Nutzer bzw. API-Schlüssel begrenzen
- **Sprecherverifikation**: Klon-APIs mit Sprecherverifikation kombinieren, um zu bestätigen, dass der Hochladende der Stimmeigentümer ist

## Stolperfallen {#gotchas}

- **Kurze Referenzen versagen bei seltenen Phonemen** – ein 5-Sekunden-Clip enthält möglicherweise nicht genug phonetische Vielfalt. Das Modell erfindet fehlende Laute, teils inkonsistent. Verwenden Sie 15–30 Sekunden lange Referenzen mit abwechslungsreichem Inhalt. Ausnahme: Voxtral 4B ist gezielt für 3-Sekunden-Referenzen ausgelegt
- **Hintergrundrauschen aus der Referenz wird übernommen** – selbst geringe Raumhall- oder Klimaanlagengeräusche werden im Sprecher-Embedding kodiert und erscheinen in der gesamten generierten Sprache. Immer zuerst entrauschen. Ausnahme: OmniVoice verarbeitet verrauschte Referenzsamples explizit
- **Akzent-Übertragung bei Cross-lingual-Klonen** – ist das Referenz-Audio auf Englisch, hat generiertes chinesisches Sprechen oft einen englisch geprägten Rhythmus. Referenz-Audio in der Zielsprache (auch nur wenige Sekunden) verbessert die Ergebnisse deutlich
- **Reine API-Klonfunktion = Vendor-Lock-in** – Qwen3.5-Omni hat die beste gemessene Klonqualität, ist aber nur über eine API verfügbar. Für Produktivsysteme Ausweichpfade zu offenen Modellen (OmniVoice, VoxCPM2) einplanen

## Siehe auch {#see-also}

- [[tts-models]] – Modellarchitekturen und Vergleichstabelle
- [[voice-conversion]] – Änderung der Stimmidentität in bestehenden Aufnahmen
- [[speech-recognition]] – ASR für transkriptionsbasierte Ausrichtung in Klon-Pipelines
