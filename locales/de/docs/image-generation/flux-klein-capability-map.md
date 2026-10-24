---
title: "FLUX.2 [klein] Capability Map: Bestätigter Operationsvertrag"
description: "Eine FLUX.2 [klein]-Fähigkeit ist nur dann nutzbar, wenn die genaue Variante, der Checkpoint, die Lizenz, die Runtime bzw. der Provider-Endpunkt, der Eingabevertrag und die Ausgabeprüfung zur Ausführungszeit bestätigt sind; die Unterstützung von Generierung und Bearbeitung auf Familienebene berechtigt nicht zu jedem Adapter, jedem Dienst, jeder kommerziellen Nutzung oder jedem Bearbeitungsergebnis."
category: reference
tags: [flux, klein, capabilities, operations, licensing, adapters, provenance]
aliases: ["Klein Operations Map", "Klein Capability Map"]
level: 2
source_sha256: b9205c899ceefbe88b49888d4e1dace0c52c1b3fb7d4fe2b782d04dacda3f962
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 [klein] Capability Map: Bestätigter Operationsvertrag {#flux2-klein-capability-map-attested-operation-contract}

Capability Maps veralten schnell. Eine Ankündigung der Modellfamilie, ein
Community-Adapter oder ein alter Provider-Endpunkt kann nicht belegen, was in
einem aktuellen Auftrag verfügbar, lizenziert, kompatibel oder sicher ist.
Behandle eine Operation erst dann als nutzbar, wenn die genaue Release- und
Ausführungskette bestätigt wurde.

## Unterstützung auf Familienebene ist kein Operationsnachweis {#family-support-is-not-an-operation-receipt}

Das [offizielle FLUX.2-Repository](https://github.com/black-forest-labs/flux2)
gibt an, dass die [klein]-Familie Text-zu-Bild, Bearbeitung mit einer
Referenzbild-Eingabe und Bearbeitung mit mehreren Referenzbildern unterstützt.
Außerdem werden die Releases 4B, 9B, 9B KV und Base mit jeweils unterschiedlich
angegebenen Zwecken und Lizenzen genannt.

Dabei handelt es sich um Fähigkeiten auf Familienebene. Daraus folgt nicht, dass:

- ein bestimmtes LoRA, ein Node, eine Checkpoint-Konvertierung, eine
  Quantisierung oder ein Community-Workflow auf der gewählten Variante geladen
  werden kann;
- ein gehosteter Provider weiterhin denselben Endpunkt, dasselbe Eingabeschema,
  denselben Preis, dieselbe Aufbewahrungsrichtlinie oder dieselben kommerziellen
  Rechte bereitstellt;
- ein Referenzbild an diesen Provider übermittelt werden darf; oder
- eine erzeugte Bearbeitung ein reales Motiv korrekt entfernt, erhalten, verschoben,
  neu beleuchtet oder identifiziert hat.

## Operation zur Ausführungszeit bestätigen {#attest-the-operation-at-execution-time}

Speichere für jeden Auftrag:

| Vertragsbereich | Erforderlicher Nachweis |
|---|---|
| Modell | genaue Variante, Checkpoint-Digest, Komponenten, Quelle und Lizenzhinweis |
| Runtime | Revision des lokalen Codes/Nodes oder des Provider-Endpunkts, Ein- und Ausgabeschema sowie Fehlerverhalten |
| Adapter | Adaptergewichte mit Konfiguration, deklariertes Ziel-Basismodell, Loader-Test, Autor/Quelle und Lizenz |
| Eingaben | Berechtigung an den Assets, Einwilligung für Referenzbilder, Vorverarbeitung, Masken/Regionen und Offenlegung Dritter |
| Richtlinie | zulässiger Zweck, kommerzieller Status und Verbreitungsstatus, Herkunft der Ausgabe und Befugnis der prüfenden Person |
| Belege | Digest der Anfrage bzw. Konfiguration, Digest der Ausgabe, Nachweis zu Modell und Runtime sowie aufgabenspezifische Prüfung |

Die [Modellübersicht](https://bfl.ai/models/flux-2-klein) von BFL enthält aktuelle,
variantenspezifische Angaben, einschließlich des beschriebenen Zwecks eines
Releases. Maßgeblich bleibt die Modellkarte bzw. die Provider-Dokumentation, die
zum Zeitpunkt der Ausführung gilt. Friere flüchtige Angaben zu VRAM, Geschwindigkeit,
Skalierung, Endpunkten oder Preisen nicht in einer operativen Zusage ein.

## Grenze zwischen Adapter und Provider {#adapter-and-provider-boundary}

Adapter sind keine nativen Fähigkeiten. Vor der Verwendung prüfe die genaue
Kompatibilität mit dem Basismodell, Format und Konfiguration des Adapters, die
Zielmodule, die Lizenz sowie das Lade- und Ausgabeverhalten. Community-Bezeichnungen
wie „remove“, „relight“, „consistency“ oder „character“ beschreiben eine beabsichtigte
Wirkung, aber keine genehmigte Befugnis, geschützte Inhalte zu verändern.

Bei einem Remote-Dienst dokumentiere den genauen Endpunkt, die Bedingungen zu
Region und Aufbewahrung, das Anfrage- und das Antwortschema, die kommerziellen
Bedingungen sowie die für den Provider sichtbaren Eingaben. Wenn eines dieser
Elemente nicht bestätigt werden kann, bleibt die Operation nicht verfügbar. Ein
stilles Ausweichen auf ein anderes Modell, einen anderen Endpunkt oder einen
lokalen Node ist nicht zulässig.

## Die Ausgabe prüfen, nicht das Label {#review-the-output-not-the-label}

Text-zu-Bild, Referenzbild-Bearbeitung und Adapter können plausible Inhalte
erzeugen. Sie stellen keine fehlenden Fakten wieder her und belegen keine
unveränderte Identität. Prüfe vor der Veröffentlichung die deklarierten
geschützten Regionen, Text, Geometrie, Material- und Farbhinweise sowie die
Rechte. Behandle unsichere Ausgaben als Vorschläge mit sichtbarer Herkunft und
nicht als quellgetreue Ergebnisse.

## Verwandte Seiten {#related-pages}

- [[flux-klein-9b-architecture]]
- [[flux-klein-9b-inference]]
- [[flux-klein-character-lora]]
- [[style-reference-ux]]
