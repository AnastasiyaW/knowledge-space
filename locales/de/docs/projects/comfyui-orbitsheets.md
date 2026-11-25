---
title: "OrbitSheets"
category: projects
date: 2026-08-17
tags: [comfyui-orbitsheets, lumosai8/comfyui-orbitsheets, project]
aliases: ["OrbitSheets"]
level: 2
source_sha256: 3649fa7ee73590bc60ce8d8e6442c9b4b5d2e5d42030c3cb4cd7092c7e671e6b
translation: machine
translated_at: '2026-10-24'
---
# OrbitSheets {#orbitsheets}

**Entwicklungslinie:** `project:comfyui-orbitsheets` · Thread `comfyui-orbitsheets`  
**Letztes Ereignis:** 2026-08-17 · 1 datiertes seit 2026-08-17 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

OrbitSheets ist ein ComfyUI-Node-Pack für Charakter-Turnarounds und Location-Sheets. Es erzeugt diese aus einem einzigen MiniMax-H3-Videotake statt aus separaten Bildprompts.

- Cut-Shot-Prompts: erstellt Promptsequenzen für Charakter- und Location-Ansichten.
- Frame-Auswahl: wählt scharfe, unterschiedliche Frames aus und baut ein Contact Sheet.
- Frame-Bewertung: bewertet Frames über In-Graph-CLIP, einen OpenAI-kompatiblen Vision-Endpunkt oder einen Fallback auf Schärfe/Diversität.
- Audio-Referenz: extrahiert eine Stimmspur des Charakters aus dem Take.

Version 0.1.0 benötigt Python >=3.10 und `requests`. Sie setzt MiniMax-H3-Assets voraus und ist keine H3-Implementierung. Verwenden Sie es als Workflow-Helfer, wenn H3 bereits läuft, nicht als eigenständiges Modell oder als veröffentlichtes Plugin.

## Entwicklungslinie {#development-line}

- **2026-08-17 — OrbitSheets-GitHub-Repository im Entwicklungs-Thread verlinkt.** Die sichtbare Entwicklungsabfolge endet beim Commit vom 2026-08-14, und GitHub hat kein Release.

## Was sich geändert hat {#what-changed}

2026-08-13 — Vier Commits fügten das MiniMax-H3-Charakter- und Location-Pack hinzu, aktualisierten die Beispiel-Workflows und ergänzten einen In-Graph-Attention-Node.  
2026-08-14 — Commit 8952eae stellte den Standard-Location-Workflow auf Cut-Views um und ergänzte eine Turn-Rate-Begrenzung. Kontinuierliche Bewegung wurde zur Option.  
2026-08-17 — An diesem Datum erschien keine neue Version. Die sichtbaren Commits enden am 2026-08-14, und GitHub hat kein Release.

## Verwendung {#how-to-use-this}

Am 2026-08-17 ist das verlinkte GitHub-Repository die datierte Quelle für OrbitSheets. Prüfen Sie Dateien direkt, bevor Sie sich auf eine Funktionsaussage verlassen.

1. Klonen Sie das Repository nach `ComfyUI/custom_nodes` und starten Sie ComfyUI neu. Die Nodes erscheinen in der Kategorie `OrbitSheets`.
2. Legen Sie das MiniMax-H3-Diffusionsmodell, den Qwen3-VL-32B-H3-Text-Encoder und das H3-Video-VAE in die ComfyUI-Modellordner. Das H3-Audio-VAE nur hinzufügen, wenn Sie die Stimmspur benötigen. Wählen Sie ein beliebiges Anker-Modell; die Beispiele verwenden Krea2.
3. Ziehen Sie für manuelle Läufe einen Graph aus `example_workflows/` per Drag & Drop auf die Oberfläche oder reichen Sie den passenden Graph aus `api_workflows/` ein. Der Pfad lautet: Anker-Bild → `MiniMaxH3ImageToVideo` → dekodierte Frames/Audio → Frame Select → Contact Sheet.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>
4. Prüfen Sie nach jedem Lauf die Ausgabe `info` von Frame Select. Sie zeigt, ob die Auswahl per In-Graph-CLIP, einem HTTP-Vision-Modell oder dem deterministischen Fallback erfolgte.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>

## Best Practices {#best-practices}

- Behalten Sie `coverage=cut views` für Location-Sheets bei. Wechseln Sie nur dann zu `continuous move`, wenn Schnitte nicht gesehene Teile erfinden würden, und halten Sie die Rotation unter dem Limit von 40°/s.
- Setzen Sie `shots` auf Ihre Zielanzahl an Ansichten. Setzen Sie `count` gleich diesem Wert, wenn Sie pro Ansicht genau ein Bild behalten wollen. Bevorzugen Sie `shot_split=views (by content)`. Wiederholen Sie den H3-Take oder senken Sie `shots`, wenn `info` weniger unterschiedliche Ansichten meldet.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>
- Verwenden Sie `full body, generous margin` für Flügel, Schwänze und Requisiten. Geben Sie dem Anker denselben Randabstand, damit die Zuschnittgrenzen das Turnaround nicht beschneiden.
- Lassen Sie `free_vram_first` vor der Vision-Bewertung aktiviert. Testen Sie Renderings, bevor Sie das verlustbehaftete Attention-Backend `comfy kitchen (int8)` verwenden.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>
- Fixieren Sie den Commit in gemeinsam genutzten Workflows, weil die GitHub-Releases-Seite kein Release enthält.
  — <https://github.com/lumosai8/ComfyUI-OrbitSheets/releases>

## Abgelöst durch {#superseded-by-this}

- 2026-08-14 — Kontinuierliche Orbit-Führung für Location-Sheets ist veraltet. `coverage=cut views` ist nun der Standard. Kontinuierliche Bewegung bleibt nur dort, wo Schnitte nicht gesehene Seiten erfinden würden.
- 2026-08-14 — Unbegrenzte Drehungen in kurzen Takes sind veraltet. Das Projekt begrenzt Drehungen über 40°/s und dokumentiert etwa neun Sekunden für eine 360-Grad-Drehung.

## Weiterhin unbekannt {#still-unknown}

- Die README widerspricht dem Code bei den Charakter-Shots. Einige Abschnitte nennen fünf Shots oder acht Frames. Der aktuelle Node-Code und der Charakter-Graph wählen sechs Ansichten, einschließlich des optionalen verängstigten Gesichts, aus einem Take mit 124 Frames.
- README und Paketmetadaten nennen keine getestete ComfyUI-Core-Version, keine H3-Paketrevision und keine Kompatibilitätsmatrix.
- Die Upstream-Tests prüfen Selector- und Prompt-Code ohne GPU. Hier wurde kein Live-Render mit MiniMax H3 verifiziert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/lumosai8/ComfyUI-OrbitSheets | GitHub — lumosai8/ComfyUI-OrbitSheets | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/commits/main | Commits — lumosai8/ComfyUI-OrbitSheets | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/commit/8952eae1d3298f241c538c029a6e929509c4813f | Location-Sheet als Schnitte statt Kamerafahrt durchs Set — Commit 8952eae | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/blob/main/pyproject.toml | ComfyUI-OrbitSheets pyproject.toml | 2026-09-05 |
| https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py | ComfyUI-OrbitSheets nodes.py | 2026-09-05 |
| https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/example_workflows/CharacterTurnaroundSheetH3.json | Mitgelieferter CharacterTurnaroundSheetH3-Canvas-Workflow | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/releases | Releases — lumosai8/ComfyUI-OrbitSheets | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:comfyui-orbitsheets`, Thread `comfyui-orbitsheets`, 1 datiertes Ereignis 2026-08-17 → 2026-08-17.
- **Praktischer Hinweis:** Stand 2026-08-17 können Praktiker das verlinkte GitHub-Repository als datierten Quellort für OrbitSheets nutzen. Die Inhalte sollten jedoch geprüft werden, bevor man sich auf Installations- oder Funktionsaussagen verlässt.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
