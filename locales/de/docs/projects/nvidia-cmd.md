---
title: "Context-Matched Distillation"
category: projects
date: 2026-08-21
tags: [context-matched-distillation, nvidia-cmd, nvidia-cosmos, project]
aliases: ["Context-Matched Distillation"]
level: 3
source_sha256: 46b3df60cce689ec9190e316927f45ccd2f36058f4fce02058c5b554b5330e7c
translation: machine
translated_at: '2026-10-24'
---
# Context-Matched Distillation {#context-matched-distillation}

**Entwicklungslinie:** `project:nvidia-cmd` · Thread `context-matched-distillation`  
**Letztes Ereignis:** 2026-08-21 · 1 datiert seit 2026-08-21 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Context-Matched Distillation (CMD) ist NVIDIAs kausale Distribution-Matching-Distillationsmethode und Checkpoint-Veröffentlichung für autoregressive Bild-zu-Video-Generierung.

- Generierung mit Chunk-1 oder Chunk-4.
- Lange Rollouts.
- Kamerakonditionierte Varianten.

Der veröffentlichte CMD-Code und die Ableitungen sind ausschließlich für nicht-kommerzielle Forschung und Lehre bestimmt. Das zugrunde liegende Cosmos-Basismodell erfordert zusätzlich eine Zugriffsgenehmigung. Nutzen Sie es zur Evaluierung interaktiver kausaler Bild-zu-Video-Forschung, nicht als einsetzbaren kommerziellen Video-Stack.

## Entwicklungslinie {#development-line}

- **2026-08-21 — Context-Matched-Distillation-Ressourcen veröffentlicht.** Am 2026-08-21 veröffentlichte NVIDIA die Projektseite, das Code-Repository, die Modellseite und die Bild-zu-Video-Demo von Context-Matched Distillation (CMD). Diese Links machten das Projekt öffentlich einsehbar.

## Was sich geändert hat {#what-changed}

- 2026-08-13 — Das CMD-Paper stellte kausales Lehrer-Scoring, Prefix Scoring und Prefix Corruption für die Few-Step-Distillation autoregressiver Videos vor.
- 2026-08-19 — Das Hugging-Face-Repository für CMD wurde angelegt.
- 2026-08-21 — CMD wurde mit seiner Projektseite, dem Code-Repository, dem Modell-Repository und einem Link zu einer Bild-zu-Video-Demo dokumentiert.
- 2026-08-23 — NVIDIA ergänzte die CMD-Modellkarte und Checkpoints für kurze, lange und kamerakonditionierte Chunk-1/Chunk-4-Varianten.
- 2026-08-24 — NVIDIA aktualisierte die Modellkarte um die arXiv-Zitation.
- 2026-08-30 — Das Modell-Repository erhielt eine config.json.

## So nutzen Sie das {#how-to-use-this}

Stand 2026-08-21: Evaluieren Sie CMD, indem Sie den verlinkten Code, die Modellseite, die Dokumentation und die Demo gemeinsam prüfen.

1. Beantragen Sie Zugriff auf das Cosmos-Predict2.5-2B-Basismodell, bevor Sie CMD ausführen.
  — <https://huggingface.co/nvidia/Cosmos-Predict2.5-2B>
2. Klonen Sie CMD, erstellen Sie die Python-3.10-Conda-Umgebung, installieren Sie die Requirements und FlashAttention und installieren Sie anschließend das Paket im Entwicklungsmodus.
  — <https://github.com/nv-tlabs/cmd>
3. Laden Sie alle CMD-Checkpoints herunter oder nur den Checkpoint, der für die gewählte Variante benötigt wird.
  — <https://huggingface.co/nvidia/cmd>
4. Stimmen Sie den Checkpoint mit der mitgelieferten Konfiguration, dem Bild, dem Prompt, der Blockgröße, dem Local-Attention-Fenster und der gewünschten Anzahl an Ausgabe-Frames ab; das Repository enthält einen Aufruf für ein Chunk-4-Kurzvideo.
  — <https://github.com/nv-tlabs/cmd>
5. Führen Sie den mitgelieferten Beispiel-Runner für eine der Varianten kurz, lang oder kamerakonditioniert aus, bevor Sie die Beispieleingaben ersetzen.
  — <https://github.com/nv-tlabs/cmd>

## Best Practices {#best-practices}

- Behandeln Sie die Zuordnung von Checkpoint und Konfiguration als feste Vorgabe: t bezeichnet die Framedauer und l die Länge der lokalen Aufmerksamkeit, während Chunk-1 und Chunk-4 unterschiedliche Generierungsgranularitäten verwenden.
  — <https://huggingface.co/nvidia/cmd>
- Evaluieren Sie lange Rollouts mit repräsentativen Eingaben: Autoregressive Fehler akkumulieren sich und verschlechtern die zeitliche Konsistenz, feine Details, Gesichter, Hände, Text und schnelle Bewegungen.
  — <https://huggingface.co/nvidia/cmd>
- Erwarten Sie nicht, dass das öffentliche DL3DV-Setup die berichtete Qualität reproduziert; es dient nur als End-to-End-Pipeline-Check, während die berichteten Trainingsdaten nicht veröffentlicht sind.
  — <https://github.com/nv-tlabs/cmd>
- Halten Sie die Nutzung von CMD und seine Ableitungen nicht-kommerziell, sofern sich die Lizenzierung nicht ändert; bei Weiterverbreitung müssen Lizenz und Hinweise erhalten bleiben.
  — <https://github.com/nv-tlabs/cmd/blob/main/LICENSE>

## Hiermit abgelöst {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die Commit-Historie auf Hugging Face datiert das ursprüngliche CMD-Repository auf 2026-08-19 und den Upload von Checkpoint und Modellkarte auf 2026-08-23, während das Ereignis vom 2026-08-21 bereits die Modell-URL enthielt. Die Linkliste wurde möglicherweise nach dem datierten Ereignis ergänzt; dies lässt sich anhand der verfügbaren Erstquellen-Historie nicht klären.
- Die öffentliche Demo-Seite war als Hugging-Face-Space erreichbar, legte aber keine reproduzierbaren Laufzeiteinstellungen und keine Verfügbarkeitsgarantie offen.
- Es wurden keine Erstquellen-Benchmarks nach der Veröffentlichung und keine Belege für einen produktiven Einsatz gefunden; die Ergebnisse im Paper bleiben Forschungsbelege und kein Produktions-SLA.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2608.13391 | Context-Matched Distillation: Teacher Causality for Autoregressive Video Distillation | 2026-09-05 |
| https://hmrishavbandy.github.io/cmd-site/ | Context-Matched Distillation project page | 2026-09-05 |
| https://github.com/nv-tlabs/cmd | nv-tlabs/cmd | 2026-09-05 |
| https://huggingface.co/nvidia/cmd | nvidia/cmd model card | 2026-09-05 |
| https://huggingface.co/nvidia/cmd/commits/main | nvidia/cmd commit history | 2026-09-05 |
| https://huggingface.co/spaces/hugging-apps/cmd-i2v-demo | NVIDIA CMD Image to Video demo | 2026-09-05 |
| https://huggingface.co/nvidia/Cosmos-Predict2.5-2B | Cosmos-Predict2.5-2B model card | 2026-09-05 |
| https://github.com/nv-tlabs/cmd/blob/main/LICENSE | NVIDIA OneWay Noncommercial License | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:nvidia-cmd`, Thread `context-matched-distillation`, 1 datiertes Ereignis 2026-08-21 → 2026-08-21.
- **Praktischer Hinweis:** Stand 2026-08-21 sollten Praktiker, die CMD evaluieren, den verlinkten Code-Repository, die Modellseite, die Projektdokumentation und die Bild-zu-Video-Demo gemeinsam heranziehen, statt die Ankündigung als unbelegte Forschungsreferenz zu behandeln.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
