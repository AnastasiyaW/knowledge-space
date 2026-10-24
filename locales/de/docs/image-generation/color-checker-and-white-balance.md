---
title: "Farbkarte und Weißabgleichskorrektur"
description: "Farbkarten- und Weißabgleichskorrektur erfordert eine gemessene physische Testkarte oder einen separat validierten Schätzer; Detektorausgaben und eine generierte Farbkarte sind keine kolorimetrische Referenzwahrheit."
category: techniques
tags: [color-checker, white-balance, color-constancy, calibration, illumination, product-photography]
aliases: ["Color Constancy", "White Balance"]
level: 3
source_sha256: 5a3d13469de01f594e9b21b8c9868e1e970b539fd4ca35ecb8cfba0c8726357e
translation: machine
translated_at: '2026-10-24'
---
# Farbkarte und Weißabgleichskorrektur {#color-checker-and-white-balance-correction}

Weißabgleich und Farbkorrektur lösen verwandte, aber unterschiedliche Probleme. Der Weißabgleich schätzt die Lichtquelle oder neutralisiert sie; eine Farbtransformation bildet eine bestimmte Aufnahme- bzw. Wiedergabeantwort auf eine definierte Referenz ab. Keines von beiden wird allein dadurch verlässlich, dass ein kartenähnliches Objekt in einem Bild erkannt wurde.

## Festlegen, was als Referenz gilt {#decide-what-counts-as-a-reference}

Verwenden Sie einen dieser Nachweiswege und dokumentieren Sie, welcher verwendet wurde:

1. **Gemessene physische Testkarte.** Nehmen Sie eine bekannte Testkarte unter derselben Beleuchtung und im selben optischen Pfad wie das Motiv auf. Lesen Sie ihre Felder aus einer nicht überbelichteten, korrekt belichteten Aufnahme aus und vergleichen Sie sie mit den Referenzwerten der Karte.
2. **Separat validierter Schätzer.** Ein gelernter Weißabgleichs- oder Beleuchtungsschätzer kann nützlich sein, wenn keine physische Testkarte vorhanden ist. Er muss jedoch an der Zielkamera, dem Renderpfad, den Materialien und der Beleuchtung validiert werden. Seine Ausgabe ist eine Schätzung, keine Messung.

Bei Schmuck- und Produktarbeiten bewahren Sie die Quellaufnahme, die Identität der Testkarte, Beleuchtung und Aufbau, die Rendertransformation sowie die Validierungsstichproben auf. Ein gefälliges Ergebnis ist kein ausreichender Nachweis dafür, dass Metall- oder Edelsteinfarben korrekt sind.

## Arbeitsablauf mit physischer Testkarte {#physical-chart-workflow}

1. Fotografieren Sie die Testkarte unter der Aufnahmebeleuchtung, ohne Lichter zu clippen und ohne Belichtung oder Beleuchtung zwischen Referenz- und Produktaufnahmen zu ändern.
2. Lokalisieren Sie die Testkarte, ordnen Sie ihre Felder und verwerfen Sie Aufnahmen mit Glanzlichtern, Unschärfe, Verdeckung, starker Perspektive oder unsicherer Feldzuordnung.
3. Leiten Sie die Transformation im deklarierten Arbeitsfarbraum ab und wenden Sie sie nur auf Aufnahmen an, die dem jeweiligen Kalibriervertrag unterliegen.
4. Validieren Sie an zurückgehaltenen neutralen, Haut-, Produkt- oder Materialfeldern, die für das tatsächliche Liefergut gewählt wurden. Prüfen Sie sowohl den numerischen Fehler als auch das gerenderte Bild.
5. Versionieren Sie die Transformation zusammen mit dem Kameraprofil, dem Objektiv- und Beleuchtungsaufbau, dem Raw-Konverter und dem Validierungsprotokoll. Kalibrieren Sie nach einer wesentlichen Änderung des Aufbaus oder der Rendering-Pipeline neu.

Die Transformation sollte Weißabgleich, Kameraprofil, Tonwertkorrektur und kreative Gradation nicht stillschweigend miteinander vermischen. Halten Sie diese Operationen explizit getrennt, damit ein späteres Review das Ergebnis reproduzieren kann.

## Erkennung ist nur Lokalisierung {#detection-is-only-localization}

[Colour Checker Detection](https://github.com/colour-science/colour-checker-detection) implementiert Segmentierungs-, template-basierte und maschinelle Lernverfahren. Das veröffentlichte YOLOv8-Modell ist für ColorChecker Classic 24 trainiert und ist kein allgemeiner Detektor für Nano- oder SG-Karten. Das Repository dokumentiert außerdem Lizenzunterschiede für den Inferenzpfad, der die Ultralytics-API verwendet.

Daher sollten Sie die Detektorversion, den Kartentyp und die Inferenzabhängigkeit festschreiben und anschließend Feldreihenfolge und Zuschnittqualität am realen Aufnahmesatz prüfen. Die Erkennung kann eine Kandidatenkarte finden; sie validiert jedoch weder den Zustand der Karte, die Beleuchtungsäquivalenz, die Belichtung noch die Kolorimetrie.

## Gelernte und generative Schätzer {#learned-and-generative-estimators}

[Deep White Balance](https://github.com/mahmoudnafifi/Deep_White_Balance) ist eine Forschungsimplementierung für gelernte Weißabgleichskorrektur gerenderter Bilder. Sie lässt sich als Schätzer evaluieren, doch Trainingsdaten und Renderannahmen müssen mit der lokalen Aufnahmepipeline verglichen werden.

Generative Color Constancy (GCC) ist eine andere Forschungsrichtung: Ihr [Artikel](https://arxiv.org/abs/2502.17435) verwendet deterministisches Inpainting, um eine virtuelle Farbkarte einzusetzen, die beine geschätzte Szenenbeleuchtung widerspiegelt. Das ist nützlich zur Untersuchung der Beleuchtungsschätzung, nicht aber, um generierte Feldwerte in ein gemessenes Ziel zu verwandeln. Eine generierte Farbkarte muss als Modellschätzung gekennzeichnet bleiben und darf in einem kolorimetrischen Abnahmetest niemals eine physische Referenz ersetzen.

## Minimales Abnahmeprotokoll {#minimal-acceptance-record}

Bewahren Sie für jede kalibrierte Charge Folgendes auf:

- Kennungen der Aufnahme und der Testkarte, Quell-Digest und deklarierten Farbraum;
- Revision des Detektors bzw. Schätzers und alle Transformationsparameter;
- verworfene Aufnahmen mit Begründung;
- zurückgehaltene Validierungsbilder und das Bestanden-/Nicht-bestanden-Kriterium; und
- den Prüfer oder den automatisierten Job, der die Freigabe genehmigt hat.

So bleibt die Farbkorrektur nachvollziehbar, wenn sich später Kamera, Beleuchtungsaufbau, Modell oder Raw-Verarbeitung ändern.

## Verwandte Seiten {#related-pages}

- [[color-correction-by-numbers]]
- [[color-space-and-gamma-reference]]
- [[diffusion-inference-acceleration]]
