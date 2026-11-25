---
title: "GeneX"
category: projects
date: 2024-12-16
tags: [genex, genex-development, project]
aliases: ["GenEx", "GeneX"]
level: 2
source_sha256: c00987acc5928b0371ac57519eb7fa5f5e5e4c139a0ecc7085235f669af22712
translation: machine
translated_at: '2026-10-24'
---
# GeneX {#genex}

**Entwicklungslinie:** `project:genex` · Thread `genex-development`  
**Letztes Ereignis:** 2024-12-16 · 2 datierte Ereignisse seit 2024-11-20 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

GeneX ist eine Forschungspipeline für das Prototyping von Embodied AI und World Models. Sie erzeugt aus einem Bild ein 360°-Panorama, generiert vorwärtsgerichtete Panoramavideos, rotiert die Ansicht und exportiert Explorationsclips. Das veröffentlichte Paar besteht aus einem 12B-BF16-Initializer und einem 2B-FP16-Explorer; die öffentliche interaktive Demo ist pausiert. Verwenden Sie es für Experimente in simulierten Welten, nicht für den Einsatz in der Navigation in der realen Welt.

## Entwicklungslinie {#development-line}

- **2024-11-20 — GeneX teilte eine interaktive Demonstration.** Am 2024-11-20 verlinkte GeneX eine interaktive Demonstration des Projekts als öffentlichen praktischen Meilenstein.
- **2024-12-16 — GeneX verlinkte seine Projektwebsite.** Am 2024-12-16 verlinkte GeneX seine Projektwebsite und verwies auf die frühere Projektnachricht. Damit wurde nach der interaktiven Demonstration ein öffentlicher Einstiegspunkt geschaffen.

## Was sich geändert hat {#what-changed}

2024-11-20 — Generative World Explorer präsentierte interaktive Exploration einer panoramakonditionierten, videogenerierten Umgebung.  
2024-12-16 — GenEx ergänzte die fehlende Stufe der Welt-Initialisierung: Ein einzelnes RGB-Bild und eine optionale Beschreibung werden vor der aktionskonditionierten Panoramavideo-Exploration zu einem 360°-Panorama.  
Heute gefunden — die aktuelle offizielle Implementierung ist ein lokaler Workflow mit zwei Modellen; die Model Cards wurden am 2025-05-06 aktualisiert.

## Verwendung {#how-to-use-this}

Ab dem 2024-11-20 konnten Anwender GeneX über die verlinkte interaktive Demonstration nutzen; ab dem 2024-12-16 konnten sie zusätzlich die verlinkte Projektwebsite als öffentlichen Einstiegspunkt verwenden.

1. Erstellen Sie eine CUDA-Python-Umgebung und installieren Sie die vom Projekt aufgelisteten Inferenz-Abhängigkeiten, einschließlich Diffusers, Transformers, PyTorch, Pillow und Pakete für den Video-Export.
  — <https://github.com/GenEx-world/genex/tree/main/code/inference>
2. Laden Sie World Initializer mit einem perspektivischen Bild; es erzeugt ein equirektangulares Panorama mit 2048×1024 Pixeln, optional mit einem Textprompt zur Initialisierung.
  — <https://huggingface.co/genex-world/World-Initializer-image-to-panorama>
3. Laden Sie World Explorer, setzen Sie das erzeugte Panorama als aktuelles Bild und generieren Sie mit der Explorer-Pipeline ein vorwärtsgerichtetes Videosegment.
  — <https://github.com/GenEx-world/genex/tree/main/code/inference>
4. Wiederholen Sie Vorwärtsbewegungen und Panoramarotationen, um einen Pfad zu erkunden, und exportieren Sie das Ergebnis als MP4 oder GIF. Verwenden Sie lokale GPUs, da die gehostete interaktive Demo derzeit pausiert ist.
  — <https://github.com/GenEx-world/genex>

## Best Practices {#best-practices}

- Verwenden Sie die beiden Stufen in der richtigen Reihenfolge: Explorer erwartet ein 360°-Panorama, daher sollten Sie zuerst eines initialisieren, anstatt Explorer ein gewöhnliches perspektivisches Bild zu übergeben.
  — <https://github.com/GenEx-world/genex/tree/main/code/inference>
- Beginnen Sie mit der dokumentierten Explorer-Baseline – 1024×512, 25 Frames, 30 Inferenzschritte und Noise Augmentation 0,02 – bevor Sie die Steuerung verändern.
  — <https://github.com/GenEx-world/genex/tree/main/code/inference>
- Begrenzen Sie Bewegungen nahe an Hindernissen: Die Publikation berichtet, dass Befehle, die sich übermäßig nah an einer Wand bewegen, die nachfolgend erzeugten Frames verschlechtern können.
  — <https://arxiv.org/html/2412.09624v4>
- Behandeln Sie bei jedem realen Embodied-Workflow die erzeugten Ansichten als simulierte Priors und behalten Sie die sensorbasierte Verifikation bei; Sim-to-Real-Transfer, Sensorintegration, dynamische Bedingungen und Schutzmaßnahmen bleiben offene Herausforderungen.
  — <https://arxiv.org/html/2412.09624v4>

## Durch diesen Stand überholt {#superseded-by-this}

- 2024-11-20 — Implementierungsanleitungen, die von einem bereits verfügbaren Panorama ausgehen, sind für das spätere GeneX-System unvollständig; die Dezember-Erweiterung ergänzt vor der Exploration die Welt-Initialisierung von Bild zu Panorama.

## Weiterhin ungeklärt {#still-unknown}

- Die Arbeiten vom November und Dezember hängen zusammen: Die Dezember-Publikation bezeichnet sich ausdrücklich als Erweiterung der November-Arbeit. Es gibt jedoch keine Migrationsnotiz des Projekts, die die interaktive Demo-Version von 2024 einem aktuellen Code-Tag oder Checkpoint zuordnet.
- Es wurde kein lokaler Lauf durchgeführt. Der benötigte GPU-Speicher, die Reproduzierbarkeit der vollständigen Demo und die Kompatibilität mit aktuellen CUDA- und Diffusers-Versionen sind nicht verifiziert.
- In den geprüften Quellen wurde keine chinesischsprachige Anwenderdokumentation des Projekts gefunden; chinesischsprachige Praxisberichte wurden nicht verwendet.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://generative-world-explorer.github.io/#interactive_demo | Generative World Explorer | 2026-09-04 |
| https://www.genex.world/ | Generative World Explorer | 2026-09-04 |
| https://arxiv.org/abs/2411.11844 | Generative World Explorer | 2026-09-04 |
| https://arxiv.org/abs/2412.09624 | GenEx: Generating an Explorable World | 2026-09-04 |
| https://arxiv.org/html/2412.09624v4 | GenEx: Generating an Explorable World | 2026-09-04 |
| https://github.com/GenEx-world/genex | GenEx-world/genex | 2026-09-04 |
| https://github.com/GenEx-world/genex/tree/main/code/inference | GenEx-Inferenzdokumentation | 2026-09-04 |
| https://huggingface.co/genex-world/World-Initializer-image-to-panorama | genex-world/World-Initializer-image-to-panorama | 2026-09-04 |
| https://huggingface.co/genex-world/GenEx-World-Explorer | genex-world/GenEx-World-Explorer | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:genex`, Thread `genex-development`, 2 datierte Ereignisse 2024-11-20 → 2024-12-16.
- **Praxishinweis:** Ab dem 2024-11-20 konnten Anwender GeneX über die verlinkte interaktive Demonstration nutzen; ab dem 2024-12-16 konnten sie zusätzlich die verlinkte Projektwebsite als öffentlichen Einstiegspunkt verwenden.
- **Konfidenz:** mittel. Die datierten Einträge „Durch diesen Stand überholt“ sind maßgeblich dafür, was veraltet ist.
