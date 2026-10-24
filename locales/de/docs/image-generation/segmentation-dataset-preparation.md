---
title: "Vorbereitung von Segmentierungsdatensätzen: Lineage- und Supervisionsvertrag"
description: "Die Vorbereitung von Segmentierungsdatensätzen ist ein Lineage- und Supervisionsvertrag: Quelle und Nutzungsrechte, Annotationsrichtlinie und Mask-Semantik, gruppendisjunkte Splits, Augmentierungs- und Interpolationsverhalten, Klassenabdeckung und Release-Metriken werden verbindlich festgelegt. Bei Leakage, ungeprüften Labels oder inkompatiblen Targets bricht die Verarbeitung ab."
category: techniques
tags: [segmentation, dataset, annotations, masks, augmentation, splits, provenance, evaluation]
aliases: ["Binary Small-Object Segmentation Dataset", "Segmentation Data Preparation"]
level: 2
source_sha256: a2baa617d2e7f0fb9e993eb5f06c7a160d7b3df6705ba50171ac8a923d3499df
translation: machine
translated_at: '2026-10-24'
---
# Vorbereitung von Segmentierungsdatensätzen: Lineage- und Supervisionsvertrag {#segmentation-dataset-preparation-lineage-and-supervision-contract}

Ein Segmentierungsdatensatz besteht nicht nur aus Bildern und Masken. Er ist ein versioniertes Supervisionssystem: Quellmaterial, Nutzungsrechte, Annotationsrichtlinie, Mask-Semantik, Sampling-Regeln, Split-Einheiten, Transformationen und Evaluation müssen zueinander passen. Ein Modell kann ansprechende Overlays erzeugen, obwohl es auf Leakage, nicht passenden Masken oder Labels trainiert wurde, die die beabsichtigte Aufgabe nicht abbilden.

## Sample- und Annotationsvertrag definieren {#define-the-sample-and-annotation-contract}

Für jedes Quellmaterial und jeden abgeleiteten Crop werden eine stabile Quell- bzw. Gruppen-ID, der Asset-Digest, Nutzungsrechte und zulässiger Zweck, Lineage von Aufnahme und Vorverarbeitung, Annotationsversion und Review-Status, Klassentaxonomie, Geometrie, Mask-Kodierung, Ignore-/Unknown-Semantik sowie gegebenenfalls Konfidenz oder Ausschlussgrund gespeichert. Es wird festgelegt, ob eine Maske binär, multiklassig, instanzbewusst, weich oder nur teilweise gelabelt ist. Die Klassenbedeutung wird niemals allein aus einem 8-Bit-Wert abgeleitet.

Quellbild, Maske, Overlay, Metadaten und Klassenzählungen werden gemeinsam geprüft. Nicht lesbare, doppelte, mehrdeutige oder ungeprüfte Labels werden in Quarantäne gesetzt und nicht stillschweigend als Hintergrund umgewandelt.

## Entlang der tatsächlichen Leakage-Einheit splitten {#split-by-the-real-leakage-unit}

Alle Crops, Augmentierungen, Frames, Near-Duplicates und wiederholten Ansichten, die auf dieselbe kausale Quelle zurückgehen, müssen in derselben Split-Gruppe verbleiben. Als Gruppe kommen je nach Fall ein Quellbild, eine Person, ein Produkt, eine Szene, eine Session, ein Zeitfenster oder ein Aufnahmegerät infrage. Es wird dokumentiert, warum diese Gruppe die erwartete Grenze des Deployments abbildet.

[scikit-learn's GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html) liefert nicht überlappende Gruppen, kann jedoch weder die richtige Gruppendefinition wählen noch nachweisen, dass zwei Assets keine Duplikate sind. Nach jedem Split werden Manifeste gespeichert und sichergestellt, dass keine Gruppe, kein Asset-Digest und keine abgeleitete Lineage zwischen Train, Validation und Test wechselt. Die Klassenabdeckung wird nach dem Gruppieren geprüft. Ein seltener Split wird nicht dadurch repariert, dass verwandte Crops in mehrere Splits gelangen.

## Bilder und Supervision synchron halten {#keep-images-and-supervision-synchronized}

Jede räumliche Transformation muss alle relevanten Targets mit derselben gesampelten Geometrie aktualisieren. Jede reine Pixel-Transformation muss gegen die Target-Semantik geprüft werden. [Albumentations' Target-Dokumentation](https://albumentations.ai/docs/2-core-concepts/targets/) unterscheidet bildartige und maskenartige Targets und erklärt, warum kategoriale Masken in der Regel eine maskensichere Interpolation benötigen. Die genaue Bibliotheksversion und die Pipeline-Konfiguration gehören trotzdem in das Dataset-Release.

Crop-, Pad- und Resize-Interpolation, Rotation, Behandlung der Maskenwerte, ignorierte Pixel, pro Split aktivierte Transformationen sowie das Target-Routing für Boxen, Instanzen, Tiefe oder Metadaten werden dokumentiert. Eine Transformation, die für das deklarierte Target nicht unterstützt wird, muss fehlschlagen, statt plausible, aber fehlausgerichtete Supervision zu erzeugen.

## Das veröffentlichte Dataset evaluieren, nicht einen bequemen Crop {#evaluate-the-released-dataset-not-a-convenient-crop}

Vor dem Tuning von Schwellenwerten oder Losses wird ein quelldisjunktes Testset eingefroren. Berichtet werden klassenweise und gruppenbezogene Metriken, Sample-Zahlen, Unsicherheit bzw. Abdeckung sowie qualitative Overlays in der Auslieferungsauflösung. Modell, Auflösung, Loss, Klassengewichtung, Schwellenwert und Augmentierung werden aus diesem versionierten Experiment abgeleitet. Ein universelles Setup für binäre Ausgaben oder ein allgemeingültiges Loss-Gewicht für seltene Objekte existiert nicht.

Bei kleinen oder sicherheitsrelevanten Zielobjekten werden falsch negative und falsch positive Ergebnisse, Grenzen und Fälle mit leeren Masken nach Quellgruppe untersucht. Eine Fehlertaxonomie wird geführt, damit künftige Annotationen und Datenerhebungen verbessert werden können, ohne historische Labels umzuschreiben.

## Fehlerfälle und Release-Grenze {#failure-and-release-boundary}

Ein Dataset-Release wird blockiert, wenn Nutzungsrechte oder Label-Richtlinie fehlen, Gruppenüberlappungen erkannt werden, Transformationen inkompatibel sind, Klassen- oder Mask-Semantik mehrdeutig ist, Testbeispiele für das Tuning verwendet wurden oder Annotationen die erforderliche Prüfung nicht durchlaufen haben. Datensätze werden nicht stillschweigend verworfen, unbekannte Pixel nicht umetikettiert, Splits nicht ersetzt und Instanzen nicht in den Hintergrund überführt, nur damit eine Metrik besser aussieht.

## Verwandte Seiten {#related-pages}

- [[in-context-segmentation]]
- [[rights-first-text-to-mask-training]]
- [[defect-detection-small-objects]]
- [[paired-training-for-restoration]]
