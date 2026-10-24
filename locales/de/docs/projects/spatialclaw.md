---
title: "SpatialClaw"
category: projects
date: 2026-07-01
tags: [nvidia, project, spatialclaw, spatialclaw-development]
aliases: ["SpatialClaw"]
level: 3
source_sha256: f0375e7190c7a73354ed8ea1720707107d70d78235b70374c47c23eb6855c450
translation: machine
translated_at: '2026-10-24'
---
# SpatialClaw {#spatialclaw}

**Entwicklungslinie:** `project:spatialclaw` · Thread `spatialclaw-development`  
**Letztes Ereignis:** 2026-07-01 · 1 datierter Eintrag seit 2026-07-01 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

SpatialClaw ist ein trainingsfreies Framework von NVIDIA und KAIST für Teams, die VLMs auf räumliche Aufgaben in 3D, Multi-View, Video und 4D prüfen. Der Agent schreibt Python-Zellen in einen persistenten Jupyter-Kernel, ruft SAM3, Depth Anything 3, Geometriefunktionen sowie NumPy/SciPy auf, untersucht Zwischenergebnisse und gibt anschließend die Antwort zurück. Messung: 59,9 % durchschnittliche Genauigkeit über 20 Benchmarks, 11,2 Prozentpunkte über SpaceTools-Toolshed im Vergleich auf Gemma 4-31B. Fazit: Es handelt sich um eine reproduzierbare Forschungs-Runtime und nicht um eine leichtgewichtige Bibliothek für eine gewöhnliche Vision-Anwendung.

## Entwicklungslinie {#development-line}

- **2026-07-01 — Verweise auf das SpatialClaw-Projekt geteilt.** Trainingsfreier Agent mit Code-as-Action-Schnittstelle, persistentem Python/Jupyter-Kernel, GPU-Wahrnehmungsserver und Läufen sowohl auf einer einzelnen GPU-Maschine als auch über SLURM.

## Was sich geändert hat {#what-changed}

2026-07-01 — Der offizielle Code und die Website von SpatialClaw wurden veröffentlicht: trainingsfreier Agent mit Code-as-Action-Schnittstelle, persistentem Python/Jupyter-Kernel, GPU-Wahrnehmungsserver und Läufen sowohl auf einer einzelnen GPU-Maschine als auch über SLURM.

Ergänzung zum Ereignis vom 2026-07-01: Das Repository präzisiert den Lieferumfang. Enthalten sind eine LangGraph-Runtime, eine AST-Prüfung der Zellen, Planning- und Reflection-Schleifen, 20 Benchmark-Loader, ein FastAPI-GPU-Tool-Server, vLLM-Discovery mit Load-Balancing sowie SLURM-Launch-Manager. Der offizielle Artikel vom 2026-06-11 nennt das ursprüngliche Ergebnis: 59,9 % auf 20 Benchmarks und +11,2 Prozentpunkte gegenüber einem kürzlich veröffentlichten Spatial Agent.

## So verwendet man es {#how-to-use-this}

Ab 2026-07-01 können Praktiker die Projektwebsite und das NVlabs-Repository als datierte primäre Ausgangspunkte für die Bewertung von SpatialClaw nutzen. Allein diese Belege rechtfertigen jedoch keine konkrete Änderung des Workflows.

1. Repository rekursiv klonen und das offizielle Setup-Skript ausführen; es legt die Umgebungen für Agent, CUDA und vLLM an.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md>
2. Linux mit NVIDIA-GPU, CUDA 12.x, Conda und Zugriff auf die gated Gewichte von SAM3.1 vorbereiten. Für die FP8-Varianten aus dem Artikel ist Hopper/H100 oder neuer erforderlich; für A100/L40S gibt die Dokumentation AWQ/GPTQ-Varianten an.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md>
3. .env kopieren und das Backend wählen: selbst gehostetes vLLM oder ein OpenAI-kompatibler Endpoint. model- und dataset-JSON festlegen und spatial_agent.entrypoints.run starten.
  — <https://github.com/NVlabs/SpatialClaw>
4. Für SLURM zuerst account, partition und Speicherlimits in den Launch-Konfigurationen an den eigenen Cluster anpassen und danach die VLM- und Wahrnehmungsgewichte vorab auf dem Login-Node herunterladen.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/running.md>

## Best Practices {#best-practices}

- Immer mit `--recursive` klonen oder die Submodule separat initialisieren: SAM3, Pi3, Depth-Anything-3 und map-anything sind auf konkrete Revisionen festgelegt.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md>
- Vor einem SLURM-Lauf alle Gewichte vorab herunterladen: Compute-Jobs laufen mit `HF_HUB_OFFLINE=1`, und ein fehlendes lokales Artefakt beendet die Aufgabe mit `LocalEntryNotFoundError`.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/running.md>
- Bei `llm_base_url=vllm` nicht den HF-Modellpfad als `llm_model` verwenden, sondern das `served_name` aus `models.json` angeben. Für einen externen OpenAI-kompatiblen Endpoint den dort erwarteten Modellbezeichner verwenden.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/configuration.md>

## Dadurch ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Die Dokumentation nennt kein eigenes versioniertes Release oder Tag für genau den 2026-07-01. Das Datum bezieht sich auf die Verfügbarkeit des Projekts und des Codes zum genannten Ereignis, nicht auf ein bestätigtes GitHub-Release.
- Die Lizenz des Repositorys ist die NVIDIA Source Code License-NC. Die Eignung für kommerzielle Nutzung muss anhand des vollständigen Lizenztexts gesondert geprüft werden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://spatialclaw.github.io/ | SpatialClaw: Rethinking Action Interface for Agentic Spatial Reasoning | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw | Repository NVlabs/SpatialClaw | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md | SpatialClaw Installation | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw/blob/main/docs/running.md | SpatialClaw Running Experiments | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw/blob/main/docs/configuration.md | SpatialClaw Configuration & Benchmarks | 2026-09-05 |
| https://arxiv.org/abs/2606.13673 | SpatialClaw: Rethinking Action Interface for Agentic Spatial Reasoning | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:spatialclaw`, Thread `spatialclaw-development`, 1 datiertes Ereignis 2026-07-01 → 2026-07-01.
- **Praktischer Hinweis:** Ab 2026-07-01 können Praktiker die Projektwebsite und das NVlabs-Repository als datierte primäre Ausgangspunkte für die Bewertung von SpatialClaw nutzen. Allein diese Belege rechtfertigen keine konkrete Änderung des Workflows.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
