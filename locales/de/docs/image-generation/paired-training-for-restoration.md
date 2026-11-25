---
title: "Gepaartes Restaurierungstraining: Nachweise und Konditionierungsvertrag"
description: "Gepaartes Restaurierungstraining lernt eine deklarierte Abbildung von einem degradierten Eingang auf ein Zielbild; es erfordert quellausgerichtete und rechtlich freigegebene Paare, einen modellkompatiblen Konditionierungspfad, nach Quelle getrennte Holdout-Mengen und eine Evaluation, die gemessene Wiederherstellung von plausibler Erfindung unterscheidet."
category: techniques
tags: [image-to-image, paired-data, restoration, conditioning, provenance, evaluation]
aliases: ["Image-to-Image Conditioning", "Paired Image Training", "Degradation Pipeline"]
level: 3
source_sha256: f3c171e8a93683dfec26052a9103591415540de40b70b4bcbcaaa1a4985d5bc0
translation: machine
translated_at: '2026-10-24'
---
# Gepaartes Restaurierungstraining: Nachweise und Konditionierungsvertrag {#paired-restoration-training-evidence-and-conditioning-contract}

Gepaartes Restaurierungstraining lernt eine deklarierte Abbildung von einem
degradierten Eingang auf ein genehmigtes Zielbild. Es ist kein gewöhnliches
Text-zu-Bild-Training mit saubereren Beschreibungen, und es darf plausible
generierte Textur nicht als rekonstruierte Quellevidenz darstellen.

[Palette](https://arxiv.org/abs/2111.05826) ist ein konditionales
Image-to-Image-Diffusionsframework, das Aufgaben wie Kolorierung, Inpainting,
Uncropping und JPEG-Restaurierung abdeckt. Die Arbeit belegt die allgemeine
Notwendigkeit einer expliziten Bildkonditionierung; sie schreibt jedoch für
nicht jedes moderne Modell ein bestimmtes Kanallayout, eine Initialisierung,
eine Verlustfunktion, einen Scheduler oder ein Trainingsrezept vor.

## Das Paar definieren {#define-the-pair}

Für jede Probe sind folgende Angaben zu erhalten:

- Herkunfts- bzw. Quellautorität und Rechtedokumentation;
- degradierter Eingang, Ziel und deren Hashes;
- Richtlinie für Ausrichtung, Zuschnitt, Größenänderung und Farbraum;
- deklarierte Degradation oder genehmigte Retusche-Operation;
- bearbeitbare versus geschützte/unbekannte Bereiche; und
- Entscheidung der prüfenden Person sowie etwaige Unsicherheit oder Ausschlussgrund.

Quelle und Ziel müssen dieselbe genehmigte Szene oder eine bewusst spezifizierte
Bearbeitung darstellen. Enthält das Ziel manuelle Verschönerung, generative
Füllung oder unbekannte historische Veränderungen, ist dies zu kennzeichnen,
statt das Ziel als saubere Ground Truth zu behandeln.

## Die Konditionierung muss zum Modell passen {#conditioning-must-match-the-model}

Bildkonditionierte Systeme können Kanalverkettung, Cross-Attention, einen
eigenen Steuerzweig, einen Bild-Encoder oder einen anderen architekturspezifischen
Mechanismus verwenden. Verwende ausschließlich den Konditionierungspfad, der für
den fixierten Checkpoint dokumentiert und trainiert wurde. Das Ändern der
Eingangskanalzahl, das Injizieren von Latents oder das Kopieren eines
Konditionierungsmoduls aus einem anderen Framework erzeugt eine neue
Modellkonfiguration, die eigene Initialisierung, Training und Evaluation
benötigt.

Den vollständigen Konditionierungsvertrag dokumentieren:

- Basismodell/Checkpoint sowie Revisionen von VAE/Encoder;
- Laufzeitumgebung, Scheduler/Zielfunktion und Implementierung des
  Konditionierungsmoduls;
- Vorverarbeitung der Eingangs- und Ziel-Latents bzw. Pixel; und
- Verhalten, wenn die Bedingung fehlt, fehlerhaft, maskiert oder außerhalb der
  Verteilung ist.

Eine Bildbedingung darf niemals stillschweigend verworfen werden, sodass ein
unkonditioniertes Ergebnis zurückgegeben wird, als wäre die Restaurierung
gelungen.

## Ehrliche Degradationsnachweise aufbauen {#build-honest-degradation-evidence}

Synthetische Degradation kann kontrollierte gepaarte Beispiele erzeugen, bildet
aber nur die deklarierten Transformationen ab. Synthetische und beobachtete
reale Degradationen sind unterscheidbar zu halten. Ohne Nachweis darf nicht
behauptet werden, dass Rausch-, Unschärfe-, Kompressions- oder
Herunterskalierungsparameter eine unbekannte Kamera- oder Bearbeitungshistorie
reproduzieren.

Trainings-, Tuning- und Holdout-Daten sind nach Originalasset, Aufnahmesitzung,
Motiv/Produkt und Ableitungskette zu trennen. Benachbarte Zuschnitte oder
mehrere degradierte Versionen desselben Originals gehören in dieselbe Teilmenge.

## Wiederherstellung getrennt von Plausibilität evaluieren {#evaluate-recovery-separately-from-plausibility}

| Nachweistyp | Was er stützen kann |
|---|---|
| Autorisiertes, ausgerichtetes Zielbild | paarweise Rekonstruktionsmetriken und visuelle Fehlerprüfung unter einer definierten Farb- und Zuschnittsrichtlinie |
| Quellfremdes reales degradiertes Bild ohne Zielbild | geprüfte Nützlichkeit und Fehleranalyse, keine Aussage zur Pixelgenauigkeit |
| Generatives oder unsicheres Zieldetail | ein abgeleiteter visueller Vorschlag, niemals rekonstruierte sachliche Ground Truth |

Text, Markierungen, Produktgeometrie, Gesichter, geschützte Bereiche und
Materialdetails sind getrennt von aggregierten Metriken zu prüfen. Ein hoher
visueller Qualitätswert kann mit einer sachlich veränderten Ausgabe
einhergehen.

## Freigabe-Gate {#release-gate}

Ein gepaartes Restaurierungsmodell darf nur mit reproduzierbaren Paaren, einem
modellkompatiblen Konditionierungspfad, quellfremden Holdout-Mengen,
Herkunftsnachweisen für Quelle und Ausgabe sowie einer Richtlinie für unsichere
oder veränderte sachliche Details freigegeben werden. Kann das Modell für den
vorgesehenen Einsatz Wiederherstellung nicht von Erfindung unterscheiden, ist es
nur als geprüfter Verbesserungsvorschlag freizugeben oder aus diesem Workflow
fernzuhalten.

## Verwandte Seiten {#related-pages}

- [[image-restoration-survey]]
- [[synthetic-dataset-pipeline]]
- [[upscaler-evaluation]]
