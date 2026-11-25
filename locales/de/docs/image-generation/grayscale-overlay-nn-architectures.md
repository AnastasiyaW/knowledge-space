---
title: "Graustufen-Overlay-Vorhersage: Vertrag für gepaarte Retusche"
description: "Die Vorhersage von Graustufen-Overlays ist eine gepaarte, pixelgenaue Retuschieraufgabe; den Blend-Vertrag und die No-op-Baseline beibehalten, jedes Quell-/Zielpaar und jede Maske binden und die komponierte Bildausgabe sowie die Karte prüfen, bevor eine automatisierte Anpassung freigegeben wird."
category: reference
tags: [image-restoration, retouching, regression, paired-data, evaluation, provenance]
level: 3
source_sha256: 11f9c34050b3dfc4d2fb32bc63decf012b8b11eb3c7dc0cb9a90fe9c12c8ed37
translation: machine
translated_at: '2026-10-24'
---
# Graustufen-Overlay-Vorhersage: Vertrag für gepaarte Retusche {#grayscale-overlay-prediction-paired-retouching-contract}

Die Vorhersage von Graustufen-Overlays schätzt eine einkanalige Anpassungskarte für eine
deklarierte Compositing-Operation. Es handelt sich um eine gepaarte, pixelgenaue
Retuschieraufgabe, nicht um einen generischen Image-Restoration-Benchmark. Die Karte
ist nur zusammen mit der genauen Blend-Implementierung, der Farbbehandlung, dem
Eingangsbild und dem genehmigten Bearbeitungsumfang aussagekräftig.

## Zuerst den Blend-Vertrag definieren {#define-the-blend-contract-first}

Bevor ein Netzwerk ausgewählt wird, muss das Ziel reproduzierbar gemacht werden:

- Eingangsfarbraum, Bittiefe, Orientierung und Alpha-Behandlung;
- Overlay-Bereich und sein neutraler No-op-Wert;
- Blend-Funktion und Implementierungsversion, einschließlich der Behandlung von linear/gamma;
- Deckkraft, Masken, geschützte Bereiche und Clipping-Verhalten; sowie
- Quellbild, Zielkarte, genehmigtes komponiertes Zielbild und Nachweis über Rechte/Einwilligung.

Eine Änderung eines dieser Punkte kann die erwartete Karte verändern, selbst wenn die
sichtbare Retusche ähnlich aussieht. Eine Zielkarte ohne ihren Compositing-Vertrag ist
keine wiederverwendbare Trainingsdaten.

## Modellkandidaten sind Hypothesen {#model-candidates-are-hypotheses}

[NAFNet](https://github.com/megvii-research/NAFNet) und
[Restormer](https://github.com/swz30/Restormer) sind veröffentlichte
Image-Restoration-Implementierungen. Sie können Kandidaten für eine gepaarte
Regressionsbaseline sein, doch ihre veröffentlichten Architekturen belegen nicht, dass
eine davon für eine einkanalige Retuschekarte die beste ist, dass eine bestimmte
Änderung am Head kompatibel ist oder dass ein fester Loss- beziehungsweise Tiling-Ansatz
für jedes Overlay sicher ist.

Beginnen Sie mit dem kleinsten versionierten Modell, das das erforderliche Kanallayout
erzeugen kann. Binden Sie Trainings- und Inferenzcode an:

1. eine Checkpoint-/Repository-Revision;
2. den Ausgabebereich und die Richtlinie zur No-op-Initialisierung;
3. das Verhalten bei voller Auflösung beziehungsweise Tiling, wie es bei der Freigabe verwendet wird; und
4. eine Baseline, die die neutrale Karte ausgibt.

Nicht unterstützte Head-Änderungen, benutzerdefinierte Hooks und das Verhalten von
Batch-Normalisierung sind als Experimente mit eigenem Nachweis zu behandeln, nicht als
implizite Architekturmerkmale.

## Paare bilden, die dasselbe bedeuten {#build-pairs-that-mean-the-same-thing}

Jedes Beispiel muss dieselbe Szenengeometrie mit der Zielanpassung paaren:

- Zwischen Eingabe und Ziel darf kein Zuschnitt, keine Perspektivkorrektur, keine
  Gesichtsausrichtung und keine Retuschieroperation verschoben werden;
- Masken sollten bearbeitbare Pixel von geschützten beziehungsweise unbekannten Pixeln
  unterscheiden;
- Quellassets müssen vor der Aufteilung in Train/Validation/Test nach Fotograf, Motiv,
  Shooting und abgeleiteter Kette getrennt werden; und
- Original, Karte, komponiertes Zielbild, Begründung der Bearbeitung und Entscheidung des
  Prüfers gemeinsam aufbewahren.

Augmentierungen sind nur gültig, wenn sie die Beziehung Bild zu Karte und den
Blend-Vertrag erhalten. Eine Transformation, die Beleuchtung, Komposition oder Geometrie
verändert, kann ein scheinbar ausgerichtetes Paar mit einem ungültigen Ziel erzeugen.

## Karte und sichtbares Ergebnis bewerten {#evaluate-the-map-and-the-visible-result}

Den paarweisen Kartenfehler erst verwenden, wenn Skala und gültiger Bereich definiert
sind. Er kann nicht zeigen, ob die Anpassung nach dem Compositing korrekt aussieht.
Beide Ebenen prüfen:

| Ebene | Prüfung |
|---|---|
| Vorhergesagte Karte | neutrale Bereiche bleiben neutral, Gradienten sind stabil, Masken werden eingehalten und Kanten laufen nicht aus |
| Komponiertes Bild | die beabsichtigte Korrektur ist sichtbar, geschützte Merkmale bleiben unverändert und es entstehen keine Banding-, Naht-, Clipping- oder Farbverschiebungen |
| Zurückgehaltene Quellen | die Leistung hält bei neuen Motiven, Beleuchtungen, Materialien und Zuschnitten stand |
| Laufzeit | Auflösung, Speicherbedarf, Tiling-Verhalten und Fallback-/Fehlerpfad entsprechen der Produktionsumgebung |

Bei Gesichtern oder Produkten erfordert ein visuell glattes Ergebnis dennoch eine Prüfung
identitätsrelevanter Merkmale, Beschriftungen, Textur und sachlicher Details. Das Netzwerk
schlägt eine Anpassung vor; es autorisiert keine fertige Retusche.

## Freigabe-Gate {#release-gate}

Eine automatisierte Overlay-Anpassung wird nur freigegeben, wenn ein Prüfer Eingabe,
Modell, Karte, Blend-Vertrag, komponierte Ausgabe und Genehmigung reproduzieren kann.
Gibt das Modell eine nicht neutrale Änderung außerhalb der erlaubten Maske aus oder kann
die Auswertung eine plausible Karte nicht von einer genehmigten Anpassung unterscheiden,
wird sie zur manuellen Korrektur zurückgehalten.

## Quellen und verwandte Seiten {#sources-and-related-pages}

- [NAFNet official repository](https://github.com/megvii-research/NAFNet)
- [Restormer official repository](https://github.com/swz30/Restormer)
- [[paired-training-for-restoration]]
- [[image-restoration-survey]]
- [[low-vram-inference-strategies]]
