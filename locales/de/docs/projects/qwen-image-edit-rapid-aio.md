---
title: "Qwen-Image-Edit-Rapid-AIO"
category: projects
date: 2025-12-29
tags: [project, qwen-image-edit-rapid-aio, qwen_image_edit_rapid_aio]
aliases: ["Qwen-Image-Edit-Rapid-AIO"]
level: 3
source_sha256: b71545247048c73c4a3ede919ac1027699acc89425fab3eddbd76029fe13ddf3
translation: machine
translated_at: '2026-10-24'
---
# Qwen-Image-Edit-Rapid-AIO {#qwen-image-edit-rapid-aio}

**Entwicklungslinie:** `project:qwen-image-edit-rapid-aio` · Thread `qwen-image-edit-rapid-aio`  
**Letztes Ereignis:** 2025-12-29 · 2 datierte seit 2025-10-07 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Qwen-Image-Edit-Rapid-AIO vereint Geschwindigkeitsbeschleuniger, VAE und CLIP für Qwen-Image-Edit in einem Checkpoint für ComfyUI-Nutzer.

- Text-zu-Bild ohne Eingabebild
- Textgesteuerte Bildbearbeitung mit mehreren Eingabebildern
- SFW- und NSFW-Varianten

Der Workflow läuft in 4 Schritten bei CFG 1; v18 wiegt 28,4 GB pro Variante.

Es eignet sich für schnelle lokale Bearbeitung und Text-zu-Bild, aber dies ist kein offizielles Qwen-Release, und der Autor wird keine neuen Versionen veröffentlichen.

## Entwicklungslinie {#development-line}

- **2025-10-07 — Öffentlicher Repository-Verweis für Qwen-Image-Edit-Rapid-AIO.** Die ursprüngliche v1 kombinierte Qwen-Image-Edit-2509 und Lightning v2.0 mit 4 Schritten.
- **2025-12-29 — Ressourcen und Workflow-Verweise zu v18 für Qwen-Image-Edit-Rapid-AIO.** Am 2025-12-29 verzeichnete das Repository Links zu seinem v18-Verzeichnis, einem Qwen-Rapid-AIO-JSON-Workflow und einer zugehörigen GGUF-Distribution. Diese datierten Links bestätigen eine spätere Distribution und einen Workflow-Verweis, belegen aber nicht die genauen Änderungen, Kompatibilität oder Leistung von v18.

## Was sich geändert hat {#what-changed}

- 2025-10-07: Der frühe Rapid-AIO-Checkpoint erschien; die ursprüngliche v1 kombinierte Qwen-Image-Edit-2509 und Lightning v2.0 mit 4 Schritten.
- 2025-12-29: v18 wurde in getrennte SFW- und NSFW-Varianten aufgeteilt; der GGUF-Spiegel ergänzte SFW-Quantisierungen Q4_K und Q5_K.
- 2026-01-08: v19 veröffentlicht.
- 2026-01-24: v23 veröffentlicht. Der Autor erklärte später, dass v19 eine bessere Konsistenz bei der Bearbeitung bietet und v23 komplexen Prompts besser folgt, und stellte danach weitere Updates ein.

## So verwenden Sie es {#how-to-use-this}

Stand 2025-12-29: Beginnen Sie die Evaluierung mit den Ressourcen des v18-Repositorys und dem JSON-Workflow, und prüfen Sie die Quellen, bevor Sie sich auf Angaben zur GGUF-Verfügbarkeit, Kompatibilität oder Qualität verlassen.

1. Laden Sie den gewählten Rapid-AIO-Checkpoint herunter und legen Sie ihn im ComfyUI-Checkpoints-Ordner ab.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO>
2. Importieren Sie den mitgelieferten JSON-Workflow; er verwendet CheckpointLoaderSimple, TextEncodeQwenImageEditPlus, KSampler und VAE Decode.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
3. Verbinden Sie ein oder zwei Quellbilder mit den optionalen Bild-Eingängen oder lassen Sie sie für Text-zu-Bild leer; setzen Sie den Prompt in TextEncodeQwenImageEditPlus.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
4. Führen Sie mit 4 Schritten, CFG 1, Sampler sa_solver und Scheduler beta aus dem Workflow aus.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
5. Für einen kleineren Download verwenden Sie die passende GGUF-Variante und einen kompatiblen GGUF-Loader anstelle des Standard-Checkpoint-Loaders.
  — <https://huggingface.co/Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF/tree/main>

## Best Practices {#best-practices}

- Beginnen Sie mit dem mitgelieferten Workflow und seinen Einstellungen von 4 Schritten/CFG 1; kopieren Sie die Standardparameter von Qwen-Image-Edit nicht blind.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
- Beschreiben Sie bei Bearbeitungen die konkrete Änderung und übergeben Sie die Quelle an den Bild-Eingang; bei Text-zu-Bild lassen Sie den Bild-Eingang leer.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
- Verkleinern Sie große Eingaben zuerst, falls Probleme auftreten: Der offizielle Qwen-Image-Edit-Workflow skaliert die Eingabe auf etwa eine Million Pixel herunter, um Qualitätsverlust bei übergroßen Bildern zu vermeiden.
  — <https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit>
- Wählen Sie für konsistente Bearbeitungen v19 statt v23; v23 ist nützlich, wenn das Befolgen komplexer Anweisungen wichtiger ist.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO>

## Abgelöst durch dieses {#superseded-by-this}

- 2025-12-29: v18 SFW GGUF Q4_K/Q5_K erweiterte die früheren NSFW-Quantisierungen von v18.
- 2026-01-24: v23 war die letzte veröffentlichte Version, ersetzt aber nicht v19, wenn die Konsistenz der Bearbeitung wichtiger ist.

## Weiterhin unbekannt {#still-unknown}

- Rapid-AIO ist ein Community-Checkpoint und kein offizielles Qwen-Image-Edit-Release; die Fähigkeiten des Basismodells können nicht für jede Rapid-AIO-Zusammenführung vorausgesetzt werden.
- Das Repository-Log für das Ereignis vom 2025-10-07 enthält nicht das ursprüngliche Commit-Datum der ersten v1-Version; die Model Card bestätigt die Beschreibung von v1, das historische Datum bleibt aber das Ereignisdatum.
- Die Hugging-Face-URL für GGUF leitet von Arunk25 auf Novice25 weiter; dies sieht nach einer Kontoumbenennung oder Übertragung aus, der Grund ist jedoch nicht bestätigt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO | Model Card von Phr00t/Qwen-Image-Edit-Rapid-AIO | 2026-09-05 |
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/commits/main | Commit-Verlauf von Phr00t/Qwen-Image-Edit-Rapid-AIO | 2026-09-05 |
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/tree/main/v18 | Dateien von Phr00t/Qwen-Image-Edit-Rapid-AIO v18 | 2026-09-05 |
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json | Qwen-Rapid-AIO ComfyUI-Workflow | 2026-09-05 |
| https://huggingface.co/Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF/tree/main | Dateien von Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF | 2026-09-05 |
| https://huggingface.co/Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF/commits/main/v18 | Commit-Verlauf von Novice25 Qwen-Image-Edit-Rapid-AIO-GGUF v18 | 2026-09-05 |
| https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit | Qwen-Image-Edit ComfyUI Native Workflow Example | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:qwen-image-edit-rapid-aio`, Thread `qwen-image-edit-rapid-aio`, 2 datierte Ereignisse 2025-10-07 → 2025-12-29.
- **Praktischer Hinweis:** Stand 2025-12-29 zuerst die Ressourcen des v18-Repositorys und den JSON-Workflow auswerten und die Quellen prüfen, bevor Angaben zu GGUF-Verfügbarkeit, Kompatibilität oder Qualität vertraut wird.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben bestimmen, was veraltet ist.
