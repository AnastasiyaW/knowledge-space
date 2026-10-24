---
title: "FLUX.2 [klein] Identity-LoRA: Einwilligungs- und Evaluierungsvertrag"
description: "Eine Identity-LoRA ist ein sensibler, versionsgebundener Adapter, der ausschließlich aus autorisierten Bildern für einen definierten Zweck trainiert wird; binden Sie Einwilligung, Basis-Checkpoint und Adapterformat, Daten- und Löschrichtlinie sowie eine quelltrennende Prüfung von Ähnlichkeit und Erhaltung, und behandeln Sie eine generierte Identitätsübereinstimmung niemals als verifizierte Identität."
category: techniques
tags: [lora, identity, consent, provenance, flux, klein, evaluation, privacy]
aliases: ["Klein Character LoRA", "Klein Identity LoRA", "Klein Person LoRA"]
level: 2
source_sha256: b31310c9912250a75883848c8a70b37b972de59e6cfbc6742773995021cf9829
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 [klein] Identity-LoRA: Einwilligungs- und Evaluierungsvertrag {#flux2-klein-identity-lora-consent-and-evaluation-contract}

Eine Identity- oder Character-LoRA ist kein gewöhnliches Stil-Preset. Sie ist ein
sensibler Adapter, der eine Person in neuen Kontexten erscheinen lassen kann.
Trainieren oder verwenden Sie eine solche LoRA nur für einen autorisierten Zweck,
mit einem klaren Widerrufs- bzw. Löschweg und mit einer Prüfung, die visuelle
Ähnlichkeit von verifizierter Identität unterscheidet.

## Befugnis vor der Datenvorbereitung klären {#establish-authority-before-data-preparation}

Dokumentieren Sie:

- die Autorisierung der abgebildeten Person, den erlaubten Zweck, die Dauer, die Offenlegung und einen Kontakt für den Widerruf;
- die Eigentumsverhältnisse an den Quellbildern, den Erhebungskontext und die zulässigen abgeleiteten Verwendungen;
- die Aufbewahrungs- und Löschrichtlinie für Originale, Beschriftungen, Zuschnitte, Masken, Adapter, Checkpoints, Vorschauen und Kopien beim Anbieter;
- ob Eingaben die genehmigte Umgebung bzw. die anwendbaren Daten- und Aufbewahrungsbedingungen des Anbieters verlassen; und
- verbotene Verwendungen, einschließlich Identifizierung, Authentifizierung, Identitätsvortäuschung, Ableitung sensibler Merkmale oder Veröffentlichung ohne die vereinbarte Prüfung.

Erstellen Sie kein Identitätsdatenset aus gescrapten Porträts, nicht überprüfbaren
Referenzen oder Bild-Embeddings, denen diese Befugnis fehlt. Ein Trigger-Wort,
eine Beschriftung, ein Gesichtszuschnitt oder ein generiertes Beispiel ersetzen
keine Einwilligung.

## Kompatibilität von Modell und Adapter festlegen {#pin-model-and-adapter-compatibility}

Binden Sie den exakten Base-Checkpoint, die Laufzeitumgebung, die Text- und
Bildkomponenten, Adaptermethode und -konfiguration, Zielmodule, Trainer-Versionen
und den Inferenz-Loader. Der [klein-Trainingsleitfaden von BFL](https://docs.bfl.ai/flux_2/flux2_klein_training)
beschreibt Base-Varianten als Ausgangspunkte für Feinabstimmung, macht aber einen
generischen Optimierer, eine Bildanzahl, einen Rang, die Platzierung der
Beschriftung oder einen „Identity“-Adapter nicht über alle Werkzeuge und Releases
hinweg kompatibel.

Bewahren Sie sowohl die Adapter-Gewichte als auch die Konfiguration auf. Das
[PEFT-Checkpoint-Format](https://huggingface.co/docs/peft/developer_guides/checkpoint)
ist ein Beispiel dafür, warum eine Konfiguration neben den Gewichten nötig ist.
Testen Sie das exakte Trainings- und Inferenz-Paar mit einer nicht sensiblen,
genehmigten Baseline, bevor Sie einen Lauf mit personenbezogenen Daten akzeptieren.

## Ein ehrliches Evaluierungsset aufbauen {#build-an-honest-evaluation-set}

Trennen Sie Trainings-, Tuning- und Holdout-Material nach Originalaufnahme,
Sitzung, Pose/Bildausschnitt, Kleidung/Hintergrund und Ableitungskette. Die
Evaluierungsrichtlinie sollte benennen, was unverändert bleiben muss und was
sich ändern darf:

- den angeforderten Kontext, Stil oder die angeforderte Bearbeitung;
- die Ähnlichkeit, beurteilt von autorisierten Prüfern unter dem angegebenen Zweck;
- geschützte Gesichts- und Körpermerkmale, Altershinweise, Markierungen, Text, Zubehör und andere Bereiche; und
- Fehler wie ungewollte Ähnlichkeit, Sexualisierung, herabwürdigenden Kontext, falsche Zuordnung oder Verlust sachlicher Produkt- bzw. Hintergrunddetails.

Verwenden Sie einen automatisierten Ähnlichkeitswert weder als Identifizierung
noch als alleinige Freigabeentscheidung. Behaupten Sie nicht, dass ein generiertes
Bild belegt, wer eine Person ist, was sie getan hat oder dass sie der Ausgabe
zugestimmt hat.

## Freigabe und Widerruf {#release-and-revocation}

Stellen Sie sicher, dass jede genehmigte Ausgabe auf ihre Base, ihren Adapter,
ihre Eingaberichtlinie und ihren Prüfbeleg zurückführbar ist. Kennzeichnen Sie
KI-Veränderungen, wo Richtlinie oder Gesetz dies verlangen. Wenn die Befugnis
abläuft oder widerrufen wird, deaktivieren Sie neue Inferenz, entfernen Sie den
Adapter und abgeleitete Daten gemäß der vereinbarten Löschrichtlinie und
dokumentieren Sie den Abschluss, ohne personenbezogenes Material offenzulegen.

Kann das Projekt diese Kontrollen nicht erfüllen, trainieren Sie keinen
Identity-Adapter; verwenden Sie stattdessen einen nicht identifizierenden
Character- oder Stil-Workflow oder halten Sie die Anfrage blockiert.

## Verwandte Seiten {#related-pages}

- [[diffusion-lora-training]]
- [[lora-fine-tuning-for-editing-models]]
- [[style-reference-ux]]
- [[flux-klein-9b-architecture]]
