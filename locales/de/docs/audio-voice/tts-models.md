---
title: "Text-to-Speech-Modelle"
category: reference
tags: [tts, speech-synthesis, voice, flow-matching, autoregressive, zero-shot, multilingual, diffusion-language-model]
level: 3
source_sha256: a7883fb6ea4a3aa1b5232ec07ad2ab8b692a0106df12303d76f3d973bd8285d3
translation: machine
translated_at: '2026-10-24'
---
# Text-to-Speech-Modelle {#text-to-speech-models}

Moderne TTS hat sich von konkatenativen und parametrischen Ansätzen hin zu neuronalen End-to-End-Modellen entwickelt. Drei dominierende Architekturen: autoregressiv (Token für Token, flexibel, aber langsam), nicht-autoregressiv / Flow Matching (feste Schrittzahl, schnellere Inferenz) und Diffusion Language Models (Text zu Multi-Codebook-Akustik-Tokens).

## Wichtigste Fakten {#key-facts}

- Zero-shot-TTS = Klonen beliebiger Stimmen anhand eines kurzen Referenzclips (3–30 Sek.) ohne Fine-Tuning
- Flow-Matching-(FM)-Modelle verwenden eine feste Anzahl an NFE-Schritten (typisch 16–32), wodurch die Inferenzzeit vorhersagbar ist
- Autoregressive (AR) Codec-Modelle erzeugen Audio-Tokens sequenziell, mit besserer Prosodie, aber variabler Latenz
- Diffusionsbasiertes TTS fügt Mel-Spektrogrammen gaußsches Rauschen hinzu und lernt, den Prozess umzukehren
- Diffusion Language Models (OmniVoice) bilden Text direkt auf Multi-Codebook-Akustik-Tokens ab – ein dritter Paradigmenansatz, der die Stärken von Flow-basierten und AR-Modellen kombiniert
- Tokenizer-freie Architekturen (VoxCPM2) verzichten vollständig auf diskrete Codec-Tokens und bewahren so prosodische Nuancen, die durch Tokenisierung verloren gehen
- Die meisten modernen TTS-Modelle geben Mel-Spektrogramme oder Audio-Codec-Tokens aus, aus denen ein Vocoder (Vocos, HiFi-GAN) die Wellenform rekonstruiert
- Abtastrate ist relevant: 16 kHz (Telefonie), 24 kHz (Standard), 44,1/48 kHz (Studioqualität)
- End-to-End-Omni-Modelle (Qwen3.5-Omni) kombinieren ASR + TTS + LLM-Reasoning in einer Architektur mit Unterstützung für Echtzeit-Konversation

## Architekturfamilien {#architecture-families}

### Flow Matching (F5-TTS-Linie) {#flow-matching-f5-tts-lineage}

Nicht-autoregressive Generierung mit fester Schrittzahl. Referenz-Audio + Text -> maskiertes Mel-Spektrogramm -> Flow Matching füllt die Maske.

```text
Pipeline:
  reference_audio -> mel_spectrogram -> [MASK target region]
  text -> phoneme_encoder -> duration_predictor -> alignment
  flow_matching(masked_mel, text_embedding, NFE=32) -> full_mel
  vocoder(full_mel) -> waveform
```

**Wichtige Modelle:**
- **F5-TTS** – grundlegendes Flow-Matching-TTS, hohe Qualität, mehrsprachig
- **LEMAS-TTS** (0,3B) – basiert auf F5-TTS, 10 Sprachen einschließlich Russisch, Trainingsdaten von 150K+ Stunden
- **CosyVoice 2** (Alibaba) – Flow Matching mit Streaming-Fähigkeit, Fokus auf Mandarin

### Autoregressiver Codec {#autoregressive-codec}

Erzeugt diskrete Audio-Tokens von links nach rechts und dekodiert sie anschließend mit einem Codec-Decoder.

```text
Pipeline:
  text -> LLM backbone -> audio_codec_tokens (e.g. EnCodec, DAC)
  codec_decoder(tokens) -> waveform
```

**Wichtige Modelle:**
- **VoxCPM2** (2B) – tokenizer-frei, 4-stufige Pipeline (LocEnc -> TSLM -> RALM -> LocDiT), Diffusion-AR-Hybrid auf MiniCPM-4-Backbone, 30+ Sprachen, nativ 48 kHz mit integrierter Super-Resolution, Apache 2.0
- **Orpheus TTS** (Canopy AI) – LLM-nativ, emotionale Steuerung über Tags
- **Fish Speech** – schneller AR-Codec, gute CJK-Unterstützung

### Diffusion Language Model {#diffusion-language-model}

Bildet Text direkt über einen Diffusionsprozess auf Multi-Codebook-Akustik-Tokens ab – vermeidet den Single-Codebook-Engpass von AR-Modellen.

```text
Pipeline:
  text -> diffusion_language_model -> multi_codebook_acoustic_tokens
  codec_decoder(multi_codebook_tokens) -> waveform
  
  Key advantage: multi-codebook = richer acoustic representation
  than single-stream AR, while still being faster than flow matching
```

**Wichtige Modelle:**
- **OmniVoice** (k2-fsa) – 600+ Sprachen, RTF 0,025 (40-fach Echtzeit), sprachübergreifendes Zero-shot-Klonen, robuste Verarbeitung verrauschter Referenzen, Apache 2.0
- **Voxtral 4B** (Mistral) – 4B Parameter, 9 Sprachen (EN/FR/DE/ES/NL/PT/IT/HI/AR, kein RU/ZH), 70 ms Latenz, Klonen ab 3 Sek., erfasst Akzent und Disfluenzen, offene Gewichte

### End-to-End-Omni-Modelle {#end-to-end-omni-models}

Kombiniert ASR + TTS + LLM-Reasoning in einem einzigen Modell. Eingabe: Audio oder Text. Ausgabe: Text und Sprache gleichzeitig.

```text
Architecture (Qwen3.5-Omni):
  Input audio/text -> Thinker module (reasoning, MoE)
  Thinker -> Talker module (speech synthesis)
  ARIA alignment: dynamic text-speech synchronization mid-generation
  
  Capabilities: real-time conversation, turn-taking detection,
  mid-conversation control (volume, tempo, emotion)
```

**Wichtige Modelle:**
- **Qwen3.5-Omni** (Alibaba) – Thinker-Talker-Dual-Modul, 113 Sprachen für ASR / 36 Sprachen für TTS / 55 Stimmen, Echtzeit-Turn-Taking, WER 6,24 auf seed-hard (vs. GPT-Audio 8,19), nur über API (nicht Open Source), 3 Varianten: Plus/Flash/Light

### Hybrid / Sonstige {#hybrid-other}

- **XTTS v2** (Coqui) – GPT-basiert + HiFi-GAN-Vocoder, bewährte Mehrsprachigkeit (RU + EN), Stimmklonen ab 6 Sek.
- **Kokoro-82M** – sehr kleines Modell (82M Parameter), 100-fach Echtzeit auf CPU, auf Englisch fokussiert
- **StyleTTS 2** – Style Diffusion + Dauerprädiktor, schnelle Inferenz
- **Chatterbox** (Resemble AI) – Emotionssteuerung, Klonen aus kurzen Samples
- **Dia** (Nari Labs) – auf Dialoge fokussiert, Generierung mit mehreren Sprechern

## Modellvergleich (2026) {#model-comparison-2026}

| Modell | Parameter | Sprachen | Abtastrate | Architektur | Stärke |
|-------|--------|-----------|-------------|-------------|----------|
| Fish Audio S2 Pro / OpenAudio S1 | 4B + 400M | 80+ | — | Dual-AR (Slow+Fast) | #1 TTS Arena, 81,88 % vs. gpt-4o-mini, 15K+ Emotions-Tags |
| VoxCPM2 | 2B | 30+ | 48 kHz | Tokenizer-frei Diff-AR | Studioqualität, Stimmdesign, Russisch |
| OmniVoice | ? | 600+ | ? | Diffusion LM | Breiteste Sprachabdeckung, RTF 0,025 |
| Qwen3.5-Omni | Groß | 36 TTS / 113 ASR | ? | Omni (Thinker-Talker) | End-to-End-Konversation |
| Voxtral 4B | 4B | 9 (kein RU/ZH) | ? | Streaming Diff-AR | 68,4 % Siege gegen ElevenLabs, 3s Klonen |
| Qwen3-TTS | 1,7B / 0,6B | 10 (inkl. RU) | ? | Eigener Codec 12 Hz | Stimmdesign, 97 ms Streaming |
| Dia 1.6B / Dia2 (Nari Labs) | 1B/2B | EN | Apache 2.0 | Dialog-TTS | Dialog mit mehreren Sprechern, Streaming, bis zu 2 Min. |
| Higgs Audio V2 (BosonAI) | 3B | Mehrsprachig | — | Llama-3.2-basiert | 75,7 % Siege gegen GPT-4o-mini-tts bei Emotionen, mehrere Sprecher |
| IndexTTS-2.5 | ? | CN/EN/JP/ES | — | Eigenentwicklung | 8-dimensionaler Emotionsvektor, präzise Dauer (Synchronisation) |
| NeuTTS Air (Neuphonic) | 748M | Mehrsprachig | Offen | GGUF | Läuft auf Raspberry Pi, 3s Stimmklonen |
| LEMAS-TTS | 0,3B | 10 | 24 kHz | Flow Matching | Mehrsprachig + Bearbeitung auf Wortebene |
| Chatterbox-Turbo | 350M–500M | 23+ (inkl. RU) | ? | Ein-Schritt-Decoder | MIT, paralinguistische Tags |
| Kokoro-82M | 82M | 6 (kein RU) | 24 kHz | StyleTTS-ähnlich | Am schnellsten: 210x RT, CPU |
| XTTS v2 | ~0,5B | 17 (inkl. RU) | 24 kHz | GPT + Vocoder | Bewährt, stabil, RU |
| CosyVoice 3 | ~0,5B | 9 (inkl. RU) | 22,05 kHz | RL-optimiertes FM | CER 0,81 %, 150 ms Latenz |
| F5-TTS Russian | 0,3B | RU | 24 kHz | Flow Matching (feinabgestimmt) | Bestes Open-Source-TTS für RU |
| Spark-TTS | 0,5B | ZH/EN | ? | BiCodec + Qwen2.5 | Steuerung von Attributen per Chain-of-Thought |
| OuteTTS 1.0 | 0,6B/1B | Mehrsprachig | ? | AR + DAC-Encoder | GGUF/EXL2, Consumer-Hardware |

## Inferenzparameter {#inference-parameters}

```text
Common TTS parameters:
  NFE steps (flow matching): 16-32, higher = better quality, slower
  CFG strength: 1.0-3.0, controls adherence to text vs naturalness
  Temperature: 0.5-1.0, controls variation in AR models
  Speed: 0.8-1.2x, pitch-preserving time stretch
  Top-k / Top-p: AR sampling parameters, same as LLM text generation
```

## Sprachbearbeitung {#speech-editing}

LEMAS-Edit und VoiceCraft ermöglichen die Bearbeitung auf Wortebene – bestimmte Wörter in einer Aufnahme ersetzen, ohne die gesamte Äußerung neu zu generieren. Zwei Backends:

- **Flow-Matching-Backend**: schneller, 10 Sprachen
- **AR-Codec-Backend**: 7 Sprachen, benötigt WhisperX + MMS-Alignment für Wortgrenzen

## Evaluationsmetriken {#evaluation-metrics}

- **MOS** (Mean Opinion Score) – menschliche Bewertung von 1 bis 5, Goldstandard, aber teuer
- **MUSHRA** – Multi-Stimulus-Vergleichstest, besser für den Vergleich von Modellen geeignet
- **WER** (Word Error Rate) – generierte Sprache transkribieren und mit dem Eingabetext vergleichen
- **Sprecherähnlichkeit** – Kosinusähnlichkeit der Sprecher-Embeddings von Referenz und Generierung
- **PESQ / POLQA** – perzeptuelle Qualität, korreliert mit MOS

## Stimmdesign (Stimmerstellung aus Textbeschreibung) {#voice-design-text-described-voice-creation}

Manche Modelle können eine Stimme aus einer Textbeschreibung erzeugen, ohne dass Referenz-Audio benötigt wird:

```text
VoxCPM2 voice design:
  Input: "A warm female voice, age 30, slight accent, cheerful"
  -> Voice design module generates synthetic speaker embedding
  -> TTS generates speech with described characteristics

OmniVoice attribute control:
  Attributes: gender, age, pitch, dialect, whisper, speaking rate
  -> Fine-grained parametric control over synthetic voice
  -> Can combine: "young female, whispering, fast pace"
```

## Latenz-Benchmarks (2026) {#latency-benchmarks-2026}

| Modell | First-Packet (TTFA) | RTF | Anmerkungen |
|-------|---------------------|-----|-------|
| Kokoro 82M | 40–70 ms | 0,005 (210x RT) | Am schnellsten, CPU-freundlich |
| Qwen3-TTS Flash | 97 ms | — | Streaming |
| CosyVoice 3 | 150 ms | — | Bi-Streaming, verlustfrei |
| Voxtral 4B | 70 ms | — | 500 Zeichen / 10 s Eingabe |
| Fish Audio S2 Pro | <100 ms | 0,195 | SGLang-Inferenz-Engine |
| VoxCPM2 | — | 0,13 (Nano-VLLM) | RTF 0,30 mit Standard-PyTorch |
| Chatterbox-Turbo | ~472 ms | 0,499 | Kompromiss durch Ein-Schritt-Decoder |

## Russisches TTS (Open Source, gerankt) {#russian-tts-open-source-ranked}

| Modell | Qualität | Anmerkungen |
|-------|---------|-------|
| F5-TTS Russian (ESpeech) | Bestes Open Source | Mehrere Fine-Tunes, 10K+ Stunden |
| ESpeech-TTS-1 RL-V2 | Ausgezeichnet | Apache 2.0 |
| Qwen3-TTS 1.7B | Stark | 1 von 10 Sprachen |
| CosyVoice 3 | Unterstützt | RL-optimiert |
| Chatterbox-ML 500M | Unterstützt | 1 von 23 Sprachen |
| VoxCPM2 2B | Unterstützt | Sprachmodell mit 30+ Sprachen |
| XTTS v2 | Gut | 17 Sprachen, bewährt |
| Silero TTS | Ausgezeichnet | Speziell für Russisch entwickelt |

Ressourcen: [Russisches TTS-Leaderboard](https://huggingface.co/spaces/ESpeech/open_tts_leaderboard_ru) | [awesome-russian-speech](https://github.com/alphacep/awesome-russian-speech)

## Stolperfallen {#gotchas}

- **Die Qualität des Referenz-Audios ist entscheidend** – verrauschte, hallige oder mit Musik verunreinigte Referenzen ergeben unabhängig von der Modellqualität schlechte Klone. Vor der Verwendung UVR5 oder DeepFilterNet zur Rauschunterdrückung einsetzen. Ausnahme: OmniVoice ist ausdrücklich robust gegenüber Rauschen und akzeptiert verrauschte Samples
- **Mehrsprachiges Zero-shot hat ungleichmäßige Qualität** – die meisten Modelle sind auf Englisch/Chinesisch stark, bauen aber bei ressourcenärmeren Sprachen ab. OmniVoice (600+ Sprachen) und VoxCPM2 (30+ Sprachen) haben die breiteste Abdeckung, dennoch immer die Zielsprache gezielt testen
- **Der NFE-Kompromiss beim Flow Matching ist nicht linear** – der Sprung von 16 auf 32 Schritte verbessert die Qualität spürbar, doch von 32 auf 64 Schritte sinkt der Nutzen deutlich, während sich die Latenz verdoppelt
- **Codec-basierte Modelle halluzinieren bei langen Eingaben** – AR-Modelle können bei Texten über 500 Zeichen in Schleifen geraten, stottern oder Wörter auslassen. Lange Texte in satzweise Abschnitte aufteilen
- **Reine API-Modelle binden an einen Anbieter** – Qwen3.5-Omni bietet das beste End-to-End-Erlebnis, ist aber nur über API verfügbar. Für den Fall von Kosten- oder Verfügbarkeitsproblemen einen Fallback auf offene Modelle (OmniVoice, VoxCPM2) einplanen
- **Tokenizer-frei vs. Codec-Kompromiss** – tokenizer-freie Modelle (VoxCPM2) bewahren prosodische Details, die codec-basierte Modelle bei der Tokenisierung verlieren, sind aber tendenziell größer und langsamer

## Siehe auch {#see-also}

- [[voice-cloning]] – eigenständige Behandlung von Klonverfahren und sprachübergreifendem Transfer
- [[voice-design]] – Erstellung eigenständiger Stimmidentitäten aus Textbeschreibungen, Stimmmischung (Slerp, Cartesia, VoxMorph)
- [[asr-stt-compression]] – KV-Cache-Kompression für TTS-Inferenz (TriAttention, TurboQuant)
- [[audio-generation]] – Generierung von Musik und Soundeffekten
- [[speech-recognition]] – ASR-Modelle für die TTS-Evaluation (WER-Messung)
