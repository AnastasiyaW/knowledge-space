---
title: "EVIE-Preview-4.5B"
category: projects
date: 2026-08-18
tags: [evie-preview-4-5b, project, tencent/evie-preview-4.5b]
aliases: ["EVIE-Preview-4.5B"]
level: 2
source_sha256: ce9f47e87fd123f85a3ff14b8bd82ece33428129b5b58994dd8d7d93f14c9d7f
translation: machine
translated_at: '2026-10-24'
---
# EVIE-Preview-4.5B {#evie-preview-45b}

**Entwicklungslinie:** `project:evie-preview-4-5b` · Thread `evie-preview-4-5b`  
**Letztes Ereignis:** 2026-08-18 · 1 datiert seit 2026-08-18 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

EVIE-Preview-4.5B ist ein offenes 4,54B-Modell für mehrsprachige Suche in Scans, Tabellen, Diagrammen und Dokumenten. Funktionen: Textabfragen an Seitenbilder; MaxSim-Retrieval mit Late Interaction; Abfragen in Englisch, Französisch, Deutsch, Italienisch, Spanisch, Portugiesisch und Chinesisch. Einschränkung: Der BF16-Checkpoint belegt 8,5 GB, und ein Index mit 1 Mio. Seiten benötigt bei 768 visuellen Token 179,2 GiB. Fazit: Geeignet für selbst gehostetes visuelles Dokument-Retrieval, sofern das Team bereit ist, einen Multi-Vektor-Index vorzuhalten und CUDA-Inferenz zu betreiben.

## Entwicklungslinie {#development-line}

- **2026-08-18 — Datierte öffentliche Referenzen zu EVIE-Preview-4.5B.** Visual-Document-Retrieval-Checkpoint mit 4,54B Parametern auf Basis von Qwen3.5-4B, mit 128-dimensionalen Token-Vektoren und Apache-2.0-Lizenz.

## Was sich geändert hat {#what-changed}

2026-08-18 — EVIE-Preview-4.5B wurde veröffentlicht: Visual-Document-Retrieval-Checkpoint mit 4,54B Parametern auf Basis von Qwen3.5-4B, mit 128-dimensionalen Token-Vektoren und Apache-2.0-Lizenz.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-08-18 können Praktiker ihre Evaluierung auf Basis der verlinkten GitHub- und Hugging-Face-Seiten zu EVIE-Preview-4.5B beginnen. Fähigkeiten, Lizenzierung und Nutzungsanforderungen sollten vor dem Einsatz direkt in diesen Quellen überprüft werden.

1. Installieren Sie `colpali-engine>=0.3.15` und `accelerate`; für einen reproduzierbaren Start verwenden Sie die Abhängigkeiten aus dem Repository.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
2. Laden Sie `ColQwen3_5` mit der Kennung `tencent/EVIE-Preview-4.5B` in BF16 auf CUDA sowie den Processor `ColQwen3_5Processor`.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
3. Aktivieren Sie vor der Verarbeitung von Abfragen bidirektionale Aufmerksamkeit für die Full-Attention-Schichten, und setzen Sie vor jedem Query-Forward `model.rope_deltas = None`; berechnen Sie anschließend die MaxSim-Werte über `processor.score`.
  — <https://github.com/Tencent/EVIE-Preview-4.5B>
4. Für die Stapelprüfung von Seiten verwenden Sie `infer.py` mit wiederholbaren Argumenten `--query` und `--image`.
  — <https://github.com/Tencent/EVIE-Preview-4.5B>

## Bewährte Vorgehensweisen {#best-practices}

- Beginnen Sie mit 768 visuellen Token pro Seite: Das ist das Trainingsbudget des Modells und die wirtschaftlichere Indexvariante.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
- Verwenden Sie keine standardmäßigen Causal Masks: Der veröffentlichte Code schaltet die Full-Attention-Schichten ausdrücklich in den bidirektionalen Modus, andernfalls entsprechen die Ergebnisse nicht den angegebenen Werten.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
- Prüfen Sie die Qualität anhand eigener Dokumente und Abfragen: Die angegebenen Ergebnisse beziehen sich auf ViDoRe und nicht auf einen beliebigen Unternehmenskorpus.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>

## Hierdurch abgelöst {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Genaues Datum und Umfang späterer Änderungen im Hugging-Face-Repository sind durch keine Primärquelle mit Kalenderdatum belegt und deshalb nicht in new_events aufgenommen.
- Aussagen über die Spitzenposition auf ViDoRe stammen aus der Model Card; eine unabhängige Reproduktion wurde in diesem Eintrag nicht geprüft.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/Tencent/EVIE-Preview-4.5B | Tencent/EVIE-Preview-4.5B — Quellcode und Startanleitung | 2026-09-05 |
| https://huggingface.co/tencent/EVIE-Preview-4.5B | tencent/EVIE-Preview-4.5B — Model Card, Parameter, Ergebnisse und Quick Start | 2026-09-05 |

## Agent Brief {#agent-brief}

- **Gegenstand:** `project:evie-preview-4-5b`, Thread `evie-preview-4-5b`, 1 datiertes Ereignis 2026-08-18 → 2026-08-18.
- **Praxishinweis:** Stand 2026-08-18 können Praktiker ihre Evaluierung auf Basis der verlinkten GitHub- und Hugging-Face-Seiten zu EVIE-Preview-4.5B beginnen. Fähigkeiten, Lizenzierung und Nutzungsanforderungen sollten vor dem Einsatz direkt in diesen Quellen überprüft werden.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
