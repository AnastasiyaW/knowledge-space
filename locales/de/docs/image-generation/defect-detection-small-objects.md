---
title: "Defekt- und Kleinobjekterkennung: Evidenzvertrag"
description: "Defekt- und Kleinobjekterkennung liefert prüfbare Kandidaten, keine automatische Qualitätswahrheit; binden Sie Modell, Aufnahmeprotokoll, Annotations- oder Normalreferenz-Policy, Slicing- oder Merge-Abbildung, Schwellenwerte und quellendisjunkte Evaluierung, bevor eine Prüf- oder Workflow-Entscheidung getroffen wird."
category: reference
tags: [defect-detection, anomaly-detection, small-objects, inspection, provenance, evaluation, tiling]
aliases: ["Anomaly Detection", "Defect Detection Models", "Small Object Detection"]
level: 3
source_sha256: ce70ab843b008e778197e00f6385e7eb855943a70269c0d37780326c0e7d05d2
translation: machine
translated_at: '2026-10-24'
---
# Defekt- und Kleinobjekterkennung: Evidenzvertrag {#defect-and-small-object-detection-evidence-contract}

Erkennungs- und Anomaliesysteme identifizieren Kandidaten für eine Prüfung. Eine Box, Maske, Heatmap oder ein Score ist kein Nachweis, dass ein Produkt defekt ist, dass eine visuelle Veränderung eingeführt wurde oder dass ein Bild sicher veröffentlicht werden kann. Binden Sie Aufnahmebedingungen, Aufgabendefinition, Modell und Prüfrichtlinie, bevor ein Ergebnis in einer operativen Entscheidung verwendet wird.

## Die Aufgabe explizit wählen {#choose-the-task-explicitly}

| Aufgabe | Erforderliche Supervision oder Referenz | Bedeutung der Ausgabe |
|---|---|---|
| Überwachte Detektion oder Segmentierung | genehmigte Klassentaxonomie und quellenverknüpfte Annotationen | Kandidat für Klasse/Region |
| Anomalieerkennung | eine definierte Normalreferenz-Policy und bekannte Ausschlüsse | Abweichung von dieser Referenzverteilung |
| Vorher/Nachher-Vergleich | ausgerichtete, autorisierte gepaarte Aufnahmen und Änderungspolicy | Kandidat für einen Unterschied |

[EfficientAD](https://anomalib.readthedocs.io/en/v2.0.0/markdown/guides/reference/models/image/efficient_ad.html)
ist in Anomalib als Student-Teacher-Anomaliemethode dokumentiert. Die zugehörige Publikation evaluiert eine bestimmte Modellfamilie auf benannten Datensätzen. Keine dieser Quellen macht eine Anomaliekarte zu einem universellen Defektlabel, legt einen sicheren Schwellenwert für jedes Material fest oder garantiert ein festes Latenz- oder Speicherbudget auf einer anderen Laufzeitumgebung.

## Aufnahme- und Trainingsevidenz binden {#bind-capture-and-training-evidence}

Speichern Sie für jede Probe bzw. jede Normalreferenz:

- Identität des Originalassets bzw. der Aufnahme, Rechte sowie Produkt- oder Szenenumfang;
- Kamera, Objektiv, Abstand, Fokus, Beleuchtung, Hintergrund und Verarbeitungsbedingungen, die sichtbare Textur beeinflussen;
- Aufgabentaxonomie, Einschluss- und Ausschlussbeispiele, Annotationsrevision und Herkunft der Prüfer;
- Modell/Checkpoint, Vorverarbeitung, Eingabeauflösung, Laufzeitumgebung und Schwellenwert-Policy; sowie
- Unsicherheit, verworfene Kandidaten und bekannte Störfaktoren.

Spiegelungen, Kompression, Staub auf dem Aufnahmepfad, Fokusänderungen, Hintergrundreflexionen und Geometrieänderungen können anomal wirken. Halten Sie reale Beobachtungen getrennt von synthetischen Defekten, und verwenden Sie eine Augmentation nicht als Nachweis, dass ein Defektdetektor für reale Bedingungen validiert ist.

## Slicing als Koordinatenvertrag behandeln {#treat-slicing-as-a-coordinate-contract}

[SAHI](https://obss.github.io/sahi/guides/sliced-inference/) dokumentiert überlappende Slices, die Detektion pro Slice und das Zusammenführen zurück in Koordinaten des Gesamtbilds. Wenn eine hochauflösende Prüfung mit Kacheln arbeitet, erfassen Sie zusammen mit der Vorhersage die Kachelgeometrie, Überlappung, Eingabetransformation, Koordinatenabbildung, Merge- bzw. Unterdrückungsregel und Randbehandlung. Das Zusammenführen von Detektionen aus Kacheln validiert weder eine Anomalie-Heatmap noch eine Pixel-Bearbeitungsnaht.

Bewerten Sie Kandidaten am Originalbild. Eine verkleinerte Vorschau kann genau das winzige Objekt oder Oberflächenartefakt verbergen, dessen Markierung das System beansprucht.

## Für die Zielumgebung validieren {#validate-for-the-target-environment}

Teilen Sie Trainings-, Tuning- und Testdaten nach Originalasset, Produkt/Motiv, Aufnahmesitzung und Ableitungskette auf. Holdout-Mengen müssen die Material-, Skalen-, Beleuchtungs- und Aufnahmevariationen enthalten, die im Betrieb zu erwarten sind. Berichten Sie aufgabenspezifische Fehleranalysen, einschließlich der Belastung durch falsche Kandidaten und übersehener kritischer Fälle, statt AUROC-, mAP-, VRAM- oder Latenzwerte aus einem Benchmark oder von einem anderen Gerät zu übernehmen.

Prüfen Sie vorhergesagte Regionen gegen das Quellbild und die genehmigte Aufgabendefinition. Halten Sie Schwellenwertänderungen versioniert, und validieren Sie erneut, wenn sich Kamera, Beleuchtung, Vorverarbeitung, Kachelplan, Modell oder Laufzeitumgebung ändern.

## Freigabe-Gate {#release-gate}

Veröffentlichen Sie nur prüfbare Kandidaten mit Modell- und Konfigurationsherkunft sowie einem sichtbaren Unsicherheits- bzw. Fehlerzustand. Lehnen Sie Inventar nicht automatisch ab, entfernen Sie keine Retusche-Details, und treffen Sie kein Sicherheits- oder Qualitätsurteil allein auf Grundlage eines Detektor-Scores. Verlangt die Policy eine automatische Aktion, definieren Sie vor der Aktivierung deren begrenzte Befugnis, Gegenprüfung, Prüfprotokoll und Rollback-Pfad.

## Verwandte Seiten {#related-pages}

- [[tiled-inference]]
- [[low-vram-inference-strategies]]
- [[skin-retouch-pipeline]]
- [[synthetic-dataset-pipeline]]
