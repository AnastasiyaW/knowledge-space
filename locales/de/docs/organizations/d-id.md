---
title: "D-ID — Öffentliche Produktoberflächen"
category: organizations
tags: [d-id, d_id_studio, organization, product_release, public-product-surfaces]
aliases: ["D-ID"]
level: 2
source_sha256: ca2345995e7b1dd0102f835334e0983976f5ba95558ea5de4254026ee9d953ee
translation: machine
translated_at: '2026-10-24'
---
# D-ID — Öffentliche Produktoberflächen {#d-id-public-product-surfaces}

**Entwicklungslinie:** `organization:d-id` · Strang `public-product-surfaces`  
**Ereignisse:** 2 datiert, 2022-08-01 → 2023-03-09 · **Recherchiert:** 2026-09-03 · Konfidenz: mittel

## Was es ist {#what-it-is}

D-ID ist eine Plattform für Teams, die entweder ein generiertes Presenter-Video oder einen Live-Visual-Agenten auf einer Website benötigen. — Erstellt Talking-Avatar-Videos aus Bild, Text oder Audio sowie Videoübersetzung. — Erstellt WebRTC-Agenten mit Avatar, Stimme, LLM-Anweisungen und optionaler RAG-Wissensdatenbank. — Bietet Studio, API, ein Website-Embed und einen Client-SDK. Einschränkung: Die Videoerstellung ist asynchron, während eingebettete Agenten Client-Schlüssel erfordern, die auf freigegebene Domains beschränkt sind. Fazit: Zuerst den Video- oder den Echtzeitpfad wählen; D-ID ist nicht mehr nur eine Demo für sprechende Fotos.

## Entwicklungslinie {#development-line}

- **2022-08-01 — Öffentliche D-ID-Demooberfläche dokumentiert.** Am 2022-08-01 verwies der versiegelte Datensatz auf eine D-ID-Demo, die auf der Create-Subdomain gehostet wurde. Dies etabliert eine öffentlich zugängliche Demonstrationsoberfläche in der Entwicklungslinie des Unternehmens, ohne jedoch die genaue Funktionalität oder den Launch-Status der Demo festzulegen.
- **2023-03-09 — D-ID-Chat-Produktoberfläche dokumentiert.** Am 2023-03-09 verwies der versiegelte Datensatz auf einen D-ID-Chat-Endpunkt auf der Chat-Subdomain. Dies deutet auf eine eigenständige öffentliche Produktoberfläche nach dem früheren Demo-Datensatz hin, legt jedoch weder deren Funktionsumfang, Freigabebedingungen noch das Verhältnis zur Demo fest.

## Was sich geändert hat {#what-changed}

2022-08-01: `create.d-id.com/demo/` war der Einstiegspunkt für die Studio-Demo. Der aktuelle Titel verweist auf Creative Reality Studio, doch der ursprüngliche Demozustand ist nicht mehr prüfbar. 2022-09-19 (heute gefunden): D-ID hat Creative Reality Studio offiziell als Self-Service-Workflow gestartet, um ein einzelnes Bild in ein moderatorgeführtes Video zu verwandeln, und damit das Produkt über die reine Enterprise-Videonachstellung hinaus geöffnet. 2023-03-07 (heute gefunden): D-ID hat die Beta von chat.D-ID gestartet, die den Streaming-Digital-Human mit ChatGPT für persönliche Gespräche kombiniert. 2023-03-09: `chat.d-id.com/` war der dokumentierte Zugangsweg zu diesem Konversationsprodukt; heute leitet er auf die Seite AI Agents von D-ID weiter. 2026-02-04 (heute gefunden): V4 Expressive Avatars wurden in Studio und API verfügbar und fügen die Auswahl der Stimmung für generierte Videos hinzu. Heute: D-ID dokumentiert zwei getrennte Arbeitspfade – asynchrone Videos und Echtzeit-Agenten mit WebRTC, LLM-Konfiguration und RAG-Wissensdatenbanken. Fazit: Die Entwicklungslinie führt von einem Self-Service-Werkzeug für Bild-zu-Presenter zu einer Plattform mit getrennten Produkten für vorab aufgezeichnete Videos und Konversationsagenten.

## Anwendung {#how-to-use-this}

Ab 2022-08-01 konnten Praktiker D-ID über eine öffentliche Demooberfläche evaluieren; ab 2023-03-09 sollten sie den Chat-Endpunkt bei der Bewertung verfügbarer Workflows als eigenständige Produktoberfläche behandeln, vorbehaltlich weiterer Recherche in Primärquellen.

1. Zuerst den Workflow wählen: Videos für asynchrone Avatar-Ausgabe oder Realtime für einen konversationsfähigen visuellen Agenten verwenden.
  — <https://docs.d-id.com/docs/quickstart>
2. Für ein V4-Video eine Avatar-ID und das erforderliche Text- oder Audioskript an den Expressives-Endpunkt senden; optional Stimmung, Hintergrund, Ergebnis-URL oder Webhook festlegen.
  — <https://docs.d-id.com/reference/createv4video>
3. Für einen Agenten diesen mit Presenter, Stimme, LLM-Anbieter/-Modell und Anweisungen erstellen; die zurückgegebene Agenten-ID aufbewahren.
  — <https://docs.d-id.com/docs/agent-quickstart>
4. Den Agenten abrufen, bis sein Status `done` ist, anschließend einen domainbeschränkten Client-Schlüssel erstellen und mit dem Client SDK verbinden, chatten und die Verbindung trennen.
  — <https://docs.d-id.com/docs/agent-session-quickstart>
5. Für eine vorgefertigte Website-Oberfläche das Single-Script-Agents-Embed verwenden; das SDK nur dann einsetzen, wenn die Anwendung eine programmatische Steuerung von Layout und Verhalten benötigt.
  — <https://docs.d-id.com/docs/embed-overview>

## Bewährte Vorgehensweisen {#best-practices}

- `status: done` und die zurückgegebene URL des Idle-Videos als Bereitschaftsprüfung behandeln, bevor Echtzeitsitzungen geöffnet werden.
  — <https://docs.d-id.com/docs/agent-quickstart>
- Jeden Frontend-Client-Schlüssel auf die exakt erlaubten Domains beschränken; er ist nur von diesen Ursprüngen aus gültig.
  — <https://docs.d-id.com/docs/agent-session-quickstart>
- Das Embed für eine Integration mit minimalem Code wählen und das SDK nur dann, wenn die Anwendung umfassendere Kontrolle über UI und Lebenszyklus benötigt.
  — <https://docs.d-id.com/docs/embed-overview>
- Für ein benutzerdefiniertes LLM in der Produktion Streaming verwenden; D-ID dokumentiert Non-Streaming als Debugging-Option, nicht als Produktionsmodus.
  — <https://docs.d-id.com/docs/llms-overview>

## Dadurch überholt {#superseded-by-this}

- 2022-08-01 — Die Rahmung als reine Demo ist für die Produktauswahl veraltet: Die aktuelle D-ID-Dokumentation trennt asynchrone Videos von Echtzeit-Agenten.
- 2023-03-09 — `chat.d-id.com/` als eigenständiger Chat-Einstiegspunkt ist operativ überholt: Die URL leitet nun auf die aktuelle Produktseite AI Agents weiter.
- 2022–2023 — Empfehlungen, die D-ID ausschließlich als Werkzeug für Presenter-Videos aus einem einzelnen Bild beschreiben, sind unvollständig, wenn ein live eingebetteter visueller Agent die eigentliche Anforderung ist.

## Weiterhin ungeklärt {#still-unknown}

- Das Demodatum 2022-08-01 liegt vor der datierten Ankündigung des Studio-Starts von D-ID am 2022-09-19. Die Demo könnte also eine frühe oder eingeschränkte Version gewesen sein und nicht den öffentlichen Start darstellen; der genaue Stand ist nicht verifiziert.
- Der ursprüngliche Seiteninhalt unter `create.d-id.com/demo/` ist heute nicht mehr einsehbar; wiederherstellbar ist nur der aktuelle Titel.
- Die Einträge Studio-Demo und Chat sind unterschiedliche Produktstränge – asynchrones Video bzw. Echtzeit-Konversation – innerhalb von D-ID und nicht verschiedene Unternehmen. Ihr genauer historischer Produktzusammenhang und Zeitplan für die Ablösung lassen sich allein anhand der beiden ursprünglichen URLs nicht rekonstruieren.
- Aktuelle Preise, regionale Verfügbarkeit und Anforderungen an Einwilligungsrichtlinien wurden in dieser Recherche nicht bewertet.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://create.d-id.com/demo/ | D-ID Creative Reality Studio | 2026-09-04 |
| https://chat.d-id.com/ | AI Agents: Create an Interactive Visual Agent | 2026-09-04 |
| https://www.d-id.com/news/d-id-launches-creative-reality-studio-self-service-video-creation-platform-with-hyper-real-ai-presenters/ | D-ID Launches Creative Reality Studio Self-Service Video Creation Platform with Hyper-Real AI Presenters | 2026-09-04 |
| https://www.d-id.com/news/press-release-chat-d-id-enables-anyone-to-talk-face-to-face-with-ai/ | Press Release: chat.D-ID enables anyone to talk face to face with AI | 2026-09-04 |
| https://docs.d-id.com/docs/quickstart | Quickstart | 2026-09-04 |
| https://docs.d-id.com/reference/createv4video | Create a Video | 2026-09-04 |
| https://docs.d-id.com/docs/agent-quickstart | Agents | 2026-09-04 |
| https://docs.d-id.com/docs/agent-session-quickstart | Agent Sessions | 2026-09-04 |
| https://docs.d-id.com/docs/embed-overview | Overview — Agents Embed | 2026-09-04 |
| https://docs.d-id.com/docs/llms-overview | Overview — LLMs | 2026-09-04 |
| https://www.d-id.com/resources/product-updates/expressive-avatars-are-live-in-d-id-studio/ | Expressive Avatars are live in D-ID Studio | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `organization:d-id`, Strang `public-product-surfaces`, 2 datierte Ereignisse 2022-08-01 → 2023-03-09.
- **Praxishinweis:** Ab 2022-08-01 konnten Praktiker D-ID über eine öffentliche Demooberfläche evaluieren; ab 2023-03-09 sollten sie den Chat-Endpunkt bei der Bewertung verfügbarer Workflows als eigenständige Produktoberfläche behandeln, vorbehaltlich weiterer Recherche in Primärquellen.
- **Konfidenz:** mittel. Die datierten Überholungshinweise oben sind maßgeblich dafür, was veraltet ist.
