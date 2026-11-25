---
title: "Lucida"
category: projects
date: 2026-07-21
tags: [lucida, lucida-development, project]
aliases: ["Lucida"]
level: 2
source_sha256: 294112d318599a234887dcbcdfef65d084c7d1b1081d507c2cc39f669b6c7694
translation: machine
translated_at: '2026-10-24'
---
# Lucida {#lucida}

**Entwicklungslinie:** `project:lucida` · Thread `lucida-development`  
**Letztes Ereignis:** 2026-07-21 · 1 datiertes seit 2026-07-21 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Lucida ist ein MIT-lizenziertes Modell für Segmentierung und Alpha-Matting für Nutzer, bei denen RMBG-2.0 oder ein gewöhnlicher Background Remover halbtransparente und feine Details verliert.

Funktionen: RGBA-Ausgabe, lokaler Start über Python, CLI oder HTTP, Transformers und ComfyUI.

Messwert: Ein veröffentlichter Test an 203 Bildern ergibt einen mittleren MAE von 0,0257 für die aktuellen v7-Gewichte.

Fazit: Wählen Sie das Modell für Text, Drucke, Camouflage und Illustrationen; bei feinen Strukturen, komplexen Szenen und Haaren bleiben die gemessenen Konkurrenten stärker.

## Entwicklungslinie {#development-line}

- **2026-07-21 — Lucida-Entwicklungsressourcen wurden verlinkt.** Die Kategorie print-design/sticker wurde hinzugefügt, der mittlere MAE beträgt auf 203 Bildern nun 0,0257, und das Modell erschien in der offiziellen ComfyUI-Modellsammlung.

## Was sich geändert hat {#what-changed}

2026-07-13 — Lucida v1.0 wurde veröffentlicht: die erste öffentliche Version mit MIT-Gewichten, Unterstützung für Transformers und einem Test an 191 Bildern in acht Kategorien. 2026-07-18 — v1.1 ergänzte Training auf 9 426 Paaren zur Erhaltung undurchsichtiger Teile transparenter Objekte und an den Bildrand abgeschnittener Objekte; der Transparenz-MAE verschlechterte sich von 0,0376 auf 0,0403. 2026-07-21 — zum Zeitpunkt dieses Schritts war Lucida v1.2 vom 2026-07-20 das aktuelle Release: Die Kategorie print-design/sticker wurde hinzugefügt, der mittlere MAE beträgt auf 203 Bildern nun 0,0257, und das Modell erschien in der offiziellen ComfyUI-Modellsammlung. 2026-07-23 — v1.3 veröffentlichte v13 mit einem Loss für Hintergrundsauberkeit und einem „Soup“ aus Checkpoints; der angegebene mittlere MAE lag bei 0,0250. 2026-07-24 — die v13-Gewichte wurden wegen einer Regression bei mehrschichtigen realen Illustrationen zurückgezogen; das Modell liefert wieder die v7-Gewichte aus, und v14 ist als laufende Arbeit gekennzeichnet.

## Verwendung {#how-to-use-this}

Ab 2026-07-21 sollten Praktiker das GitHub-Repository von Lucida, die Hugging-Face-Modellseite und die verlinkten Showcase- bzw. Demo-Spaces als datierte Ausgangspunkte behandeln, um das Projekt zu bewerten oder zu reproduzieren, und Versionen sowie Fähigkeiten unabhängig überprüfen.

1. Installieren Sie das Projekt mit Python 3.12+ über uv und führen Sie `uv run bgr remove input.jpg -o output.png --model lucida` aus; speichern Sie das Ergebnis als PNG, damit der Alpha-Kanal nicht verloren geht.
  — <https://github.com/egeorcun/lucida>
2. Für Python laden Sie `egeorcun/lucida` über `AutoModelForImageSegmentation` oder eine Pipeline mit `trust_remote_code=True`; bringen Sie die Eingabe in RGB.
  — <https://huggingface.co/egeorcun/lucida>
3. Für ComfyUI laden Sie `lucida.safetensors` in `ComfyUI/models/background_removal/` herunter und öffnen den beiliegenden Workflow Remove Background (BiRefNet).
  — <https://github.com/egeorcun/lucida>
4. Für eine schnelle Prüfung ohne lokale Installation laden Sie ein Bild in die Gradio-Demo hoch, die auf ZeroGPU läuft.
  — <https://huggingface.co/spaces/egeorcun/lucida-demo>

## Best Practices {#best-practices}

- Verwenden Sie für die Inferenz 1024×1024: Das ist die empfohlene und die Trainingsauflösung; skalieren Sie das Alpha anschließend auf die ursprüngliche Größe zurück.
  — <https://github.com/egeorcun/lucida>
- Vergleichen Sie bei komplexen Mehrobjekt-Bildern, feinen Konstruktionen und Haaren das Ergebnis mit InSPyReNet oder RMBG-2.0, statt eine generelle Überlegenheit von Lucida anzunehmen.
  — <https://github.com/egeorcun/lucida>
- Verwenden Sie v13 nicht: Die veröffentlichten Gewichte wurden nach einer festgestellten Regression bei realen Layered-Design-Bildern auf v7 zurückgesetzt.
  — <https://github.com/egeorcun/lucida/releases>
- Prüfen Sie vor einer kommerziellen Nutzung das Lizenzrisiko selbst: Einige Trainingsdatensätze sind als nur für Forschung angegeben, obwohl Code und Gewichte unter MIT veröffentlicht wurden.
  — <https://github.com/egeorcun/lucida>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2026-07-18: v1.0 wurde durch v1.1 ersetzt, für transparente Objekte mit undurchsichtigen Teilen und Objekte am Bildrand.
- 2026-07-20: v1.1 wurde durch v1.2/v7 für Aufgaben mit print-design und Sticker-Art ersetzt.
- 2026-07-24: Die Anleitung, v13 zu verwenden, ist veraltet; die veröffentlichten Gewichte wurden wegen einer Regression bei mehrschichtigen Illustrationen auf v7 zurückgesetzt.

## Weiterhin unbekannt {#still-unknown}

- Die vollständige Veröffentlichung vom 2026-07-21 enthält keinen Text, daher ist ihre genaue Kernaussage nicht rekonstruiert; der Bezug des Schritts zu v1.2 ergibt sich aus dem nächstliegenden primären Release vom 2026-07-20 und aus Verlinkungen auf dasselbe Repository, dieselben Gewichte und dieselbe Demo.
- Das Antwortschema enthält keine eigenen Felder event_findings und new_events; deren Angaben sind in der Chronologie what_changed enthalten.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/egeorcun/lucida | egeorcun/lucida — README | 2026-09-05 |
| https://huggingface.co/egeorcun/lucida | egeorcun/lucida — Hugging Face model card | 2026-09-05 |
| https://huggingface.co/spaces/egeorcun/lucida-demo | Lucida — Background Removal demo | 2026-09-05 |
| https://github.com/egeorcun/lucida/releases | egeorcun/lucida — GitHub releases | 2026-09-05 |

## Agent-Zusammenfassung {#agent-brief}

- **Gegenstand:** `project:lucida`, Thread `lucida-development`, 1 datiertes Ereignis vom 2026-07-21 bis 2026-07-21.
- **Praktischer Hinweis:** Ab 2026-07-21 sollten Praktiker das GitHub-Repository von Lucida, die Hugging-Face-Modellseite und die verlinkten Showcase- bzw. Demo-Spaces als datierte Ausgangspunkte behandeln, um das Projekt zu bewerten oder zu reproduzieren, und Versionen sowie Fähigkeiten unabhängig überprüfen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
