---
title: "ComfyUI Video Tiler"
category: projects
date: 2026-08-05
tags: [comfyui-video-tiler, comfyui_video_tiler, project]
aliases: ["ComfyUI Video Tiler"]
level: 2
source_sha256: 978bf7298dd26378230e24bc64f18d5035c285f9eceadc31a1dd9fde823d4e79
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Video Tiler {#comfyui-video-tiler}

**Entwicklungslinie:** `project:comfyui-video-tiler` · Thread `comfyui-video-tiler`  
**Letztes Ereignis:** 2026-08-05 · 1 datiertes seit 2026-08-05 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

ComfyUI Video Tiler zerlegt einen IMAGE-Videobatch in überlappende Kacheln, verarbeitet sie über einen Upscale-Workflow und führt sie ohne sichtbares Raster wieder zusammen. Das Paket richtet sich an LTX-2.3- und MiniMax-H3-Workflows.

- Variable und feste Slicer zerlegen die Frames.
- Feathered Merge überblendet die Kachelnähte, sodass kein sichtbares Raster entsteht.
- Festplattengestützte Kachel-Jobs sparen Speicher über mehrere Läufe hinweg.
- Referenzausrichtung und Farbabgleich sichern die Konsistenz über alle Kacheln.
- Audioerkennung und Sampler-Timing verfolgen das Tempo des Clips.

Der Festplattenmodus reduziert den Speicherbedarf für zwischengespeicherte Kacheln, das fertig zusammengeführte IMAGE benötigt aber weiterhin RAM oder VRAM. Verwenden Sie ihn für einen gekachelten Upscale-Workflow, der mit dem Zielmodell bereits erprobt ist, nicht als allgemeine Videopipeline.

## Entwicklungslinie {#development-line}

- **2026-08-05 — Auf das ComfyUI-Video-Tiler-Repository wurde verwiesen.** Am 2026-08-05 verwies der erfasste Link auf das GitHub-Repository von ComfyUI Video Tiler. Dieser Eintrag belegt die öffentliche Projektreferenz, aber weder ein Release, eine Version, einen Funktionsumfang noch Installationshinweise.

## Was sich geändert hat {#what-changed}

- **2026-08-05** — Das Paket wurde in der Comfy Registry registriert und erhielt Beispiel-Workflows für LTX 2.3 und MiniMax H3, festplattengepufferte Workflows sowie Sampler-Timing-Nodes. Die Repository-Historie weist an diesem Tag sieben Commits aus, darunter die Registrierung in der Registry, `disk buffered workflows`, beide modellspezifischen Beispiele und `timer nodes added`.
- **2026-08-07** — Die Beispiel-Workflows wurden aktualisiert.
- **2026-08-08** — Der Festplatten-Merge wurde entkoppelt und eine Kachelvorschau hinzugefügt. Damit steht nach der Kachelverarbeitung ein unabhängiger, ordnerbasierter Zusammenbau- und Prüfpfad zur Verfügung.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-08-05 behandeln wir das verlinkte GitHub-Repository als bestätigte Projektreferenz. Prüfen Sie vor der Verwendung die aktuelle Dokumentation und Kompatibilität.

1. Installieren Sie in `ComfyUI/custom_nodes` mit `git clone https://github.com/maDcaDDie2000/comfyui-video-tiler`, und starten Sie ComfyUI anschließend neu. Normale Nodes erscheinen unter Video Tiler, Disk-Nodes unter Video Tiler/Disk.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
2. Für einen Clip, der in den Speicher passt, verbinden Sie einen der Slicer mit dem Upscale-Workflow und führen die verarbeitete Kachelliste zusammen mit dem unveränderten `tile_config` dem Video Tile Merge zu.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
3. Für die Verarbeitung mit wenig VRAM erstellen Sie einen Disk Job, verarbeiten und speichern jede indizierte Kachel und verwenden anschließend Disk Folder Merge mit dem fertigen Job-Ordner oder Manifest. Die IMAGE- und Audio-Ausgaben leiten Sie an einen Video-Encoder weiter.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>

## Best Practices {#best-practices}

- Halten Sie `tile_config` mit dem Slicer gepaart, der es erzeugt hat. Verwenden Sie Überlappung und Feathering, um harte Nähte zu vermeiden.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
- Verwenden Sie die festplattengestützte Verarbeitung, wenn verarbeitete Kacheln nicht im Cache bleiben können. Planen Sie dann aber Speicher für das abschließende IMAGE in voller Größe ein.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
- Verwenden Sie die mitgelieferten LTX-2.3- oder MiniMax-H3-Workflows als Ausgangspunkt. Andere Modell-Stacks liegen außerhalb des primär getesteten Umfangs des Pakets.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-08-05 — Festplattengepufferte Kachel-Workflows ersetzen die reine In-Memory-Anleitung für eingeschränkte Hardware.
- 2026-08-08 — Unabhängiger ordnerbasierter Merge und Vorschau ersetzen dort, wo sinnvoll, das reine Festplatten-Merging im verbundenen Graphen.

## Weiterhin unbekannt {#still-unknown}

- Das Repository veröffentlicht in den geprüften Quellen keine formalen Release-Tags. Die Änderungen vom August 2026 werden daher anhand des Commit-Datums identifiziert und nicht anhand einer versionierten Veröffentlichung.
- Das Ausgabeschema enthält keine eigenen Felder für Ereignisbefunde und neue Ereignisse. `what_changed` erfasst deren erforderlichen Inhalt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/maDcaDDie2000/comfyui-video-tiler | ComfyUI-Video-Tiler-Repository und README | 2026-09-05 |
| https://github.com/maDcaDDie2000/comfyui-video-tiler/commits/main | ComfyUI-Video-Tiler-Commit-Historie | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:comfyui-video-tiler`, Thread `comfyui-video-tiler`, 1 datiertes Ereignis 2026-08-05 → 2026-08-05.
- **Praktischer Hinweis:** Stand 2026-08-05 können Praktiker das verlinkte GitHub-Repository als bestätigte Projektreferenz behandeln. Vor der Verwendung sollten sie jedoch dessen aktuelle Dokumentation und Kompatibilität prüfen.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
