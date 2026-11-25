---
title: "UMO"
category: projects
date: 2026-03-19
tags: [project, umo]
aliases: ["UMO"]
level: 2
source_sha256: 18ed5bffa0287f6c6b69508c3c897bdf5ce9c44e6f09f2c28d8ceef2724ae0b7
translation: machine
translated_at: '2026-10-24'
---
# UMO {#umo}

**Entwicklungslinie:** `project:umo` · Thread `umo`  
**Letztes Ereignis:** 2026-03-19 · 1 datiertes Ereignis seit 2026-03-19 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

UMO ist ein Forschungsframework für Teams, die 3D-Pipelines für menschliche Bewegung entwickeln. Es feintunt HY-Motion-Lite, statt ein herunterladbares Bewegungswerkzeug auszuliefern.

- Bewegungsgenerierung: erzeugt textkonditionierte menschliche Bewegung.
- Bewegungssteuerung: vervollständigt, bearbeitet und steuert Quellbewegungen über die Operationen Preserve, Generate und Edit.
- Aufgabenkodierung: kodiert Trajektorien, Hindernisse und Reaktionen zwischen zwei Personen als textkonditionierte Aufgaben.

## Entwicklungslinie {#development-line}

- **2026-03-19 — Die öffentliche Projektseite und das Quell-Repository von UMO wurden verlinkt.** Die Autoren stellten UMO als einheitliche Forschungsmethode für 3D-Bewegung des Menschen vor, mit qualitativen Demonstrationen und einem verlinkten Repository. Dieses Repository ist derzeit keine lauffähige Implementierung.

## Was sich geändert hat {#what-changed}

2026-03-19: Die Autoren stellten UMO als einheitliche Forschungsmethode für 3D-Bewegung des Menschen vor, mit qualitativen Demonstrationen und einem verlinkten Repository. Dieses Repository ist derzeit keine lauffähige Implementierung. 2026-08-17: Die vorläufige Liste akzeptierter Beiträge der ECCV ergänzte einen Posvermerk für UMO (#96, Poster Session 3). Dies änderte den Veröffentlichungsstatus, nicht aber die Verfügbarkeit von Code, Gewichten oder API.

## Verwendung {#how-to-use-this}

Stand 2026-03-19: Beginnen Sie für Dokumentation und Quellcode-Inspektion mit der verlinkten UMO-Projektseite und dem GitHub-Repository.

1. Prüfen Sie, ob das Ziel 3D-Skelettbewegung des Menschen ist und nicht Bild- oder Videogenerierung: Evaluierte Aufgaben umfassen Text-zu-Bewegung, Inpainting, Anweisungsbearbeitung, textserialisierte Geometrie und Reaktionen.
  — <https://arxiv.org/html/2603.15975v1>
2. Nutzen Sie das Paper und die Demonstrationen der Autoren, um ein Forschungsexperiment auf eine natürlichsprachliche Beschreibung oder Bearbeitung, eine strukturierte Trajektorie oder eine textuelle räumliche Randbedingung abzubilden.
  — <https://oliver-cong02.github.io/UMO.github.io/>
3. Prüfen Sie das offizielle Repository auf Code und Modellartefakte, bevor Sie die Implementierung einplanen. Derzeit ist kein offizieller Installations- oder Inferenzpfad veröffentlicht.
  — <https://github.com/Oliver-Cong02/UMO>

## Best Practices {#best-practices}

- Ersetzen Sie UMO bei Inpainting- oder Geometrieaufgaben nicht durch unverändertes HY-Motion: Laut Paper scheitert eine Zero-Shot- oder trainingsfreie Umwidmung deutlich.
  — <https://arxiv.org/html/2603.15975v1>
- Betrachten Sie das 4×B200-Training, 100k Schritte, den 50-Schritt-Euler-Solver und CFG 2.0 aus dem Paper als Studieneinstellungen, nicht als veröffentlichte Mindestspezifikation.
  — <https://arxiv.org/html/2603.15975v1>
- Überprüfen Sie Paper-Titel und das mit den Autoren verknüpfte Repository, bevor Sie auf Grundlage des Namens UMO handeln. ByteDance verwendet denselben Namen für ein separates Projekt zur Bildanpassung.
  — <https://github.com/bytedance/UMO>

## Hierdurch ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Kein offizielles Changelog und kein unveränderlicher Snapshot belegt die genaue Startaktion vom 2026-03-19. Dieses Datum gilt daher als öffentliches Fenster für Projekt und Repository, nicht als nachgewiesenes Datum einer Code- oder Modellveröffentlichung.
- Offizielle Quellen nennen weder einen UMO-Checkpoint, eine Lizenz, Installationsanleitungen, CLI/API, Vertrag für Eingabedateien noch eine Mindest-Hardwarespezifikation.
- Der allgemeine Name UMO wird auch von einem nicht verwandten Projekt zur Bildanpassung bei ByteDance verwendet. Die Autorennamen, der Paper-Titel und das Repository von Oliver-Cong02 identifizieren diese Arbeit als Projekt zur menschlichen Bewegung.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://arxiv.org/abs/2603.15975 | UMO: Unified In-Context Learning Unlocks Motion Foundation Model Priors — arXiv-v1-Eintrag | 2026-09-06 |
| https://arxiv.org/html/2603.15975v1 | UMO: Unified In-Context Learning Unlocks Motion Foundation Model Priors — vollständiges Paper als HTML | 2026-09-06 |
| https://oliver-cong02.github.io/UMO.github.io/ | UMO — Projektseite der Autoren und qualitative Demonstrationen | 2026-09-06 |
| https://github.com/Oliver-Cong02/UMO | Oliver-Cong02/UMO — offizielle Repository-Startseite | 2026-09-06 |
| https://eccv.ecva.net/Conferences/2026/AcceptedPapers | ECCV 2026 — vorläufige Liste akzeptierter Beiträge | 2026-09-06 |
| https://eccv.ecva.net/Conferences/2026 | ECCV 2026 — Konferenzankündigungen | 2026-09-06 |
| https://github.com/bytedance/UMO | bytedance/UMO — nicht verwandtes Projekt zur Bildanpassung mit gleichem Namen | 2026-09-06 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:umo`, Thread `umo`, 1 datiertes Ereignis 2026-03-19 → 2026-03-19.
- **Praktischer Hinweis:** Stand 2026-03-19 sollten Praktiker die verlinkte UMO-Projektseite und das GitHub-Repository als Ausgangspunkte für Dokumentation und Quellcode-Inspektion verwenden.
- **Konfidenz:** mittel. Datierte Ersetzungsvermerke oben sind maßgeblich dafür, was veraltet ist.
