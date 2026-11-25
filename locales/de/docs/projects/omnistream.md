---
title: "OmniStream"
category: projects
date: 2026-03-13
tags: [omnistream, omnistream-development, project]
aliases: ["OmniStream"]
level: 2
source_sha256: e0a25cffb8d3c956624cf3149b589f06f4b01dca603b9174b3150717d7dfd162
translation: machine
translated_at: '2026-10-24'
---
# OmniStream {#omnistream}

**Entwicklungslinie:** `project:omnistream` · Thread `omnistream-development`  
**Letztes Ereignis:** 2026-03-13 · 1 datiertes seit 2026-03-13 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

OmniStream ist ein visuelles Backbone mit 0,3 Mrd. Parametern, abgeleitet von DINOv3 ViT-L, für die kontinuierliche Merkmalsextraktion aus Videos. Es verwendet kausale raumzeitliche Aufmerksamkeit, 3D-RoPE und einen persistenten KV-Cache.

- verarbeitet Frames online, ohne vorherige Aufmerksamkeitswerte neu zu berechnen;
- überträgt ein eingefrorenes Backbone auf Perzeptions-, Rekonstruktions-, VLM- und VLA-Aufgaben;
- wird als F32-Hugging-Face-Checkpoint mit 1,21 GB sowie als offizielles Inferenz-Repository ausgeliefert.

Der öffentliche Checkpoint ist ein Bild-Feature-Extraktor. Das Repository führt Pre-Training sowie den VLM/VLA-Code weiterhin als nicht veröffentlicht. Er ist aktuell für CUDA-Experimente zur Merkmalsextraktion nutzbar, aber noch nicht als schlüsselfertiger VLM- oder Robotersteuerungs-Stack.

## Entwicklungslinie {#development-line}

- **2026-03-13 — OmniStream wurde öffentlich über seine Projekt-, Code- und Modellressourcen verlinkt.** Am 2026-03-13 erschienen Links zur OmniStream-Projektseite, zum GitHub-Quellcode-Repository und zur Hugging-Face-Ressource. Damit liegt ein datierter öffentlicher Referenzpunkt für die Web-, Code- und Modellpräsenz vor, ohne dass eine bestimmte Version, Fähigkeit oder ein bestimmter Veröffentlichungsstatus festgelegt wäre.

## Was sich geändert hat {#what-changed}

2026-03-12 — der technische Bericht (arXiv:2603.12265) wurde eingereicht. Er beschreibt das vereinheitlichte kausale Streaming-Backbone, das Training auf 29 Datensätzen und den Evaluierungsumfang.

2026-03-13 — Projektmaterialien, Code und der StreamFormer/OmniStream-Checkpoint wurden veröffentlicht bzw. aktualisiert. Die Veröffentlichung machte den 0,3-B-F32-Feature-Extraktor verfügbar. Commits an diesem Tag aktualisierten das Repository-README und die arXiv-Referenz.

2026-03-15 — das Repository entfernte umgebungsspezifische DINOv3-Pfade und den mitgelieferten DINO-Text-Code. Ein konfigurierbarer Platzhalter ersetzte den fest codierten lokalen Pfad. Dies überholt Anleitungen, die vom ursprünglichen Dateisystemlayout der Autoren ausgehen.

Der Schritt vom 13. März ergänzt zwei praktische Einschränkungen, die sich aus den Ereignislinks allein nicht ergeben: Der veröffentlichte Checkpoint hat 0,3 Mrd. Parameter, und das Repository hat weder Pre-Training- noch VLM/VLA-Code freigegeben.

## So verwendest du es {#how-to-use-this}

Ab dem 2026-03-13 sollten die verlinkte OmniStream-Projektseite, das Quellcode-Repository und die Hugging-Face-Ressource als Ausgangspunkt für die Evaluierung dienen. Exakte Modellversion, Lizenz und Nutzungshinweise sind eigenständig zu prüfen.

1. Klone das offizielle Repository, erstelle eine Python-3.10-Conda-Umgebung und installiere dann den gepinnten PyTorch-2.6.0-CUDA-12.4-Stack sowie Transformers 4.56.1.
  — <https://github.com/Go2Heart/OmniStream>
2. Lade `AutoImageProcessor` und `OmnistreamMultiFrameTransformer` aus `StreamFormer/OmniStream`, verschiebe beide Tensoren und das Modell auf CUDA, rufe `eval()` auf und führe die Inferenz unter `torch.no_grad()` aus.
  — <https://huggingface.co/StreamFormer/OmniStream>
3. Behandle die Ausgabe als visuelle Merkmale (`last_hidden_state`, `hidden_states`, `pooler_output` und Patch-Indizes); für eine nachgelagerte Aufgabe musst du selbst eine Integrationsschicht bereitstellen.
  — <https://github.com/Go2Heart/OmniStream>

## Best Practices {#best-practices}

- Verwende für den dokumentierten Inferenzpfad die gepinnten CUDA-/PyTorch- und Transformers-Versionen des Repositorys. Der Checkpoint wird nicht über einen Hugging Face Inference Provider bereitgestellt.
  — <https://github.com/Go2Heart/OmniStream>
- Behalte das offizielle `model.py` in der Umgebung. Die Model Card besagt, dass es für den Beispiel-Workflow zur Merkmalsextraktion erforderlich ist.
  — <https://huggingface.co/StreamFormer/OmniStream>
- Verlasse dich nicht auf die früheren, autorenlokalen DINOv3-Pfade. Konfiguriere den Speicherort der DINOv3-Gewichte für deine eigene Umgebung.
  — <https://github.com/Go2Heart/OmniStream/commit/780e5d7d60ea7788e9ee62395dc0d465d02dc873>

## Hierdurch überholt {#superseded-by-this}

- 2026-03-15 — umgebungsspezifische DINOv3-Pfade und der mitgelieferte DINO-Text-Quellcode wurden entfernt. Reproduziere nicht das bisherige Setup mit lokalen Pfaden.
- 2026-03-15 — beschreibe die verfügbare Implementierung nicht als veröffentlichten End-to-End-VLM/VLA-Stack. Diese Code-Veröffentlichungen sind weiterhin als TODO-Einträge gelistet.

## Weiterhin unbekannt {#still-unknown}

- Die Primärquellen geben keinen datierten Veröffentlichungszeitstempel für den Hugging-Face-Checkpoint an. Der genaue Zeitpunkt, zu dem die Gewichte herunterladbar wurden, lässt sich vom Projekt- und Code-Update am 2026-03-13 nicht trennen.
- Die Projektseite berichtet Ergebnisse für VLM- und VLA-Transfers, der öffentliche VLM- und VLA-Implementierungscode ist jedoch weiterhin nicht veröffentlicht. Die Produktionsreife dieser Pfade ist nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://arxiv.org/abs/2603.12265 | OmniStream: Mastering Perception, Reconstruction and Action in Continuous Streams | 2026-09-05 |
| https://go2heart.github.io/omnistream/ | OmniStream-Projektseite | 2026-09-05 |
| https://github.com/Go2Heart/OmniStream | Go2Heart/OmniStream | 2026-09-05 |
| https://github.com/Go2Heart/OmniStream/commits/main | OmniStream-Commit-Historie | 2026-09-05 |
| https://github.com/Go2Heart/OmniStream/commit/780e5d7d60ea7788e9ee62395dc0d465d02dc873 | fix: Hartkodierung und dino.txt | 2026-09-05 |
| https://huggingface.co/StreamFormer/OmniStream | StreamFormer/OmniStream Model Card | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:omnistream`, Thread `omnistream-development`, 1 datiertes Ereignis 2026-03-13 → 2026-03-13.
- **Praktischer Hinweis:** Ab dem 2026-03-13 sollten die verlinkte OmniStream-Projektseite, das Quellcode-Repository und die Hugging-Face-Ressource als Ausgangspunkt für die Evaluierung dienen. Exakte Modellversion, Lizenz und Nutzungshinweise sind eigenständig zu prüfen.
- **Konfidenz:** hoch. Die datierten Überholungsvermerke sind maßgeblich dafür, was veraltet ist.
