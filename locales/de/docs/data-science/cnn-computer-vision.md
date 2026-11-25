---
title: "CNNs und Computer Vision"
category: models
tags: [data-science, deep-learning, cnn, computer-vision, image-classification]
level: 4
source_sha256: 0abaa1ed448dbc1aba55baa2ddf043620908b9a5e820413eec929df0e723aa59
translation: machine
translated_at: '2026-10-24'
---
# CNNs und Computer Vision {#cnns-and-computer-vision}

Convolutional Neural Networks nutzen die räumliche Struktur von Bildern durch die Erkennung lokaler Muster und Translationsinvarianz. Von der Klassifikation bis zur Generierung haben CNNs das visuelle Verstehen revolutioniert.

## Bild als Daten {#image-as-data}

Bild = 3D-Tensor (Höhe x Breite x Kanäle). Graustufen: 1 Kanal. RGB: 3 Kanäle. Jeder Pixel = Ganzzahl [0, 255].

Für einfache Modelle: Auf 1D flachziehen (28x28 -> 784 Merkmale). Problem: Die räumliche Struktur geht verloren. CNNs lösen dieses Problem.

## Faltungsschicht (Convolution Layer) {#convolution-layer}

Einen kleinen Filter (Kernel) über die Eingabe schieben. Jeder Filter erkennt ein Muster (Kante, Textur, Form). Die Faltung besteht aus zwei Operationen: elementweise multiplizieren, dann summieren. Drei Objekte: Eingabebild, Filter (Kernel), Ausgabebild (Feature Map).

- **Kernelgröße**: typischerweise 3x3, 5x5. Gestapelte kleine Kernel ergeben ein großes rezeptives Feld
- **Stride**: Schrittweite. Stride 2 halbiert die räumlichen Dimensionen
- **Padding**: "same" erhält die Größe, "valid" verkleinert sie
- **Kanäle**: Eingabekanäle werden durch die Filtertiefe bestimmt; Ausgabekanäle = Anzahl der Filter
- **1x1-Faltung**: Linearkombination der Kanäle (Bottleneck, Dimensionsreduktion)
- **Bias-Term**: Jeder Filter hat einen skalaren Bias, der nach der Faltungssumme und vor der Aktivierung addiert wird

### Faltung als Merkmalserkennung {#convolution-as-feature-detection}

Verschiedene Kernel erkennen verschiedene Merkmale:
- **Blur-Kernel**: Mittelwertfilter glättet das Bild (Rauschreduktion)
- **Kantenerkennung**: Sobel-artige Filter heben Grenzen zwischen Regionen hervor
- **Schärfungskernel**: verstärkt Unterschiede zwischen benachbarten Pixeln

In einem trainierten CNN werden Kernel nicht von Hand entworfen, sondern per Backpropagation gelernt. Frühe Schichten lernen Kanten- und Texturdetektoren; tiefere Schichten lernen komplexe Mustererkenner (Augen, Räder, Text).

### Pooling {#pooling}

Reduziert die räumlichen Dimensionen (Downsampling). **Max-Pooling** (Maximum im Fenster) ist am gebräuchlichsten. Typisch: 2x2, Stride 2.

- Pool-Größe 2 mit Stride 2: 100x100 -> 50x50 (halbiert jede Dimension)
- Erzeugt Translationsinvarianz: Kleine Verschiebungen der Eingabe ändern die gepoolte Ausgabe nicht
- **Average-Pooling**: Mittelwert statt Maximum. Wird in einigen Architekturen verwendet (GoogLeNet)
- **Global Average Pooling**: Reduziert die gesamte Feature Map auf einen einzigen Wert pro Kanal. Ersetzt Flatten + Dense in modernen Architekturen (weniger Parameter, weniger Overfitting)

### Zweistufige CNN-Architektur {#cnn-two-stage-architecture}

Ein CNN besteht aus zwei Stufen:

1. **Merkmalsextraktion**: abwechselnd Conv- und Pool-Schichten. Hierarchisch: Jede Schicht erkennt Merkmale aus der Ausgabe der vorherigen Schicht. Diese Stufe ist ein spezialisierter Bild-Feature-Transformer
2. **Klassifikation**: standardmäßige Dense-(vollverbundene) Schichten, die die extrahierten Merkmale für Klassifikation/Regression verwenden

```php
Input -> [Conv -> BN -> ReLU -> Pool] x N -> Flatten -> Dense -> Output
```

Diese Trennung erklärt, warum Transfer Learning funktioniert: Stufe 1 lernt allgemeine Bildmerkmale (Kanten, Texturen, Formen), während Stufe 2 aufgabenspezifische Klassifikation lernt.

## Architekturentwicklung {#architecture-evolution}

| Architektur | Jahr | Zentrale Neuerung |
|-------------|------|-------------------|
| **AlexNet** | 2012 | Erstes tiefes CNN, das ImageNet gewann. ReLU, Dropout, Data Augmentation |
| **VGG** | 2014 | Nur 3x3-Faltungen, tief gestapelt. Einfach, einheitlich |
| **GoogLeNet/Inception** | 2014 | Parallele Faltungen unterschiedlicher Größe, zusammengeführt. 1x1-Bottlenecks |
| **ResNet** | 2015 | Skip-Connections: Ausgabe = F(x) + x. 50-152 Schichten |
| **DenseNet** | 2017 | Jede Schicht ist mit allen vorherigen Schichten verbunden |
| **MobileNet** | 2017 | Depthwise-separable Faltungen für Mobil- und Edge-Geräte |
| **EfficientNet** | 2019 | Compound Scaling (Breite, Tiefe, Auflösung) |
| **ViT** | 2020 | Vision Transformer: Transformer auf Bild-Patches angewendet |

### ResNet-Skip-Connections {#resnet-skip-connections}

Lösen das Problem verschwindender Gradienten bei tiefen Netzen:
```php
input -> Conv -> BN -> ReLU -> Conv -> BN -> (+input) -> ReLU
```
Die Identitäts-Abkürzung lässt Gradienten direkt durch das Netz fließen. ResNet hat gezeigt, dass mit Skip-Connections das Training eines 152-Schichten-Netzes machbar ist und flachere Alternativen übertrifft.

### Warum Architektur-Fallstudien lohnen {#why-study-architecture-case-studies}

Neuronale Netzarchitekturen, die bei einer Computer-Vision-Aufgabe gut funktionieren, lassen sich meist auf andere übertragen. Wichtige Muster des gegenseitigen Einflusses:
- **Skip-Connections von ResNet** tauchten in Transformer-Architekturen auf
- **Inceptions Multi-Scale-Verarbeitung** beeinflusste Feature Pyramid Networks
- **ViT zeigte**, dass Transformer-Attention Faltungen vollständig ersetzen kann

Das Lesen von Architektur-Papers schafft Intuition, ähnlich wie Programmierer durch das Lesen fremden Codes lernen.

## Transfer Learning {#transfer-learning}

Ein vortrainiertes Modell (ImageNet: 1,2 Mio. Bilder, 1000 Klassen) als Ausgangspunkt verwenden.

```python
import torchvision.models as models
import torch.nn as nn

model = models.resnet50(pretrained=True)

# Option A: Feature extraction (freeze everything, replace head)
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(2048, num_classes)

# Option B: Fine-tune last layers
for param in model.layer4.parameters():
    param.requires_grad = True
model.fc = nn.Linear(2048, num_classes)
```

**Faustregel**: Kleinerer Datensatz = mehr Schichten einfrieren; größerer Datensatz = mehr Schichten feinabstimmen.

## Objekterkennung (Object Detection) {#object-detection}

Objekte mit Bounding Boxes und Klassenlabels lokalisieren.

### Zweistufige Detektoren {#two-stage-detectors}
- **R-CNN**: Region Proposals (Selective Search) -> CNN pro Region -> Klassifikation
- **Fast R-CNN**: CNN auf dem gesamten Bild, Merkmalsextraktion pro Region aus der Feature Map
- **Faster R-CNN**: gelerntes Region Proposal Network (RPN). Vollständig End-to-End

### Einstufige Detektoren {#one-stage-detectors}
- **YOLO**: Bild in ein S x S Raster unterteilen, jede Zelle sagt Boxen und Klassen voraus. Ein einziger Forward-Pass. Echtzeitfähig
- **SSD**: Feature Maps unterschiedlicher Skalen für Objekte unterschiedlicher Größe

### Detektionsmetriken {#detection-metrics}
- **IoU**: Schnittmenge / Vereinigungsmenge von vorhergesagter und Ground-Truth-Box. >= 0,5 = korrekt
- **mAP@0.5**: mittlere Average Precision bei IoU-Schwelle 0,5
- **mAP@0.5:0.95**: gemittelt über IoU-Schwellen von 0,5 bis 0,95 (Schrittweite 0,05)
- **NMS** (Non-Maximum Suppression): Entfernt überlappende Detektionen, behält die mit der höchsten Konfidenz

## Segmentierung {#segmentation}

### Semantische Segmentierung {#semantic-segmentation}
Jeden Pixel klassifizieren. Keine Unterscheidung einzelner Instanzen.
- **FCN**: FC-Schichten durch Faltungen ersetzen, anschließend hochskalieren
- **U-Net**: Encoder-Decoder mit Skip-Connections. Hervorragend für medizinische Bildgebung
- **DeepLab**: Atrous- (dilatierte) Faltungen für ein größeres rezeptives Feld

### Instanzsegmentierung {#instance-segmentation}
Objekte erkennen UND Pixelgrenzen segmentieren.
- **Mask R-CNN**: Faster R-CNN + Masken-Vorhersagezweig pro erkannter Box

### Segmentierungsmetriken {#segmentation-metrics}
- **mIoU**: mittlere IoU über alle Klassen (primäre Metrik)
- **Dice-Koeffizient**: 2*|A ∩ B| / (|A| + |B|). Entspricht F1

## Generative Modelle {#generative-models}

- **GAN**: adversariales Training Generator vs. Diskriminator. Herausforderungen: Mode Collapse, Instabilität
- **VAE**: Kodierung in eine latente Verteilung, Sampling, Dekodierung. Glatte Interpolation
- **Diffusion**: iteratives Entrauschen aus reinem Rauschen. Aktueller Stand der Technik für Bildqualität
- **CycleGAN**: ungepaarte Bild-zu-Bild-Übersetzung (Stiltransfer, Domänenanpassung)

## 3D-Vision {#3d-vision}
- **Tiefenschätzung**: Abstand pro Pixel aus einem 2D-Bild vorhersagen
- **Punktwolkenverarbeitung**: PointNet für 3D-Punktdaten
- **NeRF**: 3D-Szene aus 2D-Bildern lernen, neue Ansichten rendern

## Faltung auf Farbbildern (3D-Kernel) {#convolution-on-color-images-3d-kernels}

Graustufenfaltung: Ein 2D-Filter gleitet über ein 2D-Bild. Farbbilder: Ein **3D-Filter** gleitet über eine 3D-Eingabe (H x W x C).

- Eingabe: (H, W, 3) für RGB. Kernel: (k, k, 3), gleiche Tiefe wie die Eingabekanäle
- Summation über alle drei Kanäle an jeder Position -> ein einzelner Skalarwert
- Ein 3D-Kernel wirkt als **Farbmusterdetektor**: Ein Filter für "roter Kreis" passt nicht zu blauen Kreisen
- Mehrere Filter -> mehrere Ausgabekanäle: N Filter der Form (k, k, 3) erzeugen eine Ausgabe der Form (H', W', N)
- Jede weitere Faltungsschicht: Eingabekanäle = Filteranzahl der vorherigen Schicht, nicht 3

Deshalb hat die erste Faltungsschicht nur wenige Parameter (3 Eingabekanäle), tiefere Schichten dagegen viele (64, 128, 256 Eingabekanäle aus den vorherigen Filteranzahlen).

## CNNs für Zeitreihenklassifikation {#cnns-for-time-series-classification}

CNNs sind nicht auf Bilder beschränkt. Sie funktionieren mit allen Daten, die lokale räumliche/zeitliche Struktur haben.

### 1D-Faltung für Zeitreihen {#1d-convolution-for-time-series}

Eingabeform: (Batch, Zeitschritte, Merkmale) = (N, T, D). Conv1D statt Conv2D verwenden.

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, kernel_size=5, activation='relu',
                           input_shape=(128, 9)),  # T=128, D=9
    tf.keras.layers.MaxPooling1D(pool_size=3),
    tf.keras.layers.Conv1D(64, kernel_size=3, activation='relu'),
    tf.keras.layers.GlobalMaxPooling1D(),  # alternatives: Flatten, GlobalAvgPooling1D
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
```

**Auswahl der Kernelgröße**: Für längere Sequenzen (T=128+) größere initiale Kernel (5-7) verwenden. Für kurze Sequenzen (T~10) kleinere Kernel (3). Ein größeres T rechtfertigt größere Kernel, nach demselben Prinzip wie bei größeren Bildern.

### Erkennung menschlicher Aktivität (Human Activity Recognition, HAR) {#human-activity-recognition-har}

Klassische CNN-Anwendung auf Sensor-Zeitreihen. Eingabe: Beschleunigungs- und Gyroskopdaten vom Smartphone (T=128 Zeitschritte, D=9 Kanäle für x/y/z von 3 Sensoren).

**Architektur mit mehreren Eingaben**: Zeitreihen-CNN mit tabellarischen Merkmalen (Statistiken, FFT-Merkmale) per Konkatenation kombinieren:

```python
# Time series branch
ts_input = tf.keras.Input(shape=(128, 9))
x = tf.keras.layers.Conv1D(32, 5, activation='relu')(ts_input)
x = tf.keras.layers.MaxPooling1D(3)(x)
x = tf.keras.layers.GlobalMaxPooling1D()(x)

# Tabular branch
tab_input = tf.keras.Input(shape=(num_tabular_features,))
y = tf.keras.layers.Dense(64, activation='relu')(tab_input)

# Combine
combined = tf.keras.layers.Concatenate()([x, y])
output = tf.keras.layers.Dense(num_classes, activation='softmax')(combined)
model = tf.keras.Model(inputs=[ts_input, tab_input], outputs=output)
```

### CNN für Zeitreihenprognose {#cnn-for-time-series-forecasting}

CNN als Merkmalsextraktor verwenden, dann eine Dense-Schicht für die Vorhersage. Univariate Reihen in eine Eingabe der Form (T, 1) umformen.

```python
model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, kernel_size=3, activation='relu',
                           input_shape=(window_size, 1)),
    tf.keras.layers.Conv1D(64, kernel_size=3, activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)  # single step forecast
])
```

Hinweis: Die Werte teilen sich durch die Pooling-Schichten nicht immer glatt auf. Die Ausgabeformen jeder Schicht immer mit `model.summary()` prüfen.

## Fallstricke {#gotchas}
- Bilder immer normalisieren (ImageNet-Statistiken: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- Data Augmentation ist bei Vision-Aufgaben fast immer vorteilhaft
- Höhere Eingabeauflösung = bessere Genauigkeit, aber quadratisch höherer Rechenaufwand
- Vortrainierte Modelle erwarten bestimmte Eingabegrößen und Normalisierungen
- YOLO-Versionen unterscheiden sich stark; für einen fairen Vergleich die Variante prüfen
- **Conv1D für Zeitreihen**: Der Kernel gleitet nur entlang der Zeitachse, nicht räumlich. Die Eingabeform unterscheidet sich von Conv2D
- **GlobalMaxPooling vs. Flatten**: GlobalMaxPooling reduziert unabhängig von der Eingabelänge auf eine feste Größe. Flatten benötigt eine feste Eingabegröße
- **Modelle mit mehreren Eingaben** benötigen `tf.keras.Model` (Functional API), nicht `Sequential`

## Siehe auch {#see-also}
- [[neural-networks]] - allgemeine Grundlagen des Deep Learning
- [[transfer-learning]] - detaillierte Strategien für Vortraining und Feinabstimmung
- [[data-augmentation]] - Augmentierungstechniken für Vision
- [[generative-models]] - GANs, VAEs und Diffusion im Detail
- [[time-series-analysis]] - klassische Zeitreihenmodelle
- [[rnn-sequences]] - RNN als Alternative für Sequenzdaten
