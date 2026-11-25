---
title: "SpatialEdit-16B: Geometrie- und Evaluierungsvertrag"
description: "SpatialEdit-16B ist ein Forschungsrelease für geometriegesteuerte Bildbearbeitung; das exakte Code-/Modell-Artefakt und die Bedingungen binden, Autorität über Quell- und Zielasset, Objekt-/Kameratransformations- und Koordinatenvertrag, Vorverarbeitung/Laufzeit, geometriebewusste und Erhaltungsevaluierung sowie menschliche Prüfung vor der Nutzung."
category: techniques
tags: [spatialedit, image-editing, geometry, camera-control, provenance, evaluation]
aliases: ["SpatialEdit-16B Geometric Control", "SpatialEdit Geometry Editing"]
level: 2
source_sha256: 5b010a5ade22bcc16253039f2182b7301a2f6f7f0a0b502ff490383a168b7331
translation: machine
translated_at: '2026-10-24'
---
# SpatialEdit-16B: Geometrie- und Evaluierungsvertrag {#spatialedit-16b-geometry-and-evaluation-contract}

Das [SpatialEdit-Paper](https://arxiv.org/abs/2604.04911) stellt einen
geometriegesteuerten Benchmark für Bildbearbeitung, synthetische Supervision
und eine SpatialEdit-16B-Baseline für objektzentrierte und kamerazentrierte
Bearbeitungen vor. Das [offizielle Release](https://github.com/EasonXiao-888/SpatialEdit)
veröffentlicht Code, Checkpoints, Benchmark-Assets und separate externe
Voraussetzungen. Dies unterstützt die Evaluierung des benannten Releases; es
macht aber ein plausibles Bild nicht zu einem Nachweis, dass die geforderte
Geometrie eingehalten wurde.

## Release und Bearbeitungsvertrag binden {#bind-the-release-and-edit-contract}

Für jede evaluierte oder veröffentlichte Bearbeitung sind festzuhalten:

- Repository-Revision, Modell-/Checkpoint-Kennung und Digest, Code- und
  Artefakt-Bedingungen, Dependency-/Laufzeitprotokoll sowie jede externe
  Voraussetzung, die von der gewählten Konfiguration verwendet wird;
- Digest des Quellassets, Nachweis von Eigentum oder autorisierter Bearbeitung,
  Definition von Subjekt/Objekt, geschützte Bereiche und alle untersagten
  semantischen Änderungen;
- Aufgabenklasse: Objektverschiebung, Skalierung, kanonische Rotation oder
  Änderung von Kameraperspektive/Bildausschnitt; Quell- und Zielkoordinatensysteme;
  Zielbox, Pose, Zuschnitt, Auflösung und Orientierungskonvention;
- Eingabevorverarbeitung, VAE-/Modellpfade, Seed, Scheduler/Einstellungen,
  Output-Digest und Abbildung der Ausgabepixel zurück auf den Quellrahmen; sowie
- Ergebnis der geometrischen Treue, Ergebnis der Erhaltung von Nicht-Zielbereichen,
  Fehlerbeispiele, Entscheidung der prüfenden Person und Schlussfolgerung zur
  zulässigen Nutzung.

Verfügbarkeit des Codes oder eine permissive Repository-Lizenz legen keine
Bedingungen für jeden Checkpoint, jedes Basismodell, jeden Datensatz oder jedes
Quellbild fest. Jeden Autoritätsnachweis separat führen.

## Geometrie und Erhaltung getrennt evaluieren {#evaluate-geometry-and-preservation-separately}

Verwenden Sie held-out, quelldisjunkte Assets, die die erforderlichen
Subjektklassen, Verdeckung, Spiegelungen, feine Konturen, Hintergrundkomplexität
sowie Kamera- und Objekttransformationen abdecken. Bewerten Sie die geforderte
Transformation in dem deklarierten Koordinatensystem und prüfen Sie anschließend
unabhängig Objektidentität, Hintergrundkontinuität, Konsistenz von Beleuchtung
und Schatten, Text, Logos sowie sachliche Produktdetails.

Einen visuellen Präferenzwert nicht mit geometrischer Korrektheit gleichsetzen.
Ein Ergebnis kann kohärent wirken, während Objektposition, Skalierung,
Orientierung oder Perspektivwechsel falsch sind. Mit einer deklarierten Baseline
vergleichen und sowohl erfolgreiche als auch fehlgeschlagene Fälle aufbewahren,
statt nur ansprechende Ausgaben auszuwählen.

## Stolpersteine {#gotchas}

- **Problem:** Ein Prompt kann eine semantisch plausible Szene mit falschem
  räumlichem Ergebnis liefern -> **Lösung:** Die geforderte Box, Pose, den
  Bildausschnitt bzw. die Kamerabeziehung im angegebenen Quell-Koordinatensystem
  prüfen.
- **Problem:** Das offizielle Release enthält Platzhalter-/interne Pfade und
  externe Checkpoint-Voraussetzungen -> **Lösung:** Diese nur in einer
  versionierten lokalen Konfiguration ersetzen und jedes aufgelöste Artefakt
  dokumentieren, bevor ein Lauf als reproduzierbar gilt.
- **Problem:** Es wird angenommen, dass ein allgemeines Bearbeitungsergebnis auf
  eine neue Objekt- oder Kameraoperation übertragbar ist -> **Lösung:** Diese
  Operation auf einem operationsspezifischen held-out-Set evaluieren; nicht aus
  der Modellfamilie ableiten.

## Grenze des Fehlerfalls {#failure-boundary}

Fehlt der Nachweis der Quellautorität, des exakten Releases bzw. der
Bedingungen, der Koordinatendefinition, des Vorverarbeitungsprotokolls oder der
Geometrie- und Erhaltungsprüfung, bleibt die Ausgabe im Prüfstatus. Kein
stilles Ersetzen durch ein anderes Modell, keine Umdeutung einer rein
semantischen Bearbeitung als metrische Steuerung und keine Veröffentlichung als
verifizierte Ansicht oder sachliche Rekonstruktion.

## Verwandte Seiten {#related-pages}

- [[MMDiT]]
- [[flow-matching]]
- [[tile-position-encoding]]
- [[diffusion-inference-acceleration]]
- [[flux-klein-capability-map]]
