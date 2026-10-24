---
title: "PiD — Forschungsveröffentlichung"
category: projects
date: 2026-05-25
tags: [pid, project, research-release]
aliases: ["PiD"]
level: 2
source_sha256: 8612bd230e9b3a84e5c191ac530299757f5c5382a3d155f4a22af63874042745
translation: machine
translated_at: '2026-10-24'
---
# PiD — Forschungsveröffentlichung {#pid-research-release}

**Entwicklungslinie:** `project:pid` · Strang `research-release`  
**Letztes Ereignis:** 2026-05-25 · 1 datiertes Ereignis seit 2026-05-25 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

PiD ist ein Pixel-Diffusion-Decoder für generative Bildpipelines, der Standard-VAE- und RAE-Decoder ersetzt.

- Latent-Decoding: Dekodiert Latents zu Pixeln mit gleichzeitiger 4×-Hochskalierung bzw. 8×-Hochskalierung für Scale-RAE.
- Latent-Unterstützung: Funktioniert mit konventionellen VAE-Latents und semantischen Latents, einschließlich DINOv2 und SigLIP.
- Schnelle Inferenz: Destillierte Checkpoints dekodieren in vier Schritten.

NSCLv1-Gewichte sind auf nicht-kommerzielle Forschung oder Evaluierung beschränkt.
Verwenden Sie PiD, wenn Sie kontrolliertes Latent-zu-2K/4K-Decoding auf einem unterstützten Backbone benötigen, statt eines separaten Pixel-Upscalers nach dem VAE.

## Entwicklungslinie {#development-line}

- **2026-05-25 — Forschung, Code und Modellressourcen zu PiD wurden öffentlich verfügbar gemacht.** Am 2026-05-25 wurde PiD mit verlinkter Forschungsarbeit, Quellcode und Hugging-Face-Modellressourcen veröffentlicht. Diese Links etablieren öffentliche technische Einstiegspunkte für das Projekt, allerdings legt die Veröffentlichungsevidenz keine genaue Version und keine vollständigen Fähigkeiten fest.

## Was sich geändert hat {#what-changed}

- 2026-05-25 — Veröffentlichung von Paper, Quellcode und PiD-Gewichten für FLUX, FLUX.2, Z-Image, Z-Image-Turbo, SD3, DINOv2 und SigLIP.
- 2026-05-27 — PiD-Unterstützung für ComfyUI hinzugefügt.
- 2026-06-02 — Checkpoints für SDXL, Qwen-Image und Qwen-Image-2512 veröffentlicht; Codebasis bereinigt und torch.compile-Unterstützung aktiviert.
- 2026-07-09 — Trainingscode, destillierte und nicht-destillierte PiD v1.5 2K→4K sowie v1.5-Checkpoints für FLUX, Z-Image, Z-Image-Turbo, FLUX.2 und Qwen-Image veröffentlicht.
- 2026-07-14 — Optionale Unterstützung für native Boogu-Image-Generierung und PiD-Decoding von dessen Flux-artigen VAE-Latents hinzugefügt.

## Wie Sie das nutzen {#how-to-use-this}

Ab 2026-05-25 sollten Praktiker die Forschungsseite, das Quell-Repository und die Hugging-Face-Modellseite von PiD als seine datierten öffentlichen technischen Einstiegspunkte betrachten.

1. Klonen Sie das Repository, erstellen Sie eine Python-3.12/CUDA-Umgebung mit `uv sync --frozen` oder installieren Sie die Abhängigkeiten, und führen Sie anschließend `PYTHONPATH=. python verify_env.py` aus.
  — <https://github.com/nv-tlabs/PiD>
2. Laden Sie nur den Checkpoints-Baum herunter: `hf download nvidia/PiD --local-dir . --include "checkpoints/*"`.
  — <https://github.com/nv-tlabs/PiD>
3. Verwenden Sie `from_ldm` mit `--backbone` für Prompt-zu-Bild-Generierung; verwenden Sie `from_clean`, um ein vorhandenes Bild zu kodieren und mit PiD zu dekodieren.
  — <https://github.com/nv-tlabs/PiD>
4. Wählen Sie `--pid_ckpt_type 2k` für 2K-Ausgabe; wählen Sie `2kto4k_v1pt5` für unterstützte 4K-Modelle oder `2kto4k` für SD3 und SDXL.
  — <https://github.com/nv-tlabs/PiD>

## Bewährte Vorgehensweisen {#best-practices}

- Prüfen Sie die Umgebung mit `verify_env.py`, bevor Sie Inferenz ausführen, und führen Sie Befehle aus dem Repository-Stammverzeichnis mit `PYTHONPATH=.` aus.
  — <https://github.com/nv-tlabs/PiD>
- Verwechseln Sie VAE-Dateien nicht mit PiD-Modellen: `PiD_*`-Dateien sind destillierte Decoder-Checkpoints, während `ae.safetensors`, VAE/RAE und ähnliche Dateien abhängige Encoder und Decoder sind.
  — <https://huggingface.co/nvidia/PiD>
- Wählen Sie v1.5 2K→4K für FLUX, FLUX.2 und Qwen-Image, um Farb- und Eckengitter-Artefakte zu beheben; der 2K-Checkpoint bleibt bei genau 2048 px schärfer.
  — <https://github.com/nv-tlabs/PiD>
- Prüfen Sie die Lizenz vor dem Deployment: Veröffentlichte Gewichte sind auf nicht-kommerzielle Forschung oder Evaluierung beschränkt.
  — <https://huggingface.co/nvidia/PiD>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-07-09 — Frühere `2kto4k`-Checkpoints für FLUX, FLUX.2 und Qwen-Image sind zugunsten von `2kto4k_v1pt5` veraltet; ältere Gewichte wurden nach `checkpoints_deprecated/` verschoben.
- 2026-07-09 — Der Hinweis, für neue 4K-Dekodierungen mit FLUX, FLUX.2 und Qwen-Image v1 `2kto4k` zu verwenden, ist überholt; v1 `2kto4k` bleibt für SD3 und SDXL aktuell.

## Weiterhin unbekannt {#still-unknown}

- Die ursprüngliche README nennt Daten für spätere Aktualisierungen, aber GitHub veröffentlicht keine separaten versionierten Releases; genaue Commit-SHAs und Zeitstempel sind nicht festgestellt.
- Geschwindigkeits- und Qualitätsangaben stammen aus den eigenen Benchmarks der Autoren; eine unabhängige, reproduzierbare Evaluierung auf einem bestimmten Workflow wurde hier nicht durchgeführt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://research.nvidia.com/labs/sil/projects/pid/ | PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion | 2026-09-05 |
| https://github.com/nv-tlabs/PiD | nv-tlabs/PiD — PiD: Pixel Diffusion Decoder | 2026-09-05 |
| https://huggingface.co/nvidia/PiD | Modell-Repository nvidia/PiD | 2026-09-05 |
| https://arxiv.org/abs/2605.23902 | PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:pid`, Strang `research-release`, 1 datiertes Ereignis 2026-05-25 → 2026-05-25.
- **Praktischer Hinweis:** Ab 2026-05-25 sollten Praktiker die Forschungsseite, das Quell-Repository und die Hugging-Face-Modellseite von PiD als seine datierten öffentlichen technischen Einstiegspunkte betrachten.
- **Konfidenz:** hoch. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
