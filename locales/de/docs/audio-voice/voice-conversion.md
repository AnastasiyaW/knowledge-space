---
title: "Stimmkonvertierung"
category: techniques
tags: [voice-conversion, real-time, rvc, so-vits, singing-voice, speaker-identity]
level: 3
source_sha256: 4225d0ff96ffc6c342d20aecedb98621aa6ab89fe7a0664239e9d7a0c481b923
translation: machine
translated_at: '2026-10-24'
---
Hold on, I need to correct my output: the above is not a translation. Let me redo it properly.

---
title: Stimmkonvertierung
category: techniques
tags: [voice-conversion, real-time, rvc, so-vits, singing-voice, speaker-identity]
---

# Stimmkonvertierung {#voice-conversion}

Stimmkonvertierung (Voice Conversion, VC) verändert die Sprecheridentität in vorhandenem Audio und bewahrt dabei den sprachlichen Inhalt, die Prosodie und das Timing. Anders als Voice Cloning (das neue Sprache aus Text erzeugt) arbeitet VC auf bestehenden Aufnahmen - die Eingabe ist Audio, nicht Text.

## Wichtige Fakten {#key-facts}

- Stimmkonvertierung arbeitet auf vorhandenem Audio: Eingabesprache -> Ausgabesprache mit anderer Stimmidentität
- Zentraler Unterschied zum TTS-Cloning: VC bewahrt das ursprüngliche Timing, die Intonation und die Emotion
- RVC (Retrieval-based Voice Conversion) ist der dominierende Open-Source-Ansatz, basierend auf VITS und Retrieval
- Echtzeit-VC mit weniger als 20 ms Latenz auf einer GPU ist erreichbar und ermöglicht Live-Stimmveränderung
- Singstimmkonvertierung (SVC) ist eine wichtige Anwendung - die Stimme eines beliebigen Sängers auf eine Aufnahme anwenden
- VC-Modelle benötigen typischerweise 10-30 Minuten Trainingsdaten der Zielstimme

## Architektur {#architecture}

### RVC (Retrieval-based Voice Conversion) {#rvc-retrieval-based-voice-conversion}

```text
RVC pipeline:
  Input audio
    -> Pitch extraction (RMVPE / CREPE / Harvest)
    -> Content encoder (HuBERT / ContentVec) -> content features
    -> FAISS index retrieval -> find similar features from target speaker
    -> Blend retrieved features with encoder output (index_rate: 0.0-1.0)
    -> VITS decoder (conditioned on target speaker embedding)
    -> Pitch-shifted, voice-converted output
    
Training: 10-30 min of target speaker audio, ~20 min on GPU
Inference: real-time capable on modern GPU
```

### SO-VITS-SVC {#so-vits-svc}

Speziell für die Singstimmkonvertierung entwickelt.

```text
SO-VITS-SVC pipeline:
  Input singing audio
    -> Content encoder (ContentVec)
    -> F0 (pitch) extraction and explicit pitch curve
    -> VITS decoder with speaker conditioning
    -> Output: same melody, different voice
    
Key difference from RVC: explicit pitch modeling makes it
better for singing where pitch accuracy is critical.
Training: 1-4 hours of target singer audio recommended.
```

## Echtzeit-Stimmkonvertierung {#real-time-voice-conversion}

```text
Requirements for real-time VC (<50ms latency):
  - GPU: RTX 3060+ for comfortable real-time
  - Buffer size: 128-512 samples (3-11ms at 44.1kHz)
  - Lookahead: minimal (adds latency but improves quality)
  - Model: RVC with ONNX export or TensorRT optimization
  
Practical latency breakdown:
  Audio capture:     ~5ms (WASAPI/ASIO)
  Feature extraction: ~3ms (HuBERT on GPU)
  Conversion:        ~5ms (VITS decoder on GPU)
  Audio output:      ~5ms (WASAPI/ASIO)
  Total:             ~18ms (imperceptible)
```

### Streaming-Pipeline {#streaming-pipeline}

```python
# Conceptual real-time VC pipeline
import sounddevice as sd
import numpy as np

BLOCK_SIZE = 512  # ~11ms at 44.1kHz
SAMPLE_RATE = 44100

def callback(indata, outdata, frames, time, status):
    # indata: captured microphone audio
    audio_chunk = indata[:, 0]
    
    # Extract content features (HuBERT)
    features = content_encoder(audio_chunk)
    
    # Extract pitch (RMVPE)
    f0 = pitch_extractor(audio_chunk)
    
    # Convert voice identity
    converted = vits_decoder(features, f0, target_speaker_embedding)
    
    outdata[:, 0] = converted

stream = sd.Stream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    channels=1,
    callback=callback
)
```

## Stimmkonvertierung vs. Voice Cloning {#voice-conversion-vs-voice-cloning}

| Aspekt | Voice Conversion | Voice Cloning (TTS) |
|--------|-----------------|-------------------|
| Eingabe | Audioaufnahme | Text |
| Erhält | Timing, Prosodie, Emotion | Nichts (wird von Grund auf erzeugt) |
| Ausgabe-Timing | Wie Eingabe | Vom Modell bestimmt |
| Anwendungsfall | Sprecher in vorhandenem Audio ändern | Neue Sprache erzeugen |
| Trainingsdaten | 10-30 Min. Zielsprecher | 5 Sek. (Zero-Shot) bis Stunden |
| Echtzeit | Ja (mit Optimierung) | Modellabhängig |
| Gesang | Exzellent (SVC-Modelle) | Schlecht (TTS-Modelle können nicht gut singen) |

## Training eines VC-Modells {#training-a-vc-model}

```text
RVC training workflow:
  1. Collect 10-30 min of clean target speaker audio
  2. Preprocess: denoise, normalize, segment into 5-15s clips
  3. Extract features: HuBERT content features + pitch (F0)
  4. Build FAISS index from target speaker features
  5. Train VITS decoder: 200-500 epochs, ~20 min on RTX 3090
  6. Test: convert a sample, check for artifacts
  
Quality tips:
  - More diverse training data (different emotions, speeds) = better model
  - Clean audio matters more than quantity
  - Pitch extraction method: RMVPE > CREPE > Harvest (quality vs speed)
```

## Anwendungen {#applications}

- **Gesang**: Die Klangfarbe eines beliebigen Sängers auf eigene Aufnahmen anwenden
- **Synchronisation**: Die Identität des Synchronsprechers ersetzen und dabei das Timing der Originalperformance beibehalten
- **Datenschutz**: Die Sprecheridentität in Aufnahmen anonymisieren
- **Barrierefreiheit**: Sprache in eine Stimme umwandeln, die der Zuhörer leichter versteht
- **Livestreaming**: Echtzeit-Stimmveränderung für Content-Creator

## Stolpersteine {#gotchas}

- **Tonhöhenbereich-Unterschiede verursachen Artefakte** - die Umwandlung einer tiefen männlichen Stimme in eine hohe weibliche (oder umgekehrt) erzeugt Schwanken und roboterhafte Artefakte an den Tonhöhenextremen. Halte Quelle und Ziel innerhalb einer Oktave, oder verwende explizite Tonhöhenverschiebung als Vorverarbeitungsschritt
- **RVC index_rate ist ein kritischer, aber schlecht dokumentierter Parameter** - bei 0.0 wird kein Retrieval verwendet (reine Encoder-Ausgabe, weniger ähnlich zum Ziel). Bei 1.0 volles Retrieval (ähnlicher zum Ziel, kann aber abgehackt klingen). Der optimale Bereich liegt typischerweise bei 0.3-0.6, je nachdem, wie unterschiedlich Quell- und Zielstimme sind
- **Hintergrundmusik schlägt bei der Konvertierung durch** - VC-Modelle werden auf sauberer Sprache trainiert. Musik oder Rauschen im Eingangssignal bleibt unverändert oder erzeugt Artefakte. Trenne die Gesangsspur immer zuerst (Demucs/UVR5), konvertiere und mische dann neu ab

## Siehe auch {#see-also}

- [[voice-cloning]] - auf Text-to-Speech basierendes Voice Cloning, komplementärer Ansatz
- [[tts-models]] - TTS-Architekturen, die Komponenten mit VC teilen (VITS, HuBERT)
- [[audio-generation]] - Musikgenerierung, relevant für SVC-Anwendungen
