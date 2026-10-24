---
title: "UltraPixel"
category: projects
date: 2024-09-20
tags: [project, ultrapixel, ultrapixel-development]
aliases: ["UltraPixel"]
level: 2
source_sha256: 6ddf3572fa026772845d82be11a3203189ae6daa51563debe3626bdf22ddfe82
translation: machine
translated_at: '2026-10-24'
---
# UltraPixel {#ultrapixel}

**Entwicklungslinie:** `project:ultrapixel` · Thread `ultrapixel-development`  
**Letztes Ereignis:** 2024-09-20 · 2 datierte Einträge seit 2024-07-09 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

UltraPixel — eine NeurIPS-2024-Forschungsimplementierung auf Basis von Stable Cascade für Text-zu-Bild-Generierung in mehreren hohen Auflösungen.

- erzeugt Bilder über die Stufen von Stable Cascade mit niedrigauflösender semantischer Führung;
- unterstützt Text-zu-Bild, ein mitgeliefertes Beispiel für personalisierte Katzenbilder und Canny-ControlNet;
- verfügt über einen Community-ComfyUI-Wrapper mit mitgelieferten Workflows.

Die veröffentlichten Werte für eine RTX 4090 mit 24 GB setzen eine Generierung von 4096×4096 über die Stufen C, B und die gekachelte Stufe A bei insgesamt etwa 311 Sekunden an. Fazit: nutzbar für lokale Experimente mit hoher Auflösung, die offizielle Demo läuft derzeit jedoch auf Zero, und es ist kein verwalteter Inferenzanbieter aufgeführt.

## Entwicklungslinie {#development-line}

- **2024-07-09 — Projektseite von UltraPixel geteilt.** Am 2024-07-09 verlinkte ein datierter UltraPixel-Beitrag auf die Website des Projekts. Dies ist der früheste sichtbare öffentliche Verweis auf das Projekt in der abgeschlossenen Entwicklungslinie. Der zugrunde liegende Ankündigungstext und die technischen Aussagen wurden nicht bereitgestellt.
- **2024-09-20 — UltraPixel-Repository und gehostete Demo geteilt.** Am 2024-09-20 verlinkte ein datierter UltraPixel-Beitrag auf ein GitHub-Repository und einen Hugging-Face-Space, zusammen mit einem Verweis auf den früheren „The recorded link“. Damit wurden die öffentlichen Quell- und Demo-Einstiegspunkte des Projekts in der abgeschlossenen Linie erfasst. Die Belege lassen den genauen Release-Status, Codeänderungen oder den Wortlaut der Ankündigung nicht erkennen.

## Was sich geändert hat {#what-changed}

2024-07-09 — UltraPixel wurde als Cascade-Diffusionsmethode für die Text-zu-Bild-Generierung von 1K bis 6K vorgestellt, mit niedrigauflösender Führung, impliziten neuronalen Repräsentationen und skalenbewusster Normalisierung. 2024-09-20 — die lauffähige Implementierung und die gehostete Demo wurden verfügbar; das Release umfasste lokale Gradio- und Skript-Inferenz, Modell-Downloads sowie ControlNet- und Personalisierungspfade.

## So verwendest du es {#how-to-use-this}

Ab dem 2024-09-20 sollten Praktiker das verlinkte GitHub-Repository und den Hugging-Face-Space als erfasste Quell- und Demo-Einstiegspunkte von UltraPixel nutzen. Technische Aussagen und der genaue Release-Status gelten dabei als ungeprüft, bis die verlinkten Materialien gesichtet wurden.

1. Installiere die Abhängigkeiten des Repositorys, lade die benötigten Stable-Cascade-Gewichte sowie die UltraPixel-Parameter herunter und lege sie im Modellverzeichnis des Repositorys ab.
  — <https://github.com/catcathh/UltraPixel>
2. Starte die Gradio-Oberfläche mit `CUDA_VISIBLE_DEVICES=0 python app.py` oder verwende `inference/test_t2i.py` für skriptgesteuerte Text-zu-Bild-Generierung.
  — <https://github.com/catcathh/UltraPixel>
3. Für ComfyUI den Community-Node in `custom_nodes` klonen, seine Anforderungen installieren, `workflow_default.json` oder `workflow_controlnet.json` laden und dann den Prompt in die Warteschlange stellen; beim ersten Lauf werden Modelle nach `ComfyUI/models/ultrapixel` heruntergeladen.
  — <https://github.com/2kpr/ComfyUI-UltraPixel>

## Bewährte Vorgehensweisen {#best-practices}

- Verwende `stage_a_tiled` für die Dekodierung in Stufe A, wenn der VRAM knapp ist; so wird die dokumentierte Out-of-Memory-Situation bei 4096×4096 auf einer RTX 4090 mit 24 GB vermieden, allerdings auf Kosten einer deutlich längeren Laufzeit.
  — <https://github.com/catcathh/UltraPixel>
- Formuliere den Prompt so, dass er Motiv, Hintergrund, Farbe, Beleuchtung und Stimmung angibt; betrachte Qualitätsmodifikatoren als optionale Prompt-Experimente und nicht als Garantie.
  — <https://github.com/catcathh/UltraPixel>
- Halte ControlNet innerhalb der dokumentierten 4K-Obergrenze, sofern du die Steuergewichte nicht feinabstimmst; das veröffentlichte Setup nennt 3840×2160 und 2048×2048.
  — <https://github.com/catcathh/UltraPixel>

## Durch Folgendes ersetzt {#superseded-by-this}

- 2024-09-19 — die frühere Angabe des Repositorys von etwa drei Minuten auf einer RTX 4090 für eine Generierung von 2560×5120 wurde nach der Aktualisierung der PyTorch- und Torchvision-Umgebung durch einen Wert von etwa 60 Sekunden ersetzt.
- 2024-09-26 — der Status von UltraPixel wechselte von einer Preprint-Implementierung zu einem angenommenen Paper der NeurIPS 2024.

## Weiterhin ungeklärt {#still-unknown}

- Das offizielle GitHub-Repository nennt AGPL-3.0, während die Model Card auf Hugging Face Apache-2.0 angibt; die geprüften Quellen erklären nicht, welche Lizenz für einen kombinierten Einsatz gilt. Vor einer kommerziellen Nutzung ist dies daher zu prüfen.
- Die öffentliche Demo-Seite meldet, dass sie auf Zero läuft; daraus folgt nicht, dass der Space dauerhaft nicht verfügbar ist, sondern nur, dass zum Zeitpunkt der Prüfung keine aktive gehostete Sitzung verfügbar war.
- Es wurde keine aktuelle, vom Projekt selbst gepflegte ComfyUI-Integration gefunden. Der verfügbare ComfyUI-Node bezeichnet sich selbst als Work in Progress und beschreibt sich als modifizierten Wrapper.
- Für diesen Eintrag wurde keine chinesischsprachige Primär- oder Community-Quelle verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://jingjingrenabc.github.io/ultrapixel/ | UltraPixel Gallery | 2026-09-05 |
| https://arxiv.org/abs/2407.02158 | UltraPixel: Advancing Ultra-High-Resolution Image Synthesis to New Peaks | 2026-09-05 |
| https://github.com/catcathh/UltraPixel | catcathh/UltraPixel | 2026-09-05 |
| https://huggingface.co/roubaofeipi/UltraPixel | roubaofeipi/UltraPixel Model Card | 2026-09-05 |
| https://huggingface.co/spaces/roubaofeipi/UltraPixel-demo | roubaofeipi/UltraPixel-demo | 2026-09-05 |
| https://github.com/2kpr/ComfyUI-UltraPixel | 2kpr/ComfyUI-UltraPixel | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:ultrapixel`, Thread `ultrapixel-development`, 2 datierte Ereignisse 2024-07-09 → 2024-09-20.
- **Praktischer Hinweis:** Ab dem 2024-09-20 sollten Praktiker das verlinkte GitHub-Repository und den Hugging-Face-Space als erfasste Quell- und Demo-Einstiegspunkte von UltraPixel nutzen. Technische Aussagen und der genaue Release-Status gelten dabei als ungeprüft, bis die verlinkten Materialien gesichtet wurden.
- **Konfidenz:** hoch. Für die Frage, was veraltet ist, sind die datierten Angaben unter „Durch Folgendes ersetzt“ maßgeblich.
