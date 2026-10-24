---
title: "Anatomiekorrektur in Diffusionsmodellen"
description: "Anatomiekorrektur ist ein Workflow aus Diagnose, Maskierung, Konditionierung und Inpainting; verwenden Sie geometriebewusste Forschungsmethoden und modellkompatible Bearbeitungswerkzeuge und prüfen Sie danach jede bearbeitete Hand oder Gliedmaße visuell gegen die Quelle."
category: workflows
tags: [anatomy, hands, inpainting, diffusion, image-editing, quality-control, comfyui]
aliases: ["Hand correction", "Diffusion anatomy repair"]
level: 2
source_sha256: d272fa5fbb6e97668e07de397dc146ae328265204bb6b7367d0f9de9cc5a2159
translation: machine
translated_at: '2026-10-24'
---
# Anatomiekorrektur in Diffusionsmodellen {#anatomy-correction-in-diffusion-models}

**Geprüft am: 2026-09-04.** Anatomiekorrektur ist ein lokaler Bildbearbeitungsworkflow für fehlerhafte Hände, Finger, Gesichter oder Gliedmaßen. Sie ist kein universelles Sampler-Preset, und kein Detektor, LoRA oder Inpainting-Modell kann eine generierte Anatomie allein als korrekt bestätigen.

## Die Korrekturschleife {#the-correction-loop}

1. **Quelle in Auslieferungsgröße prüfen.** Bestimmen Sie genau, was falsch ist: Anzahl, Gelenkstruktur, Verdeckung, Pose, Silhouette oder ein Rendering-Artefakt.
2. **Den kleinstmöglichen sicheren Bearbeitungsbereich wählen.** Schließen Sie die beschädigte Anatomie und einen schmalen Übergangsbereich ein, bewahren Sie unveränderte Pixel und behalten Sie die Originaldatei.
3. **Nach Möglichkeit Struktur vorgeben.** Ein Handnetz, eine Pose, eine Tiefenschätzung oder eine sorgfältig geprüfte Referenz kann die Korrektur zuverlässiger einschränken als ein generischer positiver Prompt.
4. **Einen modellkompatiblen Bearbeitungs- oder Inpainting-Workflow verwenden.** Checkpoint, Text-Encoder, VAE, Konditionierungsformat und Node-Version müssen als Satz zueinander passen.
5. **Ergebnis manuell prüfen.** Kontrollieren Sie Fingeranzahl, Gelenke, Kontakt mit Objekten, Perspektive, Kontinuität von Haut bzw. Material, Schatten und den Rand des bearbeiteten Bereichs.
6. **Neu generieren statt wiederholt zu flicken,** wenn der Fehler global ist, die beabsichtigte Pose mehrdeutig ist oder die lokale Bearbeitung Identität oder Geometrie außerhalb des Zielbereichs verändert.

## Strukturbewusste Forschungsrichtungen {#structure-aware-research-directions}

HandRefiner und HandCraft sind nützliche Referenzen für das Prinzip einer robusten lokalen Reparatur: Eine Handstruktur wird abgeleitet, in eine Konditionierung wie Tiefe oder Masken überführt und per diffusionsbasiertem Inpainting in den korrigierten Bereich integriert. Die berichteten Ergebnisse gelten für die jeweils deklarierten Forschungsaufbauten; sie belegen nicht, dass ein Node für jedes aktuelle Diffusionsmodell direkt einsetzbar ist.

Die praktische Konsequenz ist einfach: Ein Geometriesignal kann eine Bearbeitung stärker einschränken, muss aber vor der Verwendung als Konditionierung auf die Übereinstimmung mit dem Originalbild geprüft werden.

## Aktuelle Grenzen bei ComfyUI und Modellen {#current-comfyui-and-model-boundary}

ComfyUI dokumentiert derzeit getrennte Workflows für die FLUX.2-[klein]-Basis- und destillierten Varianten für die unterstützten Modellvarianten. Folgen Sie für die jeweils gewählte 4B- oder 9B-Variante dem offiziellen Workflow und den offiziellen Modellspeicherorten. Nehmen Sie nicht an, dass ein Node, Control-Modell, LoRA, Text-Encoder oder VAE, der bzw. das für FLUX.1, SDXL oder eine andere Version gebaut wurde, mit einem FLUX.2-[klein]-Workflow kompatibel ist.

Community-Nodes und Anatomie-LoRAs von Drittanbietern können als Experimente nützlich sein, doch jede benötigt eine fixierte Quellrevision, eine eigene Lizenzprüfung und einen projektspezifischen visuellen Test. Diese Seite schreibt bewusst weder ungeprüfte Community-Gewichte noch universelle Zahlenwerte vor.

## Qualitätsprüfung {#quality-gate}

| Prüfpunkt | Was beobachtet werden muss |
|---|---|
| Anatomie | plausible Anzahl, Gelenke, Proportionen und Pose |
| Interaktion | Finger, Werkzeuge, Kleidung und andere Objekte berühren sich physikalisch korrekt |
| Erhaltung | Identität, Typografie, Logos, Schmuck und nicht betroffene Geometrie bleiben unverändert |
| Komposition | Beleuchtung, Schattenrichtung, Textur und Kantenübergang stimmen mit der Quelle überein |
| Reproduzierbarkeit | Quell-Digest, Maske/Konditionierung, Modellrevision, Einstellungen, Ausgabe-Digest und Entscheidung der prüfenden Person |

Ein Detektor-Score kann helfen, einen Stapel vorzusortieren, ist aber keine Bestehensbedingung. Jedes Asset mit Personenidentität, Produktangaben, medizinischer Relevanz oder Beweiswert benötigt vor der Veröffentlichung eine menschliche Prüfung.

## Bedingungen und Daten {#terms-and-data}

Code, Modelle, Adapter, Mesh- oder Pose-Schätzer, Eingabebilder und generierte Ausgaben können unterschiedlichen Lizenzen und Einwilligungspflichten unterliegen. Prüfen Sie die genauen Artefakte und die Rechte zur Bearbeitung des Bildes vor Wiederverwendung oder kommerziellem Einsatz.

## Referenzen {#references}

- [HandRefiner paper](https://arxiv.org/abs/2311.17957)
- [HandCraft paper](https://arxiv.org/abs/2411.04332)
- [HandFixer repository](https://github.com/Xiangyu-CAS/HandFixer)
- [ComfyUI FLUX.2 [klein] documentation](https://docs.comfy.org/tutorials/flux/flux-2-klein)
