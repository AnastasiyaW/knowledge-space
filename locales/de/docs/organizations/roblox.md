---
title: "Roblox"
category: organizations
date: 2026-02-05
tags: [model_releases, organization, roblox, roblox-ai, roblox-ai-creation]
aliases: ["Roblox"]
level: 2
source_sha256: d3b73c7600218dfd36b3e274e4dc3066248989fa0262e0d6f47076969f50d0fa
translation: machine
translated_at: '2026-10-24'
---
# Roblox {#roblox}

**Entwicklungslinie:** `organization:roblox` · Thread `roblox-ai-creation`  
**Letztes Ereignis:** 2026-02-05 · 2 datierte seit 2023-02-18 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Roblox ist eine Gaming-Plattform und Roblox Studio für Entwickler; in dieser Linie bietet Cube Folgendes: — lokales Cube 3D v0.5 zur Generierung von OBJ aus Text; — GenerationService für statische Body1- oder zusammengesetzte Car5-Modelle direkt im Erlebnis; — CubePart für benannte Teile für Spielcode. Lokale Fast-Inference erfordert 24 GB VRAM, die reguläre Variante 16 GB; 4D Generation befindet sich weiterhin in der Beta, und die aktuellen Dokumente beschreiben ausdrücklich Car5 und Body1. Fazit: Verwenden Sie GenerationService für Roblox-Objekte mit vorab entworfenem Schema, und Cube 3D v0.5 für lokale Prototypen, nicht für einen versprochenen, aber noch nicht nachgewiesenen Generator beliebiger Szenen.

## Entwicklungslinie {#development-line}

- **2023-02-18 — Wired berichtet über Robloxs Ausrichtung auf generative KI.** Am 2023-02-18 veröffentlichte Wired einen Bericht, der Roblox mit generativer KI und seinem Gaming-Universum in Verbindung bringt. Die datierte verlinkte Quelle markiert einen frühen öffentlichen Meilenstein in Robloxs Entwicklungsrichtung für generative KI, wobei die vorliegenden Belege kein bestimmtes veröffentlichtes Produkt oder keine bestimmte Fähigkeit belegen.
- **2026-02-05 — Roblox treibt die Erstellung mit dem Cube Foundation Model voran.** Das Schema legt die Teile fest, und die Skripte passen sich an deren Größe und Form an.

## Was sich geändert hat {#what-changed}

2023-02-18 — Roblox testete die Eingabe in natürlicher Sprache zur Erstellung und Änderung von Code, Aussehen und Verhalten von Spielobjekten; dies war eine frühe experimentelle Linie. 2025-03-17 — Roblox stellte Cube 3D v0.1 vor und machte es als Open Source verfügbar: Modell und Startcode für Text-to-Shape sowie Beta-Mesh-Generation in Studio und über die Lua-API. 2025-07 (heute gefunden) — Cube 3D v0.5 wurde zum aktuellen Standard des Repositorys; Textübereinstimmung und Steuerung der Bounding Box wurden verbessert. 2026-02-05 — 4D Generation beta verlagerte den Schwerpunkt von statischen Meshes auf funktionale, mehrteilige Modelle: Das Schema legt die Teile fest, und die Skripte passen sich an deren Größe und Form an. 2026-05-28 (heute gefunden) — CubePart ergänzte die Generierung und Segmentierung benannter Teile anhand eines offenen, benutzerdefinierten Schemas; der direkte Zugriff in Studio ist weiterhin als zukünftig angekündigt.

## Anwendung {#how-to-use-this}

Stand 2026-02-05 sollten Praktiker, die Roblox-Werkzeuge zur Erstellung evaluieren, Roblox Cube als separat dokumentierten Foundation-Model-Weg behandeln und für aktuelle Zugangs- und Nutzungsdetails die verlinkten offiziellen Ressourcen sowie die GitHub- und Hugging-Face-Seiten konsultieren.

1. Verwenden Sie für ein Objekt innerhalb von Roblox `GenerationService:GenerateModelAsync` mit `TextPrompt` und einem Schema; beginnen Sie mit den dokumentierten `Car5` bzw. `Body1`.
  — <https://create.roblox.com/docs/reference/engine/classes/GenerationService>
2. Verarbeiten Sie das Ergebnis über `pcall`, skalieren und positionieren Sie danach das Modell, fixieren Sie dessen Teile und binden Sie erst anschließend das Spielverhalten an.
  — <https://create.roblox.com/docs/reference/engine/classes/GenerationService>
3. Für lokales Text-zu-3D klonen Sie `Roblox/cube`, installieren die Abhängigkeiten in einer virtuellen Umgebung, laden die Gewichte `Roblox/cube3d-v0.5` herunter und führen `cube3d.generate` aus; das Ergebnis wird als OBJ gespeichert.
  — <https://github.com/Roblox/cube>
4. Wenn das Objekt zu einem vorgegebenen Maß passen muss, übergeben Sie `--bounding-box-xyz`; zur Prüfung des visuellen Ergebnisses verwenden Sie die Beispiele des Repositorys oder ein Turntable-Rendering.
  — <https://github.com/Roblox/cube>

## Best Practices {#best-practices}

- Entwerfen Sie zuerst ein Schema aus den Namen der Teile, von denen der Spielcode abhängt; bei einem Fahrzeug sind das Karosserie und einzelne Räder, nicht ein einziges monolithisches Mesh.
  — <https://about.roblox.com/newsroom/2026/05/cubepart-roblox-open-vocabulary-part-controllable-3d-generator>
- Beginnen Sie neue lokale Integrationen mit Cube 3D v0.5, und belassen Sie v0.1 nur zur Reproduktion älterer Ergebnisse.
  — <https://github.com/Roblox/cube>
- Planen Sie mindestens 16 GB VRAM ein, für `--fast-inference` 24 GB; bei langsamer Dekodierung reduzieren Sie `resolution-base` in den Bereich 4.0–9.0.
  — <https://github.com/Roblox/cube>
- Setzen Sie keine extremen Bounding Boxes ohne Prüfung: v0.5 kann getrennte oder diagonal verlaufende Komponenten liefern.
  — <https://github.com/Roblox/cube>
- Veröffentlichen Sie ein CubePart-Ergebnis nicht ohne Prüfung von Überschneidungen und räumlichen Beziehungen der Teile: Roblox weist ausdrücklich darauf hin, dass Overlap und die Unterscheidung von Richtungen noch verbessert werden müssen.
  — <https://about.roblox.com/newsroom/2026/05/cubepart-roblox-open-vocabulary-part-controllable-3d-generator>

## Durch diesen Stand überholt {#superseded-by-this}

- 2023-02-18 — sich an dem frühen Experiment zur Generierung von Code und Objekten in natürlicher Sprache als funktionierendem Vertrag zu orientieren, ist überholt; es wurde durch die dokumentierten Cube- und GenerationService-Funktionen ersetzt.
- 2025-03-17 — Cube 3D v0.1 als aktuellen Standard zu verwenden, ist mit der Veröffentlichung von Cube 3D v0.5 im Juli 2025 überholt.
- 2025-03-17 — nur einen statischen Single-Mesh-Workflow anzunehmen, ist für die Roblox-Integration überholt: 4D beta ergänzte Car5 und Body1, hat aber keinen allgemeinen, beliebigen Schema-Workflow nachgewiesen.
- 2026-09-04 — `GenerationService:GenerateMeshAsync` ist als deprecated markiert; neue Integrationen sollten `GenerateModelAsync` verwenden.

## Weiterhin ungeklärt {#still-unknown}

- 4D Generation ist als Beta gekennzeichnet; die aktuellen Quellen bestätigen weder die regionale oder kontobezogene Verfügbarkeit noch Kontingente oder Kosten für ein bestimmtes Erlebnis.
- Der unternehmensweite AI Assistant und die Modell-API-Linie von Cube hängen zusammen, bilden aber keine vollständige Liste der KI-Funktionen von Roblox; die praktischen Schritte oben beziehen sich nur auf Cube, CubePart und GenerationService.
- CubePart ist als künftige Funktion von Roblox Studio angekündigt, die gefundenen Quellen nennen jedoch weder ein Datum für einen öffentlichen Studio-Release noch eine eigene Studio-API.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://www.wired.com/story/roblox-generative-ai-gaming-universe/ | Roblox Is Bringing Generative AI to Its Gaming Universe | WIRED | 2026-09-04 |
| https://about.roblox.com/newsroom/2025/03/introducing-roblox-cube | Introducing Roblox Cube: Our Core Generative AI System for 3D and 4D | Roblox | 2026-09-04 |
| https://about.roblox.com/newsroom/2026/02/accelerating-creation-powered-roblox-cube-foundation-model | Accelerating Creation, Powered by Roblox’s Cube Foundation Model | Roblox | 2026-09-04 |
| https://github.com/Roblox/cube | Cube: Generative AI System for 3D | 2026-09-04 |
| https://huggingface.co/Roblox/cube3d-v0.1 | Roblox/cube3d-v0.1 · Hugging Face | 2026-09-04 |
| https://about.roblox.com/newsroom/2026/05/cubepart-roblox-open-vocabulary-part-controllable-3d-generator | CubePart: An Open-Vocabulary Part-Controllable 3D Generator | Roblox | 2026-09-04 |
| https://create.roblox.com/docs/reference/engine/classes/GenerationService | GenerationService | Documentation - Roblox Creator Hub | 2026-09-04 |
| https://create.roblox.com/docs/zh-cn/parts/model-generation | Modellgenerierung | Dokumentation - Roblox Creator Hub | 2026-09-04 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `organization:roblox`, Thread `roblox-ai-creation`, 2 datierte Ereignisse 2023-02-18 → 2026-02-05.
- **Praktischer Hinweis:** Stand 2026-02-05 sollten Praktiker, die Roblox-Werkzeuge zur Erstellung evaluieren, Roblox Cube als separat dokumentierten Foundation-Model-Weg behandeln und für aktuelle Zugangs- und Nutzungsdetails die verlinkten offiziellen Ressourcen sowie die GitHub- und Hugging-Face-Seiten konsultieren.
- **Konfidenz:** hoch. Die datierten Überholungsangaben oben sind maßgeblich dafür, was veraltet ist.
