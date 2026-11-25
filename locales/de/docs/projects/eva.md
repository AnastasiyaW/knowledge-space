---
title: "EVA"
category: projects
date: 2026-03-26
tags: [eva, eva-public-resources, project]
aliases: ["EVA"]
level: 2
source_sha256: 4147ba2ea46c52ef80d86b8bad838b772f7c7c701d76bf4c7ea04f7c2a53563e
translation: machine
translated_at: '2026-10-24'
---
# EVA {#eva}

**Entwicklungslinie:** `project:eva` · Strang `eva-public-resources`  
**Letztes Ereignis:** 2026-03-26 · 1 datiertes seit 2026-03-26 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

EVA (Efficient Video Agent) ist ein auf Qwen2.5-VL aufgebauter Video-Agent für Forscher und Ingenieure.

- Agent-Zyklus: durchläuft eine Schleife aus Zusammenfassung → Planung → Aktion → Reflexion.
- Frame-Auswahl: wählt Videoframes aus, extrahiert sie und aktualisiert anhand des Ergebnisses den nächsten Schritt.
- Modellgewichte: gehostet unter `WRHC/EfficientVideoAgent` für die Evaluation auf sechs Videodatensätzen.

Das veröffentlichte Repository deckt Multi-GPU-Evaluation über vLLM ab, nicht eine interaktive Oberfläche. Der Aufbau eignet sich für reproduzierbare, abfragegesteuerte Videoevaluation, doch für den praktischen Betrieb ist eine eigene Inferenz-Pipeline erforderlich.

## Entwicklungslinie {#development-line}

- **2026-03-26 — EVA-Quellcode- und Modellressourcen wurden erfasst.** Am 2026-03-26 tauchte EVA mit einem GitHub-Quellrepository und einer Hugging-Face-Modellseite auf. Beide Links kennzeichnen das Projekt als öffentlich zugänglich. Allein die datierten Links bestätigen weder eine Version, Fähigkeiten oder Evaluationsergebnisse noch, ob eine der Ressourcen an diesem Tag erstmals veröffentlicht wurde.

## Was sich geändert hat {#what-changed}

2026-03-26 — Offizieller Evaluationscode und EVA-Gewichte sind öffentlich verfügbar. Das Modell ersetzt das passive gleichmäßige Frame-Sampling durch eine Agent-Schleife, die entscheidet, was und wann untersucht wird.

## So wird es verwendet {#how-to-use-this}

Stand 2026-03-26 sollten Anwender EVA als Projekt mit einer Quellcode-Referenz und einer Modell-Hosting-Referenz betrachten und Setup sowie Modelldetails vor der Verwendung direkt anhand dieser Ressourcen überprüfen.

1. Gewichte für `WRHC/EfficientVideoAgent` herunterladen und die Abhängigkeiten des Repositories zusammen mit FFmpeg installieren.
  — <https://github.com/wangruohui/EfficientVideoAgent>
2. Einen der sechs unterstützten Videodatensätze für die Evaluation vorbereiten und den lokalen `video_root` in `DATASET_CONFIG` setzen.
  — <https://github.com/wangruohui/EfficientVideoAgent>
3. Die Gewichte über einen OpenAI-kompatiblen vLLM-Endpunkt bereitstellen und anschließend URL, Tokenizer-Pfad und erlaubte Medienpfade in `eval-eva.py` setzen.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
4. Den gewählten Datensatz mit `eval-eva.py` ausführen. Denselben Befehl erneut starten, um einen unterbrochenen Lauf anhand der Cache-Datei fortzusetzen.
  — <https://github.com/wangruohui/EfficientVideoAgent>

## Bewährte Vorgehensweisen {#best-practices}

- `ffprobe` im `PATH` und die FFmpeg-Bibliotheken in `LD_LIBRARY_PATH` bereithalten, da die Frame-Extraktion während der Evaluation läuft.
  — <https://github.com/wangruohui/EfficientVideoAgent>
- Dem vLLM-Server mit `--allowed-local-media-path` Zugriff auf lokale Videodateien gewähren, damit der Agent extrahierte Frames an das Modell übergeben kann.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
- `--max-visual-tokens` über alle Läufe hinweg fixieren, da das Überschreiten des Token-Budgets die Auflösung senkt und Frames verwirft.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
- Einen einzelnen Lauf nicht als exakte Reproduktion betrachten, da die Genauigkeit selbst bei `temperature=0` um Bruchteile eines Prozentpunkts schwankt.
  — <https://github.com/wangruohui/EfficientVideoAgent>

## Abgelöst durch {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Nach der ersten Veröffentlichung existiert kein datiertes, vom Projekt selbst geführtes Changelog. Wir können nicht bestätigen, ob spätere Commits oder Modellaktualisierungen die Fähigkeiten von EVA verändert haben.
- Die öffentliche Dokumentation beschreibt ausschließlich den Evaluations-Workflow für Benchmarks. Wir finden keinen bestätigten Produktions-Inferenzaufbau, keine eigenständige API und keine Benutzeroberfläche.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/wangruohui/EfficientVideoAgent | EVA: Efficient Reinforcement Learning for End-to-End Video Agent — official evaluation code | 2026-09-05 |
| https://huggingface.co/WRHC/EfficientVideoAgent | WRHC/EfficientVideoAgent — model card and weights | 2026-09-05 |
| https://arxiv.org/abs/2603.22918 | EVA: Efficient Reinforcement Learning for End-to-End Video Agent | 2026-09-05 |
| https://huggingface.co/papers/2603.22918 | Paper page — EVA: Efficient Reinforcement Learning for End-to-End Video Agent | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:eva`, Strang `eva-public-resources`, 1 datiertes Ereignis 2026-03-26 → 2026-03-26.
- **Praktischer Hinweis:** Stand 2026-03-26 sollten Anwender EVA als Projekt mit einer Quellcode-Referenz und einer Modell-Hosting-Referenz betrachten und Setup sowie Modelldetails vor der Verwendung direkt anhand dieser Ressourcen überprüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, sind die datierten Ablösungen oben maßgeblich.
