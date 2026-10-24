---
title: "Tutu MCP"
category: projects
date: 2026-06-18
tags: [project, tutu, tutu-mcp, tutu-mcp-development]
aliases: ["Tutu MCP"]
level: 2
source_sha256: 9cec33f279f135cf02b47cb8241816dbf75386e049bd11aae210dd346d6bcbbf
translation: machine
translated_at: '2026-10-24'
---
# Tutu MCP {#tutu-mcp}

**Entwicklungslinie:** `project:tutu-mcp` · Thread `tutu-mcp-development`  
**Letztes Ereignis:** 2026-06-18 · 1 datiertes seit 2026-06-18 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Tutu MCP ist ein Streamable-HTTP-MCP-Endpunkt für Claude, Claude Code, ChatGPT, OpenCode und kompatible Agenten.

- Suche nach Flügen, Zügen, Bussen, S-Bahnen und Hotels.
- Zimmerdetails und Nutzerbewertungen.
- Übergabe an einen Checkout-Link.

Der Server wählt Optionen aus und leitet an den Checkout weiter, nimmt aber keine Zahlungen entgegen. Vor der Zahlung ist die endgültige Buchung auf der Tutu-Seite zu prüfen.

## Entwicklungslinie {#development-line}

- **2026-06-18 — Öffentlicher Tutu-MCP-Endpunkt erwähnt.** Am 2026-06-18 verwies ein Entwicklungsupdate zu Tutu MCP auf den öffentlichen MCP-Endpunkt mcp.tutu.ru/mcp.

## Was sich geändert hat {#what-changed}

- 2026-06-18 — Erkennung von Markenzügen hinzugefügt, einschließlich Lastochka und Doppelstockwagen.
- 2026-06-22 — Tutu kündigte KI-Agenten-Zugriff zur Suche und Buchung von Flügen, Zügen, Bussen, S-Bahnen und Hotels an.
- 2026-08-19 — 2026-08-21 — Tutu veranstaltete um den Server einen Hackathon: 71 Teams nahmen teil, 42 reichten Projekte ein. Dadurch wurden Frontend- und Agenten-Szenarien erweitert, ohne den bestätigten Endpunktvertrag zu verändern.

## Wie dies zu nutzen ist {#how-to-use-this}

Ab dem 2026-06-18 sollten Praktiker https://mcp.tutu.ru/mcp als öffentlichen Tutu-MCP-Endpunkt betrachten, den es zu evaluieren oder zu integrieren gilt, wobei Protokoll und Zugriffsanforderungen zu bestätigen sind.

1. Den Endpunkt `https://mcp.tutu.ru/mcp` als Remote-Streamable-HTTP-MCP ohne Authentifizierung hinzufügen.
  — <https://mcp.tutu.ru/mcp>
2. In Claude Code `claude mcp add --transport http tutu https://mcp.tutu.ru/mcp` ausführen.
  — <https://mcp.tutu.ru/mcp>
3. Abfahrts- und Zielstädte, Daten, Budget, Verkehrsart und Limits an den Agenten übergeben; Routen nach Preis und Fahrzeit vergleichen.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>
4. Endgültige Bedingungen prüfen und die Buchung auf Tutu abschließen; Drittanbieter-Apps dürfen keine Zahlung anstelle von Tutu annehmen.
  — <https://github.com/chemisttt/tutu-mcp-kit>

## Bewährte Praktiken {#best-practices}

- Den Endpunkt nicht im Browser als API öffnen: Für Browser-Clients einen Same-Origin-Proxy verwenden, damit CORS die Anfragen nicht blockiert.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>
- Wenn der Live-MCP leere Ergebnisse liefert, keine Mock-Angebote einsetzen: Den leeren Zustand anzeigen oder den Fehler diagnostizieren.
  — <https://github.com/chemisttt/tutu-mcp-kit>
- Bei geteilten Reisen Transport und Hotels getrennt abfragen, Ergebnisse deduplizieren und Checkout-Links ausschließlich aus der zurückgegebenen `checkout_ref` erzeugen.
  — <https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md>

## Durch Folgendes ersetzt {#superseded-by-this}

- 2026-07-16 — Die Registrierung des Passagierwarenkorbs und einmalige Checkout-Links ersetzten den Ablauf, bei dem der Agent auf der Seite zur Dateneingabe stoppte. Das Datum stammt aus einer Sekundärmeldung und muss durch eine Primärquelle bestätigt werden.

## Weiterhin unbekannt {#still-unknown}

- Das Antwortschema enthält die Felder `event_findings` und `new_events` nicht; Entwicklungsupdates bleiben unter `what_changed`, ohne nicht belegte Felder.
- Eine Sekundärquelle bestätigt die Erkennung von Markenzügen für das Update vom 2026-06-18, ihr Veröffentlichungsdatum war jedoch nicht verfügbar.
- Für die Veröffentlichungsstatus vom 2026-06-23, 2026-07-01, 2026-07-08, 2026-07-09 und 2026-07-16 wurde keine datierte Primärquelle von Tutu gefunden; sie bleiben daher als Produktchronologie unbestätigt.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://mcp.tutu.ru/mcp | Tutu MCP — ИИ спланирует поездку за вас | 2026-09-05 |
| https://companies.rbc.ru/news/Q1Aa56ondv/servis-puteshestvij-tutu-otkryil-bronirovanie-poezdok-cherez-ii-agentov/ | Сервис путешествий Туту открыл бронирование поездок через ИИ-агентов | 2026-09-05 |
| https://hackathon2026.tutu.ru/ | ИИ-хакатон — Туту MCP | 2026-09-05 |
| https://github.com/chemisttt/tutu-mcp-kit/blob/main/docs/MCP.md | tutu-mcp-kit: MCP operator guide | 2026-09-05 |
| https://github.com/chemisttt/tutu-mcp-kit | chemisttt/tutu-mcp-kit | 2026-09-05 |

## Agentenbriefing {#agent-brief}

- **Gegenstand:** `project:tutu-mcp`, Thread `tutu-mcp-development`, 1 datiertes Ereignis 2026-06-18 → 2026-06-18.
- **Praktischer Hinweis:** Ab dem 2026-06-18 sollten Praktiker https://mcp.tutu.ru/mcp als öffentlichen Tutu-MCP-Endpunkt betrachten, den es zu evaluieren oder zu integrieren gilt, wobei Protokoll und aktuelle Zugriffsanforderungen eigenständig zu bestätigen sind.
- **Konfidenz:** mittel. Für die Frage, was überholt ist, gelten die datierten Ersetzungen oben als maßgeblich.
