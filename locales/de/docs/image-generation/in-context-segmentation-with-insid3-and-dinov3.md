---
title: "INSID3 mit DINOv3: Vertrag für Kandidatenmasken"
description: "INSID3 mit DINOv3 überträgt eine bereitgestellte Referenzmaske über eine benannte, eingefrorene Backbone-Version als Kandidaten-Segmentierung, nicht als Ground Truth. Vor der Verwendung sind Repository- und Modellrevisionen, Lizenz und Zugriff, Herkunft von Referenz und Maske, Vorverarbeitung und Auflösung, Konfiguration der Positions-Bias-Korrektur, Unsicherheitsrichtlinie sowie quellendisjunkte Prüfung festzulegen."
category: reference
tags: [segmentation, insid3, dinov3, candidate-masks, provenance, review]
aliases: ["In-Context Segmentation with INSID3 and DINOv3", "INSID3 DINOv3 Segmentation"]
level: 2
source_sha256: 0ac75986a9b71c5ebc6d0213f6e9c9ad59a4b68fbdb5ff706c5c9316fa356804
translation: machine
translated_at: '2026-10-24'
---
# INSID3 mit DINOv3: Vertrag für Kandidatenmasken {#insid3-with-dinov3-candidate-mask-contract}

Das upstream [INSID3-Repository](https://github.com/visinf/INSID3) beschreibt
eine trainingsfreie In-Context-Segmentierungsmethode, die mit einem eingefrorenen
DINOv3-Backbone und einem bereitgestellten Referenzbild/einer Referenzmaske arbeitet.
Das [DINOv3-Referenzrepository](https://github.com/facebookresearch/dinov3)
veröffentlicht die Backbone-Artefakte. Zusammen rechtfertigen sie den Test der
benannten Version; sie machen eine vorhergesagte Maske jedoch nicht zu Ground
Truth, zu Einwilligungsnachweis, Identitätsnachweis, medizinischer Schlussfolgerung
oder automatisch erzeugtem Trainingslabel.

## Exakte Version festlegen {#bind-the-exact-release}

Für jede Kandidatenmaske sind folgende Angaben zu dokumentieren:

- INSID3-Repository- und Code-Revision, DINOv3-Modell-/Gewichtsbezeichner,
  Artefakt-Digest, Lizenz- und Zugriffsbedingungen sowie Umgebungs- und
  Abhängigkeitsprotokoll;
- Digests von Referenzbild und Referenzmaske, Urheber- und Rechtenachweis,
  Klassen-/Teildefinition, Zuschnitt/Ausrichtung/Vorverarbeitung und Prüfung der
  Referenzqualität;
- Digest des Zielobjekts, Bezeichner der Zieldomäne, Vorverarbeitung,
  Eingabeauflösung, Farb- und Ausrichtungsrichtlinie sowie Abbildung der Ausgabe
  auf Quellpixel;
- dokumentierte Konfiguration der Positions-Bias-Korrektur bzw. Debiasing,
  Verfeinerung, Schwellenwerte und Nachverarbeitung, einschließlich der
  Abweichungen vom upstream-Standard;
- Ausgabemaske, Unsicherheits- bzw. Fehlersignale (sofern verfügbar),
  Entscheidung der prüfenden Person, Korrekturartefakt und Provenienzverweis;
  sowie
- quellendisjunkte Validierungsaufteilung und aufgabenspezifische Nachweise
  zu Qualität und Erhaltung.

Ein lokaler Adapter, eine abgeleitete interne Feature-Struktur oder ein
Monkey-Patch darf nicht an die Stelle der upstream-Schnittstelle treten, sofern
diese Integration nicht eine eigene versionierte Implementierung und einen
eigenen Evaluationsnachweis besitzt.

## Kandidatenmasken vor der Verwendung prüfen {#review-candidate-masks-before-use}

Dünne Strukturen, kleine oder wiederkehrende Objekte, Verdeckungen, Spiegelungen,
transparente Materialien, Unschärfe, Schatten, schwierige Grenzen und geschützte
Bereiche sind im Koordinatensystem der Quelle zu prüfen. Eine plausibel wirkende
Grenze kann dennoch semantisch falsch oder für die vorgesehene Bearbeitung bzw.
den Datensatz unzulässig sein.

Beim Aufteilen der Evaluationsdaten sind Quellassets und Ableitungen gemeinsam
zu behandeln. Referenzbild, nahezu doppelte Zuschnitte, dasselbe Motiv oder
verwandte Ableitungen dürfen nicht zwischen Abstimmung und zurückgehaltener
Prüfmenge verschleppt werden. Transferqualität, Fehlererkennung,
Domänenverschiebung, Korrekturen durch Prüfende und betriebliche Eskalation
sind getrennt zu berichten.

## Fehlergrenze {#failure-boundary}

Ist die Herkunft von Referenz/Maske unvollständig, sind Modellversion oder
Lizenz unbekannt, weicht die Vorverarbeitung vom dokumentierten Lauf ab, liegt
das Ziel außerhalb der Verteilung oder kann die Prüfung einen geschützten
Bereich nicht validieren, ist die Maske im sichtbaren Prüfstatus zu belassen
und eine manuelle Annotation anzufordern. Sie darf nicht stillschweigend
übernommen, umetikettiert oder als Quelle sachlicher, identitätsbezogener,
medizinischer oder freigabereifer Wahrheit verwendet werden.

## Verwandte Seiten {#related-pages}

- [[in-context-segmentation]]
- [[rights-first-text-to-mask-training]]
- [[defect-detection-small-objects]]
- [[paired-training-for-restoration]]
