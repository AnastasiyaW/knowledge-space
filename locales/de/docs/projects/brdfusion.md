---
title: "BRDFusion"
category: projects
date: 2026-06-22
tags: [brdfusion, project]
aliases: ["BRDFusion"]
level: 2
source_sha256: 2a4b0c4597278df792d184bc9095cdb87748dc3d48b34fe2bd429ed7b2e6e003
translation: machine
translated_at: '2026-10-24'
---
# BRDFusion {#brdfusion}

**Entwicklungslinie:** `project:brdfusion` · Thread `brdfusion`  
**Letztes Ereignis:** 2026-06-22 · 1 datiertes seit 2026-06-22 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

BRDFusion ist eine offene Forschungspipeline, die urbanes Video in eine steuerbare 3D-Gaussian/PBR-Szene überführt. Sie steht UrbanIR mit diffusionsbasierter Verfeinerung näher als einem allgemeinen Videogenerator.

- Geometrie, Materialien und HDR-Beleuchtung: Sie werden aus dem Video rekonstruiert.
- Neue Ansichten und Neubeleuchtung: Beides wird über PBR gerendert.
- Gerendertes Video: Bilder werden mit DiffusionRenderer verfeinert.
- Szenenbearbeitung: Unterstützt werden Nachtsimulation, lokale Lichtquellen, Scheinwerfer und Bearbeitungen dynamischer Objekte.

Getestet unter Ubuntu 22.04 mit einer RTX A6000; Gen. Render kann mehr als 24 GB VRAM benötigen.
Wir nutzen es für reproduzierbare Forschung und Fahrszenensimulation auf einem Linux-GPU-Stack, nicht als leichtgewichtigen Workflow mit einem einzigen Modell.

## Entwicklungslinie {#development-line}

- **2026-06-22 — Ressourcen des BRDFusion-Projekts wurden veröffentlicht.** Am 2026-06-22 verlinkte BRDFusion seine Projektseite, das Quellcode-Repository und die Checkpoint-Sammlung. Mit dieser Veröffentlichung sind Implementierung und Modellartefakte öffentlich, sodass Forschende sie finden und nutzen können.

## Was sich geändert hat {#what-changed}

- 2026-06-15 — arXiv v1 stellte die hybride Physik-und-Generierungs-Methode von BRDFusion für inverses und direktes Rendering urbaner Szenen vor.
- 2026-06-22 — Projektseite, öffentlicher Code und vortrainierte Checkpoint-Ressourcen wurden als nutzbare Forschungsveröffentlichung verlinkt.

## Anwendung {#how-to-use-this}

Ab 2026-06-22 können wir das Projekt ausgehend von der verlinkten BRDFusion-Projektseite, dem Quellcode-Repository und der Checkpoint-Sammlung evaluieren oder reproduzieren.

1. Vor der Installation die dokumentierten Voraussetzungen für Linux, Compiler, CUDA und GPU prüfen; das Projekt verwendet getrennte Umgebungen `brdfusion` und `cosmos-predict1`.
  — <https://github.com/shigon255/BRDFusion>
2. Rekursiv klonen, beide Conda-Umgebungen erstellen, sich bei Hugging Face für die DiffusionRenderer-Gewichte authentifizieren und das erforderliche SMPL-Asset bereitstellen.
  — <https://github.com/shigon255/BRDFusion>
3. Eine bereitgestellte vorverarbeitete Szene und den passenden Checkpoint mit einer Kamera herunterladen, unter `ckpt/` entpacken und anschließend `bash scripts/stage_ckpt.sh` ausführen.
  — <https://github.com/shigon255/BRDFusion>
4. `tools/run_pipeline.py` mit `--stage render` für PBR-Ausgabe ausführen; für optional `--stage gen_render` die passende Szene, Kamera, Frame-Range und das passende Render-Ziel verwenden.
  — <https://github.com/shigon255/BRDFusion>
5. Für Neubeleuchtung oder Szenenbearbeitung die dokumentierten Umgebungsvariablen oder JSON-Spezifikationen setzen und `scripts/applications/render.sh` gegen einen bereitgestellten Checkpoint aufrufen.
  — <https://github.com/shigon255/BRDFusion>

## Bewährte Vorgehensweisen {#best-practices}

- Für Inferenz oder Evaluation zunächst die bereitgestellten Daten und vortrainierten Checkpoints verwenden, bevor Training oder neue Waymo-Szenen-Vorverarbeitung versucht wird.
  — <https://github.com/shigon255/BRDFusion>
- Nur die Szenen-Teilmenge herunterladen, die für ein Experiment benötigt wird; Training, Rendering und Metriken arbeiten pro Szene.
  — <https://github.com/shigon255/BRDFusion>
- Datensatz, Szene bzw. Pfad, Kameraeinstellung, Frame-Range und Render-Ziel zwischen Render und Gen. Render identisch halten.
  — <https://github.com/shigon255/BRDFusion>
- `--dry_run` verwenden, um ausgewählte Befehle und das Pipeline-Manifest vor aufwendigen Schritten zu prüfen; bereits vorhandene Stage-Ausgaben werden übersprungen, sofern nicht `--rerun_existing` angegeben ist.
  — <https://github.com/shigon255/BRDFusion>
- `NO_PBR=1` und `PRINT_CMD=1` setzen, um Geometrie, Kamerapfade oder erzeugte Befehle vor einem vollständigen Anwendungsrendering zu prüfen.
  — <https://github.com/shigon255/BRDFusion>

## Dadurch ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Wir haben keine datierte primäre Versionsnotiz für eine Code- oder Checkpoint-Änderung am 2026-06-22 selbst gefunden; das Datum belegt das Verlinkungsereignis, aber keine separate Upstream-Version.
- Das Repository dokumentiert 35 Commits, ohne dass in der verfügbaren Recherche ein datierter Commit-Verlauf zugänglich war. Daher können wir die aktuellen README-Funktionen keinem Entwicklungsereignis nach dem 22. Juni zuordnen.
- Der Quellcode steht unter der MIT-Lizenz, während die Checkpoint-Karte mit `License: other` gekennzeichnet ist; Nutzungsbedingungen für Checkpoints und mitgelieferte Drittanbieter-Komponenten müssen vor einem kommerziellen Einsatz geprüft werden.
- Wir haben keine unabhängige Reproduktion, keine Messung der Laufzeitleistung und keine Belege für einen produktiven Einsatz gefunden.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://shigon255.github.io/brdfusion-page/ | BRDFusion: Physics Meets Generation for Urban Scene Inverse Rendering — Projektseite | 2026-09-05 |
| https://github.com/shigon255/BRDFusion | shigon255/BRDFusion — offizielles Quellcode-Repository und Nutzungsanleitung | 2026-09-05 |
| https://huggingface.co/Shigon/BRDFusion_checkpoints | Shigon/BRDFusion_checkpoints — offizielle vortrainierte Checkpoints | 2026-09-05 |
| https://arxiv.org/abs/2606.17049 | BRDFusion: Physics Meets Generation for Urban Scene Inverse Rendering — arXiv v1, eingereicht 2026-06-15 | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:brdfusion`, Thread `brdfusion`, 1 datiertes Ereignis 2026-06-22 → 2026-06-22.
- **Praktischer Hinweis:** Ab 2026-06-22 die verlinkte BRDFusion-Projektseite, das Quellcode-Repository und die Checkpoint-Sammlung verwenden, um das Projekt zu evaluieren oder zu reproduzieren.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
