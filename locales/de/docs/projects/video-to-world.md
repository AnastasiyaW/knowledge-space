---
title: "video_to_world"
category: projects
date: 2026-03-23
tags: [project, video-to-world]
aliases: ["video_to_world"]
level: 3
source_sha256: 78a2afcb8f8ea2cb0206d3c9a28dc1cb218d50c88a29be6a12e05d697318056c
translation: machine
translated_at: '2026-10-24'
---
# video_to_world {#video_to_world}

**Entwicklungslinie:** `project:video-to-world` · Thread `video-to-world`  
**Letztes Ereignis:** 2026-03-23 · 1 datiertes seit 2026-03-23 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

video_to_world ist lokaler Forschungscode zur ECCV 2026 für Personen, die eine generierte Videosequenz als erkundbare 2DGS- oder 3DGS-Szene rekonstruieren. Es handelt sich nicht um einen Videogenerator und auch nicht um einen gehosteten Dienst.

- Depth Anything 3 schätzt Geometrie und Kameras pro Frame.
- Nicht-starre Frame-zu-Modell-ICP und globale Optimierung konsolidieren inkonsistente Ansichten.
- Eine inverse-deformationsbewusste Optimierung von Gaussian Splats erzeugt die Szene.

## Entwicklungslinie {#development-line}

- **2026-03-23 — Projektressourcen zu Video-to-World wurden öffentlich verlinkt.** Projektseite und Repository wurden erfasst; Quellen des Projekts selbst nennen dieses Datum nicht als Veröffentlichungsdatum der Upstream-Version.

## Was sich geändert hat {#what-changed}

2026-03-17: arXiv v1 und der initiale Commit des Repositorys machten Paper und erster Code öffentlich. 2026-03-18: arXiv v2 wurde zur aktuellen Version; Repository-Commits ergänzten die arXiv/BibTeX-Referenz, Setup-Anpassungen und eine Korrektur des Pfads für die automatische Auswertung. 2026-03-23: Die Projektseite und das Repository wurden erfasst; Quellen des Projekts selbst nennen dieses Datum nicht als Veröffentlichungsdatum der Upstream-Version. 2026-03-26: Der Maintainer fügte die LICENSE-Datei zum Repository hinzu. 2026-04-27: Der Maintainer erstellte einen Commit mit dem Titel „Release sample data“; die aktuelle README stellt Daten zur Paper-Szene bereit, der genaue Asset-Diff wurde nicht unabhängig überprüft.

## Anwendung {#how-to-use-this}

Stand 2026-03-23 können Praktiker die verlinkte Projektseite und das GitHub-Repository als Ausgangspunkt nutzen, um das Video-to-World-Projekt und seine verfügbaren Implementierungsmaterialien zu evaluieren.

1. Den Branch main klonen, eine Python-3.10-Conda-Umgebung anlegen, numpy<2 und opencv-python<4.12 beibehalten und anschließend Depth Anything 3 auf den dokumentierten Commit fixieren und den mitgelieferten Patch für den Trajektorien-Export anwenden.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
2. Ein bereits generiertes MP4 über `--config.input-video` oder einen Ordner mit Frames über `--config.frames-dir` übergeben; `run_reconstruction.py` übernimmt Vorverarbeitung, Ausrichtung, Training der inversen Deformation und Training der Gaussian Splats.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
3. Das Standard-Preset `fast` für den kürzeren Pfad, der nur 3DGS verwendet, nutzen; `extensive` verwenden, wenn der vollständige Pfad mit globaler Optimierung, 2DGS und 3DGS benötigt wird. Die Renderer-Auswahl kann explizit überschrieben werden.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
4. `eval_gs` verwenden, um neue Ansichten aus dem trainierten Checkpoint zu rendern; einen 3DGS-Checkpoint als PLY exportieren oder den lokalen interaktiven Viewer öffnen, sobald die Szene fertig ist.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
5. Vor einem Lauf das Vorverarbeitungsmodell prüfen: Der aktuelle Standard ist `depth-anything/DA3NESTED-GIANT-LARGE`, nicht ein Modell, das video_to_world selbst mitliefert.
  — <https://github.com/lukasHoel/video_to_world/blob/main/run_reconstruction.py>

## Best Practices {#best-practices}

- Die dokumentierte Depth-Anything-3-Quellrevision fixieren und den Repository-Patch anwenden; die Pipeline hängt vom Trajektorien-Export dieses Patches ab, daher ist das Ersetzen durch einen beliebigen DA3-Checkout nicht gleichwertig.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
- Die Frame-Anzahl und die Schrittweite (Stride) von Stage 0 als GPU-Speicherbudget behandeln: Die Standardwerte sind 100 Frames und Stride 8, und die Autoren empfehlen explizit weniger Frames auf kleineren GPUs. Stage 1 hat einen eigenen Standard von 50 Frames für die Ausrichtung.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
- Den exakten main-Commit und die aufgelöste Umgebung für jeden Lauf festhalten. Das Repository hat keine GitHub-Release-Artefakte, daher ist „aktueller main“ keine versionierte Distribution.
  — <https://github.com/lukasHoel/video_to_world/releases>
- Quellsequenzen auf erneut besuchte Bereiche prüfen, in denen Objekte hinzugefügt, entfernt oder verändert werden: Das Paper beschreibt, dass solche Halluzinationen von Videomodellen in die finale statische Geometrie konsolidiert werden können, statt durch Ausrichtung korrigiert zu werden.
  — <https://arxiv.org/html/2603.16736v2>
- Aus dem Repository allein keine kommerzielle Nutzungsfreigabe ableiten: Die Model Card des aktuellen Standardmodells DA3NESTED-GIANT-LARGE deklariert CC BY-NC 4.0 und ausschließlich nicht-kommerzielle Nutzung.
  — <https://huggingface.co/depth-anything/DA3NESTED-GIANT-LARGE>

## Durch diesen Stand ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Keine Quelle des Projekts selbst mit einem Veröffentlichungs-, Release- oder Commit-Datum von 2026-03-23 gefunden; dieses Datum wird als beobachtetes Referenzdatum beibehalten und nicht als Upstream-Launch behandelt.
- Es gibt kein GitHub-Release-Bundle und keinen vollständigen Abhängigkeits-Lock; die dokumentierte DA3-Code-Revision fixiert keine unveränderliche Revision der Modellgewichte.
- Es wurde kein lokaler GPU-Lauf durchgeführt. Die Zeit- und Speicherangaben für die A6000 stammen aus einem festen Paper-Benchmark und sind keine Kapazitätsgarantie für andere Clips oder andere Hardware.
- Der veröffentlichte Geltungsbereich sind generierte Videosequenzen. Die Leistung bei realen, stark dynamischen oder stark inkonsistenten Videos wurde hier nicht belegt.
- Die Standardgewichte von DA3 sind nicht-kommerziell; ob ein kommerziell lizenziertes Ersatzmodell kompatibel ist und die Qualität erhält, ist ungeprüft.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://lukashoel.github.io/video_to_world/ | World Reconstruction From Inconsistent Views — offizielle Projektseite | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world | lukasHoel/video_to_world — offizielles Repository | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/blob/main/README.md | video_to_world README — Installation, Pipeline, Presets und Datenfreigabe | 2026-09-05 |
| https://arxiv.org/abs/2603.16736 | World Reconstruction From Inconsistent Views — arXiv-Abstract und Versionsverlauf | 2026-09-05 |
| https://arxiv.org/html/2603.16736v2 | World Reconstruction From Inconsistent Views — arXiv HTML v2 | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/commits/main/ | video_to_world — Commit-Historie | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/releases | video_to_world — GitHub-Releases | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/blob/main/run_reconstruction.py | video_to_world run_reconstruction.py — aktuelle Pipeline-Standardwerte | 2026-09-05 |
| https://huggingface.co/depth-anything/DA3NESTED-GIANT-LARGE | Depth Anything 3 DA3NESTED-GIANT-LARGE — Model Card und Lizenz | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:video-to-world`, Thread `video-to-world`, 1 datiertes Ereignis 2026-03-23 → 2026-03-23.
- **Praktischer Hinweis:** Stand 2026-03-23 können Praktiker die verlinkte Projektseite und das GitHub-Repository als Ausgangspunkt nutzen, um das Video-to-World-Projekt und seine verfügbaren Implementierungsmaterialien zu evaluieren.
- **Konfidenz:** mittel. Die datierten Supersedes-Einträge oben sind maßgeblich dafür, was veraltet ist.
