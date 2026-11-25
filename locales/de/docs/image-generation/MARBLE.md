---
title: "MARBLE: Materialrekomposition und Blending"
description: "MARBLE führt Materialübertragung, Blending und parametrische Materialbearbeitung über CLIP-Space-Steuerungen eines vortrainierten Bildgenerators durch; Objektgeometrie, Beleuchtung und Lizenzen der Artefakte müssen für jeden Workflow geprüft werden."
category: models
tags: [material-editing, clip-space, stability-ai, sdxl, ip-adapter, roughness, metallic, transparency, pbr]
aliases: ["Material Recomposition and Blending"]
level: 2
source_sha256: 9179341c0916291d9b98aa02639cc0df4ea2fbd27c7db7cd068f1ef724d22d17
translation: machine
translated_at: '2026-10-24'
---
# MARBLE: Materialrekomposition und Blending {#marble-material-recomposition-and-blending}

**Stand der Prüfung: 2026-09-04.** MARBLE ist die veröffentlichte Methode von Stability AI zur Materialbearbeitung. Sie leitet Materialrepräsentationen im CLIP-Space ab und nutzt diese, um ein vortrainiertes Text-zu-Bild-System für drei verwandte Operationen zu steuern: Materialübertragung anhand eines Beispiels, Blending zwischen Materialreferenzen und parametrische Anpassung ausgewählter Materialattribute.

## Was sich damit darstellen lässt {#what-it-can-express}

Die Arbeit zeigt die Steuerung von Eigenschaften wie Rauheit, metallische Erscheinung, Transparenz und Glow. Die öffentliche Implementierung umfasst:

- ein Notebook für Material-Blending;
- ein Notebook für parametrische Steuerung;
- eine Gradio-Demo;
- eine ComfyUI-Erweiterung und einen Beispiel-Workflow.

Das Ziel der Methode ist die visuelle Materialbearbeitung, nicht ein physikalisch kalibrierter PBR-Solver. Ein Ergebnis, das metallischer oder transparenter wirkt, kann dennoch inkonsistente Reflexionen, veränderte Geometrie oder unplausible Beleuchtung aufweisen. Die Ausgabe ist als Bildgenerierungsergebnis zu behandeln, das aufgabenspezifisch geprüft werden muss.

## Architektur und Abhängigkeitsgrenze {#architecture-and-dependency-boundary}

MARBLE baut seine Materialblöcke auf der InstantStyle-Codebasis auf und verwendet einen vortrainierten Bildgenerator sowie zugehörige Artefakte zur Bildkonditionierung. Die gesamte Kette ist explizit festzuhalten:

1. Repository-Revision von MARBLE und deren Dependency-Lock;
2. ausgewählte Revisionen von Basisgenerator, Bild-Encoder, Adapter und Checkpoint;
3. Quellobjektbild und Materialreferenz(en), mit Berechtigung zur Verarbeitung;
4. Operationstyp – Übertragung, Blending oder parametrische Steuerung – und jeder Steuerwert;
5. Ausgabe und Abnahmenachweis.

Man darf nicht annehmen, dass eine für ein bestimmtes Basismodell, eine Objektkategorie oder ein bestimmtes Lichtsetup abgestimmte Steuerung auf ein anderes übertragbar ist. Die getestete Python-Version und die Notebook-Einstellungen des Upstream-Codes sind Kompatibilitätsnachweise für diesen Release, kein stabiler API-Vertrag.

## Abnahmeprüfungen für Produktbilder {#acceptance-checks-for-product-images}

Für Produkt- oder Schmuckanwendungen sind folgende Punkte getrennt zu prüfen:

| Anforderung | Prüfung |
|---|---|
| Objektidentität und Silhouette | Overlay oder Gegenüberstellung mit dem Original |
| Materialerscheinung | Highlights, Rauheit, Transparenz und Kantenverhalten im vorgesehenen Zuschnitt prüfen |
| Farbe und Belichtung | Vergleich mit kalibrierten Referenzwerten, sofern vorhanden |
| Bearbeitungsumfang | bestätigen, dass Hintergrund, Branding und nicht betroffene Bereiche unverändert blieben |
| Veröffentlichungsrechte | Berechtigung für das Objektfoto und das Materialbeispiel dokumentieren |

Wenn ein Materialattribut numerisch korrekt und nicht nur visuell plausibel sein muss, sind physikalisch basierte Renderings oder messtechnisch kontrollierte Farbmanagement-Workflows zu verwenden.

## Lizenzierung {#licensing}

MARBLE, InstantStyle, der ausgewählte Basisgenerator, Adapter und etwaige Beispielassets können unterschiedlichen Lizenzen und Zugangsbedingungen unterliegen. Vor gehosteter, kommerzieller oder weitergegebener Nutzung sind die aktuellen Bedingungen für jedes Artefakt zu lesen; ein öffentliches Repository gewährt kein pauschales Recht am vollständig zusammengesetzten Workflow.

## Referenzen {#references}

- [MARBLE official repository](https://github.com/Stability-AI/marble)
- [MARBLE paper](https://arxiv.org/abs/2506.05313)
- [MARBLE project page](https://marblecontrol.github.io/)
