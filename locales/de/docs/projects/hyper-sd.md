---
title: "Hyper-SD"
category: projects
date: 2024-08-28
tags: [hyper-sd, hyper_sd, project]
aliases: ["Hyper-SD"]
level: 2
source_sha256: 4a59d57496f629bdff7207b1e05ee4609fb6e70f505efa08197759c43cd0b356
translation: machine
translated_at: '2026-10-24'
---
# Hyper-SD {#hyper-sd}

**Entwicklungslinie:** `project:hyper-sd` · Thread `hyper-sd`  
**Letztes Ereignis:** 2024-08-28 · 2 datierte seit 2024-04-22 · **Recherchiert:** 2026-09-04 · Konfidenz: medium

## Was es ist {#what-it-is}

Hyper-SD — destillierte LoRAs und ein einzelnes SDXL-UNet für die Generierung mit weniger Schritten statt des üblichen mehrstufigen Samplings. — N-Step-LoRA für SDXL, SD1.5, SD3 und FLUX.1-dev. — Unified LoRA mit 1–8 Schritten für SDXL und SD1.5. — ControlNet-Beispiele und fertige ComfyUI-Workflows für SDXL/SD1.5. Grenze: Dies ist kein universelles Basismodell; FLUX.1-dev und SD3 erfordern Zugang zu geschlossenen Basisgewichten. Fazit: Nur mit einer exakt benannten, unterstützten Basis verwenden und Einstellungen nicht ungeprüft auf neue Modellfamilien übertragen.

## Entwicklungslinie {#development-line}

- **2024-04-22 — Hyper-SD veröffentlichte erstmals öffentliche Modelle und interaktive Demos.** Am 2024-04-22 veröffentlichte Hyper-SD eine öffentliche Projektseite und ein Modell-Repository sowie interaktive Demonstrationen für One-Step-XL-Text-zu-Bild und scribble-gesteuerte Workflows. Dies war ein Meilenstein der öffentlichen Verfügbarkeit des Projekts. Die verlinkten Ressourcen allein belegen keine Trainingsdetails, Benchmark-Ergebnisse oder exakten Release-Versionen.
- **2024-08-28 — Hyper-SD ergänzte FLUX.1-dev-LoRA-Checkpoint-Varianten.** Am 2024-08-28 ergänzte Hyper-SD zwei LoRA-Checkpoint-Varianten für FLUX.1-dev, entsprechend 8-Schritt- und 16-Schritt-Generierung. Damit wurde die öffentliche Artefaktlinie des Projekts auf einen FLUX.1-dev-Workflow erweitert. Die datierten Links belegen weder Qualität oder Lizenzierung der Checkpoints noch, ob sie frühere Hyper-SD-Artefakte ersetzt haben.

## Was sich geändert hat {#what-changed}

Hyper-SD — Entwicklungslinie von der Beschleunigung von SDXL/SD1.5 hin zu vier konkreten Basismodell-Familien. — 2024-04-22: praktische Einstiegspunkte erschienen — das Gewichte-Repository, Hyper-SDXL One-Step-Text-zu-Bild und Hyper-SD15 Scribble. — 2024-04-30 und 2024-05-13 [heute gefunden]: CFG-preserved LoRAs mit 8 und 12 Schritten für SDXL und SD1.5 ergänzt, ausgelegt auf CFG 5–8. — 2024-08-19 [heute gefunden]: CFG-LoRAs für SD3 mit 4, 8 und 16 Schritten ergänzt. — 2024-08-28: Hyper-FLUX.1-dev-LoRAs mit 8 und 16 Schritten ergänzt; die offizielle Modellkarte datiert deren Verfügbarkeit auf 2024-08-26. — 2024-11-04 [heute gefunden]: Artikel auf v3 aktualisiert und auf NeurIPS 2024 angenommen; ein neuer Checkpoint wird in diesem Eintrag nicht ausgewiesen. — 2026-09-04 [heute gefunden]: Die aktuelle offizielle Modellkarte dokumentiert weiterhin FLUX.1-dev, SD3-Medium, SDXL Base 1.0 und SD v1.5, beansprucht aber keine Unterstützung neuerer Familien. Messwert: Jede der geprüften FLUX-LoRAs mit 8 und 16 Schritten belegt 1,39 GB. Fazit: Der aktuelle praktische Anwendungsbereich ist die Beschleunigung dieser festgelegten Basen, nicht ein allgemeiner Adapter für neue Diffusionsmodelle.

## Anwendung {#how-to-use-this}

Ab 2024-04-22 konnten Anwender Hyper-SD über die öffentlichen Modell- und Demo-Ressourcen evaluieren. Ab 2024-08-28 sollten Anwender, die mit FLUX.1-dev arbeiten, die 8-Schritt- oder 16-Schritt-Hyper-SD-LoRA-Variante auswählen und testen, statt anzunehmen, dass die früheren Hyper-SD-Artefakte unverändert gelten.

1. Hyper-SD: Wählen Sie genau eine unterstützte Basis und eine LoRA derselben Familie mit der gewünschten Schrittzahl; verwenden Sie nicht eine Datei universell für SDXL, SD1.5, SD3 und FLUX.
  — <https://huggingface.co/ByteDance/Hyper-SD>
2. Hyper-SD: Für FLUX.1-dev oder SD3 holen Sie sich zuerst Zugang zum Basismodell, laden dann die LoRA über eine kompatible Diffusers-Pipeline, fusen Sie sie und verschieben die Pipeline auf CUDA.
  — <https://huggingface.co/ByteDance/Hyper-SD>
3. Hyper-SD: Beginnen Sie mit den offiziellen Einstellungen der Familie — für FLUX.1-dev verwenden Sie LoRA-Scale um 0.125, 8 oder 16 Schritte und Guidance 3.5; für SD3 verwenden Sie Scale 0.125 und Guidance 3/5/7 bei 4/8/16 Schritten.
  — <https://huggingface.co/ByteDance/Hyper-SD>
4. Hyper-SD: Für SDXL/SD1.5-N-Step-LoRAs setzen Sie DDIM mit Timestep-Spacing trailing; für Unified LoRA verwenden Sie TCDScheduler und stimmen die Schrittzahl mit eta ab.
  — <https://huggingface.co/ByteDance/Hyper-SD>
5. Hyper-SD: Importieren Sie in ComfyUI den Workflow, der zur Gewichtsfamilie passt; für das One-Step-SDXL-UNet installieren Sie den beigelegten Custom Scheduler in custom_nodes.
  — <https://huggingface.co/ByteDance/Hyper-SD/tree/main/comfyui>

## Bewährte Vorgehensweisen {#best-practices}

- Hyper-SD: Reproduzieren Sie zuerst die offizielle Baseline mit einem Prompt und der Zielschrittzahl und ändern Sie erst danach LoRA-Scale, CFG oder eta.
  — <https://huggingface.co/ByteDance/Hyper-SD>
- Hyper-SD: Mischen Sie keine Scheduler-Ansätze — N-Step-Varianten verwenden DDIM trailing, Unified-Varianten verwenden TCDScheduler.
  — <https://huggingface.co/ByteDance/Hyper-SD>
- Hyper-SD: Bei ControlNet behalten Sie dieselbe Basismodell-Familie und dasselbe Sampler-Rezept wie im offiziellen Beispiel bei, statt Einstellungen zwischen SDXL und SD1.5 zu übertragen.
  — <https://huggingface.co/ByteDance/Hyper-SD>
- Hyper-SD: Verwenden Sie für ComfyUI den veröffentlichten Workflow als Startkonfiguration; das One-Step-SDXL-UNet reproduziert ohne den erforderlichen Scheduler-Custom-Node nicht den angegebenen Timestep-800-Modus.
  — <https://huggingface.co/ByteDance/Hyper-SD/tree/main/comfyui>

## Durch dieses ersetzt {#superseded-by-this}

- 2024-04-22 — Die Darstellung von Hyper-SD nur als Beschleuniger für SDXL/SD1.5 ist nach den offiziellen LoRAs für SD3 vom 2024-08-19 und FLUX.1-dev vom 2024-08-26 unvollständig geworden.
- 2024-04-22 — Die Übertragung der Einstellungen der One-Step-Demo auf alle Basen taugt nicht mehr: Die späteren offiziellen Anleitungen trennen FLUX, SD3, SDXL und SD1.5 nach LoRA, Scheduler, CFG und Schrittzahl. Kein früher Checkpoint ist offiziell als deprecated markiert.

## Weiterhin unbekannt {#still-unknown}

- Die offizielle Unterstützung von Flux.1 Kontext, Flux.2, SD3.5, SDXL-abgeleiteten Checkpoints sowie aktuellen ComfyUI- und Diffusers-Versionen ist nicht bestätigt.
- Die aktuelle Modellkarte endet mit der Checkpoint-Ankündigung vom 2024-08-26; das beweist keine Einstellung des Projekts, aber eine neuere Roadmap wurde nicht gefunden.
- Hugging-Face-Spaces existieren, doch ihre erfolgreiche Generierung unter aktueller Last wurde nicht geprüft.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://hyper-sd.github.io/ | Hyper-SD: Trajectory Segmented Consistency Model for Efficient Image Synthesis | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD | ByteDance/Hyper-SD | 2026-09-04 |
| https://huggingface.co/spaces/ByteDance/Hyper-SDXL-1Step-T2I | Hyper SDXL 1Step T2I | 2026-09-04 |
| https://huggingface.co/spaces/ByteDance/Hyper-SD15-Scribble | Hyper SD15 Scribble | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD/blob/main/Hyper-FLUX.1-dev-8steps-lora.safetensors | Hyper-FLUX.1-dev-8steps-lora.safetensors | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD/blob/main/Hyper-FLUX.1-dev-16steps-lora.safetensors | Hyper-FLUX.1-dev-16steps-lora.safetensors | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD/tree/main/comfyui | ByteDance/Hyper-SD ComfyUI workflows | 2026-09-04 |
| https://arxiv.org/abs/2404.13686 | Hyper-SD: Trajectory Segmented Consistency Model for Efficient Image Synthesis | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:hyper-sd`, Thread `hyper-sd`, 2 datierte Ereignisse 2024-04-22 → 2024-08-28.
- **Praxishinweis:** Ab 2024-04-22 konnten Anwender Hyper-SD über die öffentlichen Modell- und Demo-Ressourcen evaluieren. Ab 2024-08-28 sollten Anwender, die mit FLUX.1-dev arbeiten, die 8-Schritt- oder 16-Schritt-Hyper-SD-LoRA-Variante auswählen und testen, statt anzunehmen, dass die früheren Hyper-SD-Artefakte unverändert gelten.
- **Konfidenz:** medium. Die datierten Einträge unter „Durch dieses ersetzt" oben sind maßgeblich dafür, was veraltet ist.
