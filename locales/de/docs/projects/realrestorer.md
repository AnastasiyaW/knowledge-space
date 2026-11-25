---
title: "RealRestorer"
category: projects
date: 2026-03-27
tags: [project, realrestorer]
aliases: ["RealRestorer"]
level: 2
source_sha256: dbcd624d983283fcdc41d329c6c3457ecec4627c6799b6d1b46df6095a83e60e
translation: machine
translated_at: '2026-10-24'
---
# RealRestorer {#realrestorer}

**Entwicklungslinie:** `project:realrestorer` · Thread `realrestorer`  
**Letztes Ereignis:** 2026-03-27 · 1 datiertes Ereignis seit 2026-03-27 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

RealRestorer ist ein Fine-Tuning von Step1X-Edit für die Bildrestaurierung und nicht für die allgemeine Bilderzeugung.

- Entfernt Unschärfe, Rauschen, Dunst, Regen, Moiré, Reflexionen, Blendeffekte und Kompressionsartefakte.
- Bewahrt die Szenenstruktur und den semantischen Inhalt durch eine Pipeline aus Bild und Anweisung.
- Stellt Code, Gewichte, Werkzeuge zur synthetischen Degradation und RealIR-Bench bereit.

## Entwicklungslinie {#development-line}

- **2026-03-27 — Projektressourcen von RealRestorer wurden verlinkt.** Am 2026-03-27 wurde die Entwicklungslinie von RealRestorer mit Links zu einer Projektseite, dem Quellcode-Repository, der Modellseite und der Quellenangabe erfasst. Dies ist für die Projektgeschichte relevant, weil es einen datierten öffentlichen Bezugspunkt für die zugehörigen Code- und Modellressourcen festlegt. Die angegebenen Links allein belegen jedoch weder den genauen Veröffentlichungsstatus noch die Fähigkeiten oder Versionen.

## Was sich geändert hat {#what-changed}

2026-03-26 — RealRestorer hat seine Modellgewichte, die Pipeline zur synthetischen Degradation und RealIR-Bench veröffentlicht; das Paper beschreibt neun Degradationskategorien und einen Benchmark mit 464 Bildern. 2026-03-27 — Das öffentliche Referenzset des Projekts verknüpfte Projektseite, Code, Modellkarte und Paper; der offizielle Veröffentlichungseintrag korrigiert das zugrunde liegende Startdatum auf 2026-03-26. 2026-03-29 — Eine Hugging-Face-Demo wurde verfügbar und ergänzt damit einen im Browser nutzbaren Testzugang.

## Anwendung {#how-to-use-this}

Ab 2026-03-27 sollten Praktiker RealRestorer als Projekt mit verlinkten Code- und Modellressourcen behandeln und vor dem Einsatz genaue Versionen, Fähigkeiten und Nutzungsbedingungen anhand der verlinkten Primärquellen prüfen.

1. Klonen Sie das offizielle Repository, installieren Sie den mitgelieferten gepatchten diffusers-Checkout mit Python 3.12 und installieren Sie anschließend die Anforderungen des Projekts und des Benchmarks.
  — <https://github.com/yfyang007/RealRestorer>
2. Laden Sie die Gewichte von RealRestorer/RealRestorer herunter und laden Sie sie mit RealRestorerPipeline in BF16; stellen Sie ein RGB-Eingabebild und eine Restaurierungsanweisung bereit.
  — <https://huggingface.co/RealRestorer/RealRestorer>
3. Führen Sie 28 Entrauschungsschritte, Guidance Scale 3.0, Seed 42 und Größenstufe 1024 aus; speichern Sie das zurückgegebene Bild.
  — <https://huggingface.co/RealRestorer/RealRestorer>

## Best Practices {#best-practices}

- Verwenden Sie den gepatchten lokalen diffusers-Checkout des Repositorys und gehen Sie nicht davon aus, dass eine Standardinstallation von Diffusers RealRestorerPipeline implementiert.
  — <https://github.com/yfyang007/RealRestorer>
- Beginnen Sie mit CUDA, BF16, 28 Schritten, Guidance 3.0, Seed 42 und einer Eingabe von etwa 1024×1024; planen Sie bei dieser Einstellung etwa 34 GB GPU-Spitzenspeicher ein.
  — <https://github.com/yfyang007/RealRestorer>
- Behandeln Sie das veröffentlichte Modell und die Benchmark-Assets als Material für nicht-kommerzielle akademische Forschung, auch wenn der Code für eine Veröffentlichung unter Apache-2.0 vorgesehen ist.
  — <https://huggingface.co/RealRestorer/RealRestorer>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2026-03-29 — Die Annahme, dass nur der Zugriff über die Kommandozeile möglich ist, ist veraltet: Das offizielle Repository verzeichnet die Veröffentlichung einer Hugging-Face-Demo.

## Weiterhin unbekannt {#still-unknown}

- Die verfügbaren Belege belegen nicht, dass der 2026-03-27 eine eigenständige technische Veröffentlichung darstellt und nicht lediglich die Veröffentlichung vom 2026-03-26 dokumentiert.
- Das im Paper genannte Ergebnis als bester Open-Source-Benchmark wurde in den geprüften Quellen nicht unabhängig reproduziert.
- event_findings:[{"event_date":"2026-03-27","finding":"Korrektur: Das offizielle Repository datiert die Veröffentlichungen der RealRestorer-Gewichte, der Degradations-Pipeline und von RealIR-Bench auf 2026-03-26, also einen Tag vor diesem datierten Eintrag.","source_url":"https://github.com/yfyang007/RealRestorer","source_date":"2026-03-26"},{"event_date":"2026-03-27","finding":"Das genaue veröffentlichte Modell ist RealRestorer/RealRestorer: ein 12B-BF16-Modell, feinabgestimmt aus stepfun-ai/Step1X-Edit; seine Modellkarte unterscheidet zwischen Code mit beabsichtigter Apache-2.0-Lizenz und Modell- sowie Benchmark-Assets für nicht-kommerzielle akademische Forschung.","source_url":"https://huggingface.co/RealRestorer/RealRestorer","source_date":"2026-03-26"}]
- new_events:[{"date":"2026-03-26","finding":"Das Paper, die Gewichte, die Pipeline zur synthetischen Degradation und der Start von RealIR-Bench wurden dokumentiert. Der Benchmark enthält 464 reale degradierte Bilder aus neun gängigen Degradationstypen.","source_url":"https://arxiv.org/abs/2603.25502","source_date":"2026-03-26"},{"date":"2026-03-29","finding":"Das offizielle Repository kündigte die Veröffentlichung einer Hugging-Face-Demo für RealRestorer an.","source_url":"https://github.com/yfyang007/RealRestorer","source_date":"2026-03-29"}]

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://yfyang007.github.io/RealRestorer/ | RealRestorer: Towards Generalizable Real-World Image Restoration | 2026-09-05 |
| https://github.com/yfyang007/RealRestorer | yfyang007/RealRestorer | 2026-09-05 |
| https://huggingface.co/RealRestorer/RealRestorer | RealRestorer/RealRestorer model card | 2026-09-05 |
| https://arxiv.org/abs/2603.25502 | RealRestorer: Towards Generalizable Real-World Image Restoration with Large-Scale Image Editing Models | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:realrestorer`, Thread `realrestorer`, 1 datiertes Ereignis vom 2026-03-27 bis 2026-03-27.
- **Praktischer Hinweis:** Ab 2026-03-27 sollten Praktiker RealRestorer als Projekt mit verlinkten Code- und Modellressourcen behandeln und vor dem Einsatz genaue Versionen, Fähigkeiten und Nutzungsbedingungen anhand der verlinkten Primärquellen prüfen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.
