---
title: "SANA-Streaming — SANA-Streaming"
category: projects
date: 2026-06-03
tags: [project, sana-streaming, sana_streaming]
aliases: ["SANA-Streaming"]
level: 2
source_sha256: 8d016585234049934f1d8225ea863394892e038bf4104c5b7dfaf81838dbcfb4
translation: machine
translated_at: '2026-10-24'
---
# SANA-Streaming — SANA-Streaming {#sana-streaming-sana-streaming}

**Entwicklungslinie:** `project:sana-streaming` · Thread `sana-streaming`  
**Letztes Ereignis:** 2026-06-03 · 1 datiertes seit 2026-06-03 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

SANA-Streaming ist ein 2B-Video-zu-Video-Editor für Kreative, die textgesteuerte Bearbeitungen benötigen und dabei die Bewegung des Quellmaterials sowie unbearbeitete Bereiche beibehalten.

- Langes Streaming-Editing: bearbeitet kontinuierliche Videostreams Bild für Bild.
- Kurzes bidirektionales Editing: bearbeitet Clips anhand von Vorwärts- und Rückwärtskontext.

Die berichtete Echtzeitkonfiguration läuft mit 1280×704 bei 24 End-to-End-FPS auf einer RTX 5090. Der öffentliche Inferenzpfad verwendet BF16-Checkpoints, nicht das MPQ-Deployment-Rezept aus dem Paper. Wir nutzen es für lokale V2V-Arbeiten mit langer Dauer, wenn die NVIDIA-orientierte Laufzeitumgebung und der feste 720p-Workflow zur Aufgabe passen.

## Entwicklungslinie {#development-line}

- **2026-06-03 — Projektseite von SANA Streaming referenziert.** Wir haben die Entwicklungslinie von SANA-Streaming am 2026-06-03 mit der Projektseite von NVIDIA zu SANA Streaming verknüpft. Dies ist ein wesentlicher Bezugspunkt für die öffentliche Entwicklungsgeschichte des Projekts. Die verfügbaren Belege belegen keine konkrete Veröffentlichung, Fähigkeit oder Leistungsaussage.

## Was sich geändert hat {#what-changed}

- **2026-06-03** — NVIDIA stellte SANA-Streaming als 2B-, 720p-, minutenlangen Streaming-Video-zu-Video-Editor vor. Das begleitende Paper vom 2026-05-28 berichtete 24 End-to-End-FPS und 58 DiT-FPS bei 1280×704 auf einer RTX 5090.
- **2026-07** — NVIDIA veröffentlichte Trainingsunterstützung für bidirektionale und Distillation-Pfade. Dies erweiterte die ursprüngliche Veröffentlichung von Inferenz und Checkpoints.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-06-03 sollten Sie mit der Projektseite von SANA Streaming beginnen, um offizielle Materialien zu prüfen, bevor Sie sich auf Zusammenfassungen aus zweiter Hand verlassen.

1. Installieren Sie die Repository-Umgebung, aktivieren Sie die Conda-Umgebung `sana` und behalten Sie die dokumentierten gepinnten Laufzeitversionen bei, um eine reproduzierbare bidirektionale Inferenz zu gewährleisten.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>
2. Führen Sie `long_streaming` mit dem veröffentlichten Checkpoint `sana_streaming_ar.pth` für ein Quellvideo, eine Textanweisung und bis zu 969 dekodierte Frames aus. Die dokumentierten Standardwerte verwenden vier Denoising-Schritte, CFG 1.0, zwei gecachte Blöcke und Sink-Token-Caching.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>
3. Verwenden Sie `bidirectional_short` mit `sana_bidirectional_short.pth`, wenn eine Bearbeitung von fünf Sekunden und 81 Frames ausreicht. Die dokumentierten Standardwerte verwenden 50 Schritte und CFG 6.0.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>

## Bewährte Vorgehensweisen {#best-practices}

- Behalten Sie die modusspezifische Repository-Konfiguration und die gepinnten Paketversionen bei. Fused-GDN-Kernels und der LTX-2-VAE-Pfad sind versionsabhängig.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>
- Behandeln Sie die 24-FPS-Angabe für die RTX 5090 als Ergebnis einer systemseitig co-designten MPQ-Lösung. Sie ist keine Garantie für den veröffentlichten BF16-Inferenzbefehl.
  — <https://arxiv.org/abs/2605.30409>
- Verwenden Sie Long Streaming für die Sequenzlänge und den bidirektionalen Modus für kurze Bearbeitungen. Veröffentlichte Checkpoints, Frame-Anzahlen, Sampling-Einstellungen und zeitliche Annahmen unterscheiden sich zwischen ihnen.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>

## Abgelöst durch dies {#superseded-by-this}

- **2026-07** — Das Verständnis aus dem Juni, das nur die Inferenz betraf, ist unvollständig. NVIDIA hat später Trainingspfade für bidirektionale und Distillation-Modelle veröffentlicht.

## Weiterhin unbekannt {#still-unknown}

- Das datierte Ereignis vom Juni nennt weder einen Release-Commit noch eine tagesgenaue Ankündigung. Über die Hinweise zur Juni-Veröffentlichung und das Paper-Datum vom 2026-05-28 hinaus können wir den genauen Umfang der Veröffentlichung vom 2026-06-03 nicht unabhängig festlegen.
- Dem gelieferten Antwortschema fehlen die Felder `event_findings` und `new_events`. Wir bilden ihren verifizierten Inhalt in `what_changed` und `supersedes` ab.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://nvlabs.github.io/Sana/Streaming/ | SANA-Streaming | Real-time Streaming Video Editing | 2026-09-05 |
| https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md | SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer | 2026-09-05 |
| https://github.com/NVlabs/Sana | NVlabs/Sana | 2026-09-05 |
| https://arxiv.org/abs/2605.30409 | SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:sana-streaming`, Thread `sana-streaming`, 1 datiertes Ereignis 2026-06-03 → 2026-06-03.
- **Praktischer Hinweis:** Stand 2026-06-03 sollten Praktiker die Projektseite von SANA Streaming als primären Ausgangspunkt nutzen, um die öffentlichen Materialien des Projekts zu identifizieren, bevor sie sich auf Zusammenfassungen aus zweiter Hand verlassen.
- **Konfidenz:** hoch. Die datierten Supersedes-Einträge oben sind maßgeblich dafür, was veraltet ist.
