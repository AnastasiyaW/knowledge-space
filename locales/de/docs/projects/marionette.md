---
title: "Marionette — Öffentliche Projektveröffentlichung"
category: projects
date: 2026-08-18
tags: [alayalab/marionette, marionette, project, public-project-release]
aliases: ["Marionette"]
level: 2
source_sha256: 7443d47d719be856ace9191e4f22c7ee834104de7222aa3a0c872346f19f68ac
translation: machine
translated_at: '2026-10-24'
---
# Marionette — Öffentliche Projektveröffentlichung {#marionette-public-project-release}

**Entwicklungslinie:** `project:marionette` · Thread `public-project-release`  
**Letztes Ereignis:** 2026-08-18 · 1 datiertes Ereignis seit 2026-08-18 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Marionette: Pipeline von Alaya Lab für Forschende an World Models: ActionGPT und PoseGPT sagen einen 276-dimensionalen artikulierten Zustand voraus, ein deterministischer Bridge rendert die Geometrie, und ein feinabgestimmtes Wan2.2-Fun-5B-Control erzeugt RGB-Videos.

- Steuerung: Austausch des Action Token oder der Trajectory Root auf Zustandsebene;
- Start: zwei Python-Umgebungen für Stage 1 und Stage 2;
- Grenzen: eine Monsterart, Scans konkreter Standorte und eine Lizenz für nichtkommerzielle Forschung.

Maßstab: Der veröffentlichte Observation-Checkpoint wiegt 10,0 GB, das erforderliche Basismodell eines Drittanbieters etwa 23 GB.

Fazit: Dies ist eine reproduzierbare Forschungs-Pipeline und keine universelle Game-Engine und kein fertiger Dienst zur Videogenerierung.

## Entwicklungslinie {#development-line}

- **2026-08-18 — Öffentliche Projektressourcen von Marionette wurden verlinkt.** Am 2026-08-18 war die Entwicklungslinie von Marionette durch Links zur Projektseite, zum Quellcode-Repository, zur Hugging-Face-Modellseite und zum gehosteten World-Model-Space repräsentiert. Dies ist ein wesentlicher öffentlicher Projektmeilenstein, weil er Dokumentation, Code, Modellverteilung und lauffähige Demonstration miteinander verbindet.

## Was sich geändert hat {#what-changed}

2026-08-13 — Projektseite, Inferenzcode, Laufzeit-Assets und Controllability-Demos wurden veröffentlicht; die vollständige dreistufige Pipeline wurde für den lokalen Start verfügbar. 2026-08-14 — Auf arXiv erschien die Arbeit „Marionette: Predicting World States, Rendering Geometry, Painting Appearance“; sie legte die Architektur und die behaupteten Ergebnisse zur Zustandskontrolle fest. 2026-08-18 — Projektmaterialien, Repository, Hugging-Face-Gewichte und Demonstration wurden in einer Veröffentlichung zusammengeführt; die Modellkarte präzisiert den genauen Namen des Basismodells, die Größen der Checkpoints, die Inferenzeinstellungen und die Einschränkungen.

## So verwenden Sie dies {#how-to-use-this}

Ab dem 2026-08-18 sollten Praktiker die verlinkte Projektseite, das Repository, die Hugging-Face-Modellseite und den gehosteten Space als Ausgangsbasis für die Bewertung von Marionette verwenden; Fähigkeiten, Lizenzierung und Reproduktionsschritte erfordern vor einem Einsatz dennoch eine Prüfung der Quellen.

1. Repository klonen, Marionette-Gewichte und das Basismodell eines Drittanbieters laden und anschließend `bash run_demo.sh` ausführen.
  — <https://huggingface.co/AlayaLab/Marionette>
2. Für den getrennten Start eine Render-Umgebung für Stage 1 und eine Wan-Umgebung für Stage 2 anlegen; `run_stage1_render.sh` ausführen, danach `run_stage2_wan.sh`.
  — <https://github.com/AlayaLab/Marionette>
3. Observation-Checkpoint und dessen Prompt als festes Paar verwenden; veröffentlichte Einstellungen sind 704×1280, 40 Steps, Guidance 6.0, 81-Frame-Chunks, 30 fps.
  — <https://huggingface.co/AlayaLab/Marionette>

## Bewährte Praktiken {#best-practices}

- Stage 1 und Stage 2 nicht in einer einzigen Umgebung zusammenführen: Das Rendering benötigt Python 3.12 und EGL, die Diffusionsstufe benötigt torch, diffusers und decord.
  — <https://github.com/AlayaLab/Marionette>
- `TORCH_SEED` festlegen, um die Dynamik-Stufe reproduzierbar zu machen; Ergebnisse auf derselben Maschine anhand der Gleichheit reproduzierbarer Artefakte vergleichen, nicht anhand eines portablen Video-Hashes.
  — <https://github.com/AlayaLab/Marionette>
- Action IDs nicht zwischen Checkpoints übertragen: Ihre Bedeutung wird durch das Vokabular des jeweiligen Trainingsdatensatzes bestimmt.
  — <https://huggingface.co/AlayaLab/Marionette>
- Das Modell nicht auf neue Geometrie anwenden, ohne einen neuen Terrain-Scan zu erstellen, und es nicht als allgemeines Modell für Figurenbewegung interpretieren.
  — <https://huggingface.co/AlayaLab/Marionette>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-08-13 — Der Roadmap-Status „pretrained weights uploading“ ist veraltet: Die Modellkarte von AlayaLab/Marionette listet nun die veröffentlichten Checkpoints und Ladeanweisungen auf.

## Weiterhin unbekannt {#still-unknown}

- Der Hugging-Face-Space `hugging-apps/marionette-world-model` lieferte bei der Überprüfung einen internen Fehler, daher sind sein tatsächliches Verhalten und sein Wartungsstatus nicht verifiziert.
- Das bereitgestellte Antwortschema enthält keine Felder `event_findings` oder `new_events`. Die ereignisspezifische Ergänzung zum 2026-08-18 ist daher unter `what_changed` festgehalten; die separat datierten Entwicklungen vom 2026-08-13 und 2026-08-14 sind dort ebenfalls erfasst.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://alayalab.github.io/Marionette/ | Marionette — Predicting World States, Rendering Geometry, Painting Appearance | 2026-09-05 |
| https://github.com/AlayaLab/Marionette | Repository AlayaLab/Marionette | 2026-09-05 |
| https://huggingface.co/AlayaLab/Marionette | AlayaLab/Marionette — Modellkarte der Gewichte | 2026-09-05 |
| https://arxiv.org/abs/2608.14530 | Marionette: Predicting World States, Rendering Geometry, Painting Appearance | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:marionette`, Thread `public-project-release`, 1 datiertes Ereignis 2026-08-18 → 2026-08-18.
- **Praktischer Hinweis:** Ab dem 2026-08-18 sollten Praktiker die verlinkte Projektseite, das Repository, die Hugging-Face-Modellseite und den gehosteten Space als Ausgangsbasis für die Bewertung von Marionette verwenden; Fähigkeiten, Lizenzierung und Reproduktionsschritte erfordern vor einem Einsatz dennoch eine Prüfung der Quellen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
