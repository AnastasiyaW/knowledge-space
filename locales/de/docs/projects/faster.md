---
title: "FASTER"
category: projects
date: 2026-03-20
tags: [faster, project]
aliases: ["FASTER"]
level: 2
source_sha256: 08c77261c2f7dc624dc5a41ccdb7f452fa291e6ddb44fcffb37cdb67e37156ac
translation: machine
translated_at: '2026-10-24'
---
# FASTER {#faster}

**Entwicklungslinie:** `project:faster` · Thread `faster`  
**Letztes Ereignis:** 2026-03-20 · 1 datiertes Ereignis seit 2026-03-20 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

FASTER ist eine Open-Source-Methode für schnelles Action-Sampling und Streaming-Deployment, gedacht für Teams, die Flow-Vision-Language-Action-Policies feintunen; sie ist keine eigenständige Roboter-Policy.

- Der Horizon-Aware Schedule priorisiert kurzfristige Aktionen.
- Der Streaming-Client-Server-Pfad sendet frühe Aktionen, während spätere Aktionen noch verfeinert werden.
- Der aktuelle Code baut auf JAX openpi auf und dokumentiert Workflows für π0.5 und AgileX Piper.

## Entwicklungslinie {#development-line}

- **2026-03-20 — Öffentliche FASTER-Website und Repository wurden verknüpft.** Das öffentliche Repository verzeichnete zwei README-Aktualisierungen, mit denen Projekt- und Paper-Stand dokumentiert wurden.

## Was sich geändert hat {#what-changed}

2026-03-19: Das FASTER-Paper erschien auf arXiv als v1. 2026-03-20: Das öffentliche Repository verzeichnete zwei README-Aktualisierungen, mit denen Projekt- und Paper-Stand dokumentiert wurden. 2026-04-29: arXiv v2 erschien ohne technisches Changelog. 2026-04-30: FASTER v1.0 hat die offizielle Implementierung als Open Source veröffentlicht. 2026-05-16: arXiv v3 wurde ohne Revisionshinweis zur aktuellen Paper-Version.

## Anwendung {#how-to-use-this}

Stand 2026-03-20: Nutzen Sie die öffentliche FASTER-Website und das GitHub-Repository für Projektdokumentation und Quellcodezugriff; weitere Nutzungs- oder Release-Aussagen haben wir nicht verifiziert.

1. Starten Sie mit einem JAX-openpi-Flow-Policy-Workflow und einer bereits abgebildeten Roboterplattform; verwenden Sie `pi05_faster_agilex` als gepflegte Referenz, statt FASTER als vortrainierte eigenständige Policy zu behandeln.
  — <https://github.com/innovator-zero/FASTER>
2. Klonen Sie mit Submodulen und erstellen Sie anschließend die dokumentierte uv-Umgebung mit `GIT_LFS_SKIP_SMUDGE=1 uv sync` und `GIT_LFS_SKIP_SMUDGE=1 uv pip install -e .`.
  — <https://github.com/innovator-zero/FASTER>
3. Bereiten Sie einen LeRobot-v2.1-Datensatz sowie das Mapping der Ein- und Ausgaben der Plattform vor und berechnen Sie anschließend die Normalisierungsstatistiken für die FASTER-Konfiguration.
  — <https://github.com/innovator-zero/FASTER>
4. Feintunen Sie π0.5 mit `pi05_faster_agilex` und verweisen Sie den Policy-Server auf den resultierenden Checkpoint.
  — <https://github.com/innovator-zero/FASTER>
5. Starten Sie den Policy-Server und den Roboter-Controller-Client über WebSocket; wählen Sie je nach Reaktionszeitanforderung der Aufgabe asynchrones HAS oder Streaming-Inferenz.
  — <https://github.com/innovator-zero/FASTER>

## Best Practices {#best-practices}

- Lernen Sie den ursprünglichen openpi-Workflow kennen, bevor Sie FASTER anpassen.
  — <https://github.com/innovator-zero/FASTER>
- Halten Sie die HAS-Inferenzparameter `alpha` und `u0` auf den Werten, die beim Training verwendet wurden.
  — <https://github.com/innovator-zero/FASTER>
- Setzen Sie die Controller-Verzögerung einen Schritt über der gemessenen Inferenzverzögerung, um Schwankungen von Laufzeit und Netzwerk abzufangen, und halten Sie den Execution Horizon mindestens so groß wie die Verzögerung.
  — <https://github.com/innovator-zero/FASTER>
- Verwenden Sie für Remote-Inferenz ein kabelgebundenes LAN, um Latenz und Paketverluste zu reduzieren.
  — <https://github.com/innovator-zero/FASTER>
- Reservieren Sie Streaming mit kleinem Execution Horizon für hochdynamische Aufgaben; bei gewöhnlichem Pick-and-Place oder Falten kann es Bewegungsruckeln verursachen.
  — <https://github.com/innovator-zero/FASTER>
- Beachten Sie die dokumentierten Speichergrenzen und die aktuelle Abgrenzung: Vollständiges Feintuning von π0.5 wurde unter Ubuntu 22.04 getestet, Multi-Node-Training wird nicht unterstützt.
  — <https://github.com/innovator-zero/FASTER>

## Abgelöst durch {#superseded-by-this}

- 2026-04-30: Das Open-Source-Release v1.0 hat den früheren Zustand abgelöst, in dem FASTER keine öffentliche Implementierung hatte.
- 2026-05-16: arXiv v3 hat arXiv v1 als aktuellen Paper-Text abgelöst.

## Noch unbekannt {#still-unknown}

- Offizielle Materialien stellen weder einen Checkpoint-Download noch ein vollständiges Reproduktionsrezept für das berichtete Echtroboter-Setup mit Tischtennis bereit; die Dokumentation setzt lokal trainierte Checkpoints voraus.
- arXiv datiert v2 und v3 ohne technisches Changelog, daher bleiben ihre genauen Unterschiede zu v1 unbekannt.
- Wir haben keine offizielle technische Dokumentation in vereinfachtem Chinesisch gefunden; verfügbare chinesische Erklärungen sind sekundär.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://innovator-zero.github.io/FASTER/ | FASTER: Rethinking Real-Time Flow VLAs | 2026-09-06 |
| https://github.com/innovator-zero/FASTER | FASTER: Rethinking Real-Time Flow VLAs | 2026-09-06 |
| https://arxiv.org/abs/2603.19199 | [2603.19199] FASTER: Rethinking Real-Time Flow VLAs | 2026-09-06 |
| https://github.com/innovator-zero/FASTER/commits/main | Commits · innovator-zero/FASTER | 2026-09-06 |
| https://github.com/innovator-zero/FASTER/releases/tag/v1.0 | Release FASTER Open-source · innovator-zero/FASTER | 2026-09-06 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:faster`, Thread `faster`, 1 datiertes Ereignis 2026-03-20 → 2026-03-20.
- **Praktischer Hinweis:** Stand 2026-03-20: Nutzen Sie die öffentliche FASTER-Website und das GitHub-Repository als Ausgangspunkte für Projektdokumentation und Quellcodezugriff; weitere Nutzungs- oder Release-Aussagen haben wir nicht verifiziert.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
