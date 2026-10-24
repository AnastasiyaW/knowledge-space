---
title: "OpenWorker — Projekteinführung"
category: projects
date: 2026-08-05
tags: [openworker, project, project-introduction]
aliases: ["OpenWorker"]
level: 1
source_sha256: 4cbf9c27a12925f94c0e57bc421b1a33c9e47dc6358eaa9364e9ce933dd2c2fb
translation: machine
translated_at: '2026-10-24'
---
# OpenWorker — Projekteinführung {#openworker-project-introduction}

**Entwicklungslinie:** `project:openworker` · Thread `project-introduction`  
**Letztes Ereignis:** 2026-08-05 · 1 datiertes Ereignis seit 2026-08-05 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

OpenWorker ist ein MIT-lizenzierter Desktop-KI-Coworker mit einem lokalen Python-Agent-Server und einer Tauri/React-GUI. Er unterstützt eigene Modelle (Bring-your-own-Models) und mehr als 25 Integrationen.

- Dokumente und Berichte: erzeugt sie aus Dateien, Slack und Automatisierungen.
- Leitplanken: verlangt eine Freigabe für riskante Aktionen.

Der Status ist Open Beta. Der Windows-Build hat keine Authenticode-Signatur.

## Entwicklungslinie {#development-line}

- **2026-08-05 — OpenWorker wurde öffentlich über sein GitHub-Repository referenziert.** Am 2026-08-05 verwies der erfasste Link auf das OpenWorker-GitHub-Repository und die biografische Seite von Andrew Ng. Das belegt einen datierten öffentlichen Bezugspunkt für das Projekt. Die Links allein bestätigen weder ein Release, einen Funktionsumfang noch einen Betriebsstatus.

## Was sich geändert hat {#what-changed}

2026-08-05 — Der erfasste Link verwies auf ein eigenständiges OpenWorker-Repository. Die Primärquelle zeigt kein an diesem Tag datiertes Release und keine Ankündigung.

2026-08-24 — v0.2.0 ergänzte Skills, sitzungsübergreifendes Gedächtnis, drei Security-Coworker und einen reviewer-basierten Auto-Approve. Außerdem wurde die MCP-Konfiguration verbessert, und Fehler bei Freigabe und Sicherheit wurden behoben.

2026-08-25 — v0.2.1 fügte Ox Alpha über OpenRouter zur Auswahl hinzu, mit 1M Token Kontext und Tool-Calling.

## Verwendung {#how-to-use-this}

Beginnen Sie mit dem OpenWorker-GitHub-Repository in dem Stand vom 2026-08-05. Betrachten Sie Funktionsumfang und Release-Status als ungeprüft, bis wir Belege im Repository geprüft haben.

1. Den macOS- oder Windows-Build installieren, die Anwendung öffnen und einen API-Schlüssel eines Anbieters oder ein lokales Ollama verbinden.
  — <https://github.com/andrewyng/openworker>
2. Ordnerzugriff nur im erforderlichen Modus gewähren und das gewünschte Ergebnis in einfacher Sprache beschreiben. Artefakte werden standardmäßig in einem temporären Arbeitsbereich gespeichert.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>
3. Eine Automatisierung für wiederkehrende Arbeit anlegen. Sie läuft, solange die Anwendung geöffnet bleibt. Daher den Start bei der Anmeldung aktivieren, damit sie im Hintergrund ausgeführt wird.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>
4. Einen MCP-Server über Manage → Integrations verbinden und anschließend die Freigabesteuerung für seine Tools festlegen.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>

## Best Practices {#best-practices}

- Mit einem eingeschränkten Ordner beginnen und Shell-Befehle sowie Schreibvorgänge außerhalb der gewährten Verzeichnisse freigeben. Eine lokal-first-Konfiguration nicht mit null Datenübertragung an den gewählten Modellanbieter verwechseln.
  — <https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md>
- Bei unbeaufsichtigten Automatisierungen einen Menschen im Freigabe-Posteingang belassen, damit unbeaufsichtigte Läufe nicht ihre eigenen Nebenwirkungen freigeben.
  — <https://github.com/andrewyng/openworker>
- Unter Windows mit einer SmartScreen-Warnung rechnen, da aktuelle Builds nicht code-signiert sind.
  — <https://github.com/andrewyng/openworker>

## Abgelöst durch diesen Stand {#superseded-by-this}

- 2026-08-24 — OpenWorker ist nicht mehr nur ein generischer Desktop-Coworker: v0.2.0 ergänzte Skills, Projektgedächtnis, Security-Coworker und einen Auto-Approve-Reviewer.
- 2026-08-25 — Die ursprüngliche Modellliste ist veraltet: v0.2.1 ergänzte Ox Alpha über OpenRouter mit beanspruchtem 1M Token Kontext.

## Weiterhin unbekannt {#still-unknown}

- Das Antwortschema enthält keine Felder event_findings und new_events. Daher stehen neue datierte Fakten in what_changed.
- Es wurde keine am 2026-08-05 veröffentlichte Primärquelle gefunden, die verifizierbare Details zu diesem Schritt selbst ergänzt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/andrewyng/openworker | andrewyng/openworker — README | 2026-09-05 |
| https://github.com/andrewyng/openworker/releases/tag/v0.2.0 | OpenWorker v0.2.0 — GitHub Release | 2026-09-05 |
| https://github.com/andrewyng/openworker/releases | OpenWorker releases — GitHub | 2026-09-05 |
| https://github.com/andrewyng/aisuite/blob/main/docs/openworker-quickstart.md | OpenWorker-Schnellstart — aisuite-Dokumentation | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:openworker`, Thread `project-introduction`, 1 datiertes Ereignis 2026-08-05 → 2026-08-05.
- **Praxishinweis:** Ab dem 2026-08-05 vom OpenWorker-GitHub-Repository ausgehen. Fähigkeiten und Release-Status als ungeprüft behandeln, bis wir Repository-Belege geprüft haben.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
