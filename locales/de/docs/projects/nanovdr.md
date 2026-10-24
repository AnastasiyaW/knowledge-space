---
title: "NanoVDR"
category: projects
date: 2026-03-17
tags: [nanovdr, nanovdr-public-release, project]
aliases: ["NanoVDR"]
level: 2
source_sha256: e70f2d040d188f53e961f507741934d70a8d5fcccaf24ac406596d36573e2174
translation: machine
translated_at: '2026-10-24'
---
# NanoVDR {#nanovdr}

**Entwicklungslinie:** `project:nanovdr` · Thread `nanovdr-public-release`  
**Letztes Ereignis:** 2026-03-17 · seit 2026-03-17 1 datiertes Ereignis · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

NanoVDR ist ein System zum Abruf visueller Dokumente für Teams, die in PDF-Seiten, Berichten und Seitenbildern suchen. Es fungiert als Ersatz auf der Abfrageseite und nicht als eigenständiger Dokumentindexer.

- Dokumentindexer: indexiert Seiten offline mit Qwen3-VL-Embedding-2B.
- Abfrage-Encoder: bettet Textabfragen mit Studentenmodellen mit 69–151 Mio. Parametern ein.
- Scorer: ordnet kompatible Vektoren per Skalarprodukt.

Das mehrsprachige Abfragemodell mit 69 Mio. Parametern läuft mit 51 ms pro CPU-Abfrage und benötigt Dokumente, die mit dem Lehrermodell indexiert wurden.

## Entwicklungslinie {#development-line}

- **2026-03-17 — NanoVDR verlinkte öffentliche Hugging-Face-Ressourcen und eine Demo.** Am 2026-03-17 veröffentlichte die Linie einen Blogartikel auf Hugging Face, eine Projektseite und einen Demo-Space. Damit wurden auffindbare Projekt- und Demonstrationsressourcen für die öffentliche Veröffentlichung bereitgestellt, deren Inhalte wir für diese Übersicht jedoch nicht geprüft haben.

## Was sich geändert hat {#what-changed}

- **2026-03-17** — NanoVDR wurde als textbasierter Abfrage-Encoder mit 69 Mio. Parametern vorgestellt, der aus Qwen3-VL-Embedding-2B für den Abruf visueller Dokumente destilliert wurde. Der Artikel des Herausgebers ist auf 2026-03-16 datiert und berichtet eine Teacher-Retention von 95,1 % für NanoVDR-S-Multi.
- **2026-08-11** — Die Checkpoint-Namen wurden um Encode-Tower, Lehrermodell und Embedding-Breite erweitert. Alte Links werden weitergeleitet.
- **2026-08-29** — Das Team veröffentlichte arXiv v3. Das Projekt-Repository unterscheidet die spätere Arbeit an DistilVDR-Dokument-Tower von der ursprünglichen NanoVDR-Abfrage-Tower-Linie.

## Verwendung {#how-to-use-this}

Prüfen Sie vor der Evaluierung die verlinkten Hugging-Face-Ressourcen und die öffentliche Demo, wie sie am 2026-03-17 vorlagen; konkrete Fähigkeiten, Anforderungen und Ergebnisse sind nicht verifiziert.

1. Laden Sie einen kompatiblen Abfrage-Checkpoint mit SentenceTransformers und kodieren Sie die Textabfrage.
  — <https://github.com/Ryenhails/NanoVDR>
2. Für die ursprüngliche NanoVDR-Linie indexieren Sie Seiten offline mit Qwen3-VL-Embedding-2B und ordnen anschließend dessen Seitenvektoren per Skalarprodukt dem Abfragevektor zu.
  — <https://huggingface.co/nanovdr>
3. Nutzen Sie die gehostete Demo nur für explorative Abfragen; sie kann im Ruhezustand sein, bis sie neu gestartet wird.
  — <https://huggingface.co/spaces/nanovdr/NanoVDR-Demo>

## Bewährte Methoden {#best-practices}

- Gleichen Sie Abfrage- und Dokument-Tower sowohl nach Lehrermodell als auch nach Embedding-Breite ab; Vektoren aus verschiedenen Lehrermodell-Räumen sind nicht austauschbar.
  — <https://github.com/Ryenhails/NanoVDR>
- Bevorzugen Sie den mehrsprachigen `-ML`-Abfrage-Checkpoint, sofern nicht ausdrücklich ein rein englisches Modell erforderlich ist.
  — <https://github.com/Ryenhails/NanoVDR>
- Verwenden Sie die ursprüngliche Linie für die CPU-Abfragebereitstellung mit vom Lehrermodell erstellten Indizes; das DistilVDR-Paar nur dann, wenn eine Indexierung ohne Lehrermodell erforderlich ist.
  — <https://github.com/Ryenhails/NanoVDR>

## Abgelöst durch {#superseded-by-this}

- **2026-08-11** — Checkpoint-Namen, die Tower, Lehrermodell und Vektorbreite angeben, ersetzen frühere Namen; ältere Modelllinks werden weitergeleitet.

## Noch unbekannt {#still-unknown}

- Die Felder event_findings und new_events fehlen im Antwortschema, daher bleiben die datierten Ergänzungen unter what_changed.
- Ein Artikel des Herausgebers vom 2026-03-16 bestätigt das Ereignis vom 2026-03-17.
- Die Umbenennung vom 2026-08-11 und arXiv v3 vom 2026-08-29 gehören zu späteren Aktualisierungen, nicht zum Ereignis vom 2026-03-17.
- Die öffentliche Demo war bei der Prüfung im Ruhezustand, daher ist ein interaktiver Durchlauf nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/blog/Ryenhails/nanovdr | NanoVDR: A 70M Text-Only Model That Retrieves Visual Documents as Well as a 2B VLM | 2026-09-05 |
| https://huggingface.co/nanovdr | nanovdr (NanoVDR) organization page | 2026-09-05 |
| https://huggingface.co/spaces/nanovdr/NanoVDR-Demo | NanoVDR Demo | 2026-09-05 |
| https://github.com/Ryenhails/NanoVDR | Ryenhails/NanoVDR | 2026-09-05 |
| https://arxiv.org/abs/2603.12824 | NanoVDR: Distilling a 2B Vision-Language Retriever into a 70M Text-Only Encoder for Visual Document Retrieval | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:nanovdr`, Thread `nanovdr-public-release`, 1 datiertes Ereignis vom 2026-03-17 → 2026-03-17.
- **Praktischer Hinweis:** Stand 2026-03-17 sollten Praktiker vor einer Evaluierung von NanoVDR die verlinkten Hugging-Face-Projektressourcen und die öffentliche Demo konsultieren; konkrete Fähigkeiten, Anforderungen und Ergebnisse sind nicht verifiziert.
- **Konfidenz:** hoch. Die datierten Überschreibungen sind maßgeblich dafür, was veraltet ist.
