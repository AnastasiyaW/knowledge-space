---
title: "Tencent Hunyuan — Hunyuan-Modellveröffentlichungen"
category: projects
date: 2025-07-04
tags: [hunyuan, hunyuan-model-releases, project, tencent-hunyuan, tencent_hunyuan]
aliases: ["Hunyuan-A13B", "Tencent Hunyuan"]
level: 2
source_sha256: 1c002261b69a8bcfced9d5f1c4ded7b39ea6e7aa738ebb1425fed32b4816ee2f
translation: machine
translated_at: '2026-10-24'
---
# Tencent Hunyuan — Hunyuan-Modellveröffentlichungen {#tencent-hunyuan-hunyuan-model-releases}

**Entwicklungslinie:** `project:tencent-hunyuan` · Thread `hunyuan-model-releases`  
**Letztes Ereignis:** 2025-07-04 · 2 datierte Einträge seit 2024-07-02 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Tencent Hunyuan ist keine einzelne, durchgehende Modellreihe, sondern eine Dachmarke für mehrere nicht miteinander kompatible Familien: HunyuanDiT für die Bildgenerierung und Hunyuan-A13B für Text, Reasoning und Tool Calling. Hunyuan-A13B: 80B Parameter, 13B aktiv, Kontext 256K. Praktische Schlussfolgerung: Für ein neues LLM-Projekt wird A13B mit dem offiziellen Serving-Pfad verwendet; DiT wird nur zur Unterstützung einer bestehenden T2I-Pipeline gewählt.

## Entwicklungslinie {#development-line}

- **2024-07-02 — Tencent-Hunyuan-Ressourcen rund um HunyuanDiT v1.2 wurden erfasst.** Am 2024-07-02 verlinkte der Eintrag die Modellseite von HunyuanDiT-v1.2, den Hunyuan-Captioner-Space und das Hugging-Face-Profil von Tencent-Hunyuan. Allein anhand der Links ergibt sich ein datierter öffentlicher Ressourcenbestand zu HunyuanDiT v1.2 und Captioning-Tools, nicht jedoch, ob diese Assets an diesem Tag veröffentlicht oder aktualisiert wurden.
- **2025-07-04 — Ressourcen zu Tencent Hunyuan A13B Instruct wurden erfasst.** 80B Gesamt- und 13B aktive Parameter, Modi thinking/no-thinking, 256K-Kontext sowie die offiziellen Pfade für Transformers, vLLM, SGLang und Docker.

## Was sich geändert hat {#what-changed}

2024-07-02 — HunyuanDiT v1.2 war als Paket aus Gewichten und Code für zweisprachige Text-zu-Bild-Generierung verfügbar; dabei handelte es sich nicht um ein LLM. 2024-07-08 — HYDiT/HunyuanDiT v1.2 wurde veröffentlicht; das offizielle Repository trennt dieses Update von den am 2. Juli veröffentlichten Materialien. 2024-07-15 — Für HunyuanDiT 1.1/1.2 wurden standardisierte ComfyUI-Workflows und LoRA-Kompatibilität ergänzt. 2025-06-27 — Tencent hat Hunyuan-A13B-Pretrain, Instruct, Instruct-FP8 und Instruct-GPTQ-Int4 als Open Source veröffentlicht; dabei handelt es sich um eine eigenständige MoE-LLM-Linie und nicht um eine Nachfolgeversion des DiT. 2025-07-04 — Die Aktualität dieses Schritts wird durch das A13B-Release bestätigt: 80B Gesamt- und 13B aktive Parameter, Modi thinking/no-thinking, 256K-Kontext sowie die offiziellen Pfade für Transformers, vLLM, SGLang und Docker.

## Anwendung {#how-to-use-this}

Stand 2025-07-04 sollten Praktiker die datierten öffentlichen Referenzen von Tencent Hunyuan als voneinander getrennte Checkpoints behandeln: Für die Bildmodelllinie von 2024 sind die Ressourcen zu HunyuanDiT v1.2/Captioning zu prüfen, für die Sprachmodelllinie von 2025 das A13B-Instruct-Modell samt Code-Repository. Man sollte nicht davon ausgehen, dass es sich um eine austauschbare, einheitliche Implementierung handelt.

1. Wählen Sie `tencent/Hunyuan-A13B-Instruct` für einen Chat-, Reasoning- oder Tool-Calling-Dienst; laden Sie es über Transformers mit `trust_remote_code=True` und dem Standard-Chat-Template.
  — <https://huggingface.co/tencent/Hunyuan-A13B-Instruct>
2. Für eine OpenAI-kompatible lokale API starten Sie A13B mit `vllm serve "tencent/Hunyuan-A13B-Instruct"`.
  — <https://huggingface.co/tencent/Hunyuan-A13B-Instruct>
3. Deaktivieren Sie Reasoning über `enable_thinking=False` oder das Präfix `/no_think`, wenn Latenz wichtiger ist als ausführliche Begründung.
  — <https://github.com/Tencent-Hunyuan/Hunyuan-A13B>
4. Für eine bestehende HunyuanDiT-Image-Pipeline verwenden Sie die Diffusers-Pipeline `Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers`; für schnellere Inferenz steht eine distillierte Variante zur Verfügung.
  — <https://github.com/Tencent-Hunyuan/HunyuanDiT>

## Best Practices {#best-practices}

- Vermischen Sie Gewichte, APIs und Erwartungen von HunyuanDiT nicht mit denen von A13B: Es handelt sich um einen T2I-Diffusion-Transformer bzw. ein MoE-LLM.
  — <https://github.com/Tencent-Hunyuan/HunyuanDiT>
- Für HunyuanDiT-ControlNet verwenden Sie die distillierten Basisgewichte, denn genau auf diesen wurden die veröffentlichten ControlNet-Gewichte trainiert.
  — <https://github.com/Tencent-Hunyuan/HunyuanDiT>
- Verwenden Sie für A13B beim lokalen Serving den offiziellen Container oder das dokumentierte Backend und prüfen Sie das Verhalten des Thinking-Modus an Ihren eigenen Aufgaben, bevor Sie ihn in eine agentische Route aufnehmen.
  — <https://github.com/Tencent-Hunyuan/Hunyuan-A13B>

## Durch diesen Eintrag abgelöst {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Die beiden datierten Einträge betreffen unterschiedliche Modalitäten: HunyuanDiT dient der Bildgenerierung, Hunyuan-A13B ist ein sprachliches MoE-Modell. Belege dafür, dass A13B den DiT ersetzt, gibt es nicht.
- Für das Ereignis vom 2024-07-02 wurde kein unabhängiges Primärmaterial gefunden, das das Release von v1.2 genau auf den 2. Juli datiert; das offizielle Changelog nennt für die Veröffentlichung von v1.2 den 2024-07-08.
- event_findings: 2025-07-04 — Das offizielle Repository datiert die Öffnung der vier A13B-Varianten auf 2025-06-27; Quelle: https://github.com/Tencent-Hunyuan/Hunyuan-A13B. Neue eigenständige Ereignisse: 2024-07-08 — Veröffentlichung von HYDiT v1.2; 2024-07-15 — ComfyUI-Workflows und LoRA-Kompatibilität; Quelle: https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.2.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.2 | Tencent-Hunyuan/HunyuanDiT-v1.2 Model Card | 2026-09-05 |
| https://github.com/Tencent-Hunyuan/HunyuanDiT | Tencent-Hunyuan/HunyuanDiT | 2026-09-05 |
| https://huggingface.co/tencent/Hunyuan-A13B-Instruct | tencent/Hunyuan-A13B-Instruct Model Card | 2026-09-05 |
| https://github.com/Tencent-Hunyuan/Hunyuan-A13B | Tencent-Hunyuan/Hunyuan-A13B | 2026-09-05 |
| https://developer.cloud.tencent.com/article/2536652?policyId=1003 | Tencent Hunyuan veröffentlicht erstes Open-Source-MoE-Modell mit hybridem Reasoning, starker Leistung und nur 13B aktiven Parametern | 2026-09-05 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:tencent-hunyuan`, Thread `hunyuan-model-releases`, 2 datierte Ereignisse 2024-07-02 → 2025-07-04.
- **Praktischer Hinweis:** Stand 2025-07-04 sollten Praktiker die datierten öffentlichen Referenzen von Tencent Hunyuan als getrennte Checkpoints behandeln: Für die Bildmodelllinie von 2024 sind die Ressourcen zu HunyuanDiT v1.2/Captioning zu prüfen, für die Sprachmodelllinie von 2025 das A13B-Instruct-Modell samt Code-Repository. Man sollte nicht davon ausgehen, dass es sich um eine austauschbare, einheitliche Implementierung handelt.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
