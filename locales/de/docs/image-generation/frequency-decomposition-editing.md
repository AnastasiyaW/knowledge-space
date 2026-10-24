---
title: "Frequenzzerlegung für die Bildbearbeitung: Transformation und Treuevertrag"
description: "Frequenzzerlegung ist eine deklarierte Transformation, keine semantische Bearbeitungskarte; erfassen Sie Farbdomäne, Transformation oder Filter, Randbehandlung und Rekonstruktionsrichtlinie, Bearbeitungsmasken und Ausgabeprüfung, und unterscheiden Sie mathematisch rekonstruiertes Signal von generierten oder visuell plausiblen Details."
category: techniques
tags: [frequency, wavelets, laplacian, filtering, reconstruction, retouching, fidelity]
aliases: ["Frequency Separation", "Low and High Frequency Editing"]
level: 2
source_sha256: aab36b6efbc9e636fea850a26a2c89d4e9e3fd211fb0cb90a7349b3cfe425abf
translation: machine
translated_at: '2026-10-24'
---
# Frequenzzerlegung für die Bildbearbeitung: Transformation und Treuevertrag {#frequency-decomposition-editing-transform-and-fidelity-contract}

Niedrig- und hochfrequente Bezeichnungen beschreiben die Antwort einer
gewählten Transformation oder eines gewählten Filters. Sie identifizieren
nicht automatisch „Haut“, „Detail“, „Beleuchtung“ oder einen anderen
semantischen Bereich. Ein Frequenz-Workflow ist nur dann vertrauenswürdig,
wenn Farbdomäne, Transformation, Randverhalten, Bearbeitungen, Rekonstruktion
und Prüfung allesamt deklariert sind.

## Den Signalvertrag deklarieren {#declare-the-signal-contract}

Für jeden Auftrag erfassen Sie:

- Quell-Digest, Abmessungen, Ausrichtung, Alpha-/Maskenrichtlinie, Farbkodierung
  und ob Operationen in linearen oder anzeigebezogenen Werten erfolgen;
- Transformations-/Filterfamilie, Implementierung/Version, Skala/Stufe/Radius,
  Kanäle, Datentyp und Normalisierung;
- Padding- bzw. Randerweiterungsmodus, Zuschneide- und Ausrichtungsrichtlinie
  sowie die Rekonstruktionsroutine;
- editierbare/geschützte Bereiche und jede generierte Komponente; und
- Ausgabetransformation, Clipping-/Gamut-Verhalten, numerische
  Rekonstruktionsprüfung und Nachweis der visuellen Prüfung.

Eine Änderung des Unschärferadius, der Wavelet-Familie, des Padding-Modus,
der Farbkodierung oder des Zuschnitts verändert die Bänder. Verwenden Sie
keinen numerischen Radius oder kein Frequenzband-Label aus einer anderen
Auflösung, einem anderen Objektiv, einer anderen Bilddomäne oder einer
anderen Transformation, als würde es denselben Inhalt bezeichnen.

## Eine Transformation für die deklarierte Eigenschaft wählen {#choose-a-transform-for-the-stated-property}

Gauß- und Laplace-Pyramiden, dezimierte Wavelets, stationäre Wavelets,
geführte Filter und gelernte Frequenzmodule unterscheiden sich in Redundanz,
Ausrichtung, Randverhalten und Rekonstruktion. Wählen Sie eine Methode, weil
ihre dokumentierte Eigenschaft die Aufgabe stützt, und validieren Sie sie
anschließend an repräsentativen Bildern.

[Die Dokumentation zur stationären Wavelet-Transformation in PyWavelets](https://pywavelets.readthedocs.io/en/latest/ref/swt-stationary-wavelet-transform.html)
beschreibt SWT als translationsinvariante, nicht dezimierte Modifikation der
DWT; sie hält außerdem Redundanz und Einschränkungen der Signalgröße fest.
Die [Dokumentation zur Signalerweiterung](https://pywavelets.readthedocs.io/en/latest/ref/signal-extension-modes.html)
zeigt, warum der Randmodus in den Vertrag gehört. Keine der beiden belegt,
dass eine Wavelet-Familie für jede Retusche artefaktfrei oder vorzugswürdig
ist.

## Rekonstruktionsnachweise sichern {#preserve-reconstruction-evidence}

Für eine lineare Transformation mit passender Inverser und unveränderten
Koeffizienten berechnen und speichern Sie ein numerisches Hin-und-zurück-Residuum
unter dem deklarierten Datentyp und der deklarierten Randrichtlinie. Sobald
Koeffizienten bearbeitet, geclippt, maskiert, mit einem anderen Bild gemischt
oder durch ein nichtlineares/generatives Modell geleitet werden, ist das
Ergebnis ein abgeleitetes Bild und benötigt eine eigene Treueprüfung.

Prüfen Sie Nahtstellen, Halos, Ringing, Texturstärke, Verläufe, Farbverschiebungen,
Text, Produktgeometrie, Gesichter und geschützte Bereiche in der
Auslieferungsauflösung. Wird hochfrequenter Inhalt nach einer
niederfrequenten Änderung synthetisiert, kennzeichnen Sie ihn als generiertes
Detail; stellen Sie ihn nicht als wiederhergestellte Quelltextur dar.

## Bearbeitung und Freigabegrenze {#editing-and-release-boundary}

Verwenden Sie Masken und eine explizite Änderungsabsicht, statt ein
Frequenzband als Erlaubnis zu betrachten, jeden Pixel in diesem Band zu
verändern. Ein visuell glattes Ergebnis kann dennoch sachliche Markierungen
entfernen oder Material-, Haut- bzw. Produktdetails verändern. Vergleichen
Sie mit der Quelle und einer genehmigten Aufgabenbasis, und bewahren Sie den
Transformationsnachweis zusammen mit der Ausgabe auf.

Kann die Transformation innerhalb der deklarierten Toleranz nicht rekonstruieren,
ist die Randrichtlinie mehrdeutig oder findet die visuelle Prüfung eine
Änderung geschützter Details, geben Sie einen sichtbaren Fehler- oder
Prüfstatus zurück. Injizieren Sie nicht stillschweigend ein anderes Band
erneut, wenden Sie kein neues Schärfungsmodell an und behaupten Sie keine
exakte Rekonstruktion.

## Verwandte Seiten {#related-pages}

- [[color-space-and-gamma-reference]]
- [[tiled-inference]]
- [[paired-training-for-restoration]]
- [[skin-retouch-pipeline]]
