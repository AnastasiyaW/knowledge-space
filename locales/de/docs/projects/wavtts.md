---
title: "WavTTS"
category: projects
date: 2026-06-08
tags: [project, wavtts, wavtts-development]
aliases: ["WavTTS"]
level: 2
source_sha256: 4bc106e987d74ed84836b4d87c53d11987a8839d1fd016fb4870fe658f0a56eb
translation: machine
translated_at: '2026-10-24'
---
# WavTTS {#wavtts}

**Entwicklungslinie:** `project:wavtts` · Thread `wavtts-development`  
**Letztes Ereignis:** 2026-06-08 · 1 datiert seit 2026-06-08 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

WavTTS ist ein quelloffenes Zero-Shot-Text-to-Speech-System, das sich an einer kurzen Referenzaufnahme und deren Transkript orientiert. Fähigkeiten: direkte Erzeugung aus der Rohwellenform; Inferenz über CLI und Skripte; offizieller Checkpoint mit 16 kHz; Trainings- und Evaluationscode. Einschränkung: Die veröffentlichten Gewichte stehen unter CC BY-NC 4.0, und das Modell wird nicht über einen Hugging Face Inference Provider bereitgestellt. Fazit: Geeignet für lokale, nicht-kommerzielle, stimmkonditionierte Sprachsynthese, nicht als direkt einsetzbare gehostete Produktions-API.

## Entwicklungslinie {#development-line}

- **2026-06-08 — Öffentliche Projektressourcen von WavTTS wurden erfasst.** Am 2026-06-08 wurde die WavTTS-Entwicklungslinie mit Links zur Projektwebsite, zum Quellcode-Repository, zur Modellseite, zur Demo und zu einer ComfyUI-Integration erfasst. Dies liefert einen datierten öffentlichen Bezugspunkt, um das Projekt und die zugehörigen Werkzeuge zu finden. Die vorliegenden Belege legen nicht fest, welche Veröffentlichung oder welche Codeänderung die Links gegebenenfalls begleitete.

## Was sich geändert hat {#what-changed}

2026-06-08 — WavTTS wurde mit seiner Projektseite, dem offiziellen Code und dem 16-kHz-Checkpoint, einer Web-Demo sowie einer späteren Community-ComfyUI-Integration vorgestellt; die offizielle Veröffentlichung selbst ist auf 2026-06-03 datiert.

## Anwendung {#how-to-use-this}

Stand 2026-06-08 sollten Anwender die erfassten WavTTS-Links zu Projekt, Quellcode, Modell, Demo und ComfyUI als datierten Ausgangspunkt für die Bewertung oder Integration des Projekts nutzen; allein aus dieser Zeile ergibt sich kein bestimmtes Freigabeverhalten.

1. Klonen Sie das offizielle Repository, erstellen Sie eine Conda-Umgebung mit Python 3.10, installieren Sie ein CUDA-kompatibles PyTorch und installieren Sie anschließend WavTTS im Editable-Modus.
  — <https://github.com/cwx-worst-one/WavTTS>
2. Führen Sie `wavtts_infer-cli` mit `--model WavTTS`, einer Referenz-WAV-Datei, dem Transkript dieser Aufnahme und dem zu synthetisierenden Text aus; die Standardkonfiguration lädt den offiziellen Checkpoint automatisch herunter.
  — <https://huggingface.co/worstchan/WavTTS>
3. Installieren Sie für ComfyUI den Community-Node über ComfyUI Manager oder in `custom_nodes`, starten Sie ComfyUI neu und verbinden Sie anschließend einen Referenzaudio-Eingang, das erforderliche Referenztranskript, einen Modell-Loader und den Generator-Node.
  — <https://github.com/Saganaki22/WavTTS-ComfyUI>

## Bewährte Vorgehensweisen {#best-practices}

- Verwenden Sie das bereitgestellte Conda-/Python-3.10-Setup und einen CUDA-unterstützten PyTorch-Build; das Upstream-Repository empfiehlt Conda für die Verwaltung der Abhängigkeiten.
  — <https://github.com/cwx-worst-one/WavTTS>
- Geben Sie zusammen mit der Referenzaufnahme ein korrektes Transkript an. Die ComfyUI-Integration behandelt `reference_text` als Pflichtfeld und empfiehlt einen sauberen Stimm-Prompt von 5–12 Sekunden.
  — <https://github.com/Saganaki22/WavTTS-ComfyUI>
- Für die ComfyUI-Community-Integration sollten Sie aus Gründen der Zuverlässigkeit FP32 oder für geringeren VRAM-Bedarf das Mixed-BF16-Preset bevorzugen; verzichten Sie auf FP16-Presets, die laut Maintainer nicht-endliche Samples erzeugen können.
  — <https://github.com/Saganaki22/WavTTS-ComfyUI>

## Abgelöst durch {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Der am 2026-06-08 verlinkte Hugging-Face-Space gab bei der Prüfung einen internen Fehler zurück; seine aktuelle Verfügbarkeit und genaue Oberfläche sind daher nicht verifiziert.
- Die ComfyUI-Integration ist ein separates Community-Repository und kein offizielles WavTTS-Release.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://wavtts.github.io/ | WavTTS-Projektseite | 2026-09-05 |
| https://github.com/cwx-worst-one/WavTTS | WavTTS offizielles GitHub-Repository | 2026-09-05 |
| https://huggingface.co/worstchan/WavTTS | worstchan/WavTTS offizielle Modellkarte | 2026-09-05 |
| https://github.com/Saganaki22/WavTTS-ComfyUI | WavTTS-ComfyUI Community-Integration | 2026-09-05 |
| https://arxiv.org/abs/2606.03455 | WavTTS: Towards High-Quality Zero-Shot TTS via Direct Raw Waveform Modeling | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:wavtts`, Thread `wavtts-development`, 1 datiertes Ereignis 2026-06-08 → 2026-06-08.
- **Praktischer Hinweis:** Stand 2026-06-08 sollten Anwender die erfassten WavTTS-Links zu Projekt, Quellcode, Modell, Demo und ComfyUI als datierten Ausgangspunkt für die Bewertung oder Integration des Projekts nutzen; allein aus dieser Zeile ergibt sich kein bestimmtes Freigabeverhalten.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich für die Frage, was veraltet ist.
