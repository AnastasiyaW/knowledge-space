---
title: "ViFeEdit — Öffentliche Projektpräsenz"
category: projects
date: 2026-03-18
tags: [project, public-project-presence, vifeedit]
aliases: ["ViFeEdit"]
level: 2
source_sha256: b2bdf130d24ca49c35cc3dfab92af1a8dc601339b9c0df7dcaa3a5d8ed65213e
translation: machine
translated_at: '2026-10-24'
---
# ViFeEdit — Öffentliche Projektpräsenz {#vifeedit-public-project-presence}

**Entwicklungslinie:** `project:vifeedit` · Thread `public-project-presence`  
**Letztes Ereignis:** 2026-03-18 · 1 datiertes Ereignis seit 2026-03-18 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ViFeEdit passt Wan und ähnliche Text-to-Video Diffusion Transformers für die Videogenerierung und -bearbeitung an, ohne Videotrainingsdaten zu verwenden.
- 3D-Attention-Reparametrisierung: trennt die räumliche Unabhängigkeit.
- Dual-Path-Pipeline: leitet getrennte Timestep-Embeddings über gepaarte 2D-Quell- und Zielbilder.

Das Training benötigt in der Praxis 100–250 gepaarte Bilder und weniger als 20 Epochen. Wir betrachten es als aufgabenspezifischen Tuning-Workflow und nicht als fertigen Video-Editor.

## Entwicklungslinie {#development-line}

- **2026-03-18 — Öffentliche ViFeEdit-Projektressourcen wurden verlinkt.** Am 2026-03-18 haben wir die Entwicklungslinie mit einem öffentlichen GitHub-Repository und einem Hugging-Face-Link verknüpft. Die Links identifizieren die Projektressourcen. Sie belegen weder ein Release, eine Version, eine Änderung der Fähigkeiten noch einen Veröffentlichungsstatus.

## Was sich geändert hat {#what-changed}

2026-03-16: Das ViFeEdit-Preprint stellte videofreies Tuning für Video-Diffusion-Transformers vor, das ausschließlich 2D-Bildpaare verwendet.  
2026-03-17: Die Autoren veröffentlichten Trainings- und Inferenzcode.  
2026-03-18: Das Projekt wurde über das verlinkte Repository verfügbar. Das Repository ergänzt die praktischen Grenzen, die in den Ereignislinks fehlen: 100–250 gepaarte Bilder pro Aufgabe, Training auf die ersten 20 Epochen begrenzt sowie ein Inferenzpfad mit optionaler Nachbearbeitung.

## Verwendung {#how-to-use-this}

Stand 2026-03-18 verwenden wir das verlinkte GitHub-Repository als primäre Projektquelle. Den Hugging-Face-Link behandeln wir als verwandte Ressource, bis die Recherche ihre Rolle bestätigt.

1. Klonen Sie das Repository und installieren Sie es mit `pip install -e .` in einer isolierten Python-Umgebung. Verwenden Sie eine bestehende DiffSynth-Conda-Umgebung nur, wenn ihre Abhängigkeiten kompatibel sind.
  — <https://github.com/Lexie-YU/ViFeEdit>
2. Erstellen Sie gepaarte Quell- und Zielbilder sowie eine `metadata_vife.csv`, die jeden Ziel-Prompt und jedes Zielbild dem Quellbild zuordnet, das als Referenz für das Inferenzvideo dient.
  — <https://github.com/Lexie-YU/ViFeEdit>
3. Legen Sie Daten- und Ausgabepfade in `train_vife.sh` fest, führen Sie das Skript aus und wählen Sie einen Checkpoint aus den ersten 20 Epochen, statt die konfigurierten 500 Epochen zu durchlaufen.
  — <https://github.com/Lexie-YU/ViFeEdit>
4. Konfigurieren Sie das mitgelieferte Inferenzbeispiel und führen Sie `python inference.py` aus. Verwenden Sie `postprocess.py` nur, wenn eine zusätzliche Ausrichtung der Ausgabe nötig ist.
  — <https://github.com/Lexie-YU/ViFeEdit>

## Bewährte Praktiken {#best-practices}

- Beginnen Sie mit einer eng definierten Bearbeitung und 100–250 gepaarten Bildern. Halten Sie die Paarung von Quelle und Ziel sowie die Dateinamen in den Metadaten konsistent, da das Training das Quellbild später als Quellvideo-Referenz verwendet.
  — <https://github.com/Lexie-YU/ViFeEdit>
- Betrachten Sie die ersten 20 Epochen als praktisches Trainingsfenster. Bewerten Sie Checkpoints dort, bevor Sie einen Lauf verlängern.
  — <https://github.com/Lexie-YU/ViFeEdit>
- Fixieren Sie `transformers==4.55.0` oder prüfen Sie die Version. Schlägt die editierbare Installation an `pkg_resources` fehl, verwenden Sie das im Repository dokumentierte Flag `--no-build-isolation`, statt die Abhängigkeiten zu ändern.
  — <https://github.com/Lexie-YU/ViFeEdit>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin ungeklärt {#still-unknown}

- Das Repository dokumentiert Code, Datenvorbereitung und Inferenz, nennt aber keinen herunterladbaren ViFeEdit-Checkpoint und kein unterstütztes Zielsystem für den produktiven Einsatz.
- In den hier verwendeten Quellen existiert keine erstrangige Release-Notiz nach dem 2026-03-18.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/Lexie-YU/ViFeEdit | Lexie-YU/ViFeEdit — Repository-README | 2026-09-05 |
| https://arxiv.org/abs/2603.15478 | ViFeEdit: A Video-Free Tuner of Your Video Diffusion Transformer | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:vifeedit`, Thread `public-project-presence`, 1 datiertes Ereignis 2026-03-18 → 2026-03-18.
- **Praktischer Hinweis:** Stand 2026-03-18 das verlinkte GitHub-Repository als identifizierte Projektquelle verwenden. Den Hugging-Face-Link als verwandte Ressource behandeln, bis die Recherche seine genaue Rolle klärt.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
