---
title: "Intrinsische Zerlegung: Annahmen- und Prüfvertrag"
description: "Die intrinsische Zerlegung ist eine ambiguitätsbeschränkte Schätzung von Reflektanz und Beleuchtung, keine Ground Truth. Vor der Verwendung ihrer Albedo- oder Shading-Ausgaben für Bearbeitung oder Relighting müssen die Annahmen zur Bildentstehung, Modell und Version, Farbdomäne, Residuenpolicy, Quellennachweise und die aufgabenspezifische Prüfung verbindlich festgelegt werden."
category: techniques
tags: [intrinsic-decomposition, albedo, illumination, reflectance, shading, relighting, evidence]
aliases: ["Albedo and Illumination Separation", "Intrinsic Image Decomposition"]
level: 3
source_sha256: a00166d35927c5b5a9cc80ad23ba033b91be26894bfa867c4c5eb8a7a62bc255
translation: machine
translated_at: '2026-10-24'
---
# Intrinsische Zerlegung: Annahmen- und Prüfvertrag {#intrinsic-decomposition-assumption-and-review-contract}

Die intrinsische Zerlegung schätzt Komponenten wie die Reflektanz (häufig als Albedo bezeichnet) und das Shading aus einem Bild. Sie ist keine Messung des Materials oder der Beleuchtung einer fotografierten Szene. In einem vereinfachten diffusen Modell lässt sich ein beobachtetes Bild als `I ≈ R ⊙ S + E` ausdrücken, wobei `R` die Reflektanz, `S` das beleuchtungsabhängige Shading und `E` Effekte beschreibt, die das Modell nicht abbildet. Reale Bilder enthalten Spiegelungen, Transparenz, Streuung unter der Oberfläche, Verarbeitung durch den Sensor, Clipping und gemischtes Licht. Ein einzelnes RGB-Bild bestimmt diese Komponenten in der Regel nicht eindeutig.

## Den Zerlegungsvertrag deklarieren {#declare-the-decomposition-contract}

Für jede Ausgabe sind festzuhalten:

- Digest des Quell-Assets, Zuschnitt/Orientierung, Farbkodierung, Alpha-Policy und ob das Modell lineare, szenenbezogene oder anzeigebezogene Werte sieht;
- genaue Modellversion, Gewichte, Laufzeitumgebung, Prompt- bzw. Referenzeingaben sowie die vom Verfahren dokumentierten Annahmen zur Bildentstehung;
- benannte Ausgaben, deren Einheiten/Normierung, die Behandlung von Residuen oder Konfidenzen und welche Pixel keine verlässliche Schätzung haben;
- vorgesehene Operation, etwa eine reine Beleuchtungsvorschau oder eine eingeschränkte Umfärbung, sowie geschützte Inhalte; und
- Vergleichsquelle, numerische bzw. rekonstruktive Prüfung, soweit sinnvoll, und visuelle Prüfung in der Auslieferungsauflösung.

Eine albedoähnliche Ausgabe eines Verfahrens darf nicht ohne eine implementierungsspezifische Kompatibilitätsprüfung als Albedo, Normale, Material- oder Relighting-Eingabe eines anderen Verfahrens verwendet werden.

## Schätzungen als modellgebunden behandeln {#treat-estimates-as-model-scoped}

Die Aufgabe umfasst unterschiedliche Beobachtungen und Annahmen. [Intrinsic Scene Decomposition From RGB-D Images](https://openaccess.thecvf.com/content_iccv_2015/html/Hachama_Intrinsic_Scene_Decomposition_ICCV_2015_paper.html) verwendet beispielsweise Tiefendaten und ein angegebenes Beleuchtungsmodell, während [Intrinsic Image Transformation via Scale Space Decomposition](https://openaccess.thecvf.com/content_cvpr_2018/html/Cheng_Intrinsic_Image_Transformation_CVPR_2018_paper.html) die Ausgaben für Einzelbilder als gelernte Bild-zu-Bild-Schätzungen darstellt. Diese Arbeiten belegen nicht, dass eine benannte Ausgabe für beliebige RGB-Fotografien, Haut, Produkte, transparente Objekte oder eine spätere Modellversion physikalisch korrekt ist.

Ein Verfahren darf erst ausgewählt werden, nachdem die genaue Version an repräsentativen Bildern und für die nachgelagerte Operation getestet wurde. Fehlerfälle sind zu dokumentieren, etwa harte Schatten, Spiegelhighlights, geclippte Lichter, gesättigte Farben, gemischte Beleuchtung, feine Strukturen und Artefakte der Kamerabearbeitung.

## Einen eingeschränkten Bearbeitungsworkflow verwenden {#use-a-constrained-edit-workflow}

1. Prüfen, dass Quelle, Rechte, Zuschnitt, Farbdomäne und geschützte Bereiche im Auftragsrahmen liegen.
2. Die angegebene Schätzung erzeugen und die Zuordnung von Quelle zu Ausgabe festhalten.
3. Residuen und mehrdeutige Bereiche prüfen, bevor ein Wert als Reflektanz oder Shading behandelt wird.
4. Nur die freigegebene Änderung auf explizite Masken anwenden. Eine niederfrequente oder albedoähnliche Schicht ist keine Erlaubnis, jeden Material- oder Gesichtspixel zu verändern.
5. Die Rekomposition ausschließlich mit der vom Modell deklarierten Routine durchführen. Ist ein generiertes Bild, Clipping, Blending oder ein nichtlinearer Schritt beteiligt, ist das Ergebnis als abgeleitet und nicht als exakte Rekonstruktion zu kennzeichnen.
6. Quelle und Ergebnis in Auslieferungsauflösung auf Farbverschiebungen, Halos, Schatten- oder Materialvertauschungen, Detailverlust, Geometrieänderungen und Verletzungen geschützter Inhalte prüfen.

Albedo-basierte Farbübertragung kann ein nützliches Experiment sein, wenn die Beleuchtung eine Farbbearbeitung verfälscht. Sie erfordert trotzdem einen quellenbezogenen Vergleich und beweist nicht, dass die Zielfarbe physikalisch korrekt ist. Ein Residuum darf nur erhalten bleiben, wenn das gewählte Verfahren es definiert und der Ausgabevertrag festlegt, wie es kombiniert wird.

## Fehler- und Freigabegrenze {#failure-and-release-boundary}

Eine unsichere Schätzung darf nicht stillschweigend durch ein anderes Modell ersetzt, generierte Textur darf nicht hinzugefügt und ein relightetes Ergebnis darf nicht als wiedergewonnene Quelldaten dargestellt werden. Ein sichtbarer Prüf- oder Fehlerstatus ist zurückzugeben, wenn Annahmen unbekannt sind, die Laufzeitumgebung die deklarierte Ausgabe nicht reproduzieren kann, das Residuum unerklärt bleibt oder die Prüfung eine Veränderung geschützter Inhalte feststellt.

## Verwandte Seiten {#related-pages}

- [[color-space-and-gamma-reference]]
- [[color-checker-and-white-balance]]
- [[frequency-decomposition-editing]]
- [[tiled-inference]]
