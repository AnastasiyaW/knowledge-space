---
title: "LTX-2.3 Inpaint-LoRA"
category: projects
date: 2026-03-24
tags: [ltx-2-3-inpaint-lora, ltx_2_3_inpaint_lora, project]
aliases: ["LTX-2.3 inpaint LoRA"]
level: 2
source_sha256: cdfde29e8951086bdf99b48118bcb3ceb9998a2e40dfcf5bd23772aa400a7e8a
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.3 Inpaint-LoRA {#ltx-23-inpaint-lora}

**Entwicklungslinie:** `project:ltx-2-3-inpaint-lora` · Thread `ltx-2-3-inpaint-lora`  
**Letztes Ereignis:** 2026-03-24 · 1 datiertes seit 2026-03-24 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

LTX-2.3 Inpaint-LoRA ist ein Set von Community-LoRAs für Video-Maskierung in Lightricks/LTX-2.3: Text-only-Inpaint, Inpaint mit Referenz und die Wahl eines Checkpoints je nach Prompt-Treue oder Maskennutzung. Es ersetzt oder ergänzt Objekte nur innerhalb des vorbereiteten Bereichs; die MR2V-Variante akzeptiert ein visuelles Referenzbild oder eine leere Referenz für den Text-only-Modus; es handelt sich nicht um das offizielle LTX In-Outpainting IC-LoRA und nicht um eine erklärte Lösung für Face- oder Body-Swap. Limit: Bei MR2V sind Größe und Vorbereitung der Maske entscheidend; laut Autor sinkt die Qualität unterhalb von FP8 deutlich. Fazit: geeignet für Objektkorrekturen in kurzen Videos, sofern der Workflow dessen Farbmarkierung reproduziert; für Gesichter und das offizielle LTX-2.5 In/Outpainting wird ein anderer Adapter benötigt.

## Entwicklungslinie {#development-line}

- **2026-03-24 — Verteilungslinks für LTX-LoRAs erfasst.** Am 24. März 2026 wurden für diese Entwicklungslinie Links zu einem LTX-LoRAs-Repository auf Hugging Face und einer LTX-LoRAs-Seite auf Civitai erfasst. Die Links deuten auf einen öffentlichen Verteilungs- oder Fundschritt hin, der für das Projekt relevant ist, der Eintrag belegt jedoch weder die genaue Modellvariante, das Inpaint-Verhalten, die Kompatibilität, die Herkunft noch Details zur Veröffentlichung.

## Was sich geändert hat {#what-changed}

2026-03-24 — Das LTX-2.3 Inpaint-LoRA wurde als fertiger Workflow gezeigt, um Objekte zu ersetzen, Frames lokal zu korrigieren und einen einzelnen Bereich zu reparieren, ohne den gesamten Clip neu zu generieren. 2026-04-06 — Die experimentelle MR2V-Variante `ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors` wurde veröffentlicht: referenzgestütztes Inpaint innerhalb der Maske, ausgerichtet auf Objekte, nicht auf Face- oder Body-Swap. 2026-04-08 — Das README korrigierte die Namen zweier Text-to-Video-Checkpoints: Die bisherigen `ltx23_inpaint_rank128...` wurden durch `ltx23_inpaint_masked_t2v_rank128...` ersetzt.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-03-24 sollten Anwender die verlinkten Hugging-Face- und Civitai-Stellen als Quellen behandeln, die vor der Nutzung zu prüfen und zu verifizieren sind, statt anzunehmen, dass sie ein bestätigtes LTX-2.3-Inpainting-LoRA oder eine bestimmte Kompatibilitätsaussage bereitstellen.

1. LTX-2-Pipeline über `uv sync --frozen` installieren, das LoRA-Set und den Gemma-Text-Encoder herunterladen.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/tree/main>
2. Für die native Pipeline die gewünschte Datei über `--lora` laden und mit einem Gewicht von 1.0 beginnen; für Image-to-Video `--image` hinzufügen.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/tree/main>
3. Für Inpaint die Maske nicht über einen separaten Kanal übergeben, sondern in das Guide-Video einbetten und über `LTXVAddGuideMulti` einspeisen; die Maske ist Magenta `(255,0,255)`, der Referenzbereich Chroma-Key-Grün `(0,255,0)`.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md>
4. Für den Objektersatz mit Referenz `ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors` wählen; für den Text-only-Modus eine leere Referenz und einen ausführlichen Prompt verwenden.
  — <https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/>

## Best Practices {#best-practices}

- Zuerst die Varianten mit 2500 und 10000 Steps vergleichen: Erstere ist auf Prompt-Treue ausgerichtet, letztere auf das Füllen der Maske; keinen einzelnen Checkpoint als universell besten betrachten.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md>
- Für MR2V mit Blockify Mask size 8 beginnen und die Maske bei Bedarf erweitern: Die Trainingsverteilung nutzte blockweise Markierungen, und eine enge Maske verschlechtert den Objektersatz.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md>
- MR2V nicht als Face- oder Body-Swap-Modell einsetzen; es wurde überwiegend auf Objekten trainiert. Ergebnisse mindestens in FP8 prüfen, da der Autor bei niedrigerer Genauigkeit einen deutlichen Qualitätsverlust beobachtete.
  — <https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/>

## Abgelöst durch dieses {#superseded-by-this}

- 2026-04-08: Die Namen `ltx23_inpaint_rank128_v1_02500steps.safetensors` und `ltx23_inpaint_rank128_v1_10000steps.safetensors` in den Beispielen wurden durch `ltx23_inpaint_masked_t2v_rank128_v1_02500steps.safetensors` und `ltx23_inpaint_masked_t2v_rank128_v1_10000steps.safetensors` ersetzt.
- Das offizielle LTX-2.5 In-Outpainting IC-LoRA ersetzt dieses Community-Set nicht automatisch: Es ist ein eigener Checkpoint mit eigenem Workflow.

## Weiterhin unbekannt {#still-unknown}

- Civitai lieferte während der Recherche keinen lesbaren Seiteninhalt; die Existenz dieser Quelle ist daher nur als Link aus dem Ereignis belegt, ohne unabhängige Prüfung der aktuellen Dateien oder Version.
- Der Zeitstempel des erstmaligen Uploads jeder Hugging-Face-Datei liegt nicht vor; der 24.03.2026 belegt die öffentliche Präsentation des Workflows, nicht den Git-Zeitstempel einzelner Gewichte.
- Die offizielle Datei `ltx-2.3-22b-ic-lora-in-outpainting-0.9.safetensors`, die LTX für LTX-2.5 verwendet, ist nicht als kompatibel oder austauschbar mit den Community-Dateien von Alissonerdx belegt.
- event_findings:[{"event_date":"2026-03-24","finding":"An diesem Tag wurde das Set als Workflow beschrieben, um Objekte zu entfernen oder zu ersetzen, Frames punktuell zu korrigieren und einen einzelnen Bereich zu reparieren, ohne den gesamten Clip neu zu generieren.","source_date":"2026-03-24","source_url":"https://www.youtube.com/watch?v=PX3-OqOz6rE"}]
- new_events:[{"date":"2026-04-06","finding":"Der Autor nannte die genaue experimentelle MR2V-Datei `ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors`; sie führt referenzbasiertes Inpaint innerhalb der Maske aus, ist auf Objekte ausgerichtet und nicht für Face- oder Body-Swap gedacht.","source_date":"2026-04-06","source_url":"https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/"},{"date":"2026-04-08","finding":"Das README benannte zwei T2V-Inpaint-Checkpoints in Varianten mit `masked_t2v` um und korrigierte damit zuvor gezeigte Dateinamen.","source_date":"2026-04-08","source_url":"https://huggingface.co/Alissonerdx/LTX-LoRAs/commit/345088ffcbda7ea9680bd73e145371e527450ff6"}]

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/Alissonerdx/LTX-LoRAs/tree/main | Alissonerdx/LTX-LoRAs | 2026-09-05 |
| https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md | README.md · Alissonerdx/LTX-LoRAs | 2026-09-05 |
| https://civitai.com/models/2484952/ltx-loras | LTX LoRAs - LTX-2.3 Inpainting | Civitai | 2026-09-05 |
| https://www.youtube.com/watch?v=PX3-OqOz6rE | LTX23 Inpainting Is Here: Alissonerdx Inpaint LoRA + Ready Workflows | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/ | Inpainting mit Referenz für LTX-2.3 (MR2V) | 2026-09-05 |
| https://huggingface.co/Alissonerdx/LTX-LoRAs/commit/345088ffcbda7ea9680bd73e145371e527450ff6 | Update README.md · Alissonerdx/LTX-LoRAs | 2026-09-05 |
| https://docs.ltx.io/open-source-model/feature-guides/editing-effects/in-outpainting | Inpainting und Outpainting | LTX Documentation | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:ltx-2-3-inpaint-lora`, Thread `ltx-2-3-inpaint-lora`, 1 datiertes Ereignis 2026-03-24 → 2026-03-24.
- **Praktischer Hinweis:** Stand 2026-03-24 sollten Anwender die verlinkten Hugging-Face- und Civitai-Stellen als Quellen behandeln, die vor der Nutzung zu prüfen und zu verifizieren sind, statt anzunehmen, dass sie ein bestätigtes LTX-2.3-Inpainting-LoRA oder eine bestimmte Kompatibilitätsaussage bereitstellen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich für das, was veraltet ist.
