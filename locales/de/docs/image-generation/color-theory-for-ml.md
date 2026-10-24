---
title: "Farbe für ML: Aufgaben- und Nachweisvertrag"
description: "Farbrichtlinien für ML sind ein aufgabenspezifischer Vertrag über Darstellung und Nachweise: Benennen Sie die Quellcodierung, Beleuchtungs- oder Betrachtungsannahmen, die Zieltransformation, die Absicht der Palette und den Zweck der menschlichen Überprüfung. Künstlerische Harmonie, spektrale Bezeichnungen und psychologische Assoziationen sind Hypothesen, keine universellen Labels oder Modellsteuerungen."
category: reference
tags: [color, machine-learning, colorimetry, palette, data-provenance, evaluation, color-management]
aliases: ["Color Theory", "Color Reference for Diffusion"]
level: 3
source_sha256: 3adc83a62eea23f181df5083f46cdc2d8237c089c71fb0817392a7d854a4b89c
translation: machine
translated_at: '2026-10-24'
---
# Farbe für ML: Aufgaben- und Nachweisvertrag {#color-for-ml-task-and-evidence-contract}

Farbe ist in einem ML-Workflow kein einheitliches Merkmal. Eine Beschreibung einer Palette, geräteabhängige RGB-Werte, eine kalibrierte farbmetrische Messung und eine redaktionelle Präferenz beantworten unterschiedliche Fragen. Benennen Sie die Darstellung und die Zielaufgabe, bevor Sie Farbe als Trainingssignal, Steuergröße, Bewertung oder Qualitätsaussage verwenden.

## Nachweistypen trennen {#separate-the-evidence-types}

| Verwendung | Was sie stützen kann | Was sie allein nicht belegen kann |
|---|---|---|
| Farbmanagementerfasste Aufnahme oder Zielwert | eine gemessene Transformation unter deklarierten Bedingungen | eine universelle Erscheinung unter jeder Lichtquelle oder jedem Display |
| Paletten- oder Harmoniebriefing | eine genehmigte redaktionelle Absicht | ein objektives Qualitäts- oder psychologisches Wahrheitslabel |
| Prompt oder Referenzbild | eine angeforderte visuelle Richtung | deterministische Farbsteuerung über Modellversionen hinweg |
| Annotatorenpräferenz | eine begrenzte Prüfentscheidung mit Bewertungsschema und Kontext | eine universelle menschliche Reaktion oder die Ableitung geschützter Merkmale |

[CIE Colorimetry](https://www.cie.co.at/publications/colorimetry-4th-edition) beschreibt standardisierte farbmetrische Grundlagen und verweist auf Modelle der Farberscheinung. Das stützt eine explizite Darstellung sowie explizite Betrachtungsannahmen; es macht künstlerische Positionen im Farbkreis, Wellenlängenbezeichnungen oder kulturelle Assoziationen nicht zu universellen Labels für ein Modell.

## Die Datendarstellung festlegen {#bind-the-data-representation}

Dokumentieren Sie für jeden Trainings- oder Evaluierungsdatensatz:

- Quelldatei und Profil, Decodierung, Transferfunktion und Arbeitsdarstellung;
- Beleuchtungs- oder Betrachtungsannahmen, sofern die gemessene Erscheinung relevant ist;
- jede Revision von ICC-, OpenColorIO- oder sonstigen Transformations- bzw. Konfigurationsdateien;
- Zuschnitt, Größenänderung, Tone Mapping, Gamut-Mapping und Richtlinie für Farbaugmentierung;
- Herkunft und Rechte von Palette bzw. Referenz sowie die urheberrechtliche Absicht; und
- Bewertungsschema, Annotatorenkontext, Unsicherheit und Ausschlussrichtlinie.

Die [ICC-Profilarchitektur](https://www.color.org/getting-started/) und das [OpenColorIO-Konfigurationsmodell](https://opencolorio.readthedocs.io/en/latest/guides/authoring/authoring.html) machen Transformationen explizit. Wenden Sie dieselbe Sorgfalt auf die Datenaufnahme an: Unbeschriftete RGB-Werte aus gemischten Quellen dürfen nicht als einheitlicher kalibrierter Farbraum behandelt werden.

## Steuerungen für die benannte Aufgabe entwerfen {#design-controls-for-the-named-task}

Ein Paletten-Controller lässt sich gegen eine genehmigte Zielpalette oder ein Referenzbild evaluieren. Ein Farbkorrekturmodell lässt sich gegen quellenausgerichtete Messungen evaluieren. Ein generatives Modell lässt sich daraufhin prüfen, ob seine Ausgabe einer zulässigen visuellen Richtung folgt. Jede dieser Aufgaben braucht einen eigenen Abnahmetest.

Nehmen Sie nicht an, dass ein Farbname auf einen festen Gerätewert abgebildet wird, dass ein Textprompt einen Farbton über Checkpoints hinweg identisch steuert oder dass eine Wide-Gamut-Absicht einen reinen sRGB-Quell- bzw. Ausgabepfad überlebt. Fixieren Sie Modell, Tokenizer bzw. Prompt-Prozessor, Bildpipeline und Ausgabetransformation, wenn Sie eine reproduzierbare Farbaussage treffen.

## Evaluieren, ohne menschliche Fakten zu erfinden {#evaluate-without-inventing-human-facts}

Teilen Sie Daten nach Originalasset, Aufnahmesitzung, Ableitungskette und Referenzpalette auf, damit nahezu identische Duplikate keine Farbziele in Holdout-Mengen einschleusen können. Testen Sie mit der tatsächlichen Auslieferungstransformation und prüfen Sie Verläufe, neutrale bzw. Zielbereiche, Gamut-Verhalten, Materialidentität, Text und geschützte Bereiche.

Farbe kann eine redaktionelle Prüfung beeinflussen, doch verwenden Sie sie nicht, um auf Gesundheit, Emotion, ethnische Herkunft, Attraktivität oder ein anderes sensibles Merkmal zu schließen. Psychologische oder kulturelle Farbassoziationen sind kontextabhängige Hypothesen, die eigene Einwilligung, ein eigenes Studiendesign und eine begrenzte Interpretation erfordern; sie sind keine automatischen Trainingslabels.

## Freigabe-Gate {#release-gate}

Geben Sie eine farbbewusste ML-Funktion nur frei, wenn sie eine identifizierte Darstellung, nachvollziehbare Transformationen, autorisierte Daten, quellendisjunkte Evaluierung, Herkunftsnachweis der Ausgabe und eine aufgabenspezifische menschliche Prüfung aufweist. Kann der Workflow nicht zeigen, ob ein Ergebnis eine kalibrierte Korrektur, einen angeforderten Stil oder eine plausible Generierung darstellt, kennzeichnen Sie es als prüfbaren visuellen Vorschlag und nicht als faktische Farbrekonstruktion.

## Verwandte Seiten {#related-pages}

- [[color-space-and-gamma-reference]]
- [[color-correction-by-numbers]]
- [[color-checker-and-white-balance]]
- [[style-reference-ux]]
