---
title: "Qwen-Video-Edit"
category: projects
date: 2026-08-18
tags: [project, qwen-video-edit]
aliases: ["Qwen-Video-Edit"]
level: 2
source_sha256: e6f7a89fb52a98ff8bfe993b5cd36ffd59bc477dabee3073f05a801f553406a2
translation: machine
translated_at: '2026-10-24'
---
# Qwen-Video-Edit {#qwen-video-edit}

**Entwicklungslinie:** `project:qwen-video-edit` · Thread `qwen-video-edit`  
**Letztes Ereignis:** 2026-08-18 · 1 datiertes Ereignis seit 2026-08-18 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Qwen-Video-Edit stellt Code und Checkpoints für die anweisungsbasierte Videobearbeitung ohne einen videovortrainierten Transformer bereit. Qwen-Image-Edit bearbeitet die latente Repräsentation des Wan 2.1 VAE, während Wan 2.2 das Ergebnis nachbearbeiten kann.

- Frame-Konsistenz, damit Bearbeitungen über das gesamte Video stabil bleiben.
- Anweisungen pro Chunk, um jedem Segment eines langen Clips einen eigenen Prompt zuzuweisen.
- CLI- und ComfyUI-Workflows für lokale Ausführungen.

Ein Checkpoint benötigt etwa 40 GB, die Basisgewichte und die Verbesserung erfordern etwa 55 GB Speicherplatz, und der 720P-Checkpoint wurde weniger trainiert als die anderen.
Für einen ersten Lauf empfiehlt sich 360P/step-30000; für 81-Frame-Chunks wird 480P/global_local_81 verwendet.

## Entwicklungslinie {#development-line}

- **2026-08-18 — Qwen-Video-Edit wurde öffentlich vorgestellt, mit Links zu Projekt, Code und Modellen.** Am 2026-08-18 veröffentlichten die Autoren die Projektseite, das GitHub-Repository und die Hugging-Face-Ressource, damit Nutzer die Modelle evaluieren und ausführen können.

## Was sich geändert hat {#what-changed}

- 2026-08-18 — Das initiale Release veröffentlichte den Code, den Bericht, die Projektseite und einen 360P-Checkpoint; die README datiert das initiale Release auf 2026-08-14.
- 2026-08-20 — Die Autoren ergänzten 480P-Checkpoints über verschiedene Datenteilmengen, eine 81-Frame-Variante und 720P-Gewichte sowie benutzerdefinierte Nodes für ComfyUI.

## So wird es genutzt {#how-to-use-this}

Ab 2026-08-18 lässt sich Qwen-Video-Edit über die Projektseite, das Repository und die Hugging-Face-Ressource evaluieren. Vor einer Adoption sollten Fähigkeiten, Installation, Lizenzierung und Modelldetails geprüft werden.

1. Erstelle eine Python-3.10–3.12-Umgebung mit einem CUDA-Build von PyTorch, installiere requirements.txt und setze DIFFSYNTH_MODEL_BASE_PATH.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
2. Lade den empfohlenen 360P/step-30000-Checkpoint und die Basisgewichte herunter oder lasse den Loader sie beim ersten Lauf nachladen.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
3. Führe infer.py mit dem Eingabevideo, prompts.txt und den passenden Einstellungen für Checkpoint, num_frames und video_max_pixels aus; jede Zeile in prompts.txt wird einem Segment zugeordnet.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
4. Für ComfyUI installiere das Repository in custom_nodes, importiere den Workflow und setze die Pfade zum Checkpoint und zu Wan 2.2.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>

## Best Practices {#best-practices}

- Führe Befehle aus dem Wurzelverzeichnis des Repositorys aus, damit die mitgelieferten Pakete diffsynth und wan Vorrang vor externen Paketen haben.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
- Stimme num_frames, video_max_pixels, latent_mode und pe_mode auf die Checkpoint-Tabelle ab, da nicht passende Werte nicht unterstützt werden.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
- Beginne mit 360P/step-30000 als sicherem, leichtgewichtigem Standard; 720P wurde nur 3.500 Schritte trainiert, daher auf 480P oder 360P zurückwechseln, falls die Ergebnisse schlechter werden.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>
- Teile lange Videos in Chunks auf und weise jedem einen eigenen Prompt zu; skip_enhance nur zum Debuggen verwenden.
  — <https://github.com/yunpeng1998/Qwen-Video-Edit>

## Ersetzt durch diesen Eintrag {#superseded-by-this}

- 2026-08-20 — Der initiale einzelne 360P-Checkpoint ist nicht mehr das vollständige Modellangebot: Releases umfassen nun 480P-, 81-Frame- und 720P-Varianten sowie die ComfyUI-Integration.

## Noch unbekannt {#still-unknown}

- Das Zielschema enthält die Felder event_findings und new_events nicht, daher erscheinen die datierte Klarstellung vom 2026-08-18 und das separate Ereignis vom 2026-08-20 stattdessen in what_changed und supersedes.
- Unabhängige Benchmarks haben visuelle Qualität, VRAM-Bedarf und Zuverlässigkeit bei beliebigen Eingabevideos nicht verifiziert; die aktuellen Daten stammen ausschließlich von den Projektautoren.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/yunpeng1998/Qwen-Video-Edit | Qwen-Video-Edit — GitHub repository and README | 2026-09-05 |
| https://yunpeng1998.github.io/Qwen-Video-Edit-Page/ | Qwen-Image Video-Edit — project page | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:qwen-video-edit`, Thread `qwen-video-edit`, 1 datiertes Ereignis 2026-08-18 → 2026-08-18.
- **Praktischer Hinweis:** Ab 2026-08-18 sollten Praktiker die verlinkte Projektseite, das Repository und die Hugging-Face-Ressource als Ausgangspunkt für die Evaluierung von Qwen-Video-Edit nutzen und Fähigkeiten, Installation, Lizenzierung und Modelldetails vor einer Adoption anhand dieser Quellen prüfen.
- **Konfidenz:** hoch. Die datierten supersedes-Einträge oben sind maßgeblich für das, was veraltet ist.
