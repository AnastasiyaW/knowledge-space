---
title: "FLUX.2 [Klein] KV - 9B — Modellveröffentlichung und lokale Inferenz"
category: projects
date: 2026-03-13
tags: [flux-2-klein-9b-kv, image_generation, model-release-and-local-inference, project]
aliases: ["FLUX.2 [Klein] KV - 9B"]
level: 2
source_sha256: 4db475c685d746015e7f0c3e93dec0dc9380b137476fcf1b8cd6d542eccc8eae
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 [Klein] KV - 9B — Modellveröffentlichung und lokale Inferenz {#flux2-klein-kv-9b-model-release-and-local-inference}

**Entwicklungsstrang:** `project:flux-2-klein-9b-kv` · Thread `model-release-and-local-inference`  
**Letztes Ereignis:** 2026-03-13 · 1 datiertes seit 2026-03-13 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

FLUX.2 [klein] 9B-KV ist ein 9B-Flow-Modell für lokale oder API-Bearbeitung, wenn das normale FLUX.2 [klein] 9B bei wiederholter Verarbeitung derselben Referenzen Zeit verliert. — Text-zu-Bild; — Bearbeitung eines einzelnen Bildes; — Multi-Referenz-Bearbeitung mit KV-Cache; — BF16 und die offizielle FP8-Variante sowie Quantisierungen Dritter im GGUF-Format. Kennzahlen: 9B-Flow-Modell, 8B-Qwen3-Text-Embedder, 4 Schritte; die offizielle BF16-Variante benötigt etwa 29 GB VRAM und ist für RTX 5090 oder höher ausgelegt. Fazit: Wählen Sie es für iterative Multi-Referenz-Bearbeitung, nicht zur Beschleunigung reiner Text-zu-Bild-Generierung.

## Entwicklungsstrang {#development-line}

- **2026-03-13 — Verfügbarkeit des FLUX.2 Klein 9B KV Modells und Ressourcen für die lokale Nutzung.** Schritt null berechnet K/V der Referenzen, die Schritte 1–3 verwenden den Cache erneut. Die offizielle Modellkarte nennt bis zu 2,5× für Multi-Referenz-Bearbeitung; eine detailliertere Tabelle zeigt die Abhängigkeit von Anzahl der Referenzen und Auflösung — von 1,21× bis 2,66×.

## Was sich geändert hat {#what-changed}

2026-01-15 — Black Forest Labs veröffentlichte die Familie FLUX.2 [klein]: Das 9B-Modell vereinte bereits Text-zu-Bild, Bearbeitung mit einer und mehreren Referenzen in einem 4-Schritt-Distilled-Modell. 2026-03-12 — das offizielle Inference-Repository erhielt den Commit „FLUX.2 [klein] KV“: einen eigenen Pfad zum Caching von Referenzen, die Auswahl von `flux.2-klein-9b-kv` im CLI und eine Beschleunigungstabelle. 2026-03-13 — FLUX.2 [klein] 9B-KV erschien als exakte 9B-Variante mit K/V-Caching: Schritt null berechnet K/V der Referenzen, die Schritte 1–3 verwenden den Cache erneut. Die offizielle Modellkarte nennt bis zu 2,5× für Multi-Referenz-Bearbeitung; eine detailliertere Tabelle zeigt die Abhängigkeit von Anzahl der Referenzen und Auflösung — von 1,21× bis 2,66×.

## Verwendung {#how-to-use-this}

Ab 2026-03-13 sollten Praktiker diesen Strang anhand des verlinkten Hugging-Face-Checkpoints oder der Demo bewerten und bei der Wahl eines lokalen Inferenzpfads die verlinkten GGUF- und ComfyUI-Workflow-Ressourcen nutzen.

1. Akzeptieren Sie die Bedingungen des gated Modells und der FLUX Non-Commercial License, laden Sie danach den offiziellen BF16-Checkpoint oder die FP8-Variante herunter.
  — <https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv>
2. Für den lokalen Python-Pfad aktualisieren Sie Diffusers von GitHub, laden `Flux2KleinKVPipeline`, verschieben die Pipeline in bfloat16 auf CUDA und beginnen mit 1024×1024 und 4 Inference-Schritten.
  — <https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv>
3. Für das offizielle CLI setzen Sie `KLEIN_9B_KV_MODEL_PATH`, starten `scripts/cli.py --model_name flux.2-klein-9b-kv`, geben ein oder mehrere `input_images` an und danach die Textanweisung.
  — <https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md>
4. Für ComfyUI mit kleinerem Speicher- und VRAM-Budget können Sie eine GGUF-Variante eines Drittanbieters in `ComfyUI/models/unet` ablegen, ComfyUI-GGUF installieren und einen kompatiblen Workflow importieren; dies ist ein Community-Pfad und keine offizielle Runtime von BFL.
  — <https://huggingface.co/QuantStack/FLUX.2-Klein-9B-KV-GGUF>
5. Für den Cloud-Start verwenden Sie den aktuellen `flux-2-klein-9b-preview` für die neuesten KV-Verbesserungen oder das fixierte `flux-2-klein-9b`, wenn Reproduzierbarkeit wichtig ist; fragen Sie die zurückgegebene `polling_url` ab.
  — <https://docs.bfl.ai/quick_start/generating_images>

## Bewährte Praktiken {#best-practices}

- Rechnen Sie mit einer Beschleunigung nur bei bildkonditionierten Aufgaben: Der Cache speichert genau die K/V der Referenzbilder.
  — <https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md>
- Prüfen Sie den Gewinn bei Ihrer Anzahl an Referenzen und Ihrer Auflösung: Die offizielle Tabelle gibt für vier Referenzen 2,66× bei 512×512, aber nur 1,85× bei 1440×1440 an.
  — <https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md>
- Schreiben Sie eine ausführliche, beschreibende Anweisung: FLUX.2 [klein] hat kein Prompt-Upsampling, daher müssen wichtige Objekte, Änderungen und zu erhaltende Eigenschaften explizit benannt werden.
  — <https://docs.bfl.ai/flux_2/flux2_overview>
- Übertragen Sie die Anforderung von 13 GB VRAM von Klein 4B nicht auf 9B-KV: Für das offizielle 9B-KV ist ein Richtwert von etwa 29 GB VRAM angegeben.
  — <https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv>
- Für stabile Produktionsergebnisse wählen Sie einen nicht als Preview gekennzeichneten API-Endpoint; die Preview ist für die neuesten Gewichtsänderungen gedacht.
  — <https://docs.bfl.ai/flux_2/flux2_overview>

## Durch diesen Stand abgelöst {#superseded-by-this}

- 2026-03-12 — Die manuelle Aktivierung des KV-Caches im offiziellen CLI ist nicht nötig: Die Auswahl von `flux.2-klein-9b-kv` aktiviert den KV-Pfad automatisch.
- 2026-03-13 — Für Multi-Referenz-Bearbeitung ist das normale FLUX.2 [klein] 9B nicht mehr die bevorzugte Wahl für niedrige Latenz; 9B-KV behält seine Fähigkeiten und vermeidet die wiederholte Verarbeitung der Referenzen.
- 2026-09-05 — Die Preview-API-Variante darf nicht als reproduzierbar gelten: Die aktuelle Dokumentation trennt das veränderliche `flux-2-klein-9b-preview` vom fixierten `flux-2-klein-9b`.

## Noch unklar {#still-unknown}

- Ein unabhängiger Lauf wurde nicht durchgeführt: Die angegebenen Beschleunigungen sind offizielle Messungen, aber die Modellkarte legt den vollständigen Benchmark-Aufbau nicht offen und ersetzt keine Messung mit den eigenen Referenzen und der eigenen Auflösung.
- BF16, FP8 und GGUF sind keine austauschbaren Runtime-Pfade: Die GGUF-Konvertierung, ComfyUI-GGUF und der YarvixPA-Workflow sind Integrationen Dritter und haben hier keine unabhängige End-to-End-Bestätigung.
- Die chinesischsprachige Suche ergab einen sekundären ComfyUI-Leitfaden, aber keine Primärquelle; seine Empfehlungen wurden nicht als offizielle Kompatibilität eingestuft.
- Es gibt keinen Hinweis darauf, dass sich die Links auf unterschiedliche Modelle beziehen: BF16 und FP8 sind offizielle Varianten desselben 9B-KV, und GGUF ist eine direkte Quantisierung durch Dritte auf dieser Basis.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv | black-forest-labs/FLUX.2-klein-9b-kv · Hugging Face | 2026-09-05 |
| https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv-fp8 | black-forest-labs/FLUX.2-klein-9b-kv-fp8 · Hugging Face | 2026-09-05 |
| https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md | FLUX.2 [klein] 9B KV Cache — official inference documentation | 2026-09-05 |
| https://github.com/black-forest-labs/flux2/commits/main/docs/flux2_klein_kv_cache.md | History for flux2_klein_kv_cache.md — commit “FLUX.2 [klein] KV”, 2026-03-12 | 2026-09-05 |
| https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence | FLUX.2 [klein]: Towards Interactive Visual Intelligence — Black Forest Labs, 2026-01-15 | 2026-09-05 |
| https://docs.bfl.ai/flux_2/flux2_overview | FLUX.2 Overview — Black Forest Labs documentation | 2026-09-05 |
| https://docs.bfl.ai/quick_start/generating_images | Image Generation with Text Prompts — Black Forest Labs documentation | 2026-09-05 |
| https://huggingface.co/QuantStack/FLUX.2-Klein-9B-KV-GGUF | QuantStack/FLUX.2-Klein-9B-KV-GGUF · Hugging Face | 2026-09-05 |
| https://github.com/YarvixPA/ComfyUI-YarvixPA/blob/main/example_workflows/YarvixPA%20-%20Flux2%209B%20KV%20-%20GGUF.json | YarvixPA — Flux2 9B KV GGUF workflow | 2026-09-05 |
| https://www.stablediffusiontutorials.com/2026/03/flux2-klein-9b-kv.html | Flux2 Klein 9B KV (BF16/FP8/GGUF): Improved Multi-Editing, 2026-03-13 | 2026-09-05 |
| https://www.runcomfy.com/zh-CN/comfyui-workflows/flux-2-klein-9b-kv-image-edit-in-comfyui-precision-prompt-editing | FLUX.2 Klein 9B KV ComfyUI image-edit guide, Simplified Chinese | 2026-09-05 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:flux-2-klein-9b-kv`, Thread `model-release-and-local-inference`, 1 datiertes Ereignis 2026-03-13 → 2026-03-13.
- **Praktischer Hinweis:** Ab 2026-03-13 sollten Praktiker diesen Strang anhand des verlinkten Hugging-Face-Checkpoints oder der Demo bewerten und bei der Wahl eines lokalen Inferenzpfads die verlinkten GGUF- und ComfyUI-Workflow-Ressourcen nutzen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
