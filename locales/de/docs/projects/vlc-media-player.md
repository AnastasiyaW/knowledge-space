---
title: "VLC media player — Videoverbesserung"
category: projects
date: 2023-04-13
tags: [project, video-enhancement, vlc, vlc-media-player, vlc_rtx_vsr]
aliases: ["VLC", "VLC media player"]
level: 2
source_sha256: a76811c04fb0af50721dcdc7bec9ace9ed451303233f112313b17f9d5d77a424
translation: machine
translated_at: '2026-10-24'
---
# VLC media player — Videoverbesserung {#vlc-media-player-video-enhancement}

**Entwicklungslinie:** `project:vlc-media-player` · Strang `video-enhancement`  
**Letztes Ereignis:** 2023-04-13 · 1 datiertes Ereignis seit 2023-04-13 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

VLC media player ist ein Open-Source-Mediaplayer für Nutzer, die einen einzigen Client statt des standardmäßigen Players ihres Betriebssystems benötigen: lokale Dateien, Datenträger, Netzwerk-URLs, NAS und Chromecast.

- Hardware-Dekodierung, HDR und 360°-Video.
- Auswahl von externen und eingebetteten Untertiteln und Audiospuren.
- Wiedergabe von Netzwerkstreams und Durchsuchen von Netzwerkordnern.

Die Hardware-Dekodierung hängt von Plattform und Hardware ab.

Für die reguläre Wiedergabe sollte die aktuelle stabile VLC-Version installiert werden und nicht der alte experimentelle RTX-Build.

## Entwicklungslinie {#development-line}

- **2023-04-13 — VLC testete die Integration von NVIDIA RTX Video Super Resolution.** Am 2023-04-13 stellte VLC einen Testbuild mit Unterstützung für NVIDIA RTX Video Super Resolution zur Verfügung. Dies war ein Entwicklungsschritt in Richtung GPU-gestützter Videohochskalierung während der Wiedergabe, verteilt über ein eigenes experimentelles Archiv.

## Was sich geändert hat {#what-changed}

2023-04-13 — Ein eigener Windows-Build von VLC 3.0.19 RTX Vetinari aktivierte NVIDIA RTX Video Super Resolution standardmäßig auf RTX 30/40.

2025-01-13 — VLC für Android 3.6.0 ergänzte Fernzugriff und Kindersicherung.

2026-01-08 — Die stabile VLC-Version 3.0.23 ergänzte Windows-ARM64-Unterstützung, ein dunkles Design für Windows/Linux, Codec-Aktualisierungen sowie Stabilitäts- und Sicherheitskorrekturen.

## Anwendung {#how-to-use-this}

Ab 2023-04-13 konnten Anwender mit kompatibler NVIDIA-RTX-Hardware den experimentellen GPU-Hochskalierungspfad von VLC mithilfe des verlinkten Testbuilds evaluieren. Er war jedoch nicht als standardmäßige Funktion einer stabilen Version anzusehen.

1. Installieren Sie die aktuelle stabile VLC-Version 3.0.23 für den Desktop; für Windows gibt es x64- und ARM64-Builds.
  — <https://images.videolan.org/vlc/releases/3.0.23.html>
2. Öffnen Sie eine lokale Datei über Medien → Datei öffnen oder ziehen Sie sie in das VLC-Fenster.
  — <https://docs.videolan.me/vlc-user/desktop/3.0/en/basic/media.html>
3. Für einen Stream wählen Sie Medien → Netzwerkstream öffnen, fügen die URL ein und drücken Sie Wiedergabe.
  — <https://docs.videolan.me/vlc-user/desktop/3.0/en/basic/media.html>
4. Auf Android installieren Sie die aktuelle Version von VLC, um Dateien, Netzwerkstreams und DVD-ISOs abzuspielen sowie auf NAS oder freigegebene Ordner zuzugreifen.
  — <https://images.videolan.org/vlc/download-android.html>

## Bewährte Vorgehensweisen {#best-practices}

- Halten Sie den Desktop-VLC aktuell: 3.0.23 enthält Sicherheits- und Stabilitätskorrekturen für Demuxer.
  — <https://images.videolan.org/news.html>
- Verwenden Sie unter Android die Hardware-Dekodierung, wenn das Gerät sie unterstützt; auf älteren Geräten die Software-Dekodierung.
  — <https://images.videolan.org/vlc/download-android.html>
- Wählen Sie Untertitel- und Audiospuren in den Wiedergabesteuerungen oder im Datenträgerdialog aus, statt die Datei vorab zu transkodieren.
  — <https://docs.videolan.me/vlc-user/desktop/3.0/en/basic/media.html>

## Abgelöst durch {#superseded-by-this}

- 2023-04-13 — VLC 3.0.19 RTX war ein Testbuild für RTX Video Super Resolution und kein standardmäßiges Desktop-Release; die unterstützte Version 3.0.23 (2026-01-08) ersetzt sie für den allgemeinen Gebrauch.
- 2025-01-13 — Android 3.6.0 ist nicht mehr aktuell: Android 3.7.0 wurde am 2026-02-25 veröffentlicht.

## Weiterhin unbekannt {#still-unknown}

- Der Social-Media-Beitrag vom 2025-01-13 war nicht lesbar; die offizielle Ankündigung am selben Tag bestätigt das Release von VLC für Android 3.6.0, nicht aber den genauen Wortlaut des Beitrags.
- Die Themen VLC und VLC RTX VSR gehören zum selben Projekt, verfolgen aber getrennte Produktlinien: den standardmäßigen Desktop- und Mobil-Player sowie einen temporären Windows-Build mit NVIDIA RTX VSR.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://downloads.videolan.org/testing/vlc-rtx-upscaler/ | VLC 3.0.19 RTX Vetinari - VideoLAN | 2026-09-05 |
| https://images.videolan.org/news.html | News - VideoLAN | 2026-09-05 |
| https://images.videolan.org/vlc/releases/3.0.23.html | VLC 3.0.23 Vetinari - VideoLAN | 2026-09-05 |
| https://docs.videolan.me/vlc-user/desktop/3.0/en/basic/media.html | Media — VLC Desktop User Documentation 3.0 documentation | 2026-09-05 |
| https://images.videolan.org/vlc/download-android.html | Official Download of VLC media player for Android - VideoLAN | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Thema:** `project:vlc-media-player`, Strang `video-enhancement`, 1 datiertes Ereignis 2023-04-13 → 2023-04-13.
- **Praxishinweis:** Ab 2023-04-13 konnten Anwender mit kompatibler NVIDIA-RTX-Hardware den experimentellen GPU-Hochskalierungspfad von VLC mithilfe des verlinkten Testbuilds evaluieren. Er war jedoch nicht als standardmäßige Funktion einer stabilen Version anzusehen.
- **Konfidenz:** mittel. Die datierten Ablösungshinweise oben sind maßgeblich dafür, was veraltet ist.
