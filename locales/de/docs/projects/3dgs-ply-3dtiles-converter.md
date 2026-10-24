---
title: "3DGS-PLY-3DTiles-Converter"
category: projects
date: 2026-08-06
tags: [3dgs-ply-3dtiles-converter, 3dgs_ply_3dtiles_converter, project]
aliases: ["3DGS-PLY-3DTiles-Converter"]
level: 3
source_sha256: 6185a5ceb4c747a0c1d6eb34c90b5c2f5b57152167758f6942ceead9a3f56f14
translation: machine
translated_at: '2026-10-24'
---
# 3DGS-PLY-3DTiles-Converter {#3dgs-ply-3dtiles-converter}

**Entwicklungslinie:** `project:3dgs-ply-3dtiles-converter` · Thread `3dgs-ply-3dtiles-converter`  
**Letztes Ereignis:** 2026-08-06 · 1 datiert seit 2026-08-06 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

3DGS-PLY-3DTiles-Converter ist eine Node.js-CLI, Bibliothek und ESM-Browser-API zur Konvertierung von GraphDECO- oder KHR-nativen Gaussian-Splatting-PLY-Dateien in ein explizites 3D-Tiles-Tileset.

- Adaptive LOD-Kacheln mit SPZ-komprimierten GLB-Dateien.
- Eigenständige PLY-Reduktion ohne Tileset-Erzeugung.
- WGS84-Positionierung und eine Root-Transformationsmatrix.

Die Node.js-CLI erfordert Node.js 18+; die Browser-API läuft in einem Web Worker und gibt MEMORY_EXHAUSTED zurück, wenn der Speicher erschöpft ist.

Der Converter eignet sich für die Auslieferung großer 3DGS-Szenen über 3D Tiles, jedoch ist EXT_splat_opacity kein universell unterstütztes Viewer-Format.

## Entwicklungslinie {#development-line}

- **2026-08-06 — Quellrepository und öffentliche Website des 3DGS-PLY-3DTiles-Converters erfasst.** Am 2026-08-06 wurde der 3DGS-PLY-3DTiles-Converter mit einem GitHub-Quellrepository und einer öffentlichen Vercel-Website erfasst. Dies etabliert einen datierten öffentlichen Bezugspunkt für das Projekt, ohne ein bestimmtes Release, Feature oder Startereignis zu behaupten.

## Was sich geändert hat {#what-changed}

- 2026-08-04 — GitHub Release v0.6.0 fügte eigenständiges Simplify für direkte PLY-Reduktion mit --ratio oder --target-count hinzu; die Überschrift im Changelog datiert dieses Release auf 2026-08-05.
- 2026-08-05 — v0.6.1 fügte die ESM-Browser-API mit lokaler Verarbeitung in einem Web Worker hinzu und erhöhte das Standard-memoryBudget von 3 auf 4 GB; die Überschrift im Changelog datiert das Release auf 2026-08-06.
- 2026-08-06 — v0.6.2 aktivierte EXT_splat_opacity v2 standardmäßig für CLI-, Node.js- und Browser-Konvertierung, mit einer expliziten Opt-out-Möglichkeit.
- 2026-08-28 — v0.6.3 fügte Paket-/Versionsherkunft (Provenance) zu GLB- und Tileset-Ausgaben hinzu und behob erforderliche Gaussian-Splat-Metadaten.
- 2026-08-30 — der Paketindex verzeichnet v0.6.4, jedoch sind primäre Release Notes zu seinem Inhalt nicht verfügbar.
- 2026-08-31 — der Paketindex verzeichnet v0.6.5, jedoch sind primäre Release Notes zu seinem Inhalt nicht verfügbar.

## Anwendung {#how-to-use-this}

1. Installieren Sie das Paket in einem Node.js-18+-Projekt: npm install 3dgs-ply-3dtiles-converter.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
2. Konvertieren Sie eine PLY-Datei: 3dgs-ply-3dtiles-converter scene.ply out_tiles; für CI fügen Sie --no-open-inspector hinzu.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
3. Für Georeferenzierung übergeben Sie entweder --coordinate [lat,long,height] oder --transform mit einer 4×4-Matrix und prüfen source_coordinate_system in build_summary.json.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
4. Wenn wir nur eine reduzierte PLY benötigen, verwenden Sie simplify --ratio 0.5 oder simplify --target-count 250000.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/blob/main/Splat-Simplify.md>

## Bewährte Praktiken {#best-practices}

- Zeigen Sie output_dir nicht auf ein bestehendes Verzeichnis mit wertvollen Daten: Die Standardkonvertierung leert es vor dem Neuaufbau; verwenden Sie --continue für unterbrochene Läufe.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
- Aktivieren Sie EXT_splat_opacity nur für einen verifizierten Pfad mit 3D-Tiles-RendererJS-3DGS-Plugin; andere Viewer können die Erweiterung ignorieren und auf standardmäßiges SPZ zurückfallen.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
- Fixieren Sie die Converter-Version und behalten Sie build_summary.json: v0.6.3 schreibt Paket-/Versionsherkunft und behebt erforderliche Metadaten für Splat-Inhalte.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/releases>
- Für die three.js-Integration erzeugen Sie zuerst 3D Tiles: Das begleitende Renderer-Plugin lädt Tileset- und GLB-Dateien, nicht die ursprüngliche PLY.
  — <https://github.com/WilliamLiu-1997/3D-Tiles-RendererJS-3DGS-Plugin>

## Hiermit ersetzt {#superseded-by-this}

- 2026-08-05 — die Bereitstellung einer separaten Website oder eines separaten Workers für die Browser-Konvertierung ist veraltet: v0.6.1 fügte die ESM-Browser-API mit einem Inline-Web-Worker hinzu.
- 2026-08-06 — Integrationen, die das veraltete Float32-opacityAccessor lesen, müssen auf sourceOpacityAccessor und coverageBoostRatioAccessor v2 umstellen oder den standardmäßigen SPZ-Fallback verwenden.
- 2026-08-28 — bevorzugen Sie für neue Ausgaben v0.6.3+: Sie schreibt stets colorSpace, VEC3-SH-Accessors und erforderliche Opacity-/SH0-Metadaten.

## Weiterhin unbekannt {#still-unknown}

- Primäre GitHub Releases und CHANGELOG enden bei v0.6.3, während der Paketindex v0.6.4 und v0.6.5 am 2026-08-30 bzw. 2026-08-31 auflistet. Primäre Release Notes für diese beiden Versionen sind nicht verfügbar, daher schließen wir ihre Features aus den Empfehlungen aus.
- GitHub Releases und CHANGELOG weichen bei v0.6.0 und v0.6.1 um einen Kalendertag voneinander ab; Release-Zeitstempel enthalten keine Zeitzone. Die obige Zeitleiste verwendet das GitHub-Release-Datum und hält die Abweichung fest.
- Wir konnten https://3dgs-ply-3dtiles-converter.vercel.app/ nicht unabhängig lesen; daher bleiben die aktuellen Features und die Übereinstimmung mit Paket und Browser-API unbestätigt.
- Die chinesischsprachige Suchroute ergab keine primäre chinesischsprachige Quelle und keinen reproduzierbaren Betriebsbericht.
- Eine bestätigte Kompatibilitätsmatrix für Viewer fehlt; nur das begleitende Renderer-Plugin hat eine nachgewiesene Unterstützung für EXT_splat_opacity.
- event_findings im Basisschema ausgelassen?

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter | GitHub — WilliamLiu-1997/3DGS-PLY-3DTiles-Converter | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/blob/main/CHANGELOG.md | GitHub — 3DGS-PLY-3DTiles-Converter CHANGELOG.md | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/releases | GitHub — 3DGS-PLY-3DTiles-Converter Releases | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/blob/main/Splat-Simplify.md | GitHub — Voxelbasierte Gaussian-Splat-Vereinfachung | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3D-Tiles-RendererJS-3DGS-Plugin | GitHub — 3D-Tiles-RendererJS-3DGS-Plugin | 2026-09-07 |
| https://greenflagged.dev/packages/3dgs-ply-3dtiles-converter | Greenflagged — Paketverlauf von 3dgs-ply-3dtiles-converter | 2026-09-07 |

## Agent-Auftrag {#agent-brief}

- **Gegenstand:** `project:3dgs-ply-3dtiles-converter`, Thread `3dgs-ply-3dtiles-converter`, 1 datiertes Ereignis 2026-08-06 → 2026-08-06.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Anwendung und Praktiken oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
