---
title: "PowerPaint"
category: projects
date: 2024-07-21
tags: [powerpaint, project]
aliases: ["PowerPaint"]
level: 2
source_sha256: 94a5edbe5069756a3a5ef6c13f601ab344923e7e0fb47fe390dd2d7e10da051f
translation: machine
translated_at: '2026-10-24'
---
# PowerPaint {#powerpaint}

**Entwicklungslinie:** `project:powerpaint` · Thread `powerpaint`  
**Letztes Ereignis:** 2024-07-21 · 2 datierte Ereignisse seit 2023-12-12 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

PowerPaint ist ein auf Stable Diffusion basierendes Inpainting-System zur Bearbeitung maskierter Bildbereiche.

- Textgesteuertes Einfügen von Objekten, um Elemente aus Textprompts hinzuzufügen.
- Promptfreies Entfernen von Objekten mit optionalen Negative Prompts, um Objekte zu löschen.
- Image Outpainting, um Canvas-Grenzen zu erweitern.
- Formgesteuertes Einfügen von Objekten, um hinzugefügte Elemente an einen Masken-Umriss anzupassen.

## Entwicklungslinie {#development-line}

- **2023-12-12 — PowerPaint wurde öffentlich verfügbar.** Am 2023-12-12 startete das Projekt über seine Website, eine MMagic-Implementierung und eine OpenXLab-Anwendungsseite.
- **2024-07-21 — Link zum eigenständigen OpenMMLab-Repository.** Am 2024-07-21 verwies PowerPaint auf das eigenständige Repository open-mmlab/PowerPaint. Die Links markieren diesen Wechsel, zeigen aber keine Code- oder Modelländerungen.

## Was sich geändert hat {#what-changed}

- 2023-12-12 — Das Paper zu PowerPaint führte lernbare Task-Prompts ein, sodass ein einziges Modell Context Filling, Objekteinfügung, Entfernung und Formführung abdeckt.
- 2023-12-18 — Stable-v1-Gewichte ersetzten den früheren Build.
- 2023-12-22 — Die Maintainer behoben im Demo-Pfad den Fehler beim Laden von ControlNet.
- 2024-04-06 — Ein Retraining mit BrushNet ergab PowerPaint v2 und behielt die Cross-Attention-Schichten für Task-Prompts bei.
- 2024-04-07 — Code und Gewichte von PowerPaint v2 wurden veröffentlicht.
- 2024-05-22 — Die Gewichte PowerPaint v2-1 ersetzten die ursprünglichen v2-Gewichte, um Trainingsprobleme zu beheben.
- 2024-07-21 — Das öffentliche Repository war verfügbar, sein Changelog verzeichnet jedoch keine eigene Modellveröffentlichung am 21. Juli.

## So verwenden Sie es {#how-to-use-this}

Ab 2023-12-12 lief das Projekt über seine Website, MMagic und OpenXLab; ab 2024-07-21 verwenden Sie das eigenständige OpenMMLab-Repository.

1. Klonen Sie das Repository, erstellen Sie eine Conda-Umgebung mit Python 3.9 und installieren Sie die fixierten Anforderungen.
  — <https://github.com/open-mmlab/PowerPaint>
2. Installieren Sie Git LFS und laden Sie dann den PowerPaint-v2-Checkpoint in ein lokales Checkpoint-Verzeichnis herunter.
  — <https://github.com/open-mmlab/PowerPaint>
3. Starten Sie die Gradio-UI für v2 mit `python app.py --share --version ppt-v2 --checkpoint_dir checkpoints/ppt-v2`.
  — <https://github.com/open-mmlab/PowerPaint>
4. Laden Sie ein Bild hoch, malen Sie die Bearbeitungsmaske, wählen Sie den Task-Tab und geben Sie nur für das Einfügen von Objekten oder die Formführung Text ein.
  — <https://github.com/open-mmlab/PowerPaint>
5. Lassen Sie den Textprompt für Entfernung oder Outpainting leer; legen Sie für Outpainting die horizontalen und vertikalen Erweiterungsverhältnisse fest.
  — <https://github.com/open-mmlab/PowerPaint>

## Best Practices {#best-practices}

- Lassen Sie den Prompt für das Entfernen von Objekten leer; wenn unerwünschte Objekte auftauchen, fügen Sie einen Negative Prompt hinzu und erhöhen Sie Guidance Scale auf 10 oder mehr.
  — <https://github.com/open-mmlab/PowerPaint>
- Setzen Sie Fitting degree auf 0,5–0,6, wenn das Objekt von der Maske abweichen darf, und auf 0,8–0,95, um die Maskenform genau zu treffen.
  — <https://github.com/open-mmlab/PowerPaint>
- Verwenden Sie die Gewichte v2-1 statt der ursprünglichen v2-Version, da die Maintainer v2-1 gerade zur Behebung von Trainingsproblemen veröffentlicht haben.
  — <https://github.com/open-mmlab/PowerPaint>

## Hierdurch ersetzt {#superseded-by-this}

- 2023-12-22 — Die frühe Anleitung zur ControlNet-Demo ist veraltet, da die Ladelogik behoben wurde.
- 2024-05-22 — Die ursprünglichen Gewichte von PowerPaint v2 wurden durch v2-1 ersetzt, das Trainingsprobleme korrigiert.

## Noch unbekannt {#still-unknown}

- Das Repository enthält kein getaggtes Release für eine eigenständige Veröffentlichung am 2024-07-21; das Datum könnte eher einen Umzug des Repositorys als ein Modell-Update widerspiegeln.
- Die Dokumentation behandelt die lokale Einrichtung und die Gradio-UI, lässt jedoch GPU-Speicherlimits, Unterstützung für Betriebssysteme und die Kompatibilität mit Diffusers aus.
- Weder die ursprüngliche Projektseite noch der OpenXLab-Demo-Endpunkt lieferten bei dieser Prüfung verwertbare technische Details.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://arxiv.org/abs/2312.03594 | A Task is Worth One Word: Learning with Task Prompts for High-Quality Versatile Image Inpainting | 2026-09-04 |
| https://github.com/open-mmlab/mmagic | MMagic — OpenMMLab generative-image and video toolbox | 2026-09-04 |
| https://github.com/open-mmlab/PowerPaint | open-mmlab/PowerPaint | 2026-09-04 |
| https://huggingface.co/JunhaoZhuang/PowerPaint_v2 | JunhaoZhuang/PowerPaint_v2 | 2026-09-04 |

## Agenten-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:powerpaint`, Thread `powerpaint`, 2 datierte Ereignisse 2023-12-12 → 2024-07-21.
- **Praxishinweis:** Ab 2023-12-12 war PowerPaint über seine Website, MMagic und OpenXLab zu finden; ab 2024-07-21 ist das eigenständige OpenMMLab-Repository maßgeblich.
- **Konfidenz:** mittel. Die datierten Ersetzungsangaben oben sind maßgeblich dafür, was veraltet ist.
