---
title: "Nanbeige4.2-3B"
category: projects
date: 2026-07-26
tags: [nanbeige, nanbeige-4-2-3b, nanbeige4-2-3b, project]
aliases: ["Nanbeige4.2-3B"]
level: 4
source_sha256: a7cf0d95871eb75c04f082a590924f5152072ecbb113a0ee541930970c499aab
translation: machine
translated_at: '2026-10-24'
---
# Nanbeige4.2-3B {#nanbeige42-3b}

**Entwicklungslinie:** `project:nanbeige-4-2-3b` · Thread `nanbeige4-2-3b`  
**Letztes Ereignis:** 2026-07-26 · 1 datiertes Ereignis seit 2026-07-26 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

Nanbeige4.2-3B ist ein BF16-Modell für Teams, die ihre eigene Runtime betreiben und Zielaufgaben verifizieren wollen.

- Reasoning-Modus für mehrstufiges Schlussfolgern.
- Chat-Template für strukturierte Chat-Turns.
- Tool Calling für die Ausführung von Funktionen.
- Lokale Runtimes über Transformers, SGLang, vLLM und llama.cpp.

3B Non-Embedding-Parameter gegenüber 4B auf der Hub-Karte; die angegebene Kontextlänge erreicht 262144 Tokens.

Das Modell eignet sich für kontrollierte lokale Deployments, doch benutzerdefinierter Code und langer Kontext erfordern eine fixierte Version und Tests in der Zielumgebung.

## Entwicklungslinie {#development-line}

- **2026-07-26 — Öffentliches Modell und Inferenzressourcen von Nanbeige4.2-3B wurden verlinkt.** Am 2026-07-26 verlinkte ein Entwicklungsupdate die Hugging-Face-Modellseite von Nanbeige4.2-3B, eine gefilterte Liste verwandter quantisierter Basismodell-Einträge und einen Inferenz-Space. Damit ist ein datierter öffentlicher Zugangspunkt für das Modell und die zugehörigen Deployment-Optionen belegt.

## Was sich geändert hat {#what-changed}

- 2026-07-21 — Die Hub-Historie verzeichnet den initialen Commit und einen separaten Upload von modeling_nanbeige.py. Das bestätigt frühen Zugriff auf Repository und Code, ohne den exakten Zeitpunkt für alle Gewichte festzulegen.
- 2026-07-24 — Nanbeige Lab hat Version 1 des technischen Berichts bei arXiv eingereicht.
- 2026-07-26 — configuration_nanbeige.py wurde dem Repository hinzugefügt.
- 2026-07-27 — Die Unterstützung für Nanbeige4.2 wurde in llama.cpp master gemergt, der zugehörige CI-Lauf schlug jedoch fehl.
- 2026-07-28 — Das README ersetzte den Link auf das lokale PDF des technischen Berichts durch einen arXiv-Link.
- 2026-08-14 — Ein unabhängiges Paper beschrieb Fixes für die Ausführung über Transformers auf Apple Silicon/MPS.
- 2026-09-04 — Das stabile Release llama.cpp v0.4.0 führte Unterstützung für nanbeige4.2-3B auf.

## So wird es verwendet {#how-to-use-this}

Stand 2026-07-26 sollten Praktiker die Hugging-Face-Modellseite von Nanbeige4.2-3B und die zugehörigen quantisierten Varianten konsultieren, bevor sie ein Artefakt auswählen, und den verlinkten Inferenz-Space nutzen, um die verfügbare Inferenzmöglichkeit zu prüfen.

1. Lege eine lokale Umgebung mit transformers==4.45.1 an, lade AutoTokenizer mit use_fast=false und danach AutoModelForCausalLM mit torch_dtype="auto", device_map="auto" und trust_remote_code=true.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
2. Übergib Nachrichten an tokenizer.apply_chat_template mit add_generation_prompt=true, tokenisiere ohne Spezialtokens und beginne mit einer kurzen Generierungsanfrage.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
3. Für einen OpenAI-kompatiblen Server verwende die vom Entwickler bereitgestellten Forks SGLang nbg42 oder vLLM nanbeige42 mit den Parsern nanbeige für Reasoning und Tool-Calls.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
4. Für das GGUF-Deployment nimm llama.cpp v0.4.0 als dokumentierte Basis mit integrierter Unterstützung für Nanbeige4.2-3B und verifiziere die gewählte Quantisierung mit einem kurzen Smoke-Test.
  — <https://github.com/ggml-org/llama.cpp/releases>

## Best Practices {#best-practices}

- Prüfe Autor und Code, bevor du trust_remote_code aktivierst, und fixiere dann den vollständigen Commit-Hash über revision. Der Hub empfiehlt dies, um sich vor Änderungen am Upstream-Code zu schützen.
  — <https://huggingface.co/docs/transformers/models>
- Setze preserve_thinking=false für Standard-Chat; setze es auf true für mehrstufige Tool-, Office- und Code-Aufgaben. Verwende das Template mit tools und bevorzuge tool_call_format="xml" für Tool-Calls.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
- Behandle 262144 Tokens nicht als garantiert funktionierenden Kontext; beginne mit einem kurzen Zieltest. Ein unabhängiges Paper berichtete über Probleme mit dem ursprünglichen Checkpoint unter Transformers auf Apple Silicon/MPS.
  — <https://arxiv.org/abs/2608.13987>
- Verlass dich nicht auf die veraltete Annahme, dass das Standard-llama.cpp keine Unterstützung enthält: Fixiere v0.4.0 oder verifiziere eine neuere Version separat.
  — <https://github.com/ggml-org/llama.cpp/releases>

## Hierdurch abgelöst {#superseded-by-this}

- {"claim":"Die ursprüngliche Veröffentlichung von Nanbeige4.2-3B auf 2026-07-26 datieren.","obsolete_since":"2026-09-06 (historische Prüfung)","source_url":"https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commits/main"}
- {"claim":"Das Standard-llama.cpp hat keine Unterstützung für Nanbeige4.2-3B.","obsolete_since":"2026-09-04","source_url":"https://github.com/ggml-org/llama.cpp/releases"}
- {"claim":"Das lokale PDF im Hub-README ist die kanonische Referenz auf den technischen Bericht.","obsolete_since":"2026-07-28","source_url":"https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commit/f56ec5a9650268aa098496734743c25ea778bd2d"}

## Weiterhin unbekannt {#still-unknown}

- Der exakte Zeitpunkt der initialen öffentlichen Veröffentlichung der Gewichte fehlt als absoluter Zeitstempel: Die Hub-Historie zeigt nur den Kalendertag.
- Dem inference-labs Space fehlt eine offizielle Bestätigung; wir konnten seine API, Hardwarekonfiguration oder Live-Ausgabe nicht verifizieren.
- Die geprüfte Modellkarte nennt keinen Provider-Endpunkt; das spiegelt den aktuellen Stand wider und ist kein Beleg gegen externes Hosting.
- Das offizielle Nanbeige4.2-3B-DSpark wird als 0,8B-Draft-Modell beschrieben, das das 3B-Modell beschleunigen soll. Der Hub zeigt jedoch nur relative Commit-Zeiten; ein absolutes Datum der ersten Veröffentlichung fehlt in der Zeitleiste.
- Mindest-VRAM, Latenz und Produktionsqualität für bestimmte Runtimes sind durch direkte Tests nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B | Nanbeige/Nanbeige4.2-3B · Hugging Face | 2026-09-06 |
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commits/main | Commits · Nanbeige/Nanbeige4.2-3B | 2026-09-06 |
| https://arxiv.org/abs/2607.22083 | Nanbeige4.2-3B: Unlocking Agentic Capabilities in a Compact Model | 2026-09-06 |
| https://github.com/ggml-org/llama.cpp/actions/runs/30278196993 | model: Add support for Nanbeige4.2 (#25994) · ggml-org/llama.cpp@b77d646 · GitHub | 2026-09-06 |
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commit/f56ec5a9650268aa098496734743c25ea778bd2d | Update README.md · Nanbeige/Nanbeige4.2-3B at f56ec5a | 2026-09-06 |
| https://arxiv.org/abs/2608.13987 | Nanbeige4.2-3B on Apple Silicon: Fixing Deployment Bugs and Decreasing Looped Transformer Memory Overhead | 2026-09-06 |
| https://github.com/ggml-org/llama.cpp/releases | Releases · ggml-org/llama.cpp | 2026-09-06 |
| https://huggingface.co/docs/transformers/models | Loading models · Hugging Face | 2026-09-06 |
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B-DSpark | Nanbeige4.2-3B-DSpark · Hugging Face | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:nanbeige-4-2-3b`, Thread `nanbeige4-2-3b`, 1 datiertes Ereignis vom 2026-07-26 bis 2026-07-26.
- **Praktischer Hinweis:** Stand 2026-07-26 sollten Praktiker die Hugging-Face-Modellseite von Nanbeige4.2-3B und die zugehörigen quantisierten Varianten konsultieren, bevor sie ein Artefakt auswählen, und den verlinkten Inferenz-Space nutzen, um die verfügbare Inferenzmöglichkeit zu prüfen.
- **Konfidenz:** mittel. Die datierten Einträge unter „Hierdurch abgelöst“ sind maßgeblich dafür, was veraltet ist.
