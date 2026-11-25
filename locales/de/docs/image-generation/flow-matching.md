---
title: "Flow Matching: bedingtes Vektorfeld-Training"
description: "Flow Matching trainiert ein kontinuierliches Vektorfeld entlang eines gewählten Wahrscheinlichkeitspfads; Scheduler-, Pfad- und Inferenzeinstellungen sind checkpointspezifisch und keine universellen Diffusionsstandards."
category: architectures
tags: [flow-matching, conditional-flow-matching, scheduler, sampling, continuous-normalizing-flow, ode]
aliases: ["Flow Matching", "Rectified Flow", "Flow Matching Scheduler"]
level: 2
source_sha256: 13ab6140027142ed2d477d46684c7d5b47e39321fe353def17779be40b2a93fb
translation: machine
translated_at: '2026-10-24'
---
# Flow Matching: bedingtes Vektorfeld-Training {#flow-matching-conditional-vector-field-training}

[Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747)
beschreibt eine simulationsfreie Methode zum Trainieren kontinuierlicher Normalizing Flows (CNFs).
Anstatt während des Trainings den gelernten Fluss zu simulieren, regressiert das Modell
ein Vektorfeld auf einer gewählten Familie bedingter Wahrscheinlichkeitspfade.

Der Pfad ist entscheidend. Die ursprüngliche Formulierung kann Diffusionspfade und
Pfade im Stil des optimalen Transports abdecken; sie ist weder eine einzige universelle
geradlinige Interpolation noch eine feste Gleichung für jeden Checkpoint.

## Was die Inferenz integriert {#what-inference-integrates}

Bei der Inferenz startet eine kompatible Pipeline von ihrer konfigurierten Quellverteilung
und integriert das gelernte Vektorfeld numerisch in Richtung eines Samples. Der Solver,
der Zeitplan, die Konditionierung, das Guidance-Verfahren und die Anzahl der
Funktionsauswertungen sind Teil des Vertrags von Pipeline und Modell.

Leite nicht ab, dass jeder Flow-Matching-Checkpoint:

- dieselbe Scheduler-Klasse oder denselben Schedule-Shift akzeptiert;
- bei einer bestimmten Schrittzahl besser wird;
- eine bestimmte img2img-Strength-Abbildung unterstützt; oder
- seine eigene Ausgabe in wiederholten Durchgängen sicher verfeinern kann.

Solche Aussagen brauchen Belege des Checkpoint-Herausgebers und ein Ergebnis für die
vorgesehene Aufgabe.

## Scheduler-Kompatibilität {#scheduler-compatibility}

Diffusers stellt
[FlowMatchEulerDiscreteScheduler](https://huggingface.co/docs/diffusers/api/schedulers/flow_match_euler_discrete)
als eine Implementierung bereit. Die offengelegte Konfiguration umfasst Trainings-Timesteps,
Shift-Verhalten, dynamisches Shifting, Einstellungen zur Sequenzlänge und alternative
Sigma-Schedules. Diese Optionen beschreiben eine Implementierungsschnittstelle; sie sind
keine universellen Standardwerte, die man in ein anderes Flow-Modell übernehmen sollte.

Lade nach Möglichkeit den Scheduler und die Konfiguration, die mit dem Checkpoint veröffentlicht
wurden. Wenn ein Experiment Scheduler, Shift, Solver oder Schrittplan ändert, behandle es als
neuen Sampling-Vertrag und sichere ein reproduzierbares Ergebnis, bevor du es operativ einsetzt.

## Evaluierungsprotokoll {#evaluation-protocol}

Für jedes unterstützte Modell-/Pipeline-Paar:

1. dokumentiere Checkpoint, Revisionen von Pipeline und Scheduler, Eingabe-Fixture, Seed,
   Dimensionen, Guidance, Schritte sowie Gerät und Laufzeitumgebung;
2. erstelle ein kleines, unterstütztes Raster aus Schrittzahlen oder Schedule-Einstellungen;
3. vergleiche die Determinismus der Ausgabe, die aufgabenrelevante Treue, Artefakte und die Latenz;
4. prüfe die Erhaltung der Vorlage bei img2img oder Editing separat von der Qualität bei
   Text-to-Image; und
5. veröffentliche die ausgewählte Konfiguration zusammen mit ihrem Validierungs-Fixture und
   bekannten Grenzen.

Das ist besonders bei Restaurierung und Editing wichtig: Ein Bild kann polierter wirken, während
es sich von der Vorlage entfernt, Text verändert oder eine Materialeigenschaft verändert, die
erhalten bleiben muss.

## Verwandte Seiten {#related-pages}

- [[diffusion-inference-acceleration]]
- [[SANA]]
- [[flux-klein-9b-inference]]
- [[diffusion-lora-training]]
