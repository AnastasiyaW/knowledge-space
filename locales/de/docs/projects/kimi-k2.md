---
title: "Kimi K2"
category: projects
date: 2025-07-13
tags: [kimi, kimi-k2, kimi-k2-development, project]
aliases: ["Kimi", "Kimi K2"]
level: 3
source_sha256: 68446357ebcae07371922b1587f362c38ace0dbf3bfe64aa92379cfd286b9c1a
translation: machine
translated_at: '2026-10-24'
---
# Kimi K2 {#kimi-k2}

**Entwicklungslinie:** `project:kimi-k2` · Thread `kimi-k2-development`  
**Letztes Ereignis:** 2025-07-13 · 1 datierter Eintrag seit 2025-07-13 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Kimi K2 ist eine Open-Weight-MoE-Sprachmodellfamilie für Entwickler, die ein selbst gehostetes Modell für Text- und Tool-Use benötigen und nicht die aktuelle gehostete Kimi-API.

- Kimi-K2-Base für Forschung und Fine-Tuning.
- Kimi-K2-Instruct für Chat und Agent-Loops.
- Lokales OpenAI-kompatibles Chat- und Tool-Calling; die frühere gehostete API bot außerdem Anthropic-Kompatibilität.

## Entwicklungslinie {#development-line}

- **2025-07-13 — Verweise zur öffentlichen Verfügbarkeit von Kimi K2.** Am 2025-07-13 verzeichneten offizielle Links zu Projekt, Quellcode, Modellherausgeber, Web-Chat und mobilem Zugang Kimi K2. Diese datierten Verweise markieren einen Meilenstein der öffentlichen Verfügbarkeit des Projekts. Der genaue Wortlaut der Veröffentlichung und die Versionsdetails sind anhand der Quellenrecherche noch zu verifizieren.

## Was sich geändert hat {#what-changed}

- 2025-07-13 — Kimi K2 Base und Instruct waren bereits öffentlich. Offizielle Einträge datieren das initiale Modell und die API-Veröffentlichung kimi-k2-0711-preview auf 2025-07-11, daher ist der 13. Juli keine eigenständige K2-Version.
- 2025-08-01 — kimi-k2-turbo-preview ergänzte eine hochperformante gehostete Option mit einer zeitlich begrenzten Startaktion von 50 % Rabatt.

## Anwendung {#how-to-use-this}

Ab 2025-07-13 sollte Kimi K2 anhand offizieller Projekt- und Quellenverweise bewertet werden, nicht anhand von Zusammenfassungen Dritter. Die Verfügbarkeit des Modells auf der Entwicklerplattform ist vor einer API-Integration separat zu prüfen.

1. Wählen Sie zuerst den Weg: K2 nur für eine bestehende selbst gehostete oder reproduzierbare Bereitstellung beibehalten. Für eine neue gehostete Integration ein aktuell gelistetes Kimi-Modell wählen, da alle kimi-k2-API-IDs eingestellt sind.
  — <https://platform.kimi.ai/docs/models>
2. Für lokalen Chat oder Agenten mit dem offiziellen Kimi-K2-Instruct-Checkpoint beginnen, nicht mit Base. Base ist der Basis-Checkpoint für Forschung und eigenes Post-Training.
  — <https://github.com/MoonshotAI/Kimi-K2>
3. Die K2-Gewichte mit einer der offiziell empfohlenen Engines bereitstellen: vLLM, SGLang, KTransformers oder TensorRT-LLM.
  — <https://huggingface.co/moonshotai/Kimi-K2-Instruct>
4. Die lokale Chat-Completions-Schnittstelle verwenden und Kimi-K2-Instruct mit Temperatur 0,6 starten. Einen System-Prompt beibehalten, wenn keine besondere Anweisung nötig ist.
  — <https://huggingface.co/moonshotai/Kimi-K2-Instruct>
5. Für eine Tool-Schleife die verfügbaren Tool-Schemata senden, den zurückgegebenen Aufruf in der Anwendung ausführen, das Ergebnis anhängen und fortfahren, bis die Completion keine Tools mehr anfordert.
  — <https://github.com/MoonshotAI/Kimi-K2>
6. Für einen neuen Kimi-API-Aufruf einen API-Schlüssel erstellen, die aktuelle Modell-ID aus der Modellliste verwenden und POST /v1/chat/completions unter https://api.moonshot.ai/v1 aufrufen.
  — <https://platform.kimi.ai/docs/api/chat>

## Bewährte Vorgehensweisen {#best-practices}

- Aufgabe, relevanten Kontext, Ausgabeformat und Ziellänge explizit angeben. Der Prompt-Leitfaden warnt, dass das Modell nicht genannte Anforderungen nicht erschließen kann.
  — <https://platform.kimi.ai/docs/guide/prompt-best-practice>
- Bereitgestelltes Material mit Trennzeichen abgrenzen und bei mehrstufigen Aufgaben die Schritte in fester Reihenfolge ausformulieren.
  — <https://platform.kimi.ai/docs/guide/prompt-best-practice>
- Repräsentative Beispiele verwenden, wenn Ausgabestil oder Schema wichtig sind. Wenn Fundierung erforderlich ist, verlangen, dass Antworten im bereitgestellten Referenzmaterial bleiben.
  — <https://platform.kimi.ai/docs/guide/prompt-best-practice>
- Tool-Calling nicht als einzelne Anfrage behandeln: Die zurückgegebene Tool-Call-Nachricht des Assistenten beibehalten und jedes Tool-Ergebnis anhängen, bevor das Modell zum Fortfahren aufgefordert wird.
  — <https://huggingface.co/moonshotai/Kimi-K2-Instruct>
- Historische K2-Preview-Namen für die gehostete Nutzung nicht fest im Code verankern. Sie sind eingestellt und nicht mehr unterstützt, daher migrieren und die aktuelle Modellliste neu prüfen.
  — <https://platform.kimi.ai/docs/models>
- API-Verkehr auf Nutzerebene budgetieren, nicht auf Schlüsselebene: Limits für Parallelität, RPM, TPM und TPD gelten modellübergreifend gemeinsam.
  — <https://platform.moonshot.ai/docs/introduction#text-generation-model>

## Abgelöst durch {#superseded-by-this}

- 2025-09-05 — kimi-k2-0711-preview als aktuelles gehostetes K2-Modell für neue Integrationen; abgelöst durch kimi-k2-0905-preview.
- 2026-05-25 — jede kimi-k2-Preview-, Turbo- oder Thinking-Kennung als unterstütztes gehostetes API-Ziel; die K2-Serie wurde eingestellt.
- 2026-08-31 — kimi-k2.5 als unterstützter API-Fallback für Integrationen aus der K2-Ära; es wurde außer Betrieb genommen.

## Weiterhin unbekannt {#still-unknown}

- Die Quellenlinks belegen die öffentlichen Artefakte und Veröffentlichungen von K2, nicht aber die genauen Aussagen der Meldungen vom 2025-07-13 und 2025-08-01, deren Text nicht verfügbar ist.
- Die Erstanbieter-Daten widersprechen sich. Das Plattform-Changelog, die Ankündigung zu 0905 und der Recherche-Katalog datieren die ursprüngliche K2-Veröffentlichung auf 2025-07-11, während die aktuelle Übersicht zu Kimi Agent 2025-09-05 nennt. Letzteres könnte das Update 0905 meinen, wird dort aber nicht ausdrücklich korrigiert.
- Die Kimi-App-Links vom Juli 2025 und die Veröffentlichung von K2 gehören zusammen, belegen aber nicht, welche Modellversion an diesem Tag den jeweiligen App-Client antrieb.
- Offizielle Quellen nehmen K2 aus der gehosteten API heraus, nennen aber keine Richtlinie zu Wartung oder Sicherheitsunterstützung nach der Abschaltung für selbst gehostete K2-Gewichte.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/MoonshotAI/Kimi-K2 | Kimi K2 ist die große Sprachmodellserie des Moonshot-AI-Teams | 2026-09-04 |
| https://moonshotai.github.io/Kimi-K2/ | Kimi K2: Offene agentische Intelligenz | 2026-09-04 |
| https://huggingface.co/moonshotai/Kimi-K2-Instruct | moonshotai/Kimi-K2-Instruct | 2026-09-04 |
| https://platform.moonshot.ai/docs/introduction#text-generation-model | Grundkonzepte – Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/docs/models | Modellliste – Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/docs/api/chat | Chat-Completions-API – Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/docs/guide/prompt-best-practice | Best Practices für Prompts – Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/blog/posts/changelog | Kimi Open Platform: Protokoll neuer Funktionen | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2 | Kimi K2: Offene agentische Intelligenz | 2026-09-04 |
| https://arxiv.org/abs/2507.20534 | Kimi K2: Offene agentische Intelligenz | 2026-09-04 |
| https://platform.kimi.com/blog/posts/kimi-k2-0905 | Kimi K2 模型更新，带来更强的代码能力、更快的 API | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2-thinking | Einführung von Kimi K2 Thinking | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2-5 | Kimi K2.5: Visuelle agentische Intelligenz | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2-6 | Kimi K2.6: Fortschritte bei quelloffenem Coding | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k3 | Kimi K3: Offene Spitzenintelligenz | 2026-09-04 |
| https://www.kimi.com/en/blog/ | Kimi Research-Blog | Moonshot AI | 2026-09-04 |
| https://github.com/MoonshotAI/kimi-help-center/blob/master/en-US/agent/overview.md | Übersicht Kimi Agent | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:kimi-k2`, Thread `kimi-k2-development`, 1 datierter Eintrag, 2025-07-13 → 2025-07-13.
- **Praktischer Hinweis:** Ab 2025-07-13 sollte Kimi K2 anhand offizieller Projekt- und Quellenverweise bewertet werden, nicht anhand von Zusammenfassungen Dritter. Die Verfügbarkeit des Modells auf der Entwicklerplattform ist vor einer API-Integration separat zu prüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Ablösungsangaben als maßgeblich.
