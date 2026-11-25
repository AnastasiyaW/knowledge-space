---
title: "Voice Design und Voice Mixing"
description: "Erzeugung einzigartiger synthetischer Stimmen aus Textbeschreibungen, Voice Morphing, Natürlichkeits-Benchmarks und sprachübergreifende Stimmidentität. Behandelt Qwen3-TTS VoiceDesign, VoxMorph, Cartesia-Embeddings und MOS-Werte."
level: 3
source_sha256: 6badd9d592af5fe7da3fe73f303a128082b85f39ab7f645301dd3126c4da6fa4
translation: machine
translated_at: '2026-10-24'
---
# Voice Design und Voice Mixing {#voice-design-and-voice-mixing}

Erzeugung einer synthetischen Stimmidentität, ohne eine bestimmte Person zu klonen. Es gibt zwei Ansätze: Voice Design auf Basis von Textbeschreibungen und Voice Mixing (Interpolation zwischen bestehenden Stimm-Embeddings). Stand 2026 unterstützen mehrere Open-Source-Modelle Voice Design; der Qualitätsabstand zu kommerziellen APIs hat sich auf 0,1–0,2 MOS verringert.

## Voice Design aus Textbeschreibungen {#voice-design-from-text-descriptions}

### Qwen3-TTS VoiceDesign {#qwen3-tts-voicedesign}

Steuerung über den Parameter `instruct`. 7 steuerbare Dimensionen: Geschlecht, Alter (konkrete Jahre), Tonhöhe, Sprechtempo, emotionale Färbung, Klangcharakteristik, Szenario.

```python
# Example prompt (15-40 words optimal)
voice_description = """
A young adult woman, around 25 years old. Low-pitched voice with a 
deliberate, steady pace. Calm and professional tone, suitable for 
audiobook narration.
"""
```

**5 Prinzipien:**
1. Sei konkret („tief, klar, schnelles Tempo“ statt „schöne Stimme“)
2. Nutze mehrere Dimensionen gleichzeitig
3. Sei objektiv (physikalische Eigenschaften, keine Gefühle)
4. Sei originell (keine Nachahmung von Prominenten)
5. Optimaler Bereich: 15–40 Wörter, informationsdicht

**NICHT steuerbar**: Akzent (erfordert bei den meisten Modellen Referenzaudio).

### OmniVoice (strukturierte Attributsteuerung) {#omnivoice-structured-attribute-control}

```text
Attributes (one per category, freely combinable):
  Gender:  male / female
  Age:     child / teenager / young adult / middle-aged / elderly
  Pitch:   very low / low / medium / high / very high
  Style:   normal / whisper
  EN accent: american / british / australian / indian / chinese /
              canadian / korean / portuguese / russian / japanese
  CN dialect: Sichuan / Shaanxi / Henan / ... (regional)
```

Besonderheit: **Akzentauswahl** in Textform – die meisten Modelle benötigen für den Akzent Referenzaudio.

### VoxCPM2 (tokenizerfrei, April 2026) {#voxcpm2-tokenizer-free-april-2026}

Textbasiertes Voice Design mit einer tokenizerfreien Diffusions-AR-Architektur. Vermeidet Quantisierungsartefakte, die durch Codec-Tokenisierung entstehen, und bewahrt prosodische Feinheiten. Native Ausgabe mit 48 kHz, über 30 Sprachen, Apache 2.0.

### Parler-TTS {#parler-tts}

Freie Textbeschreibung, überhaupt keine Referenzaudiodaten erforderlich. Weniger präzise als strukturierte Steuerung, benötigt aber keinerlei Audio-Assets.

```python
# parler-tts usage
description = "a warm female voice with slight British accent, speaking slowly and clearly"
input_ids = tokenizer(description, return_tensors="pt").input_ids
prompt_ids = tokenizer(text, return_tensors="pt").input_ids
generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_ids)
```

## Voice Mixing / Blending {#voice-mixing-blending}

### Cartesia Sonic (Produktions-API) {#cartesia-sonic-production-api}

192-dimensionale Stimm-Embeddings. Lineare Interpolation über die API oder den Playground.

```python
# Voice mixing via Cartesia API
new_voice = w1 * voice_a_embedding + w2 * voice_b_embedding
# Note: perception is non-linear - 50/50 mix may need non-equal weights
# Use prototype embeddings to add speed/emotion characteristics
```

**MOS 4,7** (Sonic 2), ca. 90 ms TTFB. Nur kommerziell verfügbar.

### VoxMorph (Forschung, ICASSP 2026) {#voxmorph-research-icassp-2026}

Zerlegt die Stimme in ein **Prosodie-Embedding** (Rhythmus, Tonhöhe) und ein **Timbre-Embedding** (Vokaltrakt, Formanten). Beide werden unabhängig voneinander mithilfe von **Slerp** (sphärische lineare Interpolation) gemischt.

```text
Method:
  speaker_a (5 sec) -> prosody_embedding, timbre_embedding
  speaker_b (5 sec) -> prosody_embedding, timbre_embedding
  
  Slerp on hypersphere:
  new_voice = Slerp(timbre_a, timbre_b, α) + Slerp(prosody_a, prosody_b, β)
  
  Result: voice texture of speaker A + speaking style of speaker B
```

Zero-Shot (kein Nachtraining). 2,6-fache Qualitätsverbesserung gegenüber früheren Methoden, 73 % weniger Verständlichkeitsfehler. `github.com/Bharath-K3/VoxMorph`

### INSIDE-Methode (APSIPA 2025) {#inside-method-apsipa-2025}

Erzeugt neuartige Sprecheridentitäten, die im Embedding-Raum die Lücken zwischen realen Sprechern „füllen“.

```text
Select nearby speaker pairs → compute Slerp intermediates
→ novel identity between them
+5.24% speaker verification improvement
+13.44% gender classification gain
```

### Slerp vs. lineare Interpolation {#slerp-vs-linear-interpolation}

**Bei Stimm-Embeddings immer Slerp bevorzugen.** Die lineare Interpolation hochdimensionaler Vektoren verändert deren Betrag, was Artefakte verursacht. Slerp bewegt sich entlang der Oberfläche der Hypersphäre:

```python
import numpy as np

def slerp(v0, v1, t):
    """Spherical linear interpolation."""
    dot = np.clip(np.dot(v0, v1), -1.0, 1.0)
    theta = np.arccos(dot) * t
    relative = v1 - v0 * dot
    relative /= np.linalg.norm(relative)
    return v0 * np.cos(theta) + relative * np.sin(theta)
```

## Was Stimmen unnatürlich klingen lässt {#what-makes-voices-unnatural}

| Problem | Ursache | Beste Lösungen |
|---------|---------|---------------|
| Flache Prosodie / Monotonie | TTS „mittelt“ die Tonhöhenvariation | Sesame CSM (kontextbewusst), Fish S2 (15K+ Tags), Orpheus |
| Fehlende Mikropausen | Gleichmäßiger Wortabstand | VoxCPM2 (tokenizerfreies Timing), Sesame CSM |
| Keine Atmung | TTS lässt Einatmungspausen weg | Orpheus (`<sigh>`-Tags), Chatterbox (`[cough]`, `[laugh]`) |
| Emotionale Flachheit | Prosodie ignoriert die Bedeutung | Fish S2 Pro (Sub-Wort-Tags), IndexTTS-2.5 (8D-Emotionsvektor) |
| Fehlendes Kontextverständnis | Kein Verständnis des WARUM | Sesame CSM (Modellierung des Gesprächskontexts) |
| Komprimierter Tonhöhenumfang | Enger als beim Menschen | VoxCPM2 (48 kHz, kein Verlust durch Tokenisierung) |

**Workaround-Techniken:**
- Kommas, Auslassungspunkte und Markierungen für Mikropausen einfügen, um die Prosodie zu steuern
- SSML oder modellspezifische Tags für Betonung, Pausen und Atmung verwenden
- Gesprächskontext bereitstellen (Sesame CSM)
- RL-Alignment-Nachtraining: Fish S2, CosyVoice 3

## Natürlichkeits-Benchmarks (MOS, 2026) {#naturalness-benchmarks-mos-2026}

| Modell | MOS | Methode |
|--------|-----|---------|
| Sesame CSM | 4,7 | CMOS (Expresso-Datensatz), kontextbewusst |
| Cartesia Sonic 2 | 4,7 | Branchen-Benchmark |
| Orpheus TTS | 4,6 | Berichtet |
| Fish Audio S2 Pro (EN) | 4,50 Ausdruckskraft | Interne Bewertung |
| Fish Audio S2 Pro (CN) | 4,94 Ausdruckskraft | Interne Bewertung, stärkstes Ergebnis für Chinesisch |
| Menschliche Sprache (Referenz) | 4,5–4,8 | Abhängig von der Aufnahme |

**Schrumpfender Qualitätsabstand**: 2023 lag das beste Open-Source-Modell etwa 1,0 MOS hinter ElevenLabs. 2026 beträgt der Abstand 0,1–0,2 MOS. Mehrere Open-Source-Modelle erreichen oder übertreffen ElevenLabs inzwischen.

**Gewinnraten bei menschlicher Präferenz:**
- Fish S2 Pro: Platz 1 in der TTS Arena (Bradley-Terry 3,07)
- Voxtral 4B: 68,4 % gegenüber ElevenLabs Flash v2.5 (Blindtest)
- Chatterbox-Turbo: 63,75 % Präferenz gegenüber ElevenLabs

## Steuerbare Stimmmerkmale nach Modell {#controllable-voice-characteristics-by-model}

| Merkmal | Qwen3-TTS | OmniVoice | VoxCPM2 | Fish S2 |
|---------|-----------|-----------|---------|---------|
| Geschlecht | Ja | Ja | Ja | Über Referenzaudio |
| Alter (konkrete Jahre) | Ja | 5 Kategorien | Ja | Über Referenzaudio |
| Tonhöhe | Ja | 5 Stufen | Ja | Über Tags |
| Sprechtempo | Ja | Nein | Ja | Über Tags |
| Emotion | Ja | Nein | Ja | 15K+ Tags |
| Akzent | **Nein** | EN-Akzente + CN-Dialekte | Unbekannt | Über Referenzaudio |
| Flüstern | Unbekannt | Ja | Unbekannt | `[whisper]` |
| Atmung/Lachen | Nein | Nein | Nein | Teilweise |

## Sprachübergreifende Stimmidentität {#cross-language-voice-identity}

Beibehaltung derselben Stimmidentität über mehrere Sprachen hinweg:

```text
Workflow:
  1. Create voice in English first (most training data, strongest base)
  2. Test same description/embedding in target language (RU, CN)
  3. If inconsistent: Voxtral 4B for cross-lingual identity preservation
     (preserves accent, inflection, intonation across language switch)
```

**Für RU+CN+EN**: Qwen3-TTS ist das einzige Modell, das Voice Design, alle drei Sprachen und wettbewerbsfähige Qualität vereint.

## Stolperfallen {#gotchas}

- **Ein Akzent lässt sich bei den meisten Modellen nicht aus Text gestalten.** Nur OmniVoice bietet eine strukturierte Akzentauswahl. Bei allen anderen Modellen den Akzent über Referenzaudio einer Muttersprachlerin bzw. eines Muttersprachlers mit dem gewünschten Akzent erfassen
- **Die Wahrnehmung der Mischgewichte ist nicht linear.** Eine 50/50-Mischung zweier Stimmen klingt selten nach „je 50 %“ – sie kann eher zu 80 % wie eine der beiden Stimmen klingen. Gewichte iterativ und perzeptiv anpassen, nicht rein rechnerisch
- **Kurze Textbeschreibungen verlieren an Präzision.** Beschreibungen mit weniger als 10 Wörtern erzeugen generische Stimmen. Unter 15 Wörtern dominieren die Modell-Standardwerte. Verwende 15–40 Wörter und lege mehrere Dimensionen fest (Alter + Tonhöhe + Tempo + emotionale Färbung)
- **Voice Design ist über Inferenzläufe hinweg nicht stabil.** Anders als beim Voice Cloning (deterministisch bei gleicher Referenz) variieren textbeschriebene Stimmen zwischen den Generierungen. Wenn Reproduzierbarkeit wichtig ist, den exakten Prompt UND die Generierungsparameter speichern

## Siehe auch {#see-also}

- [[tts-models]] - Modellvergleich einschließlich der Voice-Design-Fähigkeiten
- [[voice-cloning]] - Klonen aus Referenzaudio
- [[voice-agent-pipelines]] - Integration von TTS in Echtzeit-Sprachsysteme
- [[speech-recognition]] - ASR-Modelle für die Bewertung (WER-Messung)
