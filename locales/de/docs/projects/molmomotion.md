---
title: "MolmoMotion"
category: projects
date: 2026-06-18
tags: [molmomotion, molmomotion-model-availability, project]
aliases: ["MolmoMotion"]
level: 2
source_sha256: a4044eb146c0dcff85aec1f5dc7d04420041619d4135ab8d389fe88076ff5a6f
translation: machine
translated_at: '2026-10-24'
---
# MolmoMotion {#molmomotion}

**Entwicklungslinie:** `project:molmomotion` · Thread `molmomotion-model-availability`  
**Letztes Ereignis:** 2026-06-18 · 1 datiertes seit 2026-06-18 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

MolmoMotion ist ein auf Molmo 2 basierendes 4B-Modell für Forschende, die Roboterplanung oder trajektoriengeführte Videogenerierung entwickeln.

- 3D-Punktpfade: prognostiziert objektgebundene Pfade.
- Konditionierung: konditioniert auf RGB-Verlauf, 2D/3D-Abfragepunkte und eine Aktion.
- Modellvarianten: bietet AR- und Flow-Matching-Varianten.

Der H3-F30-Checkpoint benötigt drei Frames und sagt 30 zukünftige Frames voraus, etwa zwei Sekunden bei 15 fps.
Verwenden Sie ihn für Experimente zur 3D-Bewegungsprognose, nicht als Text-zu-Video-Modell oder allein als Roboterpolicy.

## Entwicklungslinie {#development-line}

- **2026-06-18 — Modellressource MolmoMotion-4B-H3-F30 erfasst.** Der autoregressive 4B-Checkpoint nimmt drei Verlaufsframes entgegen und prognostiziert 30 zukünftige 3D-Positionen pro Abfragepunkt.

## Was sich geändert hat {#what-changed}

2026-06-18 — MolmoMotion-4B-H3-F30 wurde verfügbar: Der autoregressive 4B-Checkpoint nimmt drei Verlaufsframes entgegen und prognostiziert 30 zukünftige 3D-Positionen pro Abfragepunkt.

## So verwenden Sie es {#how-to-use-this}

Ab 2026-06-18 sollten Sie MolmoMotion-4B-H3-F30 als eigenständig identifizierbare MolmoMotion-Modellressource führen. Prüfen Sie die Modellkarte, bevor Sie sich auf Fähigkeiten, Lizenz oder Deployment-Anforderungen verlassen.

1. Installieren Sie das offizielle Repository in einer Python-3.11-Umgebung mit dem Extra für Visualisierung.
  — <https://github.com/allenai/molmo-motion>
2. Laden Sie `allenai/MolmoMotion-4B-H3-F30` mit `MolmoMotionProcessor` und `MolmoMotion` und führen Sie das interne Modell in bf16 auf CUDA aus.
  — <https://github.com/allenai/molmo-motion>
3. Stellen Sie drei RGB-Frames bereit, sortiert vom frühesten bis t0, 2D-Punktkoordinaten zu t0, 3D-Punktverlauf im Kamerakoordinatensystem von t0, eine Aktionsbeschreibung und den Vorhersagehorizont 30.
  — <https://github.com/allenai/molmo-motion>
4. Rufen Sie `predict_trajectory` auf und verarbeiten Sie `future_3d` als Tensor der Form 8×30×3 mit Koordinaten im Kamerasystem in Metern; rendern Sie die Trajektorien oder übergeben Sie sie an ein nachgelagertes System.
  — <https://github.com/allenai/molmo-motion>

## Bewährte Praktiken {#best-practices}

- Wählen Sie für gewöhnliche Videoeingaben H3-F30; verwenden Sie H1-F32 nur, wenn genau ein Abfrage-Keyframe vorliegt.
  — <https://huggingface.co/allenai/MolmoMotion-4B-H3-F30>
- Behandeln Sie Trajektorien als Hilfe für Planung oder Generierung und feinabstimmen Sie das Modell für eine nachgelagerte Robotikaufgabe, anstatt den Basisprognostiker als einsetzbare Policy darzustellen.
  — <https://huggingface.co/allenai/MolmoMotion-4B-H3-F30>
- Verwenden Sie den offiziellen Quick-Start-Eingabevertrag; der 3D-Verlauf der Abfragepunkte muss im Kamerakoordinatensystem zu t0 angegeben werden.
  — <https://github.com/allenai/molmo-motion>

## Hierdurch abgelöst {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- In den herangezogenen Quellen fanden wir nach dem Checkpoint-Ereignis vom 2026-06-18 keine datierte Nachfolgeveröffentlichung des Herstellers. Das öffentliche Repository dokumentiert H1-F32 und Modellfamilien, legt aber für diese kein späteres Veröffentlichungsdatum fest.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/allenai/MolmoMotion-4B-H3-F30 | Modellkarte allenai/MolmoMotion-4B-H3-F30 | 2026-09-05 |
| https://github.com/allenai/molmo-motion | Offizielles Repository allenai/molmo-motion | 2026-09-05 |
| https://allenai.org/blog/molmo-motion | MolmoMotion: Sprachgeführte 3D-Bewegungsprognose | 2026-09-05 |
| https://arxiv.org/abs/2606.18558 | MolmoMotion: Forecasting Point Trajectories in 3D with Language Instruction | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:molmomotion`, Thread `molmomotion-model-availability`, 1 datiertes Ereignis 2026-06-18 → 2026-06-18.
- **Praktischer Hinweis:** Ab 2026-06-18 sollten Sie MolmoMotion-4B-H3-F30 als eigenständig identifizierbare MolmoMotion-Modellressource führen und die Modellkarte prüfen, bevor Sie sich auf Fähigkeiten, Lizenz oder Deployment-Anforderungen verlassen.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
