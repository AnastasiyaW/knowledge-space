---
title: "LEMAS: Mehrsprachige TTS und Sprachbearbeitung"
description: "Open-Source-Modelle LEMAS für mehrsprachige TTS und wortbasierte Sprachbearbeitung: Architektur, Installation, Unterstützung für 10 Sprachen und Vergleich mit F5-TTS und CosyVoice."
level: 3
source_sha256: 15ce79c7a45a1bb0772d361a4f740a9f8ee448de3c65ea57f80b40ae0426d21e
translation: machine
translated_at: '2026-10-24'
---
# LEMAS: Mehrsprachige TTS und Sprachbearbeitung {#lemas-multilingual-tts-and-speech-editing}

150K+ Stunden mehrsprachige Audio-Trainingsdaten in 10 Sprachen, aus denen zwei sich ergänzende Modelle hervorgehen: Zero-Shot-TTS und wortbasierte Sprachbearbeitung. CC-BY-4.0.

## Modelle {#models}

| Modell | Größe | Aufgabe | Architektur |
|-------|------|------|-------------|
| LEMAS-TTS | 0.3B | Zero-Shot-TTS | Flow Matching (basierend auf F5-TTS) |
| LEMAS-Edit | 0.3B | Sprachbearbeitung | Flow Matching + AR-Codec (basierend auf VoiceCraft) |

## Sprachen {#languages}

Chinesisch, Englisch, Spanisch, Russisch, Französisch, Deutsch, Italienisch, Portugiesisch, Indonesisch, Vietnamesisch

## LEMAS-TTS {#lemas-tts}

Zero-Shot-Voice-Cloning: 5-10 Sekunden langer Referenzclip → Sprache in einer von 10 Sprachen erzeugen.

**Parameter:**
- `nfe_steps` - Anzahl der Funktionsauswertungen (Abwägung zwischen Geschwindigkeit und Qualität)
- `cfg_strength` - Stärke der Classifier-Free Guidance
- `speed` - Multiplikator für die Sprechgeschwindigkeit der Ausgabe
- UVR5-Entrauschung (optional, verbessert die Qualität bei verrauschten Referenzen)

```bash
# Install
conda create -n lemas python=3.10 && conda activate lemas
sudo apt-get install -y ffmpeg  # or conda install -c conda-forge ffmpeg
git clone https://github.com/LEMAS-Project/LEMAS-TTS.git
cd LEMAS-TTS && pip install -r requirements.txt
# Download model weights from HuggingFace to pretrained_models/

# Launch Gradio UI
export PYTHONPATH="$PWD:${PYTHONPATH}"
python lemas_tts/scripts/inference_gradio.py --host 0.0.0.0 --port 7860 --share
```

HuggingFace Space: `LEMAS-Project/LEMAS-TTS`

## LEMAS-Edit {#lemas-edit}

Wortweises Ersetzen von Sprache ohne Neugenerierung der gesamten Äußerung. Die umgebenden Sprecheigenschaften bleiben erhalten.

**Zwei Backends:**

| Backend | Sprachen | Methode |
|---------|-----------|--------|
| `lemas_tts` (Flow Matching) | 10 Sprachen | Wie bei TTS |
| `lemas_edit` (AR-Codec) | 7 Sprachen | WhisperX- + MMS-Alignment |

Das Backend `lemas_edit` liefert bei Bearbeitungen mitten im Satz die bessere Natürlichkeit; `lemas_tts` deckt dagegen mehr Sprachen ab.

Evaluation: MUSHRA- und ABX-Tests sind in `./eval/` enthalten.

HuggingFace Space: `LEMAS-Project/LEMAS-Edit`

## Upstream-Abhängigkeiten {#upstream-dependencies}

F5-TTS, VoiceCraft, Vocos, UVR5, DeepFilterNet, Seamless-Expressive

## Die Open-TTS-Landschaft (April 2026) {#open-tts-landscape-april-2026}

| Modell | Organisation | Stärken |
|-------|-----|-----------|
| LEMAS-TTS | LEMAS Project | 10 Sprachen, Zero-Shot, CC-BY-4.0 |
| F5-TTS | - | Basisarchitektur, auf der LEMAS aufbaut |
| CosyVoice 2 | Alibaba | Stark im Chinesischen, Mehrsprecher-fähig |
| Fish Speech | - | Schnelle Inferenz, gut für EN/ZH |
| Kokoro TTS | - | Hohe Qualität (EN) |
| Orpheus TTS | Canopy AI | Ausdrucksstark, breites emotionales Spektrum |
| Dia | Nari Labs | Für Dialoge optimiert |

## Voice-Cloning-Pipeline {#voice-cloning-pipeline}

Für kontinuierliche Audioerzeugung (z. B. Lernsysteme, Sprachassistenten):

```python
# Architecture pattern for background audio generation
# 1. Claude API → lesson text (~2 min on voice)
# 2. LEMAS-TTS → synthesize to mp3 with cloned voice
# 3. Schedule + notification (plyer / win10toast)
# 4. Auto-play in background

# Container: pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime
# GPU: single modern GPU sufficient for 0.3B model
# Latency: real-time factor < 0.5 on T4 GPU
```

## Fallstricke {#gotchas}

- **Flow Matching erfordert eine feste Anzahl von NFE-Schritten** - anders als bei Diffusionsmodellen unterstützt LEMAS-TTS keine variable Schrittzahl während der Generierung. Setzen Sie NFE einmal pro Durchlauf.
- **Die Qualität der Referenzaudiodatei wirkt sich direkt auf das Ergebnis aus** - verrauschte oder hallbehaftete Referenzen erzeugen verrauschte Klone. Wenden Sie vor der Verwendung UVR5-Entrauschung auf die Referenzen an.
- **Die Spracherkennung erfolgt implizit** - das Modell erkennt die Ausgangssprache nicht automatisch. Die Zielsprache muss explizit angegeben werden. Nicht zusammenpassende Kombinationen aus Sprache und Text führen zu verschlechterter Ausgabe.
- **Der AR-Codec von `lemas_edit` ist langsamer** - die autoregressive Generierung ist langsamer als Flow Matching. Verwenden Sie für latenzkritische Anwendungen das Backend `lemas_tts`, auch für Bearbeitungen.

## Siehe auch {#see-also}

- [[tts-models]]
- [[voice-cloning]]
- [[voice-agent-pipelines]]
