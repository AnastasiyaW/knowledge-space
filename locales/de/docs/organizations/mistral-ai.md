---
title: "Mistral AI — Produkt- und Modellveröffentlichungen"
category: organizations
tags: [mistral-ai, mistral_ai, model_releases, organization, product-and-model-releases]
aliases: ["Mistral AI"]
level: 3
source_sha256: 8e3c53dcfee52fa4afe140f0dc90cea9696627967fb76e6860a17b99c6a2beed
translation: machine
translated_at: '2026-10-24'
---
# Mistral AI — Produkt- und Modellveröffentlichungen {#mistral-ai-product-and-model-releases}

**Entwicklungslinie:** `organization:mistral-ai` · Thread `product-and-model-releases`  
**Ereignisse:** 2 datiert, 2024-02-29 → 2026-02-05 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Mistral AI ist eine gehostete Modellplattform für Entwickler, deren interaktive Oberfläche für Work, Code und Chat Vibe ist.

- Studio: APIs und eine Konsole für Textgenerierung, Agents, Document AI, RAG, Audio, Schlüssel und Nutzung.
- Vibe: interaktive Arbeit im Browser, im Terminal und in der IDE.
- Voxtral: Bausteine für Batch-Transkription, Live-Transkription und Speech-to-Speech.

## Entwicklungslinie {#development-line}

- **2024-02-29 — Mistral AI verwies auf seine Entwicklerkonsole und seine Chat-Dienste.** Am 2024-02-29 verwies Mistral AI über die angegebenen offiziellen URLs sowohl auf seine Entwicklerkonsole als auch auf seinen Chat-Dienst. Dies ist ein sichtbarer Schritt beim Produktzugang in der Unternehmensgeschichte, der eine an Entwickler gerichtete Konsole und eine Chat-Oberfläche für Endnutzer umfasst. Die angegebenen Links belegen über diese Dienste hinaus weder ein konkretes Startdatum noch einen bestimmten Funktionsumfang.
- **2026-02-05 — Mistral AI veröffentlichte Ressourcen für Voxtral-Transkription und Echtzeitmodelle.** Mini Transcribe V2 deckt Batch-Verarbeitung mit Diarisierung, Context Biasing und Zeitstempeln ab, während 4B Realtime Live-Streams abdeckt. Die verlinkte offizielle Ankündigung ist auf 2026-02-04 datiert.

## Was sich geändert hat {#what-changed}

2024-02-29 — Mistral AI stellte eine URL der Entwicklerkonsole und eine separate Chat-URL bereit.

2026-02-05 — Voxtral Transcribe 2 brachte eine Speech-to-Text-Veröffentlichung mit zwei Pfaden. Mini Transcribe V2 deckt Batch-Verarbeitung mit Diarisierung, Context Biasing und Zeitstempeln ab; 4B Realtime deckt Live-Streams ab. Die verlinkte offizielle Ankündigung ist auf 2026-02-04 datiert.

2026-09-04 (heute gefunden) — Die Konsole wird jetzt als Studio dokumentiert, eine Entwicklerplattform für API, Agents, Document AI, RAG und Audio. chat.mistral.ai öffnet nun Vibe mit den Modi Work, Code und Chat.

2026-09-04 (heute gefunden) — Die aktuelle Audio-Oberfläche umfasst außerdem TTS und eine kombinierbare Speech-to-Speech-Pipeline.

Wählen Sie eine explizite Oberfläche – Studio, Vibe, Batch-Audio oder Streaming-Audio – statt Mistral als einen generischen Chat-Endpunkt zu behandeln.

## Wie man das nutzt {#how-to-use-this}

Ab 2026-02-05 sollten Praktiker, die Mistral AI für Sprachworkflows evaluieren, die offiziellen Ressourcen für Voxtral-Transkription und Echtzeit in Betracht ziehen, einschließlich des Speech-to-Text-Pfads in der Konsole, statt das Unternehmen ausschließlich als Anbieter von Textmodellen zu betrachten.

1. Wählen Sie eine Oberfläche: Nutzen Sie Vibe für interaktive Chat-, Work- oder Code-Aufgaben und Studio, wenn Sie eine Anwendung entwickeln.  
   — [Le Chat is now Vibe](https://help.mistral.ai/en/articles/682992-le-chat-is-now-vibe)
2. Aktivieren Sie Studio, erstellen Sie einen benannten API-Schlüssel, legen Sie ein Ablaufdatum fest und wählen Sie den kleinstmöglichen Connector-Scope, der zur Integration passt.  
   — [Activate Studio and generate an API key](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key)
3. Speichern Sie MISTRAL_API_KEY in der Umgebung, installieren Sie das Python- oder TypeScript-SDK (oder nutzen Sie HTTP), senden Sie eine Chat-Completion-Anfrage und prüfen Sie anschließend die zurückgegebene Antwort.  
   — [Send your first API request](https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request)
4. Nutzen Sie Studio Playground, um Prompts zu testen, Modelle und Parameter zu vergleichen, und prüfen Sie dann die Nutzung, bevor Sie den Prompt in den Anwendungscode übernehmen.  
   — [Studio](https://docs.mistral.ai/studio)
5. Für Audio verwenden Sie Voxtral Mini Transcribe 2 für Dateien, Meetings und Archive; Voxtral Realtime nur für latenzarme Streams. Testen Sie vor der Integration eine repräsentative Datei im Speech-to-Text-Playground.  
   — [Audio](https://docs.mistral.ai/studio/audio/overview)
6. Wenn ein lokaler Streaming-Betrieb erforderlich ist, folgen Sie der offiziellen Modellkarte von Voxtral Mini 4B Realtime und dem dort dokumentierten vLLM- oder Transformers-Pfad.  
   — [Voxtral Mini 4B Realtime model card](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)

## Best Practices {#best-practices}

- Beginnen Sie im Playground. Vergleichen Sie Prompts und Parameter ohne Code und machen Sie dann die getestete Konfiguration zur Basis der Integration.  
  — [Studio](https://docs.mistral.ai/studio)
- Verwenden Sie API-Schlüssel mit Ablaufdatum und Namen. Vergeben Sie den kleinstmöglichen Connector-Scope, speichern Sie den Schlüssel einmalig in einem Secret Store und rotieren Sie ihn regelmäßig.  
  — [Activate Studio and generate an API key](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key)
- Behandeln Sie den Free-Modus als ratenbegrenzt. Implementieren Sie exponentielles Backoff für 429-Antworten.  
  — [Send your first API request](https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request)
- Wählen Sie den Audiomodus nach Workload. Batch-Mini-Transcribe-2 unterstützt Diarisierung, Zeitstempel und bis zu 100 Kontextbegriffe; Realtime ist für Live-Streaming gedacht und kann keine Diarisierung verwenden.  
  — [Audio](https://docs.mistral.ai/studio/audio/overview)
- Für Namen und Fachvokabular verwenden Sie Context Biasing im Batch-Betrieb und evaluieren Sie es für Ihre Sprache. Die Release Notes besagen, dass das Feature für Englisch optimiert ist, während die Unterstützung anderer Sprachen experimentell ist.  
  — [Voxtral Transcribe 2 release notes](https://mistral.ai/news/voxtral-transcribe-2)
- Betreiben Sie Realtime nur selbst, wenn die dokumentierte Backend- und Hardware-Umgebung eingehalten wird. Die offizielle BF16-Karte nennt eine einzelne GPU mit mindestens 16 GB für vLLM-Serving und kennzeichnet einige Alternativen als ungetestet.  
  — [Voxtral Mini 4B Realtime model card](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)

## Abgelöst durch diese Änderungen {#superseded-by-this}

- 2024-02-29 — Die Chat-Oberfläche wird nicht mehr als Le Chat beschrieben. chat.mistral.ai öffnet nun Vibe unter derselben URL mit demselben Login und bestehenden Unterhaltungen.
- 2026-02-05 — Neue Audio-Integrationen sollten Batch-Transkription und Live-Streaming nicht als austauschbar behandeln. Die aktuelle Empfehlung wählt Mini Transcribe 2 für Aufnahmen und Realtime für Streams, und Realtime kann keine Diarisierung verwenden.
- 2026-02-05 — Verwenden Sie die aktuelle Kennung des Streaming-Modells, `voxtral-mini-transcribe-realtime-2602`, statt sich nur auf den Familiennamen zu verlassen.

## Noch unbekannt {#still-unknown}

- Der Eintrag vom 2024-02-29 enthält nur Einstiegs-URLs; er nennt den genauen Funktionsumfang von Konsole oder Chat zu diesem Datum nicht.
- Das aufgeführte Ereignis ist auf 2026-02-05 datiert, während Mistrals Ankündigung auf 2026-02-04 datiert ist. Die Quelle klärt die Zeitzonen- oder Erfassungsdifferenz nicht.
- `model_releases` ist ein gemeinsamer Release-Bereich und keine Chronologie nur für Mistral. Nur das verlinkte Voxtral-Ereignis ist sicher dieser Unternehmensseite zuzuordnen.
- Eine begrenzte Suche nach vereinfachtem Chinesisch ergab keine eigene chinesischsprachige Mistral-Seite, die eine China-spezifische Betriebsempfehlung stützen würde.
- Diese Betriebspraktiken stammen aus aktueller offizieller Dokumentation und der offiziellen Modellkarte; es wurde kein unabhängiger Produktionsbericht herangezogen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://console.mistral.ai/ | Mistral Console | 2026-09-04 |
| https://chat.mistral.ai/ | Vibe Chat | 2026-09-04 |
| https://mistral.ai/news/voxtral-transcribe-2 | Voxtral transcribes at the speed of sound. | Mistral AI | 2026-09-04 |
| https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602 | mistralai/Voxtral-Mini-4B-Realtime-2602 · Hugging Face | 2026-09-04 |
| https://console.mistral.ai/build/audio/speech-to-text | Mistral Studio speech-to-text playground | 2026-09-04 |
| https://docs.mistral.ai/studio | Studio | Mistral Docs | 2026-09-04 |
| https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request | Send your first API request | Mistral Docs | 2026-09-04 |
| https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key | Activate Studio and generate an API key | Mistral Docs | 2026-09-04 |
| https://docs.mistral.ai/studio/audio/overview | Audio | Mistral Docs | 2026-09-04 |
| https://help.mistral.ai/en/articles/682992-le-chat-is-now-vibe | Le Chat is now Vibe | Mistral Help Center | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `organization:mistral-ai`, Thread `product-and-model-releases`, 2 datierte Ereignisse 2024-02-29 → 2026-02-05.
- **Praktischer Hinweis:** Ab 2026-02-05 sollten Praktiker, die Mistral AI für Sprachworkflows evaluieren, die offiziellen Ressourcen für Voxtral-Transkription und Echtzeit in Betracht ziehen, einschließlich des Speech-to-Text-Pfads in der Konsole, statt das Unternehmen ausschließlich als Anbieter von Textmodellen zu betrachten.
- **Konfidenz:** mittel. Maßgeblich für die Frage, was veraltet ist, sind die datierten Abschnitte „Abgelöst durch diese Änderungen“.
