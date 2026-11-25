---
title: "Lyria"
category: projects

tags: [lyria, lyria-development, project]
aliases: ["Lyria"]
level: 2
source_sha256: 03cca4b143d80a5686729addd2a6ca8d21a8c9ce1b7810efcff8d5a1287e532f
translation: machine
translated_at: '2026-10-24'
---
# Lyria {#lyria}

**Entwicklungslinie:** `project:lyria` · Thread `lyria-development`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Lyria ist das Musikgenerierungssystem von Google DeepMind für Kreative und Entwickler. Lyria 3.5 ist über Flow Music, Gemini, die Gemini API, AI Studio und Google Vids verfügbar.

- Textprompts erzeugen Musik und Liedtexte.
- Generierte Tracks tragen ein SynthID-Wasserzeichen.

Die aktuelle Produktkommunikation unterstützt Tracks von kurzen Clips bis zu maximal drei Minuten. Verwenden Sie es für originale, promptgesteuerte Musik und prüfen Sie anschließend jede Ausgabe, bevor Sie sie veröffentlichen.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht aufgearbeitet; das bekannte Wissen findet sich in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

- 2026-02-18 — Lyria 3 kam als Beta in die Gemini-App, für 30-sekündige, text- oder bildgesteuerte Tracks.
- 2026-03-25 — Google eröffnete die Developer-Preview von Lyria 3 und Lyria 3 Pro in der Gemini API und in AI Studio. Clip war auf 30-sekündige Assets ausgerichtet, Pro auf Songs von bis zu etwa drei Minuten.
- 2026-07-29 — Lyria 3.5 startete in Google Flow Music mit behaupteten Verbesserungen bei melodischer Struktur, Texttreue, Gesangsausdruck/Aussprache sowie Tempo- und Dauersteuerung.
- 2026-07-30 — Der verlinkte Launch von Flow Music entspricht Lyria 3.5, nicht einem eigenen Lyria-Modell oder einem ersten Launch. Googles primäre Ankündigung ist auf 2026-07-29 datiert, während Google Korea seine lokale Ankündigung am 2026-07-30 veröffentlichte.
- 2026-09-04 — Lyria 3.5 wurde global in Gemini (Web und mobil) sowie in der Gemini API, AI Studio und Google Vids verfügbar.

## Anwendung {#how-to-use-this}

Stand 2026-07-30: Behandeln Sie die Flow-Music-URL nicht allein als dokumentiertes Lyria-Entwicklungsereignis. Recherchieren Sie die verlinkte Ressource und den zugrunde liegenden Beitrag, bevor Sie sich darauf verlassen.

1. Öffnen Sie Google Flow Music oder Gemini, melden Sie sich an und prüfen Sie, ob die Musikgenerierungsfunktion für das Konto verfügbar ist.
  — <https://www.flowmusic.app/>
2. Wählen Sie ein Genre sowie eine Gesangs- oder Instrumentalausrichtung und legen Sie im Prompt den beabsichtigten Einsatzzweck, Tempo, Dauer, Instrumentierung und die inhaltliche Richtung der Texte fest.
  — <https://blog.google/innovation-and-ai/products/gemini-app/better-tracks-lyria-gemini/>
3. Für eine Integration verwenden Sie die Gemini API oder AI Studio. Nutzen Sie den Textmodus für ein Track-Briefing oder den Composer-Modus, um Abschnitte wie Intro, Strophe und Bridge festzulegen.
  — <https://blog.google/innovation-and-ai/technology/developers-tools/lyria-3-developers/>
4. Hören Sie den generierten Track vollständig durch und prüfen Sie, ob er zum vorgesehenen Projekt passt, bevor Sie ihn verwenden.
  — <https://deepmind.google/models/lyria/>

## Bewährte Vorgehensweisen {#best-practices}

- Beschreiben Sie konkrete musikalische Steuerungsgrößen – Tempo, Tonart, Dynamik, Gesangsstil und Abschnittsverlauf – statt sich nur auf eine Genrebezeichnung zu verlassen.
  — <https://blog.google/innovation-and-ai/technology/developers-tools/lyria-3-developers/>
- Verwenden Sie die kürzere, cliporientierte Option für schnelle Prototypen und Social-Media-Assets. Reservieren Sie die Generierung ganzer Songs für längere, strukturierte Arbeiten.
  — <https://blog.google/innovation-and-ai/technology/developers-tools/lyria-3-developers/>
- Behandeln Sie generierte Musik als Entwurf: Prüfen Sie vor der Veröffentlichung, ob der Track dem kreativen Briefing entspricht.
  — <https://deepmind.google/models/lyria/>

## Hiermit ersetzt {#superseded-by-this}

- 2026-02-18 — Das Limit von 30-Sekunden-Tracks in der Gemini-App für Lyria 3 wird für die aktuelle Nutzung durch Verbraucher durch die Optionen für kurze oder längere Tracks von Lyria 3.5 ersetzt.
- 2026-07-29 — Die Empfehlungen zu Lyria 3 werden dort ersetzt, wo Lyria 3.5 verfügbar ist. Verwenden Sie das neuere Modell für verbesserte Texte, Gesang, Musikalität sowie Tempo- und Dauersteuerung.

## Weiterhin unbekannt {#still-unknown}

- Das vorgegebene Antwortschema enthält keine Felder event_findings oder new_events; datierte Ergänzungen und Korrekturen werden daher in what_changed festgehalten und nicht als eigene Felder ausgegeben.
- Die Startseite von Flow Music lieferte auf der abgerufenen Seite keinen lesbaren Produkttext; sie ist nur als angegebene Produkt-URL und aktueller Zugangspunkt enthalten.
- Googles öffentliche Materialien enthalten weder unabhängige Benchmark-Ergebnisse noch ein vollständiges öffentliches Inventar der Trainingsdaten für Lyria 3.5.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://www.flowmusic.app/ | Google Flow Music | 2026-09-05 |
| https://blog.google/innovation-and-ai/models-and-research/google-labs/lyria-3-5/ | Introducing Lyria 3.5 in Google Flow Music | 2026-09-05 |
| https://blog.google/intl/ko-kr/company-news/technology/lyria-3-5-kr/ | Lyria 3.5 launch in Google Flow Music | 2026-09-05 |
| https://deepmind.google/models/model-cards/lyria-3-5/ | Lyria 3.5 Model Card | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/gemini-app/better-tracks-lyria-gemini/ | Create your best tracks yet with Lyria 3.5 in Gemini | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/ | A new way to express yourself: Gemini can now create music | 2026-09-05 |
| https://blog.google/innovation-and-ai/technology/developers-tools/lyria-3-developers/ | Build with Lyria 3, our newest music generation model | 2026-09-05 |
| https://deepmind.google/models/lyria/ | Lyria 3.5 | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:lyria`, Thread `lyria-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-07-30: Behandeln Sie die Flow-Music-URL nicht allein als dokumentiertes Lyria-Entwicklungsereignis. Recherchieren Sie die verlinkte Ressource und den zugrunde liegenden Beitrag, bevor Sie sich darauf verlassen.
- **Konfidenz:** hoch. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
