---
title: "Nemotron 3 Super"
category: projects
date: 2026-03-12
tags: [llm_releases, nemotron-3-super, project]
aliases: ["Nemotron 3 Super"]
level: 3
source_sha256: a745d6398d81451ba8c56f9358c5aab8a14a7f8cbe70ffc96ebf6c682ef1fe3d
translation: machine
translated_at: '2026-10-24'
---
# Nemotron 3 Super {#nemotron-3-super}

**Entwicklungslinie:** `project:nemotron-3-super` · Thread `nemotron-3-super`  
**Letztes Ereignis:** 2026-03-12 · 1 datiertes Ereignis seit 2026-03-12 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Nemotron 3 Super ist ein offenes hybrides Mamba-Transformer-MoE-Modell von NVIDIA für Teams, die agentische Systeme, Programmierung und langen Kontext umsetzen. Fähigkeiten: Reasoning, Tool Calling, Code, Kontext bis zu 1 Mio. Token. Kennzahlen: 120B Parameter insgesamt, 12B aktiv; die BF16-Gewichte belegen 247 GB. Fazit: geeignet für Serving oder API-Integration großer agentischer Aufgaben, aber nicht für eine typische einzelne lokale GPU.

## Entwicklungslinie {#development-line}

- **2026-03-12 — NVIDIA kündigte Nemotron 3 Super an.** 120B/12B-aktiv, hybrider Mamba-Transformer Latent MoE mit MTP, Fenster von 1 Mio. Token, offene Gewichte, Datensätze und Rezepte; die primäre Ankündigung ist auf 2026-03-11 datiert, daher hält das Ereignisdatum das Erscheinen des Links fest, nicht das Veröffentlichungsdatum von NVIDIA. Ergänzung zu diesem Schritt: NVIDIA gibt RL in 21 Umgebungskonfigurationen und mehr als 1,2 Mio. Rollouts an.

## Was sich geändert hat {#what-changed}

2026-03-12 — NVIDIA-Nemotron-3-Super-120B-A12B veröffentlicht: 120B/12B-aktiv, hybrider Mamba-Transformer Latent MoE mit MTP, Fenster von 1 Mio. Token, offene Gewichte, Datensätze und Rezepte; die primäre Ankündigung ist auf 2026-03-11 datiert, daher hält das Ereignisdatum das Erscheinen des Links fest, nicht das Veröffentlichungsdatum von NVIDIA. Ergänzung zu diesem Schritt: NVIDIA gibt RL in 21 Umgebungskonfigurationen und mehr als 1,2 Mio. Rollouts an. 2026-03-25 — NVIDIA meldete Korrekturen für das Streaming mit force_nonempty_content und für Tool Calling mit dem qwen3coder-Parser in vLLM und TensorRT-LLM; bei anyOf muss ein Tool Call ein Objekt statt einer Zeichenkette zurückgeben. Dies ist eine eigenständige spätere Änderung und nicht Teil des Starts am 12. März.

## Wie man es nutzt {#how-to-use-this}

Ab 2026-03-12 sollten Praktiker, die agentische Reasoning-Modelle evaluieren, Nemotron 3 Super in ihre Evaluierungs-Shortlist aufnehmen und die verlinkten Modell- und Cookbook-Ressourcen konsultieren, um die Eignung für den Einsatz zu bewerten; dieser nicht recherchierte Zweig begründet keine Schlussfolgerungen zu Benchmarks oder Lizenzen.

1. Für einen lokalen Prototyp laden Sie den BF16-Checkpoint über Transformers mit trust_remote_code=True oder starten einen vLLM-Server mit dem Modellnamen; greifen Sie über die OpenAI-kompatible API /v1/chat/completions darauf zu.
  — <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16/tree/main>
2. Für agentisches Coding über OpenRouter setzen Sie das Modell nvidia/nemotron-3-super-120b-a12b:free und begrenzen Kontext und Output in der Agent-Konfiguration.
  — <https://docs.nvidia.com/nemotron/latest/usage-cookbook/Nemotron-3-Super/OpenScaffoldingResources/README.html>
3. Für reproduzierbares Training oder Anpassung verwenden Sie das Nemotron-Repository, uv sync und die schrittweise Pipeline aus pretrain, SFT, RL und eval auf einem Slurm-Cluster.
  — <https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/README.md>

## Bewährte Vorgehensweisen {#best-practices}

- Für Hopper wählen Sie den veröffentlichten FP8-Checkpoint, für Blackwell NVFP4; übertragen Sie Leistungserwartungen nicht zwischen beiden ohne Messung auf Ihrer eigenen Hardware.
  — <https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/quantization.md>
- Wenn Sie den qwen3coder-Tool-Parser oder Streaming verwenden, fixieren Sie die Versionen mit den Korrekturen: vLLM 0.18.0 oder ein kompatibles TensorRT-LLM-/NIM-Release. Prüfen Sie anschließend die anyOf-Struktur der Tool Calls im Integrationstest.
  — <https://github.com/NVIDIA-NeMo/Nemotron/discussions/124>

## Durch diesen Stand ersetzt {#superseded-by-this}

- 2026-03-25 — die frühere Annahme, dass Streaming mit force_nonempty_content funktioniert und qwen3coder-anyOf-Tool-Calls immer eine Objektstruktur haben, ist überholt: Es sind korrigierte Serverversionen erforderlich.
- 2026-03-12 — der bisherige Nemotron Super wird als Leistungsreferenz durch Nemotron 3 Super ersetzt; NVIDIA gibt mehr als 5× Durchsatz an, dies ist jedoch keine allgemeine Garantie für eine andere Konfiguration.

## Weiterhin unbekannt {#still-unknown}

- Das Antwortschema enthält die in der Aufgabe geforderten Felder event_findings und new_events nicht; ihre Fakten sind stattdessen in what_changed als Ergänzung zum Ereignis vom 2026-03-12 bzw. als eigenes Datum 2026-03-25 erfasst.
- Verfügbarkeit, Limits und Bedingungen der kostenlosen OpenRouter-Route zum Zeitpunkt der Nutzung wurden nicht geprüft; sie können sich ändern.
- Der PinchBench-Wert von 85,6 % ist eine Angabe von NVIDIA zu einem bestimmten Benchmark, keine unabhängige Qualitätsgarantie in Ihrer agentischen Umgebung.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/ | Introducing Nemotron 3 Super: An Open Hybrid Mamba-Transformer MoE for Agentic Reasoning | 2026-09-05 |
| https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16/tree/main | nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 | 2026-09-05 |
| https://docs.nvidia.com/nemotron/latest/usage-cookbook/Nemotron-3-Super/OpenScaffoldingResources/README.html | Nemotron 3 Super with Agentic Coding Tools | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/README.md | Nemotron 3 Super Training Recipe | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/quantization.md | Nemotron 3 Super Quantization | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Nemotron/discussions/124 | Nemotron 3 Super Improvements and Fixes | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:nemotron-3-super`, Thread `nemotron-3-super`, 1 datiertes Ereignis 2026-03-12 → 2026-03-12.
- **Praxishinweis:** Ab 2026-03-12 sollten Praktiker, die agentische Reasoning-Modelle evaluieren, Nemotron 3 Super in ihre Evaluierungs-Shortlist aufnehmen und die verlinkten Modell- und Cookbook-Ressourcen konsultieren, um die Eignung für den Einsatz zu bewerten; dieser nicht recherchierte Zweig begründet keine Schlussfolgerungen zu Benchmarks oder Lizenzen.
- **Konfidenz:** hoch. Die datierten Überholungen oben sind maßgeblich dafür, was veraltet ist.
