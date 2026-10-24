---
title: "ZoeDepth"
category: projects
date: 2023-03-01
tags: [project, zoedepth, zoedepth-public-release]
aliases: ["ZoeDepth"]
level: 2
source_sha256: 3c9bfc5f8d8603bcc4ffdc447c9315dfa6f83bee40dea409655305e6c77920ef
translation: machine
translated_at: '2026-10-24'
---
# ZoeDepth {#zoedepth}

**Entwicklungslinie:** `project:zoedepth` · Thread `zoedepth-public-release`  
**Letztes Ereignis:** 2023-03-01 · 1 datiertes Ereignis seit 2023-03-01 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

ZoeDepth ist ein PyTorch-Modell zur monokularen Tiefenschätzung, das einen einzelnen RGB-Frame in eine absolute Tiefenkarte umwandelt. ZoeD-M12-N, ZoeD-M12-K und ZoeD-M12-NK decken die Modi für Innenräume, Außenbereiche und gemischte NYU+KITTI-Szenarien ab. Die Architektur kombiniert ein Pretraining auf relativer Tiefe über 12 Datensätze mit Metric-Fine-Tuning, und die NK-Version leitet Domänen automatisch an ihren metrischen Head weiter. Die metrische Skala bleibt eine Schätzung für eine einzelne Kamera, und Intel pflegt das Quell-Repository nicht mehr. Für reproduzierbare Legacy-Pipelines sollte man den Transformers-Checkpoint verwenden, statt auf Korrekturen im Repository zu warten.

## Entwicklungslinie {#development-line}

- **2023-03-01 — Öffentliche Projektressourcen für ZoeDepth wurden verfügbar.** Am 2023-03-01 war ZoeDepth über sein GitHub-Repository, ein Google-Colab-Notebook und zwei Hugging-Face-Spaces verlinkt. Die datierten Links zeigen einen öffentlichen Zugangsschritt, der Quellcode, ein lauffähiges Notebook und gehostete Demos umfasst. Sie belegen weder eine bestimmte Modellversion, ein Benchmark-Ergebnis noch einen Release-Wortlaut.

## Was sich geändert hat {#what-changed}

- 2023-03-01 — ZoeDepth war über das offizielle Repository, Colab und Demos verfügbar; veröffentlichte Gewichte umfassten ZoeD-M12-N, ZoeD-M12-K und das zweiköpfige ZoeD-M12-NK.
- 2023-07-09 — Es erschien keine neue bestätigte Version und kein neues Modell: Der Link verweist auf einen früheren Beitrag über ZoeDepth.
- 2024-07-08 — Hugging Face Transformers hat ZoeDepth aufgenommen und bietet damit einen Standardpfad zum Laden und zur Inferenz über die Depth-Estimation-Pipeline.
- Aktueller Status — Intel hat das ursprüngliche Repository als nicht mehr unterstützt erklärt; der Checkpoint Intel/zoedepth-nyu-kitti bleibt in Transformers verfügbar.

## So nutzt man es {#how-to-use-this}

Ab dem 2023-03-01 konnten Praktiker ZoeDepth über sein Repository, das Colab-Notebook oder die gehosteten Hugging-Face-Demos evaluieren, bevor sie es in ihren eigenen Workflow integrierten.

1. Kompatible PyTorch- und Transformers-Pakete installieren und dann Intel/zoedepth-nyu-kitti über pipeline("depth-estimation") für ein einzelnes Bild laden.
  — <https://huggingface.co/Intel/zoedepth-nyu-kitti>
2. Für den ursprünglichen ZoeDepth-Stack ZoeD_N, ZoeD_K oder ZoeD_NK über torch.hub laden; N für NYU-Innenräume, K für KITTI-Außenbereiche und NK für gemischte Szenarien wählen.
  — <https://github.com/isl-org/ZoeDepth>
3. Ein RGB-Bild übergeben und die numerische Tiefenkarte speichern; farbige Visualisierungen nicht als rohe metrische Daten verwenden.
  — <https://github.com/isl-org/ZoeDepth>

## Best Practices {#best-practices}

- Den veröffentlichten Transformers-Checkpoint verwenden und Abhängigkeitsversionen für neue Inferenz-Pipelines festschreiben: Das offizielle Quell-Repository erhält keine weiteren Updates.
  — <https://github.com/isl-org/ZoeDepth>
- Das Modell an die Datendomäne anpassen: N ist für NYU trainiert, K für KITTI, und NK verwendet zwei metrische Heads für Innen- und Außenszenen.
  — <https://arxiv.org/abs/2302.12288>
- Modellladen testen und eine Testinferenz ausführen, bevor Batch-Verarbeitung startet; das Repository stellt dafür sanity_hub.py und sanity.py bereit.
  — <https://github.com/isl-org/ZoeDepth>

## Hierdurch ersetzt {#superseded-by-this}

- 2023-02-27: Die ursprünglichen torch.hub-Anleitungen sind nach der Transformers-Integration vom 2024-07-08 nicht mehr der einzige Startpfad.
- Aktuelle Empfehlung, das Quell-Repository nicht als aktiv gepflegt zu betrachten: Intel hat ausdrücklich das Ende der Entwicklung, der Fehlerbehebungen und neuer Releases angekündigt.

## Noch unbekannt {#still-unknown}

- Für 2023-07-09 ist kein eigenständiges Produkt-Release bestätigt: Der verfügbare Link verweist auf einen früheren Beitrag und nicht auf ein neues ZoeDepth-Release.
- Die metrische Tiefengenauigkeit auf eigenen Kameras und in Domänen außerhalb von NYU und KITTI erfordert eine lokale Validierung mit Ground-Truth-Daten.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/isl-org/ZoeDepth | isl-org/ZoeDepth — offizielle Implementierung und Wartungshinweis | 2026-09-05 |
| https://github.com/isl-org/ZoeDepth/releases | ZoeDepth-Releases — initiale v1.0 | 2026-09-05 |
| https://arxiv.org/abs/2302.12288 | ZoeDepth: Zero-shot Transfer by Combining Relative and Metric Depth | 2026-09-05 |
| https://huggingface.co/docs/transformers/v4.48.0/model_doc/zoedepth | Hugging Face Transformers — ZoeDepth-Dokumentation | 2026-09-05 |
| https://huggingface.co/Intel/zoedepth-nyu-kitti | Intel/zoedepth-nyu-kitti Model Card | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:zoedepth`, Thread `zoedepth-public-release`, 1 datiertes Ereignis 2023-03-01 → 2023-03-01.
- **Praktischer Hinweis:** Ab dem 2023-03-01 konnten Praktiker ZoeDepth über sein Repository, das Colab-Notebook oder die gehosteten Hugging-Face-Demos evaluieren, bevor sie es in ihren eigenen Workflow integrierten.
- **Konfidenz:** hoch. Die datierten Supersedes-Einträge sind maßgeblich für das, was veraltet ist.
