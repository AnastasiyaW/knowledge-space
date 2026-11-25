---
title: "Cosmos 3 Edge"
category: projects
date: 2026-07-21
tags: [cosmos-3-edge, nvidia-cosmos-3-edge, project]
aliases: ["Cosmos 3 Edge"]
level: 2
source_sha256: 9833a5dbf4c67e324b9f220dd9bcbfb2f1589b189b07dae8d3799252f67f429f
translation: machine
translated_at: '2026-10-24'
---
# Cosmos 3 Edge {#cosmos-3-edge}

**Entwicklungslinie:** `project:nvidia-cosmos-3-edge` · Thread `cosmos-3-edge`  
**Letztes Ereignis:** 2026-07-21 · 1 datiert seit 2026-07-21 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Cosmos 3 Edge ist ein 4B-Open-Weight-Multimodal-Weltmodell für Robotik-, autonomes-Fahren- und Smart-Space-Teams.

- Eingaben: akzeptiert Text, Bilder, Video und Aktionstrajektorien.
- Ausgaben: erzeugt Text, Bilder, Video und Aktionen.
- Policy: stellt eine DROID-Manipulationsvariante bereit.

Das aktuelle Generator-Release ist auf Bild-zu-Video ausgerichtet, mit 832×480, 121 Frames und 20 Entrauschungsschritten. Verwenden Sie es für lokales Physical-AI-Prototyping, wenn die unterstützten Generator- und Reasoner-Pfade mit dem Zielsystem übereinstimmen.

## Entwicklungslinie {#development-line}

- **2026-07-21 — NVIDIA hat Cosmos3-Edge auf Hugging Face veröffentlicht.** Am 2026-07-21 wurden der Hugging-Face-Blog von NVIDIA sowie die Modell-Repository-Links für Cosmos3-Edge erfasst. Zusammen weisen sie auf einen offiziellen Meilenstein der öffentlichen Verfügbarkeit des Projekts hin, was ihn für dessen Entwicklungsgeschichte relevant macht. Die angegebenen Links belegen keine Angaben zu Fähigkeiten, Lizenz oder Deployment.

## Was sich geändert hat {#what-changed}

- **2026-07-21** — Cosmos3-Edge und Cosmos3-Edge-Policy-DROID wurden am 2026-07-20 als 4B-Modelle unter OpenMDW 1.1 veröffentlicht; das Release ergänzte ein kompaktes multimodales Basismodell und eine DROID-Manipulationspolicy-Variante.
- **2026-08-25** — NVIDIA hat die Edge-Generatorgewichte, Standardwerte, Beispiele und Benchmarks aktualisiert; das gepflegte Generator-Rezept beschränkt sich nun auf Bild-zu-Video und ersetzt frühere Edge-Beispiele für Text-zu-Bild und Text-zu-Video.

## So verwenden Sie das {#how-to-use-this}

Ab 2026-07-21 sollten Praktiker, die Cosmos 3 Edge verfolgen, das Hugging-Face-Modell-Repository von NVIDIA als offiziellen Evaluations- und Referenzpunkt behandeln und vor der Nutzung Fähigkeiten, Lizenzierung und Deployment-Anforderungen anhand der zugrunde liegenden Materialien überprüfen.

1. Laden Sie vor der Verwendung des aktualisierten Generator-Rezepts einen frischen lokalen Snapshot des Modells herunter.
  — <https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62>
2. Für Single-GPU-Reasoning betreiben Sie Cosmos3-Edge mit vLLM und dessen OpenAI-kompatibler API; verwenden Sie vLLM 0.23.0 oder neuer.
  — <https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md>
3. Für die Generator-Inferenz verwenden Sie die aktuellen Bild-zu-Video-Parameter: 832×480, 121 Frames, 20 Schritte, Guidance 6.0 und Flow Shift 12.0.
  — <https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62>

## Best Practices {#best-practices}

- Aktualisieren Sie lokale Snapshots, wenn Sie main verfolgen; das Update vom August hat Gewichte, Standardwerte, Beispiele und Benchmarks verändert.
  — <https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62>
- Laden Sie Edge nicht über Cosmos3OmniForConditionalGeneration; die separate Transformers-Integration verwendet AutoModelForImageTextToText und Cosmos3EdgeForConditionalGeneration.
  — <https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md>
- Lassen Sie Guardrails aktiviert, sofern keine explizite Deployment-Entscheidung die Verantwortung für die Compliance übernimmt; das Deaktivieren wirkt serverweit.
  — <https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md>
- Bündeln Sie den Vision Tower in lokalen Exporten für Offline-Bild- oder Video-Reasoning; andernfalls muss er Komponenten möglicherweise vom Hub nachladen.
  — <https://github.com/NVIDIA/cosmos-framework/blob/main/docs/inference.md>

## Hiermit ersetzt {#superseded-by-this}

- 2026-08-25 — Die Edge-Generatorbeispiele für Text-zu-Bild und Text-zu-Video sind veraltet; die gepflegten Edge-Generatorbeispiele sind ausschließlich Bild-zu-Video.
- 2026-08-25 — Frühere Edge-Generator-Standardwerte sind veraltet; verwenden Sie den aktualisierten Checkpoint und das 480p-Bild-zu-Video-Rezept.

## Weiterhin unbekannt {#still-unknown}

- Der aktuelle Inferenzleitfaden von Cosmos Framework bezeichnet Edge als 2B-Modell, während die Modellkarte und die Release-Ankündigung von NVIDIA es als 4B ausweisen. Die Angabe 4B wird hier verwendet, da sie im Architekturabschnitt der Modellkarte und im Release-Material genannt wird; NVIDIA sollte die Dokumentation abgleichen.
- Das Antwortschema stellt keine separaten Felder event_findings oder new_events bereit. Der Befund vom 2026-07-21 und das separate Update vom 2026-08-25 sind in what_changed erhalten.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/blog/nvidia/cosmos3edge | Einführung in Cosmos 3 Edge | 2026-09-05 |
| https://huggingface.co/nvidia/Cosmos3-Edge | Modellkarte nvidia/Cosmos3-Edge | 2026-09-05 |
| https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62 | Cosmos3-Edge Checkpoint- und Inferenz-Rezept-Update — August 2026 | 2026-09-05 |
| https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md | Cosmos 3 Cookbooks | 2026-09-05 |
| https://github.com/NVIDIA/cosmos-framework/blob/main/docs/inference.md | Inferenzleitfaden für Cosmos Framework | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:nvidia-cosmos-3-edge`, Thread `cosmos-3-edge`, 1 datiertes Ereignis 2026-07-21 → 2026-07-21.
- **Praktischer Hinweis:** Ab 2026-07-21 sollten Praktiker, die Cosmos 3 Edge verfolgen, das Hugging-Face-Modell-Repository von NVIDIA als offiziellen Evaluations- und Referenzpunkt behandeln und vor der Nutzung Fähigkeiten, Lizenzierung und Deployment-Anforderungen anhand der zugrunde liegenden Materialien überprüfen.
- **Konfidenz:** hoch. Die datierten Ersetzungsvermerke oben sind maßgeblich dafür, was veraltet ist.
