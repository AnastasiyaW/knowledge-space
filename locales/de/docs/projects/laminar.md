---
title: "Laminar"
category: projects

tags: [laminar, laminar-development, project]
aliases: ["Laminar"]
level: 3
source_sha256: a6a945feac985cfd2f98fa1c309efc8dde00c215491e73926a668d1d4b096995
translation: machine
translated_at: '2026-10-24'
---
# Laminar {#laminar}

**Entwicklungslinie:** `project:laminar` · Thread `laminar-development`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Laminar ist eine OpenTelemetry-native Plattform für Entwickler von Agenten und eine Alternative zu Langfuse oder Helicone, kein LLM-Gateway.

- Tracing: LLM- und Tool-Aufrufe nachverfolgen.
- Browser-Sitzungen: interaktive Läufe untersuchen.
- Evaluierungen: Evaluierungsdatensätze ausführen.
- Signals: wiederkehrende Fehler erkennen.
- SQL: Ausführungsdaten direkt abfragen.
- Breakpoints: einen fehlgeschlagenen Lauf erneut abspielen.

Self-Hosting erfordert einen Stack aus mehreren Diensten. Signals erfordert einen Google-Generative-AI-API-Schlüssel.

## Entwicklungslinie {#development-line}

- Wir haben die datierte Zeitleiste noch nicht ausgearbeitet; was wir wissen, steht in den folgenden Abschnitten.

## Was sich geändert hat {#what-changed}

- 2026-03-16 — Laminar kündigte eine Seed-Finanzierungsrunde über 3 Millionen US-Dollar an und positionierte das Produkt rund um das Debugging und Monitoring langlaufender Agenten: Ansichten für Trace-Transkripte, Wiedergabe von Browser-Sitzungen, schrittweiser Debugger, Signals, SQL-Analyse und Evaluierungsdatensätze.
- 2026-03-18 — Die gemeldete Finanzierung betrug 3 Millionen US-Dollar, angeführt von Atlantic.vc mit Beteiligung von Y Combinator, AAL.vc, Ben Sigelman und Ant Wilson; der Produktumfang war Agenten-Observability und kein Modell-Release.
- 2026-07-09 — Release v0.2.1 ergänzte eine überarbeitete Clusters-Oberfläche, einen konfigurierbaren Basispfad für das Frontend, Metadaten zum Ablauf von API-Schlüsseln, CLI-Verbindung im Onboarding sowie Änderungen am Signals-Alerting.

## So wird es verwendet {#how-to-use-this}

Stand 2026-03-18 keine Implementierungs- oder Einführungsänderung vornehmen; zuerst die verlinkte Laminar-Ankündigung, den Zustand des Repositorys und die Modellreferenz prüfen.

1. Ein Projekt und einen Projekt-API-Schlüssel anlegen, das TypeScript-SDK installieren und Laminar.initialize beim Anwendungsstart aufrufen, bevor Modellaufrufe erfolgen.
  — <https://github.com/lmnr-ai/lmnr>
2. Einstiegspunkte von Agenten und relevante Anwendungsfunktionen mit observe umschließen, damit der Trace den Workflow abbildet und nicht nur einen Root-Span.
  — <https://github.com/lmnr-ai/lmnr>
3. Für Python lmnr nur mit den von der Anwendung benötigten Instrumentierungen installieren, es früh beim Start einmalig initialisieren und LMNR_PROJECT_API_KEY über die Umgebung bereitstellen.
  — <https://github.com/lmnr-ai/lmnr-python>
4. Für den kürzesten Weg verwaltetes Hosting wählen oder mit Docker Compose selbst hosten; für Produktionslasten die vollständige Compose-Konfiguration verwenden.
  — <https://github.com/lmnr-ai/lmnr>
5. Traces und Signals prüfen und dann den integrierten SQL-Editor nutzen, um Produktionsbeobachtungen in Datensätze zu überführen und Evaluierungen darauf auszuführen.
  — <https://laminar.sh/blog/2026-03-16-laminar-launch>

## Bewährte Vorgehensweisen {#best-practices}

- Das SDK einmal früh beim Start initialisieren, nicht wiederholt pro Anfrage oder Tool-Aufruf.
  — <https://github.com/lmnr-ai/lmnr-python>
- Ein bestehendes OpenTelemetry-Span-Design beibehalten und dessen OTLP-Exporter auf Laminar richten, statt Instrumentierung zu duplizieren.
  — <https://github.com/lmnr-ai/lmnr/blob/main/frontend/assets/blog/2026-03-05-migrate-from-helicone-to-laminar.mdx>
- Den leichtgewichtigen Docker-Compose-Stack nur für schnelle Starts oder geringe Nutzung verwenden; für Produktion verwaltetes Hosting oder docker-compose-full.yml nutzen.
  — <https://github.com/lmnr-ai/lmnr>
- Laminar nicht als Ersatz für Gateway-Funktionen wie Provider-Routing, Antwort-Caching oder Ratenbegrenzung behandeln.
  — <https://github.com/lmnr-ai/lmnr/blob/main/frontend/assets/blog/2026-03-05-migrate-from-helicone-to-laminar.mdx>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-03-16 — Die ursprüngliche Launch-Beschreibung ist für die Planung des Deployments unvollständig: Das aktuelle Projekt enthält die Änderungen aus Release v0.2.1, darunter konfigurierbare Frontend-Basispfade und Metadaten zum Ablauf von API-Schlüsseln.

## Noch unbekannt {#still-unknown}

- Der mitgelieferte Hugging-Face-Kurzlink konnte nicht abgerufen werden, daher haben wir ihn nicht als Beleg verwendet.
- Das Schema enthielt die Felder event_findings und new_events nicht; wir haben ihre belegbaren Fakten unter Was sich geändert hat aufgenommen.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://laminar.sh/ | Laminar — Open-source observability for AI agents | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr | lmnr-ai/lmnr — Laminar open-source observability platform | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr-python | lmnr-ai/lmnr-python — Laminar Python SDK | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr/releases | lmnr-ai/lmnr releases | 2026-09-05 |
| https://laminar.sh/blog/2026-03-16-laminar-launch | Laminar raised $3M to build observability for long-running agents | 2026-09-05 |
| https://startuprise.co.uk/laminar-raises-3m-seed-round-led-by-atlantic-vc-to-expand-ai-agent-observability/ | Laminar Raises $3M Seed Round Led by Atlantic.vc To Expand AI Agent Observability | 2026-09-05 |
| https://github.com/lmnr-ai/lmnr/blob/main/frontend/assets/blog/2026-03-05-migrate-from-helicone-to-laminar.mdx | Migrate from Helicone to Laminar | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:laminar`, Thread `laminar-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-03-18 keine Implementierungs- oder Einführungsänderung vornehmen; zuerst die verlinkte Laminar-Ankündigung, den Zustand des Repositorys und die Modellreferenz prüfen.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
