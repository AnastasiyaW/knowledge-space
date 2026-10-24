---
title: "StreamingT2V"
category: projects
date: 2024-04-08
tags: [project, streamingt2v]
aliases: ["StreamingT2V"]
level: 2
source_sha256: c2e1cb1ce78d5477dbccdcfe5da94306b63da449913cd41c264aaead7187ee6b
translation: machine
translated_at: '2026-10-24'
---
# StreamingT2V {#streamingt2v}

**Entwicklungslinie:** `project:streamingt2v` · Thread `streamingt2v`  
**Letztes Ereignis:** 2024-04-08 · 1 datiertes Ereignis seit 2024-04-08 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

StreamingT2V ist eine autoregressive Methode für lange Videos, gedacht für Forschende und Praktiker mit GPU-Ausstattung.

- CAM trägt den kurzfristigen Kontext einzelner Chunks.
- APM bewahrt das Erscheinungsbild der Szene.
- Randomisiertes Blending verfeinert überlappende Chunks.

Das Repository führt standardmäßig Image-to-Video-Inferenz mit 200 Frames bei 60 GB VRAM aus, alternativ mit 24 GB im langsameren, speicheroptimierten Modus. Der gehostete Space meldet derzeit einen Laufzeitfehler. Nutze das lokale Repository für Forschung und nicht-kommerzielle Image-to-Video-Experimente, nicht die fehlerhafte Demo und nicht einen aktuellen produktiven T2V-Dienst.

## Entwicklungslinie {#development-line}

- **2024-04-08 — Projektmaterialien zu StreamingT2V wurden öffentlich zugänglich gemacht.** Am 2024-04-08 veröffentlichte StreamingT2V eine Projektwebsite, ein öffentliches Quellcode-Repository und einen Hugging Face Space, um Forschungsmaterialien, Implementierungscode und einen interaktiven Einstiegspunkt bereitzustellen.

## Was sich geändert hat {#what-changed}

- 2024-04-08 — Das Projekt wurde öffentlich als StreamingT2V verlinkt, als autoregressive Methode zur Erweiterung der Text-zu-Video-Generierung mit Chunk-Speicher und Verfeinerung.
- 2024-06-30 — Eine spätere Referenz wurde erfasst, doch lässt sich zu diesem Datum keine unabhängig zugängliche technische Veröffentlichung oder Modelländerung zuordnen.
- 2024-08-30 — Code und Modellgewichte von StreamingSVD wurden veröffentlicht, wodurch eine auf SVD basierende Image-to-Video-Implementierung verfügbar wurde.
- 2024-11-28 — Eine speicheroptimierte Version senkte den dokumentierten VRAM-Bedarf für 200 Frames von 60 GB auf 24 GB, bei etwa 50 % geringerer Geschwindigkeit.
- 2025-02-26 — Die Arbeit wurde für die CVPR 2025 angenommen.

## So wird es verwendet {#how-to-use-this}

Wir können das Projekt ab dem 2024-04-08 über Website, Quellcode-Repository und Hugging Face Space bewerten. Die Referenz vom 2024-06-30 allein begründet keine zusätzliche Änderung am Workflow.

1. Klone das Repository, erstelle eine Python-3.9-Umgebung mit CUDA 11.8 oder neuer, installiere die Abhängigkeiten und installiere FFmpeg.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
2. Führe `python inference_i2v.py --input <image-or-folder> --output <folder>` aus dem Verzeichnis `code` aus; Eingaben müssen 16:9-Bilder sein.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
3. Setze `--num_frames` für die Länge (standardmäßig 200), `--out_fps` für die Ausgabe-Framerate (standardmäßig 24) oder `--use_memopt` bei Hardware mit 24 GB.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>

## Best Practices {#best-practices}

- Verwende den Standardpfad nur, wenn 60 GB VRAM für 200 Frames verfügbar sind; nutze `--use_memopt` bei 24 GB VRAM und plane etwa die halbe Geschwindigkeit ein.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
- Verwende randomisiertes Blending nur, wenn der Speicherdruck es erfordert; die Maintainer empfehlen bei Aktivierung eine Chunk-Größe von 38 und eine Überlappung von 12.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
- Behandle den Code als nicht-kommerzielle Forschungsnutzung, da die mitgelieferten Abhängigkeiten SVD, EMA-VFI und I2VGen-XL diese Einschränkung vorgeben.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>

## Dadurch überholt {#superseded-by-this}

- 2024-04-08 — Die Empfehlung, die verlinkte gehostete Demo zu nutzen, ist in der Praxis veraltet: Der PAIR-Hugging-Face-Space meldet derzeit einen Laufzeitfehler.
- 2024-04-08 — Die Beschreibung der verfügbaren Implementierung als allgemeine Text-zu-Video-Veröffentlichung ist veraltet: Die gepflegte README dokumentiert die Image-to-Video-Inferenz mit StreamingSVD und führt StreamingSVD für Text-zu-Video als künftiges Vorhaben auf.

## Weiterhin unbekannt {#still-unknown}

- Die verlinkten Seiten vom 2024-06-30 (X und The Source) waren nicht mit verwertbarem Text zugänglich, daher lässt sich die dort behauptete Änderung auf Produktebene nicht überprüfen.
- Nach dem Repository-Update vom März 2025 wurde keine neuere gepflegte Veröffentlichung gefunden; die aktuelle Verfügbarkeit ergibt sich aus dem Zustand von Repository und Space, nicht aus einem erfolgreich durchgeführten lokalen Lauf.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/Picsart-AI-Research/StreamingT2V | Picsart-AI-Research/StreamingT2V-Repository und README | 2026-09-05 |
| https://streamingt2v.github.io/ | StreamingT2V-Projektseite | 2026-09-05 |
| https://arxiv.org/abs/2403.14773 | StreamingT2V: Consistent, Dynamic, and Extendable Long Video Generation from Text | 2026-09-05 |
| https://huggingface.co/spaces/PAIR/StreamingT2V | PAIR/StreamingT2V Hugging Face Space | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:streamingt2v`, Thread `streamingt2v`, 1 datiertes Ereignis 2024-04-08 → 2024-04-08.
- **Praktischer Hinweis:** Ab dem 2024-04-08 konnten Praktiker die Projektseite, das Quellcode-Repository und den Hugging Face Space von StreamingT2V nutzen, um das Projekt zu bewerten oder auszuprobieren; die Referenz vom 2024-06-30 allein begründet keine zusätzliche Änderung am Workflow.
- **Konfidenz:** hoch. Die datierten Einträge unter „Dadurch überholt“ sind maßgeblich dafür, was veraltet ist.
