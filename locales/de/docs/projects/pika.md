---
title: "Pika"
category: projects
date: 2025-02-07
tags: [pika, pika-product-development, pika_camera_control, pikadditions, project]
aliases: ["Pika", "Pika AI Selves"]
level: 2
source_sha256: 54ba5be063a88d54812abc8698646f3f8df01697d239a59acc6925f0458c389f
translation: machine
translated_at: '2026-10-24'
---
# Pika {#pika}

**Entwicklungslinie:** `project:pika` · Thread `pika-product-development`  
**Letztes Ereignis:** 2025-02-07 · 2 datierte seit 2023-09-12 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Pika: eine Cloud-Plattform für Autoren kurzer Videos, die mit Runway in Text-zu-Video, Bild-zu-Video und Video-zu-Video konkurriert. Funktionen: Pika 2.5, Pikaframes, Pikascenes, Pikadditions, Pikaswaps, Pikatwists und Pikaffects. Limit im aktuellen Tarifangebot: Standardvideos 5 oder 10 Sekunden, Pikaframes bis zu 25 Sekunden. Fazit: geeignet für schnelle Generierungen und effektvolle Transformationen, ersetzt aber kein Frame-für-Frame-Compositing oder aufwendigen Schnitt.

## Entwicklungslinie {#development-line}

- **2023-09-12 — Kamerasteuerung in Pika wurde dokumentiert.** Zoom, Pan und Rotate; Schwenkrichtungen lassen sich kombinieren, Bewegungstypen dagegen nicht.
- **2025-02-07 — Pika Additions erschien in Pikas Produktlinie.** Am 2025-02-07 verwies eine offizielle Pika-URL auf eine benannte Funktion, Pika Additions. Der datierte Link belegt weder deren Mechanik, Verfügbarkeit noch Einführungsumfang; dieses Ereignis hält daher nur das Auftauchen der benannten Funktion fest.

## Was sich geändert hat {#what-changed}

2023-09-12 — In der Discord-Version erschien der Parameter -camera: zoom, pan und rotate; Schwenkrichtungen lassen sich kombinieren, Bewegungstypen dagegen nicht. 2023-11-29 — Pika 1.0 überführte das Produkt vom Discord-Bot in eine neue Weboberfläche und ein neues Modell zur Erzeugung und Bearbeitung von Videos in 3D-Animations-, Anime-, Cartoon- und filmischen Stilen. 2025-02-07 — Pikadditions ergänzte Video-zu-Video-Einfügung einer Person oder eines Objekts in ein bestehendes Video; eine unabhängige datierte Quelle belegt den Start am 6. Februar 2025. 2026-02-28 — Der Inhalt des verknüpften X-Beitrags ließ sich nicht prüfen: Die Seite lieferte keinen Text. Eine bestimmte Modell- oder Release-Zuordnung zu diesem Datum lässt sich nicht verlässlich herstellen. 2025-04-10 — Pikaframes erhielt Übergänge und Transformationen zwischen maximal fünf Bildern, mit einer Gesamtlänge von bis zu 25 Sekunden. 2025-04-24 — Pikatwists erschien für die textbasierte Beschreibung einer Videotransformation. 2025-05-01 — Neue Pikaffects erschienen; Unterstützung für Videoeingabe ist im App-Verlauf am 9. Mai 2025 vermerkt. 2026-01-26 — Der App-Verlauf verzeichnete Pika 2.5; die aktuelle Tarifseite führt es als verfügbares Modell für Text-zu-Video und Bild-zu-Video.

## Anwendung {#how-to-use-this}

Ab 2023-09-12 und 2025-02-07 sollten Praktiker Kamerasteuerung und Pika Additions als getrennte Funktionsbereiche von Pika verfolgen und das aktuelle Verhalten sowie den Zugang prüfen, bevor sie sich in einem Produktions-Workflow auf eines von beiden stützen.

1. Melden Sie sich bei Pika an und wählen Sie einen Modus: Text-zu-Video, Bild-zu-Video, Pikaframes, Pikadditions, Pikaswaps, Pikatwists oder Pikaffects.
  — <https://pika.art/pricing>
2. Laden Sie für Pikadditions das Ausgangsvideo sowie gegebenenfalls ein Referenzbild des Objekts hoch und beschreiben Sie die Ergänzung im Text; die API akzeptiert 720p oder 1080p und eine Dauer von 5 oder 10 Sekunden.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
3. Für die API laden Sie zuerst die lokale Mediendatei über einen Presigned Upload hoch und übergeben dann die zurückgegebene URL in der Generierungsanfrage.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
4. Speichern Sie die ID der asynchronen Aufgabe, fragen Sie sie ab, bis sie `completed` oder `failed` ist, und rufen Sie erst danach die Ergebnis-URL ab.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>

## Best Practices {#best-practices}

- Für gezielte Bewegung im historischen Discord-Modus setzen Sie -camera ohne Leerzeichen vor den Bindestrich; verwenden Sie zoom, pan oder rotate und kombinieren Sie keine unvereinbaren Bewegungstypen.
  — <https://mmmnote.com/article/7e7/11/article-41241b98282aa08c.shtml>
- Für die API setzen Sie einen Idempotency-Key für wiederholbare Anfragen und ändern den Anfragekörper nicht, wenn Sie den Schlüssel wiederverwenden.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
- Betrachten Sie `queued` oder `running` nicht als fertiges Video: Behandeln Sie `completed` und `failed` als Endzustände und reagieren Sie auf 429 mit Beachtung des `Retry-After`-Headers.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
- Wählen Sie Pikadditions nicht für Frame-für-Frame-Rotoskopie, pixelgenaues Compositing oder Spielfilmlängen; die Dokumentation nennt diese Aufgaben ausdrücklich als ungeeignet.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>

## Hiermit ersetzt {#superseded-by-this}

- 2023-09-12 — Die frühere Discord-Syntax -camera ist historisch und beschreibt nicht das heutige Web-Produkt.
- 2023-11-29 — Pika 1.0 und seine frühere Web-Erfahrung wurden durch nachfolgende Linien ersetzt, darunter Pika 2.5 im aktuellen Tarifangebot.
- 2025-02-07 — Die frühe Darstellung von Pikadditions als einzige Neuerung ist veraltet: Die aktuelle Linie umfasst außerdem Pikascenes, Pikaswaps, Pikatwists, Pikaffects und Pikaframes.

## Weiterhin unbekannt {#still-unknown}

- Der X-Beitrag vom 2026-02-28 lieferte bei der Prüfung keinen Text; sein Inhalt, das genaue Modell und der Umfang der Änderung sind unbekannt.
- Die Discord-Links von 2023 und „The source“ waren für eine unabhängige Prüfung nicht zugänglich; Kamerasteuerung und Pika 1.0 sind durch datierte Sekundärquellen belegt.
- Das Thema Pika AI Selves ist durch die verfügbaren Quellen nicht als eigenständiges Produkt oder Funktion von Pika belegt; möglicherweise handelt es sich um eine separate Bezeichnung in den Ausgangsmeldungen.
- Die angeforderten separaten Felder event_findings und new_events sieht das vorgegebene Antwortschema nicht vor; ihre Fakten sind in der Chronologie unter what_changed erfasst.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://mmmnote.com/article/7e7/11/article-41241b98282aa08c.shtml | Pika Labs推出影像控制新功能,-camera提升视觉丰富度 | 2026-09-05 |
| https://petapixel.com/2023/11/28/generative-video-startup-pika-labs-launches-version-1-0-raises-55-million-in-funding/ | Generative Video Startup Pika Labs Launches Version 1.0, Raises $55 Million in Funding | 2026-09-05 |
| https://pika.art/blog | Blog | Pika | 2026-09-05 |
| https://pika.art/pikadditions | Pika | 2026-09-05 |
| https://www.tomsguide.com/ai/ai-image-video/pika-labs-launches-pikadditions-to-add-anything-and-anyone-to-any-video-heres-how | Pika Labs launches 'Pikadditions' to add anything and anyone to any video — here's how | 2026-09-05 |
| https://mcp.pika.art/models/pika/pikadditions/video-to-video | Pikadditions | Pika API | 2026-09-05 |
| https://pika.art/pricing | Subscription Pricing | Pika | 2026-09-05 |
| https://apps.apple.com/us/app/pika-ai-video/id6680155400?platform=vision | Pika - AI Video App - App Store | 2026-09-05 |
| https://x.com/pika_labs/status/2027549433261658534 | x.com | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:pika`, Thread `pika-product-development`, 2 datierte Ereignisse 2023-09-12 → 2025-02-07.
- **Praxishinweis:** Ab 2023-09-12 und 2025-02-07 sollten Praktiker Kamerasteuerung und Pika Additions als getrennte Funktionsbereiche von Pika verfolgen und das aktuelle Verhalten sowie den Zugang prüfen, bevor sie sich in einem Produktions-Workflow auf eines von beiden stützen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Angaben unter „Hiermit ersetzt“.
