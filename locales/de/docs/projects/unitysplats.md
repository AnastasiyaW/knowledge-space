---
title: "UnitySplats"
category: projects
date: 2026-07-26
tags: [project, unitysplats]
aliases: ["UnitySplats"]
level: 2
source_sha256: a394280ffc62752502069e286d6f86af62a1fb248768030c3fa7f621101896c3
translation: machine
translated_at: '2026-10-24'
---
# UnitySplats {#unitysplats}

**Entwicklungslinie:** `project:unitysplats` · Thread `unitysplats`  
**Letztes Ereignis:** 2026-07-26 · 1 datiertes seit 2026-07-26 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

UnitySplats — ein Unity-6-Paket zum Importieren, Laden und Rendern von 3D-Gaussian-Splats, statt einen Renderer von Grund auf zu entwickeln. Es unterstützt PLY, SOG, SPZ und KHR_gaussian_splatting-GLB; Built-in, URP und HDRP; Laden zur Laufzeit aus Datei, Byte-Array und Stream; GPU- und CPU-Sortierung. Die minimal unterstützte Engine-Version ist Unity 6000.0; WebGL 2 verwendet CPU-Sortierung im Hauptthread und eignet sich nicht für große, unkomprimierte Szenen. Fazit: Einsetzen, wenn ein Unity-Projekt die Wiedergabe mehrerer Splat-Formate benötigt, die Zielhardware und den Rendering-Pfad jedoch benchmarken, bevor man sich für Mobile-, VR- oder Web-Auslieferung festlegt.

## Entwicklungslinie {#development-line}

- **2026-07-26 — Öffentliche Projektreferenzen zu UnitySplats.** Am 2026-07-26 wurde UnitySplats mit einem öffentlichen GitHub-Repository und einer Arloopa-Experience-Seite in Verbindung gebracht. Zusammen etablieren diese datierten Referenzen einen öffentlichen Entwicklungsbezugspunkt für das Projekt.

## Was sich geändert hat {#what-changed}

2026-07-26 — UnitySplats wurde als Open-Source-Unity-Paket vorgestellt; das initiale Release v1.0.0 des verlinkten Repositorys ist auf 2026-07-22 datiert und führte die Basis für Import und Laufzeit-Rendering mehrerer Formate ein. 2026-08-18 — v1.2.0 korrigierte Fehler bei der Tiefenreihenfolge der Direct3D-11-CPU-Sortierung und bei der Viewport-Auswahl.

## Anwendung {#how-to-use-this}

Ab 2026-07-26 können Praktiker das UnitySplats-Repository und die verlinkte Arloopa-Experience als Ausgangspunkte für die Bewertung des Projekts nutzen, sollten vor einer Übernahme jedoch Implementierungsdetails überprüfen.

1. Die OpenUPM-Registry für den Scope com.netpyoung sowie die UnitySplats-Git-Abhängigkeit in Packages/manifest.json hinzufügen oder zuerst Unity.WebP und danach UnitySplats über Git-URLs im Package Manager installieren.
  — <https://github.com/arloopa/UnitySplats>
2. Für URP das Gsplat URP Feature zum aktiven Renderer hinzufügen; für HDRP den Gsplat HDRP Pass in einem Custom Pass Volume vor dem transparenten Rendering hinzufügen.
  — <https://github.com/arloopa/UnitySplats>
3. Eine binäre PLY-, SOG-, SPZ- oder geeignete GLB-Datei in Assets importieren, bei Bedarf den UnitySplats-GLB-Importer wählen und anschließend das erzeugte GsplatAsset in der Szene platzieren.
  — <https://github.com/arloopa/UnitySplats>
4. Für Inhalte zur Laufzeit einen lokalen Pfad mit GsplatRuntimeLoader.LoadFile laden oder URI-Daten mit UnityWebRequest abrufen und die Bytes an GsplatRuntimeLoader.Load übergeben; Unity-Objekte nur im Hauptthread erzeugen und zerstören.
  — <https://github.com/arloopa/UnitySplats>

## Best Practices {#best-practices}

- Unter Android Vulkan und unter Windows Vulkan oder Direct3D 12 bevorzugen; Direct3D 11 und OpenGL verwenden den portablen CPU-Sorter.
  — <https://github.com/arloopa/UnitySplats>
- Spark-gepackte Assets verwenden, um Speicherbedarf zu senken und das Hochladen zu beschleunigen; Uncompressed nur für Fälle reservieren, die exakte Werte im Projekt erfordern.
  — <https://github.com/arloopa/UnitySplats>
- Renderer-übergreifende Sortierung für sich überlappende Spark-Renderer auf kompatiblen Vulkan-, Direct3D-12- und Metal-Zielen aktiviert lassen; auf CPU-Sortierpfaden kann sie keine gemeinsame Reihenfolge liefern.
  — <https://github.com/arloopa/UnitySplats>
- Für WebGL 2 Spark-Kompression und moderate Splat-Anzahlen verwenden, da die Sortierung synchron im Unity-Hauptthread erfolgt und der Browserspeicher begrenzt ist.
  — <https://github.com/arloopa/UnitySplats>

## Abgelöst durch diesen Stand {#superseded-by-this}

- 2026-08-18 — v1.2.0 ersetzt die frühere 16-Bit-Tiefenreihenfolge des Direct3D-11-CPU-Fallbacks und das aus der Main-Kamera abgeleitete Sortierverhalten der Scene-Ansicht.
- 2026-07-22 — v1.1.0 ändert die frühere optionale Renderer-übergreifende Sortierung, indem die Sortierung kompatibler Spark-Renderer standardmäßig aktiviert wird; bestehende Einstellungen werden dabei einmalig migriert.

## Noch unbekannt {#still-unknown}

- In den geprüften Quellen wurde kein primärer Performance-Benchmark für eine bestimmte Splat-Anzahl, Gerätklasse, Frame-Rate-Zielgröße oder XR-Konfiguration gefunden.
- Die ARLOOPA-Experience-URL wurde zusammen mit dem Ereignis angegeben, lieferte während der Recherche jedoch keinen lesbaren Seiteninhalt und wird daher nicht als Beleg verwendet.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/arloopa/UnitySplats | arloopa/UnitySplats — GitHub-Repository und Installationsdokumentation | 2026-09-05 |
| https://raw.githubusercontent.com/arloopa/UnitySplats/main/CHANGELOG.md | UnitySplats-Changelog | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:unitysplats`, Thread `unitysplats`, 1 datiertes Ereignis 2026-07-26 → 2026-07-26.
- **Praktischer Hinweis:** Ab 2026-07-26 können Praktiker das UnitySplats-Repository und die verlinkte Arloopa-Experience als Ausgangspunkte für die Bewertung des Projekts nutzen, sollten vor einer Übernahme jedoch Implementierungsdetails überprüfen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich für das, was veraltet ist.
