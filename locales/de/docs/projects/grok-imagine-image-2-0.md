---
title: "Grok Imagine Image 2.0 — Bilderzeugung mit Grok Imagine"
category: projects
date: 2026-08-10
tags: [grok, grok-imagine-image, grok-imagine-image-2-0, project]
aliases: ["Grok Imagine Image 2.0"]
level: 2
source_sha256: 3c951526db903196636baa4584cf38f75f6879e486fb93d0ac496ef10b60bab4
translation: machine
translated_at: '2026-10-24'
---
# Grok Imagine Image 2.0 — Bilderzeugung mit Grok Imagine {#grok-imagine-image-20-grok-imagine-image-generation}

**Entwicklungslinie:** `project:grok-imagine-image-2-0` · Thread `grok-imagine-image`  
**Letztes Ereignis:** 2026-08-10 · 1 datiertes Ereignis seit 2026-08-10 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Grok Imagine Image 2.0 ist das xAI-Modell zur Erzeugung und Bearbeitung von Bildern in Grok und in der API. Funktionen: Text-zu-Bild, Bearbeitung per Anweisung, bis zu fünf Referenzen, 1K/2K und Batch-Verarbeitung. Der API-Preis beginnt bei $0.04 pro Bild; für reproduzierbare Ergebnisse sollte `quality` explizit festgelegt werden. Fazit: geeignet für iterative Entwürfe und Compositing, doch der geänderte Qualitätsstandard beeinflusst jetzt Kosten und Ergebnis.

## Entwicklungslinie {#development-line}

- **2026-08-10 — Grok Imagine Image 2.0 wurde über einen Produktnews-Eintrag von xAI vorgestellt.** Das Modell wurde als Quality Mode in Grok und als `grok-imagine-image-2.0` in der API verfügbar.

## Was sich geändert hat {#what-changed}

2026-08-10 — das Ereignis entspricht dem allgemeinen Release, die offizielle Ankündigung ist jedoch auf 2026-08-07 datiert: Das Modell wurde als Quality Mode in Grok und als `grok-imagine-image-2.0` in der API verfügbar. 2026-08-28 — `quality=auto` wurde zulässig, und der Standardwert wechselte von `medium` zu `auto`; derzeit wählt auto für die Erzeugung Low und für die Bearbeitung Medium. Außerdem stieg das Referenzlimit von drei auf fünf, und die Seitenverhältnisse 21:9 und 5:2 kamen hinzu. 2026-09-02 — die Ausmusterung von `grok-imagine-image-quality` zum 2026-11-02 wurde angekündigt: Anfragen an dieses Modell werden dann von Image 2.0 mit `quality=low` bedient; Image 1.0 ist nicht betroffen.

Zum Datum des Ereignisses 2026-08-10 gibt es eine zusätzliche offizielle Klarstellung: Der ursprüngliche Release erfolgte am 2026-08-07, nicht am 2026-08-10; der Umfang des Releases umfasst grok.com/imagine, iOS, Android und die API.

## Anwendung {#how-to-use-this}

Ab 2026-08-10 sollten Praktiker, die Grok Imagine evaluieren, Image 2.0 als datierten Meilenstein der Produktlinie behandeln und die verlinkten Seiten von xAI und Grok konsultieren; Funktionen, Zugang und Verfügbarkeit müssen sie vor einer Abhängigkeit separat prüfen.

1. Öffnen Sie Grok Imagine und wählen Sie für interaktive Erzeugung oder Bearbeitung den Quality Mode.
  — <https://x.ai/news/grok-imagine-image-2>
2. Für die API erstellen Sie einen Schlüssel in der xAI Console und rufen das Modell `grok-imagine-image-2.0` auf.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
3. Für ein neues Bild senden Sie den Prompt an `POST /v1/images/generations`; legen Sie die Anzahl der Ergebnisse, das Seitenverhältnis und die Auflösung fest.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
4. Für eine Korrektur senden Sie die URL oder den base64-Data-URI des Ausgangsbilds an `POST /v1/images/edits` und beschreiben die gewünschte Änderung.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
5. Für Compositing übergeben Sie bis zu fünf Ausgangsbilder in einer einzigen Edit-Anfrage.
  — <https://docs.x.ai/developers/model-capabilities/imagine>

## Best Practices {#best-practices}

- Übergeben Sie `quality=low` oder `quality=medium` explizit: `auto` ist seit 2026-08-28 der Standard und wählt für Generation und Editing unterschiedliche Qualitätsstufen.
  — <https://docs.x.ai/developers/release-notes>
- Fixieren Sie den Slug `grok-imagine-image-2.0` in neuen Integrationen; planen Sie keine neue Arbeit mit `grok-imagine-image-quality`, das zum 2026-11-02 abgeschaltet wird.
  — <https://docs.x.ai/developers/release-notes>
- Rechnen Sie Eingabebilder separat: Eine Bearbeitung berechnet sowohl das Eingabebild als auch die erzeugte Ausgabe.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
- Verwenden Sie für große, unabhängige Mengen die vom Modell unterstützte Batch API, statt das Limit von sechs Anfragen pro Sekunde in der Echtzeit-API zu überschreiten.
  — <https://docs.x.ai/developers/models/grok-imagine-image-2.0>

## Hiermit überholt {#superseded-by-this}

- 2026-08-28: Die bisherige Annahme, dass ein fehlendes `quality` `medium` bedeutet, ist überholt; nun gilt `auto`.
- 2026-09-02: Für neue Integrationen ist die Empfehlung, `grok-imagine-image-quality` zu verwenden, überholt; seine Ausmusterung ist auf den 2026-11-02 terminiert.

## Weiterhin unbekannt {#still-unknown}

- Die offizielle Seite grok.com/imagine lieferte bei der Prüfung keinen verwertbaren Text, daher sind konkrete Tarife und die geografische Verfügbarkeit der Verbraucheroberfläche nicht bestätigt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://x.ai/news/grok-imagine-image-2 | Imagine Image 2.0 | SpaceXAI | 2026-09-05 |
| https://docs.x.ai/developers/model-capabilities/imagine | Imagine Overview | SpaceXAI Docs | 2026-09-05 |
| https://docs.x.ai/developers/models/grok-imagine-image-2.0 | Grok Imagine Image 2.0 | SpaceXAI Docs | 2026-09-05 |
| https://docs.x.ai/developers/release-notes | Release Notes | SpaceXAI Docs | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:grok-imagine-image-2-0`, Thread `grok-imagine-image`, 1 datiertes Ereignis vom 2026-08-10 bis 2026-08-10.
- **Praktischer Hinweis:** Ab 2026-08-10 sollten Praktiker, die Grok Imagine evaluieren, Image 2.0 als datierten Meilenstein der Produktlinie behandeln und die verlinkten Seiten von xAI und Grok konsultieren; Funktionen, Zugang und Verfügbarkeit müssen sie vor einer Abhängigkeit separat prüfen.
- **Konfidenz:** hoch. Die datierten Überholungen oben sind maßgeblich dafür, was veraltet ist.
