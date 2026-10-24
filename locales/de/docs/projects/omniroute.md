---
title: "OmniRoute"
category: projects
date: 2026-07-25
tags: [omniroute, project]
aliases: ["OmniRoute"]
level: 2
source_sha256: c70e84768644811a4ba3bedb90c2ca9f1152fd621096324f32e80f3adcda6489
translation: machine
translated_at: '2026-10-24'
---
# OmniRoute {#omniroute}

**Entwicklungslinie:** `project:omniroute` · Thread `omniroute`  
**Letztes Ereignis:** 2026-07-25 · 1 datiertes Ereignis seit 2026-07-25 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

OmniRoute ist ein MIT-lizenziertes Gateway, das Claude Code, Codex, Cursor, Cline und andere Clients über einen einzigen Endpunkt mit Modellanbietern verbindet.

- Anbieter und Modelle: Datenverkehr an vorgelagerte Ziele weiterleiten.
- Fallback- und Combo-Routing: Failover über mehrere Endpunkte hinweg abwickeln.
- Kontingente: Nutzungslimits verfolgen.
- MCP/A2A: Tool- und Agent-Protokolle anbinden.
- Desktop/PWA: lokale und webbasierte Oberflächen betreiben.

Die README nennt für die Linie v3.8.50 352 Anbieter und 1 312 Chat-Modell-IDs. Das System eignet sich für selbst gehostete Bereitstellungen und verwaltet mehrere API-Quellen. Vor der Dimensionierung des Datenverkehrs sollten die Daten zu kostenlosen Kontingenten geprüft werden.

## Entwicklungslinie {#development-line}

- **2026-07-25 — Referenz zum OmniRoute-GitHub-Repository.** Die Unterstützung für Gemini 3.6 flash-high, flash-medium und flash-low wurde über den Antigravity-CLI-Provider ergänzt, wartete jedoch auf das Release v3.8.49. Der Maintainer bestätigte dies am 2026-07-26.

## Was sich geändert hat {#what-changed}

2026-07-25 — Das veröffentlichte v3.8.48 hinkte der Entwicklung hinterher: Die Unterstützung für Gemini 3.6 flash-high, flash-medium und flash-low wurde über den Antigravity-CLI-Provider ergänzt, wartete jedoch auf das Release v3.8.49; der Maintainer bestätigte dies am 2026-07-26. 2026-08-06 — Die Roadmap legte den Übergang von der Linie v3.8.x zu v3.9.0 LTS und dem modularen v4 fest: v3 bleibt die stabile Linie, neue Funktionen wandern nach v4.

## Verwendung {#how-to-use-this}

Ab 2026-07-25 sollten Praktiker das verlinkte OmniRoute-GitHub-Repository als Ausgangspunkt für die Inspektion des Quellcodes nutzen, ohne einen unterstützten Funktionsumfang oder einen Release-Status abzuleiten, bevor das Repository untersucht wurde.

1. Zur Entwicklung aus dem Quellcode das Repository klonen, `npm install`, `npm run build` und `npm start` ausführen; den Entwicklungsserver mit `npm run dev` auf Port 20128 starten.
  — <https://github.com/diegosouzapw/OmniRoute/discussions/8556>
2. Einen kompatiblen Client mit dem OmniRoute-Endpunkt verbinden und Anbieter, Modelle sowie Fallback-Regeln im Dashboard oder in der Projektkonfiguration einrichten.
  — <https://github.com/diegosouzapw/OmniRoute>

## Bewährte Praktiken {#best-practices}

- Ein in Entwicklung befindliches Modell nicht mit der Verfügbarkeit in einem veröffentlichten Release verwechseln: Gemini 3.6 erforderte am 25. Juli das Release/v3.8.49 oder einen Build aus dem Quellcode.
  — <https://github.com/diegosouzapw/OmniRoute/discussions/8556>
- Für den Produktivbetrieb die stabile Linie v3/LTS wählen; Nightly- und Release-Builds nur zum Testen neuer Funktionen verwenden.
  — <https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.51/ROADMAP.md>

## Dadurch überholt {#superseded-by-this}

- 2026-07-25: Die Annahme, dass das veröffentlichte v3.8.48 Gemini 3.6 enthielt, ist veraltet; die Unterstützung existierte nur im kommenden Release/v3.8.49.
- 2026-08-06: Das Hinzufügen aller neuen Funktionen zu v3 wird durch die Aufteilung in stabiles v3/LTS und modulares v4 ersetzt.

## Noch unbekannt {#still-unknown}

- Das vorliegende Schema enthält keine Felder event_findings und new_events. Die Ereignisdetails zum 2026-07-25 und das folgende Ereignis vom 2026-08-06 sind in what_changed gespeichert; die primäre Quelle für die erste Ergänzung ist auf 2026-07-26 datiert.
- Der aktuelle stabile veröffentlichte Release ist durch diese Quellen nicht bestätigt: Das Repository zeigt release/v3.8.51, was allerdings keinen veröffentlichten Release belegt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/diegosouzapw/OmniRoute | OmniRoute-Repository und README | 2026-09-05 |
| https://github.com/diegosouzapw/OmniRoute/discussions/8556 | New Release? — Antwort des Maintainers zu Gemini 3.6 und release/v3.8.49 | 2026-09-05 |
| https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.51/ROADMAP.md | OmniRoute Roadmap | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:omniroute`, Thread `omniroute`, 1 datiertes Ereignis vom 2026-07-25 bis 2026-07-25.
- **Praktischer Hinweis:** Ab 2026-07-25 sollten Praktiker das verlinkte OmniRoute-GitHub-Repository als Ausgangspunkt für die Inspektion des Quellcodes nutzen, ohne einen unterstützten Funktionsumfang oder einen Release-Status abzuleiten, bevor das Repository untersucht wurde.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
