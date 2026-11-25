---
title: "MagicQuill"
category: projects
date: 2024-11-18
tags: [magicquill, magicquill-development, magicquill_pinokio, project]
aliases: ["MagicQuill"]
level: 3
source_sha256: 83bffc3f42b96e1320c0be817b465e6ba4602b3177089269d5918bac76a7519f
translation: machine
translated_at: '2026-10-24'
---
# MagicQuill {#magicquill}

**Entwicklungslinie:** `project:magicquill` · Thread `magicquill-development`  
**Letztes Ereignis:** 2024-11-18 · 1 datiertes Ereignis seit 2024-11-18 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

MagicQuill ist ein Forschungs-Bildeditor für Künstlerinnen und Künstler, die lokale Kontrolle über das reine Inpainting per Prompt hinaus benötigen.

- V2 steuert Inhalt, Platzierung, Struktur und Farbe über visuelle Ebenen und ergänzt einen Pinsel für lokale Bearbeitung, Vordergrund-Requisiten und SAM-Segmentierung.
- V1 steuert Ergänzungen, Entfernungen und Farbpinselbearbeitungen; Draw&Guess schlägt anhand von Skizzen Prompts vor.

## Entwicklungslinie {#development-line}

- **2024-11-18 — Öffentliche Demo, Quellcode-Repository und gehosteter Space von MagicQuill wurden verlinkt.** Projektseite, Quellcode und Hugging-Face-Demo bildeten die öffentlichen Einstiegspunkte für Praktiker.

## Was sich geändert hat {#what-changed}

- 2024-11-14 — MagicQuill V1: Das arXiv-Preprint definierte den Editor mit drei Pinseln und den Draw&Guess-Prompt-Assistenten.
- 2024-11-18 — MagicQuill V1: Projektseite, Quellcode und Hugging-Face-Demo bildeten die öffentlichen Einstiegspunkte für Praktiker.
- 2024-11-21 — MagicQuill V1: Pfadbehandlung unter Windows, Speicherverhalten und die Setup-Hilfsskripte `.bat`/`.sh` wurden aktualisiert.
- 2024-11-25 — MagicQuill V1: Drag-and-Drop-Bildupload und eine Download-Schaltfläche wurden hinzugefügt.
- 2024-12-06 — MagicQuill V1: Auto-Save und Auflösungssteuerung wurden hinzugefügt.
- 2024-12-07 — MagicQuill V1: Ein ComfyUI-Custom-Node wurde veröffentlicht.
- 2024-12-16 — MagicQuill V1: Eine ModelScope-Bereitstellung wurde hinzugefügt.
- 2025-01-02 — MagicQuill V1: Ein Docker-Container-Pfad wurde hinzugefügt.
- 2025-02-24 — MagicQuill: Eine Pinokio-Launcher-Route wurde referenziert; ihr historischer Paketstand lässt sich über den vorliegenden Endpunkt nicht rekonstruieren.
- 2025-02-27 — MagicQuill V1: Das Paper wurde auf der CVPR 2025 angenommen.
- 2025-12-02 — MagicQuill V2: Das Paper zu den geschichteten visuellen Hinweisen (Layered Visual Cues) wurde auf arXiv eingereicht.
- 2025-12-03 — MagicQuill V2: Das veröffentlichte System ging von der reinen Pinsel-Interaktion aus V1 zu Inhalts-, Raum-, Struktur- und Farbebenen auf Basis von Flux Kontext über.

## Anwendung {#how-to-use-this}

Ab dem 2024-11-18 konnten Praktiker MagicQuill über die öffentliche Demo und den gehosteten Space evaluieren; das verlinkte Repository diente dazu, die Implementierung vor einer Übernahme zu prüfen.

1. Verwende den laufenden V2-Hugging-Face-Space, wenn keine lokale GPU mit etwa 40 GB VRAM verfügbar ist.
  — <https://huggingface.co/spaces/AI4Editing/MagicQuillV2>
2. Für lokales V2 verwende das aktive Repository `zliucz/MagicQuillV2`, lege eine Python-3.10-Umgebung an und installiere die Anforderungen.
  — <https://github.com/zliucz/MagicQuillV2>
3. Lade `LiuZichen/MagicQuillV2-models` in `models/` herunter und starte die UI anschließend mit `python app.py`.
  — <https://huggingface.co/LiuZichen/MagicQuillV2-models>
4. Isoliere in V2 ein Vordergrund-Requisit mit SAM, platziere es über den Visual Cue Manager und verwende dann die Steuerungen für lokale Bearbeitung, Kanten, Farbe oder Entfernung für die jeweils relevante Ebene.
  — <https://magicquill.art/v2/>
5. Für eine 8-GB-GPU verwende V1: Klone rekursiv, sodass das LLaVA-Submodul vorhanden ist, lade die Checkpoints und starte anschließend `python gradio_run.py`.
  — <https://github.com/magic-quill/magicquill>

## Bewährte Praktiken {#best-practices}

- Behandle Draw&Guess als Vorschlag und ersetze den Prompt, wenn eine Skizze mehrdeutig ist.
  — <https://arxiv.org/abs/2411.09703>
- Bei V1 die Edge Strength senken, wenn ein grober Kritzel dem Prompt widerspricht; die Deckkraft bzw. Stärke der Farbe reduzieren, wenn die Kolorierung zu viele Details entfernt.
  — <https://arxiv.org/abs/2411.09703>
- Für schwache Hardware V1 statt V2 wählen, da V2 laut Angabe etwa 40 GB VRAM benötigt, während V1 die dokumentierte ressourcenschonendere Option ist.
  — <https://github.com/zliucz/MagicQuillV2>
- V1 mit `--recursive` klonen; andernfalls fehlt das erforderliche LLaVA-Submodul.
  — <https://github.com/magic-quill/magicquill>
- Den Pinokio-Installer als Drittanbieter-Code behandeln und vor der Nutzung prüfen: Das aktuelle Skript klont `6Morpheus6/MagicQuill`, nicht das kanonische Repository.
  — <https://raw.githubusercontent.com/pinokiofactory/MagicQuill/main/install.js>
- Vor dem Einsatz einer der beiden Implementierungen in kommerziellen Projekten prüfen, ob CC BY-NC 4.0 zum beabsichtigten Einsatz passt.
  — <https://github.com/zliucz/MagicQuillV2>

## Durch dieses ersetzt {#superseded-by-this}

- 2025-12-03 — MagicQuill V2 ersetzt V1 als aktive Funktionslinie; V1 bleibt jedoch der dokumentierte Pfad für geringen VRAM-Bedarf und ist nicht generell veraltet.
- 2026-09-04 — Das alte Clone-Ziel im V2-README ist veraltet: Die beobachtete Route `magic-quill/MagicQuillV2` liefert 404; verwende das aktive Repository `zliucz/MagicQuillV2`.
- 2026-09-04 — Pinokio sollte nicht als offizielle Anleitung für MagicQuill-Modelle gelten; der aktuelle Installer ist ein Drittanbieter-Wrapper um einen nicht kanonischen Fork.

## Noch unbekannt {#still-unknown}

- Der ursprüngliche Pinokio-Seiteninhalt vom 2025-02-24 ist über die vorliegende URL heute nicht mehr abrufbar: Sie leitet auf die allgemeine Pinokio-Website weiter, sodass Installer-Revision und Verhalten zu diesem Datum nicht bestätigt sind.
- Die V1-Route `/demo/` lieferte keinen auswertbaren Seiteninhalt, und der Hugging-Face-Space zeigt „Running on Zero“; die Vervollständigung einer Live-Bearbeitung wurde nicht unabhängig getestet.
- Pinokio ist ein Launcher-Pfad und kein zweites MagicQuill-Modell; der genaue Zusammenhang mit dem Ereignis vom 2025-02-24 ist daher unbestätigt.
- Die GitHub-Seiten von V1 und V2 zeigen keine unveränderlichen Software-Releases; daher dienen die Update-Log-Daten der READMEs als verfügbare Release-Nachweise.
- Die angegebenen Hardwarewerte für V1 und V2 sind vom Autor berichtete Anforderungen, keine unabhängigen Benchmarks.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://magicquill.art/demo/ | MagicQuill-Demo | 2026-09-04 |
| https://github.com/magic-quill/magicquill | MagicQuill V1 Repository | 2026-09-04 |
| https://huggingface.co/spaces/AI4Editing/MagicQuill | MagicQuill V1 Hugging-Face-Space | 2026-09-04 |
| https://pinokio.computer/ | Pinokio | 2026-09-04 |
| https://arxiv.org/abs/2411.09703 | MagicQuill: An Intelligent Interactive Image Editing System | 2026-09-04 |
| https://github.com/pinokiofactory/MagicQuill | Pinokio MagicQuill Repository | 2026-09-04 |
| https://raw.githubusercontent.com/pinokiofactory/MagicQuill/main/install.js | Pinokio MagicQuill Installer-Skript | 2026-09-04 |
| https://github.com/magic-quill/MagicQuillV2 | MagicQuillV2 alte GitHub-Clone-Route | 2026-09-04 |
| https://github.com/zliucz/MagicQuillV2 | MagicQuill V2 Repository | 2026-09-04 |
| https://arxiv.org/abs/2512.03046 | MagicQuillV2: Precise and Interactive Image Editing with Layered Visual Cues | 2026-09-04 |
| https://magicquill.art/v2/ | MagicQuill V2 Projektseite | 2026-09-04 |
| https://huggingface.co/LiuZichen/MagicQuillV2-models | MagicQuill V2 Model Card | 2026-09-04 |
| https://huggingface.co/spaces/AI4Editing/MagicQuillV2 | MagicQuill V2 Hugging-Face-Space | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:magicquill`, Thread `magicquill-development`, 1 datiertes Ereignis vom 2024-11-18 bis 2024-11-18.
- **Praktischer Hinweis:** Ab dem 2024-11-18 konnten Praktiker MagicQuill über die öffentliche Demo und den gehosteten Space evaluieren; das verlinkte Repository diente dazu, die Implementierung vor einer Übernahme zu prüfen.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
