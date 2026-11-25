---
title: "Step1X-Edit: bildbearbeitung releasespezifisch"
description: "Step1X-Edit ist eine multimodale Bildbearbeitungsfamilie von StepFun mit releasespezifischen Pipelines; ordnen Sie jeden Checkpoint seinem dokumentierten Diffusers-Branch zu und prüfen Sie Modell- und Artefaktbedingungen unabhängig."
category: models
tags: [image-editing, step1x, stepfun, multimodal, diffusion, lora, gedit-bench]
aliases: ["Step1X-Edit"]
level: 3
source_sha256: 7f65df47c40baaae86eb2bd4337af8f539abfefe2dd5f204e1f372ce4d221037
translation: machine
translated_at: '2026-10-24'
---
# Step1X-Edit: Bildbearbeitung releasespezifisch {#step1x-edit-release-specific-image-editing}

**Stand der Prüfung: 2026-09-04.** Step1X-Edit ist die offene Forschungs- und Modellfamilie für Bildbearbeitung von StepFun. Der veröffentlichte Ansatz verwendet ein multimodales Sprachmodell, um ein Referenzbild und eine Bearbeitungsanweisung zu verarbeiten, und koppelt die daraus entstehende latente Repräsentation an einen Diffusions-Bilddecoder. Es handelt sich um einen Bildbearbeitungs-Stack, nicht um eine generische Kompatibilitätsschicht für beliebige Bildmodelle.

## Jedes Release als eigenes Integrationsziel behandeln {#treat-each-release-as-its-own-integration-target}

Das aktuelle Upstream-Repository dokumentiert das ursprüngliche Modell zusammen mit neueren Releases `v1p1` und `v1p2`. Die lokale Laufzeitumgebung hängt ausdrücklich vom Release ab: Upstream benennt für verschiedene Checkpoints unterschiedliche Pipeline-Klassen und unterschiedliche Diffusers-Branches. Wählen Sie Model Card, Repository-Revision, Abhängigkeits-Branch und Beispiel für ein Release als eine zusammengehörige Kompatibilitätseinheit aus.

Schließen Sie nicht daraus, dass das Bearbeitungsmodell eines anderen Anbieters eine Variante von Step1X-Edit ist, nur weil beide multimodale Konditionierung oder Diffusion verwenden. Insbesondere sind die Qwen-Releases für Bildbearbeitung eigenständige Artefakte mit eigenen Pipelines und Bedingungen.

## Was das offizielle Projekt bereitstellt {#what-the-official-project-provides}

Das offizielle Repository liefert:

- lokale Inferenzbeispiele für dokumentierte Releases;
- Modellartefakte und eine GEdit-Bench-Evaluierungsressource;
- Fine-Tuning-Skripte und einen Beispielpfad für LoRA beim ursprünglichen Modell;
- optionale Performance-Integrationen und Community-Integrationen, jeweils mit eigener Kompatibilitätsgrenze.

Das Projekt unterscheidet außerdem ein neueres, auf Schlussfolgerungen ausgerichtetes Release von früheren Varianten. Deshalb ist ein versionsunabhängiges Inferenzrezept unsicher: Eine Pipeline, die für einen Checkpoint importiert wird oder läuft, ist kein Beleg dafür, dass sie für einen anderen korrekt ist.

## Sicherer Integrationsvertrag {#safe-integration-contract}

1. Wählen Sie genau einen Step1X-Edit-Checkpoint und lesen Sie dessen aktuelle Model Card sowie das passende Upstream-Beispiel.
2. Erstellen Sie die Umgebung aus dem entsprechenden dokumentierten Abhängigkeits-Branch; halten Sie den Repository-Commit und die Paketversionen fest.
3. Beginnen Sie mit einem kleinen Bild, für dessen Verwendung die Rechte geklärt sind, und einer expliziten Bearbeitungsanweisung. Bewahren Sie die unveränderte Eingabe auf.
4. Protokollieren Sie den Checkpoint-Digest, die Pipeline-Klasse, den Prompt, den Seed, sofern verfügbar, die Digests von Ein- und Ausgabe sowie alle aktivierten optionalen Module.
5. Testen Sie eine zurückgehaltene Testdatei sowohl auf die gewünschte Änderung als auch auf die Merkmale, die unverändert bleiben müssen.

Beim Fine-Tuning oder Laden eines LoRA ist es an genau das Basis-Release, die Zielmodule und den Ladepfad gebunden, mit dem es erzeugt wurde. Eine erfolgreich geladene Datei ist kein Nachweis für semantische Kompatibilität oder Erhaltungsqualität.

## Bearbeitung bewerten, nicht eine Demo-Aussage {#evaluate-editing-not-a-demo-claim}

Verwenden Sie getrennte Abnahmeprüfungen:

| Frage | Nachweis |
|---|---|
| Wurde die gewünschte Bearbeitung vorgenommen? | aufgabenspezifische visuelle Prüfung gegen die Anweisung |
| Blieb geschützter Inhalt intakt? | Vergleich nebeneinander von Gesichtern, Text, Logos, Geometrie und Produktdetails |
| Ist das Ergebnis reproduzierbar? | unveränderliche Umgebung, Modellrevision, Prompt, Seed sowie Beleg für Ein- und Ausgabe |
| Ist ein Benchmark anwendbar? | das deklarierte GEdit-Bench-Protokoll, nicht ein auf eine andere Aufgabe übertragener Wert |

Bei quellentreuer Arbeit, etwa bei Produktidentität, Dokumenten, Beweismitteln oder Messungen, ist ein bearbeitetes Bild ein abgeleitetes Artefakt. Behalten Sie das Original als maßgebliche Quelle.

## Bedingungen und Grenzen des Einsatzes {#terms-and-deployment-boundary}

Die Lizenz des Repositorys, die Checkpoint-Lizenz, die Bedingungen hostbarer Dienste, die Basisabhängigkeiten, die Trainingsdaten und die Rechte an Eingabebildern können sich voneinander unterscheiden. Prüfen Sie vor kommerziellem oder gehostetem Einsatz die aktuellen Bedingungen für jedes tatsächlich verwendete Artefakt; ein Kennzeichen auf Familienebene kann diese Prüfung nicht ersetzen.

## Referenzen {#references}

- [Step1X-Edit offizielles Repository](https://github.com/stepfun-ai/Step1X-Edit)
- [Step1X-Edit technischer Bericht](https://arxiv.org/abs/2504.17761)
- [Step1X-Edit Modellsammlung](https://huggingface.co/stepfun-ai/Step1X-Edit)
