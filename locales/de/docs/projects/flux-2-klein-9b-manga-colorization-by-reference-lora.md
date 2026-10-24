---
title: "FLUX.2 Klein 9B Manga-Kolorierungs-LoRA — Manga-Kolorierung per Referenz-LoRA"
category: projects
date: 2026-06-10
tags: [flux-2-klein-9b-manga-colorization-by-reference-lora, flux-lora, manga-colorization-by-reference-lora, project]
aliases: ["FLUX.2 Klein 9B Manga Colorization LoRA"]
level: 2
source_sha256: 1ce3f35c1e27dc6e59c8e9423cbb09842c1ae4ec469f88b3d09c4a9b97350e96
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 Klein 9B Manga-Kolorierungs-LoRA — Manga-Kolorierung per Referenz-LoRA {#flux2-klein-9b-manga-colorization-lora-manga-colorization-by-reference-lora}

**Entwicklungslinie:** `project:flux-2-klein-9b-manga-colorization-by-reference-lora` · Thread `manga-colorization-by-reference-lora`  
**Letztes Ereignis:** 2026-06-10 · 1 datiertes seit 2026-06-10 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

FLUX.2 Klein 9B Manga-Kolorierungs-LoRA ist ein LoRA-Adapter für Zeichner sowie für ComfyUI- oder Diffusers-Anwender, die Figurenfarbpaletten von einer farbigen Referenz auf Strichzeichnungen oder Graustufen-Panels übertragen.

- Palettenabgleich für Haar-, Augen-, Kleidungs- und Hauttöne.
- Unterstützung mehrerer Figuren auf einem einzigen Referenzbild.
- Prompt-Hinweise für Beleuchtungs- und Hintergrundanpassungen.

## Entwicklungslinie {#development-line}

- **2026-06-10 — Hugging-Face-Modellreferenz für das Projekt erfasst.** Wir haben das Hugging-Face-Modell-Repository für die FLUX.2 Klein 9B Manga-Kolorierung per Referenz-LoRA am 2026-06-10 erfasst.

## Was sich geändert hat {#what-changed}

2026-06-10 — Das initiale Apache-2.0-Adapter-Repository für FLUX.2 Klein 9B Base wurde veröffentlicht; es setzt den Trigger `mngclranm` und gibt das Basismodell an. 2026-07-05 — Ein Drittanbieter-ComfyUI-Workflow zeigte die Stapelkolorierung eines Seitenordners gegen eine separate Farbreferenz; dabei handelt es sich um eine Community-Integration, nicht um eine neue LoRA-Version.

## So wird es verwendet {#how-to-use-this}

Stand 2026-06-10 sollte die verlinkte Hugging-Face-LoRA als Referenz-Workflow behandelt werden. Prüfen Sie Funktionsumfang, Kompatibilität, Lizenzierung und Nutzungsanleitung, bevor Sie sie einsetzen.

1. Laden Sie `black-forest-labs/FLUX.2-klein-base-9B` und binden Sie anschließend die Adapter-Gewichte mit `load_lora_weights` oder dem Load-LoRA-Knoten in ComfyUI ein.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
2. Stellen Sie die Schwarz-Weiß-Seite als Zielbild und ein separates farbiges Figurenblatt, Coverbild oder Splash-Page als Referenz bereit.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
3. Ergänzen Sie `mngclranm` im Prompt; bei Bedarf Hinweise zu Beleuchtung, Stimmung oder Hintergrund hinzufügen.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
4. Beginnen Sie mit einem LoRA-Gewicht von 0,8–1,0; reduzieren Sie es, falls die Farbübertragung übermäßig stark wird.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>

## Bewährte Vorgehensweisen {#best-practices}

- Wählen Sie eine saubere Referenz, auf der die Seitenfiguren klar erkennbar sind; ein Cover oder Figurenblatt eignet sich für mehrere Figuren.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
- Wenn sich Figurenfarben vermischen, ändern Sie zuerst den Seed; danach die Referenz bereinigen oder die Seite in kleinere Panels aufteilen.
  — <https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/>
- Halten Sie in ComfyUI die Zielseite größer als die Referenz: Bei etwa 1,5 MP gegenüber 0,5 MP Referenz verringerte sich in gemeinsamen Tests das Übergreifen der Referenzkomposition.
  — <https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/>

## Abgelöst durch {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Die Repository-Dokumentation beschreibt einen Workflow mit zwei Referenzbildern, ihr generisches Diffusers-Widget-Beispiel zeigt jedoch nur ein Eingabebild; der genaue öffentliche Diffusers-Aufruf zur Übergabe des zweiten Farbreferenzbildes ist dort nicht dokumentiert.
- Nach dem initialen Commit vom 2026-06-10 wurde kein Changelog des Herstellers und keine spätere Modellrevision gefunden; der Eintrag vom 2026-07-05 ist Community-Workflow-Beleg, keine LoRA-Veröffentlichung.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA | thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA | 2026-09-05 |
| https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA/commit/78d5314569e7fdc7fb14dabde2281fd82db61304 | initial commit · thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA at 78d5314 | 2026-09-05 |
| https://docs.bfl.ai/flux_2/flux2_klein_training | FLUX.2 [klein] Training — Black Forest Labs | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/ | [ComfyUI] Manga Colorization with Color Reference | One-Click Batch Processing | Fast & Consistent Results | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:flux-2-klein-9b-manga-colorization-by-reference-lora`, Thread `manga-colorization-by-reference-lora`, 1 datiertes Ereignis 2026-06-10 → 2026-06-10.
- **Praktischer Hinweis:** Stand 2026-06-10 sollten Anwender die verlinkte Hugging-Face-LoRA als Kandidaten-Referenz für Manga-Kolorierungs-Workflows behandeln und ihre Funktionsweise, Kompatibilität, Lizenzierung und Nutzungsanleitung vor dem Einsatz eigenständig prüfen.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich für die Frage, was veraltet ist.
