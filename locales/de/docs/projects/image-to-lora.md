---
title: "Image-to-LoRA"
category: projects
date: 2026-06-17
tags: [image-to-lora, image-to-lora-v2-release, image_to_lora, project]
aliases: ["Image-to-LoRA"]
level: 2
source_sha256: 59033f2ee5db4d6be07e424fe0ccdd3edfdceaa41acecc78e7642c811a7a9f81
translation: machine
translated_at: '2026-10-24'
---
# Image-to-LoRA {#image-to-lora}

**Entwicklungslinie:** `project:image-to-lora` · Thread `image-to-lora-v2-release`  
**Letztes Ereignis:** 2026-06-17 · 1 datiertes seit 2026-06-17 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Image-to-LoRA ist die i2L-Methode von DiffSynth-Studio, die aus einem oder mehreren Referenzbildern explizite Style-LoRA-Gewichte erzeugt, anstatt für jeden Stil ein neues LoRA zu optimieren.

- Style-Transfer: erzeugt explizite Style-LoRA-Gewichte aus Referenzbildern.
- Fusion mehrerer Referenzen: kombiniert Stilmerkmale aus mehreren Referenzbildern.
- Kontrollierte Komposition: verbindet den Zielstil mit Generierungssteuerungen.

Die veröffentlichte V2-Familie zielt auf drei backbone-spezifische Modelle, und jedes i2L-Modell funktioniert nur mit seiner passenden Basisarchitektur. Verwenden Sie es für die schnelle Stilinstanziierung innerhalb von DiffSynth-Studio, nicht als direkten LoRA-Generator für beliebige UIs oder Backbones.

## Entwicklungslinie {#development-line}

- **2026-06-17 — Die Image-to-LoRA-V2-Sammlung wurde zu einem öffentlichen Projektmeilenstein.** Am 2026-06-17 veröffentlichte Image-to-LoRA eine öffentliche ModelScope-Sammlung für Image-to-LoRA V2. Diese Sammlung dient zu diesem Datum als öffentlicher Verteilungspunkt des Projekts. Die verfügbaren Quellen nennen über diese verlinkte Sammlung hinaus keine technischen Änderungen, keine Urheberschaft und keinen Freigabestatus.

## Was sich geändert hat {#what-changed}

- 2025-12-09 — Qwen-Image-i2L führte das frühere Image-to-LoRA-Modell ein, mit Hinweisen der Maintainer zu Grenzen bei Generalisierung und Detailerhalt.
- 2026-06-11 — Der i2L-Technical-Report beschrieb die Vorhersage expliziter LoRA-Gewichte aus einer oder mehreren Referenzen in einem einzigen Forward-Pass.
- 2026-06-15 — Image-to-LoRA V2 wurde für Z-Image, FLUX.2-klein-base-4B und HiDream-O1-Image als Open Source veröffentlicht.
- 2026-06-17 — Image-to-LoRA V2 wurde als veröffentlichte Modellfamilie mit drei backbone-spezifischen Modellen gesammelt, nicht als ein universelles LoRA.

## So verwenden Sie es {#how-to-use-this}

Ab dem 2026-06-17 nutzen Sie die verlinkte ModelScope-Sammlung als datierten Referenzpunkt, um Image-to-LoRA V2 zu finden und zu bewerten, und prüfen Sie Dokumentation und technisches Verhalten getrennt davon.

1. Installieren Sie DiffSynth-Studio aus dem Quellcode und wählen Sie bei Bedarf den internationalen ModelScope-Endpunkt oder die Hugging-Face-Download-Quelle.
  — <https://github.com/modelscope/DiffSynth-Studio>
2. Wählen Sie den V2-Checkpoint, der zum Generierungs-Backbone passt. Für Z-Image laden Sie `DiffSynth-Studio/ZImage-i2L-v2` mit der Z-Image-Pipeline und aktivieren das LoRA-Hot-Loading.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py>
3. Stellen Sie die Liste der Referenzbilder, einen Generierungsprompt und passende Negativ-Template-Eingaben bereit. Führen Sie das Template durch die Basis-Pipeline, um das gestylte Bild zu erzeugen.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py>
4. Für FLUX.2-klein-base-4B verwenden Sie das separate Beispiel `KleinBase4B-i2L-v2` und die passende FLUX.2-Pipeline, nicht den Z-Image-Checkpoint.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/flux2/model_inference/KleinBase4B-i2L-v2.py>

## Best Practices {#best-practices}

- Kombinieren Sie den i2L-Checkpoint und die Basisarchitektur exakt; V2 enthält separate Checkpoints für Z-Image, FLUX.2-klein-base-4B und HiDream-O1-Image.
  — <https://github.com/modelscope/DiffSynth-Studio>
- Verwenden Sie ein oder mehrere Referenzbilder, die den Zielstil konsistent ausdrücken, und nutzen Sie dann den Textprompt für die neue Szene oder Komposition. i2L trennt Erscheinungsbild vom Referenzinhalt.
  — <https://arxiv.org/abs/2606.13809>
- Beginnen Sie mit dem gepflegten Inferenzbeispiel, einschließlich seines LoRA-Hot-Loadings und der Negativ-Template-Eingabe-Konfiguration, bevor Sie Prompts, Anzahl der Referenzen oder Sampling-Einstellungen ändern.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py>

## Hierdurch ersetzt {#superseded-by-this}

- 2025-12-09 — Der frühere Qwen-Image-i2L-Stand wird für die von V2 unterstützten Backbones durch die V2-Familie ersetzt. Behandeln Sie seine Grenzen bei Generalisierung und Detailerhalt nicht als V2-Benchmark.
- 2026-06-15 — Hinweise, die Image-to-LoRA als einzelnes Qwen-only-Modell behandeln, sind veraltet: V2 ist eine Veröffentlichung mit drei Checkpoints, die jeweils an ein Backbone gebunden sind.

## Weiterhin unbekannt {#still-unknown}

- Die ModelScope-Sammlung war erreichbar, enthielt aber keine lesbaren Metadaten. Daher bleiben ihr Veröffentlichungszeitstempel und die Lizenzbedingungen je Checkpoint ungeprüft.
- Keine Quelle aus erster Hand belegt einen unterstützten ComfyUI-Workflow oder garantiert, dass Gewichte außerhalb von DiffSynth-Studio exportiert und verwendet werden können.
- Für 2026-06-17 legen Repository-Updates vom 2026-06-15 den genauen V2-Umfang fest: `ZImage-i2L-v2`, `KleinBase4B-i2L-v2` und `HidreamO1-i2L-v2`. Der Technical Report wurde am 2026-06-11 eingereicht. Frühere Ereignisse: 2025-12-09, Qwen-Image-i2L mit genannten Grenzen veröffentlicht; 2026-06-11, der i2L-Technical-Report eingereicht; 2026-06-15, V2 als Open Source veröffentlicht. Alle Angaben stammen aus den oben aufgeführten Quellen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://modelscope.ai/collections/DiffSynth-Studio/Image-to-LoRA-V2 | ModelScope — Sammlung DiffSynth-Studio/Image-to-LoRA-V2 | 2026-09-05 |
| https://github.com/modelscope/DiffSynth-Studio | DiffSynth-Studio — Repository und Update-Verlauf | 2026-09-05 |
| https://arxiv.org/abs/2606.13809 | Compressing Image Style Training into a Single Model Forward | 2026-09-05 |
| https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py | ZImage-i2L-v2 Inferenzbeispiel | 2026-09-05 |
| https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/flux2/model_inference/KleinBase4B-i2L-v2.py | KleinBase4B-i2L-v2 Inferenzbeispiel | 2026-09-05 |

## Agenten-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:image-to-lora`, Thread `image-to-lora-v2-release`, 1 datiertes Ereignis 2026-06-17 → 2026-06-17.
- **Praktischer Hinweis:** Ab dem 2026-06-17 nutzen Sie die verlinkte ModelScope-Sammlung als datierten Referenzpunkt, um Image-to-LoRA V2 zu finden und zu bewerten, und prüfen Dokumentation und technisches Verhalten dabei separat.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
