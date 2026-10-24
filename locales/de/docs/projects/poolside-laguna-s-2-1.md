---
title: "Laguna S 2.1 — Laguna"
category: projects
date: 2026-07-22
tags: [laguna, poolside-laguna-s-2-1, project]
aliases: ["Laguna S 2.1"]
level: 4
source_sha256: 3939d2a9f90a005b9210e3c6767340f205c4c6a78a2870ee395627599dca232f
translation: machine
translated_at: '2026-10-24'
---
# Laguna S 2.1 — Laguna {#laguna-s-21-laguna}

**Entwicklungslinie:** `project:poolside-laguna-s-2-1` · Thread `laguna`  
**Letztes Ereignis:** 2026-07-22 · 1 datiertes Ereignis seit 2026-07-22 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

Laguna S 2.1 ist das Open-Weight-Modell von Poolside für Text-zu-Text-Generierung mit Mixture-of-Experts-Architektur, gedacht für Coding und für Teams, die langlaufende Software-Agenten entwickeln.

- 118 B Parameter insgesamt, etwa 8 B aktiv pro Token
- Kontextfenster mit 1.048.576 Token, verzahnte Reasoning- und Tool-Nutzung
- Gewichte auf Hugging Face sowie gehostete und lokale Serving-Pfade

Der BF16-Checkpoint benötigt rund 236 GB für die Gewichte und mehrere GPUs; quantisierte Artefakte verschieben den Hardware-Kompromiss. Wir setzen es dort ein, wo langer Kontext, die Behandlung von Tool-Aufrufen und Self-Hosting wichtig sind, validieren aber vor dem Produktivbetrieb das Harness und den genauen Checkpoint.

## Entwicklungslinie {#development-line}

- **2026-07-22 — Poolside stellte Laguna S 2.1 vor.** Am 2026-07-22 stellte Poolside Laguna S 2.1 als neuen Schritt der Laguna-Entwicklungslinie vor. Die datierten Links verknüpfen die Veröffentlichung mit einer Ankündigung, einer Seite zur Modellverteilung, Verweisen auf quantisierte Modelle sowie aufgeführten Chat- und Provider-Zugängen. Das ist relevant, weil es eine eigenständige, benannte Version des Projekts kennzeichnet.

## Was sich geändert hat {#what-changed}

- **2026-07-21** — Laguna S 2.1 wurde als MoE mit 118 B Parametern insgesamt und 8 B aktiv, mit einem Kontextfenster von 1 M Token und offenen Gewichten veröffentlicht.
- **2026-07-22** — Ein Commit zur FP8-Variante dokumentierte eine Konfiguration mit 256K ohne SpinQuant, die laut Commit das Problem agentischer Schleifen behebt; ein zweiter Commit stellte das Standard-Thinking wieder her und bewahrte das Reasoning.
- **2026-07-28** — Poolside Desktop Assistant koppelt standardmäßig pool mit Laguna S 2.1; das ist eine Integration, kein Modell-Checkpoint.
- **2026-08-01** — FP8 RC2 wurde mit einer 1M-Konfiguration und einem Hinweis auf einen neuen Checkpoint in main übernommen.
- **2026-08-02** — Das INT4/BF16-Hybrid-Release wurde mit einer 1M-Konfiguration und einem Hinweis auf einen neuen Checkpoint in main übernommen.

## Verwendung {#how-to-use-this}

1. Für einen Test ohne Code öffnen Sie Poolside Chat, prüfen, dass Laguna S 2.1 angezeigt wird, und senden Sie eine eng umrissene Coding-Aufgabe. Nutzen Sie die angebotene Registrierung bzw. Anmeldung nur, wenn sie erforderlich ist. Übermitteln Sie kein Material, dessen Verwendung zur Modellverbesserung Sie nicht zulassen können.
  — <https://chat.poolside.ai/>
2. Für einen gehosteten Zugang wählen Sie die OpenRouter-Modell-ID poolside/laguna-s-2.1. Sie akzeptiert tools und tool_choice, erzwingt aber kein JSON-response_format; strukturierte Ausgaben müssen daher im Client validiert werden.
  — <https://openrouter.ai/poolside/laguna-s-2.1>
3. Für Standard-Self-Hosting verwenden Sie das offizielle vLLM-Rezept für poolside/Laguna-S-2.1 mit Tensor-Parallelismus, den Parsern poolside_v1 für Tools und Reasoning, auto-tool choice und aktiviertem Thinking; anschließend rufen Sie den OpenAI-kompatiblen Chat-Endpunkt auf.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
4. Für einen lokalen Betrieb mit geringerem Speicherbedarf verwenden Sie den offiziellen Ollama-Befehl ollama run laguna-s-2.1 und wählen für die verfügbare Maschine ein veröffentlichtes Quantisierungs-Tag wie q4_K_M oder q8_0.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
5. Unter macOS installieren Sie Poolside Desktop Assistant, wenn ein Multi-Agenten-Arbeitsbereich auf Basis von pool gewünscht ist; die Standardkopplung ist pool mit Laguna S 2.1.
  — <https://poolside.ai/blog/introducing-poolside-desktop-assistant>

## Bewährte Praktiken {#best-practices}

- Für agentisches Coding lassen Sie enable_thinking aktiviert und bewahren reasoning_content über Assistenten- und Tool-Turns hinweg; wird das frühere Thinking verworfen, kann späteres Reasoning ausbleiben.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
- Verwenden Sie die Laguna-spezifischen Tool- und Reasoning-Parser der Serving-Integration statt generischer Standardwerte. Die Flag-Namen von vLLM und TRT-LLM unterscheiden sich; übernehmen Sie das Rezept für die gewählte Engine exakt.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
- Beim aktuellen FP8-Checkpoint behalten Sie die Standardwerte aus generation_config bei, einschließlich top_k 20, statt eigene Werte für temperature oder top_p zu setzen. Die Modellkarte warnt außerdem, dass die Qualität bei langem Kontext nachlassen kann.
  — <https://huggingface.co/poolside/Laguna-S-2.1-FP8>
- Die Mixed-Offload- und DFlash-Konfiguration mit einer 22-GB-2080-Ti behandeln Sie als einen Testaufbau aus der Community; messen Sie vor der Übernahme der Einstellungen Kontextlänge und Durchsatz auf der Zielhardware.
  — <https://ai-muninn.com/zh-TW/blog/laguna-118b-moe-on-one-2080ti>

## Durch dieses ersetzt {#superseded-by-this}

- Frühere Kopien des Repositories poolside/Laguna-S-2.1-FP8 vor dem aktuellen FP8-Artefakt. Seit 2026-08-01 veraltet; die Karte vom August besagt, dass der Ersatz ein neuer Checkpoint mit geänderten Gewichten ist.
- Frühere Kopien des Repositories poolside/Laguna-S-2.1-INT4 vor dem aktuellen INT4-Artefakt. Seit 2026-08-02 veraltet; die Karte vom August besagt, dass der Ersatz ein neuer Checkpoint mit geänderten Gewichten ist.

## Weiterhin unbekannt {#still-unknown}

- Das zugrunde liegende Quellereignis ist auf 2026-07-22 datiert, während Poolside den Start des Basismodells auf 2026-07-21 legt. Ohne den nicht öffentlichen Quelltext lässt sich nicht klären, ob der Quelldatensatz ein verspäteter Release-Beitrag war oder ein anderer Eintrag zum selben Thema.
- In diesem Durchgang wurde keine offizielle vereinfacht-chinesische Veröffentlichung oder Dokumentation gefunden. Die hier verwendete datierte chinesische Quelle ist ein traditionell-chinesischer Community-Beleg und ersetzt keine zh-CN-Linie.
- Es wurde in diesem Durchgang keine datierte Primärquelle gefunden, die besagt, dass das Basis-Repository poolside/Laguna-S-2.1 – und nicht nur seine FP8- und INT4-Varianten – nach dem Launch am 21. Juli ersetzt wurde.
- Die Benchmark-Werte von Poolside sind erklärte Ergebnisse unter den angegebenen Harnesses und Benchmark-Bedingungen; sie sind kein unabhängiger Nachweis für die Leistung im Produktivbetrieb.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://poolside.ai/blog/introducing-laguna-s-2-1 | Introducing Laguna S 2.1 - Poolside | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1 | poolside/Laguna-S-2.1 - Hugging Face model card | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-FP8/commits/main | Commits - poolside/Laguna-S-2.1-FP8 | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-FP8 | poolside/Laguna-S-2.1-FP8 - Hugging Face model card | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-INT4/commits/main | Commits - poolside/Laguna-S-2.1-INT4 | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-INT4 | poolside/Laguna-S-2.1-INT4 - Hugging Face model card | 2026-09-06 |
| https://poolside.ai/blog/introducing-poolside-desktop-assistant | Introducing Poolside Desktop Assistant, for macOS - Poolside | 2026-09-06 |
| https://openrouter.ai/poolside/laguna-s-2.1 | Laguna S 2.1 - API Pricing & Providers - OpenRouter | 2026-09-06 |
| https://chat.poolside.ai/ | Poolside Chat | 2026-09-06 |
| https://ai-muninn.com/zh-TW/blog/laguna-118b-moe-on-one-2080ti | [洋垃圾跑大模型 #2] 一張 22G 老卡跑 118B 的 coding 大模型:Poolside Laguna S 2.1 實戰 | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:poolside-laguna-s-2-1`, Thread `laguna`, 1 datiertes Ereignis vom 2026-07-22 → 2026-07-22.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Verwendung und Praktiken oben, einschließlich deren Grenzen.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
