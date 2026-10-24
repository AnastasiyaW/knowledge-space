---
title: "LTX-2.3-Foley-LoRA — LTX Video"
category: projects
date: 2026-07-01
tags: [ltx-foley-lora, ltx-video, ltx_video, project]
aliases: ["LTX-2.3-Foley-LoRA"]
level: 2
source_sha256: 4e3d5aea59ce758a576954ce94e5c9cf11a7478eef944dff5068292c58c1285e
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.3-Foley-LoRA — LTX Video {#ltx-23-foley-lora-ltx-video}

**Entwicklungslinie:** `project:ltx-foley-lora` · Thread `ltx-video`  
**Letztes Ereignis:** 2026-07-01 · 1 datierter Eintrag seit 2026-07-01 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

LTX-2.3-Foley-LoRA ist ein 400-Schritte-Video-zu-Audio-LoRA für die Basis- oder destillierten Modelle von LTX-2.3. Es nimmt ein stummes Video und einen Aktionsprompt entgegen und erzeugt synchronisierte, nicht-sprachliche Foley-Geräusche. Es ist kein allgemeines Musik- oder Dialogmodell. Verwenden Sie einen LoRA-Multiplikator von 1–3. Es behebt LTX-2.3-Generierungen, die Hintergrundmusik hinzufügen, das Sprachverhalten ist jedoch nicht ausreichend dokumentiert.

## Entwicklungslinie {#development-line}

- **2026-07-01 — Die Modellseite von LTX-2.3-Foley-LoRA wurde erfasst.** Am 2026-07-01 veröffentlichte FuzzPuppy die Hugging-Face-Modellseite für LTX-2.3-Foley-LoRA. Die Seite stellt das Foley-LoRA-Artefakt bereit, beschreibt aber weder dessen Fähigkeiten, Herkunft, Kompatibilität noch Veröffentlichungsdetails.

## Was sich geändert hat {#what-changed}

- 2026-07-01 — LTX-2.3-Foley-LoRA wurde als 400-Schritte-Adapter veröffentlicht, um Musikeinblendungen zu unterdrücken und visuell passende Soundeffekte zu erzeugen. Der Autor hat es ohne Sprachbeispiele trainiert und Sprache nicht getestet.
- 2026-07-04 — Das zugehörige ComfyUI-Repository hat einen Sliding-Window-Workflow für lange Videos mit Überlappung und Audio-Zusammenfügung ergänzt und damit den ursprünglichen Workflow für kurze Clips erweitert.

## So verwenden Sie es {#how-to-use-this}

Ab dem 2026-07-01 sollten Sie LTX-2.3-Foley-LoRA auf Hugging Face evaluieren und überprüfen, bevor Sie es in der Produktion einsetzen; allein diese Zeile stützt keine betrieblichen Aussagen.

1. Laden Sie `ltx-2.3-foley-400-steps.safetensors` herunter, laden Sie es mit einem Video-zu-Audio-Basis- oder destillierten Modell von LTX-2.3 und beginnen Sie mit einer LoRA-Stärke von 1.0.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA>
2. Für ComfyUI installieren Sie die offiziellen LTXVideo-Nodes sowie die Hilfs-Nodes `ltx_foley_v2a` aus dem Workflow-Repository; legen Sie das LoRA in `ComfyUI/models/loras` ab.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow>
3. Verwenden Sie den kurzen Workflow für einen schnellen Clip; verwenden Sie `foley-sliding-window.json` für längere Videos, damit Fenster überlappt und zusammengefügt werden.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow>

## Best Practices {#best-practices}

- Beschreiben Sie nur die sichtbare Aktion und ergänzen Sie dann „No speech is present. No music is present“; verwenden Sie einen Anti-Musik-Negativprompt.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA>
- Erhöhen Sie die LoRA-Stärke von 1 auf 2 oder 3 nur dann, wenn weiterhin Musik in der Ausgabe enthalten ist.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA>
- Starten Sie ComfyUI mit `--cache-classic` für den Sliding-Window-Workflow, damit große Ausgaben der LTX-Nodes nicht verdrängt und zwischen den Fenstern neu berechnet werden.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow>

## Dadurch ersetzt {#superseded-by-this}

- 2026-07-04 — Den ursprünglichen Workflow für kurze Clips als einzig unterstützten Weg zu betrachten, ist für lange Videos veraltet; verwenden Sie stattdessen den Sliding-Window-Workflow.

## Weiterhin unbekannt {#still-unknown}

- Die Modellkarte dokumentiert weder Trainingsdaten, Evaluationsmetriken, genaue VRAM-Anforderungen noch zuverlässige Erhaltung von Dialogen.
- Das Workflow-Update vom 2026-07-04 erscheint in der Repository-Historie und in der Dokumentation für lange Videos, besitzt aber keine unveränderliche Versionsnotiz.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA | FuzzPuppy/LTX-2.3-Foley-LoRA | 2026-09-05 |
| https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow | FuzzPuppy/LTX-2.3-Foley-Workflow | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1uk60hg/ltx23_foley_lora_for_synced_sound_effects_without/ | LTX-2.3 Foley LoRA für synchronisierte Soundeffekte ohne ungewollte Musik | 2026-09-05 |

## Agenten-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:ltx-foley-lora`, Thread `ltx-video`, 1 datierter Eintrag 2026-07-01 → 2026-07-01.
- **Praktischer Hinweis:** Ab dem 2026-07-01 sollten Praktiker LTX-2.3-Foley-LoRA als eigenständig verlinktes Foley-LoRA-Artefakt auf Hugging Face behandeln, das vor einem Einsatz evaluiert und überprüft werden sollte; allein diese Zeile stützt keine betrieblichen Aussagen.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
