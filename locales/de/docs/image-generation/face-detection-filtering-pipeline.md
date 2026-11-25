---
title: "Gesichtserkennung und Filterung: Prüfpipeline für Kandidaten"
description: "Die Gesichtsfilterung ist eine provenienzerhaltende Pipeline zur Auswahl von Kandidaten; Detektor-Boxen und Landmarken unterstützen die Prüfung, belegen aber weder Identität, Einwilligung, Bildrealismus noch die Eignung für das Training."
category: workflows
tags: [face-detection, dataset-curation, provenance, quality-control, privacy, review]
aliases: ["Face Detection & Filtering Pipeline", "Face Dataset Review"]
level: 2
source_sha256: 8703837c0cf152ad9e399e0f68979602911ba1ff110e339913b9e037f2a9a5bb
translation: machine
translated_at: '2026-10-24'
---
# Gesichtserkennung und Filterung: Prüfpipeline für Kandidaten {#face-detection-and-filtering-candidate-review-pipeline}

Die Gesichtserkennung sollte Prüfkandidaten und strukturierte Nachweise liefern, nicht
automatisch die Aussage, dass ein Bild eine reale Person zeigt, eine verwendbare
Einwilligung vorliegt oder das Bild für das Training geeignet ist. Die Filterentscheidung
muss über eine Eingabe und eine festgelegte Richtlinie nachvollziehbar bleiben.

## Inventarisierung vor der Inferenz {#inventory-before-inference}

Erstellen Sie für jedes Asset ein unveränderliches Eingabe-Manifest mit Digest,
Quellort, Lizenz- oder Einwilligungsnachweis, Aufnahmezeitpunkt und Zugriffsklasse.
Ersetzen Sie dieses Manifest nicht durch einen Detektor-Score. Es bleibt die maßgebliche
Instanz für Rechte, Aufbewahrung und nachgelagerte Prüfung.

## Stufe der Kandidatenerkennung {#candidate-detection-stage}

Führen Sie einen versionierten Detektor aus und speichern Sie den Eingabe-Digest,
die Modellrevision, Box, Konfidenz, Zuschnittkoordinaten und den Fehlerstatus. Der
[MediaPipe Face Detector](https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector/python)
unterstützt Bild- und Videoeingaben und liefert Gesichtspositionen mit sechs Keypoints:
die Augen, die Nasenspitze, den Mund sowie die Ohr-Tragus-Punkte. Diese Ausgaben können
die Prüfung von Zuschnitt und Ausrichtung unterstützen.

Sie belegen weder die Identität, die Einwilligung, das Alter oder die Emotion einer Person
noch, ob das abgebildete Gesicht fotografisch oder synthetisch ist. Behandeln Sie die
Modellkonfidenz als Rangordnungssignal, dessen Schwellenwert lokal kalibriert wird, nicht
als allgemeines Akzeptanzkriterium.

## Qualitäts- und Relevanzprüfungen {#quality-and-relevance-gates}

Legen Sie zuerst den Zielzweck fest und messen Sie dann nur die relevanten Eigenschaften:

1. **Bildausschnitt:** ausreichende sichtbare Fläche und ein Zuschnitt, der zur beabsichtigten
   Trainings- oder Bearbeitungsaufgabe passt.
2. **Bildqualität:** Schärfe, Kompressionsschäden, Clipping, Verdeckungen und Auflösung,
   geprüft anhand lokal gelabelter Beispiele.
3. **Bearbeitbarkeit:** nur wenn die deklarierte Aufgabe sie erfordert; die Begründung des
   Prüfers wird festgehalten, statt sie aus einem allgemeinen Gesichts-Score abzuleiten.
4. **Rechte und Datenschutz:** Nachweise zu Einwilligung und Lizenz, Aufbewahrungsklasse und
   Freigabe für die beabsichtigte abgeleitete Nutzung.

Automatisierte Scores können die Warteschlange vorsortieren, unsichere Fälle sollten jedoch
in der Prüfung verbleiben und dürfen nicht stillschweigend akzeptiert oder verworfen werden.

## Ähnlichkeit, Duplikate und Splits {#similarity-duplicates-and-splits}

Verwenden Sie wahrnehmungsbasierte oder Embedding-Ähnlichkeit, um Duplikat- und
Near-Duplicate-Gruppen vorzuschlagen. Bewahren Sie jeden Quelldatensatz auf, protokollieren
Sie das Gruppierungsmodell und den Schwellenwert, und lassen Sie eine Prüfperson oder eine
eindeutige Richtlinienregel entscheiden, welche Repräsentation verwendet werden darf. Ein
Ähnlichkeitswert ist niemals ein Beweis dafür, dass zwei Bilder dieselbe Person zeigen.

Für die Modellbewertung teilen Sie nach Quelle, Aufnahmesitzung oder bekannter
Subjektgruppe, sofern verfügbar. So wird verhindert, dass nahezu identische Bilder zwischen
Trainings- und Validierungspartitionen gelangen. Dokumentieren Sie die Split-Regel und
ihre Ausnahmen.

## Ausgabeschema und Freigabeentscheidung {#output-schema-and-release-decision}

Jedes Ergebnis sollte Folgendes enthalten:

- Eingabe-Digest und Verweis auf die Provenienz;
- Revisionen des Detektors bzw. Qualitätsmodells sowie die Rohausgaben;
- Entscheidung (accept, review oder reject) mit einem Begründungscode;
- Prüfer- oder Richtlinienversion; und
- nachgelagerte Einschränkungen, einschließlich Lösch- und Aufbewahrungspflichten.

Nur ein accept-Datensatz mit Rechtenachweis und deklariertem Nutzungsumfang darf in ein
Trainingsset für Gesichtsbearbeitung aufgenommen werden. Alle übrigen Datensätze bleiben
nachvollziehbar, um Korrektur oder Prüfung zu ermöglichen.

## Verwandte Seiten {#related-pages}

- [[face-beautify-edit-lora]]
- [[rights-first-text-to-mask-training]]
- [[diffusion-lora-training]]
