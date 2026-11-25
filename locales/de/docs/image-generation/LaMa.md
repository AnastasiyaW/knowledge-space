---
title: "LaMa: Auflösungsrobustes Inpainting großer Masken"
description: "LaMa ist ein Inpainting-Modell mit Fourier-Faltungen für große Masken und Auflösungsgeneralisierung; verwenden Sie es mit einem kompatiblen Checkpoint und prüfen Sie die Textur-Kontinuität separat von der semantischen Wiederherstellung von Objekten."
category: models
tags: [inpainting, ffc, fourier, large-mask, samsung, feed-forward, resolution-robust]
aliases: ["Large Mask Inpainting", "Big-LaMa"]
level: 2
source_sha256: 98c7d5e462b0d8a64dda4074ead11d0088491fa16af4c75ec1284e2f77c411e3
translation: machine
translated_at: '2026-10-24'
---
# LaMa: Auflösungsrobustes Inpainting großer Masken {#lama-resolution-robust-large-mask-inpainting}

**Stand der Prüfung: 2026-09-04.** LaMa ist eine Feed-Forward-Inpainting-Methode für große fehlende Bereiche und hochauflösende Bilder. Die Originalarbeit kombiniert Fast Fourier Convolutions (FFC), einen perzeptuellen Verlust mit großem rezeptivem Feld und große Trainingsmasken. Ihr starkes Verhalten bei der Vervollständigung von Textur und Struktur macht sie zu einer nützlichen Baseline, sie ist jedoch kein deterministisches System zur Objektrekonstruktion.

## Warum Fourier-Faltungen wichtig sind {#why-fourier-convolutions-matter}

Eine FFC-Schicht teilt die Merkmalsverarbeitung in einen lokalen und einen globalen Pfad auf. Der globale Pfad nutzt eine Verarbeitung im Fourier-Raum, sodass eine Schicht Informationen über das gesamte Bild hinweg einbeziehen kann und nicht nur eine kleine räumliche Nachbarschaft. In der LaMa-Arbeit wird dieses breitere rezeptive Feld mit großen Masken und einem perzeptuellen Zielkriterium kombiniert, um die Vervollständigung schwieriger Lücken und periodischer Strukturen zu verbessern.

Das Quell-Repository gibt an, dass das Modell auf deutlich höhere Auflösungen als seine Trainingsauflösung generalisieren kann. Behandeln Sie dies als Fähigkeit, die auf den vorgesehenen Bildgrößen getestet werden muss, und nicht als Garantie, dass beliebige Eingaben im Megapixelbereich feine Typografie, Schmuckfacetten, Gesichter oder die Identität von Objekten bewahren.

## Einsatz für die passende Restaurierungsklasse {#use-it-for-the-right-restoration-class}

LaMa ist ein guter Kandidat, wenn das Akzeptanzkriterium ein kohärenter Hintergrund, eine Textur oder die Kontinuität einfacher Strukturen ist:

- ein maskiertes, unerwünschtes Objekt von einem texturierten oder repetitiven Hintergrund entfernen;
- eine große visuelle Lücke füllen, wenn ausreichend Kontext im Quellbild vorhanden ist;
- eine schnelle, konservative Baseline erzeugen, bevor eine aufwendigere generative Bearbeitung erfolgt.

Verwenden Sie einen separaten Pfad für semantische Bearbeitung oder manuelle Komposition, wenn die Aufgabe ein exaktes Logo, lesbaren Text, die Identität einer bestimmten Person oder ein sicherheitskritisches Objekt erfordert. Eine sauber aussehende Füllung ist kein Beleg dafür, dass der entfernte oder rekonstruierte Inhalt korrekt ist.

## Reproduzierbares Lauf-Protokoll {#reproducible-run-record}

Das Upstream-Repository veröffentlicht mehrere Modellkonfigurationen und verlinkt Checkpoints; einige historische Download-Links haben sich geändert. Bewahren Sie für jeden Lauf Folgendes auf:

1. Repository-Revision sowie Herkunft und Digest des exakten Checkpoints;
2. Bildvorverarbeitung, Methode zur Maskenerstellung und Eingabeauflösung;
3. Regel für die Komposition der Ausgabe, insbesondere ob unmaskierte Pixel aus dem Original stammen;
4. Bild vorher/nachher, Maske und ein menschliches Akzeptanzergebnis;
5. einen Rückgriff auf das unveränderte Quellbild, wenn die Füllung eine kritische Grenze überschreitet.

Drittanbieter-Apps, Portierungen und ComfyUI-Nodes, die vom Projekt aufgeführt werden, sind eigenständige Integrationen. Prüfen Sie deren Modellquelle, Datenschutzverhalten und Lizenz, bevor Sie sie als gleichwertig mit der Upstream-Implementierung behandeln.

## Lizenzgrenze {#license-boundary}

Das geprüfte Quell-Repository `advimman/lama` enthält eine Apache-2.0-Lizenz. Heruntergeladene Checkpoints, Nutzungsbedingungen von Modell-Hosting-Diensten und Drittanbieter-Portierungen können eigene Bedingungen hinzufügen. Prüfen Sie daher das genaue Artefakt vor Verteilung oder kommerziellem Einsatz.

## Referenzen {#references}

- [LaMa official repository](https://github.com/advimman/lama)
- [LaMa paper](https://arxiv.org/abs/2109.07161)
- [LaMa project page](https://advimman.github.io/lama-project/)
