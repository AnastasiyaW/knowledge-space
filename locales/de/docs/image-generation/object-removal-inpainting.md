---
title: "Objektentfernung und Inpainting: Vertrag für kontrollierte Bearbeitung"
description: "Objektentfernung ist eine eingeschränkte Bearbeitung: Quellasset, zulässiges Objekt, Maske, Modellvertrag und geschützte Bereiche binden und die Szenenkontinuität sowie die sachliche Erhaltung vor der Freigabe validieren."
category: techniques
tags: [inpainting, object-removal, erasure, masks, source-preservation, quality-control]
aliases: ["Object Removal and Inpainting Models", "Image Erasure"]
level: 2
source_sha256: 574b0f3d5a4275ce00509f9ff1c2c32cc9922129f287a470c04c88e9f2d335e4
translation: machine
translated_at: '2026-10-24'
---
# Objektentfernung und Inpainting: Vertrag für kontrollierte Bearbeitung {#object-removal-and-inpainting-controlled-edit-contract}

Objektentfernung ist keine Aufforderung, einen schöneren Hintergrund zu erzeugen. Sie ist eine eingeschränkte Bearbeitung eines benannten Quellassets mit einem auf einer Freigabeliste stehenden Entfernungsziel und geschützten Inhalten, die sich nicht ändern dürfen. Die Aufgabe kann scheitern, selbst wenn der aufgefüllte Bereich plausibel aussieht: Eine Bearbeitung kann Produktgeometrie, Text, Urheberrechtsvermerke, Schatten oder visuelle Belege außerhalb des genehmigten Umfangs verändern.

## Bearbeitungsgrenze festlegen {#define-the-edit-boundary}

Bevor ein Modell ausgewählt wird, einen Bearbeitungsdatensatz anlegen, der Folgendes enthält:

- Digest des Quellassets und die Berechtigung zur Änderung;
- zulässiges Objekt bzw. zulässiger Defekt, gewünschtes Ergebnis und Grund für die Entfernung;
- Maskenrevision, geschützte Bereiche und eine Ausschlussliste;
- Ziel-Farb- bzw. Renderingraum und Verwendungszweck der Ausgabe; und
- Modell/Laufzeit/Checkpoint, Adapter und Lizenzentscheidung.

Masken ablehnen, die geschützte Elemente berühren oder über die autorisierte Bearbeitung hinausreichen. Bei Produktbildern sollten das Produkt selbst, seine Markierungen, Geometrie und Materialbelege in der Regel geschützt und nicht rekonstruiert werden.

## Kompatible Methode wählen {#choose-a-compatible-method}

Die am wenigsten generative Methode verwenden, die die Bearbeitung erfüllt:

1. **Direkte Retusche oder patchbasiertes Füllen** für einen kleinen, gut verstandenen Hintergrunddefekt, wobei die originalen Pixelbelege erhalten bleiben.
2. **Deterministisches oder aufgabenspezifisches Inpainting**, wenn Maske und Degradation zur dokumentierten Aufgabe des Modells passen. [LaMa](https://github.com/advimman/lama) ist ein auflösungsrobustes Forschungsmodell für Inpainting großer Masken; seine Ausgabe benötigt dennoch Rand- und Inhaltsvalidierung auf den Zielbildern.
3. **Text- oder referenzgeführtes Inpainting** nur dann, wenn semantische Synthese autorisiert ist und das gewählte Modell einen kompatiblen Vertrag für Bildbearbeitung veröffentlicht. Dies ist eine neu erzeugte Region und keine wiederhergestellte Quellevidenz.

Nicht annehmen, dass ein Modell, das für eine andere Inpainting-Aufgabe trainiert wurde, ein Drittanbieter-Node oder ein LoRA für ein anderes Basismodell mit der aktuellen Pipeline austauschbar ist.

## Masken vorbereiten und prüfen {#prepare-and-review-masks}

Einen Maskenworkflow verwenden, der menschliche Korrektur ermöglicht. Die ursprüngliche Maske, Änderungen, die Entscheidung zu Dilatation/Weichzeichnung und die finale Maske speichern. Prüfen:

- Kantenkontakt mit Haaren, Schmuck, Text, Produktkonturen oder dünnen Objekten;
- transparente, reflektierende oder schattige Bereiche, die gesondert behandelt werden müssen;
- Überlappung mit Farbreferenz- oder Messbereichen; und
- jeden geschützten Bereich, der bitweise oder visuell unverändert bleiben muss.

Automatische Segmentierung kann Maskenkandidaten einordnen, aber sie kann weder Autorisierung noch sachliche Relevanz begründen. Unsichere Masken bleiben in der Prüfung.

## Ergebnis validieren {#validate-the-result}

Das Ergebnis innerhalb und außerhalb der Maske mit der Quelle vergleichen. Erforderliche Prüfungen umfassen Szenenkontinuität, Konsistenz von Beleuchtung und Reflexionen, keine unerwartete Objekteinfügung, keine Abweichung geschützter Inhalte und keine sichtbare Naht an der Maskengrenze. Bei einem Produkt oder Dokument sind sachliche Merkmale mit der genehmigten Referenz zu vergleichen und nicht nur die visuelle Plausibilität zu bewerten.

Ein Pass/Fail-Ergebnis zusammen mit Eingabe, Maske, Modellrevision, Prompt bzw. Anweisung und Ausgabe-Digest protokollieren. Schlägt eine Ausgabe fehl, wird sie als abgelehnter Kandidat aufbewahrt und nicht stillschweigend an die Stelle der Quelle gesetzt.

## Verwandte Seiten {#related-pages}

- [[skin-retouch-pipeline]]
- [[retouch-patch-harmonization]]
- [[flux-klein-jewelry-photography]]
- [[color-checker-and-white-balance]]
