---
title: "GLM-5.2-NVFP4"
category: projects
date: 2026-06-26
tags: [glm-5-2-nvfp4, project]
aliases: ["GLM-5.2-NVFP4"]
level: 3
source_sha256: 05ff2666d99ea4e4c023a0f6612605a9776405713ac9538780ac18aa3ea3c9ed
translation: machine
translated_at: '2026-10-24'
---
# GLM-5.2-NVFP4 {#glm-52-nvfp4}

**Entwicklungslinie:** `project:glm-5-2-nvfp4` · Thread `glm-5-2-nvfp4`  
**Letztes Ereignis:** 2026-06-26 · 1 datiert seit 2026-06-26 · **Recherchiert:** 2026-09-06 · Konfidenz: hoch

## Was es ist {#what-it-is}

GLM-5.2-NVFP4 ist der NVFP4-Checkpoint von NVIDIA Model Optimizer für Z.AI GLM-5.2, gedacht für den Selbstbetrieb von Agenten, Chatbots, RAG, Coding und Reasoning.

- Textgenerierung und Reasoning mit Sparse-MoE.
- Coding- und Long-Context-Anfragen.
- Tool Calling über die mitgelieferten Parser-Einstellungen für SGLang und vLLM.

753B Parameter insgesamt, 40B aktiv, und bis zu 1M Kontext auf Blackwell und Linux.
Auf Blackwell bereitstellen, nachdem der Workload validiert wurde; diese Belege etablieren keine allgemeine lokale, Nicht-NVIDIA- oder verwaltete Inferenz-Route.

## Entwicklungslinie {#development-line}

- **2026-06-26 — GLM-5.2-NVFP4 mit der Hugging-Face-Modellseite von NVIDIA verknüpft.** Am 2026-06-26 verknüpfte die Entwicklungslinie von GLM-5.2-NVFP4 auf eine Hugging-Face-Modellseite unter dem Account von NVIDIA. Dies ist ein wesentlicher Bezugspunkt für den öffentlichen Verbreitungsweg des Projekts, auch wenn die datierte Verknüpfung allein weder ein Veröffentlichungsdatum, eine Modellrevision noch technische Spezifikationen belegt.

## Was sich geändert hat {#what-changed}

- 2026-06-26 — GLM-5.2-NVFP4 wurde als NVFP4-1.0-Model-Optimizer-Checkpoint von Z.AI GLM-5.2 dokumentiert; die verlinkte Karte ist auf 2026-06-25 datiert.
- 2026-07-09 — NVIDIA NGC hat `nim-aec724e-nvfp4` hinzugefügt, ein NIM-Staging-Artefakt mit 432.95 GB; seine FP8-Beschreibung erzeugt einen Vorbehalt bezüglich der Paketidentität.
- 2026-07-20 — NVIDIA Dynamo hat eine nur für die Entwicklung gedachte SGLang-Runtime für GLM-5.2 erfasst, mit nicht upstream integrierten Patches für Stabilität, Konfigurationsparsing und Modellunterstützung.
- 2026-08-14 — NVIDIA Dynamo v1.4.0 hat aggregierte und disaggregierte SGLang-Rezepte für GLM-5.2 für B200-NVFP4- und H200-FP8-Deployments hinzugefügt.

## Vorgehen {#how-to-use-this}

1. Ein Blackwell/Linux-Deployment-Ziel bestätigen. Der veröffentlichte Checkpoint ist auf B200/B300 getestet und listet SGLang und vLLM als unterstützte Engines.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
2. Für direktes Serving mit der offiziellen SGLang- oder vLLM-Konfiguration beginnen: SGLang benötigt `transformers>=5.3.0` und `modelopt_fp4`; das vLLM-Beispiel verwendet `vllm/vllm-openai:v0.23.0`, Tensor Parallelism 8, Expert Parallelism, die GLM-Parser und einen FP8-KV-Cache.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
3. Für einen Dynamo-Cluster das B200-NVFP4-Ziel für diesen Checkpoint auswählen, den gemeinsamen Modell-Cache und das Hugging-Face-Token bereitstellen, das passende aggregierte oder disaggregierte Rezept deployen und anschließend dessen OpenAI-kompatiblen Smoke-Test ausführen.
  — <https://docs.nvidia.com/dynamo/dev/recipes/glm-5-2>
4. Genauigkeit, Sicherheit und Systemverhalten an anwendungsspezifischen Daten validieren, bevor der Produktivbetrieb beginnt.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>

## Best Practices {#best-practices}

- Die mitgelieferten Runtime-Versionen und Parser-Flags als Ausgangsvertrag behandeln, nicht als generischen GLM-5.2-Startbefehl.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
- Für NVIDIA Dynamo kein Standard-SGLang-Image anstelle des dokumentierten, nur für die Entwicklung gedachten GLM-5.2-Images verwenden, solange dessen erforderliche Patches nicht in einem stabilen Release enthalten sind.
  — <https://docs.nvidia.com/dynamo/v1.4.2/reference/model-early-access-builds>
- Die Kapazität am Deployment-Rezept planen, nicht am 1M-Limit des Checkpoints: Der dokumentierte B200-NVFP4-Pfad unterstützt bis zu 500K Kontext mit HiCache-CPU-Offload; der H200-FP8-Pfad unterstützt bis zu 250K.
  — <https://docs.nvidia.com/dynamo/dev/recipes/glm-5-2>
- Keine vollständige Quantisierung des Modells ableiten: NVIDIA gibt an, dass nur lineare Operatoren innerhalb der Transformer-Blöcke der MoE-Experten NVFP4-quantisiert sind, während der Shared Expert unquantisiert bleibt.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
- Vor der Verwendung des NIM-Artefakts Manifest und Präzision prüfen, statt sich allein auf das Katalog-Label zu verlassen.
  — <https://catalog.ngc.nvidia.com/orgs/nim/zai-org/models/glm-52/nim-aec724e-nvfp4>

## Abgelöst durch {#superseded-by-this}

- 2026-07-20 — Für die NVIDIA-Dynamo-SGLang-Route wird die generische Anleitung zur stabilen Runtime durch das dokumentierte, nur für die Entwicklung gedachte GLM-5.2-Image ersetzt, bis dessen erforderliche Patches in einem stabilen SGLang-Release verfügbar sind.

## Noch unbekannt {#still-unknown}

- NVIDIA NGC kennzeichnet `nim-aec724e-nvfp4` als NVFP4, beschreibt das Staging-Modell aber als FP8; die öffentliche Seite klärt den genauen Präzisionsvertrag des Artefakts nicht.
- Die Hugging-Face-Oberfläche zeigt 381B Parameter, während die Modellkarte 753B insgesamt und 40B aktiv angibt; die Seite erklärt die Abweichung nicht, daher sollte die Zahl aus der Oberfläche nicht zur Ableitung des Speicherbedarfs verwendet werden.
- Die 1M-Kontextangabe der Karte ist keine End-to-End-Garantie für das Deployment: Die aktuellen Dynamo-Rezepte dokumentieren 500K auf B200 und 250K auf H200.
- Es wurde keine vereinfacht-chinesische Primärquelle speziell zu NVIDIA GLM-5.2-NVFP4 gefunden; chinesischsprachige Wartungs- oder Deployment-Anleitungen bleiben ungeprüft.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/nvidia/GLM-5.2-NVFP4 | nvidia/GLM-5.2-NVFP4 · Hugging Face | 2026-09-06 |
| https://catalog.ngc.nvidia.com/orgs/nim/zai-org/models/glm-52/nim-aec724e-nvfp4 | zai-org GLM-5.2 | NVIDIA NGC | 2026-09-06 |
| https://docs.nvidia.com/dynamo/v1.4.2/reference/model-early-access-builds | Model Early Access Builds | NVIDIA Dynamo Documentation | 2026-09-06 |
| https://docs.nvidia.com/dynamo/dev/reference/releases/v1-4-0 | Dynamo v1.4.0 | NVIDIA Dynamo Documentation | 2026-09-06 |
| https://docs.nvidia.com/dynamo/dev/recipes/glm-5-2 | GLM-5.3/5.2 | NVIDIA Dynamo Documentation | 2026-09-06 |
