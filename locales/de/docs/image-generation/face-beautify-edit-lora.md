---
title: "Face-Edit-LoRA: Gepaarte lokale Korrekturen"
description: "Ein Face-Edit-LoRA ist eine gepaarte, einwilligungsbewusste Trainingsaufgabe für lokale Bearbeitungen. Binde den Adapter an sein exaktes Basismodell und validiere die gewünschte Korrektur getrennt von der Identitätserhaltung."
category: workflows
tags: [lora, image-editing, paired-data, face, consent, evaluation, privacy]
aliases: ["Face Beautify Edit LoRA", "Face Correction LoRA"]
level: 2
source_sha256: b0117e88e78687687f078de6f633bbe0aab2485c1006a0a9c5701c7342b4d8fb
translation: machine
translated_at: '2026-10-24'
---
# Face-Edit-LoRA: Gepaarte lokale Korrekturen {#face-edit-lora-paired-local-corrections}

Ein Face-Edit-Adapter sollte eine eng begrenzte, gewünschte Korrektur lernen und nicht eine umfassende Definition von „Schönheit“. Definiere die Bearbeitung in operativer Sprache, zum Beispiel: ein geschlossenes Auge wieder öffnen, wobei Pose, Beleuchtung und Identität erhalten bleiben. Benenne außerdem, was der Adapter nicht verändern darf.

## Vertrag für gepaarte Daten {#paired-data-contract}

Jeder Trainingsdatensatz benötigt ein nachprüfbares Quellbild, ein Zielbild, eine Bearbeitungsanweisung und einen Herkunftsnachweis (Provenienz). Quell- und Zielbild sollten sich, soweit praktikabel, nur in der freigegebenen Korrektur unterscheiden. Bewahre Folgendes auf:

- eine Einwilligung oder ein dokumentiertes Recht, das Paar zu trainieren und daraus abzuleiten;
- Digests von Quell- und Zielbild, Aufnahme- bzw. Generierungsprovenienz und Bearbeitungshistorie;
- die beabsichtigte lokale Änderung sowie die geschützten Bereiche oder Merkmale, die erhalten bleiben müssen;
- Ausschlussgründe für mehrdeutige, übermäßig bearbeitete oder qualitativ schwache Beispiele; und
- die Richtlinie zu Aufbewahrung und Zugriff für biometrisch sensibles Material.

Synthetische Degradationen können einen Datensatz nur dann erweitern, wenn ihr Generator, ihre Anweisungen und die Abnahmeprüfung dokumentiert sind. Sie ersetzen keine repräsentativen gepaarten Beispiele, und sie dürfen keine verdeckte Identitäts- oder Stiländerung in das Zielbild einbringen.

## Den Adapter an einen Modellvertrag binden {#bind-the-adapter-to-one-model-contract}

Ein Adapter ist nicht allein deshalb portabel, weil zwei Werkzeuge ihn als LoRA bezeichnen. Bewahre zusammen mit dem Artefakt den exakten Basis-Checkpoint bzw. Revisionsstand, die Pipeline, Text-Encoder, VAE, das Adapterformat, die Zielmodule, den Auflösungs- und Zuschnittpfad, den Optimierer und die Trainingskonfiguration auf.

[ai-toolkit](https://github.com/ostris/ai-toolkit) stellt gepflegte Beispielkonfigurationen für Fine-Tuning bereit. Beginne mit dem aktuellen Beispiel für das gewählte Basismodell, nimm nur die minimal dokumentierten Änderungen vor und speichere die exakte Konfiguration zusammen mit dem resultierenden Adapter. Ein Toolkit-Beispiel legt eine Ausführungsroute fest; es belegt jedoch kein allgemeines Ergebnis für Gesichtsbearbeitung mit einem anderen Modell oder Datensatz.

## Korrekt aufteilen und validieren {#split-and-validate-correctly}

Teile die Daten vor der Augmentierung nach Person, Quelle oder Aufnahmesitzung auf. Zufällige Aufteilungen auf Bildebene können nahezu identische Porträts in die Validierung einschleusen und lassen einen Adapter besser erscheinen, als er tatsächlich ist.

Evaluiere eine feste Bearbeitungssuite, die Folgendes enthält:

1. gewünschte lokale Korrekturen über verschiedene Bedingungen hinweg: Pose, Beleuchtung, wahrgenommenes Alter, Make-up und Bildqualität;
2. Negativ-Fixtures, bei denen der gewünschte Bereich unverändert bleiben muss;
3. Prüfungen zur Erhaltung von Identität, Pose, Beleuchtung und Hintergrund; und
4. Fehler-Fixtures, die abgelehnt statt aggressiv bearbeitet werden sollten.

Berichte den Score der gewünschten Korrektur getrennt von den Ergebnissen zur Erhaltung und zur menschlichen Prüfung. Eine gelungene ästhetische Bearbeitung belegt für sich genommen weder die Erhaltung der Identität noch die Eignung für einen produktiven Workflow.

## Freigabe-Gate {#release-gate}

Veröffentliche vor einem Einsatz außerhalb eines Experiments eine Adapter-Karte mit der Modellbindung, dem Geltungsbereich von Daten und Rechten, dem zulässigen Bearbeitungsvokabular, bekannten Fehlerfällen, den Validierungs-Fixtures und einem Rollback-Pfad. Führe die Suite erneut aus, sobald sich das Basismodell, die Laufzeitumgebung, der Adapter-Loader oder der Umfang der gewünschten Bearbeitung ändert.

## Verwandte Seiten {#related-pages}

- [[lora-fine-tuning-for-editing-models]]
- [[diffusion-lora-training]]
- [[face-detection-filtering-pipeline]]
- [[anatomy-correction-diffusion]]
