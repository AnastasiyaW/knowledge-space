---
title: "GPT-5.5"
category: projects
date: 2026-04-23
tags: [gpt-5-5, gpt-5-5-announcement, project]
aliases: ["GPT-5.5"]
level: 3
source_sha256: 449f2aaef4cb530c6f7bb8d84a57e7c44078a4c92a15c5d8377a39f0a2cb17a4
translation: machine
translated_at: '2026-10-24'
---
# GPT-5.5 {#gpt-55}

**Entwicklungslinie:** `project:gpt-5-5` · Thread `gpt-5-5-announcement`  
**Letztes Ereignis:** 2026-04-23 · 1 datiertes Ereignis seit 2026-04-23 · **Recherchiert:** 2026-09-06 · Konfidenz: hoch

## Was es ist {#what-it-is}

GPT-5.5 ist ein OpenAI-API-Modell für Teams, die Agenten für Coding, Tool-Nutzung und professionelle Arbeit entwickeln.

- Unterstützt Responses und Chat Completions, Function Calling, Structured Outputs, gehostete Tools, Computer Use und MCP.
- Bietet den fixierten Snapshot `gpt-5.5-2026-04-23`.

Kontextfenster von 1.050.000 Token; maximale Ausgabe von 128.000 Token; API Free wird nicht unterstützt. Behalten Sie das Modell für einen fixierten oder evaluierten Workload bei, verwenden Sie aber GPT-6 Astra als Ausgangspunkt für neue Workloads.

## Entwicklungslinie {#development-line}

- **2026-04-23 — Ankündigung von GPT-5.5.** Am 2026-04-23 markierte eine OpenAI-Ankündigung einen öffentlichen Meilenstein für GPT-5.5. Die Ankündigung bestätigt einen datierten öffentlichen Schritt des Projekts, legt aber weder Fähigkeiten, Verfügbarkeit, Preise noch Migrationsdetails fest.

## Was sich geändert hat {#what-changed}

- **2026-04-23:** GPT-5.5 wurde für berechtigte Pläne in ChatGPT und Codex ausgerollt, gedacht für Coding, Computer Use, Wissensarbeit und Recherche.
- **2026-04-24:** GPT-5.5 und GPT-5.5 Pro wurden in der API verfügbar; Schutzmaßnahmen für den API-Einsatz wurden ergänzt.
- **2026-05-05:** GPT-5.5 Instant ersetzte GPT-5.3 Instant als Standard in ChatGPT und erschien in der API als `chat-latest`.
- **2026-05-07:** GPT-5.5-Cyber ging in eine begrenzte Vorschau für Verteidiger kritischer Infrastruktur.
- **2026-05-28:** GPT-5.5 Instant erhielt ein Stil-Update für ChatGPT/API; Canvas wurde für Instant und Thinking entfernt.
- **2026-06-09:** Die Personalisierung von Instant wurde auf ChatGPT Go und Free ausgeweitet; Free nutzt dabei eine reduzierte Menge früherer Chats.
- **2026-06-24:** ChatGPT aktualisierte Instant für mehrstufigen Kontext, komplexe Randbedingungen und entscheidungsorientierte Gespräche.
- **2026-07-06:** GPT-5.5 Instant Mini ersetzte GPT-5.3 Instant Mini als Ausweichmodell in ChatGPT nach Rate-Limits von Instant oder Auto.

## So verwenden Sie das {#how-to-use-this}

1. Wählen Sie `gpt-5.5` für den gepflegten Alias oder `gpt-5.5-2026-04-23`, wenn das Verhalten fixiert bleiben muss; prüfen Sie zuerst die API-Nutzungsstufe.
  — <https://developers.openai.com/api/docs/models/gpt-5.5>
2. Verwenden Sie die Responses API für Reasoning, Tool-Aufrufe oder mehrstufige Arbeit.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
3. Beginnen Sie mit `reasoning.effort: medium`. Testen Sie `low` für latenzkritische Arbeit und erhöhen Sie den Aufwand erst nach einer repräsentativen Evaluierung.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
4. Verwenden Sie Structured Outputs, `previous_response_id` für den Antwortzustand und einen stabilen Prompt-Präfix für wiederkehrenden, gecachten Traffic.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
5. Legen Sie für ein neues System das Genauigkeitsziel mit GPT-6 Astra fest und vergleichen Sie dann Kosten und Latenz, bevor Sie GPT-5.5 beibehalten.
  — <https://developers.openai.com/api/docs/guides/model-selection>

## Best Practices {#best-practices}

- Behandeln Sie GPT-5.5 als neue Modellfamilie. Beginnen Sie mit einer neuen, minimalen Prompt-Baseline, statt einen älteren Prompt-Stack zu übernehmen.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Nennen Sie Ergebnis, Erfolgskriterien, Randbedingungen, Regeln für Belege, Ausgabeform und Abbruchbedingungen. Vermeiden Sie prozedurale Anweisungen, sofern der Weg selbst nicht vorgegeben ist.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Verwenden Sie Structured Outputs, statt ein JSON-Schema im Fließtext des Prompts zu beschreiben.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Platzieren Sie stabile Prompt-Inhalte zuerst und dynamischen Kontext zuletzt. Verwenden Sie `prompt_cache_key` konsistent und prüfen Sie die Nutzung gecachter Token.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Beschreiben Sie in Tool-Beschreibungen Tool-Eingaben, Seiteneffekte, Wiederholungssicherheit und Fehlermodi. Erhalten Sie `phase` unverändert, wenn Assistant-Items manuell wiedergegeben werden.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- :{

## Weiterhin unbekannt {#still-unknown}

- Verfügbarkeit, Rate-Limits und die Modellauswahl in ChatGPT hängen von Konto, Plan, Region und API-Stufe ab. Wir haben kein Zielkonto geprüft.
- GPT-5.5, GPT-5.5 Pro, Thinking, Instant, Cyber und Instant Mini sind unterschiedliche Varianten oder Zugriffsmodi. Zusagen zu Zugriff, Sicherheit oder Fähigkeiten dürfen nicht zwischen ihnen übertragen werden.
- Die geprüfte chinesischsprachige Launch-Seite enthält keinen separaten China-spezifischen Rollout und keine regionale API-Berechtigung.
- Die geprüften Quellen nennen kein offizielles Abschaltdatum für den API-Alias `gpt-5.5`.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://openai.com/index/introducing-gpt-5-5/ | Einführung von GPT-5.5 | 2026-09-06 |
| https://openai.com/index/gpt-5-5-system-card/ | GPT-5.5 System Card | 2026-09-06 |
| https://openai.com/zh-Hans-CN/index/introducing-gpt-5-5/ | 重磅发布 GPT-5.5 | 2026-09-06 |
| https://developers.openai.com/api/docs/models/gpt-5.5 | GPT-5.5 Model | OpenAI API | 2026-09-06 |
| https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5 | Model guidance | OpenAI API | 2026-09-06 |
| https://developers.openai.com/api/docs/guides/model-selection | Model selection | OpenAI API | 2026-09-06 |
| https://openai.com/index/gpt-5-5-instant/ | GPT-5.5 Instant: smarter, clearer, and more personalized | 2026-09-06 |
| https://openai.com/index/gpt-5-5-with-trusted-access-for-cyber/ | Scaling Trusted Access for Cyber with GPT-5.5 and GPT-5.5-Cyber | 2026-09-06 |
| https://help.openai.com/en/articles/6825453 | ChatGPT — Release Notes | 2026-09-06 |

## Agent-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:gpt-5-5`, Thread `gpt-5-5-announcement`, 1 datiertes Ereignis vom 2026-04-23 bis 2026-04-23.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** hoch. Die datierten Einträge unter „Abgelöst durch diesen Eintrag“ sind maßgeblich dafür, was veraltet ist.
