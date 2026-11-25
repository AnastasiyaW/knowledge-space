---
title: "MOSS-Video-Preview"
category: projects
date: 2026-06-10
tags: [moss-video-preview, project]
aliases: ["MOSS-Video-Preview"]
level: 2
source_sha256: 75c81ecd7122de156bbd6f2838ad262a02defb6a608cab82850f016b9b137af5
translation: machine
translated_at: '2026-10-24'
---
# MOSS-Video-Preview {#moss-video-preview}

**Entwicklungslinie:** `project:moss-video-preview` · Thread `moss-video-preview`  
**Letztes Ereignis:** 2026-06-10 · 1 datiertes Ereignis seit 2026-06-10 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

MOSS-Video-Preview ist eine Video-Sprachmodell-Familie unter Apache-2.0 mit eigenem Code, die auf gated Image-Video-Cross-Attention aufbaut: Base für das Pretraining, SFT für die Befolgung von Anweisungen offline und Real-Time-SFT für die Inferenz live, Frame für Frame. Der veröffentlichte Base-Checkpoint umfasst 11B in BF16. Das Projekt berichtet für einen 256-Frame-Testlauf auf einer einzelnen H200 eine mittlere TTFT von 1,9537 s. Fazit: Real-Time-SFT nur verwenden, wenn Streaming-Verhalten erforderlich ist. Dies ist eine explorative Forschungsveröffentlichung, kein gehosteter Inferenzdienst.

## Entwicklungslinie {#development-line}

- **2026-06-10 — Öffentliche Projektressourcen zu MOSS-Video-Preview referenziert.** Am 2026-06-10 wurde die Entwicklungslinie MOSS-Video-Preview mit einem öffentlichen GitHub-Repository und einer Hugging-Face-Collection verknüpft. Die datierten Links etablieren einen öffentlichen Projektbezugspunkt, belegen für sich genommen aber weder ein bestimmtes Release, eine Modellfähigkeit noch eine Versionsänderung.

## Was sich geändert hat {#what-changed}

2026-06-10 — Das verlinkte Projektpaket war öffentlich auffindbar. Primärmaterial beschreibt die Familie als gated-cross-attention-Videomodell mit etwa 10,7B bzw. 11B Parametern und getrennten Checkpoints für Base, Offline-SFT und Real-Time-SFT. 2026-06-01 — OpenMOSS veröffentlichte den technischen Bericht und Realtime-QA-100K, ein Trainings-Teilset mit 100.000 Samples für Echtzeit-Video-QA. 2026-04-08 — OpenMOSS veröffentlichte MOSS-VL-Base-0408 und MOSS-VL-Instruct-0408, nachdem die MOSS-VL-Linie begonnen worden war. 2026-03-04 — Quellcode und Architekturdetails zu MOSS-Video-Preview wurden veröffentlicht. 2025-10-18 — Das Projekt hielt ein Post-Mortem fest und begann mit MOSS-VL. 2025-10-08 — Eine interne Demo wurde gezeigt. 2025-09 — Der Real-Time-SFT-Checkpoint war fertig. 2025-08 — Der Offline-SFT-Checkpoint war fertig.

## So wird es verwendet {#how-to-use-this}

Stand 2026-06-10 sollten Praktiker das verlinkte GitHub-Repository und die Hugging-Face-Collection als initiale öffentliche Bezugspunkte für MOSS-Video-Preview nutzen und behauptete Details zu Releases anhand der primären Projektmaterialien überprüfen.

1. Klonen Sie das Repository, legen Sie die dokumentierte Python-3.12.4-Umgebung an und installieren Sie das Paket. Der getestete Stack ist PyTorch 2.4.0 mit CUDA 12.1 und DeepSpeed 0.16.1.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
2. Verwenden Sie `moss-video-preview-sft` mit `inference.offline_infer` für ein vorab aufgezeichnetes Video und einen Anweisungs-Prompt. Den Base-Checkpoint verwenden Sie für Vervollständigung oder als Ausgangspunkt für SFT.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
3. Verwenden Sie `moss-video-preview-realtime-sft` mit `inference.realtime_streaming_infer` für eingehende Frames. Base und reines SFT sind mit dem Streaming-Pfad nicht kompatibel.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
4. Laden Sie Realtime-QA-100K mit der Bibliothek `datasets` von Hugging Face, wenn Sie Real-Time-SFT-Daten reproduzieren oder anpassen. Der Datensatz enthält Annotationen, YouTube-IDs und Zeitstempel, aber keine Videodateien.
  — <https://huggingface.co/datasets/OpenMOSS-Team/Realtime-QA-100K>

## Bewährte Vorgehensweisen {#best-practices}

- Wählen Sie den Checkpoint nach Aufgabe: Base benötigt nachgelagertes SFT für die Befolgung von Anweisungen, Offline-SFT ist für ganze Clips gedacht, und Real-Time-SFT ist der erforderliche Checkpoint für Streaming.
  — <https://huggingface.co/OpenMOSS-Team/moss-video-preview-base>
- Verwenden Sie `trust_remote_code=True` erst, nachdem Sie den Repository-Code geprüft haben, da diese Modellfamilie eigene Transformers-Mappings benötigt. Verwenden Sie FlashAttention 2 auf CUDA, wenn niedrige Latenz wichtig ist.
  — <https://huggingface.co/OpenMOSS-Team/moss-video-preview-realtime-sft>
- Behandeln Sie den veröffentlichten Geschwindigkeitsvergleich als Ergebnis eines einzelnen H200-Setups und nicht als allgemeinen Benchmark. Der Test verwendete 256 extrahierte Frames aus einem 97,56 Sekunden langen 1080p-Video.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
- Bei Realtime-QA-100K müssen Sie die Verfügbarkeit und die Rechte der Videos selbst klären. Das Release enthält keine Videos, und das ursprüngliche YouTube-Material kann verschwinden oder regional eingeschränkt sein.
  — <https://huggingface.co/datasets/OpenMOSS-Team/Realtime-QA-100K>

## Durch diesen Eintrag abgelöst {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Der angegebene Endpunkt der Hugging-Face-Collection lieferte bei dieser Prüfung keinen lesbaren Inhalt. Daher sind das Erstellungsdatum und der genaue Zustand der Collection am 2026-06-10 nicht verifiziert.
- Keine geprüfte Primärquelle erklärt MOSS-Video-Preview formal für veraltet oder besagt, dass MOSS-VL es ersetzt. MOSS-VL wird daher als verwandte nachfolgende Entwicklungslinie erfasst, nicht als formaler Ersatz.
- Die aktuelle README des Projekts beschreibt weitere Skalierung, verteiltes Training sowie umfassendere Code- und Datenveröffentlichungen weiterhin als künftige Arbeit. Produktionsreife, ein gepflegter Release-Rhythmus und Unterstützung für Serving durch Dritte sind nicht verifiziert.
- event_findings:[2026-06-10] Die Projektdokumentation identifiziert das verlinkte Release als Modellfamilie mit etwa 10,7B Parametern (vermarktet als 11B), 40 Decoder-Schichten, darunter 8 gated-Cross-Attention-Schichten. Sie trennt Base, Offline-SFT und Real-Time-SFT, statt einen austauschbaren Einzel-Checkpoint auszuliefern. Quellendatum: Projektnachricht vom 2026-06-01; Quell-URL: https://github.com/OpenMOSS/MOSS-Video-Preview.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/OpenMOSS/MOSS-Video-Preview | OpenMOSS/MOSS-Video-Preview Repository und README | 2026-09-05 |
| https://huggingface.co/collections/OpenMOSS-Team/moss-video-preview | OpenMOSS-Team MOSS-Video-Preview Collection | 2026-09-05 |
| https://huggingface.co/OpenMOSS-Team/moss-video-preview-base | OpenMOSS-Team/moss-video-preview-base Model Card | 2026-09-05 |
| https://huggingface.co/OpenMOSS-Team/moss-video-preview-sft | OpenMOSS-Team/moss-video-preview-sft Model Card | 2026-09-05 |
| https://huggingface.co/OpenMOSS-Team/moss-video-preview-realtime-sft | OpenMOSS-Team/moss-video-preview-realtime-sft Model Card | 2026-09-05 |
| https://huggingface.co/datasets/OpenMOSS-Team/Realtime-QA-100K | OpenMOSS-Team/Realtime-QA-100K Dataset Card | 2026-09-05 |
| https://github.com/OpenMOSS/MOSS-VL | OpenMOSS/MOSS-VL Repository | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:moss-video-preview`, Thread `moss-video-preview`, 1 datiertes Ereignis vom 2026-06-10 → 2026-06-10.
- **Praktischer Hinweis:** Stand 2026-06-10 sollten Praktiker das verlinkte GitHub-Repository und die Hugging-Face-Collection als initiale öffentliche Bezugspunkte für MOSS-Video-Preview nutzen und behauptete Details zu Releases anhand der primären Projektmaterialien überprüfen.
- **Konfidenz:** mittel. Maßgeblich für die Frage, was veraltet ist, sind die datierten Angaben zu Ablösungen oben.
