---
title: "CoCo"
category: projects
date: 2026-03-15
tags: [coco, coco-development, project]
aliases: ["CoCo"]
level: 2
source_sha256: e0be841f620b3fffa7a82c0e9225701a872c9ab6b2565e74309673e749dd205c
translation: machine
translated_at: '2026-10-24'
---
# CoCo {#coco}

**Entwicklungslinie:** `project:coco` · Thread `coco-development`  
**Letztes Ereignis:** 2026-03-15 · 1 datiertes seit 2026-03-15 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

CoCo ist ein Forschungsworkflow, der Textprompts in ausführbaren Python- und Matplotlib-Szenencode umwandelt. Er rendert einen Entwurf in einer Sandbox, prüft das Layout gegen den Prompt und verfeinert den Entwurf zu einem finalen Bild. Er zielt auf strukturierte Layouts, räumliche Beziehungen und dichten Text. Über drei Benchmarks hinweg berichtet er von einem Trainingsdatensatz mit 10K Entwurf-Final-Paaren und Verbesserungen von 68,83 %, 54,8 % und 41,23 % gegenüber direkter Generierung. Es dient als Forschungsreferenz, nicht als fertiges Inferenzpaket.

## Entwicklungslinie {#development-line}

- **2026-03-15 — Öffentliche Projektressourcen zu CoCo verlinkt.** Am 2026-03-15 wurde CoCo über verlinkte GitHub- und Hugging-Face-Projektressourcen referenziert. Damit entsteht ein datierter öffentlicher Bezugspunkt für den Code und die modellbezogenen Materialien des Projekts.

## Was sich geändert hat {#what-changed}

- 2026-03-15 — CoCo erschien mit Code und einem Hugging-Face-Modelllink. Das Repository dokumentiert die Methode von Code über Entwurf zu Verfeinerung, enthält aber kein dokumentiertes Inferenzkommando für Endanwender.
- 2026-08-06 — arXiv v2 wurde zur aktuellen Version des Papers und vermerkt die Annahme bei ECCV 2026.

## Anwendung {#how-to-use-this}

Ab dem 2026-03-15 mit dem verlinkten GitHub-Repository und der Hugging-Face-Seite beginnen, um öffentliche Assets zu finden. Die Quelldateien vor der Verwendung direkt prüfen.

1. Bei der Methodenbeschreibung im Repository beginnen: aus einem Prompt ausführbaren Matplotlib-Szenenlayout-Code erzeugen, den Entwurf rendern und ihn dann als Zwischenplan für die Bildverfeinerung nutzen.
  — <https://github.com/micky-li-hd/CoCo>
2. Die mitgelieferte Sandbox als Forschungscode behandeln: Sie führt übergebenen Python-Code mit einem `exec`-Aufruf aus, daher nur in einer isolierten Umgebung ausführen und keinen nicht vertrauenswürdigen Code einspeisen.
  — <https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py>
3. Das Paper für das Design von Training und Evaluation verwenden; die öffentliche Hugging-Face-Seite hat keine Modellkarte, keine erfassten Downloads und keinen gehosteten Inferenzanbieter.
  — <https://arxiv.org/abs/2603.08652>

## Bewährte Praktiken {#best-practices}

- Einen ausführbaren Entwurf dort nutzen, wo reine Prompt-Planung räumliche oder strukturelle Präzision verliert; den Entwurf vor der finalen Bilderzeugung verifizieren.
  — <https://arxiv.org/abs/2603.08652>
- Codeausführung isolieren und zeitlich begrenzen: Die mitgelieferte Sandbox führt eine Prüfung auf gefährlichen Code durch und wendet ein Timeout an, führt generiertes Python aber trotzdem aus.
  — <https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-08-06 — arXiv v1 (2026-03-09) ist nicht mehr die aktuelle Paper-Version; bei Zitaten des Papers Version v2 verwenden.

## Weiterhin unbekannt {#still-unknown}

- Die Hugging-Face-Seite hat keine Modellkarte und keine erfassten Download-Daten, und das Repository enthält nur eine README, Abbildungen und Sandbox-Code. Ein reproduzierbares öffentliches Inferenz-Setup, der Inhalt der Checkpoints, Hardwareanforderungen und die Lizenz sind in den geprüften Quellen nicht dokumentiert.
- Das Repository kündigt die Veröffentlichung des Papers für den 2026-03-09 an, während das datierte Ereignis der 2026-03-15 ist. Die geprüften Primärquellen belegen nicht, was genau am 2026-03-15 geändert wurde.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/micky-li-hd/CoCo | CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation — official repository | 2026-09-05 |
| https://huggingface.co/mickyhimself/CoCo | mickyhimself/CoCo — Hugging Face model page | 2026-09-05 |
| https://arxiv.org/abs/2603.08652 | CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation | 2026-09-05 |
| https://github.com/micky-li-hd/CoCo/blob/main/sandbox.py | CoCo sandbox.py | 2026-09-05 |

## Kurzbrief für Agenten {#agent-brief}

- **Gegenstand:** `project:coco`, Thread `coco-development`, 1 datiertes Ereignis 2026-03-15 → 2026-03-15.
- **Praktischer Hinweis:** Ab dem 2026-03-15 sollten Praktiker das verlinkte GitHub-Repository und die Hugging-Face-Seite als Ausgangspunkte nutzen, um die öffentlichen Ressourcen von CoCo zu finden; deren Inhalt und Anwendbarkeit erfordern weiterhin eine Prüfung auf Quellenebene.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
