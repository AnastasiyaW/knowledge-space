---
title: "Z-Image-Turbo-Fun-Controlnet-Union"
category: projects
date: 2025-12-12
tags: [project, z-image-turbo-fun-controlnet-union, z-image-turbo-fun-controlnet-union-development, z_image]
aliases: ["Z-Image-Turbo-Fun-Controlnet-Union", "Z-Image-Turbo-Fun-Controlnet-Union-2.0"]
level: 2
source_sha256: 1087c343347ac56a0adacd640b707f9f92139bd0a459d59ac4acd6299fac351b
translation: machine
translated_at: '2026-10-24'
---
# Z-Image-Turbo-Fun-Controlnet-Union {#z-image-turbo-fun-controlnet-union}

**Entwicklungslinie:** `project:z-image-turbo-fun-controlnet-union` · Thread `z-image-turbo-fun-controlnet-union-development`  
**Letztes Ereignis:** 2025-12-12 · 2 datierte Ereignisse seit 2025-12-02 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Z-Image-Turbo-Fun-Controlnet-Union ist eine Familie von ControlNet-Gewichten für Z-Image-Turbo in VideoX-Fun. Funktionen: Steuerung der Generierung über Konturen, Tiefe, Pose, Linien, Scribble und Gray; Nutzung von Inpaint; Einsatz eines separaten Tile-Checkpoints für Super-Resolution. Die aktuelle Union 2.1-2602-8steps unterstützt sieben Kontrolltypen und ist für 8 Schritte ausgelegt. Fazit: Dies ist ein lokaler Workflow und kein gehosteter Inference-Provider; der aktuelle Zweig 2.1 hat 1.0 und 2.0 für die praktische Anwendung ersetzt.

## Entwicklungslinie {#development-line}

- **2025-12-02 — Initialer Meilenstein des Z-Image-Turbo-Fun-Controlnet-Union-Repositorys.** ControlNet auf sechs Blöcken mit Canny, HED, Depth, Pose und MLSD.
- **2025-12-12 — Meilenstein des Z-Image-Turbo-Fun-Controlnet-Union-2.0-Repositorys.** Mehr steuerbare Blöcke, längeres Training und Inpaint-Modus.

## Was sich geändert hat {#what-changed}

2025-12-02 wurde das ursprüngliche Z-Image-Turbo-Fun-Controlnet-Union veröffentlicht: ControlNet auf sechs Blöcken mit Canny, HED, Depth, Pose und MLSD. 2025-12-12 wurde Z-Image-Turbo-Fun-Controlnet-Union-2.0 veröffentlicht: mehr steuerbare Blöcke, längeres Training und Inpaint-Modus. 2025-12-17 behob 2.1 einen Fehler aus 2.0, durch den die Blöcke zwei Forward-Pässe ausführten und die Inference verlangsamten. 2025-12-22 erschienen die 8-Schritt-Destillation 2.1 und das Tile-Modell für Super-Resolution. 2026-01-12 ergänzte 2601 Scribble, Lite-Varianten sowie ein Nachtraining gegen Mask Leakage und Artefakte. 2026-02-26 ergänzte 2602 Gray Control.

## Wie man das nutzt {#how-to-use-this}

Ab 2025-12-02 sollten Praktiker das verlinkte Z-Image-Turbo-Fun-Controlnet-Union-Repository als datierten Ausgangspunkt für diese Linie verwenden. Ab 2025-12-12 sollten sie das verlinkte 2.0-Repository separat evaluieren, statt anzunehmen, dass es mit dem initialen Repository identisch ist.

1. VideoX-Fun klonen und die Modellverzeichnisse `models/Diffusion_Transformer` und `models/Personalized_Model` anlegen.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
2. Die Basisgewichte von Z-Image-Turbo sowie das aktuelle `Z-Image-Turbo-Fun-Controlnet-Union-2.1-2602-8steps.safetensors` herunterladen und das ControlNet in `models/Personalized_Model` ablegen.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
3. Das vorbereitete Control-Bild des gewünschten Typs einspeisen und den 2.1-Workflow aus VideoX-Fun ausführen; für Inpaint das passende Beispiel `predict_i2i_inpaint_2.1.py` verwenden.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
4. Für 2602 Union 8 Diffusionsschritte verwenden und genau einen Kontrolltyp wählen: Canny, Depth, Pose, MLSD, HED, Scribble oder Gray.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>

## Best Practices {#best-practices}

- Für eine neue Installation 2.1-2602-8steps wählen: Diese Version enthält die Korrekturen aus 2.0, die 8-Schritt-Destillation und Gray Control.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
- Einen detaillierten Text-Prompt verwenden; für 2.1 und 2.0 `control_context_scale` im Bereich 0.65–1.00 wählen und beim Inpaint erhöhen, um die Kontinuität des Bildes zu verbessern.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
- Für schwächere Hardware oder ein natürlicheres Ergebnis bei hohem Control Scale die Lite-Varianten 2601/2602 verwenden; dies schwächt die Steuerung ab, weil der Kontrolleinfluss auf weniger Schichten wirkt.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>

## Abgelöst durch diese Version {#superseded-by-this}

- 2025-12-17 — Z-Image-Turbo-Fun-Controlnet-Union-2.0 ist für neue Läufe veraltet: 2.1 behebt den Doppel-Forward-Pass-Fehler und stellt die Geschwindigkeit der Single-Step-Inference wieder her.
- 2025-12-22 — Das nicht destillierte 2.1 wird für die reguläre Generierung durch 2.1-8steps ersetzt: Die Modellkarte empfiehlt 8 Schritte.
- 2026-02-26 — 2.1-2601-8steps unterstützt kein Gray Control; dafür ist 2.1-2602-8steps erforderlich.

## Noch unbekannt {#still-unknown}

- Der Pfad `Z-Image-Turbo-Fun-Controlnet-Union-2.0` leitet derzeit auf 2.1 weiter; eine separate, unveränderliche Modellkarte für 2.0 ist unter dieser URL nicht verfügbar. Die historischen Eigenschaften von 2.0 sind durch den erhaltenen Abschnitt „Models Before 2601“ in der aktuellen Primärkarte belegt.
- Aus den verfügbaren Primärseiten lässt sich nicht ermitteln, welcher Begleittext zu den „The source“-Meldungen gehörte; die Aussagen beziehen sich auf die Veröffentlichungs- und Aktualisierungsdaten der Gewichte im Primär-Repository.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union | alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union — Hugging Face Modellkarte | 2026-09-05 |
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union/commits/main | Commit-Verlauf — Z-Image-Turbo-Fun-Controlnet-Union | 2026-09-05 |
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0 | URL Z-Image-Turbo-Fun-Controlnet-Union-2.0, weitergeleitet auf die gepflegte Modellkarte 2.1 | 2026-09-05 |
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1/commits/main | Commit-Verlauf — Z-Image-Turbo-Fun-Controlnet-Union-2.1 | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:z-image-turbo-fun-controlnet-union`, Thread `z-image-turbo-fun-controlnet-union-development`, 2 datierte Ereignisse vom 2025-12-02 bis 2025-12-12.
- **Praktischer Hinweis:** Ab 2025-12-02 sollten Praktiker das verlinkte Z-Image-Turbo-Fun-Controlnet-Union-Repository als datierten Ausgangspunkt für diese Linie verwenden. Ab 2025-12-12 sollten sie das verlinkte 2.0-Repository separat evaluieren, statt anzunehmen, dass es mit dem initialen Repository identisch ist.
- **Konfidenz:** hoch. Für die Frage, was veraltet ist, sind die datierten Abschnitte „Abgelöst durch diese Version“ maßgeblich.
