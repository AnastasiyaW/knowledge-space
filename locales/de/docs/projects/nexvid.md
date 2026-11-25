---
title: "NexVid — Verteilung der Browser-Erweiterung"
category: projects
date: 2026-04-17
tags: [browser-extension-distribution, nexvid, project]
aliases: ["NexVid"]
level: 3
source_sha256: 69700292e2d23129b7207b3946e34436e87a6c0816666eb8fd3b1cd26e6b786c
translation: machine
translated_at: '2026-10-24'
---
# NexVid — Verteilung der Browser-Erweiterung {#nexvid-browser-extension-distribution}

**Entwicklungsstrang:** `project:nexvid` · Thread `browser-extension-distribution`  
**Letztes Ereignis:** 2026-04-17 · 1 datiertes Ereignis seit 2026-04-17 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

NexVid ist eine Browser-Erweiterung für Menschen, die Anime, Zeichentrickserien und Web-Videos in Chrome oder Firefox ansehen.
- Anime4K-GPU-Upscaling für Videowiedergabe in Echtzeit.
- Qualitäts- und FPS-Profile, um sie an die Hardwareleistung anzupassen.
- Filter und WebGL-Shader zur Bildanpassung.
- Presets zum Speichern von Shader- und Filterketten.
- Lokaler Player für Videodateien auf dem Desktop.

Die Verarbeitung läuft während der Wiedergabe und erfordert Zugriff auf Daten aller Websites; v1.1.9 vom 2026-08-20 ist aktuell.
Sie optimiert die Wiedergabe, ersetzt aber keinen Video-Export mit neuronalem Upscaling.

## Entwicklungsstrang {#development-line}

- **2026-04-17 — Einträge der NexVid-Browser-Erweiterung erschienen für Chrome und Firefox.** Am 2026-04-17 erschienen Einträge für die NexVid-Browser-Erweiterung im Chrome Web Store und in den Firefox Add-ons. Dieser Schritt erweiterte die Verteilung auf Chrome und Firefox. Die Quelleinträge nennen für dieses Datum keine Version, keinen Funktionsumfang, keinen Verfügbarkeitsstatus und keine Änderungen.

## Was sich geändert hat {#what-changed}

- 2025-10-27 — Firefox 1.0.2 wurde zur frühesten öffentlich sichtbaren Version in der AMO-Historie.
- 2025-11-10 — Firefox 1.0.5 ergänzte lokale Videos und zusätzliche Effekte.
- 2025-12-01 — Firefox 1.1.0 ergänzte dunkle und minimalistische Themes, erhöhte die maximale FPS und behob einen Fehler bei Twitch; 1.1.1 am selben Tag behob die Profilauswahl in der minimalen Oberfläche.
- 2026-01-20 — Firefox 1.1.2 ergänzte einen Auflösungsschwellenwert, um hochwertige Quellen zu überspringen, sowie experimentelle Shader.
- 2026-03-08 — Firefox 1.1.3 ergänzte eine Website-Whitelist.
- 2026-04-17 — Chrome 1.1.6 wurde aktualisiert; dies bestätigt ein Chrome-Release, keine identische Firefox-Version an diesem Datum.
- 2026-08-20 — Chrome und Firefox bieten 1.1.9 an; die aktuellen Store-Beschreibungen nennen Anime4K, Performance-Profile, Shader, Presets und einen lokalen Player.

## Anwendung {#how-to-use-this}

Ab 2026-04-17 sollten Praktiker, die NexVid evaluieren, die Verfügbarkeit der Browser-Erweiterung über den Chrome Web Store und die Firefox Add-ons prüfen und dabei Kompatibilität und Funktionsumfang unabhängig aktuell verifizieren.

1. NexVid aus dem Chrome Web Store oder den Firefox Add-ons installieren und das gewünschte Web-Video öffnen.
  — <https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim>
2. Ein Anime4K-Profil und eine Ziel-FPS passend zur Rechnerleistung wählen und anschließend einen Auflösungsschwellenwert setzen, um hochwertige Quellen zu überspringen.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>
3. Bei Bedarf eine Kette aus Filtern und WebGL-Shadern aufbauen und dann als Preset speichern.
  — <https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim>
4. Lokale Dateien mit dem integrierten Player öffnen, statt einen Export eines hochskalierten Videos zu erwarten.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>

## Best Practices {#best-practices}

- Mit Anime und Zeichentrickserien beginnen; der Autor nennt sie als die besten Quellen.
  — <https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/>
- Die FPS nicht über die Quellrate erhöhen. Der Regler begrenzt die verarbeiteten Frames, statt neue zu erzeugen; ein Limit von 30 FPS bei einer 60-FPS-Quelle kann zu Frame-Verlusten führen.
  — <https://www.reddit.com/r/SideProject/comments/1okqhgx/i_made_a_browser_extension_that_let_you_upscale/>
- Zuerst ein Profil für die Hardwarelast wählen, dann Filter getrennt abstimmen. Der Autor empfiehlt Unsharp Mask und High-Pass für die Schärfe, bevor ein Preset gespeichert wird.
  — <https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/>
- Vor der Installation die Berechtigung für den Zugriff auf Daten aller Websites prüfen und, sofern verfügbar, die Erweiterung auf eine Website-Whitelist beschränken.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>

## Dadurch ersetzt {#superseded-by-this}

- 2025-10-31 — Der Hinweis, dass lokale Dateien nicht in NexVid geöffnet werden können, ist veraltet, seit die Unterstützung für lokale Videos am 2025-11-10 mit Firefox 1.0.5 eingeführt wurde.
- 2026-04-17 — Chrome 1.1.6 ist als empfohlene Version überholt: Der aktuelle Store-Eintrag nennt 1.1.9 vom 2026-08-20.

## Weiterhin unbekannt {#still-unknown}

- Die öffentliche Firefox-Versionshistorie endet mit 1.1.3 am 2026-03-08, während der aktuelle Eintrag 1.1.9 zeigt; zwischen diesen Versionen ist kein Changelog verfügbar.
- Chrome v1.1.6 und sein Statistik-Snapshot sind für den 2026-04-17 bestätigt, aber kein primäres Changelog erklärt den Inhalt dieses Updates.
- Der Chrome Store nennt die Erhebung von Standort- und Nutzungsaktivitätsdaten, während der Firefox-Eintrag Datenzugriff auf alle Websites verlangt; eine vergleichbare Aufschlüsselung der Berechtigungen über beide Plattformen ist nicht belegt.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim | NexVid - Real-time Video Upscaler & Enhancer - Chrome Web Store | 2026-09-05 |
| https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/ | NexVid - Real-time Video Upscaler & Enhancer – Firefox Add-ons | 2026-09-05 |
| https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/versions/ | Versionsverlauf von NexVid - Real-time Video Upscaler & Enhancer | 2026-09-05 |
| https://chrome-stats.com/d/hiocbajaikpcckgeagcngaeoioncmbim | NexVid: Real-time Video Upscaler & Enhancer | 2026-09-05 |
| https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/ | Ich habe eine Browser-Erweiterung gebaut, mit der du Videos in Echtzeit hochskalieren und verbessern kannst: NexVid | 2026-09-05 |
| https://www.reddit.com/r/SideProject/comments/1okqhgx/i_made_a_browser_extension_that_let_you_upscale/ | Ich habe eine Browser-Erweiterung gebaut, mit der du Videos in Echtzeit hochskalieren und verbessern kannst: NexVid | 2026-09-05 |
| https://www.reddit.com/r/chrome_extensions/comments/1okqerj/i_made_an_extension_that_let_you_upscale_and/ | Ich habe eine Erweiterung gebaut, mit der du Videos in deinem Browser in Echtzeit hochskalieren und verbessern kannst: NexVid | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:nexvid`, Thread `browser-extension-distribution`, 1 datiertes Ereignis 2026-04-17 → 2026-04-17.
- **Praxishinweis:** Ab 2026-04-17 sollten Praktiker, die NexVid evaluieren, die Verfügbarkeit der Browser-Erweiterung über den Chrome Web Store und die Firefox Add-ons prüfen und dabei Kompatibilität und Funktionsumfang unabhängig aktuell verifizieren.
- **Konfidenz:** mittel. Die datierten Überholungshinweise oben sind maßgeblich dafür, was veraltet ist.
