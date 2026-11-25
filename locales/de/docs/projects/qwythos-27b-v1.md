---
title: "Qwythos-27B-v1"
category: projects
date: 2026-08-03
tags: [project, qwythos, qwythos-27b-v1, qwythos-27b-v1-release]
aliases: ["Qwythos-27B-v1"]
level: 2
source_sha256: 20404391aea59556952871101f6d9c9566ab31c161efaf2ad81f630de69199af
translation: machine
translated_at: '2026-10-24'
---
# Qwythos-27B-v1 {#qwythos-27b-v1}

**Entwicklungslinie:** `project:qwythos-27b-v1` · Thread `qwythos-27b-v1-release`  
**Letztes Ereignis:** 2026-08-03 · 1 datiertes seit 2026-08-03 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Qwythos-27B-v1 ist ein Open-Weight-Checkpoint in bf16 auf Basis von Qwen3.5-27B für Entwickler, die ein lokales Modell mit Function Calling und Bildeingabe benötigen.

- Kontextfenster: stellt 1.048.576 Token über YaRN 4.0 bereit.
- Vision-Tower und native Multi-Token-Prediction: aus der Basisarchitektur übernommen.
- Post-Training-Pipeline: vollständiges SFT → DPO → ESFT als v1 vor RL.

Das native Fenster umfasst 262.144 Token; die 1M-Konfiguration verschlechtert die Qualität bei kurzen Kontexten.

Der Checkpoint eignet sich für selbst gehostete Agenten- und Tool-Workflows, die Vision-Tower wurde jedoch nicht feinabgestimmt, und sensible Einsatzszenarien erfordern eine externe Prüfung.

## Entwicklungslinie {#development-line}

- **2026-08-03 — Qwythos-27B-v1 auf Hugging Face verlinkt.** Dritte luden FancieF/Qwythos-27B-v1-MLX-VLM-4bit, FancieF/Qwythos-27B-v1-MLX-VLM-bf16 und einen separaten MTP-Draft hoch; dies ist kein neuer offizieller Checkpoint.

## Was sich geändert hat {#what-changed}

2026-07-29 — Empero veröffentlichte Qwythos-27B-v1 und ein offizielles GGUF-Set: ein Vollparameter-Modell mit 27B auf Basis von Qwen3.5-27B unter Apache-2.0, mit 1M Kontext, Vision und MTP. 2026-08-03 — Drittanbieter-Ports des Basismodells Qwythos-27B-v1 für MLX erschienen: FancieF/Qwythos-27B-v1-MLX-VLM-4bit, FancieF/Qwythos-27B-v1-MLX-VLM-bf16 und ein separater MTP-Draft; dies ist kein neuer offizieller Checkpoint.

## So wird es verwendet {#how-to-use-this}

Ab 2026-08-03 sollten Praktiker die verlinkte Hugging-Face-Modellseite als dokumentierte Referenz für Qwythos-27B-v1 verwenden und vor dem Einsatz dort die Angaben in der Model Card und die Verfügbarkeit prüfen.

1. Für die lokale Bereitstellung auf einer GPU mit 24 GB beginnen Sie mit dem offiziellen GGUF Q4_K_M; für Bildeingabe `mmproj-Qwythos-27B-F16.gguf` ergänzen.
  — <https://empero.org/writing/qwythos-27b-the-long-awaited-27b>
2. Für Transformers laden Sie `empero-ai/Qwythos-27B-v1` über `AutoModelForImageTextToText` und verwenden die integrierte Chat-Vorlage.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
3. Für OpenAI-kompatible Bereitstellung betreiben Sie vLLM oder SGLang; bei Kontextlängen nahe 1M erfordert vLLM `VLLM_ALLOW_LONG_MAX_MODEL_LEN=1` und explizit `--max-model-len`.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
4. Für Function Calling übergeben Sie die Definitionen in `tools=[...]` an die integrierte Chat-Vorlage und verarbeiten die üblichen Tool-Call-Blöcke.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>

## Bewährte Praktiken {#best-practices}

- Für agentische Anwendungen und Tool-Nutzung starten Sie mit Temperature 0,6, top_p 0,95, top_k 20, repetition_penalty 1,05 und einem Budget von mindestens 16.384 neuen Token.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
- Wird kein 1M-Kontext benötigt, senken Sie den YaRN-Faktor auf 2.0 für etwa 512k oder kehren zur nativen 262k-Konfiguration zurück, um die Qualität bei kurzen Kontexten zu verbessern.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
- Für K-Quants wählen Sie das offizielle GGUF: Es hält den sensiblen Gated-DeltaNet-Zustandspfad bei Q8_0 oder höher, statt ihn zusammen mit den übrigen Gewichten zu quantisieren.
  — <https://empero.org/writing/qwythos-27b-the-long-awaited-27b>
- Stellen Sie den unzensierten Checkpoint Nutzern nicht ohne anwendungsseitige Richtlinien, Prüfung und Zugriffskontrollen bereit.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>

## Abgelöst durch {#superseded-by-this}

- 2026-08-03: Die Annahme, dieses Datum sei die Veröffentlichung des Basismodells Qwythos-27B-v1, ist überholt; die primäre Ankündigung erfolgte am 2026-07-29, während sich der 3. August auf MLX-Konvertierungen Dritter bezieht.

## Weiterhin unbekannt {#still-unknown}

- Die offizielle Model Card beschreibt v1 und Pläne für RL-v2, primäre Quellen bestätigen jedoch nicht, dass Qwythos-27B-v2 bis 2026-09-05 veröffentlicht wurde.
- Die Liste vom 3. August bestätigt MLX-Konvertierungen Dritter, enthält aber keine unabhängige Bewertung von Qualität, Kompatibilität oder erhaltenen Fähigkeiten des Originalmodells.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/empero-ai/Qwythos-27B-v1 | empero-ai/Qwythos-27B-v1 · Hugging Face | 2026-09-05 |
| https://huggingface.co/models?other=base_model%3Aquantized%3Aempero-ai%2FQwythos-27B-v1 | Quantized Models for empero-ai/Qwythos-27B-v1 – Hugging Face | 2026-09-05 |
| https://empero.org/writing/qwythos-27b-the-long-awaited-27b | Qwythos-27B-v1: the long-awaited 27B — Empero | 2026-09-05 |
| https://huggingface.co/models?other=qwythos | Models – Hugging Face | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:qwythos-27b-v1`, Thread `qwythos-27b-v1-release`, 1 datiertes Ereignis 2026-08-03 → 2026-08-03.
- **Praktischer Hinweis:** Ab 2026-08-03 sollten Praktiker die verlinkte Hugging-Face-Modellseite als dokumentierte Referenz für Qwythos-27B-v1 verwenden und vor dem Einsatz dort die Angaben in der Model Card und die Verfügbarkeit prüfen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was überholt ist.
