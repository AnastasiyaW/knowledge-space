---
title: "Stable Diffusion 3"
category: projects
date: 2024-02-22
tags: [project, stable-diffusion-3]
aliases: ["Stable Diffusion 3", "Stable Diffusion 3 Medium"]
level: 2
source_sha256: f285f052d3e242d89cf829682aaab4f9c7738883573c2c590297a330558ee807
translation: machine
translated_at: '2026-10-24'
---
# Stable Diffusion 3 {#stable-diffusion-3}

**Entwicklungslinie:** `project:stable-diffusion-3` · Thread `stable-diffusion-3`  
**Letztes Ereignis:** 2024-02-22 · 1 datiertes Ereignis seit 2024-02-22 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Stable Diffusion 3 ist eine Familie von MMDiT-Text-to-Image-Modellen von Stability AI für ComfyUI, Diffusers und die API. Funktionen: Generierung aus Text, komplexe Kompositionen, Typografie und Image-to-Image über unterstützte Pipelines. SD3 Medium ist ein gated Modell mit 2B Parametern; für Organisationen mit kommerzieller Nutzung und einem Jahresumsatz über $1M ist eine Enterprise-Lizenz erforderlich. Fazit: SD3 Medium ist verfügbar, doch Stability AI selbst hat eingeräumt, dass der erste offene Release der Serie die Erwartungen nicht erfüllt hat, und hat SD 3.5 als Ersatzlinie veröffentlicht.

## Entwicklungslinie {#development-line}

- **2024-02-22 — Stability AI kündigte Stable Diffusion 3 an.** Angekündigt wurde eine Reihe von 0,8B–8B mit Diffusion Transformer und Flow Matching.

## Änderungen {#what-changed}

2024-02-22 — Stability AI eröffnete eine Early-Preview-Warteliste für Stable Diffusion 3: angekündigt wurde eine Reihe von 0,8B–8B mit Diffusion Transformer und Flow Matching. 2024-06-03 — Der gespeicherte Link führt zu einem nicht mehr verfügbaren Reddit-Short-Link; eine überprüfbare Modelländerung lässt sich darüber nicht feststellen. 2024-06-12 — Die offenen Gewichte von Stable Diffusion 3 Medium, einem Modell mit 2B Parametern, wurden veröffentlicht. 2024-10-22 — Stable Diffusion 3.5 Large und 3.5 Large Turbo erschienen; das Unternehmen stellte ausdrücklich fest, dass das Juni-SD3-Medium nicht seinen Erwartungen entsprach. 2024-10-29 — Stable Diffusion 3.5 Medium kam zur Reihe hinzu.

## Wie man das nutzt {#how-to-use-this}

Ab 2024-02-22 sollten Praktiker Stable Diffusion 3 als offiziell angekündigtes Projekt behandeln und die offiziellen News- und Projektseiten für verifizierte Updates verfolgen.

1. Legen Sie ein Hugging-Face-Konto an, akzeptieren Sie die Zugriffsbedingungen des gated Repositorys und laden Sie die Gewichte von SD3 Medium oder eine kompatible Diffusers-Version herunter.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
2. Für den lokalen Start in ComfyUI verwenden Sie die beigefügten offiziellen Workflows; wenn die Gewichte getrennt bereitgestellt werden, legen Sie alle drei Text-Encoder zusammen mit dem Modell ab.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
3. Für Python aktualisieren Sie Diffusers, laden StableDiffusion3Pipeline aus dem Repository stable-diffusion-3-medium-diffusers und verschieben die Pipeline auf CUDA.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
4. Prüfen Sie vor einem kommerziellen Einsatz den Umsatz der Organisation: Bei kommerzieller Nutzung ab $1M pro Jahr ist eine Enterprise-Lizenz erforderlich.
  — <https://stability.ai/license>

## Best Practices {#best-practices}

- Für reproduzierbare Ergebnisse übergeben Sie torch.Generator mit einem festen Seed; Diffusers verwendet ihn für die deterministische Latent-Sampling.
  — <https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3>
- Kombinieren Sie keine Gewichtspakete: Die Variante ohne T5XXL benötigt separate Encoder, und die FP8-Variante von T5XXL ist ein Kompromiss zwischen Qualität und Ressourcenverbrauch.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
- Vergleichen Sie für ein neues Projekt SD3 Medium mit SD 3.5: SD 3.5 wurde nach dem Eingeständnis der Mängel des ersten offenen SD3-Releases veröffentlicht.
  — <https://stability.ai/news-updates/introducing-stable-diffusion-3-5>

## Hierdurch ersetzt {#superseded-by-this}

- 2024-10-22: Die Empfehlung, neue Projekte mit SD3 Medium zu beginnen, ist für die meisten Aufgaben veraltet; Stability AI stellte SD 3.5 vor, nachdem eingeräumt wurde, dass der Juni-Release der offenen Gewichte nicht den Erwartungen entsprach.
- 2024-06-12: Der Status von SD3 als Preview/Warteliste ist nach der offenen Veröffentlichung der SD3-Medium-Gewichte veraltet.

## Weiterhin unbekannt {#still-unknown}

- Der Reddit-Short-Link zum Ereignis vom 2024-06-03 lieferte einen Internal Error; daher sind der ursprüngliche Beitrag, der Autor und die konkrete Aussage nicht verifiziert.
- In der Historie sind Stable Diffusion 3 und Stable Diffusion 3 Medium zusammengeführt. Dies ist eine Produktlinie, doch Medium ist ein konkreter 2B-Release und nicht der vollständige Satz der im Februar 2024 angekündigten Varianten.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://stability.ai/news/stable-diffusion-3 | Stable Diffusion 3 — Stability AI | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/s/xBOocPBskt | Reddit-Short-Link zum Ereignis vom 2024-06-03 | 2026-09-05 |
| https://stability.ai/news-updates/stable-diffusion-3-medium | Ankündigung der offenen Veröffentlichung von Stable Diffusion 3 Medium | 2026-09-05 |
| https://huggingface.co/stabilityai/stable-diffusion-3-medium | stabilityai/stable-diffusion-3-medium — Hugging Face | 2026-09-05 |
| https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3 | Stable-Diffusion-3-Pipeline — Diffusers-Dokumentation | 2026-09-05 |
| https://stability.ai/news-updates/introducing-stable-diffusion-3-5 | Einführung von Stable Diffusion 3.5 — Stability AI | 2026-09-05 |
| https://stability.ai/license | Stability-AI-Lizenz | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Thema:** `project:stable-diffusion-3`, Thread `stable-diffusion-3`, 1 datiertes Ereignis 2024-02-22 → 2024-02-22.
- **Praktischer Hinweis:** Ab 2024-02-22 sollten Praktiker Stable Diffusion 3 als offiziell angekündigtes Projekt behandeln und die offiziellen News- und Projektseiten für verifizierte Updates verfolgen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
