---
title: "Sun Direction LoRA Flux 2 Klein 9B — Flux 2 Klein LoRAs"
category: projects
date: 2026-07-03
tags: [flux2-klein-loras, project, sun-direction-lora-flux2-klein-9b]
aliases: ["Sun Direction LoRA Flux 2 Klein 9B"]
level: 2
source_sha256: 8c420eb60d9d31d8d379c84b6f4f1b4c755df0b838587955d776ae08338c0bce
translation: machine
translated_at: '2026-10-24'
---
# Sun Direction LoRA Flux 2 Klein 9B — Flux 2 Klein LoRAs {#sun-direction-lora-flux-2-klein-9b-flux-2-klein-loras}

**Entwicklungslinie:** `project:sun-direction-lora-flux2-klein-9b` · Thread `flux2-klein-loras`  
**Letztes Ereignis:** 2026-07-03 · 1 datiertes seit 2026-07-03 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Sun Direction LoRA Flux 2 Klein 9B ist ein 331 MB großes Image-to-Image-LoRA für Nutzer von FLUX.2 [klein] 9B. Es verschiebt die scheinbare Sonnenposition in Außenaufnahmen.

- Sonnenhöhe und Rotation: legt den Winkel relativ zur Kamera fest.
- Lit-Sphere-Referenz: konditioniert die Bearbeitung auf eine gerenderte Kugel.
- Vorbereitender Overcast-Durchlauf: entfernt bestehende Schatten vor dem Neubeleuchten.

## Entwicklungslinie {#development-line}

- **2026-07-03 — Ressourcenreferenz zu Sun Direction LoRA Flux 2 Klein 9B erfasst.** Am 2026-07-03 verlinkte der Thread Flux 2 Klein LoRAs auf dessen Hugging-Face-Repository. Wir haben noch keinen Beitragstext und keine Model Card, daher machen wir keine Aussagen zu Release-Version, Trainingssetup, Lizenz oder Leistung.

## Was sich geändert hat {#what-changed}

2026-07-03 — eine lauffähige FLUX.2-[klein]-9B-Demo dokumentierte den zweistufigen Relighting-Workflow mit Sphere-Konditionierung für den v1-Adapter.

## So wird es verwendet {#how-to-use-this}

Prüfe das Hugging-Face-Repository vom 2026-07-03, bevor du es verwendest. Wir haben keine bestätigte Kompatibilität, keine bestätigten Trigger, keine bestätigte Lizenz und keine bestätigten Qualitätsaussagen.

1. Aktualisiere ComfyUI und installiere anschließend das benötigte FLUX.2-[klein]-9B-Diffusionsmodell, den 9B-Text-Encoder und das FLUX.2-VAE für einen Image-Edit-Workflow.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>
2. Lade das v1-LoRA herunter und verwende den mitgelieferten Workflow; für die Lit-Sphere-Referenz nutze entweder den Knoten Sphere Light Render oder die enthaltene Blender-Szene.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
3. Hat das Eingangsbild bereits starkes gerichtetes Licht, erzeuge zuerst eine Overcast-Version mit reduzierten Schatten; verwende dieses Bild und das Kugelbild als Latent-Referenzen für den Relight-Durchlauf.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
4. Nimm `match the sun direction from the reference` in den Prompt auf und füge danach Szenenanweisungen wie Himmelsbedingungen hinzu.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>

## Best Practices {#best-practices}

- Verwende Außenaufnahmen und behandle Ausgaben für Innenräume als nicht unterstützt, nicht als fehlerhaftes Setup.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
- Überspringe die Overcast-Vorbereitung nur, wenn dem Eingangsbild ohnehin eine klare Schattenrichtung fehlt.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
- Halte den Seed fest, wenn du einen Relighting-Timelapse rendерst, um Flackern zu reduzieren.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
- Aktualisiere ComfyUI, wenn dem mitgelieferten Workflow zentrale Knoten fehlen.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>

## Abgelöst durch dies {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Es wurden keine öffentlichen v2-Gewichte, Release Notes, Benchmarks oder Trainingsdatensätze veröffentlicht. Die v1-Card gibt nur an, dass v2 in Arbeit ist.
- Der Autor veröffentlicht weder einen validierten LoRA-Stärkebereich noch Hardwareanforderungen für diesen Adapter.
- Der Entwicklungseintrag vom 2026-07-03 ist eine am selben Tag lauffähige Demo; die v1-Gewichte und Workflows wurden im Repository bereits am 2026-06-29 committet.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B | Sun Direction LoRA Flux 2 Klein 9B v1 | 2026-09-05 |
| https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B/tree/main | Sun-Direction-Lora-Flux2Klein9B Repository-Dateien | 2026-09-05 |
| https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B/commits/main | Sun-Direction-Lora-Flux2Klein9B Commit-Verlauf | 2026-09-05 |
| https://huggingface.co/spaces/linoyts/sun-direction-flux2-klein/commit/36259bd5c170a583fac16461a64b6ebc05f2ab84 | Sun Direction LoRA Demo (FLUX.2 klein 9B) | 2026-09-05 |
| https://docs.comfy.org/tutorials/flux/flux-2-klein | ComfyUI-Leitfaden zu Flux.2 Klein | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:sun-direction-lora-flux2-klein-9b`, Thread `flux2-klein-loras`, 1 datiertes Ereignis vom 2026-07-03 → 2026-07-03.
- **Praktischer Hinweis:** Prüfe ab dem 2026-07-03 die verlinkte Hugging-Face-Ressource, bevor du sie verwendest; wir stellen keine Aussagen zu Kompatibilität, Triggern, Lizenzierung oder Qualität auf.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
