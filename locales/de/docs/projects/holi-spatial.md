---
title: "Holi-Spatial"
category: projects
date: 2026-03-10
tags: [holi-spatial, holi-spatial-development, project]
aliases: ["Holi-Spatial"]
level: 3
source_sha256: b36c0752eaf78d23aa6d7b41cf6ba46c010d363893a539a47c2ee666c29910b9
translation: machine
translated_at: '2026-10-24'
---
# Holi-Spatial {#holi-spatial}

**Entwicklungslinie:** `project:holi-spatial` · Thread `holi-spatial-development`  
**Letztes Ereignis:** 2026-03-10 · 1 datiertes Ereignis seit 2026-03-10 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

Holi-Spatial ist eine öffentliche Datenaufbereitungspipeline für Forschungsteams, die 3D Gaussian Splatting, Masken, 3D-Boxen und räumliche QA aus ScanNet-, ScanNet++- oder DL3DV-Szenen benötigen.

- Tiefen- und Punktwolken: erstellt Tiefen- und Punktwolken mit DA3 und führt anschließend PGSR/3DGS aus.
- Objektannotation und QA: segmentiert Objekte mit SAM3 und einem VLM, hebt Masken nach 3D und erzeugt QA.
- Export multimodaler Datensätze: wandelt die Ausgabe in einen SFT-Datensatz für LLaMA-Factory um.

12K optimierte 3DGS-Szenen und über 4M räumliche Annotationen laut Paper; der verfügbare Checkpoint HoliSpatial-2M-QA-Qwen3-VL-8B ist ein BF16-Modell mit 9B Parametern und 17,6 GB.

Dies ist eine Offline-Pipeline für Kuratierung und Training mit CUDA, externen Modellen und eigenen Szenen, kein interaktiver 3D-Dienst.

## Entwicklungslinie {#development-line}

- **2026-03-10 — Holi-Spatial-Projektressourcen wurden veröffentlicht.** Am 2026-03-10 wurde Holi-Spatial mit einer öffentlichen Projektseite, einem Quellcode-Repository und einer Hugging-Face-Ressource verknüpft. Dies ist ein wesentlicher öffentlicher Entwicklungsbezugspunkt, auch wenn die vorliegenden Belege den genauen Veröffentlichungsstatus oder die Fähigkeiten der verlinkten Ressource nicht belegen.

## Was sich geändert hat {#what-changed}

- 2026-03-08 — arXiv v1 veröffentlicht: beschreibt eine dreistufige automatisierte Pipeline und Holi-Spatial-4M.
- 2026-03-10 — Holi-Spatial erhielt eine öffentliche Projektseite und ein Repository für räumliche Video-Annotation, mit Angaben von 13K+ Szenen, 1,3M+ QA und 300K+ 3D-Boxen.
- 2026-03-19 — Die offizielle Hugging-Face-Seite markiert den Datensatz ScanNetPP als aktualisiert.
- 2026-03-21 — Die offizielle Hugging-Face-Seite markiert den Datensatz ScanNet_v2 als aktualisiert.
- 2026-03-22 — Die offizielle Hugging-Face-Seite markiert HoliSpatial-QA-2M als aktualisiert.
- 2026-03-29 — Die offizielle Hugging-Face-Seite markiert HoliSpatial-2M-QA-Qwen3-VL-8B als aktualisierten 9B-Checkpoint.
- 2026-04-21 — Die offizielle Hugging-Face-Seite markiert HoliSpatial-3D-Grounding als aktualisiert.

## Anwendung {#how-to-use-this}

Ab dem 2026-03-10 sollten Praktiker die verlinkte Projektseite, das Repository und die Hugging-Face-Ressource als Ausgangspunkt für die Bewertung von Holi-Spatial nutzen und dabei Artefakt, Version und Nutzungsanleitung eigenständig überprüfen.

1. Eine CUDA-fähige Python-Umgebung anlegen und die Anforderungen mit den beiden PGSR-Submodulen installieren.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
2. Eine Szene in der erwarteten ScanNet-, ScanNet++- oder DL3DV-Struktur vorbereiten; für die QA ein Covisibility-Root hinzufügen.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
3. DA3 zunächst auf einer Szene über SCENE_DIR ausführen; depth_da3 und pointcloud_da3.ply prüfen.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
4. PGSR/3DGS trainieren, danach Mesh und mesh-gestützte Masken erzeugen.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
5. Einen OpenAI-kompatiblen vLLM-Endpunkt starten, Objekt- und Regionsannotation mit SAM3 ausführen, AABB nachbearbeiten, QA erzeugen und in LLaMA-Factory-dataset.jsonl konvertieren.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>

## Bewährte Vorgehensweisen {#best-practices}

- Mit einer Szene beginnen und Zwischenartefakte prüfen: Batch-Skripte betrachten eine Szene als abgeschlossen, sobald bereits eine finale JSON-Datei oder eine trainierte Punktwolke existiert.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
- CUDA, Depth Anything 3, SAM3-Assets und einen OpenAI-kompatiblen vLLM-Endpunkt explizit einrichten, statt sich auf implizite Abhängigkeiten zu verlassen.
  — <https://github.com/Visionary-Laboratory/Holi-Spatial>
- VLM-Verifikation für grenzwertige Instanzen beibehalten: Konfidenzfilterung erhöht die Präzision, kann aber gültige komplexe Objekte verwerfen.
  — <https://arxiv.org/abs/2603.07660>
- Ergebnisse nicht ungeprüft auf Video mit Bewegungsunschärfe, starker Verdeckung, wenigen Blickwinkeln oder dynamischen Objekten übertragen: Die Autoren nennen dies als Grenzen der Pipeline.
  — <https://arxiv.org/abs/2603.07660>

## Durch diesen Stand überholt {#superseded-by-this}

- 2026-03-10 — Der Status „Data (coming soon)“ und „Benchmark (coming soon)“ auf der Projektseite entspricht nicht mehr der Verfügbarkeit: Das Repository meldet einen veröffentlichten Datenteilsatz und Checkpoint, und die Hugging-Face-Organisation hostet nun vier Datensätze und ein Modell. Dies belegt jedoch nicht die Verfügbarkeit des vollständigen Holi-Spatial-4M.

## Weiterhin ungeklärt {#still-unknown}

- Die März- und April-Daten auf der Hugging-Face-Organisationsseite sind Datumsangaben der letzten Aktualisierung und keine bestätigten Erstveröffentlichungsdaten: Commit-Verlaufsseiten waren nicht verfügbar.
- Die Projektseite führt Daten und Benchmark weiterhin als „coming soon“, während README und Hugging Face verfügbare Artefakte zeigen. Ob sich dieser Hinweis auf das vollständige Holi-Spatial-4M bezieht oder schlicht veraltet ist, bleibt unklar.
- Dem Checkpoint fehlen eine Model Card und ein gehosteter Inference-Provider; das genaue Prompt-Template, die unterstützten Eingaben und die empfohlene Laufzeitumgebung sind nicht bestätigt.
- Weder das Repository noch die Modellseite nennen eine explizite Lizenz für Code, Datensätze oder Gewichte.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://visionary-laboratory.github.io/holi-spatial/ | Holi-Spatial | Holistic Spatial Intelligence | 2026-09-06 |
| https://github.com/Visionary-Laboratory/Holi-Spatial | GitHub - Visionary-Laboratory/Holi-Spatial: Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence | 2026-09-06 |
| https://arxiv.org/abs/2603.07660 | Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence | 2026-09-06 |
| https://huggingface.co/Holi-Spatial | Holi-Spatial (Visionary Laboratory) | 2026-09-06 |
| https://huggingface.co/Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B | Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B | 2026-09-06 |
| https://huggingface.co/Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B/tree/main | Holi-Spatial/HoliSpatial-2M-QA-Qwen3-VL-8B at main | 2026-09-06 |
| https://huggingface.co/datasets/Holi-Spatial/HoliSpatial-QA-2M | Holi-Spatial/HoliSpatial-QA-2M | 2026-09-06 |
| https://huggingface.co/datasets/Holi-Spatial/HoliSpatial-3D-Grounding | Holi-Spatial/HoliSpatial-3D-Grounding | 2026-09-06 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:holi-spatial`, Thread `holi-spatial-development`, 1 datiertes Ereignis 2026-03-10 → 2026-03-10.
- **Praktischer Hinweis:** Ab dem 2026-03-10 sollten Praktiker die verlinkte Projektseite, das Repository und die Hugging-Face-Ressource als Ausgangspunkt für die Bewertung von Holi-Spatial nutzen und dabei Artefakt, Version und Nutzungsanleitung eigenständig überprüfen.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich für die Frage, was veraltet ist.
