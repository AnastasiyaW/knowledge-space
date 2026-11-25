---
title: "ComfyUI Wan VACE Video Joiner: Release-gebundener Workflow-Vertrag"
description: "Ein ComfyUI-Wan-VACE-Video-Join ist ein release-gebundener Community-Workflow und kein generischer Übergangsknoten; vor der Veröffentlichung eines zusammengefügten Clips sind Workflow-Revision, ComfyUI-/Custom-Node-/Modellabhängigkeiten, Frame-/Zeitstempel-/Farbvorgaben der Eingaben, Regeln für generierte Brückenframes und Schleifen, Zwischenartefakte sowie die visuelle und akustische Prüfung festzuhalten."
category: workflows
tags: [comfyui, wan-vace, video, transitions, provenance, review]
aliases: ["ComfyUI Wan VACE Video Joiner", "Wan VACE Video Joiner"]
level: 2
source_sha256: cd04f963ee940b295ad7c11ea7165fb0e467d19f1139291027288c33c4cfcdbc
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Wan VACE Video Joiner: Release-gebundener Workflow-Vertrag {#comfyui-wan-vace-video-joiner-release-bound-workflow-contract}

Ein Wan-VACE-Join sollte als eine bestimmte ComfyUI-Workflow-Version behandelt
werden, nicht als generischer Übergangsknoten. Das von der Community gepflegte
[ComfyUI Wan VACE Video Joiner repository](https://github.com/stuttlepress/ComfyUI-Wan-VACE-Video-Joiner)
stellt Workflows bereit, die Brückenframes aus dem Kontext auf beiden Seiten
einer Clip-Grenze generieren. Außerdem dokumentiert es versionsabhängige
Abhängigkeiten und bekannte Fehlerbilder. Das ist ein brauchbarer
Ausgangspunkt, aber keine Garantie, dass jedes Paar von Quellclips sauber
zusammenläuft.

## Den ausführbaren Workflow festlegen {#pin-the-executable-workflow}

Für jeden Durchlauf festhalten:

- Workflow-Datei und Repository-Revision sowie alle lokalen Änderungen;
- ComfyUI-Backend- und Frontend-Version, Custom-Node-Revisionen und deren
  Installationsquelle;
- das exakt verwendete VACE-kompatible Modell/Gewicht/Precision sowie den
  Sampler-Subgraphen;
- Eingabeclips, Reihenfolgeregel, Container/Codec, Frameanzahl, Zeitstempel,
  Framerate, Auflösung, Farbinterpretation, Alpha-Behandlung und etwaiges
  Resampling;
- Übergangskontext, Ersetzungs-/Generierungsregel, Schleifenregel, Seed sowie
  Queue- und Run-Identifikatoren; und
- Zwischenframes/-dateien mit ihren Digests, die finalen Encode-Einstellungen
  und den Output-Digest.

Der Upstream-Workflow nennt derzeit Wan 2.1 VACE und Wan 2.2 Fun VACE als
kompatiblen Diffusionsmodell-Pfad. Man sollte nicht annehmen, dass ein
Nicht-VACE-Modell, eine andere Workflow-JSON oder eine nicht fixierte
ComfyUI-Installation denselben Vertrag erfüllt.

## Generierte Brückenframes als abgeleiteten Inhalt behandeln {#treat-generated-bridge-frames-as-derived-content}

Festhalten, welche Frames unveränderte Quellframes sind und welche generiert,
ersetzt, geblendet, interpoliert, farblich angepasst oder neu kodiert wurden.
Ein Übergang, der kontinuierlich wirkt, kann dennoch Belichtung, Farbe,
Geometrie, Text, Bewegung oder sachliche Details verändern. Wird eine Schleife
angefordert, ist die Grenze vom letzten zum ersten Frame separat zu prüfen;
ein Schleifen-Schalter ist kein Nachweis für eine nahtlose Schleife.

Die Quellrechte und der zulässige Bearbeitungsumfang gehören zum Clip-Datensatz.
Audio-Timing und -Kontinuität unabhängig von den Videoframes prüfen, denn
visuelle Ausrichtung belegt keine korrekte Tonspur.

## Die Zielbedingungen der Auslieferung validieren {#validate-the-target-delivery-condition}

Vor der Verarbeitung eines Stapels einen kleinen repräsentativen Join in der
fixierten Umgebung durchführen. Jede Grenze mit der Ziel-Framerate und -Auflösung
prüfen auf fehlende oder doppelte Frames, Ghosting, Bewegungsbrüche,
Helligkeits- oder Farbverschiebungen, veränderte Subjekte oder Objekte sowie
Encode- und Container-Fehler. Für eine einzelne fehlgeschlagene Grenze einen
Neudurchlauf vorsehen, statt einen ganzen Stapel ohne Nachweis zu ersetzen.

Schlägt eine erforderliche Abhängigkeit, ein Modell, eine Eingabeform oder die
Workflow-Validierung fehl, mit einem sichtbaren Abbruch samt erfasster
Umgebung und Fehlermeldung stoppen. Keinen Crossfade, kein anderes Modell,
keine geänderte Framerate und keinen anderen Knoten als gleichwertiges
Ergebnis einsetzen.

## Verwandte Seiten {#related-pages}

- [[temporal-tiling]]
- [[tiled-inference]]
- [[diffusion-inference-acceleration]]
- [[flow-matching]]
