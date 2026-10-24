---
title: "Qwen 3.6 Plus Preview — Öffentliche Modellverfügbarkeit"
category: projects
date: 2026-03-31
tags: [project, public-model-availability, qwen, qwen-3-6-plus-preview]
aliases: ["Qwen 3.6 Plus Preview"]
level: 2
source_sha256: 11f18cc766d92b7128b3c2ff5b8dadaf0aaa14a51ee1f58ac6f4998cb1d37510
translation: machine
translated_at: '2026-10-24'
---
# Qwen 3.6 Plus Preview — Öffentliche Modellverfügbarkeit {#qwen-36-plus-preview-public-model-availability}

**Entwicklungslinie:** `project:qwen-3-6-plus-preview` · Thread `public-model-availability`  
**Letztes Ereignis:** 2026-03-31 · 1 datiertes seit 2026-03-31 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Qwen 3.6 Plus Preview ist ein von Qwen gehostetes Preview-Modell, das auf OpenRouter als `qwen/qwen3.6-plus-preview:free` verfügbar ist.

- Agentisches Coding, Frontend-Arbeit und allgemeines logisches Schlussfolgern.
- Kontextfenster von 1.000.000 Token.
- OpenRouter führt das Modell als kostenlos, could aber Prompts und Completions zur Verbesserung des Modells verwenden.

## Entwicklungslinie {#development-line}

- **2026-03-31 — OpenRouter-Verfügbarkeitssignal für Qwen 3.6 Plus Preview.** Am 2026-03-31 verknüpfte der Eintrag Qwen 3.6 Plus Preview mit einer OpenRouter-URL, die als kostenloser Endpunkt gekennzeichnet war. Vorgeschlagen wird, dieses datierte Signal zur öffentlichen Verfügbarkeit festzuhalten, nicht einen verifizierten Modellstart: Die vorliegenden Belege belegen weder den Betreiber, die Fähigkeiten, die Nutzungsbedingungen noch, ob der Endpunkt an diesem Datum live war.

## Was sich geändert hat {#what-changed}

2026-03-31 — Qwen 3.6 Plus Preview wurde über OpenRouter als kostenloser Preview-Endpunkt verfügbar; OpenRouter nennt als Veröffentlichungsdatum 2026-03-30. 2026-04-03 — ein ungeklärter Community-Bericht besagte, dass das Modell über die internationale DashScope-API nicht verfügbar sei, obwohl es in Qwen Chat und im kostenlosen Qwen Code CLI verfügbar sei.

## Verwendung {#how-to-use-this}

Ab 2026-03-31 sollten Praktiker Qwen 3.6 Plus Preview nur dann als mögliche kostenlose OpenRouter-Endpunkt-Option behandeln, wenn sie die aktuelle Verfügbarkeit und die Nutzungsbedingungen geprüft haben; dieser Eintrag stellt keine Behauptungen zu Fähigkeiten oder Herkunft auf.

1. Erstellen Sie einen OpenRouter-API-Schlüssel und senden Sie dann eine standardmäßige OpenAI-kompatible Anfrage an `POST /api/v1/chat/completions` mit dem Modell `qwen/qwen3.6-plus-preview:free`.
  — <https://openrouter.ai/docs/api_reference/overview>
2. Beginnen Sie mit einer begrenzten Evaluierungsaufgabe, etwa einer Repository-Prüfung oder der Analyse langer Dokumente; reichen Sie keine vertraulichen Inhalte ein, da die Modellseite angibt, dass Prompts und Completions zur Verbesserung erfasst werden können.
  — <https://openrouter.ai/qwen/qwen3.6-plus-preview:free>
3. Bei Kontingentfehlern prüfen Sie den Schlüssel-Endpunkt und beachten `Retry-After`; verwenden Sie exponentielles Backoff bei 429-Antworten.
  — <https://openrouter.ai/docs/api_reference/limits>

## Bewährte Praktiken {#best-practices}

- Behandeln Sie dies als Evaluierungspfad für eine Preview: Fixieren Sie die exakte Modell-ID und bewahren Sie Ausgaben aus repräsentativen Tests auf, bevor Sie das Modell zu einer Abhängigkeit machen.
  — <https://openrouter.ai/qwen/qwen3.6-plus-preview:free>
- Senden Sie keine sensiblen Prompts oder Completions über diesen Endpunkt, da OpenRouter angibt, dass sie zur Modellverbesserung erfasst werden können.
  — <https://openrouter.ai/qwen/qwen3.6-plus-preview:free>
- Implementieren Sie Backoff und Kontingentüberwachung für Anfragen an kostenlose Modelle; Kapazitätsengpässe des Anbieters und Plattformlimits können 429-Fehler auslösen.
  — <https://openrouter.ai/docs/api_reference/limits>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- 2026-03-31: Die Annahme, das Veröffentlichungsdatum sei definitiv der 31. März gewesen, wird durch die aktuelle Modellseite von OpenRouter korrigiert, die den 30. März 2026 angibt.
- 2026-03-31: Qwen 3.6 Plus Preview als lokale oder Open-Weight-Qwen-Veröffentlichung zu behandeln, ist nicht belegt; der verifizierte Zugriffsweg ist der gehostete OpenRouter-Eintrag.

## Weiterhin unbekannt {#still-unknown}

- Für genau dieses Modell wurde keine Modellkarte von Qwen selbst, kein Benchmark-Bericht, keine Parameteranzahl, keine Architekturspezifikation, keine Preise nach der Preview-Phase und keine formale Verfügbarkeitserklärung gefunden.
- Die Behauptung vom 3. April zur DashScope-Verfügbarkeit ist ein Nutzerbericht in einem Qwen-GitHub-Issue, keine Bestätigung durch Maintainer.
- Die aktuelle OpenRouter-Seite ist weiterhin erreichbar und kennzeichnet das Modell als kostenlos, doch eine öffentliche Seite allein belegt weder Kapazität, Provider-Routing noch Eignung für Produktivverkehr.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://openrouter.ai/qwen/qwen3.6-plus-preview:free | Qwen3.6 Plus Preview - API Pricing & Providers | OpenRouter | 2026-09-05 |
| https://openrouter.ai/docs/api_reference/overview | OpenRouter API Reference - Complete Documentation | 2026-09-05 |
| https://openrouter.ai/docs/api_reference/limits | API Credit & Rate Limits - Handle 402 and 429 Errors | 2026-09-05 |
| https://github.com/QwenLM/Qwen3/issues/1838 | Qwen3.6 Plus - International API Access? · Issue #1838 · QwenLM/Qwen3 | 2026-09-05 |
| https://www.ithome.com/0/934/546.htm | 阿里通义千问 Qwen 3.6 Plus 免费预览版上线 OpenRouter | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:qwen-3-6-plus-preview`, Thread `public-model-availability`, 1 datiertes Ereignis 2026-03-31 → 2026-03-31.
- **Praktischer Hinweis:** Ab 2026-03-31 sollten Praktiker Qwen 3.6 Plus Preview nur dann als mögliche kostenlose OpenRouter-Endpunkt-Option behandeln, wenn sie die aktuelle Verfügbarkeit und die Nutzungsbedingungen geprüft haben; dieser Eintrag stellt keine Behauptungen zu Fähigkeiten oder Herkunft auf.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
