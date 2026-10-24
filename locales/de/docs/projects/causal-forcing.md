---
title: "Causal Forcing++"
category: projects
date: 2026-05-16
tags: [causal-forcing, causal_forcing, project]
aliases: ["Causal Forcing++"]
level: 2
source_sha256: 822add77089fb85e34b6515892dfba2d61831de1ea5de65210d2f9ac7fd6f762
translation: machine
translated_at: '2026-10-24'
---
# Causal Forcing++ {#causal-forcing}

**Entwicklungslinie:** `project:causal-forcing` · Thread `causal-forcing`  
**Letztes Ereignis:** 2026-05-16 · 1 datiertes Ereignis seit 2026-05-16 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Causal Forcing++ ist eine Forschungspipeline und ein frame-weises Modell-Release für latenzarme Text-zu-Video- und Bild-zu-Video-Generierung.

- Kausale Konsistenzdistillation: ersetzt vorberechnete kausale ODE-Trajektorien vor dem asymmetrischen DMD.
- Referenz-Checkpoints: stellt frame-weise Modelle mit 1 Schritt und 2 Schritten bereit.
- Benchmark-Gewinne: übertrifft das chunk-weise Causal Forcing mit 4 Schritten in den Benchmarks des Papers, jedoch nicht als Garantie für den Produktivbetrieb.

## Entwicklungslinie {#development-line}

- **2026-05-16 — Öffentliche Projektressourcen zu Causal Forcing++ wurden erfasst.** Am 2026-05-16 haben wir Projektlinks zur Website, zum Quellcode-Repository und zum Hugging-Face-Repository erfasst. Die Links kennzeichnen öffentliche Projektressourcen, bestätigen aber weder eine bestimmte Version, ein technisches Ergebnis noch einen Nutzungsablauf.

## Was sich geändert hat {#what-changed}

2026-05-16 — Causal Forcing++ wurde mit kausaler Konsistenzdistillation und offenen frame-weisen Checkpoints mit 1 und 2 Schritten veröffentlicht. Die Repository-Historie datiert das Release auf 2026-05-15, nachdem Version 1 des Papers am 2026-05-14 eingereicht wurde.

## Anwendung {#how-to-use-this}

Ab dem 2026-05-16 können Anwender Causal Forcing++ über die verlinkten Projekt-, Quell- und Modellorte evaluieren. Der datierte Eintrag allein rechtfertigt keine konkreten Aussagen zu Deployment oder Leistung.

1. Lege eine Python-3.10-Umgebung an, installiere anschließend die Requirements, CLIP, FlashAttention und das Paket im Editable-Modus.
  — <https://github.com/thu-ml/Causal-Forcing>
2. Lade ein Wan2.1-Basismodell sowie entweder `causal-forcing++/framewise-1step.pt` oder `framewise-2step.pt` aus dem Modell-Repository herunter.
  — <https://github.com/thu-ml/Causal-Forcing>
3. Führe `inference.py` mit passenden frame-weisen Konfigurationen für 1 oder 2 Schritte sowie `--use_ema` aus. Verwende den frame-weisen Pfad mit einem Startbild für I2V.
  — <https://github.com/thu-ml/Causal-Forcing>

## Best Practices {#best-practices}

- Teste die Inferenz mit den veröffentlichten Checkpoints, bevor du die dreistufige Trainingspipeline ausführst.
  — <https://github.com/thu-ml/Causal-Forcing>
- Wechsle das Training von BF16 zu FP32, wenn causal-CD oder DMD divergiert oder Frames unscharf bleiben.
  — <https://github.com/thu-ml/Causal-Forcing>
- Verwende das Basismodell nicht über 81 Frames hinaus; für Videos im Minutenbereich nutze Rolling Forcing.
  — <https://github.com/thu-ml/Causal-Forcing>

## Ersetzt durch diesen Stand {#superseded-by-this}

- 2026-05-15 — Causal Forcing++ ersetzt den kausalen ODE-Schritt der Stufe 2 bei der Initialisierung von Modellen mit wenigen Schritten, ohne gepaarte ODE-Trajektorien zu speichern.
- 2026-05-15 — Frame-weise Checkpoints mit 1 und 2 Schritten ersetzen die Annahme, dass Causal Forcing nur als chunk-weises Modell mit 4 Schritten läuft.

## Weiterhin unbekannt {#still-unknown}

- Für das Release werden keine separaten Ereignisprotokolle und keine strukturierten Ereignis-Feeds bereitgestellt.
- Die offizielle Dokumentation deckt nur den Forschungscode und die Checkpoints ab; verifizierte Anleitungen für den Produktivbetrieb oder Hardwareanforderungen gibt es nicht.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://thu-ml.github.io/CausalForcing.github.io/ | Causal-Forcing-Projektseite | 2026-09-05 |
| https://github.com/thu-ml/Causal-Forcing | Offizielles Repository und README von thu-ml/Causal-Forcing | 2026-09-05 |
| https://github.com/thu-ml/Causal-Forcing/commits/main | Commit-Historie von Causal-Forcing | 2026-09-05 |
| https://huggingface.co/zhuhz22/Causal-Forcing/tree/main | Modelldateien von zhuhz22/Causal-Forcing | 2026-09-05 |
| https://arxiv.org/abs/2605.15141 | Causal Forcing++: Scalable Few-Step Autoregressive Diffusion Distillation for Real-Time Interactive Video Generation | 2026-09-05 |

## Kurzbriefing für Agenten {#agent-brief}

- **Gegenstand:** `project:causal-forcing`, Thread `causal-forcing`, 1 datiertes Ereignis vom 2026-05-16 bis 2026-05-16.
- **Praxishinweis:** Ab dem 2026-05-16 können Anwender Causal Forcing++ über die verlinkten Projekt-, Quell- und Modellorte evaluieren; der datierte Eintrag allein rechtfertigt keine konkreten Aussagen zu Implementierung oder Leistung.
- **Konfidenz:** hoch. Datierte Ersetzungsvermerke oben kennzeichnen, was veraltet ist.
