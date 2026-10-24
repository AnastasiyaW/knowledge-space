---
title: "HOMIE"
category: projects
date: 2026-07-22
tags: [homie, homie-public-project-release, project]
aliases: ["HOMIE"]
level: 2
source_sha256: 8d4da0547c83aa66ac0d43c325dd3db9d948953f977f8f70b3e814de0079cdb1
translation: machine
translated_at: '2026-10-24'
---
# HOMIE {#homie}

**Entwicklungslinie:** `project:homie` · Thread `homie-public-project-release`  
**Letztes Ereignis:** 2026-07-22 · 1 datiert seit 2026-07-22 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Worum es sich handelt {#what-it-is}

HOMIE ist eine Open-Source-Pipeline zur lokalen Videogenerierung, die durch Referenzbilder von Personen, Produkten, Logos, OCR-Karten und Mehransichtsaufnahmen gesteuert wird.

- Komposition mehrerer Subjekte: kombiniert mehrere unterschiedliche Subjekte in einem Videoclip.
- Ausrichtung mehrerer Referenzen: nutzt mehrere Referenzen eines Subjekts für Textgenauigkeit oder Konsistenz der Blickwinkel.

Der Betrieb erfordert Wan2.1-T2V-14B, separate HOMIE-Gewichte mit 37,1 GB und Qwen3-VL-2B-Thinking.

Dies ist eine Forschungs-Inferenzveröffentlichung, kein Cloud-Dienst.

## Entwicklungslinie {#development-line}

- **2026-07-22 — Öffentliche Projektressourcen zu HOMIE erschienen.** Am 2026-07-22 verknüpfte das Projekt seine Website, das GitHub-Repository und die Hugging-Face-Modellseite homie-r2v-wan2.1 miteinander. Diese Links bieten öffentliche Dokumentation, Quellcode und Modellverteilung an einer Stelle. Präzise Angaben zur Veröffentlichung, Versionsdetails, Fähigkeiten und Lizenz werden nicht genannt.

## Was sich geändert hat {#what-changed}

2026-07-20 — Der technische Bericht zu HOMIE erschien auf arXiv und etablierte eine einheitliche Methode zur inter- und intra-subjektbezogenen Video-Personalisierung.

2026-07-21 — Inferenzcode und Checkpoints, feinabgestimmt auf Wan2.1-T2V-14B, wurden veröffentlicht.

2026-07-22 — Die Projektseite, der Code und die Gewichte beschrieben einen einzigen lokalen Workflow; an diesem Tag wurde keine gesonderte Versionsänderung gefunden.

## Anwendung {#how-to-use-this}

Ab dem 2026-07-22 beginnen Sie mit der verlinkten Projektseite, dem Quell-Repository und der Hugging-Face-Modellseite. Prüfen Sie vor der Nutzung die Projektdokumentation, die Anforderungen und die Lizenz.

1. Installieren Sie die Umgebung mit `set_env.sh`. Dies erfordert PyTorch 2.4.0 oder neuer mit einem kompatiblen CUDA-Build.
  — <https://github.com/YIYANGCAI/HOMIE>
2. Laden Sie Wan-AI/Wan2.1-T2V-14B-Diffusers, die Gewichte `yychai/homie-r2v-wan2.1` und Qwen/Qwen3-VL-2B-Thinking in die vorgegebenen Verzeichnisse herunter.
  — <https://github.com/YIYANGCAI/HOMIE>
3. Erstellen Sie eine JSONL-Datei: Die äußeren Listen in `reference_paths` trennen die Subjekte, und `prompt` beschreibt das Video.
  — <https://github.com/YIYANGCAI/HOMIE>
4. Führen Sie `generate_mllm_feature.py` aus und übergeben Sie anschließend die erzeugte JSONL-Datei mit den Pfaden `mllm_feature` an `generate.py`.
  — <https://github.com/YIYANGCAI/HOMIE>

## Bewährte Vorgehensweisen {#best-practices}

- Überspringen Sie die Merkmalsextraktion mit Qwen3-VL-2B-Thinking nicht: Die Inferenz erwartet eine JSONL-Datei mit ergänzten Pfaden `mllm_feature`.
  — <https://github.com/YIYANGCAI/HOMIE>
- Beginnen Sie mit dem dokumentierten Einzel-GPU-Modus: 832×480, 97 Frames, 24 fps und ein festes `base_seed`. Wenden Sie FSDP und Context Parallel nur auf einem geeigneten Multi-GPU-Knoten an.
  — <https://github.com/YIYANGCAI/HOMIE>
- Verwenden Sie für Context Parallel das dokumentierte Beispiel mit 8×A100 und `ULYSSES_SIZE=8` sowie `RING_SIZE=1`. Dies ist eine Beispielkonfiguration, keine angegebene Hardware-Mindestanforderung.
  — <https://github.com/YIYANGCAI/HOMIE>

## Ersetzt durch diesen Eintrag {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Das Repository enthält keine versionierten Releases und kein Changelog: Der genaue Commit oder das Gewicht, das dem Eintrag vom 2026-07-22 entspricht, ist nicht belegt.
- Offizieller minimaler VRAM-Bedarf, Generierungszeit und getestete Konfigurationen über das 8×A100-Beispiel hinaus werden nicht veröffentlicht.
- Das aktuelle README enthält ein Szenario für Context Parallel, die Quelle datiert dessen Aufnahme jedoch nicht, daher ist es nicht als eigenes datiertes Ereignis aufgeführt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://yiyangcai.github.io/homie-page.github.io/ | HOMIE-Demoseite | 2026-09-05 |
| https://github.com/YIYANGCAI/HOMIE | YIYANGCAI/HOMIE — Code und Inferenzanleitung | 2026-09-05 |
| https://huggingface.co/yychai/homie-r2v-wan2.1 | yychai/homie-r2v-wan2.1 | 2026-09-05 |
| https://arxiv.org/abs/2607.18217 | HOMIE: Human-object Centric Video Personalization via Multimodal Intelligent Enhancement | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:homie`, Thread `homie-public-project-release`, 1 datiertes Ereignis 2026-07-22 → 2026-07-22.
- **Praktischer Hinweis:** Ab dem 2026-07-22 sollten Praktiker, die HOMIE evaluieren, mit der verlinkten Projektseite, dem Quell-Repository und der Hugging-Face-Modellseite beginnen und anschließend Projektdokumentation, Anforderungen und Lizenz vor der Nutzung prüfen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
