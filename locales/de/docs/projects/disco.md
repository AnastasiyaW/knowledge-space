---
title: "DisCO"
category: projects
date: 2023-07-11
tags: [disco, disco-development, project]
aliases: ["DISCO", "DisCO", "DisCo"]
level: 2
source_sha256: dd67efdc71b4f62d2263e33773838623a598703526afbe5120b80c538daa7f01
translation: machine
translated_at: '2026-10-24'
---
# DisCO {#disco}

**Entwicklungslinie:** `project:disco` · Thread `disco-development`  
**Letztes Ereignis:** 2023-07-11 · 3 datierte Einträge seit 2022-10-20 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

DisCO umfasst drei aufgabenspezifische Forschungsimplementierungen für Bildpraktiker und stellt kein einzelnes einsetzbares Werkzeug dar.

- DISCO colorisiert Graustufenbilder über globale Farbanker.
- Portrait DisCO korrigiert die perspektivische Verzerrung von Nahaufnahmen von Gesichtern durch 3D-GAN-Inversion.
- Dance DisCo kombiniert Referenzvordergrund, Hintergrund und Zielpose, um menschliche Bilder oder Videos zu generieren.

## Entwicklungslinie {#development-line}

- **2022-10-20 — DisCO-Projektseite und öffentliche Demo erschienen.** Disentangled Image Colorization via Global Anchors etablierte einen Colorisierungs-Workflow für SIGGRAPH Asia 2022 mit Code, Checkpoints und einer gehosteten Demo.
- **2023-02-26 — Portrait DisCO wurde über eine Projektseite vorgestellt.** Portrait Distortion Correction with Perspective-Aware 3D GANs erschien als eigenständiges Projekt zur Korrektur der Verzerrung von Porträts aus geringer Distanz. Das Repository verzeichnet die Annahme bei IJCV am 2024-01-03 und die Veröffentlichung des Inversions-Codes am 2025-02-04, während das vollständige System und die Hugging-Face-Demo noch als TODO geführt werden.
- **2023-07-11 — DisCo-Tanzprojekt wurde mit Code und Live-Demo veröffentlicht.** Disentangled Control for Referring Human Dance Generation in Real World erschien als eigenständiges, posegesteuertes Projekt zur Tanzbildgenerierung. Das Repository verzeichnet ein Update des temporalen Moduls am 2023-11-30, die Annahme bei CVPR 2024 am 2024-04-08 und IDOL als Erweiterung von DisCo am 2024-07-15.

## Was sich geändert hat {#what-changed}

- 2022-10-20 — DISCO: Disentangled Image Colorization via Global Anchors etablierte einen Colorisierungs-Workflow für SIGGRAPH Asia 2022 mit Code, Checkpoints und einer gehosteten Demo.
- 2023-02-26 — DisCO: Portrait Distortion Correction with Perspective-Aware 3D GANs erschien als eigenständiges Projekt zur Korrektur der Verzerrung von Porträts aus geringer Distanz. Das Repository verzeichnet die Annahme bei IJCV am 2024-01-03 und die Veröffentlichung des Inversions-Codes am 2025-02-04, während das vollständige System und die Hugging-Face-Demo noch als TODO geführt werden.
- 2023-07-11 — DisCo: Disentangled Control for Referring Human Dance Generation in Real World erschien als eigenständiges, posegesteuertes Projekt zur Tanzbildgenerierung. Das Repository verzeichnet ein Update des temporalen Moduls am 2023-11-30, die Annahme bei CVPR 2024 am 2024-04-08 und IDOL als Erweiterung von DisCo am 2024-07-15.

Diese Daten bilden keine gemeinsame Entwicklungslinie. Die drei Projekte haben unterschiedliche Autoren, Aufgaben, Modelle, Repositories und Veröffentlichungswege.

## Verwendung {#how-to-use-this}

Stand 2023-07-11: Prüfen Sie aufgabenspezifische öffentliche Projektseiten und validieren Sie Fähigkeiten über den verlinkten Code oder eine Live-Demo, anstatt den Namen als ein unverändertes Werkzeug zu behandeln.

1. Für die Graustufen-Colorisierung klonen Sie das Repository, erstellen die dokumentierte Python-3.8-/PyTorch-/CUDA-Umgebung, laden einen Checkpoint in `checkpoints` herunter, legen Bilder in `data` ab und führen anschließend das mitgelieferte Inferenzskript aus.
  — <https://github.com/MenghanXia/DisentangledColorization>
2. Für die Korrektur perspektivischer Verzerrung bei Porträts initialisieren Sie EG3D und Deep3DFaceRecon, laden den FFHQ-Checkpoint herunter, erstellen die mitgelieferte Conda-Umgebung, setzen Ein- und Modellpfade in `example_configs/config.py`, führen die Vorverarbeitung aus und starten danach das Korrekturskript.
  — <https://github.com/lightChaserX/DisCO>
3. Für die Bildbearbeitung bei Tanzszenen laden Sie den Feinabstimmungs-Checkpoint und die Abhängigkeit SD Image Variations herunter, setzen deren Pfade im mitgelieferten Jupyter-Notebook und starten es auf einer lokalen GPU.
  — <https://github.com/Wangt-CN/DisCo>

## Best Practices {#best-practices}

- Für die DISCO-Colorisierung behalten Sie die Standardinferenz mit 256×256 bei, sofern Sie keine andere Einstellung validiert haben: Die Autoren kennzeichnen die Ausgabe mit `--no_resize` in Originalauflösung als instabil. Verwenden Sie absolute Pfade und fixieren Sie `--seed`, wenn Sie Ergebnisse vergleichen.
  — <https://github.com/MenghanXia/DisentangledColorization>
- Validieren Sie für Portrait DisCO die Abhängigkeitskette aus EG3D und Deep3DFaceRecon, bevor Sie Bilder verarbeiten, und betrachten Sie den veröffentlichten Inversions-Code als enger gefasst als ein vollständiges öffentliches Produkt, da das vollständige System und die gehostete Demo weiterhin als TODO aufgeführt sind.
  — <https://github.com/lightChaserX/DisCO>
- Für Dance DisCo nutzen Sie das dokumentierte lokale Notebook für einen ersten Bild-Workflow; für personenspezifische Feinabstimmung bereiten Sie Masken und Skelette mit Grounded-SAM und OpenPose vor und stimmen anschließend zuerst Lernrate und das Entfrieren der U-Net-Schichten ab.
  — <https://github.com/Wangt-CN/DisCo>

## Hiermit überholt {#superseded-by-this}

- 2022-10-20 — Die Nutzung des gehosteten DISCO-Colorisierungs-Space als Standard-Workflow ist veraltet, da dessen Seite derzeit einen Laufzeitfehler meldet. Verwenden Sie stattdessen den lokalen Repository-Pfad.
- 2023-02-26 — Die frühere Erwartung einer künftigen Code-Veröffentlichung von Portrait DisCO ist durch die Veröffentlichung des Inversions-Codes am 2025-02-04 überholt. Verwechseln Sie diese nicht mit einer Veröffentlichung des vollständigen Systems oder einer gehosteten Demo.
- 2023-07-11 — Die Behandlung des verlinkten Gradio-Endpunkts als verifizierten aktuellen Dance-DisCo-Workflow ist veraltet, da er am 2026-09-04 nicht abgerufen werden konnte. Verwenden Sie den lokalen Workflow des Repositories, bis ein gehosteter Endpunkt unabhängig bestätigt ist.
- 2023-07-11 — Die Behandlung aller Vorkommen von „DisCO“ als Versionen eines einzelnen Projekts ist veraltet. Die drei Einträge sind unabhängige Projekte, die einen Namen teilen.

## Weiterhin unbekannt {#still-unknown}

- Der Schlüssel `disco` fasst drei unabhängige Projekte zusammen. Keine Primärquelle belegt einen gemeinsamen Maintainer, eine gemeinsame Release-Linie, eine gemeinsame API, ein gemeinsames Modellgewicht oder eine Nachfolgebeziehung.
- Der aktuelle Gradio-Endpunkt von Dance DisCo konnte während der Recherche nicht abgerufen werden; dies beweist keine dauerhafte Einstellung.
- Wir haben keines der Repositories ausgeführt und keine Checkpoints heruntergeladen, daher ist die Kompatibilität mit aktuellen Versionen von CUDA, PyTorch und Abhängigkeiten nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://menghanxia.github.io/projects/disco.html | DISCO: Disentangled Image Colorization via Global Anchors | 2026-09-04 |
| https://huggingface.co/spaces/menghanxia/disco | Disco - a Hugging Face Space by menghanxia | 2026-09-04 |
| https://github.com/MenghanXia/DisentangledColorization | MenghanXia/DisentangledColorization | 2026-09-04 |
| https://portrait-disco.github.io/ | DisCO: Portrait Distortion Correction with Perspective-Aware 3D GANs | 2026-09-04 |
| https://github.com/lightChaserX/DisCO | lightChaserX/DisCO | 2026-09-04 |
| https://disco-dance.github.io/ | DisCo: Disentangled Control for Referring Human Dance Generation in Real World | 2026-09-04 |
| https://github.com/Wangt-CN/DisCo | Wangt-CN/DisCo | 2026-09-04 |
| https://5e42cfd7d54823fd8a.gradio.live/ | DisCo Gradio demo endpoint | 2026-09-04 |
| https://7b2faca424cdb265fc.gradio.live/ | DisCo project-page Gradio demo endpoint | 2026-09-04 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:disco`, Thread `disco-development`, 3 datierte Ereignisse 2022-10-20 → 2023-07-11.
- **Praxishinweis:** Stand 2023-07-11 sollten Praktiker der DisCO-Linie nach aufgabenspezifischen öffentlichen Projektseiten suchen und eine behauptete Fähigkeit über den verlinkten Code oder die Live-Demo validieren, anstatt den Namen allein als ein unverändertes Werkzeug zu behandeln.
- **Konfidenz:** mittel. Die datierten Einträge unter „Hiermit überholt“ sind maßgeblich dafür, was veraltet ist.
