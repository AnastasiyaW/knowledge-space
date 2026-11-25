---
title: "Bernini — Modellverfügbarkeit und ComfyUI-Integration"
category: projects
date: 2026-06-02
tags: [bernini, model-availability-and-comfyui-integration, project]
aliases: ["Bernini"]
level: 3
source_sha256: 1ed0848b9c92977960fb95673a0608abbbd7d260b2dcc4c611f44a7025245401
translation: machine
translated_at: '2026-10-24'
---
# Bernini — Modellverfügbarkeit und ComfyUI-Integration {#bernini-model-availability-and-comfyui-integration}

**Entwicklungsstrang:** `project:bernini` · Thread `model-availability-and-comfyui-integration`  
**Letztes Ereignis:** 2026-06-02 · 1 datiertes seit 2026-06-02 · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

Bernini ist ein Framework von ByteDance zur Videogenerierung und -bearbeitung für Praktiker, die eine lokale Alternative zu einem Workflow mit reinem Wan-Renderer benötigen.

- Vollständiges Bernini / v2: Qwen2.5-VL-7B für die semantische Planung plus ein Wan2.2-T2V-A14B-Renderer für t2i, i2i, t2v, v2v, rv2v und r2v.
- Bernini-R: die Wan-Linie mit reinem Renderer für einfachere Inferenz und die gepflegten ComfyUI-Templates.

Die offizielle Referenzumgebung ist H100, CUDA 12.6 und Python 3.11.2. Die Video-Skripte verwenden standardmäßig acht Prozesse sowie 480p, 16 fps, 81 Frames. Verwende das vollständige v2 für komplexe mehrstufige Bearbeitungen; Bernini-R nur dann, wenn sein enger gefasster Renderer-Umfang oder der ComfyUI-Pfad das Ziel ist.

## Entwicklungsstrang {#development-line}

- **2026-06-02 — Modell- und ComfyUI-Workflow-Ressourcen für Bernini verlinkt.** Am 2026-06-02 verlinkte ein datierter Bernini-Eintrag die Projektwebsite und das Modell-Repository ByteDance/Bernini auf Hugging Face. Außerdem verlinkte er eine JSON-Datei mit einem Bernini-Testworkflow sowie ein Bernini-Verzeichnis im Repository WanVideo Comfy FP8 scaled von Kijai. Zusammen markieren diese Ressourcen einen Schritt in Richtung Modellzugang und ComfyUI-Nutzung.

## Was sich geändert hat {#what-changed}

- 2026-05-22 — Das Bernini-Paper stellte die Architektur aus semantischem Planer und DiT-Renderer vor.
- 2026-06-01 — Code und Gewichte von Bernini-R wurden als Linie mit reinem Renderer veröffentlicht.
- 2026-06-02 — Anleitung zum Laden im Diffusers-Format, nur über die Konfiguration, kam mit dem ersten Renderer-Release hinzu.
- 2026-06-09 — Bernini-R erhielt eine auf Wan2.1 basierende Variante mit 1,3 Mrd. Parametern für einfachere Bearbeitungen.
- 2026-06-11 — Vollständiger Bernini-Inferenzcode und vollständige Gewichte ergänzten den Qwen-Planer um den Wan-Renderer.
- 2026-06-12 — R2V erhielt SA3D-RoPE-Interpolation für mehr als fünf Referenzbilder.
- 2026-06-13 — Das frühe Kijai-ComfyUI-Konvertierungsverzeichnis wurde gelöscht.
- 2026-07-13 — Der Trainingscode für Bernini-R wurde veröffentlicht.
- 2026-08-13 — Bernini-Diffusers-v2 erschien mit einem vorab aufgewärmten Planer-Connector und überarbeiteten, vom Anbieter berichteten Ergebnissen zur Referenzbearbeitung.

## Anwendung {#how-to-use-this}

1. Wähle zuerst das Artefakt. Verwende für semantische Planung und komplexe Bearbeitungen das vollständige `Bernini-Diffusers-v2`; `Bernini-R-Diffusers` nur für Arbeiten mit reinem Renderer.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini.md>
2. Klone das offizielle Repository und installiere seine fixierten Abhängigkeiten. Installiere das benötigte Paket VeOmni ohne Abhängigkeiten, damit es das fixierte PyTorch-Build nicht ersetzt.
  — <https://github.com/bytedance/Bernini>
3. Lade `ByteDance/Bernini-Diffusers-v2` herunter, übergib dieses Verzeichnis über `--config` und beginne mit einem mitgelieferten Bildbeispiel, bevor du zu Video- oder referenzgeführten Fällen übergehst.
  — <https://huggingface.co/ByteDance/Bernini-Diffusers-v2>
4. Verwende die gepflegten Task-Skripte und Fall-JSONs für t2i, i2i, t2v, v2v, rv2v oder r2v. Die Skripte der vollständigen Pipeline enthalten die aufgabenspezifischen Sampling-Standardwerte.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini.md>
5. Für ComfyUI verwende den gepflegten Bernini-R-Video-Workflow und das Comfy-Org-Bernini-R-Repack. Es handelt sich um einen Weg mit reinem Renderer, nicht um einen Beleg für Unterstützung von vollständigem v2.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_video_editing.json>

## Bewährte Praktiken {#best-practices}

- Bevorzuge das eigenständige Diffusers-Verzeichnis mit `--config`. Verwende separate Flags für Checkpoints mit hohem und niedrigem Rauschanteil nur bewusst, wenn du das ältere Layout nutzt.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini_r.md>
- Belasse die fixierte PyTorch/CUDA-Umgebung des Repositorys unverändert, wenn du VeOmni hinzufügst, indem du VeOmni mit `--no-deps` installierst.
  — <https://github.com/bytedance/Bernini>
- Starte mit den mitgelieferten Skripten und Fall-Dateien, statt Sampling-Einstellungen selbst zu erfinden. Der Video-Standard ist 480p, 16 fps und 81 Frames.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini.md>
- Verwende im ComfyUI-Template Turbo nur für die Iteration am Prompt, deaktiviere es für die finale Ausgabe und benenne sowohl bei der Bearbeitung die beabsichtigte Änderung als auch die Elemente, die unverändert bleiben müssen.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_image_editing.json>

## Abgelöst durch diesen Stand {#superseded-by-this}

- 2026-06-11 — Bernini insgesamt als reine Renderer-Veröffentlichung vom Juni zu behandeln, ist veraltet. Das vollständige Bernini fügte einen MLLM-Planer für die semantische Planung hinzu.
- 2026-06-13 — Der Download-Pfad Kijai `WanVideo_comfy_fp8_scaled/tree/main/Bernini` ist veraltet. Seine Historie verzeichnet die Löschung dieses Verzeichnisses.
- 2026-08-13 — Der ursprüngliche vollständige Checkpoint `Bernini-Diffusers` ist für referenzgeführte Arbeiten nicht mehr die alleinige aktuelle Empfehlung für die vollständige Pipeline. v2 beschreibt ein geändertes Trainingsrezept für den Connector, keine Garantie für Kompatibilität.

## Weiterhin unbekannt {#still-unknown}

- Wir konnten die ursprüngliche Adresse `https://huggingface.co/ByteDance/Bernini` nicht abrufen; ihr Verhältnis zu den aktuellen Bernini-R-Repositories ist daher nicht belegt.
- Wir konnten den mitgelieferten GitHub-Workflow-Anhang nicht abrufen. Sein Knotengraph, die genauen Modelldateien und das Laufzeitergebnis bleiben ungeprüft.
- Das direkte Kijai-Bernini-Verzeichnis liefert jetzt 404. Seine Historie belegt die frühe FP8-Konvertierung für hohen und niedrigen Rauschanteil sowie die Löschung, aber nicht die aktuelle Kompatibilität oder Prüfsummen.
- Wir fanden keine erstrangige Ankündigung eines datierten v2-Launches. Ein gleichtägiges Repository-Update und ein datierter Sekundärbericht bestätigen das Datum 2026-08-13; die offizielle Model Card bestätigt den Inhalt von v2, kündigt dieses Datum aber nicht an.
- Das untersuchte ComfyUI-Material enthält gepflegte Bernini-R-Templates, während die Unterstützung von vollständigem v2 noch eine offene Anfrage war. Das schließt ungeprüfte Community-Workflows für v2 nicht aus.
- Wir fanden keinen unabhängigen, aktuellen Leistungslauf für genau die v2-Umgebung. Vom Anbieter veröffentlichte Benchmark-Zahlen sind keine Garantie für den Betrieb.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://bernini-ai.github.io/ | Bernini: Latent Semantic Planning für Video-Diffusion | 2026-09-07 |
| https://github.com/bytedance/Bernini | GitHub - bytedance/Bernini | 2026-09-07 |
| https://github.com/bytedance/Bernini/blob/main/docs/bernini.md | Bernini — vollständige Pipeline | 2026-09-07 |
| https://github.com/bytedance/Bernini/blob/main/docs/bernini_r.md | Bernini-R — nur Renderer | 2026-09-07 |
| https://github.com/bytedance/Bernini/blob/main/docs/bernini_r_train.md | Bernini-R-Trainingsleitfaden | 2026-09-07 |
| https://github.com/bytedance/Bernini/commits/main | Commits · bytedance/Bernini | 2026-09-07 |
| https://huggingface.co/ByteDance/Bernini-Diffusers-v2 | ByteDance/Bernini-Diffusers-v2 · Hugging Face | 2026-09-07 |
| https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/commits/main/Bernini | Commits · Kijai/WanVideo_comfy_fp8_scaled — Bernini | 2026-09-07 |
| https://huggingface.co/Comfy-Org/Bernini-R | Comfy-Org/Bernini-R · Hugging Face | 2026-09-07 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_video_editing.json | Comfy-Org Bernini-R-Template für Video-Bearbeitung | 2026-09-07 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_image_editing.json | Comfy-Org Bernini-R-Template für Bild-Bearbeitung | 2026-09-07 |
| https://github.com/Comfy-Org/ComfyUI/issues/15702 | Consider support for ByteDance Bernini-Diffusers-v2 · Issue #15702 | 2026-09-07 |
| https://www.orcarouter.ai/blog/bernini-diffusers-v2-shipped-quietly | Bernini-Diffusers-v2: ByteDances stille Checkpoint-Veröffentlichung | 2026-09-07 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:bernini`, Thread `model-availability-and-comfyui-integration`, 1 datiertes Ereignis 2026-06-02 → 2026-06-02.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Anwendung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ablösungen sind maßgeblich dafür, was veraltet ist.
