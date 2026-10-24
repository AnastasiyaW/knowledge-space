---
title: "Frame Extractor"
category: projects
date: 2026-08-21
tags: [frame-extractor, project]
aliases: ["Frame Extractor"]
level: 2
source_sha256: 592d77c92e7cc396c41288dc9ed3f8fa398f7c5a42fe12b31be03935d4a9cd47
translation: machine
translated_at: '2026-10-24'
---
# Frame Extractor {#frame-extractor}

**Entwicklungslinie:** `project:frame-extractor` · Thread `frame-extractor`  
**Letztes Ereignis:** 2026-08-21 · 1 datiertes seit 2026-08-21 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Frame Extractor ist eine lokale GUI und CLI zur Umwandlung von Videos in eine Bildfolge für SfM und Gaussian Splatting. — passt die Bilddichte an die Kamerabewegung an; — unterstützt ein festes Intervall, ausgewählte Abschnitte der Zeitleiste und manuellen Export; — speichert JPEG/PNG, ein CSV-Manifest, Einstellungen und eine Zusammenfassung neben den Bildern. Der aktuelle Testrelease ist v0.2.0-rc.2; macOS auf Apple Silicon bleibt die wichtigste manuell getestete Plattform. Fazit: Für die Vorbereitung von Videoaufnahmen zur 3D-Rekonstruktion sollte das neue C++-GUI-Projekt verwendet werden, nicht das ursprüngliche Python-CLI.

## Entwicklungslinie {#development-line}

- **2026-08-21 — Frame-Extractor-Repository als Projektentwicklungsreferenz verknüpft.** Am 2026-08-21 enthielt die Entwicklungslinie von Frame Extractor einen Link zu seinem GitHub-Repository. Dies stellt eine datierte öffentliche Referenz für das Projekt dar, die verfügbaren Belege nennen jedoch kein bestimmtes Release, Feature, keine bestimmte Änderung und keine konkrete Betriebsfähigkeit.

## Was sich geändert hat {#what-changed}

2026-08-15 — Das ursprüngliche Python-Frame-Extractor erhielt eine Überarbeitung der Timing-Pipeline, strengere Tests, zeitgestempelte Frame-Manifeste und die verpflichtende Extraktion des letzten erfolgreich verarbeiteten Frames. 2026-08-21 — Frame Extractor war als Python-Werkzeug verfügbar, das ein reguläres Punktraster mittels dichtem OpenCV-DIS-Optical-Flow verfolgt und Keyframes anhand des kumulierten Versatzes und des Verlusts von Punkten auswählt. 2026-09-05 — Das ursprüngliche Repository wurde als Projekt markiert, dessen weitere Entwicklung in Adaptive Frame Extractor übergegangen ist: eine plattformübergreifende C++20-Anwendung mit GUI, CLI, Zeitleistenregionen und fertigen Paketen.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-08-21 sollten Anwender das verlinkte Frame-Extractor-Repository als datierte Projektreferenz betrachten, die vor dem Vertrauen auf seinen Workflow geprüft werden sollte; seine Funktionen und sein Release-Status bleiben unverifiziert.

1. Öffnen Sie Adaptive Frame Extractor, ziehen Sie ein Video hinein und wählen Sie das Ausgabeverzeichnis.
  — <https://github.com/morishuz/adaptive-frame-extractor>
2. Wählen Sie Low, Medium oder High für die adaptive Auswahl oder ein fixed interval und markieren Sie bei Bedarf die gewünschten Regionen auf der Zeitleiste.
  — <https://github.com/morishuz/adaptive-frame-extractor>
3. Wählen Sie JPEG oder PNG und starten Sie die Extraktion; verwenden Sie keyframes.csv und summary.txt als Eingabemanifest für COLMAP oder Gaussian Splatting.
  — <https://github.com/morishuz/adaptive-frame-extractor>
4. Für die Automatisierung starten Sie das CLI: ./build/release/frame-extractor input.mp4 --output-dir output.
  — <https://github.com/morishuz/adaptive-frame-extractor>

## Best Practices {#best-practices}

- Bei ungleichmäßiger Kamerabewegung beginnen Sie mit dem adaptiven Preset: Ein festes Intervall erzeugt bei Stillstand Duplikate und kann bei schneller Bewegung eine unzureichende Überlappung hinterlassen.
  — <https://github.com/morishuz/adaptive-frame-extractor>
- Beschränken Sie die Extraktion auf sinnvolle Zeitleistenregionen und bewahren Sie das CSV-Manifest zusammen mit den Bildern auf, damit die Rekonstruktion nachvollziehbar bleibt.
  — <https://github.com/morishuz/adaptive-frame-extractor>
- Übergeben Sie im Legacy-CLI explizit configs/default.yaml für einen reproduzierbaren Lauf; Parameter für DIS, Raster, Bewegungsschätzung und Schwellenwerte sind in einer YAML-Datei zusammengefasst.
  — <https://github.com/morishuz/frame-extractor>

## Abgelöst durch dieses {#superseded-by-this}

- 2026-09-05 — Die Empfehlung, das Python-Projekt über uv zu installieren und weiterzuentwickeln, ist für neue Anwender veraltet: Das Repository selbst verweist die weitere Entwicklung auf Adaptive Frame Extractor.
- 2026-09-05 — Der reine Python-Start mit Umgebungskonfiguration wurde durch eine fertige plattformübergreifende GUI-Anwendung ersetzt; das Legacy-CLI bleibt für bestehende Skripte verwendbar.

## Weiterhin unbekannt {#still-unknown}

- Für das Datum 2026-08-21 gibt es neben dem Link zum ursprünglichen Repository keine eigene datierte Primärquelle; daher ist event_findings bewusst leer. Das Startdatum von Adaptive Frame Extractor und von v0.2.0-rc.2 konnte über die verfügbare GitHub-Releases-Seite nicht bestätigt werden.
- event_findings=[]
- new_events=[{"date":"2026-08-15","source_date":"2026-08-15","summary":"Das ursprüngliche Python-Projekt erhielt ein Refactoring der Timing-Pipeline, erweiterte Testabdeckung, zeitgestempelte Keyframe-Manifeste und die Extraktion des letzten Frames.","source_url":"https://github.com/morishuz/frame-extractor/commits/main/"},{"date":"2026-09-05","source_date":"2026-09-05","summary":"Die aktuelle Dokumentation des ursprünglichen Projekts verweist neue Anwender auf Adaptive Frame Extractor, eine plattformübergreifende C++20-GUI und CLI mit lokaler Verarbeitung.","source_url":"https://github.com/morishuz/frame-extractor"}]} еиц assistant to=developer? Nein. Wir haben ungültiges JSON ausgegeben! Ich habe versehentlich Felder `

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/morishuz/frame-extractor | GitHub — morishuz/frame-extractor | 2026-09-05 |
| https://github.com/morishuz/frame-extractor/commits/main/ | GitHub — commit history for morishuz/frame-extractor | 2026-09-05 |
| https://github.com/morishuz/adaptive-frame-extractor | GitHub — morishuz/adaptive-frame-extractor | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:frame-extractor`, Thread `frame-extractor`, 1 datiertes Ereignis vom 2026-08-21 bis 2026-08-21.
- **Praktischer Hinweis:** Stand 2026-08-21 sollten Anwender das verlinkte Frame-Extractor-Repository als datierte Projektreferenz betrachten, die vor dem Vertrauen auf seinen Workflow geprüft werden sollte; seine Funktionen und sein Release-Status bleiben unverifiziert.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich für das, was veraltet ist.
