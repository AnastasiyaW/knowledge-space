---
title: "Generative Modelle"
category: models
tags: [data-science, deep-learning, gan, vae, diffusion, generative]
level: 3
source_sha256: f109a08824da676068f55792ab405de3cf38a3f4581972e04d6041510fc88f23
translation: machine
translated_at: '2026-10-24'
---
# Generative Modelle {#generative-models}

Modelle, die lernen, neue Datenproben aus einer gelernten Verteilung zu erzeugen. Von GANs bis zu Diffusionsmodellen: die Technologie hinter Bildgenerierung, Stilübertragung und Datenaugmentierung.

## GANs (Generative Adversarial Networks) {#gans-generative-adversarial-networks}

Zwei Netze im Wettstreit:
- **Generator** G: erzeugt gefälschte Proben aus zufälligem Rauschen
- **Diskriminator** D: unterscheidet echte von gefälschten Proben

Training: D versucht, korrekt zu klassifizieren, G versucht, D zu täuschen. Dieses adversariale Spiel treibt beide zur Verbesserung an.

### GAN-Varianten {#gan-variants}

| Variante | Grundidee |
|---------|----------|
| **Conditional GAN** | Generator und Diskriminator sind auf ein Klassenlabel konditioniert |
| **CycleGAN** | Ungepaarte Bild-zu-Bild-Übersetzung (A->B und B->A) |
| **StyleGAN** | Stilbasierter Generator für hochwertige Gesichtssynthese |
| **Pix2Pix** | Gepaarte Bild-zu-Bild-Übersetzung |

### CycleGAN {#cyclegan}
Lernt eine bidirektionale Abbildung ohne gepaarte Daten. Anwendungen: Altersprogression, Stilübertragung, Domain Adaptation.

### GAN-Herausforderungen {#gan-challenges}
- **Mode Collapse**: Der Generator erzeugt nur eine begrenzte Vielfalt
- **Trainingsinstabilität**: Oszillationen, fehlende Konvergenz
- **Catastrophic Forgetting**: Das Lernen neuer Kategorien löscht alte
  - **Abhilfe**: Generative Replay (alte generierte Proben während des Trainings wiederverwenden)
  - **Abhilfe**: EWC (Elastic Weight Consolidation) - Änderungen an wichtigen Gewichten bestrafen

## VAE (Variational Autoencoder) {#vae-variational-autoencoder}

Der Encoder bildet die Eingabe auf eine latente Verteilung ab (Mittelwert + Varianz), daraus wird ein Sample gezogen, und der Decoder rekonstruiert die Eingabe.

**Verlust** = Rekonstruktionsverlust + KL-Divergenz (hält den latenten Raum nahe an N(0,1))

**Vorteile gegenüber GANs**: stabiles Training, glatte Interpolation im latenten Raum, explizites Dichtemodell.
**Nachteil**: Ausgaben sind tendenziell unschärfer als bei GANs.

## Diffusionsmodelle {#diffusion-models}

Iteratives Entrauschen von reinem Gaußschen Rauschen, um Proben zu erzeugen. Derzeitiger Stand der Technik bei Bildqualität.

**Vorwärtsprozess**: Über T Schritte wird den Daten schrittweise Rauschen hinzugefügt.
**Rückwärtsprozess**: In jedem Schritt wird das Entrauschen gelernt. Ein neuronales Netz sagt das Rauschen voraus, das abgezogen werden soll.

**Wichtige Modelle**: DDPM, Stable Diffusion, DALL-E, Midjourney.

**Vorteile**: überlegene Probenqualität, stabiles Training, flexible Konditionierung.
**Nachteil**: langsame Generierung (viele Entrauschungsschritte), wobei Distillationsverfahren Abhilfe schaffen.

## 3D-Generierung {#3d-generative}

- **NeRF** (Neural Radiance Fields): lernt eine 3D-Szene aus 2D-Bildern und rendert neue Ansichten
- **Punktwolkengenerierung**: generative Modelle auf Basis von PointNet
- **3D-bewusste GANs**: erzeugen 3D-konsistente Bilder

## Neural Style Transfer {#neural-style-transfer}

Kombiniert den Inhalt eines Bildes mit dem künstlerischen Stil eines anderen. Nutzt vortrainierte CNN-Merkmalsrepräsentationen auf verschiedenen Schichten.

**Drei Komponenten:**
- **Inhaltsbild (C)**: das Foto, das transformiert werden soll
- **Stilbild (S)**: die künstlerische Vorlage (z. B. Van Goghs „Sternennacht")
- **Generiertes Bild (G)**: Ausgabe, die die Struktur von C mit dem Stil von S kombiniert

**Funktionsweise:**
1. Merkmale aus einem vortrainierten CNN (VGG-19) auf mehreren Schichten extrahieren
2. **Inhaltsverlust**: Differenz zwischen den Merkmalen von C und G auf tieferen Schichten (erfasst Struktur/Objekte)
3. **Stilverlust**: Differenz zwischen den Gram-Matrizen der Merkmale von S und G auf mehreren Schichten (erfasst Texturen/Muster/Farben)
4. **Gesamtverlust**: gewichtete Summe aus Inhalts- und Stilverlust
5. G per Gradientenabstieg über die Pixelwerte optimieren

Flache CNN-Schichten erfassen Kanten, Texturen und Farben. Tiefere Schichten erfassen Objekte, Gesichter und Komposition. Stilübertragung nutzt diese Hierarchie aus: Die Statistiken der flachen Schichten werden angeglichen (Stil), während die Aktivierungen der tiefen Schichten erhalten bleiben (Inhalt).

## Anwendungen {#applications}

- **Bildgenerierung**: Gesichter, Kunst, Produktbilder
- **Datenaugmentierung**: Trainingsproben für seltene Klassen erzeugen
- **Neural Style Transfer**: künstlerischen Stil mithilfe von CNN-Merkmalen auf Fotos anwenden
- **Super-Resolution**: Auflösung niedrig aufgelöster Bilder erhöhen
- **Inpainting**: fehlende Bereiche in Bildern auffüllen
- **Text-to-Image**: Bilder aus Textbeschreibungen erzeugen

## Stolperfallen {#gotchas}
- GAN-Training erfordert sorgfältige Hyperparameter-Abstimmung und Überwachung
- Generierte Bilder können Artefakte enthalten (zusätzliche Finger, verzerrter Text)
- Die Evaluation ist schwierig: Der FID-Score ist Standard, aber unvollkommen
- Urheberrechts- und ethische Bedenken bezüglich der Trainingsdaten
- Diffusionsmodelle benötigen für die Generierung viel GPU-Speicher und Zeit

## Siehe auch {#see-also}
- [[cnn-computer-vision]] - CNN-Architekturen, die in Generatoren verwendet werden
- [[neural-networks]] - Grundlagen des Trainings
- [[transfer-learning]] - Feinabstimmung generativer Modelle
