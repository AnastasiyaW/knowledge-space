---
title: "MAGI-2"
category: projects
date: 2026-08-07
tags: [magi, magi-2, magi-2-preview, project]
aliases: ["MAGI-2"]
level: 2
source_sha256: f35d9cc563890a4d8aff7689c00ed212c62b75c7a4f2db5762b478bf67aefe7f
translation: machine
translated_at: '2026-10-24'
---
# MAGI-2 {#magi-2}

**Entwicklungslinie:** `project:magi-2` · Thread `magi-2-preview`  
**Letztes Ereignis:** 2026-08-07 · 1 datiertes Ereignis seit 2026-08-07 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

MAGI-2 Preview ist ein vereinheitlichtes Audio-Video-MoE-Modell mit 114B Parametern für Teams, die lokal 10-Sekunden-Clips mit synchronisiertem Audio aus Text oder Bildern erzeugen wollen.

- T2V erzeugt Video aus Textprompts mit gemeinsam erzeugtem Audio.
- I2V animiert ein Startbild zu einem Video mit gemeinsam erzeugtem Audio.
- Eine zweistufige Pipeline erzeugt eine Vorschau und verfeinert die Ausgabe bis 1080p.

Das Modell nutzt 6B aktive Parameter pro Token, etwa 307 GB Gewichte und acht Hopper-GPUs. Es handelt sich um eine infrastrukturintensive Open-Preview-Veröffentlichung, kein leichtgewichtiges API-Tool.

## Entwicklungslinie {#development-line}

- **2026-08-07 — Sand AI hat Preview-Material zu MAGI-2 veröffentlicht.** Das Modell verwendet 114B Parameter mit etwa 6B aktiven pro Token auf einer vereinheitlichten MagiMoE-Audio-Video-Architektur. Die Repository-Dokumentation beschränkt die Veröffentlichung auf 10-Sekunden-Clips, eine Preview-Stufe mit Refiner bis 1080p sowie T2V und I2V mit synchronisiertem Ton.

## Was sich geändert hat {#what-changed}

2026-08-07 — MAGI-2 Preview ist mit Gewichten und Inferenzcode verfügbar. Primärmaterial von Sand AI vom 2026-08-05 gibt den Umfang vor: 114B Parameter, etwa 6B aktiv pro Token und eine vereinheitlichte MagiMoE-Audio-Video-Architektur. Die Repository-Dokumentation beschränkt die Veröffentlichung auf 10-Sekunden-Clips, eine Preview-Stufe und einen Refiner bis 1080p sowie T2V und I2V mit Ton.

## So nutzt man es {#how-to-use-this}

Stand 2026-08-07 sollte MAGI-2 als öffentlich vorab veröffentlichtes Sand-AI-Projekt betrachtet werden. Vor einer Bewertung oder Integration sollten das verlinkte Repository, die Modellseite und die API-v2-Dokumentation konsultiert werden. Konkrete Funktionen und Zugangsbedingungen müssen weiterhin direkt verifiziert werden.

1. Eine Linux-Umgebung mit Python 3.12, aktuellem CUDA, ffmpeg und acht NVIDIA-Hopper-GPUs vorbereiten, wie vom Inferenzcode vorausgesetzt.
  — <https://github.com/SandAI-org/MAGI-2-preview>
2. Das Docker-Image ziehen oder aus dem Quellcode bauen. Für Reproduzierbarkeit den Image-Tag angeben, der zum Commit passt, statt `latest` zu verwenden.
  — <https://github.com/SandAI-org/MAGI-2-preview>
3. Den vollständigen Checkpoint-Satz von sand-ai/MAGI-2-preview in den Ordner `ckpt` herunterladen, ohne Verzeichnisse umzubenennen.
  — <https://huggingface.co/sand-ai/MAGI-2-preview>
4. T2V mit einem Textprompt oder I2V mit einem Prompt und einem ersten Frame ausführen. Die Ausgabe ist ein 10-Sekunden-Clip, und 1080p läuft durch Preview und Refiner.
  — <https://github.com/SandAI-org/MAGI-2-preview>

## Bewährte Vorgehensweisen {#best-practices}

- Den Docker-Tag auf einen bestimmten Commit festlegen und ihn zusammen mit den Ergebnissen protokollieren, da sich `latest` ändert.
  — <https://github.com/SandAI-org/MAGI-2-preview>
- Das standardmäßige gestufte Offloading für Preview und Refiner bei 1080p beibehalten, da Komponenten und Aktivierungen selbst auf einer 80-GB-GPU nicht gemeinsam hineinpassen.
  — <https://github.com/SandAI-org/MAGI-2-preview>
- Strukturierte Prompt-Erweiterung für die volle 10-Sekunden-Szene verwenden, wenn ein manueller Prompt Aktion, Bildausschnitt und Audio nicht festlegt.
  — <https://github.com/SandAI-org/MAGI-2-preview>

## Abgelöst durch diesen Stand {#superseded-by-this}

- 2026-08-05 — MAGI-2 Preview wird in verifizierten Primärquellen nicht durch ein separates, öffentlich datiertes Folgerelease ersetzt; die Dokumentation kennzeichnet die destillierte Variante als „coming soon“.
- 2026-08-07 — Die Annahme, MAGI-2 sei ein fertiges öffentliches API-Produkt, ist überholt: Die verifizierte Implementierung stellt offene Gewichte und Inferenzcode mit Cluster-Anforderungen bereit.

## Weiterhin unbekannt {#still-unknown}

- Die URL https://platform.sand.ai/docs/api-v2 lieferte während der Verifikation keine lesbare Dokumentation. Daher bleiben API-Funktionen, Preise, Limits und die aktuelle Verfügbarkeit unbestätigt.
- Verifizierte Primärquellen enthalten kein separat datiertes Ereignis nach 2026-08-07. Änderungen im aktuellen README lassen sich nicht verlässlich als neues Release datieren.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://sand.ai/blog/magi-2-preview | MAGI-2 Preview: Scaling Video Generation Models Efficiently | 2026-09-05 |
| https://github.com/SandAI-org/MAGI-2-preview | SandAI-org/MAGI-2-preview | 2026-09-05 |
| https://huggingface.co/sand-ai/MAGI-2-preview | sand-ai/MAGI-2-preview | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:magi-2`, Thread `magi-2-preview`, 1 datiertes Ereignis 2026-08-07 → 2026-08-07.
- **Praktischer Hinweis:** Stand 2026-08-07 sollte MAGI-2 als öffentlich vorab veröffentlichtes Sand-AI-Projekt betrachtet werden. Vor einer Bewertung oder Integration sollten das verlinkte Repository, die Modellseite und die API-v2-Dokumentation konsultiert werden. Konkrete Funktionen und Zugangsbedingungen müssen weiterhin direkt verifiziert werden.
- **Konfidenz:** hoch. Die oben datierten Ablösungen sind maßgeblich dafür, was veraltet ist.
