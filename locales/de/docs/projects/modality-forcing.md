---
title: "Modality Forcing — Tiefenvorhersage"
category: projects
date: 2026-06-15
tags: [depth-prediction, depth_prediction, modality-forcing, project]
aliases: ["Modality Forcing"]
level: 2
source_sha256: d469bcbca0989b9a33f26b2cfa793d884c94cbd61561d158291d0decf3ebbd70
translation: machine
translated_at: '2026-10-24'
---
# Modality Forcing — Tiefenvorhersage {#modality-forcing-depth-prediction}

**Entwicklungslinie:** `project:modality-forcing` · Strang `depth-prediction`  
**Letztes Ereignis:** 2026-06-15 · 1 datiertes seit 2026-06-15 · **Recherchiert:** 2026-09-08 · Konfidenz: mittel

## Was es ist {#what-it-is}

Modality Forcing ist ein Post-Training-Rezept und ein veröffentlichter BF16-FluxRGBD-Checkpoint für Anwender, die ein einziges Modell für Text-zu-RGB-D, Bild-zu-relativer-Tiefe oder Tiefe-zu-Bild benötigen.

- Erzeugung von Text-zu-RGB, Tiefe und Punktwolke: gemeinsame Erzeugung in einem Durchlauf.
- Bild-zu-Tiefe: Vorhersage der relativen Tiefe aus einem Bild.
- Tiefe-zu-Bild: RGB-Erzeugung aus Tiefe und Text.

Der veröffentlichte Checkpoint ist flux_rgbd_9b_v2, insgesamt 12B Parameter mit einem separaten Qwen3-8B-Encoder; seine Tiefe ist relativ und keine kalibrierte metrische Tiefe. Er eignet sich für RGB-D-Experimente und Asset-Workflows, nicht für Metrologie oder kommerziellen Einsatz unter der Lizenz der öffentlichen Gewichte.

## Entwicklungslinie {#development-line}

- **2026-06-15 — Ressourcen zur Tiefenvorhersage von Modality Forcing wurden verlinkt.** Am 2026-06-15 verband ein datierter Verweis die Projektseite, das Quell-Repository, den Hugging-Face-Space und die Hugging-Face-Modellseite von Modality Forcing. Dies ist ein wesentlicher öffentlicher Bezugspunkt für die Entwicklungslinie der Tiefenvorhersage des Projekts, auch wenn die angegebenen Links weder einen bestimmten Release, eine Version noch ein technisches Ergebnis belegen.

## Was sich geändert hat {#what-changed}

- 2026-06-11 — arXiv v1 stellte das Post-Training-Rezept von Modality Forcing vor: ein DiT mit unabhängig verrauschten RGB- und Tiefenströmen für gemeinsame RGB-D-, Bild-zu-Tiefe- und Tiefe-zu-Bild-Inferenz.
- 2026-06-12 — bartduis/modality_forcing stellte in seinem ersten öffentlichen Release die öffentlichen flux_rgbd_9b_v2-Gewichte, die FLUX.2-Autoencoder-Dateien, die Modellkarte und den Anwendungsweg bereit.
- 2026-06-15 — Die verfügbaren Primärquellen datieren das Paper und das erste öffentliche Modellartefakt auf den 11. bis 12. Juni und benennen kein separates technisches Release an diesem Datum.

## So wird es verwendet {#how-to-use-this}

1. Prüfen Sie zuerst Checkpoint und Lizenz: bartduis/modality_forcing ist das Standardmodell; die veröffentlichten Gewichte stehen unter CC BY-NC 4.0.
  — <https://huggingface.co/bartduis/modality_forcing>
2. Klonen Sie das Repository, verwenden Sie Python 3.10+ und eine CUDA-GPU mit mindestens 48 GB Speicher, installieren Sie genau ein uv-CUDA-Extra, das zum Treiber passt, und prüfen Sie anschließend torch.cuda.is_available().
  — <https://github.com/Duisterhof/modality-forcing>
3. Führen Sie uv run scripts/joint.py --prompt "..." aus, um ein RGB-Bild, eine Tiefenkarte und eine farbige Punktwolke nach outputs zu schreiben.
  — <https://github.com/Duisterhof/modality-forcing>
4. Verwenden Sie scripts/i2d.py mit einem Bild für relative Tiefe oder scripts/d2i.py mit einer .npy- oder 16-Bit-Einkanal-Tiefenkarte sowie Text, um RGB zu erzeugen.
  — <https://github.com/Duisterhof/modality-forcing>
5. Behandeln Sie depth_raw.npy und die exportierte Punktwolke als Ausgabe mit relativem Maßstab; verwenden Sie die Tiefenkarte für Komposition oder Visualisierung, nicht für kalibrierte Messungen.
  — <https://github.com/Duisterhof/modality-forcing>

## Bewährte Praktiken {#best-practices}

- Wählen Sie ein treiberkompatibles PyTorch-Extra und prüfen Sie die GPU-Sichtbarkeit; ein bloßes uv sync lässt PyTorch aus.
  — <https://github.com/Duisterhof/modality-forcing>
- Belassen Sie den veröffentlichten Checkpoint bei seiner Trainingsauflösung von 512 Pixeln; vermeiden Sie nicht-quadratische lokale Eingaben für Bild-zu-Tiefe, wenn Strecken die Geometrie verändern würde.
  — <https://github.com/Duisterhof/modality-forcing>
- Verwenden Sie torch.compile nur für wiederholte lokale Sampling-Läufe: Der erste Lauf verursacht Kompilierungskosten, danach werden gecachte Kernel wiederverwendet.
  — <https://github.com/Duisterhof/modality-forcing>
- Behandeln Sie die Tiefe aus Bild-zu-Tiefe und Tiefe-zu-Bild als relativen Maßstab; leiten Sie daraus keine metrischen Distanzen aus den Rohwerten oder Punktwolken ab.
  — <https://github.com/Duisterhof/modality-forcing>
- Bei eigenen Denoising-Trajektorien sollten Sie RGB vor Tiefe priorisieren, wenn Tiefenkonsistenz das Ziel ist; das Paper berichtet für diese Richtung eine bessere Tiefenqualität.
  — <https://arxiv.org/html/2606.13676v1>

## Durch dies ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Der private Wortlaut des Ereignisses vom 2026-06-15 ist nicht verfügbar; daher lässt sich die beabsichtigte Aussage nicht rekonstruieren, weder als Paper-Ankündigung noch als Verweis auf ein Artefakt-Release.
- Das aktuelle Repository-README rundet den kontrollierten Skalierungsbereich auf 300M–3B, während arXiv v1 370M–3,3B angibt; keine der Quellen erklärt, ob es sich um Rundung oder eine Überarbeitung handelt.
- Die Genauigkeitsangaben stammen aus der Evaluation der Autoren in arXiv v1; eine unabhängige Validierung für Produktion, metrische Tiefe, Videokonsistenz oder Durchsatz wurde nicht gefunden.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://arxiv.org/html/2606.13676v1 | Modality Forcing for Scalable Spatial Generation (arXiv v1) | 2026-09-08 |
| https://huggingface.co/bartduis/modality_forcing/commit/1da410587ea9f76d3b56602af625cd77b0e650ba | Initial public release · bartduis/modality_forcing at 1da4105 | 2026-09-08 |
| https://huggingface.co/bartduis/modality_forcing | bartduis/modality_forcing · Hugging Face | 2026-09-08 |
| https://github.com/Duisterhof/modality-forcing | Duisterhof/modality-forcing · GitHub | 2026-09-08 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:modality-forcing`, Strang `depth-prediction`, 1 datiertes Ereignis 2026-06-15 → 2026-06-15.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Verwendung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
