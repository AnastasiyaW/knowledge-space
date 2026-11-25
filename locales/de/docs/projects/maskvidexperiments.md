---
title: "MaskVidExperiments"
category: projects
date: 2026-08-23
tags: [maskvid-experiments, maskvidexperiments, project]
aliases: ["MaskVidExperiments"]
level: 2
source_sha256: 90af374ab2b5a258acf9af83234c1d538798068b8b2e736365350a1e14dc3ac9
translation: machine
translated_at: '2026-10-24'
---
# MaskVidExperiments {#maskvidexperiments}

**Entwicklungslinie:** `project:maskvidexperiments` · Thread `maskvid-experiments`  
**Letztes Ereignis:** 2026-08-23 · 1 datiertes Ereignis seit 2026-08-23 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

MaskVidExperiments ist eine Sammlung von ComfyUI-Knoten für alle, die bereits eine framegenaue Objektmaske haben und das Objekt in einem Video inpainten oder stilisieren müssen, ohne einen flackernden Crop zu erhalten. — Subject Crop/Uncrop erstellt einen stabilen Crop für den gesamten Clip und fügt das bearbeitete Objekt mit Randverblendung wieder ein. — Mask Cleanup bereinigt kurze verrauschte Bereiche der Maske; Mask To Latent Space überführt die Videomaske in die Geometrie des VAE; es gibt separate Knoten für Audio-Latent und weiches Differential Diffusion. Einschränkung: angegeben sind ComfyUI >=0.15.0 und GPLv3; es handelt sich weder um einen Segmentierer noch um ein Videomodell. Fazit: einsetzen für die lokale maskenbasierte Bearbeitung bereits annotierter Videos, nicht als Ersatz für Masken, Modelle oder einen erprobten Production-Workflow.

## Entwicklungslinie {#development-line}

- **2026-08-23 — Das GitHub-Repository von MaskVidExperiments wurde öffentlich referenziert.** Der datierte Link verweist auf das bereits bestehende Projekt v0.2.0; im gesichteten main-Verlauf gibt es an diesem Datum keinen Commit.

## Was sich geändert hat {#what-changed}

2026-07-28: Der Initial-Commit wurde als Erstveröffentlichung markiert. 2026-07-29: MVEx Differential Diffusion (Soft) wurde hinzugefügt, für weiche Maskenkanten über die Denoising-Schritte. 2026-08-04: Masken werden nun anhand der exakten Grenzen der VAE-Latents gruppiert; ein Knoten wurde hinzugefügt, der die latente Maske zurück auf Pixel-Frames überträgt. 2026-08-08: Die Zuordnung zum Zyklus der VAE-Chunks und die GPU-Reduktion mit CPU-Fallback haben die Maskenübertragung näher an die Geometrie des Videomodells gebracht. 2026-08-10: Frame Range Mask sowie die Knoten Audio Mask To Latent/Debug wurden hinzugefügt. 2026-08-13: crop_scale=0 wurde zum Full-Frame-Passthrough-Modus für den Vergleich mit der Crop-Pipeline. 2026-08-14: Die Mindestversion ComfyUI 0.15.0 wurde festgeschrieben und die automatische Veröffentlichung in der Registry bei einem Version Bump ergänzt. 2026-08-15: Latente Masken werden an dem 2x2-Token-Raster von MiniMax H3 ausgerichtet. 2026-08-17: Die Projektmetadaten wurden von 0.1.0 auf 0.2.0 angehoben; ein negativer Wert für upscale_megapixels ermöglicht nun Downscaling. 2026-08-23: Der datierte Link verweist auf das bereits bestehende Projekt v0.2.0; im gesichteten main-Verlauf gibt es an diesem Datum keinen Commit.

## Wie man es verwendet {#how-to-use-this}

Ab dem 2026-08-23 können Praktiker das verlinkte MaskVidExperiments-GitHub-Repository als datierte Projektquelle nutzen. Inhalte und Versionsstand sollten jedoch als ungeprüft gelten, bis sie separat verifiziert sind.

1. Klonen Sie das Repository in ComfyUI/custom_nodes und starten Sie ComfyUI neu; die Dokumentation nennt als Mindestversion v0.15.0 und keine Abhängigkeiten über ComfyUI hinaus.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
2. Führen Sie die Frames und die fertige Maske bei kurzem Rauschen zuerst durch Mask Cleanup und dann durch Subject Crop. Leiten Sie den Crop durch Ihren Sampler bzw. Inpaint-Workflow und geben Sie ihn über Subject Uncrop zusammen mit den ursprünglichen Frames, Bboxes und Crop-Masken zurück.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
3. Für eine Videomaske verbinden Sie Mask To Latent Space mit dem VAE, belassen compression=auto, sofern der VAE angeschlossen ist, und übergeben das Ergebnis an Set Latent Noise Mask. Verwenden Sie manual nur, wenn die Geometrie des VAE bekannt ist.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>

## Bewährte Vorgehensweisen {#best-practices}

- Für minimale Bewegung des Crops wählen Sie tracked; combined eignet sich für ein einziges, unbewegtes Fenster, zoomed dann, wenn der Anteil des Objekts konstant bleiben soll. Prüfen Sie das Debug-Ergebnis; eine pixelgenaue Einfügung bleibt nur ohne Größenänderung des Crops erhalten.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
- Übergeben Sie die pixelbasierte Videomaske nicht direkt an Set Latent Noise Mask. Verwenden Sie Mask To Latent Space, damit die Maske zwischen den Frames nicht durch trilineares Resize verwischt wird.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
- Setzen Sie crop_scale=0, um die Crop-Pipeline vor einer Entscheidung für einen konkreten Clip mit dem Vollbild zu vergleichen, indem Sie zwei Bypässe nutzen.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>

## Durch Folgendes ersetzt {#superseded-by-this}

- 2026-08-17: Die Projektmetadaten 0.1.0 wurden durch 0.2.0 ersetzt (Commit d98cc89).

## Noch unbekannt {#still-unknown}

- Eine gezielte Suche nach Simplified Chinese ergab keine zugängliche Primär- oder Implementierungsquelle; die chinesische Nachweislinie bleibt unbelegt.
- Der Upstream veröffentlicht keinen Benchmark zu VRAM, Geschwindigkeit, langen Clips oder zeitlicher Stabilität; der Graph wurde nicht in einer eigenen Umgebung ausgeführt.
- Die Mindestversion ComfyUI 0.15.0 und die Unterstützung der genannten VAE-Geometrien sind in der Dokumentation bestätigt, es fehlt jedoch eine vollständige Matrix getesteter Versionen von ComfyUI, Videomodellen und Hardware.
- Vor einem Produktiveinsatz sind ein fixierter Commit sowie eine gesonderte Prüfung der Lizenzkompatibilität mit der GPLv3 erforderlich.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/drozbay/MaskVidExperiments | MaskVidExperiments — GitHub-Repository | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md | MaskVidExperiments README bei Commit d98cc89 | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/commits/main | MaskVidExperiments main-Commit-Verlauf | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/commit/d98cc899c1fac718acf81cde1735bf57281097cf | Bump version to 0.2.0 — Commit d98cc89 | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/pyproject.toml | Projektmetadaten bei Commit d98cc89 | 2026-09-06 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:maskvidexperiments`, Thread `maskvid-experiments`, 1 datiertes Ereignis 2026-08-23 → 2026-08-23.
- **Praktischer Hinweis:** Ab dem 2026-08-23 können Praktiker das verlinkte MaskVidExperiments-GitHub-Repository als datierte Projektquelle nutzen. Inhalte und Versionsstand sollten jedoch als ungeprüft gelten, bis sie separat verifiziert sind.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, sind die datierten Angaben unter „Durch Folgendes ersetzt“ maßgeblich.
