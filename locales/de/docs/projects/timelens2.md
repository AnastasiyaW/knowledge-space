---
title: "TimeLens2"
category: projects
date: 2026-07-22
tags: [project, timelens2, timelens2-development]
aliases: ["TimeLens2"]
level: 2
source_sha256: be9c7a1c507f56317676f2bc3862f3b1efcc8c19f2d3915c4924a5ec16d8ddb2
translation: machine
translated_at: '2026-10-24'
---
# TimeLens2 {#timelens2}

**Entwicklungslinie:** `project:timelens2` · Thread `timelens2-development`  
**Letztes Ereignis:** 2026-07-22 · 1 datiertes Ereignis seit 2026-07-22 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

TimeLens2 ist eine offene, auf Qwen3-VL basierende Modellfamilie für Forschende und Entwickler von Videosuchsystemen, die ein Video plus eine Textanfrage in ein oder mehrere Evidenzintervalle überführt. Sie unterstützt Grounding für kurze, lange, wiederholte Ereignisse, fragenbasierte Anfragen und egozentrische Perspektiven. Veröffentlicht wurden die Größen 2B, 4B und 8B. Das 8B-Modell erreicht laut Angaben einen mittleren mIoU von 48,0 über sieben Benchmarks. Lokale Inferenz erfordert einen kompatiblen Transformers- und Video-Stack; einen gehosteten Inferenzanbieter gibt es nicht.

## Entwicklungslinie {#development-line}

- **2026-07-22 — Öffentliche Projektressourcen von TimeLens2 wurden verlinkt.** Am 2026-07-22 verlinkte eine Nachricht der TimeLens2-Entwicklungslinie die öffentliche Projektseite, das GitHub-Quellcode-Repository, die Hugging-Face-Collection und einen Space für temporales Grounding. Diese öffentliche Veröffentlichung ermöglicht den materiellen Zugang zum Projekt, nennt aber keine Version, Modellkonfiguration oder Funktionsbehauptung.

## Was sich geändert hat {#what-changed}

2026-07-22 — TimeLens2 wurde als generalistische Veröffentlichung für temporales Grounding gestartet, mit Projektseite, Apache-2.0-Code, TimeLens2-93K-Daten, 2B/4B/8B-Checkpoints und einer 8B-Demo. Das verlinkte Paper, eingereicht am 2026-07-19, beschreibt die Aufgabe als mengenwertige Intervallvorhersage. Auf dem Qwen3-VL-Backbone berichtet es Verbesserungen von 14,2 mIoU für 2B, 13,0 für 4B und 18,1 für 8B. Am 2026-07-27 wurden passende 2B/4B/8B-SFT-Checkpoints für die Erzeugung von Rollouts und die Reproduktion von GRPO ergänzt.

## So wird es genutzt {#how-to-use-this}

Ab 2026-07-22 mit der Projektseite und dem Repository von TimeLens2 beginnen; für Assets und Demos die Hugging-Face-Collection und den Space verwenden.

1. Die Inferenz-Abhängigkeiten installieren, `MCG-NJU/TimeLens2-8B` mit Transformers laden und einen lokalen Video-URI angeben.
  — <https://huggingface.co/MCG-NJU/TimeLens2-8B>
2. Alle relevanten Spannen in Sekunden anfordern und ein JSON-Array von `[start, end]`-Paaren verlangen; die erzeugte Antwort als Evidenzmenge dekodieren.
  — <https://huggingface.co/MCG-NJU/TimeLens2-8B>
3. Für die Reproduktion die benötigten Videos herunterladen, SFT ausführen, optional Rollouts aus dem passenden `-SFT`-Checkpoint neu erzeugen, anschließend GRPO und Evaluation ausführen.
  — <https://github.com/MCG-NJU/TimeLens2>

## Best Practices {#best-practices}

- Alle passenden Spannen anfordern, nicht einen geratenen Zeitpunkt, und das Antwortformat auf Zeitstempelpaare beschränken.
  — <https://huggingface.co/MCG-NJU/TimeLens2-8B>
- Für jede Kombination aus Modell, Daten und Seed ein eigenes Ausgabeverzeichnis für Rollouts verwenden, damit parallele Shard-Jobs keine Ausgaben überschreiben.
  — <https://github.com/MCG-NJU/TimeLens2/blob/main/grpo/README.md>
- GRPO erst starten, wenn das Zusammenführen der Rollouts erfolgreich war und jede Trainingszeile die erwarteten acht Antworten enthält.
  — <https://github.com/MCG-NJU/TimeLens2/blob/main/grpo/README.md>

## Hiermit ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Das Ereignis vom 2026-07-22 verlinkt einen 8B-Space, die geprüfte Space-Seite enthält jedoch keine Betriebsgrenzen oder Deployment-Konfiguration. Die offizielle Modellkarte für 8B besagt, dass das Modell nicht von einem Inferenzanbieter bereitgestellt wird; die Verfügbarkeit dieser Demo ist daher kein Beleg für eine unterstützte gehostete API.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://mcg-nju.github.io/TimeLens2/ | TimeLens2 — Generalist Video Temporal Grounding with Multimodal LLMs | 2026-09-05 |
| https://github.com/MCG-NJU/TimeLens2 | MCG-NJU/TimeLens2 repository | 2026-09-05 |
| https://huggingface.co/collections/MCG-NJU/timelens2 | TimeLens2 collection | 2026-09-05 |
| https://huggingface.co/spaces/hugging-apps/timelens2-8b-temporal-grounding | TimeLens2-8B temporal-grounding Space | 2026-09-05 |
| https://arxiv.org/abs/2607.17423 | TimeLens2: Generalist Video Temporal Grounding with Multimodal LLMs | 2026-09-05 |
| https://huggingface.co/MCG-NJU/TimeLens2-8B | MCG-NJU/TimeLens2-8B model card | 2026-09-05 |
| https://github.com/MCG-NJU/TimeLens2/blob/main/grpo/README.md | TimeLens2 Rollout and GRPO guide | 2026-09-05 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:timelens2`, Thread `timelens2-development`, 1 datiertes Ereignis, 2026-07-22 → 2026-07-22.
- **Praktischer Hinweis:** Ab 2026-07-22 sollten Praktiker die Projektseite und das Repository als Ausgangspunkt für TimeLens2 nutzen, wobei die verlinkte Hugging-Face-Collection und der Space als öffentliche Einstiegspunkte für Assets und Demos dienen; die genauen Fähigkeiten bleiben unverifiziert.
- **Konfidenz:** hoch. Datierte Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
