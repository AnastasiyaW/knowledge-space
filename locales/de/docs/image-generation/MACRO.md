---
title: "MACRO: Strukturierte Bilddaten mit mehreren Referenzen"
description: "MACRO ist ein strukturierter Multi-Referenz-Datensatz, ein Benchmark und eine Sammlung modellspezifischer Feinabstimmungsressourcen; prüfen Sie vor dem Einsatz das kompatible Basismodell und die Bedingungen für die Artefakte."
category: models
tags: [multi-reference, dataset, benchmark, fine-tuning, bagel, omnigen2, qwen-image-edit]
aliases: ["MACRO-400K", "MacroData", "MacroBench"]
level: 2
source_sha256: 365e6eba5a7196a54c3f78e12a0b5b90f785e06c664b113509069d2be325e862
translation: machine
translated_at: '2026-10-24'
---
# MACRO: Strukturierte Bilddaten mit mehreren Referenzen {#macro-structured-multi-reference-image-data}

**Stand der Prüfung: 2026-09-04.** MACRO ist eine Forschungsveröffentlichung zur Bildgenerierung mit mehreren Referenzen und keine neue universelle Inferenzarchitektur. Die Autoren veröffentlichen strukturierte Daten, einen Benchmark, Trainingsmaterial und Checkpoints für ausgewählte offene Modelle, damit ein System lernen kann, mehr als ein Referenzbild zu nutzen, ohne sich ausschließlich auf Trainingsbeispiele mit kurzem Kontext zu stützen.

## Was veröffentlicht wird {#what-is-released}

Das Projekt beschreibt eine Datenveröffentlichung mit `400K` Samples und bis zu zehn Referenzbildern pro Sample. Es ordnet die Beispiele vier sich ergänzenden Aufgabenfamilien zu:

| Aufgabenfamilie | Was die Referenzen liefern sollen |
|---|---|
| Customization | Motive, Identität, Objekte oder visuelle Attribute |
| Illustration | multimodaler Kontext für eine gewünschte Komposition |
| Spatial | Blickwinkel, Geometrie oder Beziehungen innerhalb einer Szene |
| Temporal | visueller Zustand über die Zeit |

`MacroBench` evaluiert diese Szenarien, und das Repository stellt modellspezifische Pfade für Bagel, OmniGen2 und Qwen-Image-Edit bereit. Die Daten und der Benchmark bilden eine nützliche Evaluationsgrundlage; sie belegen jedoch nicht, dass ein beliebiges Modell zehn Bilder akzeptiert oder jede Referenz getreu erhält.

## Einen kompatiblen Weg wählen {#choose-a-compatible-route}

Verwenden Sie genau den Ablauf, den das Projekt pflegt:

1. wählen Sie ein unterstütztes Basismodell und dessen dokumentierte Revision;
2. folgen Sie der Vorverarbeitung, dem Auflösungsbudget, der Prompt-Syntax und dem Pfad zum Laden des Checkpoints dieses Modells;
3. verwenden Sie den passenden MACRO-Checkpoint oder die passende Trainingskonfiguration, statt Adapterformate zu mischen;
4. führen Sie einen Vergleichslauf mit dem unveränderten Basismodell für dieselbe Aufgabenvorlage durch.

Die Anzahl der Referenzen verändert das Bild-Token-Budget. Die Implementierung von MACRO reduziert die Auflösung der Eingabebilder dynamisch, je mehr Referenzen übergeben werden. Wenden Sie kein festes Pixelbudget aus einem älteren Tutorial auf ein anderes Basismodell an; prüfen Sie die aktuelle Konfiguration und messen Sie, ob kritische Details die Größenanpassung überstehen.

## Die reale Aufgabe evaluieren {#evaluate-the-real-task}

Die Generierung mit mehreren Referenzen hat mehrere voneinander unabhängige Fehlerarten: Vermischung von Motiven, verlorene kleine Details, falsche Beziehungen, selektives Kopieren und ein plausibel wirkendes, aber nicht getreues Ergebnis. Erstellen Sie eine Abnahmevorlage, die festlegt, welche Referenz welches Ergebnismerkmal steuert, und prüfen Sie die Ausgabe anhand dieser Zuordnung.

MacroBench verwendet einen auf LLMs basierenden Bewertungsablauf. Er kann ein reproduzierbares Forschungssignal liefern, ersetzt aber weder die manuelle Prüfung noch Rechteprüfungen oder aufgabenspezifische Validatoren in einem Produktivbetrieb. Bewahren Sie bei jedem Vergleich Prompts, Eingabereihenfolge, Modellrevision, gegebenenfalls den Zufalls-Seed und die erzeugten Artefakte auf.

## Daten, Rechte und Veröffentlichungsbedingungen {#data-rights-and-release-terms}

Das Projekt dokumentiert eine Pipeline zur Datenerstellung und stellt veröffentlichte Artefakte bereit. Herkunft und Bedingungen jeder Eingabe, jedes Basismodells, jedes Checkpoints und jeder nachgelagerten Ausgabe bleiben jedoch getrennte Fragen. Insbesondere gilt:

- Lesen Sie die Lizenz und die Modellkarte für das gewählte Basismodell und das MACRO-Artefakt;
- prüfen Sie, ob der vorgesehene Einsatz und die Weitergabe erlaubt sind;
- verwenden Sie nur Referenzbilder, zu deren Verarbeitung der Betreiber berechtigt ist;
- leiten Sie aus der Verfügbarkeit des Repositorys keine kommerzielle Erlaubnis für jede Komponente ab.

## Referenzen {#references}

- [MACRO official repository](https://github.com/HKU-MMLab/Macro)
- [MACRO paper](https://arxiv.org/abs/2603.25319)
- [MACRO project page](https://macro400k.github.io/)
