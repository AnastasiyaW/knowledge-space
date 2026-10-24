---
title: "GPT-4"
category: projects
tags: [announcements, gpt-4, gpt-4-development, gpt_4_architecture, project]
aliases: ["GPT-4"]
level: 3
source_sha256: dcb23f62395c34ce6cc9e19384bb7372296fd187d7f0f9df9ab7499e603c5e4c
translation: machine
translated_at: '2026-10-24'
---
# GPT-4 {#gpt-4}

**Entwicklungslinie:** `project:gpt-4` · Thread `gpt-4-development`  
**Ereignisse:** 1 datiert, 2023-03-09 → 2023-03-09 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

GPT-4 ist ein älteres OpenAI-Modell zur Aufrechterhaltung bestehender, rein textbasierter API-Integrationen.

- Text: nimmt Text entgegen und gibt Text zurück.
- Streaming: unterstützt Streaming.
- Fine-Tuning: unterstützt Fine-Tuning.
- Chat Completions: dokumentierte Schnittstelle.

8.192-Token-Kontext; 30 $ Input und 60 $ Output pro einer Million Token; Bild, Audio, Video, Function Calling und Structured Outputs werden nicht unterstützt.

Behalten Sie es nur dort, wo Kompatibilität gemessen wird; verwenden Sie für neue Arbeiten ein neueres Modell.

## Entwicklungslinie {#development-line}

- **2023-03-09 — Vorabprognose für GPT-4.** Am 2023-03-09 erklärte Microsoft Deutschland, dass GPT-4 in der folgenden Woche erwartet werde und multimodal sein würde. Diese Aussage war eine Behauptung vor der Veröffentlichung über erwartete Fähigkeiten, keine Bestätigung einer Veröffentlichung.

## Was sich geändert hat {#what-changed}

GPT-4 wandelte sich von einer allgemeinen Veröffentlichung zu einem abgelösten ChatGPT-Modell mit einer Rolle als Legacy-API.

- 2023-03-09: Berichte vor der Veröffentlichung prognostizierten einen unmittelbar bevorstehenden multimodalen Start.
- 2023-03-14: OpenAI kündigte GPT-4 mit Text- und Bildeingabe sowie Textausgabe an. Der öffentliche Zugang wurde mit Text eröffnet, während Bildeingabe in einer eingeschränkten Alpha blieb.
- 2023-06-22: Ein Eintrag zur Architektur hat keine URL, daher lässt sich keine Architekturänderung verifizieren.
- 2023-07-06: Der API-Zugang wurde für zahlende Entwickler allgemein verfügbar, mit der Empfehlung, Chat Completions statt der älteren Completions zu verwenden.
- 2025-04-30: OpenAI entfernte GPT-4 aus ChatGPT und ersetzte es durch GPT-4o, während die API aktiv blieb.
- 2026-09-04: Die Modellseite zeigt `gpt-4` als älteres Standardmodell, während der Katalog GPT-4 als Deprecated klassifiziert.

Die dokumentierten Betriebsgrenzen bleiben ein 8.192-Token-Kontext und 30 $/60 $ pro einer Million Text-Token.

Behandeln Sie GPT-4 als Legacy-API-Modell zur Kompatibilität, nicht als Option für ChatGPT.

## So verwenden Sie es {#how-to-use-this}

Behandeln Sie Berichte vom 2023-03-09 als vorläufig, bis die primäre Dokumentation die Fähigkeiten zum Veröffentlichungszeitpunkt bestätigt.

1. Verzichten Sie in ChatGPT auf GPT-4, da OpenAI es dort am 2025-04-30 entfernt hat; siehe die [ChatGPT-Versionshinweise](https://help.openai.com/en/articles/6825453). Verwenden Sie es nur, wenn bestehende API-Integrationen gemessenes Legacy-Verhalten erfordern.
2. Senden Sie vor dem Deployment eine authentifizierte Anfrage `GET /v1/models/gpt-4`, um sichtbare Modell-IDs und Abschaltdaten über die [Models API](https://developers.openai.com/api/reference/resources/models) zu prüfen.
3. Senden Sie geordnete Textnachrichten mit dem Modell `gpt-4` über den dokumentierten Endpunkt `POST /v1/chat/completions`, wie in [Chat Completions](https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions) beschrieben.
4. Führen Sie aufgabenspezifische Evaluierungen durch, bevor Sie GPT-4 behalten oder ersetzen, und entscheiden Sie anhand von Kosten, Funktionen und Benchmark-Werten aus den [Best Practices für Evaluierungen](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

## Best Practices {#best-practices}

- Führen Sie aufgabenspezifische Evaluierungen kontinuierlich durch und kalibrieren Sie automatisierte Bewertungen mit menschlichem Urteil, gemäß den [Best Practices für Evaluierungen](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
- Halten Sie eine menschliche Prüfung für Ausgaben mit hohem Risiko aufrecht und stellen Sie Prüfern Quellmaterial zur Verfügung, um Antworten zu verifizieren, gemäß den [Sicherheits-Best-Practices](https://developers.openai.com/api/docs/guides/safety-best-practices).
- Vermeiden Sie es, GPT-4-Workflows um Bilder, Audio, Tools oder Structured Outputs herum zu entwerfen, da die [GPT-4-Modellreferenz](https://developers.openai.com/api/docs/models/gpt-4) diese als nicht unterstützt auflistet.
- Halten Sie API-Schlüssel aus dem Quellcode heraus, trennen Sie Staging von Produktion und richten Sie Ausgabenwarnungen ein, bevor der Traffic beginnt, wie in den [Best Practices für den Produktionsbetrieb](https://developers.openai.com/api/docs/guides/production-best-practices) beschrieben.

## Hierdurch überholt {#superseded-by-this}

- 2023-03-09: Die Behandlung von Prognosen vor der Veröffentlichung als bestätigte Verfügbarkeit wurde durch den Start von OpenAI am 2023-03-14 überholt.
- 2023-03-14: Die Anleitung, GPT-4 in ChatGPT auszuwählen, wurde am 2025-04-30 obsolet, als ChatGPT es durch GPT-4o ersetzte.
- 2023-03-14: Die Behandlung von Bildeingabe als API-Fähigkeit ist obsolet, da sie beim Start in einer eingeschränkten Alpha blieb und die aktuelle `gpt-4`-Seite sie als nicht unterstützt auflistet.
- 2023-07-06: Die Anleitung zur allgemeinen Verfügbarkeit ist veraltet, da die aktuelle Dokumentation GPT-4 als älter bezeichnet, es im Katalog als Deprecated einstuft und eine Kontoverifizierung verlangt.

## Weiterhin unbekannt {#still-unknown}

- Der Eintrag `gpt_4_architecture` vom 2023-06-22 hat weder eine URL noch öffentlichen Text, daher lässt sich keine Aussage zur Architektur verifizieren.
- Der Eintrag vom 2023-03-09 und die separaten Routen `openai_gpt4` / `gpt4_development` stehen im Register im Konflikt; es bleibt unklar, ob es sich um doppelte Routen oder getrennte Themen handelt.
- Die offizielle Dokumentation widerspricht sich selbst: Die Detailseite zu GPT-4 zeigt einen Standard-Alias `gpt-4`, während der Katalog GPT-4 als Deprecated führt. Eine authentifizierte Prüfung über die Models API muss den Zugriff bestätigen.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.heise.de/news/GPT-4-is-coming-next-week-and-it-will-be-multimodal-says-Microsoft-Germany-7540972.html | GPT-4 is coming next week and it will be multimodal, says Microsoft Germany — Heise (aktueller Zugriff umgeleitet) | 2026-09-04 |
| https://openai.com/index/gpt-4-research/ | GPT-4 — OpenAI | 2026-09-04 |
| https://community.openai.com/t/gpt-4-api-general-availability-and-deprecation-of-older-models-in-the-completions-api/289518 | GPT-4 API general availability and deprecation of older models in the Completions API — OpenAI Developer Community | 2026-09-04 |
| https://openai.com/index/gpt-4-api-general-availability/ | GPT-4 API general availability and deprecation of older models in the Completions API — OpenAI | 2026-09-04 |
| https://help.openai.com/en/articles/6825453 | ChatGPT — Release Notes — OpenAI Help Center | 2026-09-04 |
| https://developers.openai.com/api/docs/models/gpt-4 | GPT-4 Model — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/models/all | All models — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/reference/resources/models | Models — OpenAI API reference | 2026-09-04 |
| https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions | Completions — OpenAI API reference | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/evaluation-best-practices | Evaluation best practices — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/safety-best-practices | Safety best practices — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/production-best-practices | Production best practices — OpenAI API | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:gpt-4`, Thread `gpt-4-development`, 1 datiertes Ereignis 2023-03-09 → 2023-03-09.
- **Praktischer Hinweis:** Behandeln Sie Berichte Dritter über eine multimodale Veröffentlichung von GPT-4 ab dem 2023-03-09 als vorläufig, bis die primäre Dokumentation die Verfügbarkeit bestätigt.
- **Konfidenz:** mittel. Die datierten Überholungs-Einträge oben sind maßgeblich dafür, was veraltet ist.
