---
title: "InstantX SD3 ControlNet — SD3-ControlNet-Checkpoint-Veröffentlichungen"
category: projects
date: 2024-06-17
tags: [instantx-sd3-controlnet, project, sd3-controlnet-checkpoint-releases]
aliases: ["InstantX SD3 ControlNet"]
level: 3
source_sha256: ffeeda56aab1973756571ad11fad481fc0997b57677386332bf02ed7bc22607b
translation: machine
translated_at: '2026-10-24'
---
# InstantX SD3 ControlNet — SD3-ControlNet-Checkpoint-Veröffentlichungen {#instantx-sd3-controlnet-sd3-controlnet-checkpoint-releases}

**Entwicklungslinie:** `project:instantx-sd3-controlnet` · Thread `sd3-controlnet-checkpoint-releases`  
**Letztes Ereignis:** 2024-06-17 · 2 datierte Einträge seit 2024-06-15 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

InstantX SD3 ControlNet stellt Control-Image-Adapter für Praktiker bereit, die Stable Diffusion 3 an strukturellen Eingaben ausrichten müssen:
- Canny: folgt Kantenkonturen.
- Pose: folgt menschlichen Posen.
- Tile: folgt Kachel- und Bildvorgaben.
- Depth: folgt Tiefenkarten.

Canny und Pose sind 0.6B-F16-Checkpoints, deren Model Cards angeben, dass das Training ausschließlich mit 1024×1024 erfolgte. Wir setzen sie ein, wenn das gegatete SD3 Medium und ein quadratischer 1024-Workflow passen. Die Kompatibilität mit der neueren SD3-Familie ist hier nicht belegt.

## Entwicklungslinie {#development-line}

- **2024-06-15 — InstantX-SD3-ControlNet-Canny-Repositories erschienen auf Hugging Face.** Am 2024-06-15 verwiesen Hugging-Face-Links, die mit InstantX SD3 ControlNet verbunden sind, auf ein Canny_alpha_512-Repository und ein Canny-Repository. Damit standen in dieser Entwicklungslinie Canny-konditionierte SD3-ControlNet-Artefakte zur Verfügung.
- **2024-06-17 — InstantX-SD3-ControlNet-Pose-Repository erschien auf Hugging Face.** Am 2024-06-17 verwies ein Hugging-Face-Link, der mit InstantX SD3 ControlNet verbunden ist, auf das SD3-Controlnet-Pose-Repository. Dadurch kam ein posenkonditioniertes Artefakt zur dokumentierten Entwicklungslinie hinzu.

## Was sich geändert hat {#what-changed}

- 2024-06-15 — Canny wurde initialisiert und erhielt seine Konfiguration und seinen Checkpoint; der separate `Canny_alpha_512`-Endpunkt ist heute weiterhin nicht verifiziert.
- 2024-06-17 — Dokumentation und Assets von Pose änderten sich, während Tile seinen Checkpoint erhielt; der ursprüngliche Pose-Checkpoint war bereits am 15. Juni erschienen.
- 2024-06-19 — Die Installation von Canny wechselte vom InstantX-Fork `sd3_control` zu `diffusers >= 0.30.0.dev0`.
- 2024-06-23 — SD3-Controlnet-Depth wurde angelegt und erhielt seinen Checkpoint.
- 2025-04-24 — Der Klassenname der Canny-Konfiguration wurde korrigiert, sodass das direkte Laden über `AutoModel.from_pretrained` funktioniert.

## Anwendung {#how-to-use-this}

Ab 2024-06-15 konnten Praktiker InstantX-SD3-ControlNet-Canny-Artefakte für kantengeführte Workflows untersuchen. Ab 2024-06-17 konnten sie zusätzlich das posenkonditionierte Artefakt für posengeführte Workflows untersuchen. Vor dem Einsatz Kompatibilität, Lizenz, Revision und Workflow-Anforderungen prüfen.

1. Die Zugriffsfreigabe für Stable Diffusion 3 Medium akzeptieren und sich vor dem Herunterladen des Basismodells bei Hugging Face authentifizieren.
  — <https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3>
2. `InstantX/SD3-Controlnet-Canny` als `SD3ControlNetModel` laden, es mit `stabilityai/stable-diffusion-3-medium-diffusers` an `StableDiffusion3ControlNetPipeline` anbinden und auf CUDA in FP16 ausführen.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Canny>
3. Für Pose-Steuerung `InstantX/SD3-Controlnet-Pose` ersetzen und ein Pose-Control-Image bereitstellen. Canny und Pose verwenden unterschiedliche passende Control-Eingaben.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Pose>
4. Einen Prompt und `control_image` übergeben. Für mehrere Controls eine Liste von SD3-ControlNets laden und pro Control ein passendes Bild übergeben.
  — <https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sd3>
5. Auf begrenzten GPUs zuerst FP16 und Model CPU Offload nutzen, bevor die Qualitätseinstellungen reduziert werden. Die drei Text-Encoder von SD3 sind selbst in FP16 unterhalb von 24 GB VRAM eine Herausforderung.
  — <https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3>

## Best Practices {#best-practices}

- Canny oder Pose mit 1024×1024 beginnen. Die Model Cards weisen darauf hin, dass andere Auflösungen suboptimal sein können, da das Training ausschließlich mit 1024×1024 erfolgte.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Canny>
- Mit dem `controlnet_conditioning_scale=0.5` der Autoren-Demo beginnen. Für jedes Control-Image gezielt nachjustieren, statt einen Wert als universell zu behandeln.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Pose>
- Für eine bekannt kompatible Konfiguration die dokumentierte SD3-Medium-Basis verwenden. Nicht davon ausgehen, dass diese Checkpoints unverändert mit einer anderen SD3-Familien-Basis funktionieren.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Canny>
- Ein chinesischer ComfyUI-Praxisbericht von Juni 2024 empfahl niedrige Gewichte, ein frühes Control-Ende und die Behandlung der Ergebnisse als Startbild. Dies ist als historische Workflow-Beobachtung zu verstehen, nicht als aktueller allgemeingültiger Bereich.
  — <https://www.youtube.com/watch?v=5SdRiZ53WPM>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- 2024-06-19 — Der alte Installationspfad, der `instantX-research/diffusers_sd3_control` am Stand `sd3_control` klonte, wurde durch die Diffusers-Anforderung ersetzt. Quelle: https://huggingface.co/InstantX/SD3-Controlnet-Canny/commit/a59221661ea027c11d813cbc595133ca8e56adb5
- 2025-04-24 — Canny-Konfigurationen vor der Korrektur des Klassennamens unterstützen das direkte Laden über `AutoModel.from_pretrained` nicht. Quelle: https://huggingface.co/InstantX/SD3-Controlnet-Canny/discussions/12

## Weiterhin unbekannt {#still-unknown}

- https://huggingface.co/InstantX/SD3-Controlnet-Canny_alpha_512 konnte in dieser Recherchesitzung nicht abgerufen werden. Seine genauen Gewichte, Auflösung und Beziehung zu Canny sind nicht verifiziert.
- Das abgerufene Depth-Update vom 2024-07-03 wird nur als Upload von zwei Dateien beschrieben, nicht als benanntes Release, daher ist sein funktionaler Umfang unbekannt.
- Für diese Canny-, Pose-, Tile- und Depth-Checkpoints wurde keine offizielle, aktuelle Kompatibilitätsmatrix für SD3.5, aktuelle ComfyUI-Versionen oder den VRAM-Bedarf moderner Consumer-GPUs gefunden.
- Aus den abgerufenen Model Cards von Canny, Pose oder Tile wurde keine explizite Lizenz verifiziert. Ihre Bedingungen nicht aus dem auf Depth sichtbaren Apache-2.0-Label ableiten.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/InstantX/SD3-Controlnet-Canny | InstantX/SD3-Controlnet-Canny | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Pose | InstantX/SD3-Controlnet-Pose | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Pose/tree/main | Dateien von InstantX/SD3-Controlnet-Pose | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Canny/commits/e42ecba9741dee3de8c54039eba8a879c0070ced | Commit-Verlauf — InstantX/SD3-Controlnet-Canny | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Pose/commits/main | Commit-Verlauf — InstantX/SD3-Controlnet-Pose | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Tile/commits/main | Commit-Verlauf — InstantX/SD3-Controlnet-Tile | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Depth/commits/main | Commit-Verlauf — InstantX/SD3-Controlnet-Depth | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Canny/commit/a59221661ea027c11d813cbc595133ca8e56adb5 | Canny-README-Update, 19. Juni 2024 | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Canny/discussions/12 | Korrektur des Klassennamens der Canny-Konfiguration | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sd3 | ControlNet with Stable Diffusion 3 — Diffusers | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3 | Stable Diffusion 3 — Diffusers | 2026-09-04 |
| https://www.youtube.com/watch?v=5SdRiZ53WPM | 在ComfyUI中使用新发布的SD3 ControlNet模型，对比SD1.5及SDXL同款，能控制但不够稳定 | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:instantx-sd3-controlnet`, Thread `sd3-controlnet-checkpoint-releases`, 2 datierte Ereignisse vom 2024-06-15 bis 2024-06-17.
- **Praktischer Hinweis:** Praktiker konnten InstantX-SD3-ControlNet-Canny-Artefakte für kantengeführte Workflows ab dem 2024-06-15 untersuchen. Ab dem 2024-06-17 konnten sie zusätzlich das posenkonditionierte Artefakt für posengeführte Workflows untersuchen. Vor dem Einsatz Kompatibilität, Lizenz, Revision und Workflow-Anforderungen prüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Ablösungsangaben als maßgeblich.
