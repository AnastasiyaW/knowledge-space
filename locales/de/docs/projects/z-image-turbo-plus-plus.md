---
title: "Z-Image Turbo++ — Forschungsreferenz"
category: projects
date: 2026-06-17
tags: [project, research-reference, z-image-turbo-plus-plus, z_image]
aliases: ["Z-Image Turbo++"]
level: 2
source_sha256: a52e80d26ecd8e6ade666154458d7f6b4c87968280490eb18aa5a25b4c6c355d
translation: machine
translated_at: '2026-10-24'
---
# Z-Image Turbo++ — Forschungsreferenz {#z-image-turbo-research-reference}

**Entwicklungslinie:** `project:z-image-turbo-plus-plus` · Thread `research-reference`  
**Letztes Ereignis:** 2026-06-17 · 1 datiertes seit 2026-06-17 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Z-Image Turbo++ ist ein Forschungsmodell für Text-zu-Bild, für Teams, die zweistufige Generierung statt der achtstufigen Generierung von Z-Image Turbo prüfen. — Distribution-Aligned Adversarial Learning: verwendet Bilder des Lehrermodells als GAN-Target. — Step-Decoupled Parameterization: trennt die Parameter der beiden Denoising-Schritte. — End-to-End Training with Iterative Regularization: überträgt die finale Qualitätsbewertung auf den ersten Schritt. 2 Schritte statt 8 beim Lehrermodell; ein separater fertiger Checkpoint ist in den untersuchten Primärquellen nicht bestätigt. Fazit: Das ist ein Richtwert zur Reproduktion der Forschung; für einen produktiven Betrieb ist heute nur Z-Image-Turbo bestätigt.

## Entwicklungslinie {#development-line}

- **2026-06-17 — Verweis auf das Z-Image-Turbo++-Paper verknüpft.** Am 2026-06-17 wurde in der Entwicklungslinie von Z-Image Turbo++ eine Hugging-Face-Papers-Seite verlinkt, identifiziert als Paper 2606.12575. Der datierte Link begründet eine Forschungsreferenz für das Projekt, belegt aber weder Titel, technische Aussagen noch Veröffentlichungsstatus des Papers. Dieser Verlaufseintrag dokumentiert die Referenz selbst und keine ungeprüften Fähigkeiten.

## Was sich geändert hat {#what-changed}

2026-06-17 — Z-Image Turbo++ wird als zweistufige Destillation von Z-Image Turbo mit acht Schritten beschrieben; der Unterschied liegt in der Schrittzahl, nicht in einem bestätigten separaten Gewichte-Release.

## Verwendung {#how-to-use-this}

Ab dem 2026-06-17 sollten Praktiker die verlinkte Hugging-Face-Papers-Seite als Forschungsreferenz zur Untersuchung behandeln, nicht als Beleg für ungeprüfte technische Aussagen oder einen Produktrelease.

1. Für die Forschungsreproduktion zwei unabhängige Denoising-Schritte implementieren, sie an Bildern des achtstufigen Lehrermodells trainieren und den Hilfs-Loss des ersten Schritts beibehalten.
  — <https://arxiv.org/abs/2606.12575>
2. Für die praktische Generierung den Lauf nicht als Turbo++ kennzeichnen, sondern das separat veröffentlichte achtstufige Tongyi-MAI/Z-Image-Turbo verwenden.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>
3. Für Z-Image-Turbo die ZImagePipeline in bfloat16 auf CUDA laden, num_inference_steps=9 setzen, was 8 DiT-Durchläufe ergibt, und guidance_scale=0.0 setzen.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>

## Bewährte Praktiken {#best-practices}

- Ergebnisse von Turbo++ und Z-Image-Turbo in Experimenten getrennt halten: Das Paper definiert Turbo++ als 2-step, die offizielle Modellkarte von Turbo als 8-step.
  — <https://arxiv.org/abs/2606.12575>
- Bei dem veröffentlichten Turbo guidance_scale nicht erhöhen: Die Modellkarte legt 0.0 fest.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>
- bfloat16 auf einer unterstützten GPU verwenden; CPU-Offload nur bei Speichermangel aktivieren und dabei einen langsameren Lauf in Kauf nehmen.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>

## Durch dies ersetzt {#superseded-by-this}

- 2026-06-10 — die Forschungsbeschränkung der Z-Image-Linie auf den Bereich von 4–8 Schritten: Die Arbeit zeigt eine zweistufige Destillation.

## Weiterhin ungeklärt {#still-unknown}

- Eigene offizielle Gewichte, Code, Modellkarte oder eine kompatible Laufzeitumgebung für Turbo++ sind in den untersuchten Primärquellen nicht bestätigt; dass sie auf den geprüften Seiten fehlen, beweist nicht, dass es sie nicht gibt.
- Das Abstract von Turbo++ enthält keine numerischen Tabellen zu Qualität oder Geschwindigkeit; für eine Einführungsentscheidung ist ein reproduzierbarer Benchmark mit denselben Prompts und derselben Hardware nötig.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/papers/2606.12575 | Paper-Seite - High-Fidelity Two-Step Image Generation via Teacher-Aligned End-to-End Distillation | 2026-09-05 |
| https://arxiv.org/abs/2606.12575 | High-Fidelity Two-Step Image Generation via Teacher-Aligned End-to-End Distillation | 2026-09-05 |
| https://arxiv.org/abs/2511.22699 | Z-Image: An Efficient Image Generation Foundation Model with Single-Stream Diffusion Transformer | 2026-09-05 |
| https://huggingface.co/Tongyi-MAI/Z-Image-Turbo | Tongyi-MAI/Z-Image-Turbo | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:z-image-turbo-plus-plus`, Thread `research-reference`, 1 datiertes Ereignis 2026-06-17 → 2026-06-17.
- **Praktischer Hinweis:** Ab dem 2026-06-17 sollten Praktiker die verlinkte Hugging-Face-Papers-Seite als Forschungsreferenz zur Untersuchung behandeln, nicht als Beleg für ungeprüfte technische Aussagen oder einen Produktrelease.
- **Konfidenz:** mittel. Die oben genannten datierten Ersetzungen sind maßgeblich dafür, was veraltet ist.
