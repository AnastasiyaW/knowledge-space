---
title: "Perspektivkalibrierung für Object Compositing"
description: "Ein lokales Entscheidungsframework zur Schätzung der Kamerageometrie, zur Validierung mit Szenenevidenz und zur Ableitung einer stabilen Platzierungstransformation vor dem Compositing eines Objekts."
level: 3
source_sha256: 75f29b17bd86bc31ac8fcd60ade7e681d996d708768f391c4e34d4856bedd7da
translation: machine
translated_at: '2026-10-24'
---
# Perspektivkalibrierung für Object Compositing {#perspective-calibration-for-object-compositing}

Die Perspektivkalibrierung ist die Geometriephase **vor** dem Object Compositing. Ihr Ergebnis ist eine begründbare Hypothese zu Kamera und Stützebene: Intrinsics `K`, Kameraorientierung, Horizont und eine Ebenenabbildung. Sie lässt ein Cut-out nicht von selbst zur Szene passen; sie verhindert aber, dass ein nachgelagerter Compositor einen unmöglichen Maßstab, eine unmögliche Neigung oder einen unmöglichen Kontaktpunkt zu kaschieren versucht.

Verwenden Sie die Kalibrierung, wenn das eingefügte Objekt auf einer ebenen Fläche aufliegen, konvergierende Kanten teilen oder nach einer kleinen Neupositionierung plausibel bleiben muss. Für eine flache Grafik, die parallel zur Bildebene platziert wird, verwenden Sie stattdessen eine 2D-Transformation. Für ein Objekt, das aus einem materiell anderen Winkel gezeigt werden muss, erfassen bzw. rendern Sie eine passende Ansicht; eine Kalibrierung aus einem einzelnen Bild rekonstruiert keine verdeckte Geometrie.

## Festlegen, was geschätzt werden muss {#decide-what-must-be-estimated}

Gehen Sie von der Bearbeitungsaufgabe aus, nicht vom Modell:

- **Platzierung nur auf einer bekannten Ebene:** Schätzen Sie `K`, Orientierung und eine Homographie für die Stützebene. Dies ist der typische Fall Produkt auf dem Boden, Schild an der Wand oder Möbel auf dem Untergrund.
- **Sichtbare Architektur oder Fahrbahnmarkierungen:** Extrahieren Sie Linien und verlangen Sie, dass ihre Fluchtrichtungen mit der Kameraschätzung übereinstimmen.
- **Schwacher, gekrümmter oder rein texturbasierter Kontext:** Verwenden Sie eine gelernte Einzelbildschätzung als Vorschlag, verlangen Sie aber manuelle Horizont-/Ankerpunkte oder ein zweites Bild, bevor Sie eine folgenreiche Platzierung festschreiben.
- **Lokale Oberflächenorientierung oder Verdeckung erforderlich:** Ergänzen Sie nach der Kamerakalibrierung monokulare Tiefe bzw. Normalen. Betrachten Sie deren Skalierung als unsicher, sofern die Quelle keine metrischen Randbedingungen liefert, die zur Szene passen.
- **Starke Tonnen- oder Fischaugenverzeichnung:** Entzerren Sie zuerst oder wählen Sie ein Kameramodell, das sie abbildet. Eine Pinhole-Schätzung auf einem sichtbar verzerrten Bild ist kein Kalibrierfehler, den ein Compositor reparieren könnte.

Das Mindestergebnis ist keine Brennweitenzahl. Speichern Sie Bildabmessungen, Kameramodell, `K`, Rotationskonvention, Horizont, Definition der Stützebene, Ankerpunkte und ein Validierungs-Overlay. Diese Artefakte machen die Objekttransformation reproduzierbar und zeigen an, wann ein späterer Zuschnitt oder eine Größenänderung sie ungültig macht.

## Werkzeugauswahl und rechtliche Grenzen {#tool-selection-and-legal-boundary}

Die Tabelle ist bewusst kurz gehalten: Wählen Sie einen Schätzer für die unbekannte Größe und anschließend eine separate Evidenzquelle zur Validierung. „Activity“ ist der Wert `pushed_at` des GitHub-Repositorys, geprüft am **21.08.2026**; er zeigt die Aktualität der Wartung an, nicht die Genauigkeit. Code- und Checkpoint-Bedingungen sind getrennte Assets und müssen separat in einem Release-Manifest dokumentiert werden.

| Rolle | Verwendung, wenn | Lokale Schnittstelle bzw. Ausgabe | Code-Lizenz | Gewichte/Checkpoint-Bedingungen | Activity, geprüft 21.08.2026 |
|---|---|---|---|---|---|
| [GeoCalib](https://github.com/cvg/GeoCalib) | Standardvorschlag für Intrinsics + Gravitation aus einem Einzelbild | `GeoCalib().calibrate(image)` liefert Kamera-, Gravitations- und Kovarianz-/Konfidenzfelder; Pinhole- und Radialmodelle | Apache-2.0 | Das offizielle Repository lädt `pinhole`-/`distorted`-Artefakte aus seinem GitHub-Release. Zum Prüfzeitpunkt wurde in README oder LICENSE des Repositorys keine separate Checkpoint-Lizenz angegeben; prüfen Sie das exakte Release-Artefakt vor einer Weitergabe. | 16.08.2026 |
| [DeepLSD](https://github.com/cvg/DeepLSD) | Genaue Szenenlinien und unabhängige VP-Evidenz | Liniensegmente; der Repository-Export unterstützt `--pred_vps` | MIT | Offizielle Checkpoints werden auf `cvg-data.inf.ethz.ch` bereitgestellt; in der README ist keine separate Gewichtslizenz angegeben. | 09.01.2025 |
| [CTRL-C](https://github.com/jwlee-vcl/CTRL-C) | Unabhängiger, linienbasierter Kalibrierungsvorschlag | Fluchtpunkte, Brennweite, Horizontlinie aus Bild + Liniensegmenten | Apache-2.0 | Offizielle Checkpoints sind über Google Drive verlinkt; die Repository-Lizenz deckt den Code ab, eigenständige Checkpoint-Bedingungen werden dort nicht genannt. | 25.06.2024 |
| [MoGe](https://github.com/microsoft/MoGe) | Benötigt Tiefe, Normalen, Intrinsics und Sichtfeld, um Stütz- und Verdeckungsevidenz aufzubauen | Punktkarte, Tiefe, Normalen, normalisierte Intrinsics | MIT; das mitgelieferte DINOv2-Teilmodul steht unter Apache-2.0 | Die offizielle Modellkarte `Ruicheng/moge-2-vitl-normal` deklariert zum Prüfzeitpunkt `mit`. Prüfen Sie die genaue Modellkarte und alle Abhängigkeiten für die gewählte Revision erneut. | 19.08.2026 |

Für eine kommerziell verteilbare Pipeline sollten Sie ein Werkzeug erst dann einsetzen, wenn die **exakte Code-Revision und der exakt heruntergeladene Checkpoint** jeweils mit den für sie geltenden Bedingungen dokumentiert sind. „Offenes Repository“ und „herunterladbarer Checkpoint“ sind keine Lizenzeinstufungen.

## Kalibrierungspipeline {#calibration-pipeline}

1. **Quelle normalisieren.** Bewahren Sie die Originalpixel und EXIF-Daten getrennt auf. Dokumentieren Sie jeden Zuschnitt, jede Größenänderung, Drehung und Objektivkorrektur. Führen Sie die Inferenz auf demselben Raster aus, das für die Platzierung verwendet wird; andernfalls müssen `K` und alle Ankerpunkte mit exakt derselben Bildtransformation umgerechnet werden.
2. **Kameramodell wählen.** Beginnen Sie mit Pinhole für geradlinige Aufnahmen. Wechseln Sie nur dann zu einem Radialmodell, wenn gerade Szenenkanten sichtbar gekrümmt sind; verwenden Sie keinen zusätzlichen Verzeichnungsparameter, nur um fehlerhafte Ankerpunkte zu kompensieren.
3. **Kamera-Vorschlag erzeugen.** Schätzen Sie Intrinsics und Gravitation mit GeoCalib und speichern Sie die Kameraparameter zusammen mit den Kovarianz-/Konfidenzausgaben. GeoCalib geht von einem zentrierten Hauptpunkt aus und optimiert ihn nicht; behandeln Sie stark beschnittene oder außermittige Bilder deshalb als Prüffall.
4. **Unabhängige Geometrie extrahieren.** Führen Sie DeepLSD aus, gruppieren Sie lange, zusammenhängende Linien nach ihrer Richtung und vergleichen Sie die resultierenden Fluchtrichtungen mit dem vorhergesagten Horizont bzw. der Rotation. Bei strukturierten Szenen führen Sie CTRL-C als unabhängigen Vorschlag aus, statt die Ausgaben blind zu mitteln.
5. **Akzeptieren, überarbeiten oder abbrechen.** Akzeptieren Sie nur, wenn sichtbare parallele Kantenfamilien, Horizont und bekannte Vertikale innerhalb der für die Bearbeitung gewählten Bildtoleranz übereinstimmen. Widersprechen sich die Belege, prüfen Sie Objektivverzeichnung, Zuschnitthistorie, nicht-planare „Referenz“-Kanten und die Linienauswahl, bevor Sie Modelle wechseln.
6. **Stützebene aufbauen.** Definieren Sie aus drei oder mehr sichtbaren Ankerpunkten ein ebenenlokales Koordinatensystem und leiten Sie daraus eine Homographie von Ebene zu Bild ab. Ein Render verwendet die Kameraprojektion; ein 2D-Warp verwendet dieselbe Ebenenhomographie. Halten Sie die physikalischen Abmessungen des Objekts im Ebenen-Koordinatensystem, statt einen bildraumbasierten Maßstab nach Augenmaß zu justieren.
7. **Platzieren und validieren.** Projizieren Sie einen Quader, eine Standfläche oder ein Drahtmodell, bevor Sie Pixel rendern. Prüfen Sie Kontaktpunkt, Höhe, Vertikalrichtung, Verdeckungsreihenfolge und die Richtung des Schlagschattens gegenüber der Quelle. Erst danach übergeben Sie das platzierte Asset an Alpha-Compositing, Matting, Relighting oder generative Harmonisierung.

Für eine Ebene `Z = 0` in Weltkoordinaten lautet eine projektive Platzierung:

```text
p ~ K [r1 r2 t] [X Y 1]^T
H_plane = K [r1 r2 t]
```

`~` bedeutet Gleichheit bis auf einen Skalierungsfaktor. Die Gleichung gilt nur für Punkte auf der deklarierten Ebene. Sie darf nicht verwendet werden, um ein volumetrisches Objekt in eine neue Ansicht zu „drehen“.

## Praktische Konfigurationsvorgabe {#practical-configuration-contract}

Dies ist eine Konfiguration auf Anwendungsebene, keine Kommandozeile, die von den Upstream-Projekten akzeptiert wird. Sie macht jede Entscheidung und jede spätere Prüfung explizit.

```yaml
source:
  image: scene.png
  raster_size_px: [4032, 3024]
  image_transform: identity          # crop/resize/rectification chain; never implicit
camera:
  estimator: geocalib
  camera_model: pinhole              # use simple_radial only after visible-distortion review
  principal_point: image_center_assumed
  save: camera.json                  # K, orientation, gravity, covariance, source hash
evidence:
  lines:
    detector: deeplsd
    minimum_length_px: 160
    use_for: [horizon_check, vanishing_direction_check]
  independent_estimate:
    estimator: ctrl-c
    required_for: high_value_structured_scene
acceptance:
  horizon_residual_px_max: 12        # edit-specific; compare at final raster size
  vertical_edge_angle_error_deg_max: 2
  require_two_consistent_edge_families: true
placement:
  support_plane: floor
  anchors_px: [[491, 2210], [2108, 2160], [2999, 1894]]
  object_size_m: [0.42, 0.18, 0.12]
  export: [placement.json, validation-overlay.png]
```

Die Schwellenwerte sind Prüfgrenzen, keine allgemeinen Genauigkeitsaussagen. Verschärfen Sie sie bei einer auffälligen architektonischen Kante; lockern Sie sie nur mit schriftlicher Begründung bei wenig auffälligem Bildmaterial. Speichern Sie ein Overlay mit Horizont, angepassten Fluchtrichtungen, Ankerpunkten, Objekt-Standfläche und Referenzvertikalen, damit ein Bediener ein unplausibles Ergebnis verwerfen kann, ohne Rohmatrizen interpretieren zu müssen.

## Validierungslogik {#validation-logic}

Verwenden Sie unabhängige Beobachtungen statt eines einzelnen skalaren „Konfidenzwerts“:

- **Horizonttest:** Der projizierte Horizont folgt mindestens zwei langen, in der Welt parallelen Kantenfamilien, sofern diese sichtbar sind.
- **Vertikaltest:** Die Welt-Up-Richtung projiziert in dieselbe Richtung wie vertrauenswürdige Vertikale; schiefe Objekte und Rollen einer handgehaltenen Kamera werden ausgeschlossen, sofern deren Pose nicht beabsichtigt ist.
- **Standflächentest:** Alle Kontaktpunkte liegen auf der deklarierten Ebene, und die Maßstabsänderung verläuft monoton mit der Tiefe.
- **Verdeckungstest:** Eine vordergründige Szenengrenze verdeckt das Objekt, bevor Farb-, Schatten- oder Textursynthese beginnt.
- **Relighting-Test:** Der Kontaktschatten entspringt der Standfläche und folgt einer quellkonsistenten Richtung. Die Übereinstimmung der Beleuchtung ist von der Kamerakalibrierung getrennt zu beurteilen.

Wenn eine projektive Schätzung leicht falsch ist, passen Sie sie erneut an explizite Landmarken an, wobei das Kameramodell fixiert bleibt. Zeigt das Residuum eine systematische Krümmung, überprüfen Sie Verzeichnung oder die Vorverarbeitung der Quelle; kompensieren Sie nicht, indem Sie nur das Objekt verschieben.

## Stolperfallen {#gotchas}

- **Zuschnitt ungültigt Intrinsics:** `K` gehört zu einem bestimmten Pixelkoordinatensystem. Ein Zuschnitt verschiebt den Hauptpunkt; eine Größenänderung skaliert Brennweiten und Hauptpunkt. **Lösung:** Behalten Sie die Kette der Bildtransformationen bei und aktualisieren Sie alle Kalibrierungsartefakte gemeinsam.
- **Scheinbar parallele Linien:** Regalkanten, Dachlinien und Pflasterfugen können im 3D-Raum nicht parallel sein oder sich unter Objektivverzeichnung krümmen. **Lösung:** Verwenden Sie mehrere lange Kantenfamilien und verwerfen Sie Cluster, die der bekannten Szenenstruktur widersprechen.
- **Annahme des Hauptpunkts:** Die dokumentierte Annahme eines zentrierten Hauptpunkts bei GeoCalib kann einen außermittigen Zuschnitt verzerren. **Lösung:** Verwenden Sie den unbeschnittenen Rahmen, sofern verfügbar, beschränken Sie die Geometrie manuell oder kennzeichnen Sie das Ergebnis als Vorschlag statt als endgültige Kamera.
- **Tiefe ist standardmäßig kein Maßstab:** Eine monokulare Tiefenkarte kann nützliche Ordnung und Normalen liefern, ohne den absoluten Objektmaßstab festzulegen. **Lösung:** Verankern Sie den Maßstab an einer bekannten Szenenabmessung oder einer kalibrierten Ebene.
- **Ein gutes Matte kann Parallaxe nicht beheben:** Saubere Alpha-Kanten, Inpainting oder Harmonisierung können aus einem Asset in Frontalansicht keine Seitenansicht machen. **Lösung:** Erfassen Sie eine kompatible Ansicht oder verwenden Sie ein 3D-Asset und rendern Sie es mit der angepassten Kamera.
- **Bedingungen können auseinanderlaufen:** Die Code-Bedingungen eines Repositorys lizenzieren nicht automatisch Checkpoints, Trainingsdaten oder ein mitgeliefertes Backbone. **Lösung:** Dokumentieren Sie jedes heruntergeladene Artefakt, jede Revision und die URL der Lizenz bzw. Modellkarte im Release-Manifest.

## Grenzen {#limitations}

Die Kalibrierung aus einem Einzelbild ist unterbestimmt. Wiederholungsmuster, begrenztes Sichtfeld, niedrige Auflösung, Rolling Shutter, starke Unschärfe, Spiegelungen und Szenen ohne verlässliche gerade Linien können mehrere plausible Kameras ergeben. Gelernte Schätzungen können als Vorschläge nützlich sein, begründen aber keine Ground Truth. Weder eine Homographie noch Tiefe/Normalen rekonstruieren verdeckte Oberflächen, objektspezifisches Materialverhalten oder eine physikalisch korrekte Lichtquelle.

Diese Pipeline trennt Geometrie bewusst von der Finalisierung. Verwenden Sie [[intrinsic-decomposition]] für die Begründung von Beleuchtung/Albedo, [[color-checker-and-white-balance]] für die Farbmessung, [[videomama-diffusion-based-video-matting]] für die Alpha-Verfeinerung und [[spatialedit-16b-geometric-control-for-diffusion-based-image-editing]], wenn ein Bildbearbeitungsmodell erst nach einer festen geometrischen Platzierung in Betracht gezogen wird.

## Primärquellen {#primary-sources}

- [GeoCalib-Repository und Inferenz-API](https://github.com/cvg/GeoCalib), [Apache-2.0-Lizenz](https://github.com/cvg/GeoCalib/blob/main/LICENSE) und [v1.0-Checkpoint-Release](https://github.com/cvg/GeoCalib/releases/tag/v1.0).
- [DeepLSD-Repository](https://github.com/cvg/DeepLSD) und [MIT-Lizenz](https://github.com/cvg/DeepLSD/blob/main/LICENSE).
- [CTRL-C-Repository](https://github.com/jwlee-vcl/CTRL-C) und [Apache-2.0-Lizenz](https://github.com/jwlee-vcl/CTRL-C/blob/main/LICENSE).
- [MoGe-Repository](https://github.com/microsoft/MoGe), [Code-Lizenz](https://github.com/microsoft/MoGe/blob/main/LICENSE) und [MoGe-2 ViT-L Normal-Modellkarte](https://huggingface.co/Ruicheng/moge-2-vitl-normal).
