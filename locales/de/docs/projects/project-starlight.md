---
title: "Project Starlight"
category: projects
date: 2025-02-11
tags: [project, project-starlight, project-starlight-public-rollout, project_starlight]
aliases: ["Project Starlight"]
level: 3
source_sha256: 946c6d6b71a0022fa6895f7d6e4b0986012f88110282466ef8ff4eb822b51d6f
translation: machine
translated_at: '2026-10-24'
---
# Project Starlight {#project-starlight}

**Entwicklungslinie:** `project:project-starlight` · Thread `project-starlight-public-rollout`  
**Letztes Ereignis:** 2025-02-11 · 2 datierte seit 2025-02-06 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Topazs ursprüngliches generatives Diffusionsmodell für Restauratoren von Archivvideos und niedrig aufgelösten GenAI-Clips.

- Hochskalierung der Auflösung.
- Rekonstruktion der Struktur.
- Wiederherstellung der zeitlichen Konsistenz.

Das ursprüngliche Modell läuft in der API als Starlight Precise 1 (`sl-1`) ohne manuelle Steuerungsmöglichkeiten und ist auf 9 000 Eingabeframes begrenzt. Es handelt sich nicht um ein festes Produkt, sondern um den Beginn einer Modellfamilie. Die Auswahl sollte daher anhand der konkreten Starlight-Variante und des Zielsystems erfolgen.

## Entwicklungslinie {#development-line}

- **2025-02-06 — Topaz Labs verwies öffentlich auf Project Starlight.** Ein cloudbasiertes Forschungs-Diffusionsmodell für die Videorestauration, das Qualität über Geschwindigkeit und Modellgröße stellt.
- **2025-02-11 — Project Starlight erschien in Topaz Labs Experiments.** Am 2025-02-11 wurde eine Project-Starlight-URL in der Webanwendung Experiments von Topaz Labs erfasst. Die vorliegenden Belege bewahren den Seiteninhalt nicht, daher hält dieser Eintrag den datierten Experiments-Endpunkt fest, ohne einen konkreten Workflow, eine Berechtigung oder einen Funktionsumfang zu behaupten.

## Was sich geändert hat {#what-changed}

- 2025-02-06 — Topaz stellte Project Starlight als cloudbasiertes Forschungs-Diffusionsmodell für die Videorestauration vor, das Qualität über Geschwindigkeit und Größe stellt.
- 2025-02-11 — Das Modell wurde über eine experimentelle Weboberfläche verfügbar. Zu diesem Zeitpunkt galten für kostenlose Vorschauen und kostenpflichtige Renderings unterschiedliche Nutzungsbedingungen für Inhalte.
- 2025-03-05 — Der frühe Zugang erweiterte sich um 4K-Starlight-Renderings.
- 2025-03-25 — Topaz bereitete die erste lokal ausführbare Variante der Serie vor.
- 2025-05-13 — Starlight Mini wurde für das lokale Rendering unter Windows mit NVIDIA-GPUs eingeführt.
- 2025-09-17 — Starlight Sharp erweiterte das lokale und cloudbasierte Angebot um eine detailreichere Variante.

## Verwendung {#how-to-use-this}

Behandle den Topaz-Labs-Experiments-Pfad ab 2025-02-11 als datierten Einstiegspunkt. Prüfe die aktuelle Experiment-Seite, bevor du sie nutzt, da diese Links allein weder Fähigkeiten noch Zugangsvoraussetzungen belegen.

1. Entscheide, ob wir ein lokales Modell in Topaz Video oder ein Cloud-Modell benötigen. Die Dokumentation nennt Mini, Sharp, Fast 2, HQ und Precise 2.5/2.6 und weist darauf hin, dass Cloud-Modelle auch in Astra laufen.
  — <https://docs.topazlabs.com/topaz-video/project-starlight-series>
2. Für das lokale Rendering installiere Topaz Video zusammen mit Neuroserver. Alle Starlight-Diffusionsmodelle setzen dies voraus. Wenn Neuroserver ausfällt, empfiehlt Topaz eine Neuinstallation der Anwendung im Repair mode.
  — <https://docs.topazlabs.com/topaz-video/project-starlight-series>
3. Für die programmatische Verarbeitung lade das Video über die Video API mit dem Modell `sl-1` hoch. Setze technische Parameter nach Bedarf und überschreite nicht 9 000 Eingabeframes.
  — <https://developer.topazlabs.com/video-models/starlight/starlight-precise-1>

## Best Practices {#best-practices}

- Plane die Warteschlange anhand der tatsächlichen Dauer, Auflösung und Bildrate. Starlight-Diffusionsläufe können von einigen Minuten bis zu mehreren Tagen dauern.
  — <https://docs.topazlabs.com/topaz-video/project-starlight-series>
- Teste einen kurzen, repräsentativen Clip, bevor du ein vollständiges Rendering startest, wenn die ursprüngliche Identität und feine Details wichtig sind. Frühe Nutzerbeispiele zeigten veränderte Gesichtsausdrücke und Artefakte bei beschädigtem VHS-Material.
  — <https://community.topazlabs.com/t/project-starlight-video-ai-6-1-beta/87108?page=10>
- Lade keine sensiblen Aufnahmen in die kostenlose Vorschau-Stufe hoch. Im Februar 2025 trennte Topaz die Modi: Kostenpflichtige Renderings wurden ohne Zustimmung nicht für das Training von Modellen verwendet, während kostenlose Vorschauen gespeichert, geprüft und in der Forschung genutzt werden konnten.
  — <https://community.topazlabs.com/t/project-starlight-video-ai-6-1-beta/87108?page=10>

## Hierdurch ersetzt {#superseded-by-this}

- 2025-05-13 — Die alte Regel, dass Starlight nur in der Cloud läuft, gilt für die gesamte Familie nicht mehr. Starlight Mini erhielt lokales Rendering unter Windows mit NVIDIA-GPUs, was jedoch keine lokale Unterstützung für das ursprüngliche `sl-1` belegt.
- 2025-09-17 — Die frühere Aufteilung in zwei Modelle, Project Starlight und Starlight Mini, ist überholt. Starlight Sharp kam zum Produktangebot hinzu.

## Weiterhin unbekannt {#still-unknown}

- Die ursprüngliche Experiment-URL belegt weder die aktuelle Oberfläche noch die aktuelle Preisstufe. Aktuelle Einstiegspunkte von Topaz führen zu Astra, Topaz Video und der API.
- Den Originaltext des X-Beitrags vom 2025-02-06 haben wir nicht direkt geprüft. Ein datierter Beitrag der Topaz Community vom selben Tag bestätigt jedoch dessen Inhalt.
- Das genaue Datum, an dem Topaz Project Starlight offiziell in Starlight Precise 1 umbenannt hat, ist nicht dokumentiert. Die aktuelle Dokumentation bestätigt die Kontinuität, nicht aber das Umbenennungsdatum.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://x.com/topazlabs/status/1887497602398073234 | Ankündigung von Project Starlight durch Topaz Labs | 2026-09-05 |
| https://app.topazlabs.com/experiments/starlight | Project-Starlight-Experiment | 2026-09-05 |
| https://community.topazlabs.com/t/the-process-of-improving-video-quality-with-project-starlight/87143 | The process of improving video quality with Project Starlight | 2026-09-05 |
| https://community.topazlabs.com/t/project-starlight-video-ai-6-1-beta/87108?page=10 | Project Starlight - Video AI 6.1 Beta | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-ai-6-0-4/87385 | Topaz Video AI 6.0.4 | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-ai-6-1-2-6-1-3/88231 | Topaz Video AI 6.1.2 + 6.1.3 | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-ai-beta-6-2-0-0-b/89146 | Topaz Video AI Beta 6.2.0.0.b | 2026-09-05 |
| https://community.topazlabs.com/t/video-ai-7-0-new-starlight-mini-local-ai-model/90631 | Video AI 7.0 - NEUES Starlight Mini (lokales) KI-Modell | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-1-0-0-new-studio-release/95523/1 | Topaz Video 1.0.0 (neue Studio-Version) | 2026-09-05 |
| https://developer.topazlabs.com/video-models/starlight/starlight-precise-1 | Starlight Precise 1 \| Entwicklerdokumentation | 2026-09-05 |
| https://docs.topazlabs.com/topaz-video/project-starlight-series | Starlight Series \| Topaz Video | 2026-09-05 |
| https://www.topazlabs.com/starlight | Project Starlight \| KI-Videoverbesserung | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:project-starlight`, Thread `project-starlight-public-rollout`, 2 datierte Ereignisse 2025-02-06 → 2025-02-11.
- **Praktischer Hinweis:** Behandle den Topaz-Labs-Experiments-Pfad ab 2025-02-11 als datierten Einstiegspunkt für Project Starlight. Prüfe die aktuelle Experiment-Seite, bevor du sie nutzt, da diese Links allein weder Fähigkeiten noch Zugangsvoraussetzungen belegen.
- **Konfidenz:** hoch. Für die Frage, was veraltet ist, sind die datierten Ersetzungshinweise maßgeblich.
