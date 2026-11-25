---
title: "Gemini 3.5 Live Translate — Gemini Live-Übersetzung"
category: projects
date: 2026-06-13
tags: [gemini-3-5-live-translate, gemini-live-translation, gemini_models, project]
aliases: ["Gemini 3.5 Live Translate"]
level: 2
source_sha256: dd37c852c2cf4e4e468500bd56f82e994196e32a988cb45333b6f9f326a9d837
translation: machine
translated_at: '2026-10-24'
---
# Gemini 3.5 Live Translate — Gemini Live-Übersetzung {#gemini-35-live-translate-gemini-live-translation}

**Entwicklungslinie:** `project:gemini-3-5-live-translate` · Thread `gemini-live-translation`  
**Letztes Ereignis:** 2026-06-13 · 1 datiertes seit 2026-06-13 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Gemini 3.5 Live Translate ist Googles Audio-zu-Audio-Übersetzungsmodell mit niedriger Latenz für Echtzeit-Sprachgespräche.

- Automatische Erkennung über 70+ Sprachen
- Kontinuierlich übersetzte Sprachausgabe
- Optionale Eingabe- und Ausgabe-Transkripte

Das Modell befindet sich weiterhin in der Vorschau, akzeptiert ausschließlich Audio und unterstützt keine Tools oder Anweisungen. Verwenden Sie es als Dolmetscher-Pipeline, nicht als universellen Sprachagenten.

## Entwicklungslinie {#development-line}

- **2026-06-13 — Google stellte die Gemini 3.5 Live Translate Vorschau vor.** Am 2026-06-13 führte Google Gemini 3.5 Live Translate als Vorschau-Modell für Echtzeitübersetzung in Gemini Live ein. Die Veröffentlichung umfasste einen Live-API-Leitfaden, eine URL zur AI-Studio-Live-Vorschau sowie Integrationsreferenzen für LiveKit und Pipecat.

## Was sich geändert hat {#what-changed}

- 2026-06-13 — Gemini 3.5 Live Translate wurde Entwicklern als öffentliche Vorschau über die Gemini Live API und Google AI Studio zugänglich.
- 2026-08-26 — Google veröffentlichte die Modellkarte für Gemini 3.5 Audio. Sie dokumentierte die Kontextlimits von Live Translate mit 128K Eingabe und 64K Ausgabe sowie Fehlermodi bei Stimme, Spracherkennung und Hintergrundgeräuschen.

## Verwendung {#how-to-use-this}

Ab dem 2026-06-13 evaluieren Sie die Gemini 3.5 Live Translate Vorschau über die Gemini Live API oder AI Studio. Bestätigen Sie den LiveKit- oder Pipecat-Integrationspfad, bevor Sie ihn einsetzen.

1. Erstellen Sie einen Gemini-API-Client und öffnen Sie eine Live-API-Sitzung mit dem Modell `gemini-3.5-live-translate-preview`.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
2. Setzen Sie `response_modalities` auf Audio und übergeben Sie `translationConfig.targetLanguageCode` als BCP-47-Code der Zielsprache.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
3. Streamen Sie 16-Bit-, 16-kHz-, Mono-, Little-Endian-PCM in Blöcken von etwa 100 ms und verarbeiten Sie die zurückgelieferte 24-kHz-PCM-Audioausgabe.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
4. Aktivieren Sie Eingabe- und Ausgabe-Transkription, wenn das Produkt Untertitel, Protokollierung oder eine lesbare Übersetzung neben dem Audio benötigt.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>

## Best Practices {#best-practices}

- Behandeln Sie das Modell als kontinuierlichen Übersetzungsstrom und nicht als rundenbasierten Agenten. Der Übersetzungsmodus unterstützt keine Tools, Anweisungen, Texteingaben, Bilder oder Videos.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
- Verwenden Sie für Browser- oder Mobil-Clients v1beta-Ephemeral-Tokens und beschränken Sie `translationConfig` serverseitig, sofern Nutzer die Zielsprache nicht selbst wählen müssen.
  — <https://ai.google.dev/gemini-api/docs/live-api/live-translate>
- Testen Sie nicht-muttersprachliche Akzente, schnelles Wechseln der Sprache, lange Pausen, Gespräche mit mehreren Sprechern und laute Räume, bevor Sie sich im Betrieb auf die übersetzte Audioausgabe verlassen.
  — <https://deepmind.google/models/model-cards/gemini-3-5-audio/>
- Kalkulieren Sie sowohl für gestreamte Eingabe- als auch für erzeugte Ausgabe-Audiodaten: Google nennt einen effektiven Preis von etwa 0,0368 $ pro Minute.
  — <https://ai.google.dev/gemini-api/docs/pricing>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-06-09 — Google plante, das bisherige Limit der Sprachübersetzung in Google Meet von fünf Sprachen mit englischzentrierter Übersetzung durch 70+ Sprachen und 2.000+ Sprachkombinationen zu ersetzen.

## Weiterhin unbekannt {#still-unknown}

- Die aktuellen Seiten von LiveKit und Pipecat beschreiben generische Gemini-Live-Integrationen, nicht einen dokumentierten, speziell für Gemini 3.5 Live Translate gedachten Adapter oder eine entsprechende Konfiguration. Validieren Sie diesen Framework-Pfad, bevor Sie eines der beiden als Übersetzungsunterstützung betrachten.
- Googles öffentliches Material belegt die öffentliche Vorschau für Entwickler, nennt aber kein Datum für die allgemeine Verfügbarkeit (General Availability) des API-Modells.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-live-3-5-translate/ | Gemini 3.5 Live Translate is here | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/live-api/live-translate | Live translation with Gemini Live API | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/models/gemini-3.5-live-translate-preview | Gemini 3.5 Live Translate model reference | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/pricing | Gemini Developer API pricing | 2026-09-05 |
| https://deepmind.google/models/model-cards/gemini-3-5-audio/ | Gemini 3.5 Audio (Live Translate, Transcribe, Transcribe Live) model card | 2026-09-05 |
| https://docs.livekit.io/agents/models/realtime/plugins/gemini/ | Gemini Live API plugin | 2026-09-05 |
| https://docs.pipecat.ai/pipecat/features/gemini-live | Building with Gemini Live | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:gemini-3-5-live-translate`, Thread `gemini-live-translation`, 1 datiertes Ereignis 2026-06-13 → 2026-06-13.
- **Praktischer Hinweis:** Ab dem 2026-06-13 evaluieren Sie die Gemini 3.5 Live Translate Vorschau über die Gemini Live API oder AI Studio und bestätigen den LiveKit- oder Pipecat-Integrationspfad, bevor Sie ihn einsetzen.
- **Konfidenz:** hoch. Datierte Ersetzungshinweise sind maßgeblich für die Frage, was veraltet ist.
