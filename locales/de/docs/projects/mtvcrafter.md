---
title: "MTVCrafter"
category: projects
date: 2025-05-22
tags: [mtvcrafter, mtvcrafter-public-development, project]
aliases: ["MTVCrafter"]
level: 3
source_sha256: cd74f7b339d4694cdf699c0a81fdb7ef4ee28386df8ca0ba87cadca58ae72d7a
translation: machine
translated_at: '2026-10-24'
---
# MTVCrafter {#mtvcrafter}

**Entwicklungslinie:** `project:mtvcrafter` · Thread `mtvcrafter-public-development`  
**Letztes Ereignis:** 2025-05-22 · 1 datiertes Ereignis seit 2025-05-22 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

MTVCrafter ist eine lokale Pipeline zur Animation menschlicher Bilder für GPU-Nutzer, die ein Referenzbild und ein Steuervideo mit rekonstruierbarer SMPL-Bewegung bereitstellen.

- 4DMoT wandelt 3D-Gelenkpositionen über die Zeit in Bewegungs-Tokens um.
- MV-DiT steuert ein Image-to-Video-Backbone auf Basis von CogVideoX oder Wan2.1.
- Der Wan-Pfad ergänzt eine Textsteuerung.

Die mitgelieferten Skripte erzeugen Einheiten zu 49 Frames und setzen CUDA voraus. Führen Sie das Repository und die Checkpoints lokal aus, da der offizielle Space keinen funktionierenden GPU-Treiber besitzt.

## Entwicklungslinie {#development-line}

- **2025-05-22 — Öffentliche Ressourcen zu MTVCrafter wurden verlinkt.** MTVCrafter etablierte den Ansatz aus 4DMoT und MV-DiT. Ein Referenzbild wird direkt aus rohen 3D-Bewegungsdaten animiert statt aus gerenderten 2D-Posenkarten.

## Was sich geändert hat {#what-changed}

- 2025-05-22: MTVCrafter etablierte den Ansatz aus 4DMoT und MV-DiT. Die Pipeline animiert ein Referenzbild direkt aus rohen 3D-Bewegungsdaten und nicht aus gerenderten 2D-Posenkarten.
- 2025-08-15: Der zugehörige MV-DiT-Checkpoint-Baum trennte die Methode in lokale Inferenzpfade für CogVideoX und Wan-2.1.

## Verwendung {#how-to-use-this}

Ab 2025-05-22 sollten Sie beim Auffinden von MTVCrafter mit der datierten Projektseite, dem Repository und der Hugging-Face-Modellseite beginnen. Der Link vom 2025-08-15 allein belegt keine neue Komponente, kein neues Release und keinen neuen Workflow.

1. Klonen Sie die aktuelle Implementierung, legen Sie eine saubere Python-3.10+-Umgebung an und installieren Sie requirements.txt.
  — <https://github.com/DINGYANB/MTVCrafter>
2. Laden Sie den NLF-Posenschätzer, ein passendes Basismodell (CogVideoX-5B für 7B oder Wan2.1 I2V-14B für 17B) sowie die MTVCrafter-Gewichte für 4DMoT/MV-DiT herunter.
  — <https://github.com/DINGYANB/MTVCrafter>
3. Beginnen Sie mit data/sampled_data.pkl; für ein Steuervideo führen Sie process_nlf.py aus, um die SMPL-Bewegungsvideo-.pkl-Eingabe zu erzeugen.
  — <https://github.com/DINGYANB/MTVCrafter>
4. Führen Sie den CogVideoX-Pfad mit infer_7b.py aus, mit einem Referenzbild, dem Pfad zu den Bewegungsdaten und --output_dir.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_7b.py>
5. Für die Textsteuerung über Wan verwenden Sie infer_17b.py mit denselben Pfaden und optional --prompt; zusätzlich akzeptiert das Skript --output_dir.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_17b.py>
6. Für den 17B-Pfad sind mindestens 89 Eingabe-Frames erforderlich: Das Skript verbindet zwei Clips zu je 49 Frames mit einer Überlappung von neun Frames.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_17b.py>

## Bewährte Praktiken {#best-practices}

- Installieren Sie die festgelegten Projektabhängigkeiten in einer sauberen Umgebung, statt einen generischen Diffusers-Stack zusammenzustellen.
  — <https://github.com/DINGYANB/MTVCrafter>
- Verwenden Sie --output_dir, das aktuell dokumentierte und implementierte Ausgabe-Flag für beide Inferenzpfade.
  — <https://github.com/DINGYANB/MTVCrafter>
- Prüfen Sie vor dem Start, ob eine CUDA-GPU verfügbar ist; der offizielle Space schlägt fehl, weil seine Laufzeitumgebung keinen NVIDIA-Treiber enthält.
  — <https://huggingface.co/spaces/yanboding/MTVCrafter>
- Validieren Sie einen ersten Lauf mit der mitgelieferten sampled_data.pkl, bevor Sie die NLF-Extraktion aus eigenem Filmmaterial debuggen.
  — <https://github.com/DINGYANB/MTVCrafter>
- Verwenden Sie die Skripte der Autoren als maßgeblichen Pfad: Das 7B-Skript baut eine eigene MTVCrafterPipeline7B und lädt CogVideoX- und 4DMoT-Assets separat.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_7b.py>
- Behandeln Sie das optionale Wan-FusionX-LoRA als Kompromiss: Die Maintainer weisen darauf hin, dass es Geschwindigkeit und Details verbessern, die Bewegungsgenauigkeit aber verschlechtern kann.
  — <https://github.com/DINGYANB/MTVCrafter>

## Dadurch überholt {#superseded-by-this}

- 2025-08-24: Die Schnellstart-Anleitung zu --output_path ist veraltet; aktuelle Inferenzskripte verwenden --output_dir.
- 2026-03-09: MTVCrafter ist nicht mehr der Titel des arXiv-Papers; zitieren Sie für das überarbeitete Paper MTVCraft und für die Repositories MTVCrafter.
- 2026-09-04: Die Empfehlung, die offizielle Demo-Space zu verwenden, ist veraltet; der Space schlägt vor der Inferenz fehl, weil seiner Laufzeitumgebung ein NVIDIA-Treiber fehlt.
- 2026-09-04: Die Annahme, DINGYANB/MTVCtafter sei der Code-Checkout, ist veraltet; es handelt sich um das statische Repository der Projektseite.

## Weiterhin unbekannt {#still-unknown}

- Der MV-DiT-Baum vom 2025-08-15 enthält kein angegebenes Veröffentlichungsdatum, daher lässt sich der genaue Zeitpunkt nicht unabhängig verifizieren.
- Die Maintainer verlinken die statische Projektseite MTVCtafter und das lauffähige Code-Repository MTVCrafter, haben aber nicht dokumentiert, warum sich die Namen unterscheiden.
- Das überarbeitete arXiv-Paper trägt den Titel MTVCraft, während Code- und Modell-Repositories weiterhin MTVCrafter verwenden; kein Hinweis der Maintainer erklärt die Namensänderung.
- Es wurde keine offizielle chinesischsprachige Dokumentation und kein unabhängig reproduzierbarer chinesischsprachiger Erfahrungsbericht gefunden.
- Es wurde keine aktuelle offizielle Angabe zum GPU-Speicherbedarf und kein unabhängig reproduzierter Qualitäts-Benchmark gefunden.
- Der generische Diffusers-Codeausschnitt auf der Modellseite ist nicht bestätigt; es ist nicht belegt, dass er die von den Autoren gepflegten Inferenzskripte reproduziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://dingyanb.github.io/MTVCtafter/ | MTVCrafter-Projektseite | 2026-09-04 |
| https://github.com/dingyanb/MTVCtafter | DINGYANB/MTVCtafter-Repository der Projektseite | 2026-09-04 |
| https://github.com/DINGYANB/MTVCtafter/blob/main/index.html | Quelltext der statischen MTVCtafter-Projektseite | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter | DINGYANB/MTVCrafter-Implementierungs-Repository | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter/commits/main | Commit-Verlauf von DINGYANB/MTVCrafter | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter/blob/main/infer_7b.py | MTVCrafter-7B-Inferenzskript | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter/blob/main/infer_17b.py | MTVCrafter-17B-Inferenzskript | 2026-09-04 |
| https://huggingface.co/yanboding/MTVCrafter | Modell-Repository yanboding/MTVCrafter | 2026-09-04 |
| https://huggingface.co/yanboding/MTVCrafter/tree/main/MV-DiT | MTVCrafter-MV-DiT-Checkpoint-Baum | 2026-09-04 |
| https://huggingface.co/yanboding/MTVCrafter/blob/main/README.md | README der MTVCrafter-Modellkarte | 2026-09-04 |
| https://huggingface.co/spaces/yanboding/MTVCrafter | MTVCrafter-Hugging-Face-Space, Laufzeitstatus | 2026-09-04 |
| https://arxiv.org/abs/2505.10238 | Eintrag zum Paper MTVCraft / MTVCrafter | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:mtvcrafter`, Thread `mtvcrafter-public-development`, 1 datiertes Ereignis 2025-05-22 → 2025-05-22.
- **Praxishinweis:** Ab 2025-05-22 sollten Praktiker beim Auffinden von MTVCrafter mit der datierten Projektseite, dem Repository und der Hugging-Face-Modellseite beginnen. Der Link vom 2025-08-15 allein belegt keine neue Komponente, kein neues Release und keinen neuen Workflow.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Überholungshinweise oben als maßgeblich.
