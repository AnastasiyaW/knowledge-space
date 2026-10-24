---
title: "Nemotron 3.5 Lightning"
category: projects
date: 2026-08-12
tags: [nemotron-3-5-lightning, nvidia-nemotron, nvidia_nemotron, project]
aliases: ["Nemotron 3.5 Lightning"]
level: 2
source_sha256: 8c32a9d423cdaf66a2297b22822944e7d4e44eeaf762494f15c2faa268d229d6
translation: machine
translated_at: '2026-10-24'
---
# Nemotron 3.5 Lightning {#nemotron-35-lightning}

**Entwicklungslinie:** `project:nvidia-nemotron` · Thread `nemotron-3-5-lightning`  
**Letztes Ereignis:** 2026-08-12 · 1 datiertes Ereignis seit 2026-08-12 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Nemotron 3.5 Lightning ist ein textbasiertes hybrides MoE-Modell mit 30B Gesamt- und 3B aktiven Parametern für Entwickler agentischer Systeme, Chatbots und RAG. Funktionen: Schlussfolgern mit Umschalter für Thinking, Tool Use, Code, langer Kontext bis zu 1M Token, Speculative Decoding; verfügbar sind NVFP4- und BF16-Varianten. Praktische Grenze: Der NVFP4-Checkpoint belegt etwa 22 GB; NVIDIA nennt den Betrieb auf einer DGX Spark oder H100. Fazit: Dies ist ein Ausführungsmodell für häufige agentische Aufrufe, kein Ersatz für ein größeres Modell für komplexe Planung.

## Entwicklungslinie {#development-line}

- **2026-08-12 — Öffentliches Modell Nemotron 3.5 Lightning und Playground-Ressourcen erschienen.** Veröffentlicht wurde NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4, ein kommerziell nutzbarer 30B/3B-aktiv-Hybrid aus Mamba-2/MoE/Attention mit Kontext bis zu 1M Token; zusammen damit wurden BF16, NVFP4, DSpark/DFlash für Speculative Decoding und Routing über NeMo Switchyard bereitgestellt. Die primäre Modellkarte datiert den Release auf 2026-08-11. Das Ereignis vom 12. August spiegelt daher den folgenden Tag der Veröffentlichung bzw. Verbreitung wider, nicht ein separates Modell.

## Was sich geändert hat {#what-changed}

2026-08-12: Veröffentlicht wurde NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4, ein kommerziell nutzbarer 30B/3B-aktiv-Hybrid aus Mamba-2/MoE/Attention mit Kontext bis zu 1M Token; zusammen damit wurden BF16, NVFP4, DSpark/DFlash für Speculative Decoding und Routing über NeMo Switchyard bereitgestellt. Die primäre Modellkarte datiert den Release auf 2026-08-11. Das Ereignis vom 12. August spiegelt daher den folgenden Tag der Veröffentlichung bzw. Verbreitung wider, nicht ein separates Modell. 2026-08-17: NVIDIA veröffentlichte eine Erläuterung des QAD-Rezepts für NVFP4: Der Checkpoint wurde von etwa 66 GB BF16 auf 22 GB komprimiert. Dies ist Dokumentation zum bereits erschienenen Checkpoint, kein neuer Basisrelease.

## Wie man es einsetzt {#how-to-use-this}

Ab 2026-08-12 sollten Praktiker Nemotron 3.5 Lightning als Linie mit öffentlichen Modellartefakten, einem gehosteten Playground und zugehörigen Switchyard-Tools behandeln. Das konkrete veröffentlichte Modell bzw. den Deployment-Pfad wählen sie aus diesen Ressourcen, statt sich auf einen nicht verifizierten Repost zu verlassen.

1. Rufen Sie für einen schnellen Prototyp die NVIDIA Build API über einen OpenAI-kompatiblen Client mit dem Modellnamen `nvidia/nemotron-3.5-lightning-30b-a3b` auf; setzen Sie `enable_thinking` und begrenzen Sie das Reasoning-Budget passend zur Aufgabe.
  — <https://build.nvidia.com/nvidia/nemotron-3.5-lightning-30b-a3b>
2. Für Self-Hosting starten Sie den NVFP4-Checkpoint über vLLM oder SGLang und verwenden den von `/v1/models` zurückgegebenen Namen im OpenAI-kompatiblen Client.
  — <https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4>
3. Leiten Sie in einem agentischen System massenhafte Aktionen – Tool-Aufrufe, Ergebnisprüfung und Formatierung – an Lightning weiter, und überlassen Sie komplexe Planung einem stärkeren Modell.
  — <https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/>

## Best Practices {#best-practices}

- Messen Sie zuerst den Basispfad NVFP4/BF16 mit Ihren eigenen Aufgaben; wählen Sie Speculative Decoding anhand der Concurrency: DSpark wird für DGX Spark und niedrige Concurrency empfohlen, MTP für mittlere und hohe.
  — <https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/>
- Verwenden Sie das Routing nicht als implizites Fallback: Legen Sie explizite Regeln fest, welche Aufgabenklasse zu Lightning geht, und prüfen Sie Qualität und Kosten der Routen über Switchyard.
  — <https://github.com/NVIDIA-NeMo/Switchyard>
- Bei einer harten Speichergrenze sollten Sie NVFP4 in Betracht ziehen. Das QAD-Rezept von NVIDIA dient der Wiederherstellung der Qualität nach aggressiver Quantisierung und erfordert eine eigene Prüfung auf den Zielbenchmarks für agentische Systeme.
  — <https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/>

## Durch diesen Eintrag überholt {#superseded-by-this}

- 2026-08-17: Die Annahme, NVFP4 sei nur gewöhnliche Post-Training-Quantisierung, ist für den offiziellen Lightning-NVFP4-Checkpoint überholt: NVIDIA beschreibt QAD-Destillation auf Basis von PTQ.
- 2026-08-12: Die frühere Empfehlung, für jeden Aufruf dasselbe große Reasoning-Modell einzusetzen, wurde für die Ausführung routinemäßiger, hochfrequenter agentischer Schritte durch die Architektur „Planung – starkes Modell, Ausführung – Lightning“ ersetzt.

## Weiterhin unbekannt {#still-unknown}

- Anhand der verfügbaren Primärquellen lässt sich der genaue Veröffentlichungszeitpunkt aller fünf Links vom 12. August nicht bestimmen. Die Modellkarte nennt als Release-Datum 2026-08-11; die Abweichung von einem Tag kann daher auf die Uhrzeit der Veröffentlichung oder auf die Zeitzone zurückzuführen sein.
- Die Angaben von NVIDIA zu Geschwindigkeit und Benchmarks ersetzen keine Messung auf konkreter Hardware, mit bestimmter Serverversion, Concurrency und agentischem Harness.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 | NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 model card | 2026-09-05 |
| https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/ | NVIDIA Nemotron 3.5 Lightning Delivers Fast, Accurate Specialized Task Execution for Long-Running Agents | 2026-09-05 |
| https://build.nvidia.com/nvidia/nemotron-3.5-lightning-30b-a3b | nvidia/nemotron-3.5-lightning-30b-a3b on NVIDIA Build | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Switchyard | NVIDIA-NeMo/Switchyard | 2026-09-05 |
| https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/ | Developing Nemotron 3.5 Lightning NVFP4 with QAD Using NVIDIA Model Optimizer | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:nvidia-nemotron`, Thread `nemotron-3-5-lightning`, 1 datiertes Ereignis 2026-08-12 → 2026-08-12.
- **Praktischer Hinweis:** Ab 2026-08-12 sollten Praktiker Nemotron 3.5 Lightning als Linie mit öffentlichen Modellartefakten, einem gehosteten Playground und zugehörigen Switchyard-Tools behandeln. Das konkrete veröffentlichte Modell bzw. den Deployment-Pfad wählen sie aus diesen Ressourcen, statt sich auf einen nicht verifizierten Repost zu verlassen.
- **Konfidenz:** hoch. Die datierten Abschnitte „Durch diesen Eintrag überholt“ sind maßgeblich dafür, was veraltet ist.
