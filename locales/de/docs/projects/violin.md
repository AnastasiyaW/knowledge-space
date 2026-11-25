---
title: "Violin"
category: projects
date: 2026-05-15
tags: [project, violin]
aliases: ["Violin"]
level: 2
source_sha256: 5b570a604f02309c9af702123a4cc6205cd6b13ea8c7747be189da9300dc0919
translation: machine
translated_at: '2026-10-24'
---
# Violin {#violin}

**Entwicklungslinie:** `project:violin` · Thread `violin`  
**Letztes Ereignis:** 2026-05-15 · 1 datiertes seit 2026-05-15 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Violin ist eine MIT-lizenzierte CLI, eine FastAPI-App und ein Claude-Code-Skill für Videoübersetzung und Synchronisation.

- Transkription: extrahiert Sprache aus Videos.
- Übersetzung: übersetzt Dialoge in Zielsprachen.
- Synchronisation: erzeugt ersetzende Sprachaufnahmen.
- SRT-Untertitel: erstellt zeitgesteuerte Untertiteldateien.
- Video-Q&A: beantwortet Fragen zum Videoinhalt.

Unterstützt 33 Zielsprachen; sechs Stilprofile sind als experimentell gekennzeichnet.

Praktisch für Videos, für die eine Berechtigung vorliegt, allerdings warnt die öffentliche Demo vor möglichen Übersetzungsfehlern.

## Entwicklungslinie {#development-line}

- **2026-05-15 — Öffentliche Vorstellung des Übersetzungsprojekts Violin.** Am 2026-05-15 wurde Violin öffentlich mit einem Artikel von Together AI, einem offenen GitHub-Repository und seiner Projektwebsite verknüpft. Die datierten Links deuten auf eine öffentliche Vorstellung eines quelloffenen, übersetzungsorientierten Projekts hin und begründen dessen erste öffentliche Referenzen.

## Was sich geändert hat {#what-changed}

2026-05-15 — Violin erschien als offene Pipeline, die ASR, LLM-Übersetzung und TTS kombiniert. Die primäre Quelle datiert den Beitrag auf 2026-05-14 statt 2026-05-15. Als ursprüngliche Modelle wurden Together Whisper Large V3, DeepSeek V4 Pro und Cartesia Sonic 3 genannt. Das aktuelle Repository zeigt Version 0.1.1, 33 Sprachen, austauschbare Anbieter Together/OpenAI/ElevenLabs und keine GitHub Releases. Diese späteren Änderungen lassen sich anhand der verfügbaren Primärquellen nicht verlässlich datieren.

## Anwendung {#how-to-use-this}

Ab 2026-05-15 sollten Praktiker Violin als öffentlich erreichbares, übersetzungsorientiertes Projekt betrachten und es anhand des verlinkten Repositorys und der Projektseite bewerten.

1. Für die lokale Nutzung Python 3.10+, ffmpeg und das Paket über `uv tool install violin` installieren. Einen Anbieterschlüssel setzen und dann `violin input.mp4 output.mp4 --language Chinese` ausführen.
  — <https://github.com/shang-zhu/violin>
2. Für die Web-UI und die REST-API `violin-api` starten. Einen Job über `POST /jobs` anlegen, ihn abfragen und die Video- oder SRT-Datei herunterladen.
  — <https://github.com/shang-zhu/violin>
3. Für einen schnellen Test die Web-Demo verwenden. Eine Datei hochladen oder eine URL einfügen und anschließend Sprache, Stimme, Untertitel und Voice-over-Modus auswählen.
  — <https://www.violin-ai.com/>

## Best Practices {#best-practices}

- Nur eigene, gemeinfreie oder unter Creative Commons stehende Medien übersetzen oder Inhalte mit ausdrücklicher Erlaubnis. Die Demo beschränkt Eingabe-URLs auf diese Regel.
  — <https://www.violin-ai.com/>
- Mit dem Standardprofil und der automatischen Stimmauswahl beginnen. Für Terminologie eine eigene YAML-Konfiguration verwenden und die Ausgabe prüfen, da die Demo als Research-Beta gekennzeichnet ist.
  — <https://github.com/shang-zhu/violin>
- In der Produktion `config/prod.yaml` verwenden. Sie begrenzt Uploads, serialisiert Jobs und begrenzt die Parallelität von ffmpeg.
  — <https://github.com/shang-zhu/violin>

## Abgelöst durch {#superseded-by-this}

- 2026-05-14 — Die erste Beschreibung nannte als Standard DeepSeek V4 Pro und Qwen3.5-397B-A17B. Die aktuelle README gibt DeepSeek-V4-Pro-0813 für die Übersetzung und GLM-5.3-Flash für den Chat an, aber kein Datum bestätigt den Wechsel.
- 2026-05-14 — Fehlendes Voice Cloning bleibt eine aktive Einschränkung. Das Repository führt es weiterhin unter TODO und nicht als verfügbare Funktion.

## Weiterhin unbekannt {#still-unknown}

- Die verfügbaren Primärquellen enthalten keine datierte Historie nach dem Start. Aktuelle Modelleinstellungen erfassen wir nicht als neue datierte Ereignisse.
- GitHub zeigt keine Releases. Version 0.1.1 erscheint in pyproject.toml, doch die verfügbaren Quellen bestätigen weder ein Veröffentlichungsdatum noch eine PyPI-Verteilung.
- Nutzer müssen die Qualität der Synchronisation für ihre eigene Sprache und ihr eigenes Material selbst prüfen. Die öffentliche Demo warnt, dass Übersetzungen Fehler enthalten können.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.together.ai/blog/violin-open-source-translation-skill | Violin: Ein Open-Source-Skill für Videoübersetzung, der Sprachbarrieren überwindet | 2026-09-05 |
| https://github.com/shang-zhu/violin | Repository und README von shang-zhu/violin | 2026-09-05 |
| https://www.violin-ai.com/ | Violin — Video Narrator | 2026-09-05 |
| https://github.com/shang-zhu/violin/releases | GitHub-Releases von Violin | 2026-09-05 |
| https://raw.githubusercontent.com/shang-zhu/violin/main/pyproject.toml | pyproject.toml von Violin | 2026-09-05 |
| https://raw.githubusercontent.com/shang-zhu/violin/main/config/default.yaml | Standardkonfiguration von Violin | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:violin`, Thread `violin`, 1 datiertes Ereignis 2026-05-15 → 2026-05-15.
- **Praktischer Hinweis:** Ab 2026-05-15 sollten Praktiker Violin als öffentlich erreichbares, übersetzungsorientiertes Projekt betrachten und es anhand des verlinkten Repositorys und der Projektseite bewerten.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, sind die datierten Ablösungen maßgeblich.
