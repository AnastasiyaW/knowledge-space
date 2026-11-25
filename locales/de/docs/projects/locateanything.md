---
title: "LocateAnything — Modellveröffentlichung"
category: projects
date: 2026-05-29
tags: [locateanything, model-release, project]
aliases: ["LocateAnything"]
level: 2
source_sha256: 13716cd93545597bbd693144635af28a8b822c3b2717b86df01e60a9a3c50880
translation: machine
translated_at: '2026-10-24'
---
# LocateAnything — Modellveröffentlichung {#locateanything-model-release}

**Entwicklungslinie:** `project:locateanything` · Thread `model-release`  
**Letztes Ereignis:** 2026-05-29 · 1 datiertes seit 2026-05-29 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

LocateAnything ist ein Forschungsmodell von NVIDIA mit 3B Parametern aus der Eagle-Familie für Visual Grounding: Objekterkennung, Referring-Expression Grounding, GUI Grounding, OCR/Textlokalisierung, Layout Grounding und Pointing. Es sagt eine vollständige Bounding Box parallel voraus, statt Koordinaten Token für Token zu erzeugen; angegeben werden 12,7 Boxen/s auf einer H100 im Hybrid Mode. Fazit: geeignet für F&E und die lokale Integration von Lokalisierungsaufgaben, die veröffentlichten Gewichte haben jedoch eine nicht-kommerzielle Lizenz.

## Entwicklungslinie {#development-line}

- **2026-05-29 — NVIDIA veröffentlichte LocateAnything-Ressourcen und eine Modellseite für LocateAnything-3B.** Am 2026-05-29 wurden die Forschungsseite von NVIDIA zu LocateAnything und die verlinkte Hugging-Face-Modellseite NVIDIA LocateAnything-3B geteilt. Dies markiert einen öffentlichen Schritt der Projekt- und Modellverfügbarkeit in der Entwicklungsgeschichte von LocateAnything.

## Was sich geändert hat {#what-changed}

2026-05-29 — LocateAnything wurde als LocateAnything-3B verfügbar; die Primärmaterialien präzisieren, dass die Veröffentlichung von Code, Gewichten, Demo, Webseite und Bericht auf 2026-05-26 datiert ist, nicht auf den 29. Mai. Das Modell kombiniert MoonViT-SO-400M, Qwen2.5-3B-Instruct und einen MLP-Projektor; Parallel Box Decoding sagt x1, y1, x2, y2 in einem Block voraus. Trainingsdaten: 12 Mio. Bilder, 138 Mio.+ Anfragen und 785 Mio. Boxen. 2026-06 — in Eagle wurden Batch-Inferenz auf FlashAttention für A100/RTX 4090 und ein LoRA-Skript für Visual-Prompt-Feinetuning ergänzt; der öffentliche Basis-Checkpoint unterstützt Visual-Prompt-Inferenz ohne Feinetuning weiterhin nicht.

## Anwendung {#how-to-use-this}

Ab 2026-05-29 können Praktiker LocateAnything über die öffentliche Forschungsressource von NVIDIA und die verlinkte Modellseite LocateAnything-3B bewerten, bevor sie es für Objektlokalisierungs-Workflows auswählen.

1. Klonen Sie NVlabs/Eagle, wechseln Sie in Embodied und installieren Sie das Paket mit dem Befehl pip install -e .
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
2. Laden Sie nvidia/LocateAnything-3B über LocateAnythingWorker, übergeben Sie ein RGB-Bild und rufen Sie detect, ground_multi, detect_text, ground_gui oder point auf.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
3. Parsen Sie die Antwort: Die Box-Koordinaten liegen im Bereich 0–1000, daher skalieren Sie sie auf Breite und Höhe des Originalbildes.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
4. Für die Stapelverarbeitung laden Sie das Modell-Repository herunter und starten batch_infer.py mit --attn la_flash und einer passenden Batch-Größe.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>

## Best Practices {#best-practices}

- Verwenden Sie für den regulären Betrieb den Hybrid Mode: Der Fast Mode ist standardmäßig aktiv, problematische Blöcke werden im Slow Mode nachverarbeitet.
  — <https://research.nvidia.com/labs/lpr/locate-anything/>
- Setzen Sie für eine vollständige Antwort max_new_tokens=8192; die Modellkarte empfiehlt den Hybrid Mode als Kompromiss zwischen Geschwindigkeit und Genauigkeit.
  — <https://huggingface.co/nvidia/LocateAnything-3B>
- Auf A100 und anderen GPUs außerhalb von Hopper/Blackwell verwenden Sie die la_flash-Batch-Laufzeit statt dense SDPA; das veröffentlichte A100-Beispiel senkt den reservierten Spitzenspeicher von 35,12 GB auf 11,71 GB.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
- Rechnen Sie bei dem ursprünglichen nvidia/LocateAnything-3B nicht mit Visual-Prompt-Inferenz: Dafür ist ein eigenes Feinetuning auf Basis des veröffentlichten Codes erforderlich.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>

## Hierdurch abgelöst {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Die Primärquellen datieren die erste Veröffentlichung auf 2026-05-26, das Ereignis ist dagegen auf 2026-05-29 erfasst; die verfügbaren Materialien erklären die dreitägige Abweichung nicht.
- Für die Juni-Aktualisierungen von Eagle wird nur der Monat, nicht der genaue Tag veröffentlicht, daher lassen sie sich nicht verlässlich einzelnen Tagesereignissen zuordnen.
- Es gibt keinen Primärnachweis, dass die öffentlichen Gewichte eine kommerzielle Genehmigung erhalten haben; die Modellkarte beschränkt sie weiterhin auf akademische und nicht-kommerzielle Forschung.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://research.nvidia.com/labs/lpr/locate-anything/ | LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding | 2026-09-05 |
| https://huggingface.co/nvidia/LocateAnything-3B | nvidia/LocateAnything-3B model card | 2026-09-05 |
| https://github.com/NVlabs/EAGLE | NVlabs/Eagle repository | 2026-09-05 |
| https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md | LocateAnything implementation and usage guide | 2026-09-05 |
| https://arxiv.org/abs/2605.27365 | LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:locateanything`, Thread `model-release`, 1 datiertes Ereignis 2026-05-29 → 2026-05-29.
- **Praxishinweis:** Ab 2026-05-29 können Praktiker LocateAnything über die öffentliche Forschungsressource von NVIDIA und die verlinkte Modellseite LocateAnything-3B bewerten, bevor sie es für Objektlokalisierungs-Workflows auswählen.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
