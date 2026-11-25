---
title: "Qwen2.5-Coder"
category: projects
date: 2024-11-12
tags: [project, qwen, qwen2-5-coder, qwen2-5-coder-launch]
aliases: ["Qwen2.5-Coder"]
level: 2
source_sha256: 7ceb0f41f470ef60dba2cbb23a93162ba9edb0e2104adff127c525b8a4816c40
translation: machine
translated_at: '2026-10-24'
---
# Qwen2.5-Coder {#qwen25-coder}

**Entwicklungslinie:** `project:qwen2-5-coder` · Thread `qwen2-5-coder-launch`  
**Letztes Ereignis:** 2024-11-12 · 2 datierte seit 2024-11-12 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Qwen2.5-Coder ist eine Familie von sechs Code-LLMs mit Basis- und instruktionsangepassten Varianten, von 0,5B bis 32B, für Completion, Chat, Code-Reparatur und Feinabstimmung.

- Generierung: erzeugt Code.
- Reasoning: denkt sich durch Programmieraufgaben.
- Reparatur: behebt Fehler im Code.
- Fill-in-the-middle: vervollständigt Code zwischen Präfix und Suffix.

Der Kontext reicht bis zu 128K, die Standardkonfiguration setzt jedoch 32K.
Die Familie eignet sich für lokale und selbst gehostete Aufgaben, Qwen verweist neue agentische Entwicklung jedoch auf Qwen3-Coder.

## Entwicklungslinie {#development-line}

- **2024-11-12 — Qwen veröffentlichte die Modellfamilie Qwen2.5-Coder.** Zu den bisher verfügbaren 1,5B- und 7B-Modellen ergänzte Qwen 0,5B, 3B, 14B und 32B in Basis- und Instruct-Varianten.
- **2024-11-12 — Qwen stellte eine Artifacts-Erfahrung für Qwen2.5-Coder bereit.** Zu den bisher verfügbaren 1,5B- und 7B-Modellen ergänzte Qwen 0,5B, 3B, 14B und 32B in Basis- und Instruct-Varianten.

## Was sich geändert hat {#what-changed}

2024-11-12 — Qwen eröffnete das vollständige Qwen2.5-Coder-Sortiment: Zu den bisher verfügbaren 1,5B- und 7B-Modellen ergänzte Qwen 0,5B, 3B, 14B und 32B in Basis- und Instruct-Varianten. 2025-07-22 — Qwen veröffentlichte Qwen3-Coder als nächste Generation für agentisches Coding; das ursprüngliche Qwen2.5-Coder-Repository leitet nun dorthin weiter.

## So wird es verwendet {#how-to-use-this}

Ab 2024-11-12 konnten Praktiker Qwen2.5-Coder über die veröffentlichte Modellsammlung, Demo, das Repository und die Artifacts-Erfahrung evaluieren, statt sich nur auf eine allgemeine Chat-Oberfläche zu verlassen.

1. Für interaktive Aufgaben wählen Sie eine Instruct-Variante passender Größe, laden Tokenizer und Modell über Transformers und erstellen die Anfrage mit apply_chat_template.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct>
2. Für eine selbst gehostete API stellen Sie den gewählten Checkpoint über vLLM bereit; der Server stellt einen OpenAI-kompatiblen Endpunkt /v1/chat/completions bereit.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct>
3. Für Completion oder FIM betreiben Sie das Basismodell; für normale Dialoge verwenden Sie Instruct statt Basis.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-7B>

## Bewährte Praktiken {#best-practices}

- Verwenden Sie Basismodelle nicht für Konversation ohne eigenes Post-Training; wählen Sie für einen Assistenten Instruct.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-7B>
- Aktivieren Sie YaRN nur, wenn Kontext über 32K wirklich benötigt wird: statische Skalierung kann kurze Anfragen beeinträchtigen.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct>
- Aktualisieren Sie Transformers auf mindestens Version 4.37, sonst schlägt das Laden der Qwen2-Architektur mit KeyError fehl.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-7B>

## Abgelöst durch {#superseded-by-this}

- 2025-07-22 — Qwen3-Coder wurde Qwens aktuelle Linie für agentisches Coding; Qwen2.5-Coder bleibt als verfügbare Menge von Checkpoints erhalten, doch das ursprüngliche GitHub-Repository leitet auf Qwen3-Coder weiter.

## Noch unbekannt {#still-unknown}

- Der aktuelle Status des öffentlichen Qwen2.5-Coder-Artifacts-Space ist pausiert; sein Verfügbarkeitsverlauf und seine Eignung als funktionierendes Produkt sind nicht bestätigt.
- Die 3B-Variante hat eine abweichende Lizenz: Sie verwendet die Qwen Research License, während 0,5B, 1,5B, 7B, 14B und 32B Apache 2.0 verwenden.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://qwenlm.github.io/blog/qwen2.5-coder-family/ | Qwen2.5-Coder Series: Powerful, Diverse, Practical. | 2026-09-05 |
| https://arxiv.org/abs/2409.12186 | Qwen2.5-Coder Technical Report | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen2.5-Coder-7B | Qwen/Qwen2.5-Coder-7B model card | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct | Qwen/Qwen2.5-Coder-32B-Instruct model card | 2026-09-05 |
| https://github.com/QwenLM/Qwen2.5-Coder | QwenLM/Qwen2.5-Coder repository redirect | 2026-09-05 |
| https://qwenlm.github.io/blog/qwen3-coder/ | Qwen3-Coder: Agentic Coding in the World | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:qwen2-5-coder`, Thread `qwen2-5-coder-launch`, 2 datierte Ereignisse 2024-11-12 → 2024-11-12.
- **Praktische Anmerkung:** Ab 2024-11-12 konnten Praktiker Qwen2.5-Coder über die veröffentlichte Modellsammlung, Demo, das Repository und die Artifacts-Erfahrung evaluieren, statt sich nur auf eine allgemeine Chat-Oberfläche zu verlassen.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
