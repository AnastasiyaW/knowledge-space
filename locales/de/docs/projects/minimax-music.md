---
title: "MiniMax Music"
category: projects
date: 2025-10-31
tags: [minimax-music, minimax-music-development, model_releases, project]
aliases: ["MiniMax Music", "MiniMax Music 2.0"]
level: 3
source_sha256: 51fbd4abecf5411ce4705edfaeda58d160327280bac24cd7703d63875219e185
translation: machine
translated_at: '2026-10-24'
---
# MiniMax Music {#minimax-music}

**Entwicklungslinie:** `project:minimax-music` · Thread `minimax-music-development`  
**Letztes Ereignis:** 2025-10-31 · 1 datiertes Ereignis seit 2025-10-31 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

MiniMax Music erzeugt vollständige Songs aus Liedtexten und einer Stilbeschreibung für Kreative und Entwicklerteams.

- Gesangsstücke aus Textprompts und Liedtexten.
- Instrumentalmusik ohne Gesangsparts.
- Cover aus bestehenden Audiodateien auf Basis einer Referenzaufnahme.
- Lokaler Betrieb über offene Gewichte für Music 3.

Der kostenpflichtige Neuzugang zur Music- und Lyrics-API wurde am 2026-08-20 eingestellt. Lokales Music 3 erfordert CUDA mit mindestens 24 GB VRAM im vollständigen Diffusers-Pfad. Neueinsteiger sollten mit MiniMax Audio beginnen oder Music 3 selbst hosten. Den API-Pfad sollten nur bestehende zahlende Kunden weiter nutzen.

## Entwicklungslinie {#development-line}

- **2025-10-31 — Musikgenerierung von MiniMax wurde über dokumentierte Modell-Endpunkte verfügbar.** MiniMax veröffentlichte am 2025-10-31 eine offizielle Produktseite und API-Referenz für Musikgenerierung. Ein gehosteter fal.ai-Modell-Endpunkt bot am selben Datum einen weiteren entwicklerorientierten Zugangsweg.

## Was sich geändert hat {#what-changed}

- 2025-10-31 — MiniMax Music 2.0 erschien mit natürlicheren Gesangsstimmen, Beispielen für mehrstimmigen Gesang bzw. a cappella, Instrumentensteuerung und Songs von bis zu fünf Minuten Länge.
- 2026-01-28 — MiniMax Music 2.5 ergänzte Abschnittssteuerung auf Absatzebene, 14 strukturelle Varianten, über 100 Instrumente und eine überarbeitete Abmischung.
- 2026-02-09 — Kein unabhängig abrufbarer Quelltext belegt für dieses Datum eine eigenständige Veröffentlichung oder Fähigkeitsänderung von MiniMax Music.
- 2026-03-04 — MiniMax Music 2.5+ ergänzte die reine Instrumentalgenerierung und erweiterte damit die Linie über die Erstellung von Gesangsstücken hinaus.
- 2026-03-18 — Music-2.6 tauchte in den offiziellen Modell-Release-Notes als Update für Musik und Cover auf. Die aktuelle Dokumentation bezeichnet es als Text-zu-Musik-Modell der vorherigen Generation.
- 2026-08-13 — MiniMax Music 3.0 erschien als Open-Weights-Veröffentlichung der nächsten Generation für vollständige Songs von bis zu fünf Minuten Länge.
- 2026-08-20 — Neue zahlende Music- und Lyrics-API-Nutzer wurden abgeschnitten, und kostenlose Music-Generierungs-APIs wurden eingestellt. Bestehende zahlende Nutzer behielten den Zugang.

## Verwendung {#how-to-use-this}

Bevor Sie ab 2025-10-31 einen Integrationsweg wählen, prüfen Sie die offizielle API-Dokumentation zur Musikgenerierung und die unterstützten gehosteten Modell-Endpunkte.

1. Wählen Sie zuerst den Zugangsweg: Als neuer Nutzer verwenden Sie MiniMax Audio oder hosten Music 3 selbst. Der neue kostenpflichtige Zugang zur Music-/Lyrics-API ist geschlossen, und kostenlose Endpunkte wurden eingestellt. Bestehende zahlende API-Nutzer können weitermachen.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
2. Als bestehender zahlender API-Nutzer senden Sie JSON mit Bearer-Authentifizierung an `POST /v1/music_generation` und wählen `music-3.0`, das in der Referenz als empfohlen markiert ist.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
3. Beschreiben Sie Genre, Stimmung und Szenario im Feld `prompt`. Übergeben Sie strukturierte Liedtexte in `lyrics` oder setzen Sie `lyrics_optimizer=true`, wenn keine Liedtexte vorhanden sind. Setzen Sie `is_instrumental=true` für einen Track ohne Gesang.  
  — <https://platform.minimax.io/docs/guides/music-generation>
4. Für ein Cover wählen Sie `music-cover` und geben genau eine Referenzaudio-URL oder eine Base64-Nutzlast an. Die akzeptierte Referenz umfasst 6 Sekunden bis 6 Minuten und höchstens 50 MB.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
5. Für lokales Music 3 laden Sie `MiniMaxAI/MiniMax-Music3` herunter und betreiben es mit SGLang-Omni. Die Liedtexte kommen in `input`, die Musikbeschreibung in `instructions`. Diffusers und ComfyUI werden ebenfalls unterstützt.  
  — <https://huggingface.co/MiniMaxAI/MiniMax-Music3>

## Best Practices {#best-practices}

- Halten Sie Musikanweisungen im `prompt` und Liedtexte in `lyrics`. Steuern Sie den Aufbau über dokumentierte Abschnittstags, statt Anweisungen in den Liedtext zu mischen.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
- Wenn Sie keine Liedtexte angeben, setzen Sie `lyrics_optimizer`. Wenn Sie keinen Gesang wünschen, setzen Sie `is_instrumental` explizit und lassen `lyrics` weg.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
- Laden Sie ein Ergebnis im URL-Format innerhalb von 24 Stunden herunter oder verwenden Sie bei Streaming die Hex-Ausgabe, da Streaming nur Hex unterstützt.  
  — <https://platform.minimax.io/docs/api-reference/music-generation>
- Für lokales Music 3 beschreiben Sie globale Metadaten, Gesangsdetails und Arrangement ausführlich. Setzen Sie Liedtext-Tags jeweils auf eine eigene Zeile und behandeln Sie angefordertes Tempo, Tonart, Instrumentierung und Struktur als generative Steuerungen, nicht als Garantien.  
  — <https://huggingface.co/MiniMaxAI/MiniMax-Music3>
- Prüfen Sie die lokale Kapazität, bevor Sie Music 3 laden: CUDA ist erforderlich. Der dokumentierte direkte Diffusers-Pfad benötigt mindestens 24 GB VRAM, während CPU- bzw. Layer-Offloading mit 8 GB auskommt, aber langsamer ist.  
  — <https://huggingface.co/MiniMaxAI/MiniMax-Music3>

## Durch diesen Stand ersetzt {#superseded-by-this}

- 2026-08-13 — MiniMax Music 2.0 als aktuelles Standardmodell für Musik von MiniMax.
- 2026-03-04 — Die Vorgabe, dass MiniMax Music immer Gesang und angegebene Liedtexte benötigt.
- 2026-08-13 — Music-2.6 als empfohlenes Text-zu-Musik-API-Modell.
- 2026-08-20 — Die Anleitung für neue Nutzer, sich für die kostenpflichtige Music-API anzumelden oder Music-3.0-free, Music-2.6-free bzw. music-cover-free zu verwenden.

## Weiterhin unbekannt {#still-unknown}

- Die Quellen zum Datum 2026-02-09 belegen keine eigenständige Veröffentlichung von MiniMax Music. Die WeChat-Seite war nicht abrufbar, und die X-Seite zeigte keinen Beitragstext. Sie lässt sich daher nicht sicher mit Music 2.5 oder einer anderen Version gleichsetzen.
- Die API-Referenz enthält neben der Schließungsmitteilung vom 2026-08-20 weiterhin Modellbeispiele und Namen kostenloser Modelle. Die Fortführung für Bestandskunden ist angegeben, Neuregistrierung und Berechtigungswege wurden aber nicht unabhängig geprüft.
- Aktuelle Preise von MiniMax Audio, regionale Verfügbarkeit, kommerzielle Lizenzierung und Kontingente der Web-Produkte wurden nicht verifiziert. Die Angabe von fal über $0,03 gilt nur für den eigenen v2-Endpunkt.
- Die Music3-Modellkarte besagt, dass kein Hugging-Face-Inference-Provider das Modell hostet. Einen verwalteten Hosted-Inference-Weg außerhalb von MiniMax Audio konnte ich nicht verifizieren.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://www.minimax.io/audio/music | MiniMax Audio | AI Music Generator | 2026-09-04 |
| https://www.minimax.io/news/minimax-music-20 | Making Music Creation Accessible to Everyone - MiniMax News | MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/music-generation | Music Generation - MiniMax API Docs | 2026-09-04 |
| https://fal.ai/models/fal-ai/minimax-music/v2 | MiniMax Music 2.0: State of the Art AI Text-to-Music Generator | fal | 2026-09-04 |
| https://mp-weixin-qq-com.translate.goog/s/hy1RzvAytRSxX63qodEExw?_x_tr_sl=zh-CN&_x_tr_tl=en&_x_tr_hl=en | WeChat article via Google Translate (title unavailable) | 2026-09-04 |
| https://x.com/wavespeed_ai/status/2020165909646586220?s=20 | WaveSpeed AI X post 2020165909646586220 (body unavailable) | 2026-09-04 |
| https://www.minimax.io/news/minimax-music-25 | MiniMax Music 2.5: Breakthrough Across All Dimensions — Direct the Detail. Define the Real - MiniMax News | MiniMax | 2026-09-04 |
| https://www.minimax.io/news/minimax-music-25-2 | MiniMax Music 2.5+: Unlock instrumental music, break through style boundaries. - MiniMax News | MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/release-notes/models | Models - MiniMax API Docs | 2026-09-04 |
| https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model | MiniMax Music 3.0: Next-Generation Open-Weights, Production-Ready & Versatile Music Model - MiniMax Research | MiniMax | 2026-09-04 |
| https://platform.minimax.io/docs/guides/music-generation | Music Generation - MiniMax API Docs | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-Music3 | MiniMaxAI/MiniMax-Music3 · Hugging Face | 2026-09-04 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:minimax-music`, Thread `minimax-music-development`, 1 datiertes Ereignis vom 2025-10-31 → 2025-10-31.
- **Praktischer Hinweis:** Prüfen Sie die offizielle MiniMax-API-Dokumentation und die gehosteten Endpunkte, bevor Sie ab 2025-10-31 einen Integrationsweg wählen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Ersetzungshinweise oben.
