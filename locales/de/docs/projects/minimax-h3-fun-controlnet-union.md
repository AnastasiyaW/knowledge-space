---
title: "MiniMax-H3-Fun-Controlnet-Union — MiniMax H3 Fun ControlNet Union"
category: projects
date: 2026-08-24
tags: [minimax-h3-fun-controlnet-union, minimax_h3_fun_controlnet_union, project]
aliases: ["MiniMax-H3-Fun-Controlnet-Union"]
level: 2
source_sha256: bc6807995cdf199098a2bd4934e92e1c4e63c1ab23b428291635c1d6c9c7cabd
translation: machine
translated_at: '2026-10-24'
---
# MiniMax-H3-Fun-Controlnet-Union — MiniMax H3 Fun ControlNet Union {#minimax-h3-fun-controlnet-union-minimax-h3-fun-controlnet-union}

**Entwicklungslinie:** `project:minimax-h3-fun-controlnet-union` · Thread `minimax-h3-fun-controlnet-union`  
**Letztes Ereignis:** 2026-08-24 · 1 datiertes Ereignis seit 2026-08-24 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

MiniMax-H3-Fun-Controlnet-Union ist ein Control-Adapter für den Basis-Videogenerator MiniMax-H3, entwickelt für Nutzer von VideoX-Fun.

- Einheitlicher Checkpoint für Conditioning mit Canny, Depth, HED, MLSD und Pose.
- Video-zu-Video-Pipeline, um die Generierung über ein Control-Video zu steuern.
- Video-Inpainting-Pipeline zum Bearbeiten maskierter Bereiche.

Die Control-Gewichte sind nicht eigenständig lauffähig; Basis-Transformer und Qwen3-VL benötigen zusammen mehr als 80 GB VRAM. Verwenden Sie es, wenn die Bewegungsstruktur wichtiger ist als reine Text-zu-Video-Generierung und Offload verfügbar ist.

## Entwicklungslinie {#development-line}

- **2026-08-24 — MiniMax H3 Fun ControlNet Union mit einem VideoX-Fun-Beispiel verknüpft.** Am 2026-08-24 verknüpfte ein Projekt-Update das Hugging-Face-Repository MiniMax-H3-Fun-Controlnet-Union mit einem Beispielverzeichnis von VideoX-Fun für MiniMax H3 Fun. Die Verknüpfung verbindet die Modellgewichte mit einem Implementierungsbeispiel. Setup-Details und Funktionsumfang der Veröffentlichung wurden nicht unabhängig verifiziert.

## Was sich geändert hat {#what-changed}

2026-08-24 — VideoX-Fun hat das Verzeichnis `examples/minimax_h3_fun` hinzugefügt, und ControlNet-Union für MiniMax-H3 ist als eigenständiges Control-Modell verfügbar geworden. 2026-08-27 — ComfyUI hat das Laden des Checkpoints, das Conditioning für Video und Inpainting sowie die Anwendung des Control-Streams vorbereitet, PR #15860 ist jedoch weiterhin offen.

## So wird es verwendet {#how-to-use-this}

Bewerten Sie das MiniMax-H3-Fun-Beispiel von VideoX-Fun zusammen mit MiniMax-H3-Fun-Controlnet-Union ab 2026-08-24; genaues Setup und Funktionsumfang bleiben unverifiziert.

1. Klonen Sie VideoX-Fun und erstellen Sie `models/Diffusion_Transformer`. Legen Sie das MiniMax-H3-Basismodell und `MiniMax-H3-Fun-Controlnet-Union.safetensors` in getrennte Verzeichnisse, wie in der Model Card angegeben.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
2. Setzen Sie in `examples/minimax_h3_fun/predict_v2v_control.py` das Basismodell, `minimax_h3_control.yaml`, den Pfad zu den Control-Gewichten, das Control-Video und den Prompt und führen Sie anschließend das Skript aus.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
3. Für die Bearbeitung mit Masken führen Sie `predict_v2v_control_inpaint.py` anstelle des Standard-Skripts für Control-Videos aus.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
4. Aktivieren Sie auf einer einzelnen 80-GB-GPU `model_group_offload` oder `model_cpu_offload_and_qfloat8`; erwarten Sie nicht, dass Basis-Transformer und Qwen3-VL zusammen in den Speicher passen.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>

## Best Practices {#best-practices}

- Belassen Sie `guidance_scale = 1.0`. Der Checkpoint ist guidance-destilliert, daher wendet ein höherer Wert die Guidance erneut an und verschlechtert die Ausgabe.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Halten Sie die Struktur des Control-Netzwerks unverändert. Die Konfiguration muss `control_blocks_places: [0, 10, 20, 30, 40]`, `control_in_dim: 49` und deaktivierte Audio-Steuerung beibehalten, da die Gewichte sonst nicht geladen werden.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Beginnen Sie mit `control_context_scale = 1.0`. Senken Sie den Wert nur, um das Folgen des Control-Videos abzuschwächen; `0.0` deaktiviert das Conditioning durch die Steuerung vollständig.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Prüfen Sie die MiniMax H3 Community License vor Weitergabe oder gehosteter Nutzung. Sie schließt EU, UK, die Republik Korea und die USA aus dem Applicable Territory aus und legt Sonderbedingungen für Umsätze von mehr als 20 Mio. USD pro Jahr fest.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- `event_findings` und `new_events` wurden als Objekterweiterungen hinzugefügt, weil die Aufgabe sie verlangt, das System-JSON-Schema sie jedoch nicht enthält.
- Die öffentliche Veröffentlichung des Hugging-Face-Repositorys vor 2026-08-24 ist nicht bestätigt; die Commit-Seite zeigt eine relative Zeitangabe statt eines ISO-Zeitstempels.
- PR #15860 in ComfyUI ist weiterhin offen; die Bestätigung der Unterstützung in einer Veröffentlichung erfordert einen Merge upstream oder einen Nachweis über ein Release.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/aigc-apps/VideoX-Fun/tree/main/examples/minimax_h3_fun | VideoX-Fun — examples/minimax_h3_fun | 2026-09-05 |
| https://github.com/aigc-apps/VideoX-Fun/commits/main/examples/minimax_h3_fun | VideoX-Fun — Verlauf für examples/minimax_h3_fun | 2026-09-05 |
| https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union | Model Card alibaba-pai/MiniMax-H3-Fun-Controlnet-Union | 2026-09-05 |
| https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0 | Update Weights — MiniMax-H3-Fun-Controlnet-Union | 2026-09-05 |
| https://github.com/Comfy-Org/ComfyUI/pull/15860 | ComfyUI PR #15860 — Support MiniMax-H3 fun controlnet | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:minimax-h3-fun-controlnet-union`, Thread `minimax-h3-fun-controlnet-union`, 1 datiertes Ereignis vom 2026-08-24 bis 2026-08-24.
- **Praktischer Hinweis:** Bewerten Sie das MiniMax-H3-Fun-Beispiel von VideoX-Fun zusammen mit dem Artefakt MiniMax-H3-Fun-Controlnet-Union ab 2026-08-24; genaues Setup und Funktionsumfang bleiben unverifiziert.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
