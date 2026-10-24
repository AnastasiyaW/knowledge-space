---
title: "IGGT4D"
category: projects
date: 2026-07-22
tags: [iggt4d, project]
aliases: ["IGGT4D"]
level: 2
source_sha256: 13e8a151b22e2973817a863f35541c025f4cd630ead0ca6475126f96d49a7851
translation: machine
translated_at: '2026-10-24'
---
# IGGT4D {#iggt4d}

**Entwicklungslinie:** `project:iggt4d` · Thread `iggt4d`  
**Letztes Ereignis:** 2026-07-22 · 1 datiertes seit 2026-07-22 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

IGGT4D verarbeitet Videoframes sequenziell und sagt Kamera, Geometrie, persistente Objektidentitäten und Instanzmasken gemeinsam voraus.

- Streaming-4D-Rekonstruktion
- Posenschätzung
- Objekttracking
- Open-Vocabulary-Segmentierung

Der Checkpoint mit 1 Milliarde Parametern erfordert die Akzeptanz der Zugriffsbedingungen auf Hugging Face. Datensatz, Benchmark sowie Trainings- und Evaluationscode sind noch nicht veröffentlicht.
Er eignet sich für Inferenz-Experimente mit eigenen Bildsequenzen, nicht aber für reproduzierbares Training oder Benchmarking.

## Entwicklungslinie {#development-line}

- **2026-07-22 — Die GitHub-Pages-Seite von IGGT4D wurde verlinkt.** Kausales Streaming-Modell, das Szenengeometrie und persistente Objektidentitäten vereint.

## Was sich geändert hat {#what-changed}

2026-07-22 — IGGT4D wurde als Streaming 4D Instance-Grounded Geometry Transformer vorgestellt: ein kausales Streaming-Modell, das Szenengeometrie und persistente Objektidentitäten vereint.

## Wie man das nutzt {#how-to-use-this}

Ab dem 2026-07-22 sollten Praktiker die verlinkte GitHub-Pages-Seite von IGGT4D als Referenzpunkt für das Projekt betrachten. Vor einer Verwendung sollten sie jedoch die konkrete Anleitung bzw. den Release-Status prüfen.

1. Das offizielle Repository klonen und mit Python 3.10 eine Conda-Umgebung anlegen.
  — <https://github.com/HorizonRobotics/IGGT4D>
2. PyTorch installieren; das README nennt als Beispiel PyTorch 2.8.0 mit CUDA 12.8. Danach das Paket mit `pip install -e .` installieren.
  — <https://github.com/HorizonRobotics/IGGT4D>
3. Die Zugriffsbedingungen des Checkpoints auf Hugging Face akzeptieren, ihn herunterladen und als `checkpoints/model.safetensors` speichern.
  — <https://huggingface.co/HorizonRobotics/IGGT4D>
4. `python streaming_infer.py` für die Demo ausführen oder `--image-dir` und `--output-dir` für eine eigene Sequenz aus RGB-Frames übergeben.
  — <https://github.com/HorizonRobotics/IGGT4D>
5. Bei Bedarf `--camera` für externe Kameraparameter aktivieren und die Ergebnisse über `--save-npy` oder `--save-ply` speichern.
  — <https://github.com/HorizonRobotics/IGGT4D>

## Best Practices {#best-practices}

- Für lange Sequenzen den Streaming-Modus als Standard beibehalten; `--mode full` ist die Offline-Variante mit Full Attention.
  — <https://github.com/HorizonRobotics/IGGT4D>
- Training, Evaluation oder Vergleich auf dem offiziellen Benchmark vor dessen Veröffentlichung nicht einplanen: Das Repository führt diese Artefakte als ausstehend auf.
  — <https://github.com/HorizonRobotics/IGGT4D>

## Hiermit ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Zum Ereignis vom 2026-07-22 gibt die primäre arXiv-Quelle als Einreichungsdatum des Papers den 2026-07-21 16:00:01 UTC an. Das bestätigt Titel, zehn Autoren und den Umfang InsScene4D-147K, liefert aber keine eigene datierte Veröffentlichung für den 2026-07-22.
- Das genaue Datum, an dem Inferenzcode und Checkpoint verfügbar wurden, ist auf den gelesenen primären Seiten nicht angegeben. Deshalb haben wir es nicht als eigenes datiertes Ereignis aufgenommen.
- Die öffentliche Projektseite gibt an, dass Datensatz und Benchmark später folgen. Das Repository wartet zusätzlich noch auf Trainings- und Evaluationscode.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://iggt4d.github.io/ | IGGT4D: Streaming 4D Instance-Grounded Geometry Transformer | 2026-09-05 |
| https://arxiv.org/abs/2607.19228 | IGGT4D: Streaming 4D Instance-Grounded Geometry Transformer | 2026-09-05 |
| https://github.com/HorizonRobotics/IGGT4D | HorizonRobotics/IGGT4D | 2026-09-05 |
| https://huggingface.co/HorizonRobotics/IGGT4D | HorizonRobotics/IGGT4D Modellkarte | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:iggt4d`, Thread `iggt4d`, 1 datiertes Ereignis vom 2026-07-22 bis 2026-07-22.
- **Praktischer Hinweis:** Ab dem 2026-07-22 sollten Praktiker die verlinkte GitHub-Pages-Seite von IGGT4D als Referenzpunkt für das Projekt betrachten. Vor einer Verwendung sollten sie jedoch die konkrete Anleitung bzw. den Release-Status prüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Angaben unter „Hiermit ersetzt“.
