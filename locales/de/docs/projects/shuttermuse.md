---
title: "ShutterMuse"
category: projects
date: 2026-07-03
tags: [project, shuttermuse]
aliases: ["ShutterMuse"]
level: 2
source_sha256: 631f96242f53e44accefc3b894fa6e007301503e9f871f13eff7a7060e6838f8
translation: machine
translated_at: '2026-10-24'
---
# ShutterMuse {#shuttermuse}

**Entwicklungsstrang:** `project:shuttermuse` · Thread `shuttermuse`  
**Letztes Ereignis:** 2026-07-03 · 1 datiertes seit 2026-07-03 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ShutterMuse ist ein Assistent für die Fotografie zum Zeitpunkt der Aufnahme, gedacht für Fotografen und Porträtierte.

- Bildausschnitt-Bewertung: bewertet den Bildausschnitt.
- Verfeinerung der Kompositionsboxen: verfeinert Kompositionsboxen.
- COCO-17-Posenführung: führt bei Porträtposen.

Der veröffentlichte Checkpoint hat 9B Parameter in BF16, und für das Projekt ist keine Quellcode-Lizenz angegeben. Er eignet sich für lokale Forschung und Evaluation, nicht für einen produktionsreifen gehosteten Dienst.

## Entwicklungsstrang {#development-line}

- **2026-07-03 — Öffentliche Projektlinks zu ShutterMuse wurden geteilt.** Am 2026-07-03 teilte ShutterMuse Links zu einer Projektwebsite, einem GitHub-Repository und einer Hugging-Face-Seite. Diese Links begründen eine öffentliche Präsenz über Website, Quellcode-Repository und Modellplattform. Sie belegen keine bestimmte Veröffentlichung, Version, Fähigkeit oder technisches Ergebnis.

## Was sich geändert hat {#what-changed}

- 2026-06-24 — ShutterMuse stellte CaptureGuide-Bench vor, einen Entwicklungsdatensatz mit 130K Beispielen, sowie ein einheitliches MLLM, das mit überwachtem und bestärkendem Feintuning trainiert wurde.
- 2026-07-03 — Die ShutterMuse-Dokumentation verlinkte die Projektseite, den Code und das Modell. Die README datiert die Veröffentlichung von Code, Benchmark und Gewichten nur auf 2026-06; eine eigenständige Juli-Version ist daher nicht belegt.

## Anwendung {#how-to-use-this}

Stand 2026-07-03 ist ShutterMuse als Projekt mit öffentlichen Verweisen auf Website, Quellcode und Modell zu behandeln. Genaue Fähigkeiten und Versionen sind vor dem Einsatz anhand dieser Quellen zu prüfen.

1. Klonen Sie das Repository, erstellen Sie seine Python-3.10-Conda-Umgebung und installieren Sie die deklarierten Abhängigkeiten.
  — <https://github.com/lijayuTnT/ShutterMuse>
2. Stellen Sie den Basis- oder zusammengeführten Qwen-VL-Checkpoint sowie den ShutterMuse-LoRA-/Checkpoint bereit. Lassen Sie den LoRA-Pfad nur bei einem vollständig zusammengeführten Checkpoint leer.
  — <https://github.com/lijayuTnT/ShutterMuse>
3. Führen Sie quick_start.sh mit --side photographer für Bildausschnitt-Hinweise oder mit --side subject für Posenhinweise aus. Prüfen Sie die JSON-Vorhersage und die WebP-Visualisierung.
  — <https://github.com/lijayuTnT/ShutterMuse>
4. Für die Evaluation laden Sie CaptureGuide-Bench in Benchmark/ herunter und führen jeweils ein offizielles Evaluationsziel aus.
  — <https://huggingface.co/datasets/ShutterMuse/CaptureGuide-Bench>

## Bewährte Vorgehensweisen {#best-practices}

- Wählen Sie bewusst den Workflow für Fotograf oder Porträtierten: Sie liefern unterschiedliche Hinweise und erfordern unterschiedliche Eingaben.
  — <https://github.com/lijayuTnT/ShutterMuse>
- Behandeln Sie die Trainingsskripte als Startvorlagen. Legen Sie vor dem Ausführen lokale Pfade für Modell, Datensatz, GPU und Ausgabe explizit fest.
  — <https://github.com/lijayuTnT/ShutterMuse>
- Fixieren Sie für Experimente die Revisionen von Repository und Gewichten. Das Repository hat derzeit Commits, aber kein versioniertes Release.
  — <https://github.com/lijayuTnT/ShutterMuse>
- Klären Sie die Nutzungsrechte vor einem kommerziellen Einsatz oder einer Weitergabe. Der Benchmark ist nur für Forschungszwecke freigegeben, und der Lizenzabschnitt des Repositorys ist noch nicht fertiggestellt.
  — <https://huggingface.co/datasets/ShutterMuse/CaptureGuide-Bench>

## Hiermit abgelöst {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Kein genaues Changelog und kein getaggtes Release nennt eine Modell-, Repository- oder Benchmark-Revision, die speziell am 2026-07-03 veröffentlicht wurde. Die README der Projektautoren datiert die Veröffentlichung der Assets nur auf 2026-06.
- Der Lizenzabschnitt des Repositorys besagt, dass er noch ergänzt wird. Kommerzielle Nutzungs- und Weitergaberechte für Code und Gewichte sind hier nicht geklärt.
- Zum beobachteten Zeitpunkt ist kein gehosteter Inferenzanbieter für das Modell aufgeführt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://lijayutnt.github.io/ShutterMuse/ | ShutterMuse: Capture-Time Photography Guidance with MLLMs | 2026-09-05 |
| https://github.com/lijayuTnT/ShutterMuse | GitHub - lijayuTnT/ShutterMuse | 2026-09-05 |
| https://huggingface.co/ShutterMuse/ShutterMuse | ShutterMuse/ShutterMuse · Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2606.25763 | ShutterMuse: Capture-Time Photography Guidance with MLLMs | 2026-09-05 |
| https://huggingface.co/datasets/ShutterMuse/CaptureGuide-Bench | ShutterMuse/CaptureGuide-Bench | 2026-09-05 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:shuttermuse`, Thread `shuttermuse`, 1 datiertes Ereignis 2026-07-03 → 2026-07-03.
- **Praxishinweis:** Stand 2026-07-03 können Praktiker ShutterMuse als Projekt mit öffentlichen Verweisen auf Website, Quellcode und Modellverteilung behandeln; genaue Fähigkeiten und Versionen sind vor dem Einsatz anhand dieser Quellen zu prüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Angaben unter „Hiermit abgelöst“.
