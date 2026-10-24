---
title: "OpenPose Studio für ComfyUI — Projektentwicklung"
category: projects
date: 2026-07-28
tags: [comfyui-openpose-studio, comfyui_openpose_studio, project, project-development]
aliases: ["OpenPose Studio for ComfyUI"]
level: 2
source_sha256: f4301fc023d765bed1ddb90fa6a9f056b7d624069c88849372d9ccb1b1f01733
translation: machine
translated_at: '2026-10-24'
---
# OpenPose Studio für ComfyUI — Projektentwicklung {#openpose-studio-for-comfyui-project-development}

**Entwicklungslinie:** `project:comfyui-openpose-studio` · Thread `project-development`  
**Letztes Ereignis:** 2026-07-28 · 1 datiertes Ereignis seit 2026-07-28 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Worum es geht {#what-it-is}

OpenPose Studio für ComfyUI ist ein Posen-Editor innerhalb von ComfyUI für Künstler, die das Skelett, die Hände oder das JSON korrigieren wollen, statt das Ergebnis des Pose-Estimators unverändert zu übernehmen. Funktionen: COCO-18-Körper, punktweise Korrektur der Hände, Galerie und Zusammenführung von JSON-Posen, DWPose-Eingang sowie IMAGE/JSON/KPS-Ausgänge. Einschränkung: Gesichtspunkte werden gespeichert und gerendert, lassen sich aber nicht einzeln bearbeiten. Fazit: Dies ist eine praktische Alternative zu einem eigenständigen OpenPose-Editor, wenn die Posenkontrolle ohnehin im ComfyUI-Graphen benötigt wird.

## Entwicklungslinie {#development-line}

- **2026-07-28 — ComfyUI-OpenPose-Studio-Repository referenziert.** Der Handeditor erhielt mehr Arbeitsfläche, und Hintergrundreferenzen sowie Hilfslinien wurden für den vergrößerten Modus korrigiert.

## Was sich geändert hat {#what-changed}

2026-07-28 — Der aktuelle nächste Stand war OpenPose Studio 2.0.2: Der Handeditor erhielt mehr Arbeitsfläche, und Hintergrundreferenzen sowie Hilfslinien wurden für den vergrößerten Modus korrigiert. 2026-07-29 — Version 2.1.0 ergänzte eine Vorschau der ausgewählten Pose in der Galerie, 14 Handgesten sowie Werkzeuge zum Wiederherstellen und Löschen von Handpunkten. 2026-07-30 — Version 2.1.1 ergänzte eine Lokalisierung für Hindi. 2026-08-08 — Version 2.2.0 ergänzte das Einfügen einer fehlenden Hand per Drag-and-drop, die Auswahl der Handflächenausrichtung und eine Update-Benachrichtigung. 2026-08-14 — Version 2.3.0 ergänzte eine adaptive Touch-Oberfläche und eine kompakte mobile Galerie.

## Anwendung {#how-to-use-this}

Stand 2026-07-28 sollten Anwender ComfyUI-OpenPose-Studio als Projekt behandeln, das anhand des verlinkten GitHub-Repositorys zu bewerten ist; der vorliegende Stand erlaubt noch keine spezifischere Empfehlung zur Installation oder zum Workflow.

1. Öffnen Sie im ComfyUI Extension Manager den Nodes Manager, suchen Sie nach `openpose-studio`, installieren Sie die Erweiterung und starten Sie ComfyUI neu.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
2. Fügen Sie den Knoten `image > OpenPose Studio` hinzu, öffnen Sie den Editor über die Vorschau, wählen Sie eine Pose aus einer Voreinstellung oder der Galerie und ziehen Sie die Schlüsselpunkte an die gewünschte Position.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
3. Klicken Sie auf Apply; verbinden Sie `image` mit den nachfolgenden Image-Knoten und `kps` mit einem ControlNet- oder OpenPose-kompatiblen Knoten.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
4. Um das Ergebnis des Detektors zu korrigieren, verbinden Sie den Ausgang des DWPose Estimator mit dem optionalen Eingang `pose_keypoint` und verfeinern Sie anschließend die Punkte im Editor.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>

## Bewährte Praktiken {#best-practices}

- Prüfen Sie JSON vor dem Import: Erforderlich sind numerische Koordinaten und eine Struktur mit `pose_keypoints_2d`; für den Körper werden 18 Schlüsselpunkte erwartet.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
- Skalieren Sie Posen mit abweichenden Abmessungen zuerst auf die Zielauflösung: Pose Merger gleicht die Auflösung einer Sammlung nicht automatisch an.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
- Wenn der Editor oder die Vorschau nicht erscheint, starten Sie ComfyUI vollständig neu, führen Sie ein hartes Neuladen der Seite durch und prüfen Sie die Browser-Konsole und das Startup-Log.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
- Verwenden Sie Hintergrundbilder nur als temporäre Referenz: Sie bleiben innerhalb der ComfyUI-Sitzung erhalten, werden aber nicht im Workflow gespeichert.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>

## Durch diesen Stand ersetzt {#superseded-by-this}

- 2026-07-29: Die bisherige Galerie ohne Vorschau der ausgewählten Pose und ohne 14 integrierte Handgesten wurde durch das Verhalten von 2.1.0 ersetzt.
- 2026-08-08: Der bisherige manuelle Weg zum Hinzufügen fehlender Hände wurde durch das unterstützte Einfügen per Drag-and-drop auf die Arbeitsfläche in 2.2.0 ersetzt.
- 2026-08-14: Das bisherige, auf den Desktop ausgerichtete Layout wurde durch die adaptiven Touch-Ansichten von 2.3.0 ersetzt.

## Weiterhin unbekannt {#still-unknown}

- Für das Ereignis vom 2026-07-28 wurde kein eigenständiges primäres Release und kein Commit mit genau diesem Datum gefunden. Das bestätigte nächste Release 2.0.2 ist im Changelog des Autors auf 2026-07-27 datiert; seine Details werden daher als Präzisierung zum Ereignis angegeben, nicht als neuer Schritt am 2026-07-28.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/andreszs/ComfyUI-OpenPose-Studio | andreszs/ComfyUI-OpenPose-Studio — Repository | 2026-09-05 |
| https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/CHANGELOG.md | OpenPose Studio Changelog | 2026-09-05 |
| https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md | OpenPose Studio Dokumentation | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:comfyui-openpose-studio`, Thread `project-development`, 1 datiertes Ereignis vom 2026-07-28 bis 2026-07-28.
- **Praktischer Hinweis:** Stand 2026-07-28 sollten Anwender ComfyUI-OpenPose-Studio als Projekt behandeln, das anhand des verlinkten GitHub-Repositorys zu bewerten ist; der vorliegende Stand erlaubt noch keine spezifischere Empfehlung zur Installation oder zum Workflow.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.
