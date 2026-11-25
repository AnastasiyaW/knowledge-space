---
title: "In-Kontext-Segmentierung: Referenzgebundene Kandidatenmasken"
description: "In-Kontext-Segmentierung überträgt eine mitgelieferte Referenzmaske über ein benanntes Vision-Modell; ihre Ausgabe ist eine Kandidatenmaske, keine Ground Truth, und erfordert Herkunftsnachweis der Referenz, Prüfung des Zielbilds, Unsicherheitsbehandlung und quellendisjunkte Validierung."
category: reference
tags: [segmentation, dinov3, few-shot, in-context, candidate-masks, review]
level: 2
source_sha256: 8b0e7575fbb6324fbe515cbcf1c0bd39b12d92178f2f43f99ae71fa5c69a826e
translation: machine
translated_at: '2026-10-24'
---
# In-Kontext-Segmentierung: Referenzgebundene Kandidatenmasken {#in-context-segmentation-reference-bound-candidate-masks}

In-Kontext-Segmentierung verwendet ein oder mehrere Referenz-Bild/Masken-Paare,
um eine Maske für ein Zielbild vorzuschlagen. Das Ergebnis überträgt die visuelle
Bedeutung der Referenz über ein bestimmtes Vision-Modell; es ist eine **Kandidatenmaske**,
keine Ground Truth, kein Einwilligungsnachweis, kein Identitätsnachweis und kein
automatisch erzeugtes Trainingslabel.

## Aktuelle Grenze des Upstream-Projekts {#current-upstream-boundary}

[INSID3](https://github.com/visinf/INSID3) beschreibt eine trainingsfreie Methode
zur In-Kontext-Segmentierung, die ein eingefrorenes DINOv3-Backbone verwendet. Das
[DINOv3-Referenzrepository](https://github.com/facebookresearch/dinov3) veröffentlicht
das Backbone und das Evaluationsmaterial. Deren Paper und Code rechtfertigen es,
die benannte Methode zu testen; sie machen jedoch nicht jedes Referenz-Zielbild-Paar
gleichwertig und begründen keinen allgemeinen Annotationsdienst.

Verwenden Sie die dokumentierte Vorverarbeitung, Gewichte und Inferenz-Einstiegspunkte
des Upstream-Releases. Rekonstruieren Sie keine internen Feature-Manipulationen und
ersetzen Sie keine Modellkomponenten durch eine ungetestete lokale Interpretation.

## Vertrag für Referenz und Ziel {#reference-and-target-contract}

Für jede vorgeschlagene Maske sind folgende Angaben aufzubewahren:

- Digests des Referenzbilds und der Referenzmaske, Protokoll zu Urheber und Rechten,
  Klassen- bzw. Teildefinition sowie Qualitätsprüfung der Referenz;
- Digest des Zielbilds, Pfad für Zuschnitt, Orientierung und Vorverarbeitung sowie
  Kennung der Zieldomäne;
- Modell, Gewichte, Code-Revision sowie Revision von Vor- und Nachverarbeitung;
- Ausgabemaske, Konfidenz- bzw. Unsicherheitsinformationen, sofern verfügbar, und
  Prüfstatus; sowie
- eine klare Regel für geschützte, mehrdeutige, fehlende und außerhalb des Geltungsbereichs
  liegende Regionen.

Die Referenzmaske legt fest, was das System zu übertragen versucht. Eine mehrdeutige,
schlecht zugeschnittene oder unpassende Referenz ist ein Datenqualitätsfehler und
kein Grund, eine plausibel aussehende Zielmaske zu akzeptieren.

## Prüfung und Validierung {#review-and-validation}

Prüfen Sie Kandidatenmasken, bevor Sie sie in einer Bearbeitung, einem Datensatz oder
einem nachgelagerten Modell verwenden. Achten Sie besonders auf dünne Strukturen,
Verdeckung, transparente Materialien, Bewegungsunschärfe, Haare/Fell, Schatten,
wiederholte Objekte und Grenzen nahe geschützter Regionen.

Erstellen Sie Evaluationssplits nach Quellasset und Ableitungskette. Lassen Sie nicht zu,
dass Beinahe-Duplikate von Zuschnitten, dasselbe Motiv oder das Referenzbild selbst in
Training/Tuning und Holdout-Evaluation auftauchen. Berichten Sie getrennte Ergebnisse für:

| Frage | Nachweis |
|---|---|
| Übertragungsqualität | geprüfte Maskenüberlappung gegen eine autorisierte Ground Truth, sofern vorhanden |
| Fehlererkennung | leere, übergroße, fragmentierte oder semantisch unpassende Masken werden markiert statt stillschweigend akzeptiert |
| Domänenverschiebung | Held-out-Quellen, Beleuchtung, Blickwinkel, Materialien und Zielgrößen |
| Operativer Einsatz | Prüfzeit der Bearbeiter, Korrekturweg, Aufbewahrung der Herkunftsnachweise und Eskalationsregel |

Eine numerische Überlappungsmetrik gilt nur für eine geprüfte Ground-Truth-Maske unter
einer definierten Grenzregel. Sie kann die semantische Korrektheit für nicht gelabelte
Zielbilder nicht belegen.

## Grenze für Datensatz und Bearbeitung {#dataset-and-editing-boundary}

Kandidatenmasken können die Annotation beschleunigen, müssen aber mit ihrer Referenz und
der Entscheidung des Prüfers verknüpft bleiben. Wandeln Sie sie nicht in automatische
Labels, medizinische Schlussfolgerungen, Personenmerkmale oder freigabefähige
Bearbeitungsmasken um, ohne die eigene Prüf- und Freigaberichtlinie der Aufgabe.

Ist ein Zielbild außerhalb der Verteilung, die Referenz unklar oder verändert die Maske
einen sachlich, produktbezogen oder identitätsrelevanten Bereich, schlagen Sie sichtbar
fehl und fordern Sie eine manuelle Annotation an. Eine trainingsfreie Methode verändert
die Trainingsanforderung; sie hebt die Verifikationsanforderung nicht auf.

## Verwandte Seiten {#related-pages}

- [[synthetic-dataset-pipeline]]
- [[face-detection-filtering-pipeline]]
- [[paired-training-for-restoration]]
