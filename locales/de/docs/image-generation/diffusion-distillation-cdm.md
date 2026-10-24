---
title: "Continuous-Time Distribution Matching: Vertrag für Forschungs-Distillation"
description: "Continuous-Time Distribution Matching (CDM) ist eine Forschungsmethode für Few-Step-Diffusion-Distillation und kein Drop-in-Schalter für mehr Geschwindigkeit. Vor dem Einsatz sind Paper, Code, Checkpoint und Lizenz, Teacher- und Student-Parametrisierung sowie Schedule, Trainings- und verteilte Laufzeitumgebung, quellenabgetrennte Qualitäts-, Diversitäts- und Erhaltungsbewertung sowie rollback-fähige Serving-Nachweise verbindlich festzulegen."
category: optimization
tags: [cdm, diffusion-distillation, flow-matching, evaluation, serving, reproducibility]
aliases: ["CDM Diffusion Distillation", "Continuous-Time Distribution Matching Distillation"]
level: 2
source_sha256: 0fbde824bce9af395fb604845fb2b5070644a823afa67a41558afa63c5b0d5a6
translation: machine
translated_at: '2026-10-24'
---
# Continuous-Time Distribution Matching: Vertrag für Forschungs-Distillation {#continuous-time-distribution-matching-research-distillation-contract}

[Continuous-Time Distribution Matching](https://arxiv.org/abs/2605.06376)
ist eine Forschungsmethode für Few-Step-Diffusion-Distillation. Das Paper beschreibt
Continuous-Time Distribution Matching für die genannten experimentellen
Architekturen und verweist auf den Code. Es dient als Nachweis dafür, dieses
Release unter den dort genannten Bedingungen zu reproduzieren oder zu erweitern.
Es ist kein Versprechen für eine bestimmte Schrittzahl, Beschleunigung,
Qualitätsstufe, GPU-Topologie oder Kompatibilität mit einem anderen Teacher-Modell.

## Teacher, Student und Trajektorie festlegen {#bind-teacher-student-and-trajectory}

Für jedes Experiment sind folgende Angaben festzuhalten:

- Paper-Version, Code-Commit, Checkpoint- bzw. Artefakt-Identifikatoren und
  Digests, Lizenz- und Zugangsbedingungen, Framework- und Dependency-Revisionen
  sowie Protokoll der verteilten Laufzeit und Hardware;
- Teacher- und Student-Parametrisierung, Konditionierungspfad, Vorhersageziel,
  Noise- bzw. Trajektorien-Schedule, Verlustzweige und Gewichtungen,
  Datenpipeline, Seeds sowie Checkpoint- und Resume-Richtlinie;
- ein quellenabgetrennter Evaluationsdatensatz mit Messungen für Aufgabenqualität,
  Diversität, Erhaltung nicht zielbezogener Inhalte, Sicherheit und Rechte,
  Reproduzierbarkeit und Fehlerverhalten;
- vergleichbare Baseline-Läufe mit derselben Prompt- bzw. Eingabeverteilung,
  Ausgabeauflösung, Inferenzumgebung, Warm- bzw. Steady-State-Latenz,
  Durchsatz, Speicherbedarf und Fehlerrichtlinie; sowie
- Serving-Artefakt und -Version, Rollback-Ziel, Herkunftsnachweis der Ausgaben,
  Monitoring und Release-Entscheidung.

Wer Teacher, Basisarchitektur, Scheduler, Konditionierungsvertrag oder die
verteilte Implementierung ändert, verändert das Distillationsproblem. Ein
Adapter-Interface, ein Schedule, ein Verlustzweig oder ein veröffentlichtes
Ergebnis aus einer anderen Modellfamilie darf ohne explizite Implementierung
und gemessene Validierung nicht übernommen werden.

## Beschleunigung getrennt von der Ausgabevertrauenswürdigkeit bewerten {#evaluate-acceleration-separately-from-output-trust}

Few-Step-Ausgaben sind mit dem deklarierten Teacher und mit der Baseline für
die angeforderte Aufgabe zu vergleichen. Geschwindigkeit und Kosten sind getrennt
von Treue, Diversität, Text- bzw. Geometrieerhaltung und Artefaktrate zu
berichten. Ein optisch überzeugendes Sample belegt nicht, dass ein Student
Quellfakten erhält, auf einer neuen Prompt-Verteilung konsistent arbeitet oder
sicher ausgeliefert werden kann.

Checkpoints und Ausgabe-Lineage müssen so vollständig erhalten bleiben, dass
eine fehlgeschlagene Evaluation erneut ausgeführt oder ein ausgerollter Student
zurückgesetzt werden kann. Ein Trainingslauf, der vorzeitig abbricht, die
Herkunftsnachweise verliert oder seine Evaluation nicht reproduzieren kann,
bleibt unvollständig.

## Grenze bei Fehlern {#failure-boundary}

Fehlt der Teacher-Student-Vertrag, fehlen Code oder Artefakte, ist die Lizenz
ungeklärt, fehlt die quellenabgetrennte Evaluation oder der Rollback-Pfad, bleibt
CDM im Forschungsstatus. Ein anderes Distillationsverfahren darf dann nicht als
Ersatz eingesetzt, kein ungemessener Checkpoint veröffentlicht und kein schnellerer
Sampler nicht als gleichwertiges CDM-Ergebnis beworben werden.

## Verwandte Seiten {#related-pages}

- [[flow-matching]]
- [[diffusion-inference-acceleration]]
- [[MMDiT]]
- [[diffusion-lora-training]]
