---
title: "Qwen3.8-Flash-Next — Qwen"
category: projects
date: 2026-08-26
tags: [project, qwen, qwen3-8-flash-next]
aliases: ["Qwen3.8-Flash-Next"]
level: 3
source_sha256: 378eb01d21d8440e184eb41b127e3da6ac667a4eb078bd415d68b7676c742a1f
translation: machine
translated_at: '2026-10-24'
---
# Qwen3.8-Flash-Next — Qwen {#qwen38-flash-next-qwen}

**Entwicklungslinie:** `project:qwen3-8-flash-next` · Thread `qwen`  
**Letztes Ereignis:** 2026-08-26 · 1 datiertes Ereignis seit 2026-08-26 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Qwen3.8-Flash-Next: ein offenes multimodales MoE-Modell für Entwickler, die Vision+Text, Coding und agentische Szenarien benötigen. — läuft über Transformers, vLLM, SGLang, TokenSpeed und llama.cpp; — nutzt Gated DeltaNet, Qwen Sparse Attention, Gated Residual und N-Gram-Embeddings. 125 Mrd. Parameter im Hauptmodell, 51 Mrd. Parameter in den N-Gram-Embedding-Tabellen und 6 Mrd. aktive Parameter pro Token; das offizielle Serving-Beispiel setzt einen Kontext von 262 144 Token. Praktische Wahl für Experimente mit offenen Modellgewichten; für eine verwaltete Produktions-API wird der offizielle Qwen3.8-Flash separat positioniert.

## Entwicklungslinie {#development-line}

- **2026-08-26 — Ressourcen des Projekts Qwen3.8-Flash-Next wurden dokumentiert.** Zum multimodalen MoE-Modell und zur frühen Preview der Architektur Qwen4.

## Was sich geändert hat {#what-changed}

2026-08-26 — offene Gewichte von Qwen3.8-Flash-Next veröffentlicht: des multimodalen MoE-Modells und der frühen Preview der Architektur Qwen4. 2026-08-31 — ein technischer Bericht mit Architektur-Ablationen, Effizienzbewertung und Trainingsstabilität ist erschienen.

## So nutzen Sie das {#how-to-use-this}

Stand 2026-08-26 sollten Praktiker Qwen3.8-Flash-Next über das verlinkte Quell-Repository, die Modell-Hosting-Ressourcen und die Demo verifizieren, bevor sie einen Checkpoint oder eine Deployment-Route auswählen.

1. Für einen Prototyp mit Bild und Text laden Sie `Qwen/Qwen3.8-Flash-Next` über die Transformers-Pipeline `image-text-to-text` oder über `AutoProcessor` und `AutoModelForMultimodalLM`.
  — <https://huggingface.co/Qwen/Qwen3.8-Flash-Next>
2. Für eine selbst gehostete, OpenAI-kompatible API starten Sie vLLM; das offizielle Beispiel verwendet Tensor Parallelism 4, `--max-model-len 262144`, den Reasoning-Parser `qwen3` und den Tool-Call-Parser `qwen3_coder`.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
3. Wenn Sie keine Infrastruktur für offene Gewichte betreiben möchten, nutzen Sie Qwen Cloud: das aktuelle verwaltete Qwen3.8-Flash ist mit den APIs von OpenAI und Anthropic kompatibel.
  — <https://www.qwencloud.com/>

## Best Practices {#best-practices}

- Für Läufe mit Tool Calls aktivieren Sie gleichzeitig den Reasoning-Parser `qwen3` und den Tool-Call-Parser `qwen3_coder`; ohne sie ist für diesen Modus kein offizielles Serving-Rezept angegeben.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
- Auf Apple Silicon verwenden Sie mlx-vlm oder eine fertige MLX-Quantisierung; für llama.cpp wählen Sie kompatible GGUF-Gewichte statt des ursprünglichen Checkpoints.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
- Übertragen Sie das 262K-Limit aus dem selbst gehosteten Beispiel nicht auf das verwaltete Modell: Qwen Cloud gibt für Qwen3.8-Flash einen Kontext von 1M an.
  — <https://www.qwencloud.com/>

## Ersetzt durch diese {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Für das Ereignis vom 2026-08-26: Das offizielle Repository datiert die Veröffentlichung auf 2026-08-26 und präzisiert, dass die offenen Gewichte von Qwen3.8-Flash-Next veröffentlicht wurden — einem multimodalen MoE-Modell mit 125 Mrd. Parametern und 6 Mrd. aktiven Parametern pro Token; source_date=2026-08-26; source_url=https://github.com/QwenLM/Qwen3.8-Flash-Next.
- Neues Ereignis: 2026-08-31 — der technische Bericht beschreibt 14 Pre-Training-Benchmarks: Das Modell übertrifft den Vorgänger 397B-A17B bei acht und liegt bei den übrigen um höchstens 2,6 Punkte zurück, bei etwa einem Drittel der aktiven Parameter, einem Drittel der Trainingstoken und etwa einem Neuntel der FLOPs; source_date=2026-08-31; source_url=https://arxiv.org/abs/2608.30320.
- Die aktuelle Modellkarte bezeichnet Qwen3.8-Flash als Produktionsversion auf Basis von Flash-Next mit 1M Kontext und integrierten Tools, nennt aber kein Datum für diesen Übergang. Er lässt sich daher weder dem Ereignis vom 2026-08-26 zuordnen noch als datiertes supersedes führen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/QwenLM/Qwen3.8-Flash-Next | QwenLM/Qwen3.8-Flash-Next | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.8-Flash-Next | Modellkarte Qwen/Qwen3.8-Flash-Next | 2026-09-05 |
| https://arxiv.org/abs/2608.30320 | Zum Design der Qwen3.8-Next-Architektur: Evaluation, Effizienz und Trainingsstabilität | 2026-09-05 |
| https://www.qwencloud.com/ | QwenCloud — Plattform für KI-native Modelle, Tools und Apps | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:qwen3-8-flash-next`, Thread `qwen`, 1 datiertes Ereignis 2026-08-26 → 2026-08-26.
- **Praktischer Hinweis:** Stand 2026-08-26 sollten Praktiker Qwen3.8-Flash-Next über das verlinkte Quell-Repository, die Modell-Hosting-Ressourcen und die Demo verifizieren, bevor sie einen Checkpoint oder eine Deployment-Route auswählen.
- **Konfidenz:** hoch. Die oben datierten supersedes sind maßgeblich dafür, was veraltet ist.
