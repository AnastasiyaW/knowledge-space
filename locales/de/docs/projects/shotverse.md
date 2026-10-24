---
title: "ShotVerse"
category: projects
date: 2026-03-14
tags: [project, shotverse, shotverse-development]
aliases: ["ShotVerse"]
level: 2
source_sha256: 59a59037327e56418feeb432e0c84d81cc6c8db3eb43155fc5482b4146e11c33
translation: machine
translated_at: '2026-10-24'
---
# ShotVerse {#shotverse}

**Entwicklungslinie:** `project:shotverse` · Thread `shotverse-development`  
**Letztes Ereignis:** 2026-03-14 · 1 datiertes seit 2026-03-14 · **Recherchiert:** 2026-09-06 · Konfidenz: hoch

## Was es ist {#what-it-is}

ShotVerse ist ein Forschungssystem für Kreative und Forschende, die explizite, konsistente Kamerabewegungen über mehrere Einstellungen hinweg benötigen.

- Der Planner wandelt eine globale Beschreibung und Beschreibungen einzelner Einstellungen in Kamerabahnen um.
- Der Controller rendert Multi-Shot-Videos aus Text und Trajektorien.

ShotVerse-Bench meldet 20 500 Clips und 12 Millionen Frames; die Experimente setzen Szenen aus 2–4 Einstellungen mit jeweils 249 Frames zusammen. Stand 2026-09-06 handelt es sich um eine Methodenspezifikation und einen Benchmark, nicht um ein installierbares Werkzeug: Das offizielle Repository kennzeichnet Gewichte, Inferenzcode, Datensatz und Training weiterhin als zukünftige Veröffentlichungen.

## Entwicklungslinie {#development-line}

- **2026-03-14 — Öffentliche Projektreferenzen zu ShotVerse wurden geteilt.** Am 2026-03-14 wurde auf ShotVerse mit Links zur Projektwebsite, zum GitHub-Repository und zu einem Hugging-Face-Ziel verwiesen. Zusammen markieren diese Links einen datierten öffentlichen Bezugspunkt für das Projekt und die zugehörigen Ressourcen.

## Was sich geändert hat {#what-changed}

2026-03-14 — ShotVerse wurde als Forschungsmethode für explizite Kamerasteuerung in Multi-Shot-Videos vorgestellt. Primärmaterialien mit direkten Datumsangaben bestätigen an diesem Tag kein lauffähiges öffentliches Release.

## So verwenden Sie das {#how-to-use-this}

Stand 2026-03-14 dienen die ShotVerse-Website und das GitHub-Repository als Ausgangspunkte für öffentliche Projektressourcen. Das verlinkte Hugging-Face-Ziel erfordert vor der Nutzung eine separate Überprüfung.

1. Lesen Sie das aktuelle Paper und ordnen Sie Ihre Aufgabe seiner Eingabe zu: eine globale Beschreibung plus Beschreibungen je Einstellung, nicht ein einzelner Text-Prompt.
  — <https://arxiv.org/abs/2603.11421>
2. Prüfen Sie die Projektseite und die Beispiele unter Prompt Details, um Kamerabewegungen und Schnittstruktur zu beurteilen.
  — <https://shotverse.github.io/>
3. Prüfen Sie das Repository, bevor Sie einen Einsatz planen: Offizielle Installations- und Inferenz-Pipelines existieren noch nicht, daher sind die Paper-Einstellungen kein lauffähiges Rezept.
  — <https://github.com/Songlin1998/ShotVerse>

## Bewährte Vorgehensweisen {#best-practices}

- Behalten Sie die zweistufige Eingabe für die Reproduktion der Forschung bei: einen globalen Szenenkontext und eine eigene Beschreibung für jede Einstellung, da der Planner diese Struktur erwartet.
  — <https://arxiv.org/html/2603.11421v1>
- Behandeln Sie die Metriken, den Stack aus Qwen3-VL-2B/HoloCine und das Training auf 96 H20 als experimentelles Setup, nicht als verifizierten Anwender-Workflow.
  — <https://arxiv.org/html/2603.11421v1>
- Integrieren Sie ShotVerse nicht in eine Produktionspipeline, bevor offizielle Artefakte verfügbar sind: Ein öffentliches Repository bedeutet nicht, dass ein Modell verfügbar ist.
  — <https://github.com/Songlin1998/ShotVerse>

## Abgelöst durch {#superseded-by-this}

- 2026-08-24 — arXiv v2 ersetzt v1 vom 2026-03-12 als aktuelle Paper-Version. Dies verschiebt den Status vom 2026-03-14 nicht rückwirkend und belegt nicht, dass Code oder Gewichte veröffentlicht wurden.

## Weiterhin unbekannt {#still-unknown}

- Wir haben keinen primären archivarischen Nachweis gefunden, dass die aktuelle Website oder das Repository am 2026-03-14 existierte.
- Wir haben keinen unabhängigen reproduzierbaren Lauf, keine Modelllizenz, keine Checkpoints, keinen öffentlichen Datensatz und keine verifizierten Anwenderpraktiken gefunden.
- Chinesischsprachige Suchanfragen lieferten Aggregator-Zusammenfassungen statt primärer Dokumentation oder praktischer Berichte.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2603.11421v1 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation (arXiv v1) | 2026-09-06 |
| https://arxiv.org/html/2603.11421v1 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation (arXiv v1 full text) | 2026-09-06 |
| https://arxiv.org/abs/2603.11421 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation (current arXiv record) | 2026-09-06 |
| https://shotverse.github.io/ | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation | 2026-09-06 |
| https://github.com/Songlin1998/ShotVerse | GitHub - Songlin1998/ShotVerse | 2026-09-06 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:shotverse`, Thread `shotverse-development`, 1 datiertes Ereignis 2026-03-14 → 2026-03-14.
- **Praktischer Hinweis:** Stand 2026-03-14 die ShotVerse-Website und das verlinkte GitHub-Repository als Ausgangspunkte für öffentliche Projektressourcen behandeln. Das verlinkte Hugging-Face-Ziel erfordert vor der Nutzung eine separate Überprüfung.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich für das, was veraltet ist.
