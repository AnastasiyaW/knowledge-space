---
title: "Farbkorrektur: Messgebundener Kalibrierungsvertrag"
description: "Farbkorrektur ist nur gegenüber einem deklarierten Messziel, Beleuchtungsmittel, einer Kamera bzw. einem Profil, einem Arbeitsfarbraum und einer Betrachtungstransformation gültig; neutrale Proben und Chart-Felder sind Nachweise, wenn ihre Herkunft bekannt ist, während Szenenmittelwerte und Hauttonverhältnisse keine universelle Grundwahrheit sind."
category: techniques
tags: [color-correction, white-balance, color-checker, calibration, profiles, evaluation]
aliases: ["Color Correction by Numbers", "White Balance Measurement"]
level: 3
source_sha256: ac7f1845139c6ec71538b30a498b2ff9ec167250b9d4caeedea97a7af1a773e4
translation: machine
translated_at: '2026-10-24'
---
# Farbkorrektur: Messgebundener Kalibrierungsvertrag {#color-correction-measurement-bound-calibration-contract}

Numerische Korrektur ist belastbar, wenn die Zahlen an ein deklariertes
Messziel und einen definierten Farbmanagement-Pfad gebunden sind. Pixelmittelwerte,
ein szenenweites RGB-Verhältnis oder eine angenommene Hautfarbregel legen weder
eine Beleuchtung, einen Reflexionsgrad, eine Kameraantwort noch eine beabsichtigte
kreative Gradation fest.

## Mit einem Korrekturziel beginnen {#start-with-a-correction-target}

Wählen Sie vor dem Verändern von Pixeln einen dieser expliziten Zwecke:

| Zweck | Erforderliche Nachweise |
|---|---|
| Aufnahmekalibrierung | ein bekanntes Target, Aufnahmebedingungen, Eingangstransformation und gemessene Referenzwerte für dieses Target |
| Kamerübergreifendes Angleichen | freigegebene Referenzaufnahmen, beide Kameratransformationen, Betrachtungsbedingungen und Freigabe durch Prüfer |
| Redaktionelle Gradation | ein verfasstes Ziel bzw. ein verfasster Look und eine Freigaberichtlinie, kein Anspruch auf physikalische Neutralität |
| Automatisierter Vorschlag | eine begrenzte Schätzung mit Konfidenzwert und Prüfung, kein automatisches Wahrheitslabel |

[Calibrite's ColorChecker White Balance target](https://calibrite.com/us/product/colorchecker-white-balance/?noredirect=en-US)
ist als spektral neutrale Referenz für individuelle Weißabgleichs­korrektur
konzipiert. Das unterstützt einen Messablauf, wenn das tatsächliche Target
sichtbar und rückverfolgbar ist; es macht jedoch keine beliebige Wand, keine
überstrahlte Lichtstelle und keinen Bildmittelwert zu einer universellen
neutralen Referenz.

## Die Messung binden {#bind-the-measurement}

Bewahren Sie für jede Korrektur Folgendes auf:

- Target-Typ, Revision, Eigentümerschaft, Position in der Szene und Target-
  Region-Maske;
- Beleuchtungsmittel bzw. Aufnahmebedingungen, Kameraeinstellungen,
  Raw-Decoder bzw. Eingangsprofil sowie eventuelle In-Kamera-Verarbeitung;
- Quellkodierung, Linearisierungsrichtlinie, Arbeitsfarbraum, Versionen der
  Transformationen sowie Ausgabe- bzw. Betrachtungstransformation;
- gemessene Feld- oder Neutralwerte mit ihrer Abtastmethode; und
- vorgeschlagene Transformation, Verhalten bei Clipping und Gamut, Entscheidung
  des Prüfers sowie Output-Digest.

Bekannte Chart-Werte hängen vom Chart, vom Beleuchtungsmittel, von der
Messgeometrie und von der Kodierung ab. Hinterlegen Sie keine feste Tabelle mit
RGB-Werten für Raw-, szenenlineare, anzeigebezogene oder anders profilierte
Bilder.

## Einen verwalteten Transformationspfad verwenden {#use-a-managed-transform-path}

Das [ICC-Profil-Handbuch](https://www.color.org/getting-started/) erklärt, dass
Geräteprofile über einen definierten Profile Connection Space verbunden werden.
Ein RGB-Tripel benennt Gerätekanäle, solange Kodierung und Profil nicht bekannt
sind. [OpenColorIO](https://opencolorio.readthedocs.io/en/latest/guides/authoring/authoring.html)
behandelt Farbräume und Anzeigeansichten ebenfalls als explizite
Konfigurationsobjekte. Wenden Sie eine Korrektur in einem deklarierten Pfad an
und validieren Sie diesen Pfad, statt anzunehmen, dass ein Mischmodus oder eine
Kanalkurve in jeder Kodierung die Luminanz isoliert.

Eine Implementierung darf Verstärkungen, eine Matrix oder eine andere
Transformation schätzen, muss ihre Annahmen aber offenlegen. Fehlen Metadaten,
ist das Target nicht sichtbar oder die Eingangsinterpretation unklar, geben Sie
eine prüfbare Schätzung oder einen expliziten Zustand „Kalibrierung nicht
möglich“ zurück, statt einen numerischen Referenzwert zu erfinden.

## Farbe und Inhalt gemeinsam bewerten {#evaluate-color-and-content-together}

Verwenden Sie zurückgehaltene Aufnahmen, die unter den vorgesehenen
Aufnahme- und Auslieferungsbedingungen entstanden sind. Vergleichen Sie
Target-Felder bzw. freigegebene Referenzregionen nach derselben
Ausgabetransformation, die auch für die Auslieferung verwendet wird, und prüfen Sie:

- Neutral- bzw. Target-Region-Fehler nach der deklarierten Messmethode;
- Clipping in Lichtern und Schatten, Gamut-Mapping und Verlaufskontinuität;
- Produkt- bzw. Materialidentität, Text, Masken und geschützte Bereiche; und
- Erscheinungsbild in der validierten Betrachtungskonfiguration.

Wählen Sie während der Validierung aufgabenspezifische Metriken und Schwellenwerte;
eine einzelne RGB-Differenz, eine Kanalhierarchie oder ein Hauttonverhältnis ist
kein Freigabekriterium für alle Motive, Beleuchtungsmittel oder Render-Intents.

## Grenze für Menschen und Sicherheit {#human-and-safety-boundary}

Leiten Sie aus Farbwerten keine Ethnizität, keinen Gesundheitszustand, keine
Attraktivität und kein kanonisches menschliches Erscheinungsbild ab. Menschliche
Haut ist kein Kalibrierungs-Chart. Wenn eine Person im Umfang liegt, verwenden
Sie Einwilligung, eine freigegebene visuelle Referenz und Prüfkriterien, die
Farbmessungen nicht in Labels für sensible Merkmale umwandeln.

## Verwandte Seiten {#related-pages}

- [[color-checker-and-white-balance]]
- [[color-space-and-gamma-reference]]
- [[color-theory-for-ml]]
- [[intrinsic-decomposition]]
