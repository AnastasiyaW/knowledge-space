---
title: "Seoul World Model — Öffentliche Projektveröffentlichung"
category: projects
date: 2026-03-17
tags: [project, public-project-release, seoul-world-model]
aliases: ["Seoul World Model"]
level: 2
source_sha256: d50b3371a7fdeb72425cefacfce1bb8b4903e1112f86966eeabba123da7b9747
translation: machine
translated_at: '2026-10-24'
---
# Seoul World Model — Öffentliche Projektveröffentlichung {#seoul-world-model-public-project-release}

**Entwicklungslinie:** `project:seoul-world-model` · Thread `public-project-release`  
**Letztes Ereignis:** 2026-03-17 · 1 datiertes Ereignis seit 2026-03-17 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Seoul World Model (SWM) ist ein Forschungs-World-Model. Es erzeugt aus Koordinaten, Kameratrajektorien und Textskripten Routenvideos, indem es Street-View-Bilder von Seoul aus einem räumlichen Index abruft.

- Retrieval-augmentierte Konditionierung bewahrt die Geometrie der Orte und das visuelle Erscheinungsbild.
- Freie Kamerabewegung unterstützt beliebige Trajektorien und textuelle Szenenänderungen.
- Virtual Lookahead Sink verankert die Videogenerierung erneut an den kommenden Routenwegpunkten.

Stand 2026-09-05 sind Gewichte, Inferenzcode, synthetische Daten und Interpolationscode nicht veröffentlicht. Deshalb können wir es nicht deployen.

## Entwicklungslinie {#development-line}

- **2026-03-17 — Öffentliches Projekt und Code-Referenzen zu Seoul World Model erfasst.** Am 2026-03-17 veröffentlichte das Projekt Links zu einer öffentlichen Projektwebsite und einem GitHub-Repository und etablierte damit seine offizielle Präsentationsseite und sein Quell-Repository.

## Was sich geändert hat {#what-changed}

2026-03-17 — Seoul World Model wurde als offizielles Projekt für *Grounding World Simulation Models in a Real-World Metropolis* gestartet. Das Repository kündigte die spätere Veröffentlichung von Gewichten, Inferenzcode, synthetischen Daten und Werkzeugen zur Vorbereitung von Trainingsvideos an.

Ergänzung zum Ereignis vom 2026-03-17: Das Preprint vom 2026-03-16 benennt das System als Seoul World Model (SWM) und beschreibt es als Feinabstimmung eines vortrainierten Video-World-Models. Es nennt Trainingsdaten aus 440 Tausend Seoul-Street-View-Bildern, realen Fahrvideos und synthetischen Stadtdaten.
  — <https://arxiv.org/abs/2603.15583>

Neues Ereignis 2026-03-16: Die Autorinnen und Autoren veröffentlichten das Preprint *Grounding World Simulation Models in a Real-World Metropolis*. Die Arbeit definiert die Kernmethode: georeferenziertes Retrieval, zeitübergreifendes Pairing, synthetische Trajektorien und Virtual Lookahead Sink.
  — <https://arxiv.org/abs/2603.15583>

## Verwendung {#how-to-use-this}

Ab 2026-03-17 nutzen Sie die Projektwebsite von Seoul World Model und das verlinkte GitHub-Repository, um das Projekt zu bewerten, statt ungeprüfter Weiterverbreitungen.

1. Prüfen Sie das offizielle Repository, bevor Sie Experimente planen: Es stellt derzeit keine Modell-Downloads und keine Inferenzanleitung bereit.
  — <https://github.com/naver-ai/seoul-world-model>
2. Verwenden Sie die Projektseite und das Paper als Spezifikation für die Reproduktion der Forschung: Die Eingaben des Systems sind die geografische Ausgangsposition, die Kameratrajektorie, der Textprompt und lokale Street-View-Referenzen.
  — <https://seoul-world-model.github.io/>
3. Behaupten Sie keine Reproduzierbarkeit oder Produktionsreife, bevor die Autorinnen und Autoren Gewichte, Inferenzcode und Daten veröffentlichen.
  — <https://github.com/naver-ai/seoul-world-model>

## Best Practices {#best-practices}

- Messen Sie die Verankerung im Ort getrennt vom visuellen Realismus: In Ablationsstudien verringerte eine geringere Anzahl von Referenzbildern den mPSNR, auch wenn FID und FVD keine klare Verschlechterung zeigten.
  — <https://arxiv.org/abs/2603.15583>
- Holen Sie bei langen Routen Vorwärtsreferenzen entlang der Trajektorie ab, statt sich nur auf das Anfangsbild zu verlassen: Das folgt der Virtual-Lookahead-Sink-Methode aus dem Paper.
  — <https://arxiv.org/abs/2603.15583>
- Behandeln Sie eine angekündigte Veröffentlichung nicht als verfügbares Werkzeug: Das Repository vermerkt weiterhin, dass Gewichte und Code später folgen.
  — <https://github.com/naver-ai/seoul-world-model>

## Hiermit ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Das offizielle Repository enthält nur ein README und keine GitHub Releases. Die Autorinnen und Autoren haben keine Veröffentlichungstermine für Gewichte, Inferenzcode, synthetische Daten oder Interpolationscode angekündigt.
- Die Datensatzangaben widersprechen sich zwischen den Quellen. Die Projektseite nennt 1,2 Millionen Panoramen und 10 Tausend synthetische Videos, während das Paper 440 Tausend Street-View-Bilder für die Feinabstimmung angibt. Die Autorinnen und Autoren haben den aufbereiteten Datensatz und die genauen Trainingskonfigurationen nicht veröffentlicht.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://seoul-world-model.github.io/ | Seoul World Model: Grounding World Simulation Models in a Real-World Metropolis | 2026-09-05 |
| https://github.com/naver-ai/seoul-world-model | naver-ai/seoul-world-model | 2026-09-05 |
| https://github.com/naver-ai/seoul-world-model/releases | Releases · naver-ai/seoul-world-model | 2026-09-05 |
| https://arxiv.org/abs/2603.15583 | Grounding World Simulation Models in a Real-World Metropolis | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:seoul-world-model`, Thread `public-project-release`, 1 datiertes Ereignis 2026-03-17 → 2026-03-17.
- **Praktischer Hinweis:** Ab 2026-03-17 sollten Praktikerinnen und Praktiker die Projektwebsite von Seoul World Model zusammen mit dem verlinkten GitHub-Repository als Ausgangspunkt nutzen, um das Projekt zu bewerten und zu beziehen, statt sich auf eine ungeprüfte Weiterverbreitung zu verlassen.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
