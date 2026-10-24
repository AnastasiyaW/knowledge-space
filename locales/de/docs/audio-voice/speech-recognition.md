---
title: "Spracherkennung"
category: reference
tags: [asr, whisper, parakeet, qwen3-asr, streaming, transcription, multilingual, speech-to-text, edge-asr]
level: 4
source_sha256: 8d1ab5119e8fb8851aed2e004eca1ee32dce2be7ca11320783099c9d11c5b084
translation: machine
translated_at: '2026-10-24'
---
# Spracherkennung {#speech-recognition}

Automatische Spracherkennung (Automatic Speech Recognition, ASR) wandelt gesprochenes Audio in Text um. Stand Anfang 2026 hat das Feld die Dominanz von Whisper hinter sich gelassen: Qwen3-ASR, NVIDIA Canary-Qwen und Voxtral Realtime übertreffen Whisper bei Genauigkeit und/oder Geschwindigkeit deutlich. Whisper large-v3 bleibt eine verlässliche Baseline, wurde aber nicht aktualisiert.

## Kernfakten {#key-facts}

- **Qwen3-ASR** (Jan 2026) ist das neue Open-Source-SOTA für mehrsprachige ASR: 52 Sprachen, Apache 2.0, trainiert auf ~40 Mio. Stunden
- **MAI-Transcribe-1** (Apr 2026) ist das neue kommerzielle SOTA: 3,8 % WER auf den FLEURS-Top-25-Sprachen, proprietär
- Whisper large-v3 bleibt nutzbar, hat aber kein v4-Update erhalten; das Ökosystem ist über es hinweggegangen
- Streaming-ASR ist mit Voxtral Realtime (13 Sprachen) und Nemotron Speech (EN, <24 ms) produktionsreif
- Edge-ASR mit <1 GB RAM ist mit Moonshine v2 (27M Parameter, 50 ms) und Parakeet.cpp (reines C++) praktikabel
- SALM (Speech-Augmented Language Model) kombiniert ASR-Encoder und LLM-Decoder, sodass Transkription und Schlussfolgerung in einem Modell erfolgen

## Modellvergleich {#model-comparison}

| Modell | Architektur | Parameter | Sprachen | Streaming | Key WER | Stärke |
|--------|-------------|-----------|----------|-----------|---------|--------|
| Qwen3-ASR 1.7B | AuT + Qwen3 LLM | 1.7B | 52 | Ja (dynamisch) | TEDLIUM 4,50 | Bestes Open-Source-Modell für Mehrsprachigkeit |
| MAI-Transcribe-1 | Enc-Dec Transformer | ? | 25 | Nein | FLEURS 3,8 % | Beste kommerzielle Genauigkeit |
| Canary-Qwen 2.5B | FastConformer + Qwen3 | 2.5B | EN (+LLM) | Nein | LS-Clean 1,6 % | ASR + Zusammenfassung/QA |
| Voxtral Realtime 4B | LM + Encoder | 4B | 13 | Ja (80 ms–2,4 s) | Nahe Offline-Qualität | Konfigurierbare Latenz |
| Whisper large-v3 | Enc-Dec Transformer | 1.55B | 100+ | Nein | LS 2,7 % | Die meisten Sprachen, stabil |
| Parakeet-TDT-V3 | FastConformer-TDT | 0.6B | 25 EU | Ja | RTFx ~2000 | Schnellstes Open-Source-EN-ASR |
| Canary-1B-V2 | Multi-task CTC | 1B | 25 EU (inkl. RU) | Nein | 10x schneller als 3x größeres Modell | Übersetzung integriert |
| Nemotron Speech | Cache-Aware Conformer | 0.6B | EN | Ja (<24 ms) | 7,2–7,8 % | 560 Streams/H100 |
| Moonshine v2 Tiny | Ergodic Streaming Enc | 27M | EN | Ja (50 ms) | Auf Augenhöhe bei 6x Größe | Edge, <500 MB RAM |
| Fun-ASR-Nano | End-to-end | ? | 31 (Schwerpunkt Asien) | Ja | 93 % bei Rauschen | Chinesische Dialekte/Akzente |
| Whisper.cpp | GGML Whisper | 1.55B | 100+ | Chunked | ~3 % | CPU-/Edge-Deployment |

## Qwen3-ASR (empfohlen, Open Source, 2026) {#qwen3-asr-recommended-open-source-2026}

Stand Anfang 2026 das beste mehrsprachige Open-Source-ASR. Apache 2.0. Trainiert auf ~40 Mio. Stunden pseudo-gelabelter Daten.

```text
Architecture:
  AuT (Audio Transformer) encoder -> learned projector -> Qwen3 LLM decoder
  
  0.6B variant: AuT 180M params (hidden 896) + Qwen3 decoder
  1.7B variant: AuT 300M params (hidden 1024) + Qwen3 decoder

Key benchmarks (1.7B):
  TEDLIUM (EN): 4.50 WER  (vs GPT-4o 7.69, Whisper-lv3 6.84)
  WenetSpeech (ZH): 4.97  (vs GPT-4o 15.30, Whisper-lv3 9.86)
  Language ID (30 langs): 97.9% (vs Whisper-lv3 94.1%)

Streaming: dynamic flash attention, window 1s-8s
Latency (0.6B): 92ms TTFT, 2000x throughput at concurrency 128
Long audio: up to 20 minutes per pass
VRAM: ~2GB (0.6B), ~6GB (1.7B)
```

Außerdem veröffentlicht: Qwen3-ForcedAligner-0.6B für die Text-Sprache-Ausrichtung in 11 Sprachen.

## Whisper-Nutzung (Legacy-Baseline) {#whisper-usage-legacy-baseline}

### Einfache Transkription {#basic-transcription}

```python
import whisper

model = whisper.load_model("large-v3")
result = model.transcribe("audio.mp3", language="en")

print(result["text"])
for segment in result["segments"]:
    print(f"[{segment['start']:.1f}s - {segment['end']:.1f}s] {segment['text']}")
```

### Faster-Whisper (Produktion) {#faster-whisper-production}

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.mp3", beam_size=5, vad_filter=True)

print(f"Detected language: {info.language} ({info.language_probability:.2f})")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

### Zeitstempel auf Wortebene {#word-level-timestamps}

```python
# Faster-Whisper word timestamps
segments, _ = model.transcribe("audio.mp3", word_timestamps=True)
for segment in segments:
    for word in segment.words:
        print(f"  {word.start:.2f}s - {word.end:.2f}s: '{word.word}' (p={word.probability:.2f})")
```

## Streaming-ASR {#streaming-asr}

Stand 2026 ist natives Streaming-ASR in mehreren Sprachen produktionsreif.

```text
Native streaming models (recommended):
  1. Voxtral Realtime 4B - 13 languages (incl. EN/ZH/RU), configurable latency
     At 480ms: competitive with Whisper + ElevenLabs Scribe v2
     At 960ms: surpasses both
     At 2400ms: within 1% of offline quality
     Open-source, Apache 2.0, ~8-10GB VRAM

  2. Nemotron Speech Streaming 600M - English only, <24ms final transcripts
     Cache-Aware FastConformer-RNNT, chunk sizes 80-1120ms
     560 concurrent streams on single H100 at 320ms chunk
     3x throughput vs traditional buffered streaming

  3. Qwen3-ASR 0.6B - 52 languages, streaming via dynamic flash attention
     Window sizes 1s-8s, 92ms TTFT
     Best multilingual streaming option

  4. Moonshine v2 - 27M-medium params, edge streaming
     50ms (Tiny) to 258ms (Medium) latency
     <1GB memory, designed for edge processors

Legacy approaches (still valid for Whisper):
  5. Chunked Whisper - split into overlapping 30s chunks
     Latency: chunk_duration + inference (2-5 sec)
  
  6. VAD + Whisper - transcribe complete utterances
     Latency: utterance_end + inference
```

### Pipeline mit VAD-Unterstützung {#vad-assisted-pipeline}

```python
# Silero VAD + Faster-Whisper pipeline
import torch
from faster_whisper import WhisperModel

vad_model, utils = torch.hub.load('snakers4/silero-vad', 'silero_vad')
(get_speech_timestamps, _, read_audio, _, _) = utils

wav = read_audio('audio.wav', sampling_rate=16000)
speech_timestamps = get_speech_timestamps(wav, vad_model, sampling_rate=16000)
# Each timestamp = a speech segment to transcribe independently
```

## WhisperX – erweiterte Ausrichtung {#whisperx-enhanced-alignment}

WhisperX ergänzt eine erzwungene Phonem-Ausrichtung für präzise Wortgrenzen, die für Sprachbearbeitung und Untertitelerstellung unverzichtbar ist.

```text
WhisperX pipeline:
  1. Whisper transcription (batch mode for speed)
  2. VAD-based segmentation (cut on silence)
  3. Forced alignment via wav2vec2 / MMS alignment model
  4. Speaker diarization (optional, via pyannote)
  
Output: word-level timestamps with <50ms accuracy
```

## Auswahlhilfe für mehrsprachige ASR {#multilingual-asr-selection-guide}

Bestes Modell je Sprachkombination (Open Source, 2026):

| Ziel | Bestes Modell | Ausweichlösung | Anmerkungen |
|------|---------------|----------------|-------------|
| ZH + EN + RU | Qwen3-ASR 1.7B | Voxtral Realtime | Qwen3 hängt Whisper bei Chinesisch deutlich ab |
| Nur EN | Canary-Qwen 2.5B | Parakeet-TDT V3 | 1,6 % WER + LLM-Reasoning-Modus |
| EN-Streaming | Nemotron Speech | Voxtral Realtime | <24 ms, 560 Streams/H100 |
| Mehrsprachiges Streaming | Voxtral Realtime | Qwen3-ASR 0.6B | 13 Sprachen, konfigurierbare Latenz |
| Chinesische Dialekte | Fun-ASR-Nano | Qwen3-ASR | 7 Dialekte, 26 Akzente |
| Edge / Mobil | Moonshine v2 Tiny | Sherpa-ONNX | 27M Parameter, <500 MB RAM |
| Kommerzielles SOTA | MAI-Transcribe-1 | Qwen3.5-Omni ASR | 3,8 % WER FLEURS, nur per API |

## Sprachspezifische Hinweise {#language-specific-notes}

- **Russisch**: Qwen3-ASR und Voxtral Realtime unterstützen beide RU. Canary-1B-V2 umfasst RU in seinen 25 europäischen Sprachen. Whisper ist für reines Russisch weiterhin nutzbar
- **Chinesisch**: Qwen3-ASR ist klar im Vorteil – WER 4,97 auf WenetSpeech gegenüber 9,86 bei Whisper. Fun-ASR-Nano ist bei chinesischen Dialekten stark (Wu, Kantonesisch, Hokkien usw.)
- **Code-Switching** (Sprachmischung): Qwen3-ASR und Fun-ASR-Nano bewältigen freien Sprachwechsel besser als Whisper
- **Akzentuierte Sprache**: Fun-ASR-Nano deckt 26 regionale chinesische Akzentvarianten ab. Für andere Sprachen bietet Whispers breit gestreute Trainingsdaten weiterhin eine vernünftige Robustheit gegenüber Akzenten

## On-Device- / Edge-ASR {#on-device-edge-asr}

```text
Deployment options (2026):
  Moonshine v2 Tiny:  27M params, <500MB RAM, 50ms latency
  Parakeet.cpp:       Pure C++, no Python/ONNX, Metal GPU 27ms/10s audio
  Sherpa-ONNX:        Android/iOS/HarmonyOS/RPi/RISC-V, 12 languages
  Qwen3-ASR 0.6B:     MLX port for Apple Silicon (mlx-qwen3-asr)
  whisper.cpp:         CPU/Metal, still viable for Whisper models

Edge deployment guidelines:
  - INT4/INT8 quantization essential for mobile
  - Streaming architectures reduce memory 40%+ vs standard transformers
  - Tiny/Base variants: <500MB RAM target
```

## Aussprachebewertung {#pronunciation-assessment}

Open-Source-Aussprachebewertung bleibt eine Lücke. Proprietäre APIs (Azure Speech, SpeechSuper) dominieren den Markt.

Bester Open-Source-Weg: Qwen3-ASR + erzwungene Ausrichtung (Qwen3-ForcedAligner-0.6B) + Goodness-of-Pronunciation-Bewertung.

Verfügbare Ressourcen:
- **SpeechOcean762** – öffentlicher Datensatz (5000 englische Sätze mit Qualitätsbewertungen)
- **Kaldi GOP** – Goodness-of-Pronunciation-Metrik, ausgereift
- **Qwen3-ForcedAligner-0.6B** – Text-Sprache-Ausrichtung in 11 Sprachen, Baustein für die Aussprachebewertung

## Fallstricke {#gotchas}

- **Whisper halluziniert bei Stille** – enthält die Eingabe lange stille Abschnitte, erzeugt Whisper Phantomtext (wiederholte Phrasen, zufällige Wörter). Wende vor der Transkription immer VAD-Filterung an (`vad_filter=True` in faster-whisper). Neuere Modelle (Qwen3-ASR, Voxtral) sind dagegen robuster
- **Die 30-Sekunden-Fenstergrenze schneidet Wörter** – Whispers festes 30-s-Kontextfenster kann Wörter an den Grenzen teilen. Native Streaming-Modelle (Voxtral Realtime, Nemotron) vermeiden dies mit Sliding-Window-Architekturen vollständig
- **Spracherkennung erfolgt pro Datei, nicht pro Segment** – Whisper erkennt die Sprache einmal für das gesamte Audio. Qwen3-ASR bietet eine Sprachidentifikation pro Segment mit 97,9 % Genauigkeit über 30 Sprachen
- **Die Genauigkeit der Zeitstempel hängt von der Sprechgeschwindigkeit ab** – Wortzeitstempel aus Whispers Cross-Attention sind ungefähr (±200 ms). Für präzise Ausrichtung nutze die erzwungene Ausrichtung von WhisperX oder Qwen3-ForcedAligner
- **Whisper ist für die meisten Aufgaben nicht mehr die beste Wahl** – Stand Anfang 2026 übertrifft Qwen3-ASR Whisper bei der Genauigkeit für unterstützte Sprachen, Voxtral Realtime schlägt es beim Streaming und Moonshine v2 im Edge-Bereich. Whispers Vorteil liegt nur noch in der Sprachanzahl (100+ gegenüber 52)
- **Der Zielkonflikt zwischen VRAM und Genauigkeit hat sich verschoben** – Qwen3-ASR 0.6B mit ~2 GB VRAM übertrifft Whisper large-v3 mit ~10 GB bei Chinesisch. Prüfe Benchmarks, bevor du standardmäßig auf größere Modelle setzt

## Siehe auch {#see-also}

- [[podcast-processing]] - vollständige Pipeline mit ASR, Diarisierung und Bearbeitung
- [[tts-models]] - TTS-Modelle, die ASR zur Qualitätsbewertung nutzen
- [[voice-cloning]] - WhisperX-Ausrichtung in Sprachbearbeitungs-Workflows
- [[asr-stt-compression]] - KV-Cache-Kompression für ASR/TTS-Inferenz (TriAttention, TurboQuant)
