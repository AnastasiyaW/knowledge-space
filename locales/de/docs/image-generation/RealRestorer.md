---
title: "RealRestorer: Generalisierbare Wiederherstellung realer Bilder"
description: "RealRestorer ist ein großer Workflow zur Bildrestaurierung auf Basis eines Bildbearbeitungsmodells für neun dokumentierte Degradationstypen; verwenden Sie die gepatchte lokale Laufzeitumgebung des Repositorys und bewerten Sie die Treue getrennt von Benchmark-Ergebnissen."
category: models
tags: [image-restoration, deblur, denoise, dehaze, derain, compression-artifacts, low-light, moire, flare, reflection]
aliases: ["RealRestorer", "RealIR-Bench"]
level: 2
source_sha256: 6490d45ffa0b5fbf0d429f33258786396337969b1e43e72501f3f0fd3c1d7fe4
translation: machine
translated_at: '2026-10-24'
---
# RealRestorer: Generalisierbare Wiederherstellung realer Bilder {#realrestorer-generalizable-real-world-image-restoration}

**Stand der Prüfung: 2026-09-04.** RealRestorer ist ein veröffentlichter Workflow zur Bildwiederherstellung, der auf einem großen Bildbearbeitungsmodell aufbaut. Das Projekt kombiniert ein Modell, eine Pipeline zur synthetischen Erzeugung von Degradationen und Bewertungsmaterial von RealIR-Bench, um neun dokumentierte Degradationskategorien aus der Realwelt zu adressieren. Es handelt sich um einen Forschungs- und Engineering-Stack, nicht um eine generische `pip install`-Schnittstelle zur Bildwiederherstellung.

## Unterstützte Aufgabenklassen {#supported-task-classes}

Das aktuelle Repository dokumentiert promptgesteuerte Workflows für Unschärfe, Kompressionsartefakte, Linsenreflexe (Lens Flare), Moiré, Dunst, Bilder bei schlechten Lichtverhältnissen, Rauschen, Regen und Spiegelungen. Wählen Sie bewusst genau eine Aufgabenkategorie aus und speichern Sie den Aufgaben-Prompt zusammen mit dem Durchlauf; vage Anweisungen können ein Bildbearbeitungsmodell dazu verleiten, Inhalte über die Degradation hinaus zu verändern.

Unterscheiden Sie bei jedem Ergebnis Folgendes:

- Entfernung der angeforderten Degradation;
- Erhalt von Identität, Geometrie, Text und kleinen Produktdetails;
- neu erfundene Details, Glättung oder unerwünschte inhaltliche Veränderungen;
- visuelle Plausibilität im Gegensatz zu quellgetreuer Rekonstruktion.

Bei Dokumenten, Belegen, Produktidentität oder Messwerten gilt das Originalbild als maßgeblich. Ein generiertes Restaurierungsergebnis ist als abgeleitete Ausgabe zu kennzeichnen und anhand des Originals zu prüfen.

## Veröffentlichte Grenzen der Laufzeitumgebung {#published-runtime-boundary}

Der offizielle Schnelleinstieg setzt derzeit das gepatchte lokale `diffusers/`-Checkout voraus, das im RealRestorer-Repository enthalten ist. Dieses Checkout wird im Editable-Modus installiert, und vor der Inferenz wird geprüft, ob `RealRestorerPipeline` importiert werden kann. Es wird nicht vorausgesetzt, dass ein allgemein installiertes Diffusers-Wheel dieselbe Pipeline bereitstellt.

Beginnen Sie mit dem aktuellen Repository und dokumentieren Sie:

1. Repository-Commit, Revision des lokalen gepatchten Diffusers, Python-Umgebung und alle Digests der Modellartefakte;
2. Eingabebild, gewählte Degradationskategorie, Prompt, Seed, Präzision und Inferenzeinstellungen;
3. Ausgabebild und einen expliziten Vergleich mit der Quelle;
4. Fehlerprotokolle sowie einen Rückgriff auf das unveränderte Quellbild.

Das Repository stellt außerdem eine Pipeline zur synthetischen Erzeugung von Degradationen und Code zur Benchmark-Auswertung bereit. Halten Sie synthetische Testdaten von echten Produktionsbildern getrennt, damit ein Benchmark-Fixture nie als Nachweis im Live-Betrieb missverstanden wird.

## Benchmarks sind Evidenz, kein Freigabezertifikat {#benchmarks-are-evidence-not-a-release-certificate}

RealIR-Bench kombiniert ein wahrnehmungsbasiertes Distanzmaß mit einer VLM-basierten Bewertung zu seinem ausgewiesenen Ergebnis. Das kann einen wiederholbaren Vergleich innerhalb des deklarierten Benchmark-Aufbaus stützen, kann jedoch weder die Quelltreue für ein anderes Bild, die Lizenzkonformität noch die Korrektheit einer veröffentlichten Retusche belegen.

Verwenden Sie zusammen mit jedem Benchmark-Ergebnis einen aufgabenspezifischen Prüfsatz mit harten Erhaltungsprüfungen. Ist ein Abnahmekriterium „kein Logo, Gesicht, Gestein, Dokumententext oder Messwert darf verändert werden“, nehmen Sie es als explizites Fixture auf und prüfen Sie es in der Auflösung der Auslieferung.

## Lizenzierung und Bereitstellung {#licensing-and-deployment}

Code, gepatchte Abhängigkeiten, Modellgewichte, Benchmark-Daten, gehostete Demos und Artefakte der Basismodelle können jeweils eigene aktuelle Bedingungen haben. Prüfen Sie vor einer kommerziellen oder gehosteten Bereitstellung die genaue Lizenz des Repositorys und der Modellkarte, Zugriffsbeschränkungen, Weitergabebedingungen sowie die Rechte an den Eingabebildern. Leiten Sie eine Entscheidung zur kommerziellen Nutzung nicht aus einem einzelnen Metadaten-Tag ab.

## Referenzen {#references}

- [RealRestorer official repository](https://github.com/yfyang007/RealRestorer)
- [RealRestorer paper](https://arxiv.org/abs/2603.25502)
- [RealRestorer model collection](https://huggingface.co/RealRestorer/RealRestorer)
- [RealIR-Bench dataset](https://huggingface.co/datasets/RealRestorer/RealIR-Bench)
