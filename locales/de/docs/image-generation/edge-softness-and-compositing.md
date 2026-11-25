---
title: "Kantenweichheit und Compositing"
description: "Die Kante messen statt sie zu wählen: 10-90-Übergangsbreite, robuste Konturanpassung, signierte Distanzrundung ohne die zwei klassischen Fehler, flächenintegrierte Verkleinerung, prämultipliziertes Resampling und Abdeckungs-Alpha statt verwischtem Alpha."
level: 3
source_sha256: d48c766c7df144c5d61a88ed00a415c6ba7d719702da5f8e740527e38dbccdc9
translation: machine
translated_at: '2026-10-24'
---
# Kantenweichheit und Compositing {#edge-softness-and-compositing}

Jede Einfügung, Maske, Matte oder Komposition trifft ihre Umgebung **an der Kante**, und das Auge
erfasst die Kante vor Farbe oder Geometrie: Treppeneffekt, Halo, Matsch und Aufkleber-Optik werden
alle als Kantenfehler wahrgenommen. Die Kante ist daher keine Geschmacksentscheidung und kein
Bibliotheksstandard, sondern wird am bearbeiteten Frame gemessen und dann reproduziert.

## 1. Weichheit wird gemessen, nicht gewählt {#1-softness-is-measured-not-chosen}

Das Intensitätsprofil senkrecht zur Grenze abtasten und die 10-90%-Übergangsbreite bestimmen.
Über einen Satz von sechs fotografischen Frames lag die gemessene Breite bei **1,75-2,50 px**,
bedingt durch Optik und Kompression und nicht durch Vorliebe. Eine harte 1,0-px-Kante in eine
Umgebung zu setzen, deren eigene Übergänge 2,2 px betragen, *ist* der Treppeneffekt, den der
Kunde meldet.

```python
import numpy as np

def edge_softness_px(gray, points, normals, half=6.0, step=0.25, min_contrast=0.15):
    """Median 10-90 transition width across samples along one boundary.

    points/normals: Nx2 arrays of boundary positions and unit normals (image coords).
    Bilinear sampling at sub-pixel offsets; low-contrast profiles are discarded so
    noise does not dominate the median.
    """
    offsets = np.arange(-half, half + step, step)
    widths = []
    for p, n in zip(points, normals):
        xs = p[0] + n[0] * offsets
        ys = p[1] + n[1] * offsets
        prof = bilinear_sample(gray, xs, ys)
        lo, hi = np.percentile(prof, 2), np.percentile(prof, 98)
        if hi - lo < min_contrast:
            continue
        t = (prof - lo) / (hi - lo)
        i10 = np.interp(0.10, t, offsets) if t[0] < t[-1] else np.interp(0.10, t[::-1], offsets[::-1])
        i90 = np.interp(0.90, t, offsets) if t[0] < t[-1] else np.interp(0.90, t[::-1], offsets[::-1])
        widths.append(abs(i90 - i10))
    return float(np.median(widths)) if widths else float("nan")
```

Den Median über etwa hundert Abtastungen pro Seite bilden; ein einzelnes Profil, das eine
spiegelnde Glanzstelle kreuzt, repräsentiert die Kante nicht.

## 2. Gerade Dinge bekommen gerade Kanten {#2-straight-things-get-straight-edges}

Eine Segmentierungsmaske schwankt um die tatsächliche Grenze. Gegenüber einer angepassten Geraden wich
die Kontur eines ebenen, rechteckigen Objekts um **0,29-0,60 px RMS** ab. Bei einem Objekt, das als
eben und rechteckig bekannt ist (eine Platte, ein Bildschirm, ein Etikett, eine Facette), ist dieses
Schwanken Modellrauschen und keine Form.

Die vier Seiten robust anpassen und für die Ecken schneiden:

```python
def fit_line_huber(pts, iters=6, delta=1.0):
    """Robust line fit; a specular blob or shadow otherwise drags a least-squares fit."""
    w = np.ones(len(pts))
    for _ in range(iters):
        mean = np.average(pts, axis=0, weights=w)
        cov = np.cov((pts - mean).T, aweights=w)
        direction = np.linalg.eigh(cov)[1][:, -1]          # principal direction
        normal = np.array([-direction[1], direction[0]])
        r = (pts - mean) @ normal
        s = 1.4826 * np.median(np.abs(r - np.median(r))) + 1e-9
        a = np.abs(r / s)
        w = np.where(a <= delta, 1.0, delta / a)           # Huber weights
    return mean, normal
```

Das Anpassen der Kontur schließt außerdem Löcher, die die Maske im Inneren des Objekts hinterlassen
hat, weil dunkle Details für Hintergrund gehalten wurden.

## 3. Abgerundete Ecken: die Definition verwenden, keine Näherung {#3-rounded-corners-use-the-definition-not-an-approximation}

Ein abgerundetes Polygon ist die Menge aller Punkte, die höchstens `r` vom Polygon entfernt liegen,
das um `r` nach innen geschrumpft wurde. Pro Kante implementiert:

```python
def rounded_signed_distance(depths, r):
    """depths: per-edge inside-depth (positive inside). Returns signed distance.

    Two classic bugs live in these four lines - see below.
    """
    violation = np.maximum(r - depths, 0.0)                # per-edge shortfall
    outside = np.sqrt(np.sum(violation ** 2, axis=0))      # Euclidean, NOT min()
    inner = np.min(depths, axis=0)
    return np.where(outside > 0, r - outside, inner)       # keep growing inside
```

**Fehler 1 - Bildung von `min` über die Kanten vor der Quadratwurzel.** Algebraisch reduziert sich
das auf `min(depth, r)`, also genau die nicht abgerundete Grenze: Der Radius bewirkt stillschweigend
nichts, während die Maske weiterhin plausibel aussieht. Erkennbar ist das, wenn man `r=12` gegen
`r=0` rendert und einen Unterschied verlangt. Die erwartete Fläche, die an einer rechtwinkligen
Ecke entfernt wird, beträgt `r^2 * (1 - pi/4)`; bei vier Ecken mit `r=12` sind das 124 px, und eine
korrekte Implementierung ergab gemessene 126 px.

**Fehler 2 - Begrenzung des Inneren auf `r`.** Wenn die Distanz im Inneren nicht mehr wächst, sättigt
das Alpha bei `r / (2 * half) + 0.5`. Mit `r = 2.1 px` und einer Weichheit von `5.0 px` ergibt das
**0,92 über das gesamte Innere** - die Einfügung ist transluzent, und das, was sie verdecken soll,
scheint durch. Beide Fehler bestehen eine grüne Testsuite; nur ein Render-Diff deckt sie auf.

Auch der Radius wird gemessen: Über dieselben sechs Frames lag er bei **0,91-15,39 px** (13,8-fach als
Anteil der Objekthöhe). Ein fest codierter Radius ist fast überall falsch.

## 4. Verkleinerung: integrieren, nicht abtasten {#4-minification-integrate-do-not-sample}

Bei einer Verkleinerung um den Faktor 3-4,5 **tastet** `INTER_LANCZOS4` ab, statt die Fläche zu
mitteln, sodass ein dünner Strich in eine punktierte Linie zerfällt. Supersampling mit
Flächenmittelung behob einen gemessenen Strichfehler von **33-39 % -> 0,5-2,2 %**.

```python
import cv2

def integrate_minified_warp(src, M, out_size, scale_x, scale_y, ss=4):
    """Area-integrated warp. Gate: only when BOTH axes shrink by >= 1.2x."""
    if scale_x > 1/1.2 or scale_y > 1/1.2:
        return cv2.warpPerspective(src, M, out_size, flags=cv2.INTER_LANCZOS4)
    w, h = out_size
    big = cv2.warpPerspective(
        src, np.diag([ss, ss, 1.0]) @ M, (w * ss, h * ss), flags=cv2.INTER_NEAREST)
    return big.reshape(h, ss, w, ss, -1).mean(axis=(1, 3)).astype(src.dtype)
```

Die Bedingung ist wichtig: Auf einer Achse, die *vergrößert* wird, erzeugt Blockmittelung Blockartefakte.

## 5. Vor jedem Resampling prämultiplizieren {#5-premultiply-before-any-resample}

Jede Interpolation, die Farbe mit Alpha mischt (Skalierung, Rotation, Verzerrung), muss auf
prämultiplizierten Daten laufen, da sonst die Hintergrundfarbe durch den teiltransparenten Rand
durchbricht - der dunkle Halo um eine helle Einfügung.

```python
def to_premultiplied(rgba_f32):
    rgb, a = rgba_f32[..., :3], rgba_f32[..., 3:4]
    return np.concatenate([rgb * a, a], axis=-1)

def from_premultiplied(pm_f32, eps=1e-6):
    rgb, a = pm_f32[..., :3], pm_f32[..., 3:4]
    return np.concatenate([rgb / np.maximum(a, eps), a], axis=-1)
```

Den Hin- und Rückweg im linearen Licht durchführen, nicht im gammacodierten sRGB - siehe
[[color-space-and-gamma-reference]].

## 6. Abdeckungs-Alpha, kein verwischtes Alpha {#6-coverage-alpha-not-blurred-alpha}

Der Treppeneffekt wird durch den **Anteil der Pixelfläche** behoben, den die Form abdeckt, nicht
durch Weichzeichnen des Alpha-Kanals. Weichzeichnen "heilt" ihn durch Verschmieren: Über 12 Grenzen
gemessen ergab Abdeckungs-Alpha eine Übergangszone von **6,0 -> 2,0 px** und eine Abweichung von der
tatsächlichen Linie von **0,21 -> 0,08 px RMS**. Eine weiche, breite Kante ist keine Lösung für
Aliasing - sie ist eine andere Beanstandung (Matsch statt Stufen).

```python
def coverage_alpha(signed_distance, softness_px):
    """Analytic coverage from a signed distance field; softness measured in step 1."""
    half = max(softness_px, 1e-3) / 2.0
    return np.clip(0.5 + signed_distance / (2.0 * half), 0.0, 1.0)
```

## 7. Einen Parameter prüfen, indem zwei Einstellungen gerendert werden, die sich unterscheiden müssen {#7-verify-a-parameter-by-rendering-two-settings-that-must-differ}

Ein Parameter gilt als belegt, wenn man mit und ohne ihn rendert und **verlangt**, dass sich die
Bilder unterscheiden, und dann die Größe des Unterschieds gegen die Geometrie prüft (die
Eckflächenprüfung `r^2 (1 - pi/4)` oben). Beide Rundungsfehler aus Abschnitt 3 bestanden die
Unit-Tests; erst der Render-Diff hat sie aufgedeckt. Siehe
[[negative-controls-for-verification]].

## Stolperfallen {#gotchas}

- **Problem:** Die Weichheit wurde als Konstante gewählt, "weil es gut aussieht". Auf der Hälfte der
  Frames ist sie sichtbar falsch, und die Beanstandung lautet je nach Richtung "Treppeneffekt" oder
  "Matsch". -> **Lösung:** Die 10-90-Breite am Frame messen und daran angleichen.
- **Problem:** `min` über die Kantentiefen pro Kante vor der Quadratwurzel im SDF für abgerundete
  Ecken. Der Radiusparameter ist wirkungslos, während die Maske korrekt aussieht. -> **Lösung:**
  Euklidische Norm der Verletzungen pro Kante; prüfen, dass sich `r=12` von `r=0` unterscheidet, und
  die Eckfläche gegen `r^2 (1 - pi/4)` prüfen.
- **Problem:** Die Distanz im Inneren der Form ist auf `r` begrenzt, daher sättigt das Alpha im
  Inneren unter 1 und die Einfügung ist durchsichtig. -> **Lösung:**
  `where(outside > 0, r - outside, inner_depth)`; prüfen, dass das Alpha im Inneren == 1 ist.
- **Problem:** RGBA wurde ohne Prämultiplikation skaliert oder verzerrt, was bei hellem Inhalt vor
  dunklem Hintergrund einen dunklen Rand erzeugt. -> **Lösung:** Prämultiplizieren, resamplen,
  Prämultiplikation rückgängig machen, im linearen Licht.
- **Problem:** Lanczos für eine 4-fache Verkleinerung dünner Striche verwendet, die in Striche zerfallen.
  -> **Lösung:** Supersampling mit Flächenintegration, nur wenn beide Achsen verkleinert werden.
- **Problem:** Aliasing wurde durch Weichzeichnen des Alphas "behoben", was eine scharfe Beanstandung
  gegen eine weiche eintauscht. -> **Lösung:** Abdeckungsbasiertes Alpha; die Übergangszone auf der
  gemessenen Breite halten.
- **Problem:** Der Kantenparameter gilt als korrekt, weil die Testsuite grün ist, ohne dass ein
  einziger direkter Vergleichs-Render existiert. -> **Lösung:** Zwei Einstellungen rendern, die sich
  unterscheiden müssen, und mit einer geometrischen Vorhersage vergleichen.

## Siehe auch {#see-also}

- [[retouch-patch-harmonization]] - Anpassung des Patch-Inneren an seine Umgebung
- [[perspective-calibration-for-compositing]] - Geometrie vor der Kantenbehandlung
- [[object-removal-inpainting]] - Randbehandlung bei Entfernungen
- [[tiled-inference]] - Nahtüberblendung zwischen Kacheln
- [[color-space-and-gamma-reference]] - warum das Resampling im linearen Licht erfolgt
- [[intrinsic-decomposition]] - Trennung von Schattierung und Albedo vor dem Überblenden
- [[negative-controls-for-verification]] - Nachweis, dass ein Rendering-Parameter wirksam ist
