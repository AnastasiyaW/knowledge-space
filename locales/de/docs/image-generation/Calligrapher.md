---
title: "Calligrapher: referenzgeführte Anpassung von Textbildern"
description: "Calligrapher passt Textbilder anhand von Stilreferenzen mithilfe von FLUX.1-Fill-dev, SigLIP, Masken und Projektgewichten an; Typografiegenauigkeit und Lizenzierung sind als getrennte Abnahmeprüfungen zu behandeln."
category: models
tags: [text-editing, typography, style-reference, flux-fill, siglip, self-distillation, multilingual]
aliases: ["Calligrapher"]
level: 2
source_sha256: 4342e99b7c6144336d63a3e9d5fb3cf467bf06584b2058b3848f7264997501e7
translation: machine
translated_at: '2026-10-24'
---
# Calligrapher: referenzgeführte Anpassung von Textbildern {#calligrapher-reference-guided-text-image-customization}

**Stand der Prüfung: 2026-09-04.** Calligrapher ist ein diffusionsbasiertes Projekt zum Erzeugen oder Bearbeiten von Textbildern, bei dem ein visueller Stil aus einer Referenz übertragen wird. Die dokumentierten Modi umfassen Selbstreferenz, Kreuzreferenz und Anpassung ohne Textreferenz. Es eignet sich für Typografie-Experimente und Prototypen der Art-Direction, generierte Schreibweise, Komposition und Rechte müssen jedoch unabhängig geprüft werden.

## Was der Workflow verwendet {#what-the-workflow-uses}

Der veröffentlichte Aufbau kombiniert:

- eine zulässige lokale Kopie von `FLUX.1-Fill-dev`;
- den SigLIP-Bildencoder;
- Calligrapher-Projektgewichte und Testdaten;
- ein Eingabebild und eine bearbeitbare Maske;
- eine Textanweisung und, sofern die Aufgabe dies erfordert, eine Stilreferenz.

Das Repository bietet eine einfache Gradio-Demo mit manuell gezeichneter Maske sowie eine Version, die eine benutzerdefinierte Inpainting-Maske akzeptiert. Platzierung der Maske und Seitenverhältnis beeinflussen das Ergebnis erheblich: Das Modell füllt den angeforderten Bereich aus und passt ihn an das umgebende Bild an, anstatt als deterministischer Textrenderer zu arbeiten.

## Den Referenzmodus bewusst wählen {#choose-the-reference-mode-deliberately}

| Modus | Vorgesehene Verwendung | Prüfschwerpunkt |
|---|---|---|
| Selbstreferenz | Text ersetzen und den Stil desselben Bildes beibehalten | Quelltextbereich und Erhalt des lokalen Hintergrunds |
| Kreuzreferenz | Typografie aus einer separaten Referenz übertragen | Stilübertragung ohne ungewollt kopierte Inhalte |
| Referenz ohne Text | eine typografische Gestaltung aus einer visuellen Vorlage ableiten | ob der Stil erkennbar ist und der Text lesbar bleibt |
| Mehrsprachiger Pfad | die dokumentierte, TextFLUX-gestützte Demo verwenden | sprachspezifische Glyphenqualität und Schreibweise |

Die mehrsprachige Demo ist optional und verwendet einen anderen Basismodell-Pfad. Das Projekt warnt, dass ihre Qualität schwanken kann; ein positives englischsprachiges Ergebnis sollte nicht als Nachweis für eine andere Schrift oder Sprache gelten.

## Auflösung, Text und menschliche Prüfung {#resolution-text-and-human-review}

Die Autoren trainieren mit 512 Pixeln und empfehlen 512 oder 768 Pixel als praktischen Kompromiss. Sehr hohe Auflösungen können Rechtschreibfehler verursachen. Dies ist als Ausgangspunkt für eine Testvorlage zu verstehen, nicht als allgemeine Anforderung an die Ausgabe.

Für ein veröffentlichbares Asset sind folgende Punkte getrennt zu bewerten:

1. exakter Text und Zeichensetzung;
2. Reihenfolge der Glyphen, Sprach- und Schriftunterstützung sowie Lesbarkeit in der Liefergröße;
3. Treue zum angeforderten Stil, ohne geschützte Inhalte zu kopieren;
4. Maskenrand, Hintergrund, Beleuchtung und visuelle Artefakte;
5. Quelle, Prompt, Modellversion, Maske und Ausgabe, die für eine nachvollziehbare Prüfung benötigt werden.

Wenn exakte, deterministische Schrift gefordert ist, sollte ein übliches Typografie- oder Layoutwerkzeug verwendet werden. Diffusionsausgaben sind am besten als Bildkandidat zu betrachten, der möglicherweise nachbearbeitet oder komponiert werden muss.

## Zugang und Rechtsgrenzen {#access-and-rights-boundary}

Das FLUX-Basismodell erfordert einen eigenen Zugang und eigene Bedingungen, während das Calligrapher-Projekt und etwaige Zusatzgewichte eigene Verbreitungsbedingungen haben. Vor kommerziellem Einsatz, Weitergabe oder der Verwendung einer visuellen Referenz eines Dritten sind alle aktuellen Model Cards und Lizenzen zu prüfen. Die Verfügbarkeit einer Demo erteilt keine Erlaubnis, alle Referenzen oder Ausgaben für jeden Zweck zu verwenden.

## Referenzen {#references}

- [Calligrapher official repository](https://github.com/EzioBy/Calligrapher)
- [Calligrapher paper](https://arxiv.org/abs/2506.24123)
- [Calligrapher weights and test assets](https://huggingface.co/Calligrapher2025/Calligrapher)
