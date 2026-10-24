---
title: "Cohere Transcribe"
category: projects
date: 2026-03-27
tags: [cohere-transcribe, project]
aliases: ["Cohere Transcribe"]
level: 2
source_sha256: b52cdcdcfa2e2a807e37e60a66673cdb8891845d5f8b0eb44ec1160074a1612c
translation: machine
translated_at: '2026-10-24'
---
# Cohere Transcribe {#cohere-transcribe}

**Entwicklungslinie:** `project:cohere-transcribe` · Thread `cohere-transcribe`  
**Letztes Ereignis:** 2026-03-27 · 1 datiertes Ereignis seit 2026-03-27 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Cohere Transcribe ist ein ASR-Modell (Automatic Speech Recognition) mit Conformer-Encoder-Decoder unter Apache-2.0 für Workflows von Audio zu Text.

- Transkribiert 14 Sprachen mit dem Basismodell `cohere-transcribe-03-2026`.
- Läuft lokal über Transformers oder vLLM oder über die Transkriptions-API von Cohere.
- Ergänzt `cohere-transcribe-arabic-07-2026` für arabische Dialekte und Arabisch-Englisch-Audio.

## Entwicklungslinie {#development-line}

- **2026-03-27 — Cohere veröffentlicht Ressourcen zu Cohere Transcribe.** Am 2026-03-27 veröffentlichte Cohere Ressourcen zu Cohere Transcribe: eine Blog-Seite, ein Hugging-Face-Modell-Repository und einen Demo-Space. Die verlinkte Model-Vault-Seite ordnet das Projekt in das Modellzugangsangebot von Cohere ein.

## Was sich geändert hat {#what-changed}

- 2026-03-27 — `cohere-transcribe-03-2026` wurde als offenes ASR-Modell mit 2B Parametern und 14 Sprachen in die Produktlinie aufgenommen; Cohere datiert die Veröffentlichung auf 2026-03-26.
- 2026-07-07 — Cohere veröffentlichte das separate 2B-Fine-Tune `cohere-transcribe-arabic-07-2026` für arabische Dialekte, Arabisch-Englisch-Sprache und Code-Switching-Workloads.

## Wie man das nutzt {#how-to-use-this}

Ab 2026-03-27 Cohere Transcribe über das veröffentlichte Modell-Repository und den Demo-Space von Cohere evaluieren und die verlinkten Cohere-Materialien auf Zugangs- und Bereitstellungsbedingungen prüfen.

1. `cohere-transcribe-03-2026` für das 14-sprachige Basismodell wählen; `cohere-transcribe-arabic-07-2026` wählen, wenn der Workload überwiegend Arabisch oder Arabisch-Englisch ist.
  — <https://docs.cohere.com/docs/audio-transcription-quickstart>
2. Für den gehosteten Weg einen Cohere-API-Schlüssel beschaffen und eine Multipart-Anfrage an `POST /v2/audio/transcriptions` senden, mit `model`, einer ISO-639-1-`language` und der Audiodatei.
  — <https://docs.cohere.com/reference/create-audio-transcription>
3. Gehostete Eingabedateien auf höchstens 25 MB begrenzen und FLAC, MP3, MPEG, MPGA, OGG oder WAV verwenden.
  — <https://docs.cohere.com/docs/audio-transcription-quickstart>
4. Für lokale Inferenz das Basis-Checkpoint mit Transformers laden, das Audio mit 16 kHz übergeben und die Sprache explizit setzen; für längere Aufnahmen den Long-Form-Chunking-Pfad aus der Model Card verwenden.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
5. Für selbst gehostetes Produktivbetrieb dem vLLM-Bereitstellungspfad von Cohere folgen und dessen OpenAI-kompatiblen Endpunkt für Audio-Transkriptionen aufrufen.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>

## Best Practices {#best-practices}

- Pro Anfrage genau eine erwartete Sprache angeben, da dem Basismodell die automatische Spracherkennung fehlt und es bei Code-Switching-Audio uneinheitlichen Text erzeugt.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
- VAD oder ein Noise Gate vor das Modell schalten, damit Stille und leises Raumrauschen keinen Text erzeugen.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
- Eine separate Stufe für Diarisierung und Zeitstempel ergänzen, wenn die Anwendung Sprecher oder Wortzeiten benötigt; das Basismodell liefert beides nicht.
  — <https://huggingface.co/CohereLabs/cohere-transcribe-03-2026>
- Für arabische Dialekte und Arabisch-Englisch-Sprache das Arabisch-Fine-Tune statt des Basismodells verwenden; Cohere berichtet bei beiden Verbesserungen gegenüber dem Basismodell.
  — <https://cohere.com/blog/transcribe-arabic>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2026-03-26 — Das Arabisch-Fine-Tune vom 2026-07-07 ersetzt das 14-sprachige Basismodell für die Transkription arabischer Dialekte und von Arabisch-Englisch; das Basismodell selbst bleibt für seinen breiteren Sprachumfang unterstützt.

## Noch unbekannt {#still-unknown}

- Es existiert keine offizielle Ankündigung oder Dokumentation zur Nutzung für vereinfachtes Chinesisch; die Unterstützung für Mandarin-Transkription begründet keine lokalisierten Betriebshinweise.
- Die berichteten Ergebnisse in Bestenlisten und zum Durchsatz sind vom Anbieter veröffentlichte Messwerte; wir haben sie nicht unabhängig reproduziert.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://cohere.com/blog/transcribe | Introducing Cohere Transcribe: a new state-of-the-art in open-source speech recognition | 2026-09-05 |
| https://huggingface.co/CohereLabs/cohere-transcribe-03-2026 | CohereLabs/cohere-transcribe-03-2026 | 2026-09-05 |
| https://huggingface.co/blog/CohereLabs/cohere-transcribe-03-2026-release | Introducing Cohere-transcribe: state-of-the-art speech recognition | 2026-09-05 |
| https://docs.cohere.com/v2/changelog | Release Notes | 2026-09-05 |
| https://docs.cohere.com/docs/transcribe | Cohere Transcribe | 2026-09-05 |
| https://docs.cohere.com/reference/create-audio-transcription | Create a transcription | 2026-09-05 |
| https://docs.cohere.com/docs/audio-transcription-quickstart | Audio Transcription - quickstart | 2026-09-05 |
| https://cohere.com/blog/transcribe-arabic | Meet Cohere Transcribe Arabic | 2026-09-05 |
| https://huggingface.co/CohereLabs/cohere-transcribe-arabic-07-2026 | CohereLabs/cohere-transcribe-arabic-07-2026 | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:cohere-transcribe`, Thread `cohere-transcribe`, 1 datiertes Ereignis 2026-03-27 → 2026-03-27.
- **Praktischer Hinweis:** Ab 2026-03-27 sollten Praktiker Cohere Transcribe über das veröffentlichte Modell-Repository und den Demo-Space von Cohere evaluieren und dabei die verlinkten Cohere-Materialien auf Zugangs- und Bereitstellungsbedingungen prüfen.
- **Konfidenz:** hoch. Die datierten Einträge unter „Durch diesen Eintrag ersetzt“ sind maßgeblich dafür, was veraltet ist.
