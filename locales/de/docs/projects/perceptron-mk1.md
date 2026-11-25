---
title: "Perceptron Mk1 — Erstveröffentlichung"
category: projects
date: 2026-05-14
tags: [initial-public-release, perceptron-mk1, perceptron_mk1, project]
aliases: ["Perceptron Mk1"]
level: 3
source_sha256: 6518c2541f51f09ac3623e8fd2d16be1dce4eb15ea99d083d96f20c8c73f6666
translation: machine
translated_at: '2026-10-24'
---
# Perceptron Mk1 — Erstveröffentlichung {#perceptron-mk1-initial-public-release}

**Entwicklungslinie:** `project:perceptron-mk1` · Thread `initial-public-release`  
**Letztes Ereignis:** 2026-05-14 · 1 datiertes Ereignis seit 2026-05-14 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

Perceptron Mk1 ist ein geschlossenes Vision-Language-Modell für Teams, die Bild- und Videoanalyse in APIs integrieren wollen, kein Videogenerator.

- Multimodale Eingabe: akzeptiert Text, Bilder und Videos.
- Strukturierte Ausgabe: liefert Text mit räumlichen oder zeitlichen Annotationen.
- Visuelle Aufgaben: unterstützt Q&A, OCR, Objekterkennung, Captioning, Videoereignis-Clipping und visuelle Beispiele im Kontext.
- Konfiguration: setzt `vision_config` für Reasoning und typisiertes Grounding.

## Entwicklungslinie {#development-line}

- **2026-05-14 — Öffentliche Vorstellung von Perceptron Mk1.** Am 2026-05-14 erschien Perceptron Mk1 auf einer öffentlichen Vorstellungsseite. Der Beitrag verlinkt eine Demo, die Dokumentation und eine Modellseite bei OpenRouter und markiert einen wesentlichen öffentlichen Entwicklungsmeilenstein. Diese Links allein belegen weder Modellfähigkeiten, technisches Design noch Zugangsbedingungen.

## Was sich geändert hat {#what-changed}

2026-05-14 — Perceptron veröffentlichte die Ankündigung zu Mk1; die offizielle Release-Historie datiert den tatsächlichen Start auf 2026-05-12 und nennt Bild- und Videoeingabe, 32K Kontext, Reasoning, Modellspezifikationen und Video-Leitfäden. 2026-06-09 — Ein eigener Endpunkt `/v1/detect` ergänzte direkte, verankerte Erkennung auf Basis von Kategorien, Beispielen oder erschöpfenden Anfragen. 2026-06-15 — Eine Files API ergänzte wiederverwendbare hochgeladene Bild- und Videoreferenzen über mehrere Anfragen hinweg. 2026-06-22 — Chat Completions erhielten zeitgestempelte Inline-`video_frames` als Alternative zu einer Video-URL.

## So wird es verwendet {#how-to-use-this}

Stand 2026-05-14: Beginnen Sie mit der öffentlichen Dokumentation und der Demo und prüfen Sie vor dem Einsatz die aktuelle Verfügbarkeit und die Bedingungen bei OpenRouter.

1. Öffnen Sie die Demo, melden Sie sich bei Aufforderung an und testen Sie vor der Integration einen konkreten Prompt an einem Beispielmaterial.
  — <https://www.perceptron.inc/demo>
2. Erstellen Sie einen Perceptron-API-Schlüssel, wählen Sie `perceptron-mk1` und verwenden Sie das Python SDK, cURL oder einen OpenAI-kompatiblen Client.
  — <https://docs.perceptron.inc/>
3. Senden Sie Text zusammen mit einer JPEG-, PNG-, WebP-, MP4- oder WebM-Datei an die Chat-Completions-API.
  — <https://docs.perceptron.inc/>
4. Legen Sie den Ergebnisvertrag vorab fest: Aktivieren Sie Thinking für Reasoning-Aufgaben oder fordern Sie die Annotationen `point`, `box`, `polygon` oder `clip` für verankerte Ausgaben an.
  — <https://docs.perceptron.inc/perceptron-mk1/models/perceptron-mk1>
5. Für Dateien, die über mehrere Anfragen hinweg wiederverwendet werden, laden Sie sie einmal hoch und referenzieren Sie die Datei-ID; jede Datei ist auf 128 MiB begrenzt.
  — <https://docs.perceptron.inc/perceptron-mk1/guides/files>
6. Als geroutete Alternative wählen Sie `perceptron/perceptron-mk1` über OpenRouter und prüfen vor dem Einsatz die aktuelle Modellkarte.
  — <https://openrouter.ai/perceptron/perceptron-mk1>

## Best Practices {#best-practices}

- Verwenden Sie überprüfbare Prompts und typisierte Ausgabeanforderungen: benannte Klassen für die Erkennung und ein exaktes Ereignisprädikat für das Clipping.
  — <https://docs.perceptron.inc/perceptron-mk1/best-practices/prompting-reference>
- Aktivieren Sie Thinking für Text-Q&A, OCR, Captioning und Clips; lassen Sie es für die Lokalisierung mit `point`, `box` und `polygon` deaktiviert.
  — <https://docs.perceptron.inc/perceptron-mk1/models/perceptron-mk1>
- Fordern Sie bei Videoclips den genauen Zeitpunkt oder Bereich an; behandeln Sie einen zurückgegebenen einzelnen Zeitstempel als ungefähren Zeitpunkt und nicht als Intervall der Länge null.
  — <https://docs.perceptron.inc/perceptron-mk1/capabilities/video-clipping>
- Halten Sie Timeouts für interaktive Anfragen und `max_tokens` knapp; skalieren Sie Medien clientseitig und berücksichtigen Sie nach einem 429 den Header `Retry-After` samt Jitter.
  — <https://docs.perceptron.inc/perceptron-mk1/guides/scaling>
- Speichern Sie Schlüssel in Umgebungsvariablen oder einem Secret Manager, entfernen Sie personenbezogene Daten aus gespeicherten Prompts und Logs und schützen Sie annotierte Beispiele als proprietäres Bildmaterial.
  — <https://docs.perceptron.inc/perceptron-mk1/best-practices/security>

## Hiermit abgelöst {#superseded-by-this}

- 2026-06-22 — Nichts dokumentiert: Das öffentliche Changelog beschreibt die Juni-Funktionen als Ergänzungen, ohne Mk1, Chat Completions oder die Eingabe `video_url` als veraltet zu markieren.

## Weiterhin unbekannt {#still-unknown}

- Der angegebene Launch-Artikel unter `https://www.perceptron.inc/blog/introducing-perceptron-mk1` lieferte bei dieser Prüfung den Status 403; sein Text und sein Veröffentlichungszeitstempel wurden daher nicht als primärer Nachweis verwendet.
- Das Datum 2026-05-14 kann eher das Erscheinen des Beitrags als den tatsächlichen Produktstart widerspiegeln; nicht verfügbarer nicht-öffentlicher Text verhindert eine Bestätigung.
- Im öffentlichen Changelog nach 2026-06-22 erscheint keine spätere Mk1-Modellrevision, wobei undokumentierte Dienständerungen weiterhin möglich sind.
- Die Erstanbieter-Dokumentation nennt 32K Kontext, während OpenRouter 33K anzeigt; OpenRouter gibt zudem 32.768 Token an, daher handelt es sich vermutlich um eine Rundung und nicht um einen wesentlichen Widerspruch.
- Es wurde keine vereinfachte chinesische Veröffentlichung des Anbieters gefunden. Die zitierte chinesische Übersicht bestätigt die Launch-Angaben, validiert aber die Leistungsangaben des Anbieters nicht unabhängig.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.perceptron.inc/demo | Perceptron-Demo | 2026-09-06 |
| https://docs.perceptron.inc/ | Schnellstart - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/models/perceptron-mk1 | Perceptron Mk1 - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/changelog | Changelog - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/best-practices/prompting-reference | Prompting-Referenz - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/capabilities/video-clipping | Video Clipping - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/guides/files | Files - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/guides/scaling | Scaling-Leitfaden - Perceptron Docs | 2026-09-06 |
| https://docs.perceptron.inc/perceptron-mk1/best-practices/security | Security - Perceptron Docs | 2026-09-06 |
| https://openrouter.ai/perceptron/perceptron-mk1 | Perceptron Mk1 - API Pricing & Providers | OpenRouter | 2026-09-06 |
| https://b.coolplus.me/archives/ai--2026-05-13 | AI 新闻摘要 2026-05-13 - 酷加的博客 | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:perceptron-mk1`, Thread `initial-public-release`, 1 datiertes Ereignis 2026-05-14 → 2026-05-14.
- **Praktischer Hinweis:** Stand 2026-05-14: Testen Sie zuerst die öffentliche Dokumentation und die Demo und prüfen Sie dann die aktuelle Verfügbarkeit und die Bedingungen bei OpenRouter, bevor Sie es einsetzen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
