---
title: "RealityScan — Start und Veröffentlichung der mobilen Photogrammetrie"
category: projects
date: 2022-12-05
tags: [mobile-photogrammetry-launch-and-release, project, realityscan, realityscan_beta_launch]
aliases: ["RealityScan"]
level: 2
source_sha256: dc4c6666a73a7a7f2b5b83e9e3d20934902e59c9250a01ef11514013b1c2046e
translation: machine
translated_at: '2026-10-24'
---
# RealityScan — Start und Veröffentlichung der mobilen Photogrammetrie {#realityscan-mobile-photogrammetry-launch-and-release}

**Entwicklungslinie:** `project:realityscan` · Strang `mobile-photogrammetry-launch-and-release`  
**Letztes Ereignis:** 2022-12-05 · seit 2022-04-04 2 datierte Ereignisse · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

RealityScan ist ein Werkzeug für Ersteller von 3D-Assets: Die mobile App nimmt ein Objekt in einer Serie von Fotos auf und verarbeitet das Modell in der Cloud, die Desktop-Version arbeitet mit Fotos und Laserscans. Die mobile Version setzt iOS 16+ oder Android 7+ mit ARCore voraus; die Desktop-Version ist bis zu einem Jahresumsatz von 1 Mio. $ kostenlos. Fazit: Für die schnelle Erfassung von Objekten eignet sich die mobile Version, für präzise Aufnahmen und große Datensätze wird RealityScan Desktop benötigt.

## Entwicklungslinie {#development-line}

- **2022-04-04 — RealityScan Beta wurde vorgestellt.** Die begrenzte Beta der mobilen RealityScan-App startete — 10 000 TestFlight-Plätze, Verarbeitung von Fotos zu einem 3D-Modell und Export über Sketchfab.
- **2022-12-05 — RealityScan wurde öffentlich verfügbar.** Die App verließ die Beta als kostenlose iOS/iPadOS-Version; zum Zeitpunkt der Veröffentlichung wurde Android noch nicht unterstützt.

## Was sich geändert hat {#what-changed}

2022-04-04: Die begrenzte Beta der mobilen RealityScan-App startete — 10 000 TestFlight-Plätze, Verarbeitung von Fotos zu einem 3D-Modell und Export über Sketchfab. 2022-12-05: Die App verließ die Beta als kostenlose iOS/iPadOS-Version; zum Zeitpunkt der Veröffentlichung wurde Android noch nicht unterstützt. 2023-06-20: Die mobile Version wurde auf Android verfügbar und erhielt einen schrittweisen Workflow; Epic meldete mehr als 200 000 Downloads der iOS-Version. 2024-06-24: RealityScan Mobile 1.5 ergänzte den lokalen Download von Modellen, eine optionale Veröffentlichung auf Sketchfab sowie den Export als OBJ unter iOS bzw. als GLB unter Android. 2025-06-17: Das professionelle RealityCapture wurde in RealityScan umbenannt; RealityScan 2.0 wurde zum Desktop-Produkt, die Telefon-App heißt RealityScan Mobile. 2026-06-24: RealityScan 2.2 ergänzte die hardwarebeschleunigte Rekonstruktion auf unterstützten AMD Radeon und Ryzen AI Max unter Windows.

## Anwendung {#how-to-use-this}

Ab 2022-12-05 konnten Praktiker RealityScan als öffentlich verfügbare mobile Photogrammetrie-Option betrachten und nicht nur als neu angekündigte Beta.

1. Prüfen Sie die Gerätekompatibilität: iOS 16+ oder Android 7+ mit ARCore; installieren Sie anschließend die App und melden Sie sich mit einem Epic-Games-Konto an.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/RealityScan-System-Requirements-and-Installation?lang=en-US>
2. Erstellen Sie ein Projekt im Augmented Reality Mode und umkreisen Sie das Objekt in mehreren Bögen in unterschiedlicher Höhe; das Aufnahmelimit liegt bei 300 Bildern.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
3. Sehen Sie sich die Punktwolke an, begrenzen Sie die reconstruction region, starten Sie die Verarbeitung und warten Sie auf den Status Processed.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
4. Öffnen Sie View/Edit Scan, schneiden Sie das Ergebnis zu und exportieren Sie das Modell auf das Gerät oder senden Sie es an Sketchfab.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
5. Für die Verarbeitung am Desktop installieren Sie die gewünschte Version über den Tab RealityScan im Epic Games Launcher.
  — <https://dev.epicgames.com/documentation/en-us/realityscan/getting-realityscan>

## Bewährte Praktiken {#best-practices}

- Halten Sie das Objekt mindestens zur Hälfte im Bild und sorgen Sie für eine hohe, überlappende Abdeckung von allen verfügbaren Seiten: Bereiche, die in keinem Foto mehrfach sichtbar sind, gelangen nicht in das Modell.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
- Wechseln Sie während des Hochladens und der ersten Analyse nicht in eine andere App, damit der Aufnahme-Workflow nicht unterbrochen wird.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
- Entfernen Sie vor der Verarbeitung den Hintergrund und überflüssige Punkte innerhalb der reconstruction region: Alles außerhalb der Grenzen wird nicht rekonstruiert.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
- Verwenden Sie für kontrollierte Aufnahmen den Camera Control Mode und halten Sie Licht- und Blitzeinstellungen innerhalb einer Sitzung konstant.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-mobile-1-6-release-notes?lang=en-US>

## Hierdurch überholt {#superseded-by-this}

- 2022-04-04: Die begrenzte TestFlight-Beta und das Versprechen eines künftigen iOS Early Access wurden durch die öffentliche mobile App ersetzt.
- 2022-12-05: Der reine iOS-Status ist nach der Android-Veröffentlichung vom 2023-06-20 veraltet.
- 2022-12-05: Der verpflichtende Export über Sketchfab ist seit RealityScan Mobile 1.5 vom 2024-06-24 veraltet, das den lokalen Download von Modellen ergänzte.
- 2025-06-17: RealityCapture als aktueller Name des Desktop-Produkts wurde durch RealityScan ersetzt; der alte Name bleibt nur für Legacy-Versionen und Lizenzen bestehen.

## Noch unbekannt {#still-unknown}

- Im vorgegebenen Antwortschema fehlen die Felder event_findings und new_events, daher sind zusätzliche Ereignisdaten in what_changed und supersedes aufgenommen.
- Die Ereignisse vom 2022-04-04 und 2022-12-05 gehören zu einer einzigen mobilen RealityScan-Linie; das Desktop-RealityScan erschien unter diesem Namen erst nach der Umbenennung von RealityCapture im Jahr 2025.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.capturingreality.com/introducing-realityscan | Introducing RealityScan: Now in Limited Beta | 2026-09-05 |
| https://habr.com/ru/news/t/703566/ | Мобильный 3D-сканер RealityScan от Epic Games вышел из беты и доступен в App Store | 2026-09-05 |
| https://forums.unrealengine.com/t/realityscan-is-now-free-to-download-on-ios/717656 | RealityScan is now free to download on iOS | 2026-09-05 |
| https://forums.unrealengine.com/t/realityscan-is-now-available-for-android-devices/1204921 | RealityScan is now available for Android devices! | 2026-09-05 |
| https://forums.unrealengine.com/t/realityscan-1-5-0-release-notes/1914888 | RealityScan 1.5.0 Release Notes | 2026-09-05 |
| https://www.realityscan.com/news/realityscan-20-new-release-brings-powerful-new-features-to-a-rebranded-realitycapture | RealityScan 2.0: New release brings powerful new features to a rebranded RealityCapture | 2026-09-05 |
| https://www.realityscan.com/news/realityscan-2-2-is-here-with-full-amd-gpu-support-download-today | RealityScan 2.2 is here with full AMD GPU support—download today | 2026-09-05 |
| https://dev.epicgames.com/documentation/realityscan-mobile/RealityScan-System-Requirements-and-Installation?lang=en-US | RealityScan System Requirements and Setup | 2026-09-05 |
| https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide | RealityScan Step by Step Guide | 2026-09-05 |
| https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-mobile-1-6-release-notes?lang=en-US | RealityScan Mobile 1.6 Release Notes | 2026-09-05 |
| https://dev.epicgames.com/documentation/en-us/realityscan/getting-realityscan | Getting RealityScan | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:realityscan`, Strang `mobile-photogrammetry-launch-and-release`, 2 datierte Ereignisse vom 2022-04-04 bis 2022-12-05.
- **Praktischer Hinweis:** Ab 2022-12-05 konnten Praktiker RealityScan als öffentlich verfügbare mobile Photogrammetrie-Option betrachten und nicht nur als neu angekündigte Beta.
- **Konfidenz:** hoch. Die datierten Einträge zu überholten Inhalten oben sind maßgeblich dafür, was veraltet ist.
