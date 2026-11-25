---
title: "Llama 3.1"
category: projects
date: 2024-07-23
tags: [llama-3-1, project]
aliases: ["Llama 3.1"]
level: 3
source_sha256: d39ac0fb4d5c8a2b2545fae035645cd1c9a148ba8363b2ee034d2c7414f2e041
translation: machine
translated_at: '2026-10-24'
---
# Llama 3.1 {#llama-31}

**Entwicklungslinie:** `project:llama-3-1` · Thread `llama-3-1`  
**Letztes Ereignis:** 2024-07-23 · 1 datiert seit 2024-07-23 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Llama 3.1 — Metas statische Modellfamilie von 2024 für Teams, die eine herunterladbare, lizenzierte Alternative zu einer gehosteten Text-Generierungs-API benötigen.

- Vortrainierte und Instruct-Varianten mit 8B, 70B und 405B für Text- und Code-Generierung, mehrsprachige Chats, RAG und toolgestützte Systeme.
- 128K Kontextlänge und acht unterstützte Sprachen.
- Text rein, Text raus; Wissensstand bis Dezember 2023. Das 405B-Modell ist ein Deployment-Problem für mehrere GPUs.

## Entwicklungslinie {#development-line}

- **2024-07-23 — Offizielle Ressourcen für den Zugang zu Llama 3.1 wurden verfügbar.** Am 2024-07-23 eröffneten offizielle Llama-3.1-Ressourcen Wege zu Modell-Downloads, Meta AI, einem Repository für agentische Systeme und einem gehosteten Chat-Modell. Damit wurde die praktische Verfügbarkeit der Linie für Entwickler und Nutzer über diese Kanäle markiert.

## Was sich geändert hat {#what-changed}

- 2024-07-23 — Llama 3.1 erschien mit überarbeiteten 8B- und 70B-Modellen sowie 405B, mit 128K Kontext, acht unterstützten Sprachen, Unterstützung für Tool-Use und begleitenden Sicherheits- und Systemkomponenten.
- 2024-09-25 — Llama 3.2 ergänzte Text-Edge-Modelle mit 1B/3B sowie Vision-Modelle mit 11B/90B; Llama 3.1 blieb rein textbasiert.
- 2024-12-06 — Llama 3.3 brachte ein späteres Instruct-Textmodell mit 70B und 128K Kontext.
- 2025-04-05 — Llama 4 Scout und Maverick führten Metas neuere, nativ multimodale Mixture-of-Experts-Generation von Llama ein.

## Anwendung {#how-to-use-this}

Stand 2024-07-23 konnten Teams Llama 3.1 über die offiziellen Download-, Chat- und Entwicklerkanäle evaluieren. Prüfen Sie vor dem Deployment die genaue Modellvariante und die Bedingungen anhand der offiziellen Materialien.

1. Prüfen Sie, ob die reine Text-Ein- und Ausgabe, der Größenbereich 8B/70B/405B und die Unterstützung für acht Sprachen zum Workload passen; wählen Sie für Assistenten-Chats einen Instruct-Checkpoint.
  — <https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md>
2. Beantragen Sie den gated Zugang und akzeptieren Sie die Llama 3.1 Community License, bevor Sie die Modellgewichte herunterladen.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
3. Starten Sie einen ersten lokalen Chat mit Transformers 4.43+, der offiziellen Instruct-Modell-ID und einer Text-Generation-Pipeline oder AutoModelForCausalLM.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
4. Senden Sie rollenbasierte Nachrichten über tokenizer.apply_chat_template vor der Generierung, statt die Llama-Steuertokens selbst zusammenzusetzen.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
5. Stellen Sie den Checkpoint mit vLLM bereit und rufen Sie /v1/chat/completions für einen OpenAI-kompatiblen lokalen Endpunkt auf.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
6. Planen Sie für 405B FP8 einen Node mit 8×80GB H100-GPUs ein; für den unquantisierten 405B-Checkpoint verwenden Sie Multi-Node-Inferenz.
  — <https://github.com/meta-llama/llama-cookbook/blob/main/getting-started/inference/local_inference/README.md>

## Best Practices {#best-practices}

- Verwenden Sie für Assistenten-Dialoge ein Instruct-Modell; das vortrainierte Basismodell behalten Sie für Adaption oder andere Textgenerierung.
  — <https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md>
- Bewahren Sie das offizielle Chat-Template mit apply_chat_template, einschließlich des Generation-Prompts.
  — <https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct>
- Befolgen Sie die Llama 3.1 Community License als Voraussetzung für die Weitergabe: Verteilte Materialien und Dienste unterliegen Namensnennungspflichten, und Produkte mit mehr als 700 Millionen monatlich aktiven Nutzern benötigen eine separate Lizenz von Meta.
  — <https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct-FP8>
- Testen Sie die Sicherheit und passen Sie das Modell für die Anwendung an, und sichern Sie das Modell anschließend mit Schutzmechanismen rund um das Modell und externe Tools ab; setzen Sie das Modell nicht allein ein.
  — <https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md>
- Kalkulieren Sie 405B nicht allein anhand der Parameterbezeichnung: Trennen Sie das FP8-Serving auf einem Node von der unquantisierten Multi-Node-Bereitstellung.
  — <https://github.com/meta-llama/llama-cookbook/blob/main/getting-started/inference/local_inference/README.md>

## Durch diesen Stand überholt {#superseded-by-this}

- 2024-09-25 — Die Wahl von Llama 3.1 für die Verarbeitung von Text oder Bildern auf dem Gerät ist veraltet; Llama 3.2 führte die Pfade 1B/3B für Edge-Text und 11B/90B für Vision ein.
- 2024-12-06 — Der alleinige Vergleich von Llama 3.1 70B oder 405B für einen neuen Meta-70B-Textdienst ist veraltet; Llama 3.3 70B Instruct ist die spätere Option mit 128K.
- 2025-04-05 — Llama 3.1 als neueste Llama-Generation von Meta zu bezeichnen, ist veraltet; Llama 4 brachte native Multimodalität und Mixture-of-Experts-Modelle.

## Weiterhin unbekannt {#still-unknown}

- Die Quellen- und X-Links lieferten in diesem Durchgang keinen abrufbaren Text. Wir verwenden daher nur deren Datum und URLs, nicht unverifizierte Aussagen.
- Der historische Link llama-agentic-system leitet auf ogx-ai/llama-stack-apps weiter. Diese Seite enthält keine datierte Herkunft von Meta, weshalb wir sie nicht als aktuelle offizielle Leitlinie von Meta behandeln.
- Wir fanden eine chinesische Hugging-Face-Übersetzung vom selben Tag, aber keine separate primäre Ankündigung von Meta. Wir treffen keine China-spezifischen Aussagen zu Verfügbarkeit oder Kompatibilität.
- Uns liegen keine Angaben zu Workload, Hardware-Budget, Zielregion oder Lizenzkontext vor. Deshalb wählen wir weder eine bestimmte Llama-3.1-Größe noch einen späteren Nachfolger aus.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://ai.meta.com/blog/meta-llama-3-1/ | Introducing Llama 3.1: Our most capable models to date | 2026-09-04 |
| https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md | Llama 3.1 model card — meta-llama/llama-models | 2026-09-04 |
| https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct | meta-llama/Llama-3.1-8B-Instruct | 2026-09-04 |
| https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct-FP8 | meta-llama/Llama-3.1-405B-Instruct-FP8 | 2026-09-04 |
| https://github.com/meta-llama/llama-cookbook/blob/main/getting-started/inference/local_inference/README.md | Llama Cookbook — local inference guide | 2026-09-04 |
| https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/ | Llama 3.2: Revolutionizing edge AI and vision with open, customizable models | 2026-09-04 |
| https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/MODEL_CARD.md | Llama 3.3 model card — meta-llama/llama-models | 2026-09-04 |
| https://ai.meta.com/blog/llama-4-multimodal-intelligence/ | The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation | 2026-09-04 |
| https://github.com/meta-llama/llama-agentic-system | llama-agentic-system URL, currently redirected to ogx-ai/llama-stack-apps | 2026-09-04 |
| https://huggingface.co/blog/zh/llama31 | Llama 3.1：405B/70B/8B 模型的多语言与长上下文能力解析 | 2026-09-04 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:llama-3-1`, Thread `llama-3-1`, 1 datiertes Ereignis 2024-07-23 → 2024-07-23.
- **Praxishinweis:** Stand 2024-07-23 konnten Praktiker Llama 3.1 über die offiziellen Download-, Chat- und Entwicklerressourcen evaluieren. Prüfen Sie vor dem Deployment die genaue Modellvariante und die geltenden Bedingungen anhand der offiziellen Materialien.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, sind die datierten Überholungshinweise maßgeblich.
