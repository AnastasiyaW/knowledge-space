---
title: "Rekurrent-Tiefe-Transformer: Laufzeit-Evidenzvertrag"
description: "Rekurrent-Tiefe-Transformer verwenden einen versionsspezifischen gemeinsamen Block über mehrere Iterationen hinweg; binde die veröffentlichte Architektur, den Checkpoint und die Laufzeit, das Rekurrenzbudget, das Cache- und Terminierungsverhalten sowie die gemessene Qualität und Kosten, und leite latentes Schlussfolgern, frühes Beenden, Stabilität oder Einsatzfähigkeit nicht aus dem Familiennamen ab."
category: techniques
tags: [recurrent-depth, transformers, recurrence, inference, evaluation, runtime, evidence]
aliases: ["Recurrent-Depth Transformer", "RDT Architecture", "Looped Transformer"]
level: 3
source_sha256: 40d8d9b1eb3e810e0c17f3dd0689061488ab91cc98471908fad6261f853fe260
translation: machine
translated_at: '2026-10-24'
---
# Rekurrent-Tiefe-Transformer: Laufzeit-Evidenzvertrag {#recurrent-depth-transformer-runtime-evidence-contract}

Rekurrent-Tiefe-Transformer ist ein Familienname und kein standardisierter Checkpoint oder keine standardisierte Serving-Schnittstelle. Die definierende Idee ist die Wiederverwendung einer gemeinsamen Berechnung über mehrere Iterationen, doch die Anordnung der Blöcke, die Eingabeeinspeisung, das Gating, das Cache-Layout, die Stoppbedingung, das Trainingsverfahren und die unterstützten Rekurrenztiefen gehören zu einer bestimmten Implementierung.

## Architektur festlegen, bevor man sie diskutiert {#bind-the-architecture-before-discussing-it}

Eine veröffentlichte Anordnung lässt sich so zusammenfassen:

`input → prelude → shared recurrent core repeated r times → coda → logits`

[Scaling up Test-Time Compute with Latent Reasoning](https://arxiv.org/abs/2502.05171)
beschreibt ein Design aus Prelude, gemeinsamem Kern und Coda. Ein neueres
[Gated Recurrent Transformers paper](https://arxiv.org/abs/2608.15062) zeigt ein anderes,
gegatetes rekurrentes Design. Keine der beiden Quellen belegt, dass alle „RDT“-Modelle
dieselbe Update-Regel, Adapter, Mixture-of-Experts-Schichten, denselben Aufmerksamkeitsmechanismus,
dieselbe Stabilitätsbedingung oder dasselbe Verhalten beim frühen Beenden besitzen.

Für eine konkrete Veröffentlichung sind festzuhalten:

- Paper-/Code-Release, Checkpoint-Digest, Lizenz, Tokenizer, Präzision,
  Laufzeit/Backend und alle nicht-standardmäßigen Patches;
- die genaue Zusammensetzung aus Prelude, Kern und Coda, ob die Kernparameter gebunden sind,
  die Richtlinie für Eingabeeinspeisung/Gating und die unterstützten Rekurrenzwerte;
- Cache-Format, Batching-Richtlinie, Determinismus, Implementierung von Terminierung/frühem Beenden,
  Fehlerverhalten und die Quelle des gewählten Rekurrenzbudgets;
- Evaluationskorpus/Split, Prompt-/Template-Richtlinie, Qualitätsmetriken, Sicherheitstests und Baseline; sowie
- gemessene Latenz, Speicherbedarf, Durchsatz und Ausgabeänderungen bei jeder veröffentlichten
  Rekurrenzeinstellung auf der eingesetzten Hardware.

## Rekurrenz als gemessene Steuergröße behandeln {#treat-recurrence-as-a-measured-control}

Mehr Iterationen erhöhen den Rechenaufwand, verbessern aber nicht universell jede Aufgabe.
Eine Änderung von `r` kann Qualität, Latenz, Speicherdruck, Batch-Packing und die
Verteilung der Fehler verändern. Ein Deployment darf nur jene Tiefenwerte anbieten, auf
denen das Modell trainiert und getestet wurde. Extrapoliere keine beliebige Schleifenanzahl aus
einem Paper-Diagramm und nimm nicht an, dass ein gemeinsamer Kern über den dokumentierten
Laufzeitbereich hinaus stabil ist.

Vergleiche Rekurrenzeinstellungen auf einem quellenseitig disjunkten Evaluationsset und halte
die vollständige Qualitäts-/Kostenkurve fest. Berichte Fehlschläge, nicht nur den besten Punkt.
Wird frühes Beenden beansprucht, evaluiere dessen Exit-Entscheidung und die finalen Ausgaben
gegen die Baseline mit voller Tiefe für das genannte Release; leite es nicht aus der
gemeinsamen Gewichtung rekurrenter Schichten ab.

## Latente Berechnung nicht überbewerten {#do-not-overstate-latent-computation}

Wiederholte Aktualisierungen des verborgenen Zustands sind keine sichtbare Gedankenkette, keine
Erklärung, kein Beleg für Schlussfolgerungen und keine Inspektionsschnittstelle. Behaupte nicht,
latente Schritte entsprächen einer bestimmten Anzahl geschriebener Begründungsschritte, ihre
Inhalte seien interpretierbar oder verborgene Berechnung mache ein Modell sicher. Bewerte
Ausgaben und deklarierte Steuerungen direkt.

## Grenze des Serving {#serving-boundary}

Ein Rekurrent-Tiefe-Modell darf erst dann eingesetzt werden, wenn die tatsächliche Laufzeit das
benannte Artefakt laden, das angeforderte Rekurrenz-/Cache-Verhalten beibehalten und unter
Last die gemessenen Ausgaben erzeugen kann. Ein generischer Transformer-Server, ein quantisierter
Checkpoint oder ein Adapter-Loader gilt nicht als kompatibel. Melde einen Fehler, wenn das
Rekurrenzbudget, die Cache-Richtlinie oder die Artefaktidentität nicht verifiziert werden
kann; führe niemals stillschweigend ein dichtes Ersatzmodell oder eine nicht spezifizierte Tiefe aus.

## Verwandte Seiten {#related-pages}

- [[low-vram-inference-strategies]]
- [[tiled-inference]]
- [[diffusion-lora-training]]
