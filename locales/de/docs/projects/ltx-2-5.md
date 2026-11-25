---
title: "LTX-2.5 — LTX Video"
category: projects
date: 2026-08-11
tags: [ltx-2-5, ltx-video, project]
aliases: ["LTX-2.5"]
level: 3
source_sha256: 0e46f32e9ae83c764df19afae2ec9ac426d0902ae6ab15ea4dbc81415edba868
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.5 — LTX Video {#ltx-25-ltx-video}

**Entwicklungslinie:** `project:ltx-2-5` · Thread `ltx-video`  
**Letztes Ereignis:** 2026-08-11 · 1 datierter Eintrag seit 2026-08-11 · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

LTX-2.5 ist die 22B-Audio-Video-Modellfamilie von Lightricks für lokale ComfyUI- und Python-Setups oder gehostete Generierung.

- Synchronisierte Video- und Audiogenerierung aus Text-, Bild-, Video- und Audio-Conditioning.
- Lokale Tools für Video-to-Video, LoRA/IC-LoRA, HDR und Fine-Tuning-Pfade.
- Gehosteter API-Zugriff über `ltx-2-5-fast` und `ltx-2-5-pro` ohne Retake, Extend oder Reframe.

Der technische Leitfaden für den lokalen Betrieb verlangt eine NVIDIA-GPU mit mindestens 32 GB VRAM, 32 GB RAM, 100 GB freien Speicher, CUDA 12.7+ und Python 3.12+. Die Produktseite nennt davon getrennt ein Minimum von 16 GB. LTX-2.5 eignet sich, wenn synchronisierter Ton, Self-Hosting oder lokale Anpassung wichtig sind. Für einen gehosteten Workflow mit Retake, Extend oder Reframe bleibt LTX-2.3 die bessere Wahl.

## Entwicklungslinie {#development-line}

- **2026-08-11 — Offizielle Modell- und Anwendungslinks zu LTX-2.5 wurden geteilt.** Am 2026-08-11 verwies ein datierter Eintrag im LTX-Video-Thread auf die offizielle LTX-2.5-Modellseite und die LTX-Anwendung. Das markiert ein bestimmtes LTX-2.5-Modell und dessen offiziellen Zugangsweg. Die verfügbaren Belege klären nicht, ob es sich um einen Launch, ein Update oder eine Änderung der Verfügbarkeit handelt.

## Was sich geändert hat {#what-changed}

- 2026-08-10 — `ltx-2-5-fast` erhielt automatische Dauer für Text-to-Video und Image-to-Video, noch vor dem benannten Release.
- 2026-08-11 — LTX führte gehostete Fast- und Pro-Varianten für Text-, Image- und Audio-to-Video ein; LTX-2 v1.2.0 ergänzte die lokale 2.5-Runtime und Trainingsunterstützung.
- 2026-08-12 — ComfyUI ergänzte LTX-2.5-Templates zum Day-0-Start sowie sowohl lokale Gewichtsrouten als auch gehostete Partner-Node-Routen.
- 2026-08-16 — Die älteren API-IDs `ltx-2-fast` und `ltx-2-pro` wurden entfernt, wodurch die Migration auf 2.3 oder 2.5 verpflichtend wurde.
- 2026-08-18 — Audio-to-Video erhielt die Auflösungsstufen Fast 4K und Pro 1080p.
- 2026-08-19 — Audio-to-Video erhielt Steuerungen für Bildrate, letztes Frame und Kamerabewegung.
- 2026-08-25 — LTX-2 v1.3.0 änderte lokales DFR mit gekacheltem 4K, Multi-GPU-Ausführung, keyframe-bewusster Dekodierung und neuen DFR-Flags.
- 2026-09-02 — `ltx-2-5-pro` wurde für Text-, Image- und Audio-to-Video auf 1440p/4K und 48 fps erweitert.

## So verwendest du es {#how-to-use-this}

1. Wähle zuerst die Oberfläche. Nutze `ltx-2-5-fast` für Geschwindigkeit und niedrigere Kosten oder `ltx-2-5-pro` für höhere Qualität bei gehosteten Text-to-Video-, Image-to-Video- oder Audio-to-Video-Routen. Verwende einen lokalen Pfad, wenn du Self-Hosting oder Anpassung brauchst.
  — <https://docs.ltx.io/models/ltx-2-5>
2. Übergib für eine gehostete Image-to-Video-Anfrage `duration: null` nur, wenn das Endframe nicht fixiert ist. Automatische Dauer lässt sich nicht mit `last_frame_uri` kombinieren.
  — <https://docs.ltx.io/models/ltx-2-5>
3. Für den visuellen lokalen Pfad installierst du `ComfyUI-LTXVideo`, wählst ein LTX-2.5-Template, lädst die aufgeführten passenden Dateien herunter, ergänzt einen Prompt oder Referenzen und stellst den Job in die Warteschlange.
  — <https://docs.ltx.io/open-source-model/getting-started/quick-start>
4. Für Code oder Automatisierung klonst du LTX-2, führst `uv sync` aus, verschaffst dir Zugriff auf das Modell-Repository, lädst die aufgeteilten Komponenten herunter und übergibst jeden Komponentenpfad an `ltx-pipelines`.
  — <https://docs.ltx.io/open-source-model/integration-tools/pytorch-api>
5. Für lokale Generierung müssen Breite und Höhe durch 32 teilbar sein. Verwende eine Frame-Anzahl der Form `8n + 1` oder lasse die Frame-Anzahl weg, damit der Duration-Head von LTX-2.5 sie wählt.
  — <https://docs.ltx.io/open-source-model/integration-tools/pytorch-api>

## Best Practices {#best-practices}

- Halte die Checkpoint-Komponenten zueinander passend, insbesondere den LTX-spezifisch feinabgestimmten Gemma-4-Text-Encoder. Ersetze ihn nicht durch das Standard-Gemma-4 von Google.
  — <https://github.com/Lightricks/LTX-2/blob/main/packages/ltx-trainer/docs/configuration-reference.md>
- Starte das ComfyUI-Text-to-Video-Template mit 768x512, 97 Frames und 24 fps. Erhöhe Länge oder Auflösung erst, wenn die Hardware die Basiskonfiguration bewältigt, und fixiere den Seed, wenn du Reproduzierbarkeit brauchst.
  — <https://docs.ltx.io/open-source-model/usage-guides/text-to-video>
- Formuliere Prompts als chronologische Szene. Benenne Einstellung, Szene, Handlung, Figur, Kamerabewegung und Audio. Schreibe Prompts aus anderen Videomodellen um, statt deren Tags oder Shot-List-Syntax unverändert zu übernehmen.
  — <https://docs.ltx.io/open-source-model/usage-guides/prompting-guide>
- Verwende für native Multi-Shot-Arbeit einen chronologischen Absatz. Benenne jeden Schnitt explizit, wiederhole wiederkehrende Kennungen und die Audiokontinuität und bevorzuge zwei bis vier Shots pro Generierung.
  — <https://docs.ltx.io/open-source-model/usage-guides/prompting-guide>
- Nutze die native Zwei-Stufen-Pipeline für lokale Produktion. Verwende die destillierte Pipeline für Geschwindigkeit oder Batch-Läufe.
  — <https://docs.ltx.io/open-source-model/integration-tools/pytorch-api>
- Plane lokale Arbeit anhand der technischen Basis: 32 GB+ NVIDIA-VRAM, 32 GB RAM, 100 GB Speicher, CUDA 12.7+ und Python 3.12+. Validiere den tatsächlichen Workflow auf der Zielhardware.
  — <https://docs.ltx.io/open-source-model/getting-started/system-requirements>

## Dadurch überholt {#superseded-by-this}

- 2026-08-16 — Die API-Modell-IDs `ltx-2-fast` und `ltx-2-pro` bleiben gültig. Quelle: https://docs.ltx.io/api-changelog/2026/8/16
- 2026-08-18 — Audio-to-Video auf `ltx-2-5-fast` ist auf 1080p begrenzt. Quelle: https://docs.ltx.io/api-changelog/2026/8/18
- 2026-08-19 — Audio-to-Video kann keine Bildrate, Kamerabewegung oder letztes Frame festlegen. Quelle: https://docs.ltx.io/api-changelog/2026/8/19
- 2026-09-02 — LTX-2.5 Pro ist auf 720p/1080p begrenzt. Quelle: https://docs.ltx.io/api-changelog/2026/9/2
- 2026-08-25 — DFR verwendet `--checkpoint-path`, `--distilled-lora` und `--temporal-upsample-rounds`. Quelle: https://github.com/Lightricks/LTX-2/blob/main/CHANGELOG.md

## Weiterhin ungeklärt {#still-unknown}

- Ein zweiter, ungeklärter LTX-2.5-Eintrag mit Datum 2026-08-12 nutzt den vorläufigen Schlüssel `ltx_2_5` und abweichende Hugging-Face-URLs. Er könnte eher ein nachgelagertes Artefakt als diesen Basis-Release betreffen. Führe seine Historie nicht zusammen, ohne eine geprüfte, exakte Identität.
- Die gehosteten API-Namen `fast`/`pro` und die lokalen Checkpoint-Namen `dev`/`distilled` sind getrennte, dokumentierte Oberflächen. Keine hier gefundene Primärquelle legt eine eindeutige Zuordnung zwischen ihnen fest.
- Primärquellen widersprechen sich beim lokalen VRAM: Die Produktseite nennt 16 GB als Minimum, die technische Seite zu den Systemanforderungen 32 GB+. Eine Klärung wurde nicht gefunden; für die praktische Basis wird der höhere Wert verwendet.
- Die angegebene URL der gehosteten Anwendung lieferte in dieser Recherche keine lesbare Dokumentation. Aktuelle UI-Steuerelemente, Kontoablauf und Preise wurden nicht unabhängig überprüft.
- Die Suche in vereinfachtem Chinesisch lieferte Community-Seiten, aber keine verifizierte, datierte und reproduzierbare Praxisquelle zu LTX-2.5. Es ist keine chinesischsprachige Parameterangabe enthalten.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://ltx.io/model/ltx-2-5 | LTX-2.5: LTX's Latest AI Open-Source Foundation Model | LTX | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/10 | 10. August 2026 | LTX-Dokumentation | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/11 | 11. August 2026 | LTX-Dokumentation | 2026-09-07 |
| https://github.com/Lightricks/LTX-2/releases/tag/v1.2.0 | Release v1.2.0 · Lightricks/LTX-2 · GitHub | 2026-09-07 |
| https://blog.comfy.org/p/ltx-25-day-0-support-in-comfyui | LTX-2.5 Day-0 Support in ComfyUI | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/16 | 16. August 2026 | LTX-Dokumentation | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/18 | 18. August 2026 | LTX-Dokumentation | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/8/19 | 19. August 2026 | LTX-Dokumentation | 2026-09-07 |
| https://github.com/Lightricks/LTX-2/blob/main/CHANGELOG.md | LTX-2/CHANGELOG.md at main · Lightricks/LTX-2 · GitHub | 2026-09-07 |
| https://docs.ltx.io/api-changelog/2026/9/2 | 2. September 2026 | LTX-Dokumentation | 2026-09-07 |
| https://docs.ltx.io/models/ltx-2-5 | LTX-2.5 | LTX-Dokumentation | 2026-09-07 |
| https://huggingface.co/Lightricks/LTX-2.5 | Lightricks/LTX-2.5 · Hugging Face | 2026-09-07 |
| https://docs.ltx.io/open-source-model/getting-started/quick-start | Quick Start | LTX-Dokumentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/usage-guides/text-to-video | Text-to-Video Workflow for Beginners | LTX-Dokumentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/integration-tools/pytorch-api | PyTorch API | LTX-Dokumentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/getting-started/system-requirements | System Requirements | LTX-Dokumentation | 2026-09-07 |
| https://docs.ltx.io/open-source-model/usage-guides/prompting-guide | Prompting Guide | LTX-Dokumentation | 2026-09-07 |
| https://github.com/Lightricks/LTX-2/blob/main/packages/ltx-trainer/docs/configuration-reference.md | LTX-2 trainer configuration reference · Lightricks/LTX-2 · GitHub | 2026-09-07 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:ltx-2-5`, Thread `ltx-video`, 1 datierter Eintrag 2026-08-11 → 2026-08-11.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Überholungshinweise sind maßgeblich dafür, was veraltet ist.
