---
title: "Stream.FM"
category: projects
date: 2026-05-14
tags: [project, stream-fm, stream-fm-development, stream_fm]
aliases: ["Stream.FM"]
level: 3
source_sha256: 00b978984b5aa8aaa9acac66ab98cff536406c97bcabd0eaf2434dd0beb0316e
translation: machine
translated_at: '2026-10-24'
---
# Stream.FM {#streamfm}

**Entwicklungslinie:** `project:stream-fm` · Thread `stream-fm-development`  
**Letztes Ereignis:** 2026-05-14 · 1 datiertes seit 2026-05-14 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Stream.FM ist eine PyTorch-Forschungscodebasis unter AGPL-3.0 für Audio-ML-Ingenieure, die frame-weise Sprachrestaurierung entwickeln.

- Sprachverbesserung und Enthallung
- Nachfilterung von Codecs, Bandbreitenerweiterung und STFT-Phasenrekonstruktion
- Mel-Vocoding über die mitgelieferte, verwandte MelFlow-Implementierung

## Entwicklungslinie {#development-line}

- **2026-05-14 — Projektressourcen zu Stream.FM wurden verlinkt.** Am 2026-05-14 wurde Stream.FM über eine Beispiel-Website, ein GitHub-Quellcode-Repository und einen Google-Drive-Ordner verlinkt. Zusammen etablieren diese Verweise ein öffentliches Projekt-Ressourcenpaket für die Linie, auch wenn sie weder ein versioniertes Release noch den Inhalt der ergänzenden Materialien belegen.

## Was sich geändert hat {#what-changed}

- 2025-09-18 — MelFlow, die verwandte Arbeit zu Streaming-Mel-Vocodern, die später mit Stream.FM gebündelt wurde, erschien als arXiv-Preprint.
- 2025-12-22 — Stream.FM erschien als arXiv-Preprint.
- 2026-04-21 — arXiv v3 wurde zur neuesten gelisteten Revision des Stream.FM-Papers.
- 2026-05-05 — die Autoren demonstrierten gemeinsame Echtzeit-Sprachverbesserung und Bandbreitenerweiterung auf der ICASSP.
- 2026-05-11 — der initiale öffentliche Stream.FM- und MelFlow-Quellcode wurde committet.
- 2026-05-13 — AGPL-3.0 wurde dem Quellcode-Repository hinzugefügt.
- 2026-05-14 — die Projektseite, das Repository und die Checkpoint-Ordner-Links wurden gemeinsam erfasst; für dieses Datum ist kein separater Upstream-Commit und kein GitHub-Release belegt.
- 2026-05-23 — Pflege der Repository-Zitation hat nur die Dokumentation geändert.
- 2026-06-05 — der zuletzt angezeigte Upstream-Push hat ausschließlich die TASL-Zitation für Stream.FM aktualisiert.

## Verwendung {#how-to-use-this}

Prüfe die Beispiel-Website, das Repository und die Drive-Materialien gemeinsam, wenn du Stream.FM zum Stand 2026-05-14 bewertest. Ein konkretes Setup, Ergebnis oder eine Release-Version ist noch nicht verifiziert.

1. Lege eine Python-3.10+-Umgebung an und installiere die dokumentierten Anforderungen mit einem PyTorch-CUDA-Wheel-Index, der zur lokalen CUDA-Laufzeit passt.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
2. Lade einen Checkpoint aus dem dokumentierten Google-Drive-Ordner mit dem gepflegten gdown-Befehl in ein lokales Checkpoint-Verzeichnis herunter.
  — <https://drive.google.com/drive/folders/1u2QKjGAdxblQVV8-qmifSM9AwhT86LER>
3. Wähle die Task-Konfiguration, die zur Checkpoint-Architektur passt, und führe anschließend inference.py mit einem Eingabe-WAV-Verzeichnis, einem Ausgabeverzeichnis, dem Solver und dem Checkpoint-Pfad aus.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
4. Für die Live-Integration frame-weise implementierst du die Zustandsinitialisierung und die forward_step-Aufrufe um das CausalNCSNpp-Backbone herum, statt einen fertigen Streaming-Server zu erwarten.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>

## Best Practices {#best-practices}

- Beginne mit dem von den Autoren empfohlenen 5xeuler-Solver und erhöhe die GPU-Parallelität nur dann, wenn die Zielmaschine über entsprechende GPUs verfügt.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
- Halte die Hydra-Konfiguration und die Checkpoint-Architektur aufeinander abgestimmt; der dokumentierte Inferenzpfad setzt diese Paarung voraus.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
- Evaluiere für Streaming CUDA-Graphen und den Standard-torch.compile-Wrapper auf der Zielhardware, statt anzunehmen, dass die Latenz aus dem Paper unverändert übertragbar ist.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
- Messe die End-to-End-Latenz auf der Zielhardware; das veröffentlichte Ergebnis von 48 ms ist ein gemessenes Forschungssetup und keine hardwareunabhängige Garantie.
  — <https://arxiv.org/abs/2512.19442>
- Lade nur vertrauenswürdige Checkpoints: Die Inferenz verwendet torch.load mit weights_only=False.
  — <https://raw.githubusercontent.com/sp-uhh/streamfm/main/inference.py>
- Prüfe die Pflichten aus der AGPL-3.0, bevor du Repository-Code in ein Produkt oder einen Netzwerkdienst integrierst.
  — <https://github.com/sp-uhh/streamfm/blob/main/LICENSE>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-05-14 — Korrigiert: Dies ist das Datum, an dem die Links erfasst wurden, nicht ein separat belegtes Upstream-Release von Stream.FM; der öffentliche Quellcode begann am 2026-05-11, und GitHub listet keine Releases.
- 2026-05-23 — Repository-Pflege, die nur die Zitation betrifft, ist kein Beleg für ein neues Modell, einen Checkpoint oder ein Laufzeit-Release.
- 2026-06-05 — Das Update der TASL-Zitation betrifft nur die Dokumentation; in den geprüften Quellen wurde kein späteres offizielles Modell-, Datensatz- oder Paket-Release gefunden.

## Weiterhin unbekannt {#still-unknown}

- Der verlinkte Drive-Ordner konnte hier nicht aufgelistet werden; sein Checkpoint-Inventar vom 2026-05-14, Hashes, Verfügbarkeit und Inhalte sind daher nicht verifiziert.
- Die AGPL-3.0 ist für den Repository-Quellcode verifiziert; eine separate Checkpoint-Lizenz oder Model Card für die über Drive bereitgestellten Gewichte wurde nicht verifiziert.
- Die Latenzergebnisse des Papers belegen keine Latenz auf dem Zielgerät, für Audio-I/O oder im Produktivbetrieb.
- Es wurde kein GitHub-Release, kein Paketartefakt und kein Checkpoint-Versionsmanifest gefunden; Anwender müssen den exakten Quellcode-Commit und die Checkpoint-Identität, die sie verwenden, dokumentieren.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://sp-uhh.github.io/streamfm_examples/ | Stream.FM | Real-Time Streamable Generative Speech Restoration with Flow Matching | 2026-09-05 |
| https://github.com/sp-uhh/streamfm | sp-uhh/streamfm | 2026-09-05 |
| https://drive.google.com/drive/folders/1u2QKjGAdxblQVV8-qmifSM9AwhT86LER | Stream.FM-Checkpoint-Ordner | 2026-09-05 |
| https://arxiv.org/abs/2512.19442 | Real-Time Streamable Generative Speech Restoration with Flow Matching — arXiv:2512.19442 | 2026-09-05 |
| https://arxiv.org/abs/2509.15085 | Real-Time Streaming Mel Vocoding with Generative Flow Matching — arXiv:2509.15085 | 2026-09-05 |
| https://cmsworkshops.com/ICASSP2026/view_demosession.php?mid=55 | ICASSP 2026 Show-and-Tell-Demo-Auflistung | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/17ec317c3974e1a4b0b4e3ebfe2a3a99fbbd616c | Initiales öffentliches Stream.FM- & MelFlow-Code — 17ec317 | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/c4b9c2b | sp-uhh/streamfm-Commit c4b9c2b | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/1a8226884432a17c7b71945a4b7d3c015dfe6cc8 | sp-uhh/streamfm-Commit 1a822688 | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/ab2700c1154acc5c2ce67a5344182028336413f5 | sp-uhh/streamfm-Commit ab2700c | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/blob/main/README.md | README.md — sp-uhh/streamfm | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/blob/main/LICENSE | LICENSE — sp-uhh/streamfm | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/releases | Releases — sp-uhh/streamfm | 2026-09-05 |
| https://raw.githubusercontent.com/sp-uhh/streamfm/main/inference.py | inference.py — sp-uhh/streamfm | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:stream-fm`, Thread `stream-fm-development`, 1 datiertes Ereignis 2026-05-14 → 2026-05-14.
- **Praxishinweis:** Stand 2026-05-14 sollten Praktiker, die Stream.FM bewerten, die Beispiel-Website, das Quellcode-Repository und die ergänzenden Drive-Materialien gemeinsam heranziehen; ein konkretes Setup, Ergebnis oder eine Release-Version ist bisher nicht verifiziert.
- **Konfidenz:** mittel. Die datierten Einträge unter „Hierdurch ersetzt“ sind maßgeblich dafür, was veraltet ist.
