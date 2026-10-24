---
title: "SDXL"
category: projects
date: 2023-06-22
tags: [project, sdxl, sdxl-development]
aliases: ["SDXL", "SDXL 0.9", "SDXL 1.0"]
level: 2
source_sha256: fdcc92cf54ef02510fc3464644de778f2d49863834ba99fe0bf5b5bdc4b877a0
translation: machine
translated_at: '2026-10-24'
---
# SDXL {#sdxl}

**Entwicklungslinie:** `project:sdxl` · Thread `sdxl-development`  
**Letztes Ereignis:** 2023-06-22 · 2 datierte Ereignisse seit 2023-05-24 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

SDXL: ein Stable-Diffusion-Modell für Praktiker, die promptgesteuerte Bildgenerierung benötigen.

- Erzeugt Text-zu-Bild-, Bild-zu-Bild- und Inpainting-Ergebnisse.
- Betreibt den offiziellen 1.0-Basis-Checkpoint allein oder mit einem optionalen Refiner.
- Standardziel: 1024×1024; die Standard-Checkpoints werden unterhalb von 512 Pixeln nicht empfohlen.

## Entwicklungslinie {#development-line}

- **2023-05-24 — Meilenstein des SDXL-Trainingsfortschritts wurde gemeldet.** Am 2023-05-24 deutete ein datierter SDXL-Entwicklungslink darauf hin, dass das Modelltraining einen Zwischenmeilenstein erreicht hatte, und verwies Leser auf einen Community-Diskussionskanal. Dies ist ein wesentlicher Kontrollpunkt, da er das Projekt in einer aktiven Pre-Release-Phase aus Training und Feedback dokumentiert.
- **2023-06-22 — Stability AI veröffentlichte ein Update zu SDXL 0.9.** Es war über Clipdrop verfügbar, Forschungsgewichte waren verfügbar, und 1.0 war für Mitte Juli geplant.

## Was sich geändert hat {#what-changed}

2023-05-24 — SDXL war noch etwa zur Hälfte trainiert; ein Discord-Bot sammelte während der Parametertests Bewertungen zu Bildpräferenzen, es handelte sich also um Trainingsfeedback und nicht um ein Release. 2023-06-22 — SDXL 0.9 ging von der Beta in Richtung einer eingeschränkten Forschungsveröffentlichung über: Es war über Clipdrop verfügbar, Forschungsgewichte waren verfügbar, und 1.0 war für Mitte Juli geplant. 2023-06-25 — der verlinkte offizielle Beitrag kann heute nicht abgerufen werden, daher lässt sich daraus keine weitere technische Änderung verifizieren. 2023-07-26 (gefunden 2026-09-04) — SDXL 1.0 wurde als offenes Modell veröffentlicht und ersetzte das eingeschränkte, nur für die Forschung gedachte 0.9-Release durch die Basis-plus-optionaler-Refiner-Linie 1.0. 2026-09-04 (heute gefunden) — der gepflegte praktische Weg ist der offizielle Checkpoint `stabilityai/stable-diffusion-xl-base-1.0` über Diffusers; die Basis bleibt ohne Refiner nutzbar.

## Verwendung {#how-to-use-this}

Ab 2023-06-22 sollten Praktiker SDXL 0.9 in Modell- und Workflow-Notizen separat erfassen: Diese Linie wechselt von einem Trainingsstatus-Update zu einer benannten SDXL-0.9-Veröffentlichung.

1. Installieren Sie Diffusers, Transformers, Accelerate und die optionale Abhängigkeit invisible-watermark gemäß dem aktuellen SDXL-Leitfaden.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
2. Laden Sie `stabilityai/stable-diffusion-xl-base-1.0` mit `StableDiffusionXLPipeline` oder `AutoPipelineForText2Image`, vorzugsweise als fp16-Safetensors auf einem unterstützten Beschleuniger.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
3. Beginnen Sie Text-zu-Bild-Arbeiten mit 1024×1024; verwenden Sie 768×768 oder 512×512 nur, wenn der Workflow es erfordert, und vermeiden Sie kleinere Abmessungen mit dem Standard-Checkpoint.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
4. Für eine Bearbeitung verwenden Sie die geladene Pipeline erneut als Bild-zu-Bild mit einem Eingabebild oder als Inpainting mit einem Eingabebild und einer Maske.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
5. Fügen Sie `stabilityai/stable-diffusion-xl-refiner-1.0` nur hinzu, wenn ein abschließender Entrauschungsdurchlauf den zusätzlichen Rechenaufwand wert ist; die dokumentierte Ensemble-Übergabe besteht aus 80 % Base-Entrauschung und 20 % Refiner-Entrauschung.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
6. Prüfen Sie vor dem Veröffentlichen oder Automatisieren von Ausgaben die Lizenz der Model Card, die Grenzen der vorgesehenen Verwendung und bekannte Fehler bei Text, Gesichtern, Komposition und sachlichen Darstellungen.
  — <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0>

## Bewährte Praktiken {#best-practices}

- Verwenden Sie den offiziellen 1.0-Basis-Checkpoint als Ausgangspunkt und behandeln Sie den Refiner als optional; die Basis ist ein unterstützter eigenständiger Weg.
  — <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0>
- Halten Sie die Standardgenerierung mit SDXL nahe am nativen Ziel von 1024×1024; nutzen Sie Größen- und Crop-Konditionierung für die Komposition, anstatt zu erwarten, dass der Standard-Checkpoint unterhalb von 512 Pixeln gut arbeitet.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
- Bei Out-of-Memory-Fehlern verwenden Sie Model CPU Offload, bevor Sie den dokumentierten Auflösungsbereich aufgeben; setzen Sie `torch.compile` oder xFormers nur ein, wenn die Laufzeitumgebung sie unterstützt.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
- Behalten Sie die Abhängigkeit invisible-watermark bei, wenn die Kennzeichnung generierter Bilder vom Workflow verlangt wird; Diffusers aktiviert sie standardmäßig, sofern sie installiert ist.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
- Verwenden Sie SDXL-Ausgaben nicht als sachliche Darstellung von Personen oder Ereignissen, und behalten Sie eine menschliche Prüfung für lesbaren Text, Gesichter und räumliche Beziehungen bei.
  — <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0>

## Durch diesen Stand überholt {#superseded-by-this}

- 2023-05-24 — Discord-Abstimmungen und Parameterexperimente waren ein Pre-Release-Prozess für Trainingsfeedback und kein Deployment-Pfad; die offenen Gewichte von SDXL 1.0 haben diesen Zustand am 2023-07-26 abgelöst.
- 2023-06-22 — Die Hinweise zu den Forschungsgewichten von SDXL 0.9 und zur Clipdrop-Vorschau sind für neue Deployments veraltet; verwenden Sie stattdessen den benannten Basis-Checkpoint von SDXL 1.0.
- 2023-06-22 — Der geplante Wechsel zu 1.0 Mitte Juli ist keine zukünftige Handlungsanweisung mehr; das offene Release von SDXL 1.0 erfolgte am 2023-07-26.

## Weiterhin ungeklärt {#still-unknown}

- Die angegebene Twitter-URL vom 2023-06-25 lieferte im verfügbaren Reader keine lesbaren Beitragsdaten; ihre genaue Aussage und technische Auswirkung bleiben ungeprüft.
- Dies behauptet keine aktuelle Verfügbarkeit, Preisgestaltung oder Supportstatus für die 2023 genannten Legacy-Engines der Stability API; die aktuelle Evidenz stützt nur den Checkpoint-und-Diffusers-Workflow.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://www.reddit.com/r/StableDiffusion/comments/13ppmtk/sdxl_is_now_50_trained_and_we_need_your_help/ | SDXL ist jetzt zu ~50 % trainiert – und wir brauchen Ihre Hilfe! | 2026-09-04 |
| https://stability.ai/blog/sdxl-09-stable-diffusion | Stability AI startet SDXL 0.9: Ein Sprung nach vorn in der KI-Bildgenerierung | 2026-09-04 |
| https://twitter.com/emostaque/status/1672700056154275841?s=21&t=RcamOh5xDIh5ilUsd6CSdA | Beitrag von Emad Mostaque zu SDXL (Inhalt nicht abrufbar) | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-sdxl-1-announcement | Ankündigung von SDXL 1.0 | 2026-09-04 |
| https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 | stabilityai/stable-diffusion-xl-base-1.0 — SD-XL 1.0-base Model Card | 2026-09-04 |
| https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl | Stable Diffusion XL — Diffusers-Dokumentation | 2026-09-04 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:sdxl`, Thread `sdxl-development`, 2 datierte Ereignisse 2023-05-24 → 2023-06-22.
- **Praktischer Hinweis:** Ab 2023-06-22 sollten Praktiker SDXL 0.9 in Modell- und Workflow-Notizen separat erfassen: Diese Linie wechselt von einem Trainingsstatus-Update zu einer benannten SDXL-0.9-Veröffentlichung.
- **Konfidenz:** mittel. Die datierten Vermerke zur Ersetzung oben sind maßgeblich dafür, was veraltet ist.
