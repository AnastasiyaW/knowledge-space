---
title: "Boogu-Image"
category: projects
date: 2026-06-18
tags: [boogu-image, boogu-image-development, boogu_image, project]
aliases: ["Boogu-Image"]
level: 3
source_sha256: 85cddaee9ee3f72d6c4071bfa65d71fe8bc0dc28988b1d03cec2c0f9b7bfd612
translation: machine
translated_at: '2026-10-24'
---
# Boogu-Image {#boogu-image}

**Entwicklungslinie:** `project:boogu-image` · Thread `boogu-image-development`  
**Letztes Ereignis:** 2026-06-18 · 1 datiertes Ereignis seit 2026-06-18 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Boogu-Image ist eine Familie offener Checkpoints für Forschung, für Teams, die ein lokales Pendant zur Kombination aus Qwen-Image und ComfyUI benötigen. — Base: Text-to-Image, dichte chinesische und englische Typografie, Fine-Tuning. — Turbo: Text-to-Image in 3–4 Schritten, vor allem fotorealistisch. — Edit und Edit-Turbo: Bearbeitung per Textanweisung. Umfang: Die Hauptvarianten haben 10B Parameter; Base/Edit sind für 1K, 1.5K und 2K angegeben, Turbo für 1K. Fazit: geeignet für Forschung und lokale Integration, nicht als fertige kostenpflichtige API oder Production-Dienst ohne eigene Schutzmaßnahmen und Validierung.

## Entwicklungslinie {#development-line}

- **2026-06-18 — Öffentliche Projektressourcen von Boogu-Image wurden verlinkt.** An diesem Datum wurde kein separates offizielles Release gefunden; die öffentlichen Einstiegspunkte führten bereits zur Familie 0.1, zum Code, zu den Gewichten und zur Demo.

## Was sich geändert hat {#what-changed}

2026-06-16: Boogu-Image-0.1-Base, -Edit und das vierstufige -Turbo erschienen. 2026-06-17: ComfyUI-Boogu erschien; später wurde dieser Weg nach nativer Unterstützung in ComfyUI zu Legacy. 2026-06-18: An diesem Datum wurde kein separates offizielles Release gefunden; die öffentlichen Einstiegspunkte führten bereits zur Familie 0.1, zum Code, zu den Gewichten und zur Demo. 2026-06-25: Turbo erhielt einen Hotfix-20260625 für Artefakte bei unterschiedlichen Seitenverhältnissen und Hintergrundartefakte, ohne neue Funktionen. 2026-06-30: Die vierstufige Image-to-Image-Variante Edit-Turbo erschien. 2026-07-08: Edit-Turbo erhielt einen Hotfix für Qualitätsverlust und schwache Objektentfernung; empfohlen wird Revision 1K. 2026-07-16: Der technische Bericht Boogu-Image-0.1 wurde veröffentlicht. 2026-07-22: Der Pfad für Online-Serving über vLLM-Omni wurde ergänzt. 2026-07-23: Im Branch npu erschien ein initialer Backend-Support für NPU.

## Verwendung {#how-to-use-this}

Stand 2026-06-18 sollten Praktiker die verlinkte Projektseite, das Repository, die Hugging-Face-Organisation, Demos und die Galerie als initiale Einstiegspunkte zur Evaluierung von Boogu-Image nutzen.

1. Base für dichten Text, Steuerbarkeit und 2K wählen; Turbo für schnelle fotorealistische T2I; Edit oder Edit-Turbo für die Bearbeitung eines Bildes per Anweisung.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
2. Eine saubere Python-3.10-Umgebung mit kompatiblen PyTorch/CUDA anlegen, die Projektabhängigkeiten installieren und den gewünschten Checkpoint über die Hugging-Face-CLI in das lokale Verzeichnis models/ herunterladen.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
3. Für lokales T2I dasselbe device in der Umgebungsvariable und im CLI-Argument setzen, dann inference.py mit dem Pfad zu Base oder Turbo, der Anweisung und output_image_path starten.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md>
4. Für die Bearbeitung einen Edit-kompatiblen Checkpoint verwenden und das Eingabebild zusammen mit der Textanweisung übergeben; für einen portablen Workflow gilt ein Referenzbild als aktuell sichere Obergrenze.
  — <https://raw.githubusercontent.com/vllm-project/vllm-omni/main/recipes/Boogu/Boogu-Image.md>
5. In ComfyUI die Hauptinstallation aktualisieren, die repackagten Dateien von Comfy-Org herunterladen und einen Workflow aus den Standardknoten Load Diffusion Model, Load CLIP mit type boogu, Load VAE und TextEncodeBooguEdit für die Bearbeitung aufbauen.
  — <https://raw.githubusercontent.com/boogu-project/ComfyUI-Boogu/main/README.md>
6. Für API-Serving vLLM-Omni mit --omni auf Base oder Edit starten und die Antwort mit einem festen Seed prüfen; der dokumentierte Start für Base benötigt eine A100/H100 mit 40GB+ VRAM.
  — <https://raw.githubusercontent.com/vllm-project/vllm-omni/main/recipes/Boogu/Boogu-Image.md>

## Best Practices {#best-practices}

- ComfyUI-Boogu nicht ohne besonderen Grund als Legacy installieren: Die aktuelle Anleitung empfiehlt die nativen ComfyUI-Knoten und die repackagten Modelle.
  — <https://raw.githubusercontent.com/boogu-project/ComfyUI-Boogu/main/README.md>
- Für dichte zweisprachige Typografie mit Base auf 2K beginnen; für fotorealistisches T2I standardmäßig Turbo wählen.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
- Für Edit-Turbo den Hotfix-1k-20260708 verwenden, nicht den ursprünglichen Checkpoint: Die Autoren bezeichnen 1K als stabiler.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
- Mit der Default-Pipeline beginnen: Prompt-Tuning ist als optionaler Forschungspfad markiert und weniger robust als der normale Lauf.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md>
- Nicht mehrere Offload-Modi gleichzeitig aktivieren; zuerst einen stabilen Lauf ohne Cache-Beschleunigung erreichen und torch.compile bei schwarzen Frames deaktivieren.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md>
- Nicht ohne eigene Moderation, Validierung und Compliance-Prüfungen in Production einsetzen: Das Projekt beschränkt das Release ausdrücklich auf Forschungszwecke.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>

## Durch dies überholt {#superseded-by-this}

- 2026-06-18: Die Deutung dieses Datums als Startdatum ist veraltet — das offizielle Changelog datiert Base, Edit und Turbo auf 2026-06-16.
- 2026-06-25: Der ursprüngliche Turbo sollte bei Problemen mit Artefakten bei Seitenverhältnissen und Hintergrund durch die Revision hotfix-20260625 ersetzt werden.
- 2026-07-08: Der ursprüngliche Edit-Turbo sollte durch hotfix-1k-20260708 ersetzt werden; den 1.5K-Hotfix gibt es zwar, 1K wird aber als stabiler empfohlen.
- 2026-06-17: Die Installation des Legacy-Custom-Node ComfyUI-Boogu ist nicht mehr der empfohlene Weg; aktuell ist der native ComfyUI-Workflow.

## Weiterhin unbekannt {#still-unknown}

- Das offizielle README veröffentlicht Code und Gewichte unter Apache-2.0 und bezeichnet Boogu-Image-0.1 als "research project rather than an official model release"; die praktische Bedeutung dieser Formulierung für kommerzielle Nutzung ist nicht geklärt.
- Die offizielle Projektseite beschreibt Boogu-Image-0.1-Pro als fünfte Variante, in der geprüften Modellliste auf Hugging Face wurde jedoch kein separater Checkpoint oder eine datierte Ankündigung für Pro gefunden.
- Die Dokumentation widerspricht sich bei der Anzahl der Referenzbilder: Eine frühe Release-Notiz und das vLLM-Rezept nennen eines, während der allgemeine Inference Guide mehrere Pfade beschreibt; bis zu einem separaten reproduzierbaren Test gilt ein Referenzbild als sichere portable Grenze.
- Die Primärdokumente wurden geprüft, eine unabhängige Replikation der angegebenen Arena- und Benchmark-Ergebnisse wurde jedoch nicht durchgeführt.
- Die Daten deuten nicht auf zwei verschiedene Projekte mit dem Namen Boogu-Image hin: Die Links und die aktuellen offiziellen Oberflächen führen zur selben Familie 0.1.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://boogu.org/ | Boogu-Image-0.1 — official project page | 2026-09-05 |
| https://github.com/boogu-project/Boogu-Image | boogu-project/Boogu-Image | 2026-09-05 |
| https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md | Boogu-Image README | 2026-09-05 |
| https://huggingface.co/Boogu | Boogu on Hugging Face | 2026-09-05 |
| https://huggingface.co/Boogu/Boogu-Image-0.1-Edit-Turbo/tree/hotfix-1k-20260708 | Boogu-Image-0.1-Edit-Turbo hotfix-1k-20260708 | 2026-09-05 |
| https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md | Boogu Inference Guide | 2026-09-05 |
| https://raw.githubusercontent.com/boogu-project/ComfyUI-Boogu/main/README.md | ComfyUI-Boogu README | 2026-09-05 |
| https://raw.githubusercontent.com/vllm-project/vllm-omni/main/recipes/Boogu/Boogu-Image.md | vLLM-Omni Boogu-Image recipe | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:boogu-image`, Thread `boogu-image-development`, 1 datiertes Ereignis 2026-06-18 → 2026-06-18.
- **Praktischer Hinweis:** Stand 2026-06-18 sollten Praktiker die verlinkte Projektseite, das Repository, die Hugging-Face-Organisation, Demos und die Galerie als initiale Einstiegspunkte zur Evaluierung von Boogu-Image nutzen.
- **Konfidenz:** mittel. Die datierten Überholungshinweise oben sind maßgeblich dafür, was veraltet ist.
