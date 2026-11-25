---
title: "FP8 E4M3: Gemessener Quantisierungsvertrag"
description: "FP8-E4M3-Quantisierung ist ein versions- und backendspezifischer numerischer Vertrag; binden Sie das Tensorformat, das Skalierungsverfahren, unterstützte Operationen und Hardware, Kalibrierungs- oder Amax-Nachweise, den Serialisierungs- bzw. Laufzeitpfad sowie Qualitäts-, Latenz- und Speicher-Messungen, und ersetzen Sie niemals stillschweigend durch Clipping oder ein anderes Format."
category: optimization
tags: [fp8, e4m3, quantization, transformer-engine, inference, measurement]
aliases: ["FP8 Quantization Optimization for E4M3", "E4M3 Quantization"]
level: 3
source_sha256: b92587c3b44bf0a3a4b6319c99d06eaafa36e6052ff08ffe583d478183a5f0f9
translation: machine
translated_at: '2026-10-24'
---
# FP8 E4M3: Gemessener Quantisierungsvertrag {#fp8-e4m3-measured-quantization-contract}

FP8 ist kein austauschbarer Optimierungsschalter. Die [Transformer-Engine-Dokumentation zu current scaling](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/features/low_precision_training/fp8_current_scaling/fp8_current_scaling.html) beschreibt E4M3 als FP8-Format mit einem Vorzeichenbit, vier Exponentenbits, drei Mantissenbits, endlichen Werten bis plus oder minus 448 sowie NaN. Es wird E5M2 gegenübergestellt, dessen Abwägung zwischen Wertebereich und Genauigkeit sich unterscheidet. Diese Formate, ihre Kernels und ihre Skalierungsverfahren dürfen nicht stillschweigend ersetzt werden.

## Ein dokumentiertes numerisches Verfahren auswählen {#select-a-documented-numerical-path}

Die zitierte Transformer-Engine-Version beschreibt current scaling als einen FP32-Skalierungsfaktor pro Tensor: Absolutmaximum berechnen, auf den gewählten FP8-Bereich skalieren und casten. Sie weist darauf hin, dass dafür zwei Lesezugriffe auf den Tensor nötig sind. Das erklärt einen Zielkonflikt für genau dieses benannte Verfahren; es rechtfertigt jedoch keine universelle statische Skalierung, keinen harten Clipping-Pfad, keine Schichtanzahl, keine Latenzaussage und kein Hardwareversprechen für ein anderes Framework oder Modell.

Dokumentieren Sie die exakte Framework- bzw. Engine-Version, GPU und Treiber, Modell bzw. Checkpoint, Präzisionseinstellungen, unterstützte Operationen, Tensorlayout sowie das Verhalten bei Fallback und Fehlern. Prüfen Sie die Matrix aus unterstützten Geräten und Operationen für die verwendete Version, anstatt ein dokumentiertes Ergebnis auf einen anderen Beschleuniger oder eine andere Laufzeitumgebung zu übertragen.

## Kalibrierungs- und Messnachweise aufbewahren {#keep-calibration-and-measurement-evidence}

Für jeden vorgesehenen Ausführungspfad bewahren Sie Folgendes auf:

- Tensorformat und Skalierungsverfahren je Operation, einschließlich der Angabe, ob Amax, delayed, Block oder eine andere dokumentierte Strategie verwendet wird;
- Kalibrierungsdaten oder Live-Amax-Nachweise, die Richtlinie für Skalierungsaktualisierungen sowie Beobachtungen zu Ausreißern und Sättigung;
- Laden, Serialisierung, Kompilierung und Bereitstellungspfad des Checkpoints, einschließlich der Stellen, an denen Konvertierungen stattfinden;
- vergleichbare Baseline- und FP8-Läufe mit Warm- und Steady-State-Latenz, Spitzenspeicherbedarf, Durchsatz, Reproduzierbarkeit, numerischen Fehlern und Ergebnissen der Aufgabenqualität; sowie
- für die tatsächliche Aufgabe festgelegte Akzeptanzschwellen sowie die Mess­umgebung und einen quellenseitig disjunkten Evaluationsdatensatz.

Die Aktivierungsverteilung, der Kalibrierungslauf oder das Compiler-Verhalten eines Modells belegen nicht die Eignung eines anderen Modells, einer anderen Prompt-Verteilung, Auflösung, Batch-Form oder Trainingsphase.

## Grenzen bei Fehlern {#failure-boundary}

Wenn eine erforderliche Operation oder ein erforderliches Gerät den deklarierten Pfad nicht unterstützt, Amax- oder Qualitätsnachweise fehlen, eine Serialisierungsgrenze das Format verändert oder Messungen die Aufgabenschwelle verletzen, melden Sie einen sichtbaren Fehler- bzw. Prüfstatus. Ersetzen Sie E4M3 nicht durch E5M2, deaktivieren Sie die Skalierung nicht, klemmen Sie keine Werte und wechseln Sie nicht auf eine andere Präzision, während Sie das Ergebnis als denselben FP8-Lauf beschreiben.

## Verwandte Seiten {#related-pages}

- [[low-vram-inference-strategies]]
- [[diffusion-inference-acceleration]]
- [[diffusion-lora-training]]
- [[tiled-inference]]
