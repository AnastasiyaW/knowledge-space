---
title: "V-RAE"
category: projects
date: 2026-08-24
tags: [project, v-rae, v-rae-development, v_rae]
aliases: ["V-RAE"]
level: 2
source_sha256: e3e1d290506a725f34bd02117467adb62419500dd2a66b710c9bce7603808030
translation: machine
translated_at: '2026-10-24'
---
# V-RAE {#v-rae}

**Entwicklungslinie:** `project:v-rae` · Thread `v-rae-development`  
**Letztes Ereignis:** 2026-08-24 · 1 datiertes Ereignis seit 2026-08-24 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

V-RAE ist eine Forschungs-Codebasis und ein Checkpoint-Satz für Videorekonstruktion und Videogenerierung. Es kombiniert eingefrorene DINOv3-, SigLIP2-, V-JEPA2.1- oder EUPE-Encoder mit zeitlichem Pooling und einem Video-Decoder.

- Videorekonstruktion aus eingefrorenen Repräsentationen.
- Klassenkonditionierte Generierung über Video-Benchmarks hinweg.
- Vorhersage zukünftiger Frames ohne Aktualisierung der Encoder-Gewichte.

Die bisher berichteten besten Generierungsergebnisse sind 117,86 gFVD auf UCF101 und 19,16 auf Kinetics-600. Der Code ist forschungsorientiert und setzt Linux, NVIDIA CUDA, FFmpeg, Python 3.10+ sowie passende Encoder-Gewichte voraus.

## Entwicklungslinie {#development-line}

- **2026-08-24 — Projektressourcen zu V-RAE wurden verlinkt.** Am 2026-08-24 veröffentlichte das Projekt Eintragslinks zu seiner Website, dem GitHub-Repository und der Hugging-Face-Modellseite, ohne gesonderte Release-Details oder verifizierte Fähigkeiten.

## Was sich geändert hat {#what-changed}

- 2026-08-13 — Das V-RAE-Paper wurde auf arXiv eingereicht; es definiert den Representation-Autoencoder-Ansatz und das tFVD-Diagnosemaß für die zeitliche Kohärenz.
- 2026-08-14 — Die offizielle Implementierung begann mit einem initialen GitHub-Release.
- 2026-08-19 — Das Repository ergänzte Daten-Manifeste, visuelle Ergebnisse und eine Korrektur für nicht zueinander passende Konfigurationen.
- 2026-08-24 — Öffentliche Einstiegspunkte umfassten die Projektseite, die offizielle Implementierung und das Checkpoint-Repository; keine Quelle aus erster Hand belegt an diesem Datum ein eigenständiges Code- oder Modell-Release.
- 2026-08-26 — Das Repository aktualisierte die GIF-Visualisierungsergebnisse.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-08-24 sollten Sie die verlinkte V-RAE-Website, das GitHub-Repository und die Hugging-Face-Modellseite als Ausgangspunkte betrachten, um Projektdokumentation, Quellcode und Modellverfügbarkeit zu prüfen; genaue Versionen und Nutzungsvoraussetzungen müssen noch recherchiert werden.

1. Implementierung klonen, eine Python-3.10-Umgebung anlegen, FFmpeg und die gepinnten Paketabhängigkeiten installieren.
  — <https://github.com/V-RAE/V-RAE>
2. Das V-RAE-Checkpoint-Repository in `ckpts` herunterladen und anschließend die eingefrorenen Encoder-Gewichte herunterladen, die zur gewählten Variante passen.
  — <https://huggingface.co/Guomh0707/V-RAE-Models>
3. Eingabeclips unter `assets/sample1.mp4` bis `assets/sample3.mp4` ablegen, dann `python sampling.py dino`, `siglip`, `vjepa` oder `eupe` ausführen; Ergebnisse unter `outputs/<variant>/` vergleichen.
  — <https://github.com/V-RAE/V-RAE>

## Bewährte Vorgehensweisen {#best-practices}

- Jeden V-RAE-Checkpoint dem zugehörigen eingefrorenen Encoder-Gewicht zuordnen; die Checkpoints sind benutzerdefinierte PyTorch-Dateien für die offizielle Codebasis.
  — <https://huggingface.co/Guomh0707/V-RAE-Models>
- Linux mit einer NVIDIA-GPU, einem CUDA-kompatiblen Treiber, FFmpeg und Python 3.10 oder neuer verwenden; CUDA und TorchCodec vor der Inferenz prüfen.
  — <https://github.com/V-RAE/V-RAE>
- Die veröffentlichten Zahlen als aufgabenspezifische Forschungsergebnisse behandeln: rFVD misst die Rekonstruktion, gFVD die Generierung und tFVD die zeitliche Kohärenz; sie sind nicht als einheitlicher universeller Qualitätswert zu vergleichen.
  — <https://github.com/V-RAE/V-RAE>

## Hiermit ersetzt {#superseded-by-this}

- 2026-08-19 — Die ursprünglichen Repository-Konfigurationen wurden durch die dokumentierte Korrektur für nicht zueinander passende Konfigurationen ersetzt.

## Weiterhin unbekannt {#still-unknown}

- Für 2026-08-24 selbst existiert kein datierter Release-Nachweis aus erster Hand; das verlinkte Paper und das initiale Repository-Release liegen vor diesem Datum.
- Der Model Hub weist auf der abgerufenen Seite keine datierte Revision aus, sodass das ursprüngliche Veröffentlichungsdatum des Checkpoints nicht verifiziert ist.
- Es gibt keinen gehosteten Inferenz-Endpunkt und keine Hinweise zum Produktivbetrieb; die Modellkarte besagt, dass kein Inference Provider das Modell bereitstellt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/V-RAE/V-RAE | V-RAE/V-RAE offizielle Implementierung, README | 2026-09-05 |
| https://huggingface.co/Guomh0707/V-RAE-Models | Guomh0707/V-RAE-Models, Modellkarte | 2026-09-05 |
| https://arxiv.org/abs/2608.13556 | V-RAE: Rethinking Video Latent Spaces for Generation | 2026-09-05 |
| https://github.com/V-RAE/V-RAE/commits/main/ | V-RAE/V-RAE Commit-Verlauf | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:v-rae`, Thread `v-rae-development`, 1 datiertes Ereignis vom 2026-08-24 bis 2026-08-24.
- **Praktischer Hinweis:** Stand 2026-08-24 sollten Praktiker die verlinkte V-RAE-Website, das GitHub-Repository und die Hugging-Face-Modellseite als Ausgangspunkte für die Prüfung von Projektdokumentation, Quellcode und Modellverfügbarkeit betrachten; genaue Versionen und Nutzungsvoraussetzungen müssen noch recherchiert werden.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich für die Frage, was veraltet ist.
