---
title: "Flux2-Klein-9B-Consistency"
category: projects
date: 2026-03-13
tags: [flux2-klein-9b-consistency, flux2-klein-9b-consistency-releases, lora_releases, project]
aliases: ["Flux2-Klein-9B-Consistency"]
level: 2
source_sha256: 3a558395c18179aa744aba75df8accb316aa78ce4d3036e4674b5458aa8b52f9
translation: machine
translated_at: '2026-10-24'
---
# Flux2-Klein-9B-Consistency {#flux2-klein-9b-consistency}

**Entwicklungslinie:** `project:flux2-klein-9b-consistency` · Thread `flux2-klein-9b-consistency-releases`  
**Letztes Ereignis:** 2026-03-13 · 1 datiertes seit 2026-03-13 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Flux2-Klein-9B-Consistency ist ein Image-to-Image-LoRA für das Basismodell black-forest-labs/FLUX.2-klein-9B.

- Erhaltung von Bildaufbau und Details bei semantischer Bearbeitung.
- Reduzierter Farbstich und geringere Übersättigung in V2.

Der Adapter ist kein eigenständiges 9B-Modell; die Lizenzbedingungen des Basismodells gelten separat. V2 eignet sich für die kontrollierte Bearbeitung von Quellbildern, nicht als allgemeiner Generator.

## Entwicklungslinie {#development-line}

- **2026-03-13 — Flux2-Klein-9B-Consistency-Ressource verlinkt.** Am 2026-03-13 verlinkte die Flux2-Klein-9B-Consistency-Linie eine Hugging-Face-Ressource von dx8152 sowie ein YouTube-Video. Die Links markieren einen Meilenstein der öffentlichen Verfügbarkeit, belegen aber weder Modellfähigkeiten, Versionsdetails noch vorgesehenen Workflow.

## Was sich geändert hat {#what-changed}

- 2026-03-13 — Consistency-Adapter für FLUX.2 Klein 9B veröffentlicht; ein Drittanbieter-Eintrag vom 2026-03-06 spezifizierte den Workflow-Graphen und CFG=1.
- 2026-04-17 — Flux2-Klein-9B-consistency-V2.safetensors hinzugefügt, um Farbstich, übermäßige Detailschärfe und Übersättigung aus V1 zu beheben. Die V2-Datei ist 331 MB groß, SHA-256 61db2017ce420b97bd5ef11984e5a894c90003a6bbf0dc9473f8d7b9ebb3ff93.

## Anwendung {#how-to-use-this}

Prüfe vor dem Einsatz das Hugging-Face-Repository von dx8152 und das verlinkte Video vom 2026-03-13, um die Eignung zu beurteilen.

1. Aktuelle diffusers, transformers und accelerate installieren; das Basismodell black-forest-labs/FLUX.2-klein-9B in bfloat16 auf CUDA laden.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
2. Adapter-Gewichte über load_lora_weights("dx8152/Flux2-Klein-9B-Consistency") laden und das Quellbild mit Bearbeitungsanweisungen übergeben.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
3. Für lokales ComfyUI das 9B-Basismodell, den Qwen-3-8B-Text-Encoder und das flux2-VAE in den jeweiligen Verzeichnissen ablegen und das LoRA anschließend in einem Image-Edit-Workflow anwenden.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>

## Best Practices {#best-practices}

- V2 gegenüber V1 bevorzugen: Die Version behebt Farbverschiebung, verrauschte Details und Übersättigung.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
- Bei Kombination mit Beleuchtungs-LoRAs mit Stärke 0,3–0,5 beginnen: Dies schützt die Details, dämpft aber die Lichtveränderung.
  — <https://www.patreon.com/foxfuressence/posts/lighting-angle-162733880>
- Gegen die eigene Basismodellversion und den eigenen Workflow testen: Nutzerberichte weichen voneinander ab, wobei schlechte Ergebnisse bei FP8- und GGUF-Varianten gemeldet wurden.
  — <https://www.reddit.com/r/comfyui/comments/1rv6juw/fixing_the_plastic_look_in_flux2_klein_9b_with/>

## Abgelöst durch {#superseded-by-this}

- 2026-04-17 — V1 ist veraltet, sobald neutrale Farben, saubere Details und kontrollierte Sättigung wichtig sind.

## Weiterhin unbekannt {#still-unknown}

- Primärprotokolle bestätigen das genaue Upload-Datum von V1 nicht; Einträge vom 2026-03-06 bestätigen das Basismodell, den Zweck und CFG=1 für die Veröffentlichung vom 2026-03-13.
- Video JXMbbbdfnSg war nicht lesbar, daher wurde sein Inhalt nicht als Beleg verwendet.
- Kein unabhängiger, reproduzierbarer Benchmark bestätigt die behaupteten Konsistenzgewinne; Nutzerberichte weichen in Qualität und Kompatibilität voneinander ab.
- Das Adapter-Repository nennt Apache-2.0, während die Dokumentation von BFL für 9B Base die FLUX Non-Commercial License vorgibt; vor kommerzieller Nutzung die Gewichte des Basismodells prüfen.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency | dx8152/Flux2-Klein-9B-Consistency | 2026-09-05 |
| https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency/commit/ab936d843fea26adb9fac23132d7fc834c529ed7 | Upload Flux2-Klein-9B-consistency-V2.safetensors | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1rm3g3j/dx8152_flux_2_klein_9b_consistency_lora/ | DX8152 Flux 2 Klein 9b consistency lora | 2026-09-05 |
| https://docs.comfy.org/tutorials/flux/flux-2-klein | ComfyUI Flux.2 Klein Guide | 2026-09-05 |
| https://www.patreon.com/foxfuressence/posts/lighting-angle-162733880 | Lighting Angle Change workflow! | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1rv6juw/fixing_the_plastic_look_in_flux2_klein_9b_with/ | Fixing the „Plastic“ Look in Flux.2 Klein 9B with the Consistency LoRA | 2026-09-05 |
| https://docs.bfl.ai/flux_2/flux2_klein_training | FLUX.2 [klein] Training | 2026-09-05 |

## Agent brief {#agent-brief}

- **Gegenstand:** `project:flux2-klein-9b-consistency`, Thread `flux2-klein-9b-consistency-releases`, 1 datiertes Ereignis 2026-03-13 → 2026-03-13.
- **Praxishinweis:** Stand 2026-03-13 sollten Praktiker Flux2-Klein-9B-Consistency als öffentlich verlinkte Ressource von dx8152 einordnen und deren Hugging-Face-Seite sowie das verlinkte Video prüfen, bevor sie entscheiden, ob sie in ihren Workflow passt; Fähigkeiten und Kompatibilität bleiben ungeprüft.
- **Konfidenz:** mittel. Die datierten Abschnitte „Abgelöst durch“ sind maßgeblich dafür, was veraltet ist.
