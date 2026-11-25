---
title: "PixVerse — Öffentliche Verfügbarkeit"
category: projects
date: 2025-04-29
tags: [pixverse, project, public-availability]
aliases: ["PixVerse"]
level: 2
source_sha256: c1715fe0325eb7d12d4eac5444f8e8429f24aa5b20df5977274848427040b189
translation: machine
translated_at: '2026-10-24'
---
# PixVerse — Öffentliche Verfügbarkeit {#pixverse-public-availability}

**Entwicklungslinie:** `project:pixverse` · Thread `public-availability`  
**Letztes Ereignis:** 2025-04-29 · 2 datierte Einträge seit 2024-02-09 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

PixVerse ist eine proprietäre Plattform zur Videogenerierung für Kreative und Teams.

- Text-zu-Video- und Bild-zu-Video-Generierung
- Vorlagen und Übergangssteuerung
- Lip Sync
- API- und CLI-Zugang

V6 erzeugt Clips von bis zu 15 Sekunden in 1080p mit Multi-Shot-Logik und nativem Audio. Die Plattform eignet sich für kurze Videos, die älteren Hinweise zu V2 und V3 gelten jedoch nicht für das aktuelle Angebot.

## Entwicklungslinie {#development-line}

- **2024-02-09 — Öffentliche Website von PixVerse.** Am 2024-02-09 wurde PixVerse mit der öffentlichen Website pixverse.ai verknüpft. Dieser Eintrag etablierte einen öffentlichen Web-Endpunkt für das Projekt. Allein der Link bestätigt weder ein Startdatum, eine Version noch Funktionen.
- **2025-04-29 — PixVerse Web-App und iOS-Eintrag.** Am 2025-04-29 verwiesen Quellen neben der Website auf die PixVerse Web-App und einen Eintrag im iOS App Store. Bis zu diesem Datum waren sowohl der Web- als auch der iOS-Zugang verfügbar. Diese Hinweise bestätigen nicht, ob einer der beiden Zugänge an diesem Datum gestartet, seine Version gewechselt oder eine bestimmte Funktion erhalten hat.

## Was sich geändert hat {#what-changed}

- **2024-02-09:** Der Webdienst diente als früher Einstiegspunkt zu PixVerse. Spätere Rückblicke datieren die Veröffentlichung von V2 mit der DiT-Architektur auf Februar 2024.
- **2024-10-30:** Nach der Veröffentlichung von V3 am 29. Oktober ergänzte die Plattform LipSync, Effect, Extend, ein überarbeitetes Style-Werkzeug und 5 Seitenverhältnisse.
- **2025-04-29:** PixVerse veröffentlichte ein MCP für die API-Integration. Damit wurde das Werkzeug von einem Consumer-Web-Generator zu einer Schnittstelle für Agenten und Code erweitert.

## Anwendung {#how-to-use-this}

Bewerten Sie PixVerse Stand 2025-04-29 über die Web-App und den iOS-Eintrag und nicht allein anhand des Homepage-Links. Prüfen Sie die aktuelle Verfügbarkeit und Funktionen direkt.

1. Öffnen Sie PixVerse, wählen Sie V6 und entscheiden Sie sich zwischen Text-zu-Video-Generierung oder Bildanimation.
  — <https://pixverse.ai/en/model/pixverse-v6>
2. Legen Sie Dauer, Auflösung und Seitenverhältnis für den Ausspielkanal fest, bevor Sie die Generierung starten.
  — <https://pixverse.ai/en/model/pixverse-v6>
3. Beschreiben Sie Motiv, Szene, Kamerabewegung, Licht und Audio, generieren Sie dann das Video und prüfen Sie Bewegungsstabilität, Figurenkonsistenz und Ton.
  — <https://pixverse.ai/en/model/pixverse-v6>
4. Für die API erzeugen Sie einen API-Schlüssel, senden für jede Aufgabe eine eindeutige AI-Trace-ID, speichern die video_id und rufen die Datei ab, sobald sich der Status von 5 auf 1 ändert.
  — <https://docs.platform.pixverse.ai/quick-start-796052m0>

## Bewährte Vorgehensweisen {#best-practices}

- Verwenden Sie für Bild-zu-Video ein eindeutiges Referenzbild mit klaren Kanten und Komposition und geben Sie die Kamerabewegung direkt an.
  — <https://pixverse.ai/en/model/pixverse-v6>
- Beschreiben Sie die Szene konkret mit Motiv, Schauplatz, Handlung, Kamera, Beleuchtung und Ton; vage Prompts verringern die Kontrolle über das Ergebnis.
  — <https://pixverse.ai/en/model/pixverse-v6>
- Halten Sie die zentralen Figurenmerkmale über alle Einstellungen hinweg konsistent und prüfen Sie einen kurzen Testclip, bevor Sie eine ganze Sequenz skalieren.
  — <https://pixverse.ai/en/model/pixverse-v6>
- Verwenden Sie eine AI-Trace-ID nicht erneut: Eine identische Kennung erzeugt keine neue Generierungsaufgabe.
  — <https://docs.platform.pixverse.ai/quick-start-796052m0>

## Hierdurch abgelöst {#superseded-by-this}

- **2024-02-09:** PixVerse als eigenständigen Web-Generator zu betrachten, ist veraltet. Der Dienst umfasst inzwischen Web, API, CLI, eine Agenten-Schnittstelle und mehrere Modelle.
- **2024-10-30:** Die Hinweise zu V3 spiegeln nicht die Grenzen von V6 wider: bis zu 15 Sekunden in 1080p mit Multi-Shot-Logik und nativem Ton.
- **2025-04-29:** Das MCP war ein erster Integrationsschritt. Die aktuelle API-Oberfläche umfasst neuere Modelle und Funktionen, die im Changelog beschrieben sind.

## Noch unbekannt {#still-unknown}

- Der Text der 3 ursprünglichen Beiträge fehlt; daher bestätigen spätere Quellen den Zusammenhang zwischen 2024-02-09 und dem genauen V2-Veröffentlichungsdatum nur auf Monatsebene.
- Der ursprüngliche Link app.pixverse.ai/home und der App-Store-Link lieferten 404, und der verkürzte t.co-Link ließ sich nicht auflösen; ihre Inhalte sind daher nicht berücksichtigt.
- Angaben zu V3 stützen sich auf eine sekundäre Zusammenfassung mit Verweis auf WeChat, da der primäre WeChat-Beitrag nicht direkt zur Prüfung zugänglich war.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://pixverse.ai/ | The Generative Core Behind Digital Worlds and Experiences | PixVerse | 2026-09-04 |
| https://en.tmtpost.com/post/7842608 | PixVerse Releases World's First Real-Time World Model for Interactive Video | TMTPOST | 2026-09-04 |
| https://www.aihub.cn/news/pixverse-v3/ | 爱诗科技发布PixVerse V3，模型能力重磅提高，多种玩法上线 | AIHub | 2026-09-04 |
| https://docs.platform.pixverse.ai/change-logs-906383m0 | Changelogs | PixVerse Platform Docs | 2026-09-04 |
| https://pixverse.ai/en/model/pixverse-v6 | PixVerse V6 AI Video Generator for 1080p Creative Workflows | PixVerse | 2026-09-04 |
| https://docs.platform.pixverse.ai/quick-start-796052m0 | Quick Start | PixVerse Platform Docs | 2026-09-04 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:pixverse`, Thread `public-availability`, 2 datierte Ereignisse 2024-02-09 → 2025-04-29.
- **Praktischer Hinweis:** Bewerten Sie PixVerse Stand 2025-04-29 über die Web-App und den iOS-Eintrag und nicht nur als Homepage-Verweis; prüfen Sie die aktuelle Verfügbarkeit und Funktionen unabhängig.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
