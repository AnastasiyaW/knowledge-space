---
title: "ControlNet für SDXL — SDXL-ControlNet-Modellveröffentlichungen"
category: projects
date: 2023-08-14
tags: [controlnet-sdxl, controlnet_sdxl, project, sdxl-controlnet-model-releases]
aliases: ["ControlNet Depth for SDXL", "ControlNet OpenPose for SDXL", "ControlNet for SDXL"]
level: 2
source_sha256: 041923eb31f3a46ff3a079f89c0c69bb63dac9f5586b63dbcd57ceeb4d1073b7
translation: machine
translated_at: '2026-10-24'
---
# ControlNet für SDXL — SDXL-ControlNet-Modellveröffentlichungen {#controlnet-for-sdxl-sdxl-controlnet-model-releases}

**Entwicklungslinie:** `project:controlnet-sdxl` · Thread `sdxl-controlnet-model-releases`  
**Letztes Ereignis:** 2023-08-14 · 3 datierte Einträge seit 2023-08-10 · **Recherchiert:** noch nicht · Konfidenz: nicht recherchiert

## Was es ist {#what-it-is}

ControlNet für SDXL passt Conditioning-Modelle an SDXL an. Wir haben noch keine Recherche zum aktuellen Stand durchgeführt; diese Seite enthält daher nur die datierte Angabe und den nachstehenden praktischen Hinweis, nicht mehr.

## Entwicklungslinie {#development-line}

- **2023-08-10 — Diffusers veröffentlichte ein SDXL-ControlNet-Beispiel und ein Modell.** Am 2023-08-10 verlinkte Hugging Face Diffusers ein SDXL-spezifisches ControlNet-Beispiel sowie das Modell-Repository diffusers/controlnet-sdxl-1.0. Dies war ein öffentlicher Entwicklungsschritt, um ControlNet-Workflows an SDXL anzupassen. Der begleitende Reddit-Link ist ergänzender Kontext und kein eigenständiges Ereignis.
- **2023-08-14 — Ein OpenPose-ControlNet-Modell für SDXL wurde verlinkt.** Am 2023-08-14 wurde das Modell-Repository thibaud/controlnet-openpose-sdxl-1.0 verlinkt. Es bietet eine SDXL-ControlNet-Option für die Posensteuerung mit OpenPose und erweitert den verfügbaren Satz an SDXL-ControlNet-Modellen.
- **2023-08-14 — Ein Depth-ControlNet-Modell für SDXL wurde verlinkt.** Am 2023-08-14 wurde das Modell-Repository diffusers/controlnet-depth-sdxl-1.0 verlinkt. Es ergänzt einen SDXL-ControlNet-Checkpoint für Tiefen-Conditioning und stellt damit neben dem OpenPose-Modell eine eigenständige Steuerungsmodalität bereit.

## Anwendung {#how-to-use-this}

Stand 2023-08-14: Wähle SDXL-spezifische ControlNet-Checkpoints nach dem Steuersignal aus, statt anzunehmen, dass ein früherer ControlNet-Checkpoint zu SDXL passt. Verwende OpenPose für Posensteuerung und Depth für Tiefensteuerung.

## Ersetzt durch {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

Den aktuellen Stand haben wir nicht recherchiert. Die datierte Entwicklungslinie oben ist noch nicht gegen Primärquellen geprüft.

## Quellen {#sources}

| source |
|---|
| https://github.com/huggingface/diffusers/blob/main/examples/controlnet/README_sdxl.md |
| https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0 |
| https://huggingface.co/diffusers/controlnet-sdxl-1.0 |
| https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0 |
| https://www.reddit.com/r/StableDiffusion/comments/15n6lso/comment/jvki53u/ |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:controlnet-sdxl`, Thread `sdxl-controlnet-model-releases`, 3 datierte Ereignisse 2023-08-10 → 2023-08-14.
- **Praktischer Hinweis:** Stand 2023-08-14 konnten Anwender SDXL-spezifische ControlNet-Checkpoints nach Steuersignal auswählen, etwa OpenPose für Posensteuerung und Depth für Tiefensteuerung, statt anzunehmen, dass ein früherer ControlNet-Checkpoint für SDXL geeignet sei.
- **Konfidenz:** nicht recherchiert. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
