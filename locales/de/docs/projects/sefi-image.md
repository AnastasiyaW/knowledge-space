---
title: "SeFi-Image"
category: projects
date: 2026-06-26
tags: [project, sefi-image, sefi-image-development]
aliases: ["SeFi-Image"]
level: 2
source_sha256: bf8faae64e0c1fc49f36b6c746c29d59b46b6e819c96e4ef72bbc9814368a218
translation: machine
translated_at: '2026-10-24'
---
# SeFi-Image {#sefi-image}

**Entwicklungslinie:** `project:sefi-image` · Thread `sefi-image-development`  
**Letztes Ereignis:** 2026-06-26 · 1 datierter Eintrag seit 2026-06-26 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

SeFi-Image trennt semantische und texturbezogene latente Ströme, sodass die Struktur vor den Details entrauscht wird. Es werden die Modelle 1B, 2B und 5B Base, ein 5B-RL-Modell sowie die Modelle 1B/2B/5B Turbo angeboten. Base und RL verwenden 50 Schritte bei Guidance 4.0; Turbo verwendet standardmäßig vier Schritte bei Guidance 1.0. Wir betreiben es für kontrollierte lokale Forschung, nicht für kommerziellen Einsatz oder gehostete Inferenz.

## Entwicklungslinie {#development-line}

- **2026-06-26 — Offizielle Projektressourcen von SeFi-Image wurden verlinkt.** Am 2026-06-26 verlinkte eine Nachricht der Entwicklungslinie die Projektwebsite, das Quell-Repository und die Hugging-Face-Seite. Die Belege bestätigen diese Links, zeigen aber keinen konkreten Release, kein konkretes Modell und keinen technischen Meilenstein.

## Was sich geändert hat {#what-changed}

2026-06-26 — arXiv v3 beschrieb SeFi-Image als öffentliche T2I-Familie mit semantik-zuerst-Diffusion, mit den Skalen 1B, 2B und 5B sowie DMD2-destillierten Turbo-Varianten.

## So wird es genutzt {#how-to-use-this}

Stand 2026-06-26 nutzen wir die verlinkte Projektwebsite, das GitHub-Repository und die Hugging-Face-Seite, um SeFi-Image zu bewerten.

1. Akzeptieren Sie die Zugriffsbedingungen für die Checkpoints und wählen Sie dann einen Checkpoint: Base für Analyse oder Fine-Tuning, RL für auf Alignment ausgerichtete Generierung oder Turbo für schnelle Generierung.
  — <https://huggingface.co/SeFi-Image/SeFi-Image-5B-Base>
2. Installieren Sie die Laufzeitumgebung des Repositorys in Python 3.11 mit PyTorch passend zur lokalen CUDA-Version und installieren Sie anschließend Diffusers, Transformers, Accelerate, Safetensors, Hugging Face Hub, OmegaConf und Pillow.
  — <https://github.com/jmliu206/SeFi-Image>
3. Führen Sie `inference.py` mit einer Checkpoint-ID, einem Prompt, einem Ausgabeverzeichnis und einem Seed aus; verwenden Sie einen Base-Checkpoint wie `SeFi-Image/SeFi-Image-5B-Base` für den Standardpfad mit 50 Schritten.
  — <https://github.com/jmliu206/SeFi-Image>
4. Für Generierung mit niedriger Latenz wählen Sie einen Turbo-Checkpoint und setzen vier Schritte mit einer Guidance Scale von 1.0.
  — <https://github.com/jmliu206/SeFi-Image>
5. Für einen Standard-Diffusers-Workflow laden Sie einen `-diffusers`-Checkpoint mit `SeFiPipeline` oder `DiffusionPipeline` in BF16 auf CUDA.
  — <https://huggingface.co/SeFi-Image/SeFi-Image-5B-turbo-diffusers>

## Bewährte Praktiken {#best-practices}

- Belassen Sie Turbo bei 4, 8 oder 10 Entrauschungsschritten und einer Guidance Scale von 1.0; das Projekt dokumentiert vier Schritte als Standard.
  — <https://github.com/jmliu206/SeFi-Image>
- Verwenden Sie Base-Checkpoints als Ausgangspunkt für Fine-Tuning und Analyse; reservieren Sie Turbo für schnelle Generierung und RL für stärker auf Alignment ausgerichtete Ausgaben.
  — <https://huggingface.co/SeFi-Image/SeFi-Image-5B-Base>
- Behandeln Sie die veröffentlichten Gewichte als CC BY-NC 4.0, zugangsbeschränkt und nur für Forschungszwecke; wenden Sie menschliche Aufsicht, Moderation, Validierung und Compliance-Prüfungen an, bevor sie breiter eingesetzt werden.
  — <https://github.com/jmliu206/SeFi-Image>

## Durch dieses ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die Quellen enthalten kein datiertes Changelog, das die inhaltlichen Unterschiede zwischen arXiv v3, v4 und v5 beschreibt.
- Keine Quelle aus erster Hand belegt eine Option für produktives Serving; die geprüften Hugging-Face-Diffusers-Karten besagen, dass kein Inference Provider die Modelle bereitstellt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://jmliu206.github.io/sefi-web/ | SeFi-Image | Semantic-First Diffusion | 2026-09-05 |
| https://github.com/jmliu206/SeFi-Image | GitHub - jmliu206/SeFi-Image | 2026-09-05 |
| https://huggingface.co/SeFi-Image | SeFi-Image-Organisation auf Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2606.22568 | SeFi-Image: Ein Text-zu-Bild-Foundation-Modell mit Semantic-First Diffusion | 2026-09-05 |
| https://huggingface.co/SeFi-Image/SeFi-Image-5B-Base | SeFi-Image/SeFi-Image-5B-Base | 2026-09-05 |
| https://huggingface.co/SeFi-Image/SeFi-Image-5B-turbo-diffusers | SeFi-Image/SeFi-Image-5B-turbo-diffusers | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:sefi-image`, Thread `sefi-image-development`, 1 datiertes Ereignis vom 2026-06-26 bis 2026-06-26.
- **Praktischer Hinweis:** Stand 2026-06-26 die verlinkte Projektwebsite, das GitHub-Repository und die Hugging-Face-Seite als Ausgangspunkte nutzen, um SeFi-Image zu bewerten.
- **Konfidenz:** hoch. Datierte Ersetzungen weiter oben sind maßgeblich für die Frage, was veraltet ist.
