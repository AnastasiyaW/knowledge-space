---
title: "MetaHuman"
category: projects
date: 2022-06-10
tags: [metahuman, metahuman-development-and-applications, metahuman_applications, project]
aliases: ["MetaHuman"]
level: 2
source_sha256: cfee1a85a578910e84b8296956887cca055e57d05bff12ebfdf9a655a4523309
translation: machine
translated_at: '2026-10-24'
---
# MetaHuman {#metahuman}

**Entwicklungslinie:** `project:metahuman` · Thread `metahuman-development-and-applications`  
**Letztes Ereignis:** 2022-06-10 · 1 datiertes seit 2022-06-10 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

MetaHuman ist ein Framework für Unreal Engine für Character-Artists, Virtual-Production-Teams und Spieleentwickler.

- Asset-Erstellung: Erstellt bearbeitbare Assets für Gesicht, Körper, Haare, Kleidung und Materialien.
- Mesh-Konformierung: Passt Scans, Sculpts und andere Meshes an einen animationsfähigen MetaHuman an.
- Target-Zusammenstellung: Packt Assets für cineastische oder Echtzeit-Targets.

## Entwicklungslinie {#development-line}

- **2022-06-10 — Ein MetaHuman-Update führte den Import eigener Köpfe ein.** Wir tracken Landmarks auf einem texturierten, individuellen Gesichtsmesh und gleichen es cloudbasiert mit der MetaHuman-Topologie ab. Das System liefert einen vollständig gerigten Charakter. Das Release brachte 23 Grooms, zehn Gesichtsanimations-Loops, sechs Körperposen, fünf Gesichtsposen sowie Kompatibilität mit Rigging und Retargeting in UE5.

## Was sich geändert hat {#what-changed}

- **2022-06-10** — Mesh to MetaHuman wurde im Plugin MetaHuman für Unreal Engine eingeführt. Wir tracken Landmarks auf einem texturierten, individuellen Gesichtsmesh und gleichen es cloudbasiert mit der MetaHuman-Topologie ab. Es liefert einen vollständig gerigten Charakter. Das Release brachte 23 Grooms, zehn Gesichtsanimations-Loops, sechs Körperposen, fünf Gesichtsposen sowie Kompatibilität mit Rigging und Retargeting in UE5.
- **2022-06-21** — Das verlinkte Video kann derzeit weder zuverlässig abgerufen noch identifiziert werden. Daher ist diesem Datum keine Release-Aussage zugeordnet.
- **2023-06-15** — MetaHuman Animator ergänzte die hochpräzise Lösung von Gesichtsperformances, aufgenommen mit einem iPhone oder einer stereoskopischen Head-Mounted-Kamera.
- **2024-03-28** — MetaHuman wurde in UEFN verfügbar. Unreal Engine 5.4 führte den Weg über CLO/Marvelous Designer für dynamische Kleidung ein.
- **2025-06-03** — MetaHuman 5.6 verließ die Early Access und verschob Creator, Animator und Mesh to MetaHuman in Unreal Engine. Es ergänzte parametrische Körper, Outfit Assets, Echtzeit-Animation über unterstützte Kameras oder Audio sowie eine breitere Lizenzierung.
- **2026-06-17** — MetaHuman 5.8 ergänzte Mesh to MetaHuman für den gesamten Körper, MetaHuman Crowds und weitere quelloffene Technologiekomponenten.

## Wie du das nutzt {#how-to-use-this}

Ab dem 2022-06-10 können wir den Workflow für den Import eigener Köpfe in MetaHuman für digitale Menschen evaluieren, statt ihn auf Standard-Charaktervorlagen beschränkt zu betrachten.

1. Installiere Unreal Engine mit MetaHuman Creator Core Data und aktiviere danach das Plugin MetaHuman Creator im Projekt.
  — <https://dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-creator-in-unreal-engine>
2. Erstelle im Content Browser ein Asset vom Typ MetaHuman Character, bearbeite Gesicht, Körper und Materialien und baue es anschließend für das gewünschte Unreal-Target zusammen.
  — <https://dev.epicgames.com/documentation/metahuman/metahuman-creator-in-unreal-engine>
3. Für einen Scan oder Sculpt importierst du das Mesh und erstellst eine MetaHuman Identity. Tracke eine neutrale Pose, führe Identity Solve aus und rigge oder konformiere das Ergebnis anschließend automatisch im Creator-Workflow innerhalb der Engine.
  — <https://dev.epicgames.com/documentation/metahuman/from-mesh>
4. Wenn du einen älteren webbasierten Charakter weiterverwenden willst, nutze den Pfad Migrate bzw. Import and Migrate in Quixel Bridge, statt ihn weiterhin als veraltetes Web-Asset zu bearbeiten.
  — <https://dev.epicgames.com/documentation/metahuman/metahuman-creator-migration-guide-in-unreal-engine>

## Best Practices {#best-practices}

- Verwende ein texturiertes FBX oder OBJ mit sichtbarer Sklera. Wähle OBJ für Meshes mit mehr als 200.000 Vertices, da der FBX-Import deutlich langsamer sein kann.
  — <https://dev.epicgames.com/documentation/metahuman/from-mesh>
- Verwende eine frontale neutrale Pose mit klar erkennbaren Gesichtsmerkmalen. Füge seitliche Aufnahmen nur hinzu, um schlecht passende Ohren oder Nasenlöcher zu korrigieren.
  — <https://dev.epicgames.com/documentation/metahuman/from-mesh>
- Bei eingeschränkten Netzwerken solltest du Epics Texture-Synthesis-, Auto-Rigging- und erforderliche S3-Endpunkte auf die Allowlist setzen, bevor du einen Produktiv-Workflow aufbaust.
  — <https://dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-creator-in-unreal-engine>

## Hierdurch abgelöst {#superseded-by-this}

- 2022-06-09 — Der auf die Web-App zentrierte Workflow von MetaHuman Creator in der Early Access ist für neue Projekte ab UE 5.6 veraltet. Creator ist in Unreal Engine integriert.
- 2025-06-03 — Mesh to MetaHuman erzeugt keinen neuen Charakter mehr in der Webanwendung MetaHuman Creator. Erstelle stattdessen die Identity und konformiere sie in Unreal Engine.

## Weiterhin unbekannt {#still-unknown}

- Die YouTube-URL vom 2022-06-21 konnte nicht abgerufen oder einem Titel, Autor oder Veröffentlichungsdatum zugeordnet werden. Ihr Bezug zur Entwicklungszeitleiste von MetaHuman ist daher nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.fxguide.com/fxfeatured/huge-update-for-metahuman-import-your-own-head/ | Großes Update für MetaHuman: Importiere deinen eigenen Kopf! | 2026-09-05 |
| https://www.metahuman.com/news/new-release-brings-mesh-to-metahuman-to-unreal-engine-and-much-more | Neues Release bringt Mesh to MetaHuman in Unreal Engine und vieles mehr! | 2026-09-05 |
| https://www.metahuman.com/news/delivering-high-quality-facial-animation-in-minutes-metahuman-animator-is-now-available?lang=en-US | Hochwertige Gesichtsanimation in Minuten: MetaHuman Animator ist jetzt verfügbar! | 2026-09-05 |
| https://www.metahuman.com/news/metahuman-comes-to-uefn-dynamic-clothing-with-marvelous-designer-and-more | MetaHuman kommt nach UEFN, dynamische Kleidung mit Marvelous Designer und mehr | 2026-09-05 |
| https://www.metahuman.com/news/metahuman-leaves-early-access-with-a-feature-packed-new-release | MetaHuman verlässt die Early Access mit einem funktionsreichen neuen Release | 2026-09-05 |
| https://forums.unrealengine.com/t/metahuman-5-8-released/2729288 | MetaHuman 5.8 veröffentlicht! | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-creator-in-unreal-engine | Erste Schritte mit MetaHuman Creator in Unreal Engine | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/metahuman-creator-in-unreal-engine | MetaHuman Creator in Unreal Engine | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/from-mesh | From Mesh | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/metahuman-creator-migration-guide-in-unreal-engine | Migrationsleitfaden für MetaHuman Creator in Unreal Engine | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:metahuman`, Thread `metahuman-development-and-applications`, 1 datiertes Ereignis vom 2022-06-10 → 2022-06-10.
- **Praktischer Hinweis:** Ab dem 2022-06-10 können wir beim Planen der Erstellung digitaler Menschen den Workflow für den Import eigener Köpfe in MetaHuman evaluieren, statt ihn auf die Standard-Charaktervorlagen beschränkt zu betrachten.
- **Konfidenz:** hoch. Die datierten Abschnitte „Hierdurch abgelöst“ sind maßgeblich dafür, was veraltet ist.
