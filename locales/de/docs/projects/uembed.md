---
title: "UEmbed"
category: projects
date: 2026-08-05
tags: [project, uembed]
aliases: ["UEmbed"]
level: 2
source_sha256: 0b0c651112c74bbff7033a302689e783a3f2f33ef58f1f869714077e4bca9789
translation: machine
translated_at: '2026-10-24'
---
# UEmbed {#uembed}

**Entwicklungslinie:** `project:uembed` · Thread `uembed`  
**Letztes Ereignis:** 2026-08-05 · 1 datiertes Ereignis seit 2026-08-05 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

UEmbed ist eine auf Qwen3.5 basierende Embedding-Familie mit reinem Decoder für Teams, die andernfalls separate dichte und dünnbesetzte Retriever betreiben müssten.

- Dichte und dünnbesetzte Repräsentationen: erzeugt normalisierte dichte Vektoren und dünnbesetzte lexikalische Vektoren in einem einzigen kausalen Forward-Durchlauf.
- Multimodale Kodierung: kodiert Text, Bilder, Videos und gemischte Eingaben für Retrieval und die Suche in visuellen Dokumenten.
- Modellfamilie: wird als UEmbed-2B, UEmbed-4B und UEmbed-9B ausgeliefert; die Inferenz mit dünnbesetzten Vektoren erfordert die Zusatzdateien `sparse_info.json` und `sparse_weights.pt`.

## Entwicklungslinie {#development-line}

- **2026-08-05 — Öffentliches UEmbed-Projekt, Code und UEmbed-9B-Ressourcen wurden verlinkt.** Am 2026-08-05 haben wir die offizielle Projektseite, das zugehörige GitHub-Quellcode-Repository und die UEmbed-9B-Modellseite auf Hugging Face verlinkt. Die datierten Links belegen einen öffentlich sichtbaren Meilenstein zur Verfügbarkeit von Projekt und Modell, belegen aber keine bestimmte Release-Version, keinen Benchmark und keine Leistungsaussage.

## Was sich geändert hat {#what-changed}

- 2026-08-05 — Die erste Veröffentlichung von UEmbed wurde als multimodale Decoder-only-Checkpoints mit 2B, 4B und 9B dokumentiert, die dichte und dünnbesetzte Repräsentationen ausgeben.
- 2026-08-13 — Die Inferenz wurde auf das native Laden über Transformers umgestellt, ohne `trust_remote_code` oder Processor-Patching, und erhielt ein vLLM-Backend für das Serving dichter und dünnbesetzter Repräsentationen.
- 2026-08-15 — Das Projekt meldete Spitzenplatzierungen bei MMEB-v3 in den Tracks Text und Agenten sowie den zweiten Platz unter offenen Modellen bei MMEB-v2, hinter Qwen3-VL-Embedding.
- 2026-08-17 — Unterstützung für überwachtes Feintuning mit ms-swift wurde hinzugefügt.

## Verwendung {#how-to-use-this}

Ab 2026-08-05 können wir UEmbed über die offizielle Projektdokumentation evaluieren, das Quellcode-Repository prüfen und die UEmbed-9B-Modellressource finden. Leiten Sie keine ungeprüften Leistungs- oder Kompatibilitätsaussagen ab.

1. Installieren Sie eine aktuelle, mit Qwen3.5/Qwen3-VL kompatible Laufzeitumgebung: `transformers>=5.4.0`, PyTorch, qwen-vl-utils, tokenizers, Hugging Face Hub, Pillow und NumPy.
  — <https://github.com/Alibaba-NLP/UEmbed>
2. Wählen Sie den Checkpoint mit 2B, 4B oder 9B und laden Sie das vollständige Repository herunter; bewahren Sie die Sparse-Zusatzdateien zusammen mit den Gewichten auf.
  — <https://github.com/Alibaba-NLP/UEmbed>
3. Laden Sie `Qwen35Embedder`, übergeben Sie Dictionaries mit Text-, Bild-, Video- oder gemischten Eingaben und geben Sie bei Retrieval-Anfragen gegebenenfalls eine aufgabenspezifische Instruktion an.
  — <https://huggingface.co/Alibaba-NLP/UEmbed-9B>
4. Wählen Sie `pooling="last.normal"` für dichte Vektoren oder `pooling="splade.last"` für dünnbesetzte lexikalische Vektoren und senden Sie die gewählte Repräsentation an den passenden Retrieval-Index.
  — <https://github.com/Alibaba-NLP/UEmbed>

## Best Practices {#best-practices}

- Laden Sie das gesamte Checkpoint-Repository herunter; der Sparse-Modus funktioniert nicht ohne beide Sparse-Zusatzdateien.
  — <https://github.com/Alibaba-NLP/UEmbed>
- Instanziieren Sie nur den dichten oder dünnbesetzten Pooling-Modus, den der Retrieval-Pfad benötigt, statt anzunehmen, dass ein Ausgabeformat für beide Indizes passt.
  — <https://github.com/Alibaba-NLP/UEmbed>
- Verwenden Sie aufgabenspezifische Query-Instruktionen für das Retrieval, und setzen Sie BF16 zusammen mit FlashAttention 2 nur ein, wenn GPU und Laufzeitumgebung dies unterstützen.
  — <https://github.com/Alibaba-NLP/UEmbed>

## Abgelöst durch diese Angaben {#superseded-by-this}

- 2026-08-13 — Frühere Inferenzhinweise, die `trust_remote_code` oder Processor-Patching voraussetzten, sind für den offiziellen nativen Transformers-Pfad überholt.

## Weiterhin unbekannt {#still-unknown}

- Es wurde kein unveränderlicher Snapshot des Repositorys oder der Modellkarte gefunden, der unabhängig belegt, dass alle drei Checkpoint-Dateien am 2026-08-05 herunterladbar waren; das Paper gibt an, dass sie veröffentlicht wurden, während die datierten Links die 9B-Karte enthalten.
- Die Benchmark-Angaben vom 2026-08-15 stammen vom Projekt selbst und wurden nicht unabhängig reproduziert.
- Die Hugging-Face-Karte bezeichnet den Checkpoint als UEmbed-9B, zeigt aber „Model size 8B params“ an; die offiziellen Materialien erklären die Abweichung nicht.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://alibaba-nlp.github.io/UEmbed/ | UEmbed: Unified Sparse and Dense Multimodal Embeddings | 2026-09-05 |
| https://github.com/Alibaba-NLP/UEmbed | Alibaba-NLP/UEmbed | 2026-09-05 |
| https://huggingface.co/Alibaba-NLP/UEmbed-9B | Alibaba-NLP/UEmbed-9B | 2026-09-05 |
| https://arxiv.org/abs/2608.02583 | UEmbed: Unified Sparse and Dense Multimodal Embeddings | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:uembed`, Thread `uembed`, 1 datiertes Ereignis vom 2026-08-05 → 2026-08-05.
- **Praktischer Hinweis:** Ab 2026-08-05 können wir UEmbed über die offizielle Projektdokumentation evaluieren, das Quellcode-Repository prüfen und die UEmbed-9B-Modellressource finden. Leiten Sie keine ungeprüften Leistungs- oder Kompatibilitätsaussagen ab.
- **Konfidenz:** mittel. Die datierten Abschnitte „Abgelöst durch diese Angaben“ sind maßgeblich dafür, was überholt ist.
