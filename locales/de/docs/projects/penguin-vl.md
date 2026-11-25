---
title: "Penguin-VL"
category: projects
date: 2026-03-09
tags: [penguin-vl, penguin-vl-public-release, project, tencent-ailab]
aliases: ["Penguin-VL"]
level: 2
source_sha256: 2601042161c6bf18ed0e71d3bd8c71ef9567da2b1d3dcae467f323bd3ab811c7
translation: machine
translated_at: '2026-10-24'
---
# Penguin-VL {#penguin-vl}

**Entwicklungslinie:** `project:penguin-vl` · Thread `penguin-vl-public-release`  
**Letztes Ereignis:** 2026-03-09 · 1 datiertes Ereignis seit 2026-03-09 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Penguin-VL ist eine VLM-Familie auf Basis von Qwen3 für Praktiker, die lokale multimodale Inferenz statt einer gehosteten Vision-API benötigen.

- Prompts mit Bildern, Dokumenten, Diagrammen, mehreren Bildern und Videos
- Bereitstellung über Transformers, Gradio und vLLM
- 2B- und 8B-Checkpoints sowie ein 0.4B-Vision-Encoder

## Entwicklungslinie {#development-line}

- **2026-03-09 — Öffentliche Projektressourcen zu Penguin-VL wurden veröffentlicht.** Am 2026-03-09 verlinkte Penguin-VL die Projektwebsite, das Quellcode-Repository, die Hugging-Face-Collection und den interaktiven Hugging-Face-Space. Dieser öffentliche Meilenstein ermöglicht es, das Projekt zu bewerten, seine veröffentlichten Assets zu finden und die Demo zu testen. Allein die datierten Links belegen jedoch weder die genaue Modellversion, die technischen Aussagen, die Lizenz noch den Umfang des Releases.

## Was sich geändert hat {#what-changed}

2026-03-09 — Tencent veröffentlichte Penguin-VL-2B, Penguin-VL-8B, Penguin-Encoder, Inferenzcode, ein vLLM-Plugin und eine Gradio-Demo. 2026-03-17 — Trainingscode wurde veröffentlicht. 2026-03-20 — Penguin-Recap-I, die begleitenden rekonstruierten Bild-Trainingsdaten, wurde veröffentlicht. 2026-03-26 — lmms-eval erhielt Unterstützung für die Penguin-VL-Benchmarks. 2026-03-30 — Penguin-Recap-V, Videodaten mit dichten Annotationen auf Zeit-, Absatz- und Videoebene, wurde veröffentlicht.

## Anwendung {#how-to-use-this}

Stand 2026-03-09 evaluieren Sie Penguin-VL über die Website, das Quellcode-Repository, die Hugging-Face-Collection und die Demo. Prüfen Sie Fähigkeiten, Versionen, Lizenzierung und Anforderungen an die Bereitstellung in diesen primären Ressourcen, bevor Sie sich darauf verlassen.

1. Erstellen Sie eine saubere Umgebung mit Python 3.11.13, PyTorch 2.5 oder neuer und CUDA 11.8 oder neuer. Installieren Sie die Anforderungen des Repositorys und führen Sie danach das mitgelieferte Transformers-Beispiel mit entweder `tencent/Penguin-VL-2B` oder `tencent/Penguin-VL-8B` aus.
  — <https://github.com/tencent-ailab/Penguin-VL>
2. Für die direkte Python-Integration laden Sie `tencent/Penguin-VL-8B` über `AutoModelForCausalLM` und `AutoProcessor` mit `trust_remote_code=True`. Übergeben Sie Bild-, Video- oder Texteingaben über den Processor.
  — <https://huggingface.co/tencent/Penguin-VL-8B>
3. Für eine interne visuelle Test-UI starten Sie `inference/launch_gradio_demo.py --model-path tencent/Penguin-VL-2B` oder den 8B-Checkpoint und verwenden anschließend die lokale Oberfläche.
  — <https://github.com/tencent-ailab/Penguin-VL>
4. Für einen OpenAI-kompatiblen Serving-Endpunkt installieren Sie den separat versionierten vLLM-Stack. Starten Sie das Projekt-Plugin mit `python -m penguinvl.plugin.vllm serve tencent/Penguin-VL-8B`.
  — <https://github.com/tencent-ailab/Penguin-VL>

## Bewährte Vorgehensweisen {#best-practices}

- Betreiben Sie Transformers-Inferenz und vLLM-Inferenz in getrennten Umgebungen: Der dokumentierte vLLM-0.11.0-Pfad setzt PyTorch 2.8 voraus, während der Standardpfad PyTorch 2.5 oder neuer empfiehlt.
  — <https://github.com/tencent-ailab/Penguin-VL>
- Installieren Sie bei Nutzung des vLLM-Pfads vLLM vor Flash Attention, um Abhängigkeitskonflikte zu vermeiden. Dies ist die vom Projekt dokumentierte Reihenfolge.
  — <https://github.com/tencent-ailab/Penguin-VL>
- Verwenden Sie das mitgelieferte Inferenz-Notebook und testen Sie repräsentative OCR-, Dokument-, Diagramm- und Video-Eingaben, bevor Sie Benchmark-Aussagen für das Produktiv-Routing übernehmen.
  — <https://github.com/tencent-ailab/Penguin-VL>

## Hiermit ersetzt {#superseded-by-this}

- 2026-03-17 — Die reine Inferenz-Veröffentlichung vom 2026-03-09 ist für Praktiker, die Training reproduzieren oder anpassen müssen, eine unvollständige Anleitung; Trainingscode ist jetzt verfügbar.
- 2026-03-20 — Die Aussage, dass Trainingsdaten für Penguin-VL nicht verfügbar seien, ist für die Bildseite überholt; Penguin-Recap-I ist verfügbar.
- 2026-03-30 — Die Anleitung zu reinen Bild-Trainingsdaten ist für Videoarbeit unvollständig; Penguin-Recap-V ergänzt Videoannotationen auf mehreren Granularitätsstufen.

## Noch unbekannt {#still-unknown}

- Der gehostete Hugging-Face-Space zeigte am 2026-09-05 bei der Abfrage einen Konfigurationsfehler; die lokale Gradio-Demo bleibt der dokumentierte Demo-Weg.
- In den konsultierten Primärquellen fanden wir keine unabhängigen Messungen zu Bereitstellung oder Kosten.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/tencent-ailab/Penguin-VL | Tencent AI Lab Penguin-VL Repository und Release-Historie | 2026-09-05 |
| https://huggingface.co/tencent/Penguin-VL-8B | tencent/Penguin-VL-8B Model Card | 2026-09-05 |
| https://huggingface.co/collections/tencent/penguin-vl | Tencent Penguin-VL Collection | 2026-09-05 |
| https://huggingface.co/spaces/tencent/Penguin-VL | Tencent Penguin-VL Space | 2026-09-05 |
| https://arxiv.org/abs/2603.06569 | Penguin-VL: Exploring the Efficiency Limits of VLM with LLM-based Vision Encoders | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:penguin-vl`, Thread `penguin-vl-public-release`, 1 datiertes Ereignis 2026-03-09 → 2026-03-09.
- **Praxishinweis:** Stand 2026-03-09 können Praktiker mit der Evaluation von Penguin-VL über die verlinkte Website, das Quellcode-Repository, die Hugging-Face-Collection und die Demo beginnen; prüfen Sie Fähigkeiten, Versionen, Lizenzierung und Anforderungen an die Bereitstellung anhand dieser primären Ressourcen, bevor Sie sich darauf verlassen.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
