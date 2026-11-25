---
title: "Hautretusche: Einwilligungsbewusster Korrektur-Workflow"
description: "Hautretusche ist ein einwilligungsbewusster, auf den Umfang begrenzter Korrektur-Workflow; Identität, Textur und geschützte Merkmale bleiben erhalten, jede Maske und Bearbeitung ist nachvollziehbar, und alle veränderten Hautbereiche müssen geprüft werden."
category: workflows
tags: [skin-retouch, inpainting, consent, privacy, masks, texture-preservation, quality-control]
aliases: ["Skin Retouch Pipeline", "Blemish Correction Workflow"]
level: 2
source_sha256: ae13db7c36f0197bf792c23ae5ba3ce1da370f29dc84db88b55997355f52cb04
translation: machine
translated_at: '2026-10-24'
---
# Hautretusche: Einwilligungsbewusster Korrektur-Workflow {#skin-retouching-consent-aware-correction-workflow}

Hautretusche soll ein ausdrücklich freigegebenes visuelles Problem korrigieren,
ohne Identität, Alterswirkung, Hautton, Körpermerkmale oder gesundheitsbezogene
Erscheinung stillschweigend zu verändern. Es handelt sich nicht um eine allgemeine
„Verschönerungs“-Operation, und sie darf niemals verwendet werden, um medizinische
oder sensible persönliche Merkmale abzuleiten oder zu klassifizieren.

## Aufnahme und Einwilligung {#intake-and-consent}

Für jedes Quellbild sind der Bild-Digest, die Berechtigung zur Bearbeitung, der
genehmigte Zweck, der angeforderte Korrekturumfang, die Zugriffs- und
Aufbewahrungsrichtlinie sowie alle untersagten Änderungen zu dokumentieren.
Porträts sind auch dann als sensibles Material zu behandeln, wenn die beabsichtigte
Bearbeitung rein kosmetisch ist.

Anfragen sind in begrenzten visuellen Begriffen zu beschreiben, etwa als vorübergehend
sichtbarer Fehler in einem benannten Bereich. Ist eine Anfrage mehrdeutig, potenziell
medizinisch oder verändert sie geschützte Erscheinungsmerkmale, wird sie an die
menschliche Prüfung weitergeleitet und nicht automatisiert retuschiert.

## Maskenorientierter Workflow {#mask-first-workflow}

1. Eine Maske für das freigegebene Problem erstellen oder prüfen.
2. Geschützte Bereiche markieren, einschließlich Augen, Lippen, Haaransatz,
   Gesichtskonturen, Tätowierungen, Schmuck sowie aller Inhalte, die laut Anfrage
   erhalten bleiben sollen.
3. Die am wenigsten generative Korrektur wählen, die die Maske erfüllen kann.
4. Original, Maske, Operationsparameter und bearbeitetes Ergebnis zusammen aufbewahren.
5. Jeden veränderten Bereich in Auslieferungsauflösung und neben der Quelle prüfen.

Automatische Erkennung oder Segmentierung kann Masken vorschlagen, aber nicht
entscheiden, welches Hautmerkmal verändert werden soll. Ein Konfidenzwert eines
Detektors darf niemals Einwilligung, Zweck oder eine menschliche Abnahmeentscheidung
ersetzen.

## Erhalt von Textur und Identität {#texture-and-identity-preservation}

Ein repräsentativer Validierungsdatensatz dient dazu, Porentextur-Kontinuität,
Kantenübergänge, Beleuchtung, Farbe und Gesichtsgeometrie zu prüfen. Ein verwischter
oder übermäßig glatter Bereich gilt als Fehler, selbst wenn der angeforderte Fehler
verschwunden ist. Wird ein Inpainting-Modell verwendet, ist der generierte Bereich
vom beobachteten Quelldetail zu unterscheiden. Ausgaben, die Identität, geschützte
Merkmale oder angrenzende Objekte verändern, werden verworfen.

Für eine umfangreichere Bearbeitung oder ein Bearbeitungsmodell ist die gewünschte
Korrektur getrennt vom Erhalt zu validieren; siehe [[face-beautify-edit-lora]].
Für Hintergrund- oder Objektbereinigung um eine Person gilt der eingeschränkte
Masken-Vertrag in [[object-removal-inpainting]].

## Freigabeprotokoll {#release-record}

Eine genehmigte Retusche benötigt die Digests von Quelle und Ergebnis, die Maskenversion,
die Modell- oder Werkzeugrevision, die Anweisung, den Prüfer, die Entscheidung zum
Umfang sowie einen umkehrbaren Auslieferungsweg. Das Originalmaterial darf nicht durch
ein bearbeitetes Bild ersetzt werden, ohne dass beide aufbewahrt werden.

## Verwandte Seiten {#related-pages}

- [[face-beautify-edit-lora]]
- [[object-removal-inpainting]]
- [[face-detection-filtering-pipeline]]
- [[retouch-patch-harmonization]]
