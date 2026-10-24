---
title: "MuScriptor — Öffentliche Projektverfügbarkeit"
category: projects
date: 2026-07-22
tags: [muscriptor, project, public-project-availability]
aliases: ["MuScriptor"]
level: 2
source_sha256: a715a5750a5dacbc0975cd8e3f96145282a3874be5965b73c6e4fb9c08ff67a8
translation: machine
translated_at: '2026-10-24'
---
# MuScriptor — Öffentliche Projektverfügbarkeit {#muscriptor-public-project-availability}

**Entwicklungslinie:** `project:muscriptor` · Thread `public-project-availability`  
**Letztes Ereignis:** 2026-07-22 · 1 datiertes seit 2026-07-22 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

MuScriptor ist ein Open-Weight-Modell zur Musiktranskription von Mirelo und Kyutai. Es wandelt Aufnahmen mit mehreren Instrumenten in MIDI-Notenereignisse um.

- Checkpoints: Modelle mit kleiner (100M), mittlerer (300M) und großer (1.3B) Parameteranzahl.
- Laufzeitumgebung: Python-API, CLI und lokales HTTP-Serving.
- Eingabe: Mono-Audio mit 16 kHz in 5-Sekunden-Abschnitten.
- Ausgabe: Tonhöhe, Onset, Offset und Instrumentenlabels mit 36 Gruppen.

Die Gewichte stehen unter CC-BY-NC und sind zugangsbeschränkt; Vorhersagen enthalten keine Velocity.

## Entwicklungslinie {#development-line}

- **2026-07-22 — Öffentliche Projektressourcen zu MuScriptor waren verfügbar.** Am 2026-07-22 wurden öffentliche Links zur Projektseite, zum Repository, zur Modellseite, zur interaktiven Demo und zur Installation freigeschaltet. Diese Links bestätigen die Projektverfügbarkeit an diesem Datum. Sie legen weder eine bestimmte Release-Version, eine Modellfähigkeit noch eine technische Änderung fest.

## Was sich geändert hat {#what-changed}

- 2026-07-22 — Projektlinks machten das öffentliche MuScriptor-Ökosystem zugänglich. Das vorangegangene Release v0.2.2 vom 2026-07-21 ergänzte strikt instrumentenbeschränktes Decoding, direkte MIDI-HTTP-Ausgabe, FP16/MPS-Unterstützung für Apple Silicon, optimierte Decoding-Kernels und Anleitungen für GPU-Nutzung unter Windows.
- 2026-07-21 — GitHub v0.2.2 erweiterte das lauffähige Paket um Demo- und Service-Workflows.
- 2026-07-10 — Release v0.2.1 ermöglichte Serving ohne Build-Schritt. Kyutai veröffentlichte die Projektankündigung.
- 2026-07-09 — Das Paper stellte das Open-Weight-Modell für mehrere Instrumente vor. Das Training kombinierte Synthetic Pre-Training, Fine-Tuning mit realen Audiodaten und RL-Post-Training.
- 2026-06-30 — Öffentliche Checkpoint-Sammlung angelegt. Dies markiert Repository-Metadaten, nicht ein Trainingsdatum.

## Wie man das nutzt {#how-to-use-this}

Wir können MuScriptor seit 2026-07-22 über die öffentlichen Einstiegspunkte für Code, Modell, Demo und Installation evaluieren. Bestätigen Sie genaue Fähigkeiten und Versionen vor einer Einführung anhand der Primärquellen.

1. Installation aus dem Git-Repository; die PyPI-Installation ist weiterhin als ausstehend gelistet.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
2. Wählen Sie small, medium oder large. Führen Sie `muscriptor transcribe --model large audio.wav -o out.mid` aus oder rufen Sie in Python `TranscriptionModel.load_model()` und `transcribe_to_midi()` auf.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
3. Laden Sie Audio für einen interaktiven Test in den gehosteten Transkriptions-Space hoch. Für lokale Integration verwenden Sie die CLI oder die Server-Implementierung des Repositorys.
  — <https://huggingface.co/spaces/hugging-apps/muscriptor-music-transcription>

## Best Practices {#best-practices}

- Verwenden Sie Instrumenten-Conditioning, wenn die Instrumentengruppen der Spuren bekannt sind. Die Modellkarte merkt an, dass Conditioning die Ergebnisse verbessert und die Zuordnungen über Abschnitte hinweg konsistent hält.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
- Behandeln Sie die Ausgabe als bearbeitbaren MIDI-Entwurf und nicht als fertige Partitur, besonders bei dichtem, ungewöhnlichem oder stark bearbeitetem Audio.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
- Verwenden Sie nur Aufnahmen mit bestätigten Rechten. Die Modellkarte untersagt unautorisierte Transkription ausdrücklich.
  — <https://huggingface.co/MuScriptor/muscriptor-large>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-07-21 — v0.2.2 ersetzt v0.2.1 für Nutzer, die direkte MIDI-HTTP-Antworten, strikte Instrumentenbeschränkungen oder native FP16-Inferenz auf Apple Silicon benötigen.
- 2026-07-10 — v0.2.1 ersetzte v0.2.0 für Serving ohne Build-Schritt.

## Weiterhin unbekannt {#still-unknown}

- Das Ereignis vom 2026-07-22 nennt nicht, welche verlinkte Oberfläche an diesem Tag geändert wurde. GitHub datiert v0.2.2 auf 2026-07-21; deshalb wird dieses Update als nächstliegende Ergänzung aus erster Hand berichtet und nicht als Release vom 2026-07-22.
- Das Schema stellt keine separaten Felder für `event_findings` oder `new_events` bereit; datierte Befunde bleiben daher unter `what_changed`.
- Die gehostete Demo war erreichbar, der gerenderte Seitentext enthielt jedoch keine Betriebsdokumentation.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/MuScriptor/muscriptor-large | MuScriptor — Modellkarte large (≈1.3B) | 2026-09-05 |
| https://github.com/muscriptor/muscriptor/releases | MuScriptor GitHub-Releases | 2026-09-05 |
| https://arxiv.org/abs/2607.08168 | MuScriptor: Ein offenes Modell für die Multi-Instrument-Musiktranskription | 2026-09-05 |
| https://kyutai.org/blog/2026-07-10-muscriptor/ | MuScriptor: Automatische Multi-Instrument-Transkription | 2026-09-05 |
| https://huggingface.co/spaces/hugging-apps/muscriptor-music-transcription | MuScriptor Music Transcription Space | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:muscriptor`, Thread `public-project-availability`, 1 datiertes Ereignis vom 2026-07-22 bis 2026-07-22.
- **Praktischer Hinweis:** Ab 2026-07-22 konnten Praktiker MuScriptor über die öffentlichen Einstiegspunkte für Code, Modell, Demo und Installation evaluieren; vor einer Einführung sollten genaue Fähigkeiten und Versionen anhand der verlinkten Primärquellen bestätigt werden.
- **Konfidenz:** hoch. Die datierten Ablösungshinweise oben sind maßgeblich dafür, was veraltet ist.
