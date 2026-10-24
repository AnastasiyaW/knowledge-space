---
title: "GUSH3R"
category: projects
date: 2026-07-08
tags: [gush3r, gush3r-development, project]
aliases: ["GUSH3R"]
level: 2
source_sha256: b46195a6b42b6ef02ed50225ecf45f67a5d7e611eb4b4cb64d2c35bc33c592c0
translation: machine
translated_at: '2026-10-24'
---
# GUSH3R {#gush3r}

**Entwicklungslinie:** `project:gush3r` · Thread `gush3r-development`  
**Letztes Ereignis:** 2026-07-08 · 1 datiertes Ereignis seit 2026-07-08 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

GUSH3R ist Forschungscode für die Rendering neuer Ansichten von sich bewegenden Personen in einer Szene aus monokularem Video. Er ersetzt eine separate Pipeline aus AnySplat für den Hintergrund und LHM für den menschlichen Teil.

- Statische Szenen-Gaussians: rekonstruieren den Hintergrund.
- Dynamische menschliche Gaussians: rekonstruieren sich bewegende Personen.
- Gemeinsames Rendering im metrischen Raum: vereinheitlicht die Geometrie von Hintergrund und Menschen.
- Kausale Frame-Verarbeitung: verarbeitet Frames kausal und kann rekurrente TTT3R-Updates verwenden.

Der herunterladbare zusammengeführte Checkpoint hat 4,87 GB, und für die Inferenz werden zusätzlich separat lizenzierte SMPL/SMPL-X-Assets benötigt.

Wir können es für Forschungsreproduktion und kontrollierte Videoexperimente einsetzen. Für eine robuste Produktions-Capture-Pipeline ist es nicht geeignet, da sich Fehler bei Pose, Kamera, Detektion und verdeckten Identitäten auf das Ergebnis fortpflanzen.

## Entwicklungslinie {#development-line}

- **2026-07-08 — Öffentliche Projektressourcen von GUSH3R verlinkt.** Am 2026-07-08 wurde die GUSH3R-Entwicklungslinie mit einer öffentlichen Projektseite, einem Quellcode-Repository und einer Hugging-Face-Ressource verknüpft. Diese Links eröffnen öffentlichen Zugang zum Projekt, ohne weitere technische Details festzulegen.

## Was sich geändert hat {#what-changed}

2026-07-08 — Die erste öffentliche Forschungsveröffentlichung von GUSH3R umfasst Code, einen zusammengeführten Inferenz-Checkpoint `gush3r.pth` und eine Projektseite. Das zugehörige arXiv-v1, eingereicht am 2026-07-06, bezeichnet die Methode als Gaussian-Unified Scene Human 3D Reconstruction. Die Veröffentlichung ergänzt eine einstufige, streamingfähige 3D-Gaussian-Repräsentation für statische Szenen und dynamische Menschen. Sie berichtet 1,70 FPS auf ihrem Benchmark mit einer Person und 1,45 FPS auf ihrem Multi-Human-BEDLAM-Benchmark.

## Anwendung {#how-to-use-this}

Ab 2026-07-08 können wir GUSH3R anhand der verlinkten Projektseite, des Quellcode-Repositorys und der Hugging-Face-Ressource bewerten. Deren Inhalte sind in diesem Review nicht recherchiert.

1. Das Repository klonen, die empfohlene Python-3.10-Umgebung anlegen, CUDA-12.1-PyTorch, die Requirements, PyTorch3D und den Gaussian-Rasterizer installieren.
  — <https://github.com/abkeito/GUSH3R>
2. `checkpoints/gush3r.pth` aus dem Modell-Repository herunterladen, lizenzierte SMPL- und SMPL-X-Assets beschaffen und hilfsweise den mitgelieferten Body-Model-Helper ausführen.
  — <https://github.com/abkeito/GUSH3R>
3. `infer.py` auf einem monokularen Video ausführen; mit `--max_frames 3` beginnen und anschließend `outputs/<name>/render.mp4` prüfen.
  — <https://github.com/abkeito/GUSH3R>

## Best Practices {#best-practices}

- Vor einer vollständigen Sequenz den Smoke-Test mit drei Frames ausführen und bei der Fehlersuche `--subsample` verwenden, um die Last der Sequenz zu verringern.
  — <https://github.com/abkeito/GUSH3R>
- Ergebnisse manuell prüfen, wenn Identitätszuordnung, starke Verdeckung zwischen Personen, Bewegungsunschärfe, große Posenänderungen, Gesichter, Hände und Kleidungstextur auftreten.
  — <https://arxiv.org/html/2607.05243v1>
- Die akkumulierte Komplexität des Hintergrunds mit `--bg_gaussian_max`, dem Maskenschwellenwert und der Voxelgröße steuern, statt ein unbegrenztes Wachstum der Szene zuzulassen.
  — <https://github.com/abkeito/GUSH3R>

## Hierdurch ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- In den geprüften Primärmaterialien wurden keine spätere offizielle Veröffentlichung, keine Replikation der Benchmarks, keine hardwarespezifischen Anforderungen für die Inferenz und keine gepflegte Richtlinie für Produktionssupport gefunden.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://abkeito.github.io/gush3r-page/ | GUSH3R: Everyone Everywhere All at Once as Gaussians | 2026-09-05 |
| https://github.com/abkeito/GUSH3R | abkeito/GUSH3R | 2026-09-05 |
| https://huggingface.co/abkeito/GUSH3R/tree/main | abkeito/GUSH3R Modelldateien | 2026-09-05 |
| https://arxiv.org/abs/2607.05243 | GUSH3R: Everyone Everywhere All at Once as Gaussians | 2026-09-05 |
| https://arxiv.org/html/2607.05243v1 | GUSH3R-Paper, HTML-Version | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:gush3r`, Thread `gush3r-development`, 1 datiertes Ereignis 2026-07-08 → 2026-07-08.
- **Praktischer Hinweis:** Ab 2026-07-08 können Praktiker die verlinkte Projektseite, das Quellcode-Repository und die Hugging-Face-Ressource als datierte öffentliche Einstiegspunkte zur Bewertung von GUSH3R nutzen; deren Inhalte sind in diesem Review nicht recherchiert.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
