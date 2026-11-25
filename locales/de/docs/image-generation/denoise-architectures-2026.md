---
title: "Denoising-Architekturen: Degradation und Nachweisvertrag"
description: "Eine Denoising-Architektur wird anhand einer deklarierten Degradation und eines Fidelity-Ziels ausgewählt, nicht anhand einer Leaderboard-Platzierung oder eines Familiennamens; Aufnahme-/Rauschannahmen, Modell und Checkpoint, Vorverarbeitungs-, Kachelungs- und Farbpfad, autorisierte Trainings- und Evaluationssplits, Task- und Erhaltungsmetriken sowie visuelle Prüfung binden, bevor generierte oder restaurierte Details akzeptiert werden."
category: reference
tags: [denoising, restoration, degradation, evaluation, fidelity, provenance]
aliases: ["Denoise Architectures 2026", "Image Denoising Architectures"]
level: 2
source_sha256: 5aa1d877cc8bdd49fb2705094c356294238c13462f227d5bf11dcaa3599751c7
translation: machine
translated_at: '2026-10-24'
---
# Denoising-Architekturen: Degradation und Nachweisvertrag {#denoising-architectures-degradation-and-evidence-contract}

Architekturnamen identifizieren weder die zu entfernende Degradation noch die
zu erhaltenden Details. Ein Denoiser kann Sensorrauschen, Kompressionsartefakte,
Unschärfe, Regen, eine synthetische Störung oder eine Mischung davon schätzen;
jede Aufgabe benötigt einen eigenen Vertrag für Eingabe, Fidelity und Evaluation.

Der [NTIRE 2025 Image Denoising Challenge Report](https://openaccess.thecvf.com/content/CVPR2025W/NTIRE/html/Sun_The_Tenth_NTIRE_2025_Image_Denoising_Challenge_Report_CVPRW_2025_paper.html)
berichtet Methoden und Ergebnisse für seine spezifizierte AWGN-Challenge mit
Sigma 50. Seine Befunde sind als Evidenz für diesen Benchmark nützlich. Sie
ordnen Architekturen jedoch nicht universell ein, weder über Kamera-Pipelines,
Rauschmischungen, künstlerische Nachbearbeitung und forensische Wiederherstellung
noch über Laufzeitgrenzen oder Anforderungen an den Schutz feiner Details hinweg.

## Restaurierungsziel deklarieren {#declare-the-restoration-target}

Für jede Modellevaluation oder jeden Deployment-Lauf sind festzuhalten:

- Herkunft des Quellasset bzw. der Aufnahme, Orientierung, Farbprofil,
  Dynamikumfang, Kompressionshistorie, Alpha-/Masken-Policy und das
  deklarierte Degradationsmodell;
- Modell/Checkpoint, Code/Laufzeit/Version, kompatibler Eingabebereich,
  Farbdomäne, Vorverarbeitung, Padding, Crop-/Kachelungs- und Blending-Policy
  sowie Output-Transformation;
- autorisierte gepaarte oder normal-referenzierte Daten,
  Annotations-/Ground-Truth-Policy, gruppendisjunkte Splits und ein etwaiger
  synthetischer Degradationsgenerator;
- Task-Metriken und Erhaltungsmetriken, evaluiert auf einem quelldisjunkten
  Datensatz; und
- visuelle Prüfung von Rauschentfernung, Textur, Text, Kanten, Produktgeometrie,
  Gesichtern, Schatten, Verläufen, Farbe und geschützten Bereichen in
  Auslieferungsgröße.

Ein Wechsel von Kamera, Codec, Rauschverteilung, Crop, Arbeitsfarbraum,
Kachelplan oder Checkpoint erzeugt eine neue Konfiguration. Ein Ergebnis aus
einer anderen Degradation oder einem anderen Quellsplit ist keine Evidenz dafür.

## Auswahl nach gemessenem Fehlerverhalten {#choose-by-measured-failure-behavior}

Convolutional-, Transformer-, State-Space-, Fourier- und diffusionsbasierte
Ansätze treffen unterschiedliche Annahmen über Lokalität, Konditionierung und
Generierung. Die dokumentierte Version ist nur dort zu verwenden, wo ihre
Annahmen zur deklarierten Aufgabe passen; danach ist sie gegen eine benannte
Baseline unter identischen Eingaben und identischem Export-Pfad zu vergleichen.

Latenz und Peak-Speicherbedarf sind getrennt von der Rekonstruktionsqualität zu
messen. Erzeugt eine Methode plausible Textur oder Details, die vom Eingangssignal
nicht gestützt werden, ist die Ausgabe als abgeleitet/generiert zu kennzeichnen
und nicht als wiederhergestelltes Quellsignal. Bei maskierter Korrektur sind die
Maske zu dokumentieren und unveränderte Bereiche separat zu verifizieren; ein
scheinbar wirkungsloser Bereich außerhalb der Maske gilt ohne Vergleich nicht
als belegt.

## Fehlergrenze {#failure-boundary}

Fehlen Degradationsannahmen, Modellkompatibilität, Ground-Truth-Autorität,
quelldisjunkte Evaluation oder die Prüfung geschützter Details, ist ein sichtbarer
Review-/Fehlerzustand zurückzugeben. Ein Modell darf nicht allein deshalb
gewählt werden, weil es ein anderes Leaderboard anführt, nicht stillschweigend
auf einen generativen Prior umgeschaltet werden, und plausible Details dürfen
nicht als faktische Restaurierung dargestellt werden.

## Verwandte Seiten {#related-pages}

- [[image-restoration-survey]]
- [[paired-training-for-restoration]]
- [[tiled-inference]]
- [[frequency-decomposition-editing]]
