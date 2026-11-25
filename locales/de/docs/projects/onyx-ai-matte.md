---
title: "ONYX Ai Matte"
category: projects
date: 2026-03-10
tags: [onyx-ai-matte, project]
aliases: ["ONYX Ai Matte"]
level: 2
source_sha256: 08536999395bc015895c0b8c358e3283104c5cd05c6b46857d5d0e2ae9ca06c2
translation: machine
translated_at: '2026-10-24'
---
# ONYX Ai Matte {#onyx-ai-matte}

**Entwicklungslinie:** `project:onyx-ai-matte` · Thread `onyx-ai-matte`  
**Letztes Ereignis:** 2026-03-10 · 1 datiertes seit 2026-03-10 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ONYX Ai Matte ist ein lokales OFX-Werkzeug für Rotoscoping und Alpha-Extraktion in Nuke, DaVinci Resolve, Fusion, Flame und Natron. Funktionen: Prompts als Box, Punkt, Text oder Maske, Tracking von bis zu 16 Objekten, Kantenverfeinerung mit VitMatte/MeMatte und Export gebackener Masken. Einschränkungen: Windows erfordert NVIDIA RTX 20-Serie oder neuer und 6 GB VRAM; macOS erfordert Apple Silicon und macOS 15 oder neuer. Das Ergebnis deckt in der Regel 60–80 % des Mattes ab, die finale Feinarbeit übernimmt der Compositor. Fazit: eine praktikable Alternative zu Magic Mask für lokale OFX-Pipelines, aber kein Ersatz für die Qualitätskontrolle der finalen Maske.

## Entwicklungslinie {#development-line}

- **2026-03-10 — Projektressourcen von ONYX Ai Matte wurden verknüpft.** Am 2026-03-10 wurde die Entwicklungslinie von ONYX Ai Matte mit der Projektwebsite und einem Hugging-Face-Ressourcenlink verknüpft. Die datierten Links belegen eine extern erreichbare Projektreferenz, belegen jedoch ohne den Originalbeitrag oder die Recherche weder ein bestimmtes Release, eine Modellversion, eine Funktion noch eine Änderung.

## Was sich geändert hat {#what-changed}

2026-03-10 — Der Link im Ereignis führte auf die offizielle ONYX-Website; eine unabhängige datierte Bestätigung einer konkreten Änderung genau an diesem Tag wurde nicht gefunden. 2026-03-24 — ONYX Ai Matte v2.5 wurde veröffentlicht: fünf Betriebsmodi, Auto-Tracking, Text- und Maskenprompts sowie mehrobjektige Segmentierung. 2026-07-17 — v3.1.0 ergänzte die Steuerung des Eingangsfarbraums für ACES/OCIO, die Proxy-Aktivierung und Stabilitätskorrekturen. 2026-08-03 — v3.2.0 ergänzte Apple Silicon/macOS und Flame. 2026-08-12 — v3.3.0 vergrößerte den Cache für getrackte Masken auf etwa 12 000 6K-Frames. 2026-08-31 — v3.4.0 ergänzte getrennte Kanäle für Object Mask und Unknown Zone im Refiner Direct.

## So wird es verwendet {#how-to-use-this}

Ab dem 2026-03-10 sollten Anwender ONYX Ai Matte als separat verknüpfte Projekt-/Ressourcenlinie behandeln und vor dem Einsatz Verfügbarkeit und Nutzung auf der offiziellen Website und der Hugging-Face-Ressource prüfen.

1. Schließen Sie die Host-Anwendung, installieren Sie das aktuelle Paket, starten Sie den Host neu und fügen Sie den OFX-Effekt ONYX Ai Matte v3 hinzu; die 7-tägige Testphase beginnt beim ersten Hinzufügen des Nodes.
  — <https://onyxofx.com/docs/>
2. Speisen Sie den Clip in Source ein, markieren Sie auf dem Startframe das Objekt mit einem Box-, Punkt-, Text- oder Masken-Prompt und starten Sie einen einmaligen Durchlauf für durchgehendes Tracking.
  — <https://onyxofx.com/docs/>
3. Prüfen Sie die Maske, korrigieren Sie die Kante mit VitMatte/MeMatte und backen Sie bei Bedarf die PNG-/EXR-Sequenz in einen separaten Ordner.
  — <https://onyxofx.com/docs/>

## Bewährte Praktiken {#best-practices}

- Deaktivieren Sie Loop beim Tracking; für einen vollständigen Durchlauf vom Startframe in beide Richtungen verwenden Sie Bounce/Ping-Pong.
  — <https://onyxofx.com/docs/>
- Bei einem instabilen Track oder einem Track, der bei schneller Bewegung abgeschnitten wird, erhöhen Sie Crop Padding oder deaktivieren Sie Crop Mode.
  — <https://onyxofx.com/docs/>
- Verwenden Sie das AI-Matt nicht ungeprüft: Das Werkzeug liefert etwa 60–80 % des Ergebnisses, die finale Feinarbeit bleibt dem Compositor überlassen.
  — <https://onyxofx.com/docs/>

## Dadurch ersetzt {#superseded-by-this}

- 2026-08-31 — Der Refiner-Direct-Modus wurde in v3.4.0 durch die Zuweisung von Object Mask und Unknown Zone auf getrennte Eingangskanäle ersetzt.
- 2026-08-12 — Der frühere kleine Tracking-Cache wurde durch den komprimierten Cache der v3.3.0 ersetzt.
- 2026-08-03 — Der Stand vor der macOS-/Flame-Unterstützung ist seit v3.2.0 veraltet.

## Weiterhin unbekannt {#still-unknown}

- Die offiziellen Release Notes enthalten keinen Eintrag für 2026-03-10; daher lässt sich diesem Tag keine bestimmte Version oder Funktion zuverlässig zuordnen.
- Im vorgegebenen JSON-Schema fehlen die Felder event_findings und new_events; bestätigte zusätzliche Daten sind unter what_changed aufgeführt, die Zuordnung zum Ereignis vom 2026-03-10 bleibt als Unsicherheit erhalten.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://onyxofx.com/ | ONYX Ai Matte — AI Roto for Nuke & Resolve. No Subscription | 2026-09-05 |
| https://onyxofx.com/docs/ | ONYX Ai Matte Documentation | Install and Parameters | 2026-09-05 |
| https://onyxofx.com/release-notes/ | Release Notes — ONYX Ai Matte | 2026-09-05 |
| https://www.cgchannel.com/2026/03/onyx-ai-matte-automatically-generates-masks-from-video-footage/ | ONYX Ai Matte automatically generates masks from video | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:onyx-ai-matte`, Thread `onyx-ai-matte`, 1 datiertes Ereignis 2026-03-10 → 2026-03-10.
- **Praxishinweis:** Ab dem 2026-03-10 sollten Anwender ONYX Ai Matte als separat verknüpfte Projekt-/Ressourcenlinie behandeln und vor dem Einsatz Verfügbarkeit und Nutzung auf der offiziellen Website und der Hugging-Face-Ressource prüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Angaben unter „Dadurch ersetzt“.
