---
title: "Self Gradient Forcing"
category: projects
date: 2026-07-24
tags: [project, self-gradient-forcing, self-gradient-forcing-development, self_gradient_forcing]
aliases: ["Self Gradient Forcing"]
level: 2
source_sha256: 2dcb78d6c268b7b354d36306549df95cc123d0316db21fd361432994ad847dd5
translation: machine
translated_at: '2026-10-24'
---
# Self Gradient Forcing {#self-gradient-forcing}

**Entwicklungslinie:** `project:self-gradient-forcing` · Thread `self-gradient-forcing-development`  
**Letztes Ereignis:** 2026-07-24 · 1 datiertes seit 2026-07-24 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Self Gradient Forcing (SGF) ist eine Trainingsmethode für autoregressive Video-Diffusionsmodelle. Sie spielt gesampelten, selbst erzeugten Kontext erneut ab, sodass Verluste für künftige Frames den kausalen KV-Speicher trainieren, ohne Gradienten über den gesamten Rollout zu speichern.

- Code und Checkpoints: aufbauend auf Wan2.1 T2V 1.3B und 14B als Basismodelle, in framewise- und chunkwise-Varianten.
- Zeithorizont: berichtetes Trainingsfenster von 5 Sekunden, mit Demonstrationen und Auswertungen bis zu 60 und 240 Sekunden.

Verwenden Sie es als Forschungsimplementierung für die Extrapolation von Videos über lange Zeithorizonte, nicht als sofort einsatzbereiten gehosteten Videogenerator.

## Entwicklungslinie {#development-line}

- **2026-07-24 — Projektressourcen zu Self Gradient Forcing wurden verlinkt.** Am 2026-07-24 wurden die Projektseite, das GitHub-Repository und die Hugging-Face-Modellseite verlinkt. Sie bieten Projektübersicht, Code und Modellgewichte an einem Ort. Die Links zeigen nicht, ob es sich um eine erste Veröffentlichung, ein Update oder einen anderen technischen Meilenstein handelt.

## Was sich geändert hat {#what-changed}

- 2026-07-22 — Das Paper führte eine begrenzte zweistufige Rekonstruktion ein, um die historische Kontext-Gradientenlücke bei Self Forcing mit eingefrorenem Cache zu schließen.
- 2026-07-23 — Die Autoren veröffentlichten das Paper, den Inferenz- und Trainingscode sowie die Modell-Checkpoints öffentlich.
- 2026-07-24 — Die verlinkte Projektseite, das Repository und die Modellsammlung machten die Veröffentlichung auffindbar und spezifizierten framewise- und chunkwise-Releases statt eines generischen Checkpoints.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-07-24 können Praktiker über die verlinkte Projektseite, das GitHub-Repository und die Hugging-Face-Seite die öffentliche Übersicht, die Implementierung und die Modellressourcen von Self Gradient Forcing finden.

1. Erstellen Sie eine Python-3.10-Umgebung, installieren Sie die Repository-Anforderungen und FlashAttention und installieren Sie anschließend das Projekt im Entwicklungsmodus.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
2. Führen Sie `scripts/download_weights.sh` aus; es lädt die Wan2.1-T2V-1.3B/14B-Basismodelle, Causal-Forcing-Initialisierungen, SGF-Checkpoints und Prompts herunter.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
3. Wählen Sie den passenden Release-Modus und führen Sie `bash scripts/infer_self_gradient_forcing.sh framewise` bzw. `chunkwise` aus; verwenden Sie die passende Konfiguration und den passenden Checkpoint.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
4. Für Training oder Adaption starten Sie das entsprechende framewise- oder chunkwise-Trainingsskript und erhalten die von SGF definierte Aufteilung in Rollout und Rekonstruktion.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>

## Bewährte Vorgehensweisen {#best-practices}

- Bewerten Sie das Verhalten über lange Zeithorizonte getrennt von kurzen Clips: Das Paper behandelt 5-Sekunden-VBench als Plausibilitätsprüfung und richtet den Hauptvergleich auf die Extrapolation über 60 und 240 Sekunden, wo sich Speicherfehler anhäufen.
  — <https://arxiv.org/abs/2607.20368>
- Halten Sie Release-Setting, Konfiguration und Checkpoint aufeinander abgestimmt: framewise- und chunkwise-Varianten verwenden unterschiedliche Cache-Geometrien und sind nicht austauschbar.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
- Verwenden Sie EMA-Gewichte für veröffentlichte oder trainierte Checkpoints, sofern Sie nicht bewusst die rohen Generatorgewichte vergleichen.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-07-22 — Self Forcing mit eingefrorenem Cache wird durch SGF nur für den fehlenden Kontext-Gradientenpfad abgelöst: SGF behält den gradientenfreien seriellen Rollout bei, rekonstruiert aber die gesampelte Berechnung so, dass künftige Verluste das Schreiben in den Speicher trainieren. Dies ist keine allgemeine Ablösung aller Self-Forcing-Workflows.

## Noch unbekannt {#still-unknown}

- Unabhängige Ergebnisse: Keine externe Reproduktion deckt Qualität, Rechenaufwand oder Kompatibilität ab; die berichteten Gewinne bei langen Zeithorizonten bleiben von den Autoren berichtet.
- Produktionsunterstützung: Das Release-Material legt keine stabile Support-Richtlinie für den Produktionseinsatz und keinen gepflegten Inferenzdienst fest.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2607.20368 | Self Gradient Forcing: Native Long Video Extrapolation | 2026-09-05 |
| https://github.com/zhuang2002/Self_Gradient_Forcing | zhuang2002/Self_Gradient_Forcing | 2026-09-05 |
| https://huggingface.co/JunhaoZhuang/Self_Gradient_Forcing | JunhaoZhuang/Self_Gradient_Forcing | 2026-09-05 |
| https://zhuang2002.github.io/SelfGradientForcing/ | Self Gradient Forcing: Native Long Video Extrapolation project page | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:self-gradient-forcing`, Thread `self-gradient-forcing-development`, 1 datiertes Ereignis 2026-07-24 → 2026-07-24.
- **Praktischer Hinweis:** Stand 2026-07-24 konnten Praktiker über die verlinkte Projektseite, das GitHub-Repository und die Hugging-Face-Seite die öffentliche Übersicht, die Implementierung und die Modellressource von Self Gradient Forcing finden.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich für das, was veraltet ist.
