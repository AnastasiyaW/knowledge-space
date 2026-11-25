---
title: "HY-WU — Tencent Hunyuan"
category: projects
date: 2026-03-06
tags: [hy-wu, project, tencent-hunyuan]
aliases: ["HY-WU"]
level: 3
source_sha256: 53799f20cc1190f7fefc0711385bd252aaeb9f82f07c5d4510155e9cf183d021
translation: machine
translated_at: '2026-10-24'
---
# HY-WU — Tencent Hunyuan {#hy-wu-tencent-hunyuan}

**Entwicklungslinie:** `project:hy-wu` · Thread `tencent-hunyuan`  
**Letztes Ereignis:** 2026-03-06 · 1 datiertes Ereignis seit 2026-03-06 · **Recherchiert:** 2026-09-06 · Konfidenz: hoch

## Was es ist {#what-it-is}

HY-WU — ein lokaler Forschungs-Stack für Teams mit Multi-GPU-Hardware, die Bild-zu-Bild-Bearbeitungen ohne das Training eines bearbeitungsspezifischen LoRA benötigen.

- LoRA-Generator: erzeugt instanzkonditionierte LoRA-Updates und injiziert sie in ein eingefrorenes Backbone.
- Gepaartes Modell: betreibt `tencent/HY-WU` zusammen mit `tencent/HunyuanImage-3.0-Instruct`.
- Bearbeitungsaufgaben: demonstriert Kleidungsfusion, Outfit-Transfer, Gesichtsidentitäts-Transfer, virtuelles Anprobieren und Textursynthese.

## Entwicklungslinie {#development-line}

- **2026-03-06 — Offizielle Projektressourcen von HY-WU wurden verfügbar.** Am 2026-03-06 gingen offizielle HY-WU-Ressourcen über eine Projektseite, ein GitHub-Repository und eine Hugging-Face-Seite online. Zu Release-Version, Ankündigung und vollem Funktionsumfang liegen uns keine bestätigten Details vor.

## Was sich geändert hat {#what-changed}

2026-03-06 — HY-WU hat Inferenzcode und Modellgewichte für die Inferenz mit HunyuanImage-3.0-Instruct veröffentlicht. 2026-03-07 — Der technische Bericht zu HY-WU erschien auf arXiv als v1, als Forschungsarbeit und nicht als eigenständiger Checkpoint. 2026-03-18 — GitHub verzeichnet den Commit `a9f4206` mit dem Titel „add configurable image size“; die aktuelle Inferenz akzeptiert `image_size`. 2026-06-18 — arXiv v2 überarbeitete den technischen Bericht; wir haben kein neueres Code- oder Gewichts-Release gefunden.

## Anwendung {#how-to-use-this}

Wir können HY-WU ab 2026-03-06 über die Projektseite, das Quell-Repository und die Hugging-Face-Seite evaluieren. Für Produktionsaufgaben liegen uns nicht genügend Belege vor, um einen Einsatz zu empfehlen.

1. Lesen Sie zuerst die Community-Lizenz und prüfen Sie, ob das vorgesehene Territorium und die nachgelagerte Nutzung abgedeckt sind.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/LICENSE>
2. Stellen Sie vor dem Setup die dokumentierte Multi-GPU-Kapazität bereit: mindestens 8×40 GB oder 4×80 GB VRAM.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
3. Klonen Sie `Tencent-Hunyuan/HY-WU`, wechseln Sie in das Verzeichnis und installieren Sie `requirements.txt`.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
4. Führen Sie `python infer.py` aus oder erstellen Sie `WUPipeline` mit `tencent/HunyuanImage-3.0-Instruct` als Basismodell und `tencent/HY-WU` als Parametergenerator.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py>
5. Stellen Sie ein Basisbild, ein oder mehrere Referenzbilder und eine Anweisung bereit, die sowohl den gewünschten Transfer als auch alles, was unverändert bleiben muss, benennt; speichern Sie das generierte Bild.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py>
6. Für die optionale lokale Oberfläche installieren Sie Gradio und führen Sie `python gradio/app.py` aus.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>

## Best Practices {#best-practices}

- Beginnen Sie mit dem vorgelagerten, abgestimmten Modellpaar, statt ein nicht gelistetes Backbone zu verwenden; destillierte Checkpoints und Checkpoints anderer Backbones sind im Projektplan weiterhin ungeprüft.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
- Reproduzieren Sie das mitgelieferte Zwei-Bild-Rezept mit seiner expliziten Erhaltungsanweisung, 50 Diffusionsschritten und festem Seed, bevor Sie die Generierungseinstellungen ändern.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py>
- Behandeln Sie die GPU-Kapazität als Preflight-Prüfung: Die vorgelagerte Dokumentation verlangt ausdrücklich Multi-GPU-Inferenz für das Basismodell.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
- Hart codieren Sie nicht den in der README angegebenen Gradio-Port: Die aktuelle App bindet Port 7860, während die README 7680 nennt; prüfen Sie den laufenden Endpunkt.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/gradio/app.py>
- Verwenden Sie die Arbeit und ihre Ausgaben nicht zur Verbesserung eines Nicht-Hunyuan-Modells und betreiben Sie sie nicht in Territorien, die durch die genannte Lizenz ausgeschlossen sind.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/LICENSE>

## Durch Neuerungen überholt {#superseded-by-this}

- 2026-03-07 — arXiv v1 wurde durch arXiv v2 überholt, überarbeitet am 2026-06-18; dies belegt kein neueres Modell- oder Gewichts-Release.

## Weiterhin unbekannt {#still-unknown}

- Die offizielle Hugging-Face-Modellkarte nennt derzeit „March 6, 2025“, was dem Lizenzdatum vom 6. März 2026 und der Repository-Historie widerspricht; es scheint sich um einen Dokumentationsfehler und nicht um einen separaten Start im Jahr 2025 zu handeln.
- Es wurde kein unabhängig verifizierter erfolgreicher lokaler Lauf, keine Durchsatzmessung, kein Workaround für Consumer-GPUs und kein destillierter Checkpoint gefunden.
- Ein späteres Modellgewichts-Release des Herstellers ist nicht belegt; arXiv v2 ist eine Überarbeitung des Berichts und kein Nachweis eines Implementierungsupdates.
- Es wurde keine zugängliche, datierte chinesischsprachige Unternehmensankündigung von Tencent zum Projekt-Release gefunden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://tencent-hy-wu.github.io/ | HY-WU (Teil I): Ein erweiterbares funktionales neuronales Speichergerüst und eine Instanziierung für textgesteuerte Bildbearbeitung | 2026-09-06 |
| https://github.com/Tencent-Hunyuan/HY-WU | Tencent-Hunyuan/HY-WU | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md | HY-WU README | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/LICENSE | Tencent Hunyuan Community License Agreement für HY-WU | 2026-09-06 |
| https://huggingface.co/tencent/HY-WU | tencent/HY-WU Modellkarte | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py | HY-WU Inferenzbeispiel | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/gradio/app.py | HY-WU Gradio-Anwendung | 2026-09-06 |
| https://github.com/Tencent-Hunyuan/HY-WU/commits/main | HY-WU Commit-Historie | 2026-09-06 |
| https://arxiv.org/abs/2603.07236v2 | HY-WU (Teil I) arXiv v2 | 2026-09-06 |
| https://github.com/Tencent-Hunyuan/HY-WU/releases | HY-WU GitHub-Releases | 2026-09-06 |

## Kurzbrief für Agenten {#agent-brief}

- **Gegenstand:** `project:hy-wu`, Thread `tencent-hunyuan`, 1 datiertes Ereignis 2026-03-06 → 2026-03-06.
- **Praktischer Hinweis:** Wir können HY-WU ab 2026-03-06 über die offizielle Projektseite, das Quell-Repository und die Hugging-Face-Seite evaluieren; die vorliegenden Belege rechtfertigen keine fähigkeitsspezifischen Empfehlungen zur Einführung.
- **Konfidenz:** hoch. Die datierten Überholungsvermerke oben sind maßgeblich dafür, was veraltet ist.
