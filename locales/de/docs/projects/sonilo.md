---
title: "Sonilo"
category: projects
date: 2026-06-29
tags: [project, sonilo, sonilo-v1-1]
aliases: ["Sonilo"]
level: 3
source_sha256: 52b6247125f3ed7ffabbd2966aab27dd62b7aa7fd05f9648a5d48ffd3a305d7a
translation: machine
translated_at: '2026-10-24'
---
# Sonilo {#sonilo}

**Entwicklungslinie:** `project:sonilo` · Thread `sonilo-v1-1`  
**Letztes Ereignis:** 2026-06-29 · 1 datiertes seit 2026-06-29 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Sonilo ist ein API-first-Audiowerkzeug für Editoren, Teams kreativer Produkte und Entwickler, die Musik oder Sound an einen Schnitt binden müssen.

- erzeugt Musik aus Text oder Video;
- erzeugt textgeführte und videogeführte Soundeffekte;
- mischt bereitgestellte Sprache und Musik mit automatischem Ducking.

## Entwicklungslinie {#development-line}

- **2026-06-29 — Sonilo v1.1 mit einem Text-to-Music-Endpoint verknüpft.** Die Version liefert eine engere Ausrichtung von Video auf Musik, erhält die Originalsprache und ergänzt Prompts pro Segment. Das Release des Herstellers selbst ist auf 2026-06-18 datiert.

## Was sich geändert hat {#what-changed}

2026-06-29 — Sonilo v1.1 liefert eine engere Ausrichtung von Video auf Musik, erhält die Originalsprache und ergänzt Prompts pro Segment. Das Release des Herstellers selbst ist auf 2026-06-18 datiert.

## So verwenden {#how-to-use-this}

Ab 2026-06-29 behandeln wir Sonilo v1.1 als eigenständigen Kandidaten-Endpoint, der über die verlinkte Text-to-Music-Route und die Sonilo-Plattform zu bewerten ist. Fähigkeiten oder Migrationsanforderungen setzen wir nicht voraus, bis die Quellseiten ausgewertet sind.

1. Einen API-Schlüssel erstellen, serverseitig aufbewahren und das erforderliche API-Guthaben hinzufügen, bevor eine Generierung versucht wird.
  — <https://platform.sonilo.com/docs/quickstart>
2. Die für das Konto aktivierten Dienste und die Nutzung vorab prüfen und danach Text-to-Music für ein musikalisches Briefing oder Video-to-Music für eine fixierte visuelle Timeline auswählen.
  — <https://platform.sonilo.com/docs/api>
3. Für die direkte Textgenerierung einen Prompt und eine Dauer von 5–360 Sekunden per POST an /v1/text-to-music senden.
  — <https://platform.sonilo.com/docs/text-to-music>
4. Gestreamte Audio-Chunks nur über das complete-Event verarbeiten oder den Async-Modus verwenden und die zurückgegebene Task-ID bis zu einem Endzustand abfragen.
  — <https://platform.sonilo.com/docs/text-to-music>
5. Falls das Produkt bereits fal nutzt, das Textmodell v1.1 unter sonilo/v1.1/text-to-music aufrufen, statt eine eigene Provider-Integration zu bauen.
  — <https://fal.ai/models/sonilo/v1.1/text-to-music>

## Best Practices {#best-practices}

- API-Schlüssel in einer serverseitigen Umgebungsvariable halten. Einen offengelegten Schlüssel widerrufen und ersetzen, statt ihn in eine Client-App einzubetten.
  — <https://platform.sonilo.com/docs>
- 401, 402, 403 und 429 als getrennte Zustände für Einrichtung, Guthaben, Dienstzugriff und Backoff behandeln. Nach einer fehlgeschlagenen Anfrage kein Platzhalter-Audio erzeugen.
  — <https://platform.sonilo.com/docs/text-to-music>
- Videoeingabe verwenden, wenn Timing, Schnitte oder Sprachraum den Soundtrack bestimmen sollen. Texteingabe verwenden, wenn die Aufgabe ein eigenständiger Cue ist.
  — <https://platform.sonilo.com/docs/api>
- Bei bezahlter oder Kundenarbeit den erzeugten Track gegen Voice-over und Szenenwechsel prüfen, Ausgabe und Kontodaten aufbewahren und bestätigen, dass der aktuelle Tarif die beabsichtigte Veröffentlichung abdeckt.
  — <https://sonilo.com/blog/ai-music-video-creators-2026>

## Hiermit ersetzt {#superseded-by-this}

- 2026-06-18 — Für Videovertonung, die erhaltene Dialoge oder szenenspezifische Vorgaben verlangt, ersetzt v1.1 die Generierung im Stil von v1.0 ohne diese Steuerungsmöglichkeiten. Das Release sagt nicht, dass v1.0-Endpoints abgeschaltet wurden.
- 2026-08-03 — Wenn ein Projekt bereits getrennte Sprach- und Musikassets hat, ersetzt der dokumentierte Audio-Ducking-Endpoint die manuelle Lautstärkeführung, sofern sein Zwei-Eingangs-Workflow passt.

## Noch unbekannt {#still-unknown}

- Das vorliegende Ereignis ist auf 2026-06-29 datiert, während die Release-Seite von Sonilo v1.1 auf 2026-06-18 datiert; es wurde keine Primärquelle gefunden, die die Differenz von elf Tagen erklärt.
- Die Vergleichszahlen zu v1.1 stammen vom Anbieter selbst; ein öffentliches Bewertungsprotokoll oder eine unabhängige Replikation wurde nicht gefunden.
- Der direkte Sonilo-Text-Endpoint dokumentiert eine Obergrenze von 360 Sekunden, der fal-Text-Endpoint für v1.1 dokumentiert 600 Sekunden. Grenzwerte gelten routenspezifisch, bis sie für das vorgesehene Konto bestätigt sind.
- In diesem Durchgang wurde keine öffentliche Primärquelle gefunden, die einen Nachfolger von v1.1 benennt.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://sonilo.com/news/sonilo-v1-1 | Sonilo v1.1 vorgestellt | Sonilo | 2026-09-05 |
| https://fal.ai/models/sonilo/v1.1/text-to-music | Sonilo V1.1 Text to Music (Text to Audio) API auf fal | 2026-09-05 |
| https://platform.sonilo.com/ | Sonilo API — Enterprise AI Music API | 2026-09-05 |
| https://platform.sonilo.com/docs | Einführung · Sonilo Docs | 2026-09-05 |
| https://platform.sonilo.com/docs/quickstart | Schnellstart · Sonilo Docs | 2026-09-05 |
| https://platform.sonilo.com/docs/text-to-music | Text to Music · Sonilo Docs | 2026-09-05 |
| https://platform.sonilo.com/docs/api | API-Referenz | 2026-09-05 |
| https://sonilo.com/zh-CN/news/sonilo-v1 | 介绍 Sonilo v1.0 | Sonilo | 2026-09-05 |
| https://sonilo.com/blog/sonilo-comfyui | Exciting News: Sonilo is Now Live on ComfyUI! | Sonilo | 2026-09-05 |
| https://sonilo.com/blog/product/audio-ducking-api-guide | Audio Ducking API: Stimme und Musik automatisch mischen | Sonilo | 2026-09-05 |
| https://sonilo.com/blog/ai-music-video-creators-2026 | Lizenzierte KI-Musik für YouTube, Werbung und Kundenvideos (Leitfaden 2026) | Sonilo | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:sonilo`, Thread `sonilo-v1-1`, 1 datiertes Ereignis 2026-06-29 → 2026-06-29.
- **Praktischer Hinweis:** Ab 2026-06-29 behandeln wir Sonilo v1.1 als eigenständigen Kandidaten-Endpoint, der über die verlinkte Text-to-Music-Route und die Sonilo-Plattform zu bewerten ist. Fähigkeiten oder Migrationsanforderungen setzen wir nicht voraus, bis die Quellseiten ausgewertet sind.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
