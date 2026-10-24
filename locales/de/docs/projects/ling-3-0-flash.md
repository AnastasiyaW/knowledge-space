---
title: "Ling-3.0-flash — Modellverfügbarkeit"
category: projects
date: 2026-07-27
tags: [ling-3-0-flash, ling_flash, model-availability, project]
aliases: ["Ling-3.0-flash"]
level: 3
source_sha256: 7121a3985c41133c59f10051dd5643a8471687d65ba1184e90e6f611a9ff88da
translation: machine
translated_at: '2026-10-24'
---
# Ling-3.0-flash — Modellverfügbarkeit {#ling-30-flash-model-availability}

**Entwicklungslinie:** `project:ling-3-0-flash` · Thread `model-availability`  
**Letztes Ereignis:** 2026-07-27 · 1 datierter Eintrag seit 2026-07-27 · **Recherchiert:** 2026-09-08 · Konfidenz: hoch

## Was es ist {#what-it-is}

Ling-3.0-flash ist ein textgenerierendes MoE-Modell der Ant Group für Teams, die Coding-, Tool-Use- und Long-Context-Agenten entwickeln.

- Native hybride lineare MoE-Architektur mit Reasoning und Tool Calling.
- Die OpenRouter-Route bietet kontextuell ein Fenster von 262.144 Token und bis zu 32.768 Ausgabe-Token.

124 Mrd. Parameter insgesamt, etwa 5,1 Mrd. aktiv pro Token; die OpenRouter-Route ist nur für Text verfügbar. Das Modell eignet sich für Agenten-Workloads, aber JSON-Validierung und Tool-Ausführung müssen in der Anwendung verbleiben.

## Entwicklungslinie {#development-line}

- **2026-07-27 — Ling-3.0-flash erhielt einen datierten OpenRouter-Modellverweis.** Am 2026-07-27 verlinkte ein Eintrag auf die öffentliche Modellseite von OpenRouter für InclusionAI Ling-3.0-flash. Das liefert einen datierten öffentlichen Verweis auf das Modell, belegt aber weder dessen Veröffentlichungsdatum, Fähigkeiten noch die aktuelle Verfügbarkeit des Dienstes.

## Was sich geändert hat {#what-changed}

- 2026-07-23 — Ant Ling v2.0.0 machte Ling-3.0-flash im Chat sowie über OpenAI- und Anthropic-kompatible APIs verfügbar, mit einem Schalter für Deep Thinking.
- 2026-07-24 — Die offizielle Release-Ankündigung ergänzte einen zeitlich begrenzten kostenlosen Zugang auf Ant Ling und OpenRouter.
- 2026-07-27 — Ant Ling v2.0.1 fügte das Modul Explore hinzu; es war weder ein Modell-Release für Ling-3.0-flash noch eine Änderung der Anbieterlistung.
- 2026-08-02 — Das offizielle Repository der Basisgewichte wurde angelegt und befüllt.
- 2026-08-04 — Die offiziellen Repositories der FP8- und INT4-Gewichte wurden angelegt und befüllt.

## So wird es verwendet {#how-to-use-this}

1. Sende eine OpenAI-kompatible Chat-Completions-Anfrage an OpenRouter mit der exakten Modell-ID `inclusionai/ling-3.0-flash`, einem Bearer-Key und `messages`.
  — <https://openrouter.ai/docs/quickstart>
2. Halte Prompt plus Completion innerhalb des aktuellen Kontextfensters von 262.144 Token; begrenze die Completion für den jeweiligen Workload auf 32.768 Token oder weniger.
  — <https://openrouter.ai/inclusionai/ling-3.0-flash>
3. Für Tool-Use sende `tools` und `tool_choice`, führe den zurückgegebenen Aufruf im Client aus, hänge sein Ergebnis an und stelle die nächste Modellanfrage.
  — <https://openrouter.ai/docs/guides/features/tool-calling>
4. Sende während eines produktiven Piloten `X-OpenRouter-Metadata: enabled` und speichere die zurückgegebenen Routing-Metadaten, um den ausgewählten Anbieter und etwaige Fallback-Versuche nachzuvollziehen.
  — <https://openrouter.ai/docs/guides/features/router-metadata>

## Bewährte Vorgehensweisen {#best-practices}

- Betrachte Preis-, Verfügbarkeits- und Anbieterangaben von OpenRouter als aktuelle Beobachtungen und nicht als feste Modelleigenschaft; prüfe sie erneut, bevor du Budget- oder Latenzzusagen machst.
  — <https://openrouter.ai/inclusionai/ling-3.0-flash>
- Verlass dich auf der aktuellen OpenRouter-Route nicht auf `response_format` für striktes JSON: Die Modellseite besagt, dass JSON nicht erzwungen wird. Validiere die geparsten Ausgaben in der Anwendung.
  — <https://openrouter.ai/inclusionai/ling-3.0-flash>
- Behalte die Tool-Ausführung unter Kontrolle des Clients: Das Modell schlägt einen Aufruf vor, während die Anwendung ihn ausführt und das Ergebnis zurückgibt.
  — <https://openrouter.ai/docs/guides/features/tool-calling>
- Für einen Workload mit striktem JSON-Schema verwende nur einen Endpunkt, der derzeit Structured Outputs anbietet, und verlange in den Routing-Präferenzen unterstützte Parameter.
  — <https://openrouter.ai/docs/guides/features/structured-outputs>
- Beim Self-Hosting gehe vom Sampling-Rezept des Herausgebers (`temperature=0.6`, `top_p=0.95`, `top_k=20`) und dessen laufzeitspezifischer Parser-Konfiguration aus, statt beides ungeprüft auf ein anderes Gateway zu übertragen.
  — <https://huggingface.co/inclusionAI/Ling-3.0-flash>

## Hiermit ersetzt {#superseded-by-this}

- 2026-07-27 — Das Behandeln des mit OpenRouter verknüpften Ereignisdatums als Veröffentlichungsdatum von Ling-3.0-flash; das offizielle Changelog datiert den Modellstart auf 2026-07-23, und die Änderung vom 27. Juli betrifft Explore.
- 2026-08-03 — Kostenloser API-Zugang während der Startphase; die formale Ankündigung legte das Ende auf 23:00 Uhr Pekinger Zeit fest, daher ist dies keine aktuelle Preisangabe.

## Weiterhin unbekannt {#still-unknown}

- Kein archivierter Nachweis für den ersten Listungszeitpunkt belegt, dass OpenRouter dieses Modell am 2026-07-27 erstmals bereitgestellt hat; der datierte Link belegt nur eine Beobachtung an diesem Tag.
- Der aktuelle Anbietersatz, die Preise, das Routing und die Funktionsmatrix von OpenRouter sind volatil und wurden nicht rückwirkend auf das Juli-Ereignis übertragen.
- Ling-3.0-flash-VL ist ein separat benanntes multimodales Modell; die geprüften Quellen belegen nicht, dass es ein Checkpoint-Update dieses reinen Textmodells ist.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://openrouter.ai/models/inclusionai/ling-3.0-flash | OpenRouter-Modell-URL, die mit dem datierten Ereignis angegeben wurde | 2026-09-08 |
| https://openrouter.ai/inclusionai/ling-3.0-flash | Ling 3.0 Flash - API-Preise & Benchmarks \| OpenRouter | 2026-09-08 |
| https://developer.ant-ling.com/en/docs/getting-started/changelog/ | Changelog \| Ant Ling | 2026-09-08 |
| https://developer.ant-ling.com/zh-CN/blogs/ling-3.0-flash-release | Ling-3.0-flash：智以密胜 \| Ant Ling | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash | inclusionAI/Ling-3.0-flash \| Hugging Face | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash/commits/main | Commits · inclusionAI/Ling-3.0-flash \| Hugging Face | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash-fp8/commits/main | Commits · inclusionAI/Ling-3.0-flash-fp8 \| Hugging Face | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash-int4/commits/main | Commits · inclusionAI/Ling-3.0-flash-int4 \| Hugging Face | 2026-09-08 |
| https://openrouter.ai/docs/quickstart | OpenRouter Quickstart Guide | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/tool-calling | Tool & Function Calling - Tools mit OpenRouter verwenden | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/router-metadata | Router Metadata - Routing-Entscheidungen bei jeder Antwort einsehen | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/structured-outputs | Structured Outputs - Typsichere JSON-Antworten von KI-Modellen | 2026-09-08 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:ling-3-0-flash`, Thread `model-availability`, 1 datierte Ereignisse 2026-07-27 → 2026-07-27.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich für das, was veraltet ist.
