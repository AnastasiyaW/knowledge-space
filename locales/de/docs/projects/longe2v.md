---
title: "LongE2V"
category: projects

tags: [longe2v, longe2v-development, project]
aliases: ["LongE2V"]
level: 2
source_sha256: e2f7bf63445dff3e8febad526d3f9ff84c79d4b08709e61fb25af969314f7d1f
translation: machine
translated_at: '2026-10-24'
---
# LongE2V {#longe2v}

**Entwicklungslinie:** `project:longe2v` · Thread `longe2v-development`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

LongE2V ist ein Open-Source-Forschungsstack für Event Vision, der als LoRA auf THUDM/CogVideoX-5B-I2V feinabgestimmt wurde.

- Videorekonstruktion aus spärlichen Event-Streams.
- Langfristige Vorhersage aus spärlichen Event-Streams.
- Frame-Interpolation aus spärlichen Event-Streams.

Ein Standardlauf erfordert Linux, NVIDIA/CUDA 12.8, Python 3.10 und Event-Voxel; einen gehosteten Inferenzanbieter gibt es nicht. Der Stack eignet sich für die Reproduktion und Evaluation von Event-Kamera-Aufgaben, nicht für die standardmäßige Videogenerierung aus Fotos.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; was bekannt ist, steht in den folgenden Abschnitten.

## Was sich geändert hat {#what-changed}

2026-07-12 — LongE2V erschien als SIGGRAPH-2026-Projekt mit Code für einen einheitlichen Diffusionsansatz für eventbasierte Rekonstruktion, Vorhersage und Frame-Interpolation. 2026-07-14 — Das zugehörige LongE2V-Modell und Datensatz auf Hugging Face wurden als aktualisiert markiert; der öffentliche Pfad umfasst nun fertige LoRA-Gewichte und vorverarbeitete Daten für die lokale Reproduktion.

## So verwenden Sie es {#how-to-use-this}

1. Klonen Sie das Repository, erstellen Sie eine Python-3.10-Umgebung und installieren Sie PyTorch 2.8.0 für CUDA 12.8 sowie die Projektabhängigkeiten.
  — <https://github.com/cdfan0627/LongE2V>
2. Laden Sie die veröffentlichte LoRA-Datei in weights/ herunter und holen Sie die vorverarbeiteten Daten, oder bereiten Sie Event-Voxel manuell vor.
  — <https://github.com/cdfan0627/LongE2V>
3. Wählen Sie Rekonstruktion, Vorhersage oder Interpolation und führen Sie das passende infer_*.sh mit dem gesetzten Wert DATASET aus.
  — <https://github.com/cdfan0627/LongE2V>
4. Verarbeiten Sie die Ausgabe-Frames vor dem Vergleich der Metriken: skalieren Sie sie, wenden Sie für Rekonstruktion und Vorhersage eine Helligkeitskorrektur an und führen Sie dann das passende Metrik-Skript aus.
  — <https://github.com/cdfan0627/LongE2V>

## Best Practices {#best-practices}

- LongE2V: Ersetzen Sie Event-Streams nicht durch Standard-Eingabebilder; die Methoden konditionieren auf Event-Voxel und lösen Event-Kamera-Aufgaben.
  — <https://arxiv.org/abs/2607.08770>
- LongE2V: Verwenden Sie die veröffentlichte Datenstruktur für reproduzierbare Ergebnisse; fehlende oder zusätzliche Voxel-Dateien verändern die Event-Chunks, und Reverse-Voxel werden nur für die Interpolation benötigt.
  — <https://github.com/cdfan0627/LongE2V>
- LongE2V: Betreiben Sie das System auf einer GPU und achten Sie auf Kompatibilität mit CUDA 12.8 und den fixierten Paketen; Multi-GPU ist nicht getestet, und ein kleineres ATTENTION_SCORE_CHUNK_SIZE spart Speicher auf Kosten der Geschwindigkeit.
  — <https://github.com/cdfan0627/LongE2V>
- LongE2V: Vergleichen Sie keine rohen Frames mit veröffentlichten Metriken; Rekonstruktions- und Vorhersagemetriken erfordern eine separate EVREAL-Umgebung, weil pyiqa mit den Kernabhängigkeiten in Konflikt steht.
  — <https://github.com/cdfan0627/LongE2V>

## Abgelöst durch dieses {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- LongE2V — Es existiert kein öffentliches Changelog, kein Tag und kein GitHub Release, daher lassen sich die genauen Daten der ersten Code- und Gewichtsveröffentlichung sowie nachfolgender inhaltlicher Änderungen nicht zuverlässig rekonstruieren.
- LongE2V — Verfügbarkeit und Kompatibilität mit beliebigen eigenen Event-Daten und GPUs wurden nicht durch einen Live-Lauf bestätigt; die Dokumentation belegt nur den veröffentlichten Forschungspfad.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://cdfan0627.github.io/LongE2V-page/ | LongE2V — Projektseite | 2026-09-06 |
| https://github.com/cdfan0627/LongE2V | cdfan0627/LongE2V — offizielle Implementierung und README | 2026-09-06 |
| https://arxiv.org/abs/2607.08770 | LongE2V: Long-Horizon Event-based Video Reconstruction, Prediction, and Frame Interpolation with Video Diffusion Models | 2026-09-06 |
| https://huggingface.co/fansam39/LongE2V | fansam39/LongE2V — LoRA-Modellkarte | 2026-09-06 |
| https://huggingface.co/datasets/fansam39/LongE2V-data | fansam39/LongE2V-data — vorverarbeiteter Datensatz | 2026-09-06 |
| https://huggingface.co/papers/2607.08770 | Hugging-Face-Papierseite für arXiv:2607.08770 | 2026-09-06 |
| https://github.com/cdfan0627/LongE2V/releases | LongE2V GitHub Releases | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:longe2v`, Thread `longe2v-development`, 0 datierte Ereignisse - → -.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
