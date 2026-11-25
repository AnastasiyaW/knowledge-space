---
title: "Retusche-Patch-Harmonisierung für gepaarte Vorher-/Nachher-Bilder"
description: "Ein Trainingsdaten-Design für Defect-Inpainting, das den Farbraum des sauberen Zielbilds beibehält und lokalisierte Defektdetails aus einem ausgerichteten Vorher-Bild einbringt."
category: techniques
tags: [retouching, inpainting, image-harmonization, paired-data, frequency-separation, poisson-blending]
level: 3
source_sha256: 3c6735a7c815b2de698f6bdb0b85df99b3aff186b8a0d23617facf3b1b242e69
translation: machine
translated_at: '2026-10-24'
---
# Retusche-Patch-Harmonisierung für gepaarte Vorher-/Nachher-Bilder {#retouch-patch-harmonization-for-paired-beforeafter-images}

Verwende diese Konstruktion, wenn ausgerichtete `before`/`after`-Paare sowohl lokale Defektentfernung als auch großflächigere Farb- oder Tonwertbearbeitungen enthalten. Ziel ist Defect-Inpainting, nicht die Reproduktion jeder Bearbeitung am `after`-Bild. Erzeuge beschädigte Eingaben im Farbraum des sauberen Bilds und behalte das saubere `after`-Bild als Target.

## Problemabgrenzung {#problem-boundary}

Sei `B` ein ausgerichtetes Vorher-Bild, `A` das retuschierte Bild und `M` eine Defektmaske. Eine rohe gepaarte Abbildung `B -> A` zwingt ein Modell, mindestens zwei verschiedene Transformationen zu erklären:

- Entfernung oder Ersetzung lokaler Textur- und Defektdetails;
- globales oder lokales Grading, Beleuchtungs-, Glättungs- und Farbbearbeitungen.

Diese Trennung ist eine Entscheidung beim Datensatzdesign und keine Aussage, die die zitierten Arbeiten belegen. Sie folgt der Formulierung der Bildharmonisierung: Ein Vordergrund soll mit seiner Hintergrunddomäne kompatibel gemacht werden. DoveNet formuliert Harmonisierung in diesem Sinne und trainiert auf synthetischen Composites, die mit echten Bildern gepaart sind; die iHarmony4-Daten stammen aus COCO-, Adobe5k-, Flickr- und day2night-Quellen [DoveNet / iHarmony4, CVPR 2020](https://openaccess.thecvf.com/content_CVPR_2020/html/Cong_DoveNet_Deep_Image_Harmonization_via_Domain_Verification_CVPR_2020_paper.html).

## Empfohlene Paarkonstruktion {#recommended-pair-construction}

1. Richte `B` geometrisch an `A` aus; verwirf Paare mit sichtbarer Verschiebung von Landmarken, Haaren oder Pose innerhalb der erweiterten Maske.
2. Schätze entfernbare Details über eine mehrskalige Hochpass-Zerlegung ab.
3. Beginne jede synthetische Eingabe mit `A`, nicht mit `B`.
4. Injiziere nur ausgewählte Defekt-/Detailresiduen aus `B` innerhalb einer erweiterten Maske `M+`.
5. Harmonisiere die eingesetzte Grenze an die umgebende `A`-Leinwand.
6. Trainiere gegen das unveränderte Target `A`; stelle `M` als Eingabekanal bereit, sofern der Modellvertrag dies erlaubt.

```text
input  = harmonize(A, inject(A, defect_residual(B, A), M+), M+)
target = A
model_input = concat(input, M)  # optional but explicit conditioning
```

Damit wird das Modell bewusst darauf trainiert, eine eingefügte lokale Inkonsistenz zu entfernen, statt eine inverse globale Retuschetransformation zu erschließen.

## Frequenz- und Farbzerlegung {#frequency-and-colour-decomposition}

Für einen Unschärfeoperator `G_sigma` definiere ein Residuum bei Skala `sigma`:

```text
low_sigma(I)    = G_sigma(I)
detail_sigma(I) = I - low_sigma(I)
```

Ein konservatives Defektresiduum lautet:

```text
D = M * max(0, detail_sigma(B) - detail_sigma(A))
X0 = clip(A + D, 0, 1)
```

Werte dies über mehrere Unschärfeskalen aus, zum Beispiel `sigma in {2, 4, 8}` Pixel nach Normalisierung der Auflösung. Die Formel ist eine praktische Syntheseregel und keine Garantie eines Detektors: Wähle zusammenhängende Komponenten erst aus, nachdem geprüft wurde, dass sie entferntem Detail entsprechen und nicht Ausrichtungsfehlern oder bewusster Texturreduktion.

Für farbspezifische Flecken füge ein begrenztes lokales Chroma-Residuum in einem wahrnehmungsorientierten Farbraum hinzu:

```text
delta_ab = clamp(ab(B) - ab(A), -c, c)
X0_lab[M+] = A_lab[M+] + [0, delta_ab]
```

Halte Helligkeits- und Chroma-Steuerung getrennt. HDRNet zeigt, dass gepaarte Eingabe-/Ausgabe-Bearbeitungen durch lokale affine Farbtransformationen im bilateralen Raum angenähert werden können, auch inhaltsabhängige fotografische Bearbeitungen. Daraus folgt nicht, dass eine einzelne globale inverse Transformation das Originalbild eines Retuscheurs wiederherstellt [HDRNet-Projekt und Paper](https://groups.csail.mit.edu/graphics/hdrnet/).

## Optionen zur Grenzharmonisierung {#boundary-harmonization-options}

### Baseline über lokale Statistiken {#local-statistics-baseline}

Passe die Patch-Statistiken an einen Ring unmittelbar außerhalb von `M+` an, pro Kanal oder in Lab. Für den Quell-Patch `P` und den Zielring `R`:

```text
P' = (P - mean(P)) * std(R) / max(std(P), epsilon) + mean(R)
```

Wende dies nur auf Kanäle an, die für die Harmonisierung vorgesehen sind; ein Pass mit lokalen Statistiken darf das eingebrachte Defektsignal nicht auslöschen. Globaler Farbtransfer ist eine nützliche diagnostische Baseline, doch die klassische Methode überträgt globale Erscheinungsstatistiken des Bildes und kodiert keine räumlich lokalen Beleuchtungsentscheidungen [Color Transfer Between Images](https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf).

### Baseline im Gradientenraum {#gradient-domain-baseline}

Poisson-Editing löst ein randbeschränktes Problem der Gradientenanpassung. Für unbekannte Patchwerte `f`, Führungsfeld `v` und Zielrand `f*`:

```text
min_f integral_Ω ||grad(f) - v||², subject to f|∂Ω = f*|∂Ω
```

Äquivalent dazu:

```text
Laplacian(f) = div(v) in Ω, with f|∂Ω = f*|∂Ω
```

Verwende Quellgradienten als Führung, wenn das Erhalten eingebrachter Strukturen wichtig ist; verwende gemischte Gradienten, wenn die Textur des Zielbilds dominieren soll. Dies ist eine Baseline zur Nahtkontrolle und kein Beleg dafür, dass Poisson-Blending ein semantisch korrektes Inpainting erzeugt. Die Originalmethode unterstützt ausdrücklich nahtloses Klonen sowie lokale Änderungen von Textur, Beleuchtung und Farbe [Poisson Image Editing](https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf).

## Lauffähige Referenz: Detailinjektion und Poisson-Nahtkontrolle {#runnable-reference-detail-injection-poisson-seam-control}

Benötigt Python 3.10+, NumPy und OpenCV. Die Eingaben müssen bereits pixelgenau ausgerichtet sein; `before.png`, `after.png` und `mask.png` müssen dieselben räumlichen Abmessungen haben; Maskenpixel ungleich null markieren Defekte.

```python
from pathlib import Path

import cv2
import numpy as np

root = Path(".")
before = cv2.imread(str(root / "before.png"), cv2.IMREAD_COLOR)
after = cv2.imread(str(root / "after.png"), cv2.IMREAD_COLOR)
mask = cv2.imread(str(root / "mask.png"), cv2.IMREAD_GRAYSCALE)
if (before is None or after is None or mask is None
        or before.shape != after.shape or mask.shape != after.shape[:2]):
    raise ValueError("aligned before/after/mask inputs are required")

mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)[1]
expanded = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)
blur_b = cv2.GaussianBlur(before, (0, 0), sigmaX=4)
blur_a = cv2.GaussianBlur(after, (0, 0), sigmaX=4)
detail_b = before.astype(np.int16) - blur_b.astype(np.int16)
detail_a = after.astype(np.int16) - blur_a.astype(np.int16)
removed = np.maximum(detail_b - detail_a, 0)

candidate = after.astype(np.int16)
inside = expanded > 0
candidate[inside] += removed[inside]
candidate = np.clip(candidate, 0, 255).astype(np.uint8)

ys, xs = np.where(expanded > 0)
if len(xs) == 0:
    raise ValueError("mask contains no defect pixels")
center = (int(xs.mean()), int(ys.mean()))
input_image = cv2.seamlessClone(candidate, after, expanded, center, cv2.MIXED_CLONE)
cv2.imwrite(str(root / "synthetic-input.png"), input_image)
```

`cv2.seamlessClone` wird hier nur verwendet, um eine Beschädigung mit kontrollierter Naht zu erzeugen. Das Trainingstarget bleibt `after.png`.

## Verlust- und Evaluationsgrenzen {#loss-and-evaluation-boundary}

Ein maskiertes Rekonstruktionsziel hält die beabsichtigte Region explizit:

```text
L = lambda_m * mean(M * |prediction - A|)
  + lambda_b * mean(ring(M) * |prediction - A|)
  + lambda_u * mean((1 - M) * |prediction - input|)
```

Der unmaskierte Term ist optional und sollte entsprechend dem gewünschten Bearbeitungsumfang des Modells gewählt werden. Berichte keine Benchmark-Ergebnisse der Bildharmonisierung als Ergebnisse für Hautretusche: iHarmony4 besteht aus synthetischen Composite-/Echtbild-Paaren, nicht aus gepaarten klinischen oder kosmetischen Retuschebildern. Evaluiere getrennt nach Ausrichtungsqualität, Präzision der Restmaske, Sichtbarkeit der Naht, Texturerhalt und unerwünschten Änderungen außerhalb von `M`.

## Einschränkungen {#limitations}

- Gepaarte Bilder mit Pose-, Ausdrucks-, Fokus- oder Beleuchtungsänderungen verletzen die Annahme eines Pixelresiduums; Registrierungsfehler werden zu synthetischen Defekten.
- Ein unscharfes Residuum kann einen unerwünschten Hautmangel nicht von bewusster Texturentfernung, Make-up, Entrauschung oder Beleuchtungsretusche unterscheiden. Verwende einen geprüften Maskengenerator und behalte Ablehnungsfälle bei.
- Poisson-Methoden erzwingen Randkompatibilität, können aber niederfrequente Farbe verschieben oder ungeeignete Quellgradienten erhalten; prüfe das Patch-Innere ebenso wie die Nähte.
- Die Angleichung lokalen Mittelwerts und lokaler Standardabweichung setzt voraus, dass der umgebende Ring repräsentativ ist. Sie versagt bei Verdeckungen, scharfen Schatten, Haut-/Haargrenzen und starken Glanzlichtern.
- Eine synthetische Beschädigungsverteilung kann enger sein als reale Produktionsdefekte. Sie ist kein Beweis dafür, dass das trainierte Modell auf neue Kameras, Hauttöne oder Retuschestile generalisiert.

## Fallstricke {#gotchas}

- **Problem: Vor der Synthese wird ein globales Farb-Rollback von Vorher nach Nachher angewendet.** Dies verändert die Zieldomäne und kann unverwandtes Grading zurück in die Defektaufgabe bringen. **Lösung:** Verwende das Rollback nur als Diagnose; erzeuge die beschädigte Eingabe auf der Leinwand von `after`.
- **Problem: Rohe `before`-Pixel werden injiziert.** Rohe Patches enthalten niederfrequente Beleuchtungs-, Glättungs- und Weißabgleichsunterschiede, wodurch die Nahtaufgabe das Defektsignal dominiert. **Lösung:** Beginne mit einem hochfrequenten Residuum; füge ein separat begrenztes Chroma-Residuum nur für geprüfte Fleckenklassen hinzu.
- **Problem: Nahtkontrolle mit einer nicht erweiterten Maske.** Die Blending-Grenze kann auf der Defektkante liegen und einen Ring oder Halo hinterlassen. **Lösung:** Erweitere die Injektions-/Blending-Region und behalte für den Hauptverlust und die Evaluation die ursprüngliche Defektmaske bei.
- **Problem: Nahtloses Klonen wird als Ground Truth für Inpainting behandelt.** Blending im Gradientenraum kann eine Grenze kontinuierlich machen und dabei das falsche Detail bewahren. **Lösung:** Verwende es nur als Baseline für die Eingabebeschädigung und behalte das geprüfte saubere `after`-Bild als Target.

## Siehe auch {#see-also}

- [[skin-retouch-pipeline]] - Defekterkennung, Maskenerweiterung und texturerhaltendes Retusche-Routing
- [[object-removal-inpainting]] - Modellauswahl und Grenzen maskenbasierten Inpaintings
- [[frequency-decomposition-editing]] - Konzepte frequenzgetrennter Bildbearbeitung
- [[color-space-and-gamma-reference]] - Umgang mit Farbräumen und linearem Licht
