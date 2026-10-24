---
title: "V-JEPA"
category: projects
date: 2026-03-20
tags: [project, v-jepa]
aliases: ["V-JEPA"]
level: 2
source_sha256: 78a744eb9d05bf488c78c7d804b5fbd19279d2f16eabc5dbf7515509d3c5f4d4
translation: machine
translated_at: '2026-10-24'
---
# V-JEPA {#v-jepa}

**Entwicklungslinie:** `project:v-jepa` · Thread `v-jepa`  
**Letztes Ereignis:** 2026-03-20 · 1 datiertes Ereignis seit 2026-03-20 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

V-JEPA ist eine Familie von PyTorch-Modellen von Meta für Entwickler im Bereich Video-Verständnis und Robotik. — extrahiert Repräsentationen aus Videos ohne manuelle Annotation; — sagt Aktionen und Zustände im latenten Raum voraus; — V-JEPA 2-AC ergänzt aktionskonditionierte Planung für Manipulatoren; — V-JEPA 2.1 ist auf räumlich und zeitlich konsistente Dense-Features ausgerichtet. Die 2.1-Linie umfasst ViT-B mit 80M, ViT-L mit 300M, ViT-g mit 1B und ViT-G mit 2B Parametern bei 384 px. Fazit: Für neue Aufgaben in Segmentierung, Depth, Tracking und Video-Features sollte man mit V-JEPA 2.1 beginnen; 2-AC ist nur nötig, um den robotischen Forschungsablauf zu reproduzieren.

## Entwicklungslinie {#development-line}

- **2026-03-20 — V-JEPA wurde mit dem V-JEPA-2-Repository verknüpft.** Familie von Dense-Video/Image-Encodern mit Dense Predictive Loss, Deep Self-Supervision und multimodalen Tokenizern; die erste Ankündigung im README ist auf 2026-03-16 datiert, der Artikel wurde am 2026-03-15 veröffentlicht.

## Was sich geändert hat {#what-changed}

2026-03-20 — Im V-JEPA-Repository war V-JEPA 2.1 verfügbar: eine Familie von Dense-Video/Image-Encodern mit Dense Predictive Loss, Deep Self-Supervision und multimodalen Tokenizern; die erste Ankündigung im README ist auf 2026-03-16 datiert, der Artikel wurde am 2026-03-15 veröffentlicht. 2025-06-11 — Meta stellte V-JEPA 2 vor, ein Video-World-Model mit 1,2 Mrd. Parametern, sowie V-JEPA 2-AC: eine aktionskonditionierte Variante, die mit weniger als 62 Stunden unannotierten DROID-Videos für Zero-Shot-Pick-and-Place feinabgestimmt wurde. 2026-03-15 — Der Artikel zu V-JEPA 2.1 ergänzte vier Checkpoint-Größen von 80M bis 2B und meldete Verbesserungen bei Dense-Aufgaben, darunter 0,307 RMSE auf NYUv2 und 77,7 % auf Something-Something-V2.

## Verwendung {#how-to-use-this}

As of 2026-03-20, practitioners should treat the linked facebookresearch/vjepa2 repository as the recorded implementation reference for this V-JEPA line; the sealed evidence alone does not justify operational guidance beyond that.

Stand 2026-03-20 sollten Praktiker das verlinkte Repository facebookresearch/vjepa2 als dokumentierte Implementierungsreferenz für diese V-JEPA-Linie behandeln; die gesicherte Evidenz allein rechtfertigt keine darüber hinausgehenden operativen Empfehlungen.

1. Installieren Sie PyTorch, timm und einops; für den lokalen Start ist ein PyTorch-Build mit CUDA zu bevorzugen.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
2. Laden Sie den Preprocessor und das gewünschte 2.1-Backbone über torch.hub; für einen geringeren Ressourcenbedarf beginnen Sie mit vjepa2_1_vit_base_384, für maximale Qualität mit gigantic.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
3. Verarbeiten Sie Videos mit dem Encoder und trainieren Sie einen leichtgewichtigen Head oder einen Linear Probe für Ihre Downstream-Aufgabe; die fertige Demo zeigt Inferenz auf Videos.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
4. Für ein robotisches Experiment verwenden Sie V-JEPA 2-AC mit Image Goals und Model-Predictive Control; dies ist ein eigenständiger aktionskonditionierter Checkpoint und kein gewöhnlicher 2.1-Encoder.
  — <https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/>

## Best Practices {#best-practices}

- Wählen Sie V-JEPA 2.1 für Dense-Repräsentationen: Das Release ändert gezielt Objective und Tokenizer für räumlich-zeitliche Konsistenz und vergrößert nicht nur das Modell.
  — <https://arxiv.org/abs/2603.14482>
- Passen Sie die Checkpoint-Größe an Aufgabe und Ressourcen an: Für 2.1 bei 384 px sind Varianten mit 80M, 300M, 1B und 2B verfügbar.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
- Unter macOS ersetzen Sie decord vorab: Das Basispaket unterstützt macOS nicht; die Autoren legen keinen bestimmten empfohlenen Fork fest.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>

## Dadurch ersetzt {#superseded-by-this}

- 2026-03-15 — Für neue Aufgaben mit Dense-Video/Image-Repräsentationen ist das bisherige V-JEPA 2 kein bevorzugter Ausgangspunkt mehr: V-JEPA 2.1 wurde gerade zur Verbesserung von Dense- und zeitlich konsistenten Features veröffentlicht.
- 2026-03-15 — V-JEPA 2.1 darf nicht als neuer aktionskonditionierter Robotik-Checkpoint gelten: V-JEPA 2-AC bleibt ein eigenständiger Post-Training-Zweig von V-JEPA 2.

## Weiterhin unbekannt {#still-unknown}

- Das offizielle Repository veröffentlicht keine GitHub Releases. Das Datum des Schritts 2026-03-20 ist bestätigt als Vorhandensein von V-JEPA 2.1 im Repository; die primären Daten des Artikels und des README sind jedoch 2026-03-15 bzw. 2026-03-16.
- Die offiziellen Anleitungen zeigen PyTorch Hub für V-JEPA 2.1, das Transformers-Beispiel im README nennt jedoch nur V-JEPA-2-Repositorys; die Unterstützung von 2.1 über diesen Weg ist im README nicht belegt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/facebookresearch/vjepa2 | facebookresearch/vjepa2 — offizielles Repository | 2026-09-05 |
| https://github.com/facebookresearch/vjepa2/blob/main/README.md | README des V-JEPA-2-Repositorys | 2026-09-05 |
| https://arxiv.org/abs/2603.14482 | V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning | 2026-09-05 |
| https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/ | Introducing the V-JEPA 2 world model and new benchmarks for physical reasoning | 2026-09-05 |
| https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/ | V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:v-jepa`, Thread `v-jepa`, 1 datiertes Ereignis 2026-03-20 → 2026-03-20.
- **Praktischer Hinweis:** Stand 2026-03-20 sollten Praktiker das verlinkte Repository facebookresearch/vjepa2 als dokumentierte Implementierungsreferenz für diese V-JEPA-Linie behandeln; die gesicherte Evidenz allein rechtfertigt keine darüber hinausgehenden operativen Empfehlungen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
