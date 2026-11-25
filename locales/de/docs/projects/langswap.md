---
title: "Langswap — Stack für Sprachübersetzung und Synchronisation"
category: projects
date: 2026-06-11
tags: [langswap, project, speech-translation-and-dubbing-stack]
aliases: ["Langswap"]
level: 3
source_sha256: a2d4878caac2568fc6a01c09f35d9ed1a0974b73fbe5b083deab010b5dedf984
translation: machine
translated_at: '2026-10-24'
---
# Langswap — Stack für Sprachübersetzung und Synchronisation {#langswap-speech-translation-and-dubbing-stack}

**Entwicklungslinie:** `project:langswap` · Thread `speech-translation-and-dubbing-stack`  
**Letztes Ereignis:** 2026-06-11 · 1 datiert seit 2026-06-11 · **Recherchiert:** 2026-09-05 · Konfidenz: medium

## Was es ist {#what-it-is}

Langswap ist ein lokales Tool zur Videosynchronisation für Teams, die direkte Kontrolle über Mediendateien und Modelle benötigen.

Standardmäßige Stack-Komponenten:
- ASR: transkribiert Audio mit faster-whisper large-v3 und markiert Sprachsegmente mit Silero VAD.
- Übersetzung: übersetzt Text mit Gemma-4-E2B GGUF.
- Voice-Cloning-TTS: synthetisiert Sprache über OmniVoice.
- Output-Timing: richtet das Timing der Sprache aus und exportiert SRT-Untertiteldateien.

Anforderungen und Grenzen:
Erfordert Python 3.12 und eine NVIDIA-GPU mit einem CUDA-13-Stack. Inhalte mit hohen Anforderungen erfordern eine manuelle Prüfung.

## Entwicklungslinie {#development-line}

- **2026-06-11 — Langswap stellte einen modularen Stack für Sprachübersetzung und Synchronisation vor.** Am 2026-06-11 verlinkte Langswap Quellpfade für einen Speech-to-Text-Manager, einen ASR/VAD-Client, einen Llama.cpp-Übersetzungsclient, einen OmniVoice-TTS-Client und FFmpeg. Die Links umfassten außerdem das Hauptrepository und einen Artikel über KI-Synchronisation. Anhand dieser Links können wir nicht bestätigen, ob die referenzierten Dateien an diesem Datum erstellt oder geändert wurden.

## Was sich geändert hat {#what-changed}

- 2026-06-11 — Die Quellen beschreiben eine modulare Pipeline vom Video über ASR-Segmente und Übersetzung bis zu TTS und der FFmpeg-Zusammenstellung. Der verfügbare Snapshot bestätigt keine eigenständige Veröffentlichung an diesem Datum.

## Wie man es verwendet {#how-to-use-this}

Ab dem 2026-06-11 sollten ASR/VAD, Übersetzung, TTS und FFmpeg als getrennte Integrationspunkte behandelt werden. Überprüfen Sie ihr Laufzeitverhalten und ihre Versionen vor dem Einsatz in der Produktion.

1. Installieren Sie Python 3.12, NVIDIA-GPU-Treiber, ffmpeg und rubberband-cli. Verwenden Sie uv mit dem Extra `gpu` für den lokalen GPU-Stack.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>
2. Bauen Sie das Docker-Image, starten Sie es mit `--gpus all` und binden Sie die Verzeichnisse für Gewichte und Daten ein, um schnell loszulegen.
  — <https://github.com/langswap-app/langswap>
3. Öffnen Sie Gradio unter localhost:7860, laden Sie ein Video hoch und wählen Sie die Zielsprache, um eine MP4-Datei sowie SRT-Dateien für Quelle und Übersetzung zu erzeugen.
  — <https://github.com/langswap-app/langswap>
4. Führen Sie `main.py local` zum Debuggen aus: Zwischenstände im JSON-Format werden in `data/<id>` gespeichert, sodass Neustarts bereits abgeschlossene Stufen überspringen.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>
5. Aktivieren Sie Diarisierung nur bei Bedarf, da dafür HF_TOKEN-Zugriff auf pyannote/speaker-diarization-3.1 erforderlich ist.
  — <https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md>

## Best Practices {#best-practices}

- Behalten Sie VAD-ASR als Standard bei, sofern Sie kein separates Forced Alignment benötigen: faster-whisper liefert den Text, und Silero VAD markiert die Sprachgrenzen.
  — <https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/asr_vad_client.py>
- Wiederholen Sie fehlgeschlagene Stufen über den lokalen Runner, anstatt das gesamte Video neu zu verarbeiten: Transkript und Segment-Remapping werden zwischengespeichert.
  — <https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/speech_to_text_manager.py>
- Prüfen Sie Text, Zeitcodes und Intonation vor der Veröffentlichung von Nachrichten oder Filmen durch einen menschlichen Prüfer: Ein Human-in-the-Loop-Workflow markiert die praktische Grenze der Automatisierung.
  — <https://www.forbes.ru/tekhnologii/554358-masinal-naa-ozvucka-v-cem-zaklucautsa-problemy-ii-dublaza>
- Prüfen Sie für den Quellcode die Lizenz AGPL-3.0-or-later und für heruntergeladene Modelle die jeweiligen Lizenzbedingungen, bevor Sie kommerziell oder netzwerkbasiert einsetzen.
  — <https://github.com/langswap-app/langswap>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-06-24 — Für SRT existiert kein bestätigter Nachfolger: PR #12 schlägt WebVTT vor, ist aber noch offen und ändert die dokumentierte Ausgabe nicht.

## Weiterhin unbekannt {#still-unknown}

- Wir haben keinen datierten Git-Snapshot für 2026-06-11, daher können wir eine Veröffentlichung oder den genauen Codestand zu diesem Datum nicht überprüfen.
- Die Dokumentation widerspricht sich bei HF_TOKEN: Die README führt Gemma als Gated Model auf, während der erweiterte Leitfaden das Token nur für die pyannote-Diarisierung voraussetzt.
- Kein unabhängiger End-to-End-Benchmark bestätigt Qualität, Geschwindigkeit oder Hardware-Kompatibilität des aktuellen Stacks.
- Chinesische Suchanfragen lieferten keine brauchbaren primären oder praktischen Quellen.
- 2026-06-11: Ein am 2026-02-01 veröffentlichter Artikel weist auf die Grenzen modularer Synchronisation hin: Automatisierung beschleunigt die Entwurfsarbeit, doch Präzision, Kultur und Emotionen erfordern einen Menschen im Prozess. Dabei handelt es sich um einen Meinungsbeitrag, nicht um einen Benchmark.
- 2026-06-24: PR #12 schlägt vor, die Untertitelerzeugung von SRT auf WebVTT umzustellen, die Änderungen sind jedoch nicht zusammengeführt und stellen keine Veröffentlichung dar.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/langswap-app/langswap | langswap — GitHub repository | 2026-09-05 |
| https://raw.githubusercontent.com/langswap-app/langswap/main/docs/advanced.md | langswap — advanced guide | 2026-09-05 |
| https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/speech_to_text_manager.py | SpeechToTextManager source | 2026-09-05 |
| https://github.com/langswap-app/langswap/blob/main/langswap/ml/speech_to_text_service/asr_vad_client.py | VAD ASR client source | 2026-09-05 |
| https://www.forbes.ru/tekhnologii/554358-masinal-naa-ozvucka-v-cem-zaklucautsa-problemy-ii-dublaza | Машинальная озвучка: в чем заключаются проблемы ИИ-дубляжа | 2026-09-05 |
| https://github.com/langswap-app/langswap/pull/12 | Pull request #12: SRT-to-WebVTT proposal | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:langswap`, Thread `speech-translation-and-dubbing-stack`, 1 datiertes Ereignis 2026-06-11 → 2026-06-11.
- **Praktischer Hinweis:** Ab dem 2026-06-11 sollten Praktiker, die Langswap bewerten, ASR/VAD, Übersetzung, TTS und FFmpeg in seinem Sprachsynchronisations-Workflow als getrennte Integrationspunkte behandeln und deren Laufzeitverhalten sowie Versionen prüfen, bevor sie sich darauf verlassen.
- **Konfidenz:** medium. Die datierten Ersetzungshinweise oben sind maßgeblich für das, was veraltet ist.
