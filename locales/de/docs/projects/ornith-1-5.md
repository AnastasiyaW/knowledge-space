---
title: "Ornith-1.5"
category: projects
date: 2026-08-20
tags: [ornith, ornith-1-5, project]
aliases: ["Ornith-1.5"]
level: 2
source_sha256: 7cc51670671e0f90b03a2189c82bba359d263a88830c8dde31f9d7b441e6c87b
translation: machine
translated_at: '2026-10-24'
---
# Ornith-1.5 {#ornith-15}

**Entwicklungslinie:** `project:ornith-1-5` · Thread `ornith-1-5`  
**Letztes Ereignis:** 2026-08-20 · 1 datiertes seit 2026-08-20 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Ornith-1.5 — eine Familie MIT-lizenzierter multimodaler Modelle für Entwickler, die einen lokalen OpenAI-kompatiblen Endpoint statt einer geschlossenen API benötigen. — 9B Dense für eine einzelne GPU und quantisierte Builds. — 35B-A3B MoE mit etwa 3B aktiven Parametern pro Token. — 397B MoE für Multi-GPU-Serving. Der Basiskontext beträgt bis zu 262 144 Token; 397B benötigt etwa 800 GB in bf16. Fazit: 35B-A3B ist die praktische Serveroption, 397B ist eine Option für Infrastruktur mit mehreren Beschleunigern.

## Entwicklungslinie {#development-line}

- **2026-08-20 — Ornith-1.5-Release-Seite und Modell-Collection wurden verlinkt.** Die Linie aus 9B Dense, 35B MoE und 397B MoE erweiterte Ornith-1.0 von der Generierung von Scaffold und Rollout um die gemeinsame Generierung von Aufgaben, Scaffold und Rollout für RL.

## Was sich geändert hat {#what-changed}

2026-08-20 — Ornith-1.5 wurde veröffentlicht: Die Linie aus 9B Dense, 35B MoE und 397B MoE erweiterte Ornith-1.0 von der Generierung von Scaffold und Rollout um die gemeinsame Generierung von Aufgaben, Scaffold und Rollout für RL.

Ergänzung zum Ereignis: Das 35B-Modell heißt Ornith-1.5-35B-A3B und aktiviert etwa 3B Parameter pro Token; der Flaggschiff-Checkpoint Ornith-1.5-397B wird als 397B MoE angekündigt.

## Wie man das nutzt {#how-to-use-this}

Ab 2026-08-20 sollten Praktiker Ornith-1.5 als eigenständige Release-Linie behandeln und vor der Wahl eines Checkpoints oder Workflows die verlinkte offizielle Seite und die Modell-Collection konsultieren.

1. Checkpoint wählen: 9B für einen kompakten Start, 35B-A3B für serverseitiges Reasoning/Coding, 397B — falls ein Multi-GPU-Knoten verfügbar ist.
  — <https://huggingface.co/collections/ornith-ai/ornith-15>
2. Für 35B-A3B aktuelles vLLM oder SGLang installieren und einen OpenAI-kompatiblen Server mit Parser für Reasoning und Tool Calls starten.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
3. Client an den lokalen /v1-Endpoint anbinden und die finale Antwort aus content lesen, den Reasoning-Trace aus reasoning_content.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
4. Für einen einfachen lokalen Test den 9B-Checkpoint über die Transformers-Pipeline laden oder mit vLLM starten.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-9B/tree/main>

## Best Practices {#best-practices}

- Für übliche Aufgaben mit temperature=0.6, top_p=0.95 und top_k=20 beginnen; temperature=1.0 ist laut Autor für das Reproduzieren von Benchmarks gedacht.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
- Für 35B-A3B eine Runtime verwenden, die nicht älter ist als Transformers 5.8.1, vLLM 0.19.1 oder SGLang 0.5.9.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
- YaRN/RoPE-Scaling bei kurzen Anfragen nicht aktivieren: statische Skalierung kann die Qualität verschlechtern; factor auf das tatsächlich benötigte Fenster abstimmen.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- 2026-08-20 — Ornith-1.5 ersetzt Ornith-1.0 als aktuelle Linie für Aufgaben, bei denen die vollständige Self-Improvement-Loop wichtig ist; Ornith-1.0 bleibt der vorherige Stand, nicht ein gelöschtes Modell.
- 2026-08-20 — Für das 35B-Modell lautet der aktuelle Checkpoint-Name Ornith-1.5-35B-A3B, nicht das allgemeine „Ornith-1.5-35B“.

## Noch unbekannt {#still-unknown}

- Die erste Ornith-Seite ist nur mit „Aug. 2026“ datiert; der genaue Tag 2026-08-20 ist daher durch das Eingangsereignis bestätigt, nicht separat auf der Seite des Autors.
- Die angegebenen Benchmarks sind Ergebnisse des Ornith-Teams; eine unabhängige Reproduktion in den verwendeten Primärquellen gibt es nicht.
- Die Mobile-Variante Ornith-1.5-9B wird in der Ankündigung erwähnt, ihre eigene aktuelle Modellkarte und die Startanforderungen wurden aber nicht geprüft.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://ornith.ai/ornith_1_5.html | Ornith-1.5: From Self-Scaffolding to Self-Improvement | 2026-09-05 |
| https://huggingface.co/collections/ornith-ai/ornith-15 | Ornith-1.5 - a ornith-ai Collection | 2026-09-05 |
| https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200 | ornith-ai/Ornith-1.5-35B-A3B | 2026-09-05 |
| https://huggingface.co/ornith-ai/Ornith-1.5-9B/tree/main | ornith-ai/Ornith-1.5-9B | 2026-09-05 |
| https://huggingface.co/ornith-ai/Ornith-1.5-397B/blame/main/README.md | README.md · ornith-ai/Ornith-1.5-397B | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:ornith-1-5`, Thread `ornith-1-5`, 1 datiertes Ereignis 2026-08-20 → 2026-08-20.
- **Praktischer Hinweis:** Ab 2026-08-20 sollten Praktiker Ornith-1.5 als eigenständige Release-Linie behandeln und vor der Wahl eines Checkpoints oder Workflows die verlinkte offizielle Seite und die Modell-Collection konsultieren.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
