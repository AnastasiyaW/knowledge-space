---
title: "Huihui-Qwen3.8-27B-abliterated — Öffentliche Verfügbarkeit des Modells"
category: projects
date: 2026-08-17
tags: [huihui-ai/huihui-qwen3.8-27b-abliterated, huihui-qwen3-8-27b-abliterated, project, public-model-availability]
aliases: ["Huihui-Qwen3.8-27B-abliterated"]
level: 2
source_sha256: 2330aa43f3e8ed29cb0650b16081ff13298e00d2ab6da0445e79bd2cc204f635
translation: machine
translated_at: '2026-10-24'
---
# Huihui-Qwen3.8-27B-abliterated — Öffentliche Verfügbarkeit des Modells {#huihui-qwen38-27b-abliterated-public-model-availability}

**Entwicklungslinie:** `project:huihui-qwen3-8-27b-abliterated` · Thread `public-model-availability`  
**Letztes Ereignis:** 2026-08-17 · 1 datiert seit 2026-08-17 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Huihui-Qwen3.8-27B-abliterated ist eine abliterated Variante des Basismodells Qwen3.8-27B für Entwickler, die einen offenen multimodalen Checkpoint benötigen, der mit Transformers, vLLM oder SGLang kompatibel ist.

- Chat für dialogorientierte Textgenerierung.
- Bildverarbeitung für visuelle Eingaben.
- OpenAI-kompatibles Serving für Remote-API-Aufrufe.

Die Sicherheitsfilterung ist deutlich reduziert, und die Model Card empfiehlt Forschung und kontrollierte Umgebungen. Das Modell ist kein Ersatz für ein sicheres Produktionsmodell.

## Entwicklungslinie {#development-line}

- **2026-08-17 — Huihui-Qwen3.8-27B-abliterated wurde über Hugging Face öffentlich verfügbar.** Das Artefakt enthält 18 Safetensors-Dateien und belegt 55,6 GB; das README legt fest, dass MTP und die Vision-Komponente unverändert bleiben.

## Was sich geändert hat {#what-changed}

2026-08-17 — verifizierte Revision d42ca89 ist fixiert: Das Artefakt enthält 18 Safetensors-Dateien und belegt 55,6 GB; das README stellt klar, dass MTP und die Vision-Komponente unverändert bleiben.

Die Model Card gibt an, dass die Abliteration nur auf die Layer 18–51 angewendet wird, um den Großteil der ursprünglichen Leistung zu erhalten. Wir können die vorherige Version auf Revision d42ca89 festlegen.

## Verwendung {#how-to-use-this}

Stand 2026-08-17 können wir Huihui-Qwen3.8-27B-abliterated als öffentlich auffindbare Modelllinie behandeln und das verlinkte Modellartefakt, verwandte quantisierte Varianten und den ZeroGPU Space evaluieren. Die datierten Links allein rechtfertigen weder die Auswahl einer bestimmten Variante noch die Verlassung auf Leistungsaussagen.

1. Für lokale multimodale Läufe AutoProcessor und AutoModelForMultimodalLM laden, Nachrichten mit Text und Bildern über das Chat-Template formatieren und `generate` aufrufen.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
2. Für einen OpenAI-kompatiblen Endpunkt vLLM installieren, `vllm serve "huihui-ai/Huihui-Qwen3.8-27B-abliterated"` ausführen und Anfragen an `/v1/chat/completions` senden.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
3. Für SGLang `python3 -m sglang.launch_server --model-path "huihui-ai/Huihui-Qwen3.8-27B-abliterated"` ausführen und den Endpunkt auf dem gewählten Port verwenden.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>

## Best Practices {#best-practices}

- Die Revision für reproduzierbare Läufe festlegen: Die Model Card verweist für die frühere Version direkt auf d42ca89.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
- Eine manuelle Prüfung der Ausgaben beibehalten und den Checkpoint nicht direkt in öffentlichen oder risikoreichen Produkten einsetzen: Der Autor warnt vor reduzierter Sicherheitsfilterung.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
- Für llama.cpp, Ollama oder LM Studio separate abgeleitete Quantisierungen wählen, statt das BF16-Repository als für diese Laufzeitumgebungen einsatzbereit zu betrachten.
  — <https://huggingface.co/models?other=base_model%3Aquantized%3Ahuihui-ai%2FHuihui-Qwen3.8-27B-abliterated>

## Dadurch abgelöst {#superseded-by-this}

- Nach 2026-08-17 wurde die Beschreibung der fixierten Revision d42ca89 mit nur unverändertem MTP obsolet: Ihr README stellte klar, dass auch die Vision-Komponente unverändert ist.

## Weiterhin unbekannt {#still-unknown}

- In der verfügbaren primären Historie ist der genaue Kalenderzeitpunkt für Commit d42ca89 relativ angegeben („19 days ago“); er entspricht am Prüfdatum 2026-08-17, aber die primäre Quelle lieferte keinen ISO-Zeitstempel.
- Ob der ZeroGPU Space aus dem Ereignis ein offizieller Startpfad ist oder dieselbe Modellrevision repräsentiert, bleibt unbestätigt.
- Das Datum der nachfolgenden Abliteration-Änderung auf die Layer 18–51 erscheint in der verfügbaren primären Ausgabe nicht; daher führen wir sie nicht als eigenes datiertes Ereignis auf.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated | huihui-ai/Huihui-Qwen3.8-27B-abliterated — Hugging Face Model Card | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated/commit/d42ca8978c5a66e92c3446d46e8adfe03ef692ff | Update README.md · huihui-ai/Huihui-Qwen3.8-27B-abliterated at d42ca89 | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated/tree/d42ca8978c5a66e92c3446d46e8adfe03ef692ff | huihui-ai/Huihui-Qwen3.8-27B-abliterated at d42ca89 | 2026-09-05 |
| https://huggingface.co/models?other=base_model%3Aquantized%3Ahuihui-ai%2FHuihui-Qwen3.8-27B-abliterated | Quantized Models for huihui-ai/Huihui-Qwen3.8-27B-abliterated | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.8-27B | Qwen/Qwen3.8-27B — Hugging Face Model Card | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:huihui-qwen3-8-27b-abliterated`, Thread `public-model-availability`, 1 datiertes Ereignis 2026-08-17 → 2026-08-17.
- **Praktischer Hinweis:** Stand 2026-08-17 können Praktiker Huihui-Qwen3.8-27B-abliterated als öffentlich auffindbare Modelllinie behandeln und das verlinkte Modellartefakt, verwandte quantisierte Varianten und den ZeroGPU Space evaluieren. Die datierten Links allein rechtfertigen weder die Auswahl einer bestimmten Variante noch die Verlassung auf Leistungsaussagen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was obsolet ist.
