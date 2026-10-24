---
title: "Worldstream: worldstream-3d-world-model — Worldstream 3D-Weltmodell"
category: "projects"
date: 2026-10-22
tags: ["project", "worldstream", "worldstream-3d-world-model"]
aliases: ["Worldstream: worldstream-3d-world-model"]
level: 2
source_sha256: d5a9f393de0d1517398397cba41e924c1aa7cce97939833c6d99ceae9fd71ebd
translation: machine
translated_at: '2026-10-24'
---
# Worldstream: worldstream-3d-world-model — Worldstream 3D-Weltmodell {#worldstream-worldstream-3d-world-model-worldstream-3d-world-model}

**Entwicklungslinie:** project:worldstream · Thread worldstream-3d-world-model  
**Letztes Ereignis:** 2026-10-22 · 2 datierte Einträge seit 2026-10-22 · **Recherchiert:** 2026-10-23 · Konfidenz: hoch

## Was es ist {#what-it-is}

WorldStream ist eine offene, interaktive 3D-Weltmodell-Architektur. Sie richtet sich an Forscher im Bereich Simulation und an Entwickler virtueller Umgebungen.

Funktionen:

- Terrain-Streaming: erzeugt kontinuierliches 3D-Terrain über die Grenzen einer vordefinierten Karte hinaus.
- Hierarchische Planung: eine Makroebene legt Ökologie und Verkehr fest, eine Mikroebene kompiliert einzelne Kacheln.
- Prozedurale Kompilierung: deterministischer Code wandelt strukturierte Entscheidungen in Terrain, Straßen, Vegetation, Siedlungen und Entitäten um.
- Sprachsteuerung: offene natürlichsprachliche Anweisungen verändern die Welt und steuern Entitäten darin.
- Persistenz: Nutzeränderungen, Randverpflichtungen und zustandsbehaftete NPC-Datensätze bleiben erhalten, wenn Kacheln entladen und wieder geladen werden.

Durchsatz und räumliche Konsistenz hängen von zwei Faktoren ab: einer präzisen Vorhersage des Bewegungskorridors und begrenzten Budgets für die prozedurale Kompilierung. WorldStream ist eine praktikable strukturierte Alternative zu Black-Box-Video- oder Voxel-Generierung, da es symbolische Planung mit deterministischer Grafikkompilierung verbindet.

## Entwicklungslinie {#development-line}

- **2026-10-22 — WorldStream: streamingfähiges interaktives 3D-Weltmodell mit hierarchischer Planung.** Forschende haben WorldStream vorgestellt, ein offenes 3D-Weltmodell. Es erweitert spielbares Terrain über vorab festgelegte Karten hinaus, reagiert auf offene Sprachanweisungen in der laufenden Welt und stellt besuchte Orte mitsamt ihren Änderungen wieder her. Ein hierarchischer Planer (Makro- und Mikrostufe) übergibt seine Pläne an deterministischen lokalen Code, der sie zu Terrain, Straßen, Siedlungen, Vegetation und Entitäten kompiliert. Das Streaming-Design plant voraus entlang des vorhergesagten Bewegungskorridors.
- **2026-10-22 — WorldStream als offenes interaktives 3D-Weltmodell eingeführt.** Ein Preprint mit Datum 2026-10-22 stellt WorldStream vor. Das Modell erweitert spielbares Terrain über eine vordefinierte Karte hinaus, reagiert auf offene Sprachanweisungen und stellt besuchte Regionen mitsamt ihren Änderungen wieder her. Der hierarchische Planer gibt strukturierte Entscheidungen für Terrain, Siedlungen und Entitäten aus. Das Streaming kompiliert nur die Regionen, die bald benötigt werden. Ein persistenter Welt-Datensatz speichert Änderungen und zustandsbehaftete NPCs.
- **2026-10-22 — weitere Berichterstattung zu diesem Datum.**
  - Die Arbeit legt fest, dass der hierarchische Planer auf einem typisierten Entscheidungsmodell arbeitet. Die Makroplanung umfasst Gruppen räumlicher Kacheln und legt die globale ökologische, hydrologische und verkehrstechnische Topologie fest. Die Mikroplanung spezialisiert diese Vorgaben auf das gemessene lokale Terrain und auf Randverpflichtungen gegenüber benachbarten Kacheln. Geometrie hinter dem vorhergesagten Bewegungskorridor des Spielers wird aktiv entladen, sodass der Speicherbedarf innerhalb eines begrenzten Budgets bleibt. (2026-10-22) — <https://arxiv.org/abs/2610.28827>
  - Die Arbeit beschreibt, dass der persistente Welt-Datensatz pro Kachel geführt wird. Er speichert Seeds, veränderliche Entitätsidentitäten und Randverpflichtungen zusammen mit Nutzeränderungen an Attributen. Eine zurückkehrende Kachel wird aus diesen strukturierten Datensätzen neu kompiliert, nicht neu inferiert und nicht als schweres Roh-Mesh gespeichert. (2026-10-22) — <https://arxiv.org/abs/2610.28827>

## Was sich geändert hat {#what-changed}

Die erste Forschungsarbeit begründete das zentrale WorldStream-Framework. Sie verlagert die Erzeugung offener Welten von monolithischer Offline-Synthese hin zu entkoppelter Streaming-Ausführung. Die Architektur führt ein:

- zweistufige hierarchische Planung über Kachelcluster und lokale Zellen;
- deterministische prozedurale Kompilierung zur Reduzierung des Speicherbedarfs;
- zustandsbehaftete Persistenz pro Kachel, sodass Änderungen erhalten bleiben, wenn eine Region erneut besucht wird.

## Anwendung {#how-to-use-this}

1. Globale Generierungs-Seeds und Umweltpriors setzen. Sie initialisieren die Makroplanungsschicht für regionale Ökologie, Hydrologie und Verkehrsnetze.
  — <https://arxiv.org/abs/2610.28827>
2. Position und Blickrichtungsvektoren des Agenten übergeben, um den Bewegungskorridor zu projizieren. Dies löst die Mikroplanung für die als Nächstes anstehenden Kacheln im Voraus aus.
  — <https://arxiv.org/abs/2610.28827>
3. Lokale deterministische prozedurale Kompilierung ausführen. Sie wandelt freigegebene Entscheidungen der Mikroplanung in darstellbare 3D-Terrain-, Vegetations- und Siedlungsassets um.
  — <https://arxiv.org/abs/2610.28827>
4. Natürlichsprachliche Befehle absetzen, um Laufzeitentitäten oder Kachelattribute zu aktualisieren. Geänderte Zustände werden in der Datenbank des persistenten Welt-Datensatzes pro Kachel gespeichert.
  — <https://arxiv.org/abs/2610.28827>

## Best Practices {#best-practices}

- Planungshorizonte getrennt von der Geometriekompilierung entlang der vorhergesagten Korridore halten, damit die Bildraten stabil bleiben und die Rechenlast nicht sprunghaft ansteigt.
  — <https://arxiv.org/abs/2610.28827>
- In der Mikroplanung strikte Randverpflichtungen zwischen Kacheln durchsetzen, damit unabhängig kompilierte Zellen keine visuellen oder topologischen Nähte zeigen.
  — <https://arxiv.org/abs/2610.28827>
- Legt der Agent große Strecken zurück, aus den Seed- und Änderungsdatensätzen pro Kachel neu kompilieren, statt hochpolygonige Meshes im Speicher zwischenzuspeichern.
  — <https://arxiv.org/abs/2610.28827>

## Dadurch abgelöst {#superseded-by-this}

- Monolithische Offline-Generierung von 3D-Welten, die Simulationen auf statische, vorab berechnete Karten ohne dynamisches, unendliches Streaming beschränkt.
  — <https://arxiv.org/abs/2610.28827>
- Zustandsloses Streaming, das Nutzeränderungen am Terrain und die Historie von NPC-Interaktionen verwirft, sobald eine Kachel entfernt wird.
  — <https://arxiv.org/abs/2610.28827>

## Weiterhin unbekannt {#still-unknown}

- Unabhängige externe Laufzeit-Benchmarks und die Verfügbarkeit des Open-Source-Codes sind nicht verifiziert, bis ein öffentliches Repository veröffentlicht wird.
- Community-Evaluierungen und Praxisberichte liegen noch nicht vor; der Preprint wurde am 22. Oktober 2026 veröffentlicht.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://arxiv.org/abs/2610.28827 | WorldStream: Streaming Interactive 3D Worlds with Hierarchical Planning and Persistent State | 2026-10-23 |

## Agenten-Kurzfassung {#agent-brief}

- **Thema:** project:worldstream, Thread worldstream-3d-world-model, 2 datierte Ereignisse vom 2026-10-22 bis 2026-10-22.
- **Praxishinweis:** Siehe die oben belegten Abschnitte zu Anwendung und Praxis, einschließlich ihrer Grenzen.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
