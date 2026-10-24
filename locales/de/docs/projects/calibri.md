---
title: "Calibri"
category: projects
date: 2026-03-29
tags: [calibri, project]
aliases: ["Calibri"]
level: 2
source_sha256: 664d9e97c3eec161fca71f0df3c7f6339b0f5608ff6e6fd97e1db6ccd72addef
translation: machine
translated_at: '2026-10-24'
---
# Calibri {#calibri}

**Entwicklungslinie:** `project:calibri` · Thread `calibri`  
**Letztes Ereignis:** 2026-03-29 · 1 datiertes Ereignis seit 2026-03-29 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Calibri: Open-Source-Methode zur Kalibrierung von Diffusion Transformers für Entwickler von Text-to-Image-Pipelines. — fügt Koeffizienten an den Ausgängen der DiT-Blöcke hinzu; — bestimmt diese mit CMA-ES anhand eines Reward-Modells; — unterstützt FLUX.1-dev, Stable Diffusion 3.5 und Qwen-Image. Einschränkung: Fertige Gewichte sind nur für FLUX.1-dev und Qwen-Image veröffentlicht; ein offizielles gehostetes Inferenzangebot gibt es nicht. Fazit: Dies ist ein Werkzeug zur Beschleunigung und Anpassung eines bestehenden DiT-Modells, kein neues Basismodell.

## Entwicklungslinie {#development-line}

- **2026-03-29 — Die Projektressourcen zu Calibri wurden öffentlich auffindbar.** 12B `v-gen-ai/flux-calibri-gates` und 20B `v-gen-ai/qwen-calibri`; der Artikel wurde erstmals am 2026-03-25 bei arXiv eingereicht.

## Was sich geändert hat {#what-changed}

2026-03-29 — Es erschienen zwei fertige BF16-Modelle von Calibri: 12B `v-gen-ai/flux-calibri-gates` und 20B `v-gen-ai/qwen-calibri`; der Artikel wurde erstmals am 2026-03-25 bei arXiv eingereicht. 2026-04-13 — Offene Calibration Weights für FLUX.1-dev und Qwen-Image wurden veröffentlicht. 2026-07-29 — Der Artikel wurde auf arXiv v2 aktualisiert; das Repository beschreibt für diese Fassung kein eigenes neues Runtime-Release.

## So verwenden Sie es {#how-to-use-this}

Ab dem 2026-03-29 sollten Praktiker die verlinkte Projektseite, das Repository und die Hugging-Face-Collection als Ausgangspunkte für die Evaluierung von Calibri nutzen; genaue Versions- und Nutzungshinweise bleiben unverifiziert.

1. Für fertige Generierung mit FLUX laden Sie `v-gen-ai/flux-calibri-gates` über Diffusers in BF16 auf CUDA und verwenden 15 Schritte, Guidance Scale 3.5 und die Basisauflösung 512×512.
  — <https://huggingface.co/v-gen-ai/flux-calibri-gates>
2. Für fertige Generierung mit Qwen verwenden Sie `v-gen-ai/qwen-calibri` mit der in der Model Card angegebenen Custom Pipeline; Startparameter sind 15 Schritte, `true_cfg_scale=4.0`, 512×512.
  — <https://huggingface.co/v-gen-ai/qwen-calibri>
3. Für eigene Kalibrierung klonen Sie das Repository, erstellen die Umgebung über `uv sync`, starten den gewünschten Reward-Server und starten CMA-ES über Accelerate mit der Konfiguration aus `configs/calibri.py`.
  — <https://github.com/v-gen-ai/Calibri>

## Bewährte Praktiken {#best-practices}

- Beginnen Sie mit den veröffentlichten Gewichten und deren vorgesehenen Parametern statt mit eigenem Training: Für FLUX legt die Model Card 15 Schritte, Guidance Scale 3.5 und 512×512 fest.
  — <https://huggingface.co/v-gen-ai/flux-calibri-gates>
- Beim Training starten Sie zuerst den HPSv3- oder Q-Align-Reward-Server; das zentrale Training-Script ist ohne gewählten Reward-Dienst kein reproduzierbarer Lauf.
  — <https://github.com/v-gen-ai/Calibri>
- Wählen Sie die Granularität der Suche je nach Aufgabe: Block Scaling etwa 57 Parameter, Layer Scaling etwa 76, Gate Scaling etwa 114.
  — <https://github.com/v-gen-ai/Calibri>
- Prüfen Sie die Kalibrierung mit Ihrem eigenen Validation Dataset: Ein Inferenzlauf ohne `--prompt` erzeugt Validierungsbilder und berechnet Reward-Metriken.
  — <https://github.com/v-gen-ai/Calibri>

## Dadurch überholt {#superseded-by-this}

- 2026-04-13 — Für FLUX.1-dev und Qwen-Image ist die Annahme überholt, dass Calibri nur über eigene CMA-ES-Kalibrierung erhältlich ist: Es wurden fertige Calibration Weights veröffentlicht.
- 2026-07-29 — arXiv v1 vom 2026-03-25 wurde durch die Fassung v2 ersetzt; der Inhalt der Änderungen zwischen den Versionen ist in den ausgewerteten Quellen nicht offengelegt.

## Weiterhin unbekannt {#still-unknown}

- `event_findings`: 2026-03-29 — Die Hugging-Face-Collection, aktualisiert am 2026-03-27, präzisiert, dass das Release aus `v-gen-ai/flux-calibri-gates` (12B) und `v-gen-ai/qwen-calibri` (20B) bestand; arXiv v1 ist auf 2026-03-25 datiert. Quellen: https://huggingface.co/collections/v-gen-ai/calibri-models; https://arxiv.org/abs/2603.24800.
- `new_events`: 2026-04-13 — Calibration Weights für FLUX.1-dev und Qwen-Image wurden veröffentlicht. Quelle: https://github.com/v-gen-ai/Calibri.
- `new_events`: 2026-07-29 — arXiv v2 hat den Artikel aktualisiert; der eingesehene Eintrag enthält keine Liste inhaltlicher Unterschiede zu v1. Quelle: https://arxiv.org/abs/2603.24800.
- Der automatisch generierte Diffusers-Abschnitt in der Qwen-Model-Card weicht vom eigenständigen Abschnitt Guide to run ab: Letzterer verweist auf `makriot/qwen-calibri`, `custom_pipeline` und `trust_remote_code=True`. Anhand der ausgewerteten Quellen lässt sich nicht bestätigen, welcher der beiden Wege derzeit der kanonische ist.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://v-gen-ai.github.io/Calibri-page/ | Calibri: Parameter-Efficient Calibration of Diffusion Transformers | 2026-09-05 |
| https://github.com/v-gen-ai/Calibri | v-gen-ai/Calibri — offizielle Implementierung und README | 2026-09-05 |
| https://huggingface.co/collections/v-gen-ai/calibri-models | Calibri models — v-gen-ai Collection | 2026-09-05 |
| https://huggingface.co/v-gen-ai/flux-calibri-gates | v-gen-ai/flux-calibri-gates Model Card | 2026-09-05 |
| https://huggingface.co/v-gen-ai/qwen-calibri | v-gen-ai/qwen-calibri Model Card | 2026-09-05 |
| https://arxiv.org/abs/2603.24800 | Calibri: Enhancing Diffusion Transformers via Parameter-Efficient Calibration | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:calibri`, Thread `calibri`, 1 datiertes Ereignis vom 2026-03-29 → 2026-03-29.
- **Praktischer Hinweis:** Ab dem 2026-03-29 sollten Praktiker die verlinkte Projektseite, das Repository und die Hugging-Face-Collection als Ausgangspunkte für die Evaluierung von Calibri nutzen; genaue Versions- und Nutzungshinweise bleiben unverifiziert.
- **Konfidenz:** hoch. Die datierten Überholungsangaben oben sind maßgeblich dafür, was veraltet ist.
