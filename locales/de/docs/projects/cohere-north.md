---
title: "North"
category: projects
date: 2026-06-30
tags: [cohere, cohere-north, north-mini-code, project]
aliases: ["North"]
level: 2
source_sha256: 9f2decf3b570aaf683f04dc55cf02bbfd9b93dfa51c3c362bffece3411c57d20
translation: machine
translated_at: '2026-10-24'
---
# North {#north}

**Entwicklungslinie:** `project:cohere-north` · Thread `north-mini-code`  
**Letztes Ereignis:** 2026-06-30 · 1 datiertes seit 2026-06-30 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Cohere North Mini Code ist ein Text-Sparse-MoE-Modell für Engineers, die eine lokale Alternative zu kleinen agentischen Code-Modellen benötigen.
- Codegenerierung.
- Ausführung von Terminal-Tools.
- Mehrschrittige agentische Aufgaben.
- Strukturierte Tool-Aufrufe.

30B Parameter insgesamt, 3B aktiv, 256K Kontext, Generierung bis zu 64K Tokens. Es eignet sich für kontrollierte Coding-Agent-Harnesses, erfordert jedoch eine kompatible Runtime und die korrekte Weitergabe des Tool- und Thinking-Zustands.

## Entwicklungslinie {#development-line}

- **2026-06-30 — CohereLabs veröffentlichte die Modellseiten von North Mini Code 1.0 auf Hugging Face.** Am 2026-06-30 verweist die Entwicklungslinie auf die Hugging-Face-Seiten für North-Mini-Code-1.0 und eine w4a16-Variante. Dies markiert einen wesentlichen Verteilungsschritt für die Linie North Mini Code, da sowohl ein Basismodell-Artefakt als auch eine eigenständig benannte Variante identifiziert werden.

## Was sich geändert hat {#what-changed}

- 2026-06-09 — Cohere veröffentlichte North-Mini-Code-1.0 unter Apache 2.0 als erstes Modell der North-Familie für agentische Workflows und stellte BF16-, FP8- und W4A16-Gewichte bereit.
- 2026-06-30 — Repositories für das Basismodell North-Mini-Code-1.0 und dessen W4A16-Variante wurden erfasst. Damit ist bestätigt, dass es sich um Formate eines einzigen Releases handelt und nicht um zwei getrennte Modelle.

## Verwendung {#how-to-use-this}

Ab 2026-06-30 sollten die getrennten Hugging-Face-Seiten für das Basis-Artefakt North-Mini-Code-1.0 und dessen w4a16-Variante geprüft werden, anstatt von einem einheitlichen Modellpaket auszugehen.

1. Basisgewichte über Transformers laden, das integrierte Chat-Template auf die Messages anwenden und Antworten mit den Sampling-Parametern aus der Model Card generieren.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
2. Das Modell über vLLM ausführen und `/v1/chat/completions` für einen OpenAI-kompatiblen lokalen Endpunkt aufrufen.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
3. Funktionen mit JSON Schema für einen Tool-nutzenden Agenten definieren, Tool-Ergebnisse mit der `tool`-Rolle übergeben und die Generierung fortsetzen.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>

## Bewährte Praktiken {#best-practices}

- `temperature=1.0` und `top_p=0.95` setzen, wie von Cohere für die Generierung empfohlen.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
- Interleaved-Thinking-Inhalte in nachfolgende Agent-Schritte und Konversationsrunden übernehmen, da die Model Card angibt, dass dies die Ausgabequalität verbessert.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
- Die Versionskompatibilität für vLLM prüfen: Die Model Card gibt vLLM main und `cohere_melody>=0.9.0` vor, damit Antworten korrekt geparst werden.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>

## Hierdurch überholt {#superseded-by-this}

- 2026-06-30 — Die Annahme, dass North-Mini-Code-1.0 und North-Mini-Code-1.0-w4a16 unabhängige Releases seien, ist überholt: W4A16 ist ein Gewichtsformat für North Mini Code 1.0.

## Weiterhin unbekannt {#still-unknown}

- Primärquellen bestätigen das Release vom 2026-06-09, erklären jedoch nicht, welche konkrete Änderung am 2026-06-30 erfolgte; dieses Datum könnte das Erfassen von Repositories oder die Veröffentlichung von Links widerspiegeln und keine neue Modellveröffentlichung.
- Dem System-Antwortschema fehlen die Felder `event_findings` und `new_events`; Details zu früheren Releases und zur Klärung von Ereignissen finden sich in `what_changed` und `unknowns`.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://huggingface.co/CohereLabs/North-Mini-Code-1.0 | CohereLabs/North-Mini-Code-1.0 · Hugging Face | 2026-09-05 |
| https://huggingface.co/CohereLabs/North-Mini-Code-1.0-w4a16 | CohereLabs/North-Mini-Code-1.0-w4a16 · Hugging Face | 2026-09-05 |
| https://cohere.com/blog/north-mini-code | North Mini Code: Agentic Coding für Entwickler | Cohere | 2026-09-05 |
| https://docs.cohere.com/v2/changelog | Versionshinweise | Cohere | 2026-09-05 |
| https://github.com/cohere-ai/cohere-developer-experience/blob/main/fern/pages/models/north/north-mini-code-1.0.mdx | north-mini-code-1.0.mdx | Cohere Developer Experience | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:cohere-north`, Thread `north-mini-code`, 1 datierte Ereignisse 2026-06-30 → 2026-06-30.
- **Praktischer Hinweis:** Ab 2026-06-30 sollten Praktiker, die North Mini Code bewerten, die getrennten Hugging-Face-Seiten für das Basis-Artefakt North-Mini-Code-1.0 und dessen w4a16-Variante prüfen, anstatt von einem einheitlichen Modellpaket auszugehen.
- **Konfidenz:** hoch. Die datierten Einträge unter „Hierdurch überholt“ sind maßgeblich dafür, was veraltet ist.
