---
title: "InfiniSplat"
category: projects
date: 2026-08-07
tags: [infinisplat, infinisplat-public-availability, project]
aliases: ["InfiniSplat"]
level: 2
source_sha256: 41056d020f2d3d30c583657b9cf9c4c4180d109f639fc1e6f261b047a0fccba9
translation: machine
translated_at: '2026-10-24'
---
# InfiniSplat {#infinisplat}

**Entwicklungslinie:** `project:infinisplat` · Thread `infinisplat-public-availability`  
**Letztes Ereignis:** 2026-08-07 · 1 datiertes Ereignis seit 2026-08-07 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

InfiniSplat erzeugt aus einem einzelnen RGB-Bild oder einem ausgerichteten RGB-Tiefenpaar eine 3D-Gaussian-Szene für das Rendern neuer Ansichten. Es bietet einen reinen RGB-Modus und einen Modus mit Tiefensensor-Unterstützung. Der veröffentlichte Workflow arbeitet mit einem einzelnen Bild und nicht mit einer Multi-View-Rekonstruktion. Verwenden Sie es für schnelle Ausgaben von Spatial Photos, nicht für metrische Szenenerfassung aus beliebigem Bildmaterial.

## Entwicklungslinie {#development-line}

- **2026-08-07 — Öffentliche Projektressourcen von InfiniSplat wurden dokumentiert.** Der Checkpoint `infinisplat_rgb.ckpt` verarbeitet reine RGB-Eingaben, und `infinisplat_lidar.ckpt` verarbeitet ausgerichtetes RGB plus Tiefe. Die Methode verwendet geometriegeführte Supports und query-konditionierte implizite Gaussian-Dekodierung.

## Was sich geändert hat {#what-changed}

- 2026-08-03 — arXiv v1 stellte InfiniSplat vor: Implicit Gaussian Decoding for Large-Baseline Monocular View Synthesis.
- 2026-08-04 — arXiv v2 überarbeitete das Paper.
- 2026-08-07 — Veröffentlichter Code und Demo stellten zwei vollständige Checkpoints bereit: `infinisplat_rgb.ckpt` für reine RGB-Eingaben und `infinisplat_lidar.ckpt` für ausgerichtetes RGB plus Tiefe. Die Methode verwendet geometriegeführte Supports und query-konditionierte implizite Gaussian-Dekodierung.

## So nutzen Sie es {#how-to-use-this}

Ab 2026-08-07 können wir die verlinkte InfiniSplat-Projektseite, das Repository und den Hugging-Face-Space nutzen, um die Implementierung zu prüfen und die Oberfläche vor einer Einführung zu testen.

1. Erstellen Sie die dokumentierte Python-3.10-Umgebung, installieren Sie die PyTorch-Abhängigkeiten für CUDA 12.8 und laden Sie anschließend die beiden Checkpoints herunter.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/INSTALL.md>
2. Führen Sie RGB-only-Inferenz auf einem Bild oder einem Verzeichnis mit `python -m src.demo.infer_batch_images --input PATH` aus.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/README.md>
3. Für tiefengeführte Rekonstruktion stellen Sie räumlich ausgerichtete RGB- und Tiefendateien mit übereinstimmenden Dateinamen (Stems) bereit und verwenden `--mode lidar`.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>
4. Verwenden Sie die exportierte PLY-Datei als Basisartefakt. Optional können Sie gsplat für MP4-Renderings oder splat-transform für interaktives HTML installieren.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>

## Best Practices {#best-practices}

- Geben Sie Kamera-Intrinsics oder die Brennweite an, wenn sie bekannt sind. Andernfalls greift der Runner auf eine feste Brennweite von 30 mm (Kleinbild-äquivalent) zurück.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>
- Verwenden Sie Tiefendaten, die auf das RGB-Bild ausgerichtet sind und als Tiefe statt als Disparität vorliegen. Gültige dekodierte Werte müssen endlich sein und streng zwischen 1 und 100 liegen.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>
- Vermeiden Sie `--overwrite`, wenn die Ausgaben bereits gültig sind. Der Runner überspringt abgeschlossene Artefakte und erzeugt nur ein fehlendes, angefordertes Artefakt.
  — <https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md>

## Hiermit ersetzt {#superseded-by-this}

- 2026-08-04 — arXiv v2 ersetzt das Preprint-Paper v1 vom 2026-08-03.
- 2026-08-07 — Betrachten Sie InfiniSplat als veröffentlichten Inferenz-Workflow mit zwei Modi, nicht nur als Paper oder Vorschau.

## Noch unbekannt {#still-unknown}

- Es wurde kein unabhängig datierter InfiniSplat-Release nach 2026-08-07 verifiziert. Die Projektseite enthält eine undatierte Multi-View-Vorschau „InfiniSplat V2“, daher behandeln wir sie nicht als veröffentlichten Nachfolger.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://arxiv.org/abs/2608.02437 | InfiniSplat: Implicit Gaussian Decoding for Large-Baseline Monocular View Synthesis | 2026-09-05 |
| https://zju3dv.github.io/InfiniSplat/ | InfiniSplat project page | 2026-09-05 |
| https://github.com/zju3dv/InfiniSplat/blob/main/README.md | InfiniSplat README | 2026-09-05 |
| https://github.com/zju3dv/InfiniSplat/blob/main/INSTALL.md | InfiniSplat installation guide | 2026-09-05 |
| https://github.com/zju3dv/InfiniSplat/blob/main/docs/inference.md | InfiniSplat inference guide | 2026-09-05 |
| https://huggingface.co/spaces/PLUS-WAVE/InfiniSplat | PLUS-WAVE InfiniSplat hosted demo | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:infinisplat`, Thread `infinisplat-public-availability`, 1 datiertes Ereignis 2026-08-07 → 2026-08-07.
- **Praktischer Hinweis:** Ab 2026-08-07 können wir die verlinkte InfiniSplat-Projektseite, das Repository und den Hugging-Face-Space nutzen, um die Implementierung zu prüfen und die Oberfläche vor einer Einführung zu testen.
- **Konfidenz:** hoch. Datierte Ersetzungsvermerke oben sind maßgeblich dafür, was veraltet ist.
