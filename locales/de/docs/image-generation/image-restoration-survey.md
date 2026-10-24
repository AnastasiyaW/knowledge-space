---
title: "Bildwiederherstellung: Aufgaben- und Treue-Leitfaden"
description: "Bildwiederherstellung muss die Degradation und das Treueziel deklarieren; anschließend ist eine aufgabenkompatible deterministische oder Diffusionsmethode zu wählen und die gemessene Wiederherstellung getrennt von plausibel wirkenden, aber erfundenen Details zu validieren."
category: techniques
tags: [image-restoration, denoising, deblurring, super-resolution, jpeg-artifacts, diffusion, fidelity, evaluation]
aliases: ["Image Restoration Survey", "Image Enhancement", "Denoising Survey"]
level: 3
source_sha256: 65f1bf83a00073b2f9eb0d334b0bb5d2d8dee8ed5dd5d781ac967be050fa4c94
translation: machine
translated_at: '2026-10-24'
---
# Bildwiederherstellung: Aufgaben- und Treue-Leitfaden {#image-restoration-task-and-fidelity-guide}

Bildwiederherstellung erfordert eine deklarierte Degradation und ein deklariertes Treueziel.
„Sieht besser aus“ reicht für Produkt-, Dokumentar-, wissenschaftliches oder
forensisches Material nicht aus: Eine generative Methode kann plausible Details
erzeugen, die im beobachteten Bild nicht belegt sind.

## Den Wiederherstellungsvertrag festlegen {#start-with-the-restoration-contract}

Definieren Sie:

- Degradationstyp und bekannte Aufnahmehistorie, etwa Rauschen, Unschärfe,
  Kompression, fehlende Bereiche, Schwachlicht oder begrenzte Auflösung;
- das geforderte Ausgabeverhalten: messtreue Wiederherstellung, wahrnehmungsbezogene
  Bereinigung oder klar gekennzeichnete kreative Rekonstruktion;
- verfügbares Referenzziel oder eine quellenspezifische Validierungsmethode;
- geschützte Inhalte wie Text, Gesichter, Produktgeometrie, Farben und Markierungen;
  und
- die zulässigen Grenzen für Modell, Daten und Lizenz.

Kombinieren Sie Degradationsklassen nicht unter einer generischen Aktion „verbessern“,
sofern das Modell für genau diesen kombinierten Vertrag trainiert und validiert wurde.

## Methodenfamilien {#method-families}

### Aufgabenspezifische deterministische Modelle {#task-specific-deterministic-models}

Aufgabenspezifische CNN- und Transformer-Ansätze bleiben geeignet, wenn die
Degradation bekannt ist und pixeltreue Wiederherstellung wichtig ist. Beispiele sind
[SwinIR](https://github.com/JingyunLiang/SwinIR),
[NAFNet](https://github.com/megvii-research/NAFNet) und
[Restormer](https://arxiv.org/abs/2111.09881). Ihre veröffentlichten Ergebnisse gelten
für bestimmte Aufgaben, Datensätze und Checkpoints; wählen Sie eine kompatible Version
aus, statt eines davon als universelles Wiederherstellungsmodell zu behandeln.

### Bedingte Diffusions-Wiederherstellung {#conditional-diffusion-restoration}

[Palette](https://research.google/pubs/palette-image-to-image-diffusion-models/)
demonstriert bedingte Diffusion für Bild-zu-Bild-Aufgaben wie Colorization, Inpainting,
Uncropping und JPEG-Wiederherstellung. Diffusionsmethoden können eine breitere
Ausgabeverteilung modellieren, doch gerade diese Flexibilität macht nicht unterstützte
Details zu einem zentralen Akzeptanzrisiko.

[IR-SDE](https://arxiv.org/abs/2301.11699) ist eine weitere Forschungsformulierung, die
eine mean-reverting stochastische Differentialgleichung für die Wiederherstellung nutzt.
Sie legt weder einen Standardschedule noch eine Produktionskonfiguration für einen
anderen Checkpoint fest.

### Editing- und Foundation-Model-Workflows {#editing-and-foundation-model-workflows}

Allgemeine Bildbearbeitungssysteme können für eine begrenzte, masken- und
anweisungsgesteuerte Reparatur nützlich sein. Sie erfordern eine Bewertung der
Quellenerhaltung und müssen klar von metrikorientiertem Denoising oder
Super-Resolution getrennt bleiben. Siehe [[RealRestorer]] für einen versionsspezifischen
Workflow, nicht für eine Rangliste aller Restaurierungsverfahren.

## Evaluation, die Erfindungen erkennt {#evaluation-that-catches-invention}

Verwenden Sie nach Möglichkeit einen Validierungssatz mit bekannten Zielen und geben Sie
die Metrik in ihrem Aufgabenkontext an. Ergänzen Sie eine visuelle Prüfung auf:

- halluzinierten Text, Geometrie, Textur oder Details kleiner Objekte;
- Farb- und Tonwertverschiebungen, besonders nach Kompression oder Schwachlichtkorrektur;
- Nähte und Diskontinuitäten an Masken, Zuschnitten oder Kacheln;
- Erhaltung von Produkt-, Dokument- oder medizinischen/wissenschaftlichen Belegen; und
- Verhalten bei degradierten Eingaben außerhalb der Trainingsverteilung.

Trennen Sie ein Metrikergebnis von der Freigabeentscheidung. Eine hohe
Rekonstruktionsmetrik belegt nicht automatisch die sachliche Erhaltung, und eine
visuell ansprechende Diffusionsausgabe kann inakzeptabel sein, wenn Pixel als Beleg
dienen.

## Freigabeprotokoll {#release-record}

Speichern Sie den Eingabe-Digest, die Degradationsdiagnose, Modell/Checkpoint,
Parameter, das Referenzziel bzw. die Validierungsfixture, die Ausgabe, das
Akzeptanzergebnis sowie eine explizite Kennzeichnung jeder kreativen Rekonstruktion.
Wiederholen Sie die Validierung nach einer Änderung von Modell, Laufzeitumgebung oder
Eingabedomäne.

## Verwandte Seiten {#related-pages}

- [[RealRestorer]]
- [[color-checker-and-white-balance]]
- [[tiled-inference]]
- [[diffusion-inference-acceleration]]
