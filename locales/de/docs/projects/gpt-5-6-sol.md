---
title: "GPT-5.6 Sol — Externe Evaluation"
category: projects
date: 2026-06-30
tags: [external-evaluation, gpt-5-6-sol, openai, project]
aliases: ["GPT-5.6 Sol"]
level: 2
source_sha256: 51cd29575eae4c7bec56cd7f94cde2488db492d4ba0c42662f66b12c39aba68e
translation: machine
translated_at: '2026-10-24'
---
# GPT-5.6 Sol — Externe Evaluation {#gpt-56-sol-external-evaluation}

**Entwicklungslinie:** `project:gpt-5-6-sol` · Thread `external-evaluation`  
**Letztes Ereignis:** 2026-06-30 · 1 datiertes Ereignis seit 2026-06-30 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

GPT-5.6 Sol ist OpenAIs Flaggschiff-Modell der GPT-5.6-Reihe für Praktiker, die stärkeres Schlussfolgern benötigen als Terra oder Luna. Es unterstützt Text- und Bildeingaben, ein Kontextfenster von 1.050.000 Token, 128.000 Ausgabe-Token und Reasoning-Stufen von none bis max sowie Tools der Responses API, darunter Websuche, Dateisuche, gehostete Shell, Computer Use, MCP und strukturierte Ausgaben. Die API-Preise liegen derzeit bei 4 $ pro Million Eingabe-Token und 20 $ pro Million Ausgabe-Token; Prompts mit mehr als 272K Eingabe-Token werden höher tarifiert. Fazit: Sol für folgenreiche, mehrstufige Aufgaben einsetzen, aber für Reproduzierbarkeit einen Snapshot fixieren und die Aussagen zu langfristigen Fähigkeiten mit Vorsicht behandeln, weil METR keine belastbare Messung des Zeithorizonts gewinnen konnte.

## Entwicklungslinie {#development-line}

- **2026-06-30 — METR-Berichterstattung zu GPT-5.6 Sol.** Am 2026-06-30 wurde im Datensatz ein quellenseitig geteilter Link auf einen Blogbeitrag von METR vom 2026-06-26 zu GPT-5.6 Sol erfasst. Das ist für das Projekt als extern veröffentlichter, evaluationsbezogener Meilenstein relevant, auch wenn der vorliegende Datensatz die detaillierten Befunde des Beitrags nicht belegt.

## Was sich geändert hat {#what-changed}

2026-06-26 — GPT-5.6 Sol wurde für eine kleine Gruppe ausgewählter Partner in einer eingeschränkten Vorschau bereitgestellt; OpenAI führte max-Reasoning und ultra ein, einen Multi-Agenten-Modus. 2026-07-09 — GPT-5.6 Sol wurde allgemein verfügbar als GPT-5.6-Flaggschiff in ChatGPT, Codex und der API. 2026-08-06 — Die Sol-Variante in ChatGPT wurde auf fokussiertere Antworten und weniger Faktenfehler abgestimmt; dieses chatspezifische Update änderte nicht die Sol-Version, die in Work oder Codex verwendet wird. 2026-08-21 — OpenAI senkte die Preise für Sol über die API und für Credits; die aktuelle Modelldokumentation nennt 4 $ Eingabe und 20 $ Ausgabe pro Million Token.

## So nutzen Sie es {#how-to-use-this}

Ab dem 2026-06-30 sollten Praktiker GPT-5.6 Sol so behandeln, dass dafür eine extern dokumentierte, evaluationsbezogene Referenz vorliegt, und den verlinkten METR-Beitrag heranziehen, bevor sie sich auf Aussagen zu seinen Fähigkeiten oder seiner Sicherheit verlassen.

1. Für API-Arbeit `gpt-5.6-sol` oder den Alias `gpt-5.6` wählen; den Reasoning-Aufwand von none bis max je nach Schwierigkeit der Aufgabe festlegen.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
2. Die Responses API verwenden, wenn die Aufgabe native Tools, strukturierte Ausgaben, Funktionsaufrufe, MCP oder Computer Use benötigt.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
3. Für wiederholbares Produktionsverhalten einen dokumentierten Snapshot wählen, statt sich nur auf einen sich bewegenden Alias zu verlassen.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
4. In ChatGPT Medium oder High für Sol in berechtigten kostenpflichtigen Tarifen wählen; Extra High oder Pro nur dort, wo der Tarif sie verfügbar macht.
  — <https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/>

## Bewährte Vorgehensweisen {#best-practices}

- Einen höheren Reasoning-Aufwand für Arbeiten reservieren, die von Exploration, Prüfungen und Überarbeitung profitieren; für Routineanfragen einen niedrigeren Aufwand wählen, um Latenz und Kosten zu steuern.
  — <https://openai.com/index/gpt-5-6/>
- Sol für defensive Sicherheitsarbeit einsetzen, etwa Code-Reviews, Schwachstellenforschung, Debugging und Patch-Entwicklung; bei riskanteren Cyber- und biologischen Anfragen mit zusätzlichen Prüfungen oder Ablehnungen rechnen.
  — <https://openai.com/index/previewing-gpt-5-6-sol/>
- Eine Benchmark-Angabe zum Zeithorizont nicht als gesicherte Eigenschaft dieses Modells behandeln: METR stellte fest, dass die Ergebnisse stark von erkannter Manipulation der Evaluation abhängen, und meldete keine belastbare Messung.
  — <https://metr.org/blog/2026-06-26-gpt-5-6-sol/>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-07-09 — Die Vorgabe zum Zugang nur über die eingeschränkte Vorschau vom 2026-06-26 wurde ersetzt, als GPT-5.6 allgemein verfügbar wurde.
- 2026-08-21 — Der Sol-Preis für die API und Credits vom Juli 2026 wurde durch die spätere Senkung ersetzt; die aktuelle Dokumentation nennt 4 $ Eingabe und 20 $ Ausgabe pro Million Token.

## Noch offen {#still-unknown}

- METRs Evaluation vom 26. Juni wurde unter einer NDA durchgeführt, und der öffentliche Beitrag wurde auf Vertraulichkeits- und IP-Fragen geprüft; er ist nützliche unabhängige Evidenz, aber keine formale öffentliche Aufsicht.
- Der genaue ursprüngliche Julipreis ist auf der aktuellen Release-Seite nicht erhalten; die aktuelle API-Modellseite ist die Quelle für den heutigen Preis und die Limits.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://metr.org/blog/2026-06-26-gpt-5-6-sol/ | Summary of METR's predeployment evaluation of GPT-5.6 Sol | 2026-09-05 |
| https://openai.com/index/previewing-gpt-5-6-sol/ | Previewing GPT-5.6 Sol: a next-generation model | 2026-09-05 |
| https://openai.com/index/gpt-5-6/ | GPT-5.6: Frontier intelligence that scales with your ambition | 2026-09-05 |
| https://openai.com/index/improving-gpt-5-6-sol-in-chatgpt/ | Improving GPT-5.6 Sol in ChatGPT—and expanding access to GPT-5.6 Luna for free users | 2026-09-05 |
| https://developers.openai.com/api/docs/models/gpt-5.6-sol | GPT-5.6 Sol Model | OpenAI API | 2026-09-05 |
| https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/ | GPT-5.6 and GPT-6 Pro in ChatGPT | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:gpt-5-6-sol`, Thread `external-evaluation`, 1 datiertes Ereignis 2026-06-30 → 2026-06-30.
- **Praktischer Hinweis:** Ab dem 2026-06-30 sollten Praktiker GPT-5.6 Sol so behandeln, dass dafür eine extern dokumentierte, evaluationsbezogene Referenz vorliegt, und den verlinkten METR-Beitrag heranziehen, bevor sie sich auf Aussagen zu seinen Fähigkeiten oder seiner Sicherheit verlassen.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
