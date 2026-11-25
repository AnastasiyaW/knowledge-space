---
title: "Wan Video"
category: projects
date: 2025-09-01
tags: [project, wan-video, wan-video-development, wan_video]
aliases: ["Wan 2.2", "Wan Video"]
level: 2
source_sha256: 839278044f2b89af3a796d607088173f82d36c9a03a47c669ec8ee9b7fe91fe8
translation: machine
translated_at: '2026-10-24'
---
# Wan Video {#wan-video}

**Entwicklungslinie:** `project:wan-video` · Thread `wan-video-development`  
**Letztes Ereignis:** 2025-09-01 · 2 datierte seit 2025-04-23 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Wan Video ist Alibabas offene Modellfamilie für Videogenerierung und Videotransformation.

- T2V: erzeugt Videos aus Text-Prompts.
- I2V: belebt Standbilder zu Videos.
- TI2V: erzeugt Videos aus kombinierten Text- und Bildeingaben.
- Speech-to-Video: erzeugt Videos, die durch Sprachaudio gesteuert werden.
- Figurenanimation und Figurenersetzung: animiert menschliche Figuren und tauscht Charaktere über Videos hinweg aus.

TI2V-5B läuft mit 720p auf einer GPU mit 24 GB VRAM; A14B-Modelle benötigen im Single-GPU-Modus mindestens 80 GB VRAM. Dies ist ein praktikabler lokaler Stack für kontrollierte Videogenerierung, bei dem Modellgewichte und VRAM den Laufzeitpfad bestimmen.

## Entwicklungslinie {#development-line}

- **2025-04-23 — Wan Video eröffnete einen öffentlichen Workflow zur Videoerstellung.** Am 2025-04-23 verwies eine offizielle wan.video-Seite auf eine Oberfläche zur Videoerstellung. Die Seite allein zeigt nicht, ob dies einen neuen Start, ein Update oder ein bereits bestehendes Werkzeug markiert.
- **2025-09-01 — Wan 2.2 erhielt einen Kamera-LoRA für Orbit-Aufnahmen.** Am 2025-09-01 veröffentlichte ein Hugging-Face-Repository ein Wan-2.2-I2V-14B-LoRA für Orbit-Kamerabewegungen. Das Repository klärt weder den offiziellen Status noch die Kompatibilität mit getesteten Umgebungen.

## Was sich geändert hat {#what-changed}

Am 2025-04-23 führte die URL zur Wan-Weboberfläche. Die aktuelle Adresse leitet direkt zum Generator weiter, doch das Quellmaterial verknüpft dieses Datum nicht mit einer eigenständigen Modellveröffentlichung. Am 2025-09-01 erschien ein Community-LoRA für Orbit-Kamerabewegungen auf Wan2.2-I2V-A14B. Der Commit-Verlauf des Repositorys zeigt, dass die Dateien bereits am 2025-08-20 hinzugefügt wurden; der 1. September ist daher nicht das Veröffentlichungsdatum des Adapters.

## Anwendung {#how-to-use-this}

Ab 2025-04-23 können Praktiker Wan Video als öffentlichen Workflow zur Videoerstellung betrachten. Ab 2025-09-01 können sie ein spezialisiertes Wan-2.2-I2V-14B-LoRA für Orbit-Aufnahmen evaluieren, wenn Orbit-Kamerabewegungen benötigt werden, nachdem die Kompatibilität geprüft wurde.

1. Wähle TI2V-5B für ein einzelnes 720p-Modell, das T2V und I2V auf einer GPU mit 24 GB VRAM abdeckt; lade den Checkpoint herunter und führe `generate.py` mit `--task ti2v-5B` aus.
  — <https://github.com/Wan-Video/Wan2.2>
2. Verwende Wan2.2-I2V-A14B für 480p- oder 720p-I2V mit Eingabebild und Prompt; die Zielauflösung legt die Pixelfläche fest, während das Seitenverhältnis aus dem Eingabebild stammt.
  — <https://github.com/Wan-Video/Wan2.2>
3. Lade beide Adapter in Diffusers auf Basis von `Wan-AI/Wan2.2-I2V-A14B`, um die Kameraorbitierung zu steuern, und hänge sie anschließend an die I2V-Pipeline an.
  — <https://huggingface.co/ostris/wan22_i2v_14b_orbit_shot_lora>
4. Übergib für Figurenanimation ein Referenzbild sowie extrahierte Pose- und Gesichtsmerkmale an Diffusers; Rohvideo ist keine gültige Pipeline-Eingabe.
  — <https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan>

## Best Practices {#best-practices}

- Beginne mit TI2V-5B, wenn nur eine Consumer-GPU zur Verfügung steht; für A14B sind mindestens 80 GB VRAM oder ein verteilter Cluster einzuplanen.
  — <https://github.com/Wan-Video/Wan2.2>
- Aktiviere `--offload_model True`, `--convert_model_dtype` und `--t5_cpu` bei OOM-Fehlern, um Ausführungsgeschwindigkeit gegen geringeren Speicherbedarf einzutauschen.
  — <https://github.com/Wan-Video/Wan2.2>
- Wähle die Prompt-Erweiterung bewusst: Lokales Qwen vermeidet externe Aufrufe, während DashScope einen API-Schlüssel und eine entfernte Abhängigkeit erfordert.
  — <https://github.com/Wan-Video/Wan2.2>
- Extrahiere Pose-Keypoints und Gesichtsmerkmale mit den Standard-Vorverarbeitungsskripten für Wan-Animate; übergib niemals Rohvideodateien direkt.
  — <https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan>

## Abgelöst durch {#superseded-by-this}

- 2025-07-28: Wan2.2 ersetzte Wan2.1 als primäre offene Basis für neue T2V-, I2V- und TI2V-Aufgaben; Wan2.1 wird weiterhin für VACE und FLF2V gepflegt.
- 2025-09-19: Wan2.2-Animate-14B ersetzte externe Pipelines als offiziellen Wan-Weg für Animation und Figurenersetzung.

## Weiterhin unbekannt {#still-unknown}

- Die Primärquelle erklärt nicht, was sich am 2025-04-23 in der Weboberfläche geändert hat.
- Der Orbit-Shot-LoRA ist ein Drittanbieter-Adapter und keine offizielle Wan-Veröffentlichung; seine Model Card führt trotz der Ausrichtung auf Wan2.2 I2V den Eintrag Text-to-Image auf.
- Testprotokolle bestätigen die genaue Kompatibilität der beiden LoRA-Dateien mit bestimmten Diffusers- oder UI-Wrapper-Versionen nicht.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://wan.video/wanxiang/videoCreation | Wan AI: Führendes KI-Modell zur Videogenerierung | 2026-09-05 |
| https://huggingface.co/ostris/wan22_i2v_14b_orbit_shot_lora | ostris/wan22_i2v_14b_orbit_shot_lora | 2026-09-05 |
| https://huggingface.co/ostris/wan22_i2v_14b_orbit_shot_lora/commits/main | Commit-Verlauf für wan22_i2v_14b_orbit_shot_lora | 2026-09-05 |
| https://github.com/Wan-Video/Wan2.1 | Wan2.1 | 2026-09-05 |
| https://github.com/Wan-Video/Wan2.2 | Wan2.2 | 2026-09-05 |
| https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan | Wan-Pipelines — Diffusers-Dokumentation | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:wan-video`, Thread `wan-video-development`, 2 datierte Ereignisse 2025-04-23 → 2025-09-01.
- **Praktischer Hinweis:** Ab 2025-04-23 können Praktiker Wan Video als öffentlichen Workflow zur Videoerstellung betrachten; ab 2025-09-01 können sie ein spezialisiertes Wan-2.2-I2V-14B-LoRA für Orbit-Aufnahmen evaluieren, wenn Orbit-Kamerabewegungen benötigt werden, nachdem die Kompatibilität geprüft wurde.
- **Konfidenz:** hoch. Die datierten „Abgelöst durch“-Einträge sind maßgeblich für das, was veraltet ist.
