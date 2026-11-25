---
title: "ChronoEdit"
category: projects
date: 2025-11-18
tags: [chronoedit, chronoedit-release-and-adapters, project]
aliases: ["ChronoEdit"]
level: 3
source_sha256: 1b6d4edb567a48210af8048de07a17de04c4888ed08d8e10d0f8538b785e1bc9
translation: machine
translated_at: '2026-10-24'
---
# ChronoEdit {#chronoedit}

**Entwicklungslinie:** `project:chronoedit` · Strang `chronoedit-release-and-adapters`  
**Letztes Ereignis:** 2025-11-18 · 3 datierte seit 2025-10-31 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

ChronoEdit ist ein Diffusers-Bildeditor für Kreative und Entwickler, die eine Objektbearbeitung benötigen, die innerhalb ihrer Szene plausibel bleibt.

- Behandelt das Quell- und das bearbeitete Bild als Endpunkte eines kurzen Videos und nutzt anschließend zeitliches Schlussfolgern, um die Bearbeitung zu steuern.
- Unterstützt promptbasierte Bearbeitung, ein LoRA zur Destillation auf acht Schritte, ein Upscaling-LoRA und ein Paint-Brush-LoRA für die Umwandlung von Skizzen in Objekte.
- Der 14B-Basis-Workflow benötigt etwa 34 GB VRAM mit Model Offload bzw. etwa 38 GB mit zeitlichem Schlussfolgern; der Upscaler ist bis 2K getestet.

Einsetzbar für lokale CUDA-Workflows zur Bildbearbeitung, bei denen die Interaktion mit Objekten wichtig ist. Es handelt sich nicht um einen leichtgewichtigen Desktop-Editor.

## Entwicklungslinie {#development-line}

- **2025-10-31 — ChronoEdit-Projekt, Code, Demo und 14B-Modellressourcen wurden verlinkt.** Am 2025-10-31 veröffentlichten Links die ChronoEdit-Forschungsseite, das GitHub-Repository, den Hugging-Face-Space und das Modell ChronoEdit-14B-Diffusers.
- **2025-11-11 — ChronoEdit 14B Diffusers Upscaler LoRA wurde der Linie hinzugefügt.** Am 2025-11-11 veröffentlichten Links das separate Begleitartefakt ChronoEdit-14B-Diffusers-Upscaler-Lora.
- **2025-11-18 — ChronoEdit 14B Diffusers Paint Brush LoRA wurde der Linie hinzugefügt.** Am 2025-11-18 veröffentlichten Links das separate Begleitartefakt ChronoEdit-14B-Diffusers-Paint-Brush-Lora, nach dem Basismodell und dem Upscaler-LoRA.

## Was sich geändert hat {#what-changed}

ChronoEdit wechselte von einem 14B-Basiseditor zu einer vorgelagerten Diffusers-Pipeline mit zwei aufgabenspezifischen LoRAs.

- 2025-10-31 — der 14B-Diffusers-Checkpoint, der Quellcode und die Demo machten den Basis-Workflow nutzbar; das Repository von NVIDIA datiert die Veröffentlichung des Checkpoints auf 2025-10-29.
- 2025-11-11 — das Upscaler-LoRA ergänzte einen eigenen Workflow zur inhaltserhaltenden Super-Resolution; NVIDIA datiert dessen Veröffentlichung auf 2025-11-10.
- 2025-11-18 — das Paint-Brush-LoRA ergänzte die Bearbeitung von schwarzen Skizzen zu Objekten; NVIDIA datiert dessen Veröffentlichung auf 2025-11-16 und empfiehlt, es mit dem LoRA zur Destillation auf acht Schritte zu kombinieren.
- 2026-09-04 — die offizielle Diffusers-Dokumentation führt das 14B-Basismodell und die zwei LoRAs als unterstützte ChronoEdit-Assets auf.

## So wird es verwendet {#how-to-use-this}

Wir behandeln ChronoEdit ab dem 2025-11-18 als 14B-Diffusers-Basismodell mit separaten Upscaler- und Paint-Brush-LoRA-Adaptern. Prüfen Sie vor dem Ausführen die primäre Dokumentation auf Kompatibilität und Verwendung.

1. Richten Sie Linux mit Python 3.10 ein, installieren Sie die Repository-Umgebung und laden Sie `nvidia/ChronoEdit-14B-Diffusers` herunter.
  — <https://github.com/nv-tlabs/ChronoEdit>
2. Laden Sie den Basis-Checkpoint über `ChronoEditPipeline` in Diffusers auf CUDA, laden Sie das Quellbild und skalieren Sie es auf das unterstützte Latent-Raster.
  — <https://huggingface.co/docs/diffusers/api/pipelines/chronoedit>
3. Führen Sie das Bild mit einem Prompt aus, der die Änderung und das Unveränderte beschreibt; verwenden Sie das letzte erzeugte Frame als bearbeitetes Bild.
  — <https://huggingface.co/docs/diffusers/api/pipelines/chronoedit>
4. Für schnelle Standardbearbeitung laden Sie das mitgelieferte LoRA zur Destillation auf acht Schritte mit `flow_shift=2.0`, Guidance Scale `1.0` und acht Inferenzschritten.
  — <https://github.com/nv-tlabs/ChronoEdit>
5. Für inhaltserhaltende Vergrößerung laden Sie das Upscaler-LoRA mit seinem Super-Resolution-Prompt; bleiben Sie bei oder unter der getesteten Grenze von 2K.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora>
6. Für eine Bearbeitung über gezeichnete Objekte laden Sie Paint Brush zusammen mit dem LoRA zur Destillation auf acht Schritte, stellen eine schwarze Bleistiftskizze bereit und beschreiben das Zielobjekt.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora>

## Bewährte Vorgehensweisen {#best-practices}

- Verwenden Sie für die Basisbearbeitung den mitgelieferten Prompt-Enhancer und die Prompt-Guidance, sofern der Speicher es erlaubt; das Repository bezeichnet dies als Pfad mit den besten Ergebnissen.
  — <https://github.com/nv-tlabs/ChronoEdit>
- Aktivieren Sie zeitliches Schlussfolgern nur, wenn die Szenenkonsistenz den zusätzlichen Speicherbedarf rechtfertigt: Die dokumentierte Anforderung steigt von etwa 34 GB auf 38 GB VRAM.
  — <https://github.com/nv-tlabs/ChronoEdit>
- Belassen Sie die Einstellungen des Destillations-LoRAs bei acht Schritten, Guidance Scale 1.0 und Flow Shift 2.0, anstatt sie als beliebiges LoRA-Preset zu behandeln.
  — <https://github.com/nv-tlabs/ChronoEdit>
- Verwenden Sie für das Upscaler-LoRA dessen inhaltserhaltenden Trigger-Prompt und verzichten Sie auf den Prompt-Enhancer; die offizielle Modellkarte erklärt ihn für unnötig.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora>
- Verwenden Sie für das Paint-Brush-LoRA schwarze Skizzen und kombinieren Sie es mit dem LoRA zur Destillation auf acht Schritte; andere Skizzenfarben funktionieren schlechter.
  — <https://github.com/nv-tlabs/ChronoEdit>

## Durch diesen Stand überholt {#superseded-by-this}

- 2025-11-10 — das Repository-Wrapping als alleinige Inferenzroute ist veraltet: ChronoEdit wurde in Hugging Face Diffusers integriert.
- 2025-11-10 — die reine Basis-Vergrößerung wird durch den Upscaler-LoRA-Workflow ersetzt, der bis 2K getestet ist.
- 2025-11-16 — reine Textbearbeitung für Skizzen wird durch Paint Brush LoRA mit dem Workflow zur Destillation auf acht Schritte ersetzt.

## Weiterhin ungeklärt {#still-unknown}

- Es wurde keine originäre Anleitung in vereinfachtem Chinesisch gefunden; die hier zitierte operative Anleitung ist auf Englisch.
- Offizielle Quellen nennen das 14B-Basismodell und zwei LoRAs, bestätigen aber nicht, ob neuere Checkpoints an anderer Stelle existieren.
- Der offizielle gehostete Space lieferte bei dieser Prüfung einen internen Fehler; die Verfügbarkeit der Live-Demo ist weiterhin nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://research.nvidia.com/labs/toronto-ai/chronoedit/ | ChronoEdit: Towards Temporal Reasoning for Image Editing and World Simulation | 2026-09-04 |
| https://github.com/nv-tlabs/ChronoEdit | nv-tlabs/ChronoEdit — ChronoEdit: Towards Temporal Reasoning for Image Editing and World Simulation | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/chronoedit | ChronoEdit — Hugging Face Diffusers documentation | 2026-09-04 |
| https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers | nvidia/ChronoEdit-14B-Diffusers | 2026-09-04 |
| https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora | nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora | 2026-09-04 |
| https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora | nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora | 2026-09-04 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:chronoedit`, Strang `chronoedit-release-and-adapters`, 3 datierte Ereignisse 2025-10-31 → 2025-11-18.
- **Praktischer Hinweis:** Wir behandeln ChronoEdit ab dem 2025-11-18 als 14B-Diffusers-Basismodell mit separaten Upscaler- und Paint-Brush-LoRA-Adaptern. Prüfen Sie vor der Verwendung die primäre Dokumentation auf Kompatibilität und Verwendungshinweise.
- **Konfidenz:** mittel. Die datierten Überholungen oben bestimmen, was veraltet ist.
