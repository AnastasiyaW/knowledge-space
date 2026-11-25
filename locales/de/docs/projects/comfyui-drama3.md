---
title: "ComfyUI"
category: "projects"
date: 2026-10-17
tags: ["comfy-cloud-pricing", "comfyui", "comfyui-development", "comfyui-drama3", "comfyui_core_updates", "comfyui_desktop", "ecosystem_grants", "product_updates", "project"]
aliases: ["Comfy Cloud", "ComfyUI"]
level: 3
source_sha256: aa2db946caa6556f70f30ed68983e247ea0ddcda403f4dde9eda6f2dc2a91cf3
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI {#comfyui}

**Entwicklungsstrang:** project:comfyui-drama3 · thread comfyui-development  
**Letztes Ereignis:** 2026-10-17 · 20 datierte Ereignisse seit 2023-11-24 · **Recherchiert:** 2026-10-19 · Konfidenz: hoch

## Was es ist {#what-it-is}

ComfyUI-Drama3 ist eine Custom-Node-Erweiterung für ComfyUI. Sie führt Fish Audios Drama 3 lokal auf Consumer-GPUs aus, ein Text-to-Speech- und Voice-Cloning-Modell mit 35 Milliarden Parametern.

- Zero-Shot-Voice-Cloning aus sauberen Sprachaufnahmen.
- Mehrsprecher-Dialoge mit bis zu 16 unterscheidbaren Stimmen in einem einzigen Skript.
- Emotionale Vortragsweise, gesteuert über Tags in eckigen Klammern.
- Spracherkennung über lokale Begleit-Aligner-Nodes.

Inaktive MoE-Routing-Experten werden in den Systemspeicher ausgelagert, aktive Experten bleiben im GPU-Cache. Es werden mindestens 8 GB VRAM benötigt.

## Entwicklungsstrang {#development-line}

- **2023-11-24 — Stable-Video-Diffusion-Workflows.** ComfyUI veröffentlichte erste offizielle Beispiel-Workflows für Stable Video Diffusion zur Bild-zu-Video-Generierung. Sie dokumentierten die Platzierung der Modelle sowie die Steuerung von Framezahl, Bewegung, Framerate und Classifier-Free Guidance.
- **2024-06-12 — SD3 im Core.** Commit 8c4a9be fügte dem Core-Engine-Support für SD3 hinzu. SD3-Workflows konnten nun nativ aufgebaut werden.
- **2024-09-16 — SD3- und Flux-Inpainting-ControlNet.** Commit f48e390 fügte Unterstützung für AliMama-ControlNet-Modelle für SD3- und Flux-Inpainting hinzu. Damit wurde strukturell konditioniertes Inpainting für beide Modellfamilien erweitert.
- **2024-10-21 — V1-Oberfläche und Desktop-Beta.** ComfyUI führte die V1-Oberfläche ein und öffnete das Desktop-Paketformat für eine geschlossene Beta. V1 brachte einen mitgelieferten Manager, Tabs, Einstellungen, Browser für Modelle und Workflows sowie Hilfe beim Herunterladen von Modellen. Die ursprüngliche Oberfläche wechselte in einen Wartungspfad.
- **2024-12-06 — Kompromittierung des Ultralytics-Pakets.** Schadhafte Ultralytics-Pakete in den Versionen 8.3.41 und 8.3.42 tauchten über einige Abhängigkeitsketten von Custom Nodes auf. ComfyUI dokumentierte seine Reaktion und trennte die kompromittierte Abhängigkeit vom ComfyUI-Core. Der Manager erhielt Warnungen und Versions-Pinning.
- **2025-07-28 — Wan 2.2 am ersten Tag.** Die native Unterstützung war vom ersten Tag an verfügbar. Sie kam mit offiziellen Text-to-Video- und Image-to-Video-Workflows mit Mixture-of-Experts-Architektur sowie gebündelten Modelldateien.
- **2025-08-13 — Wan 2.2 Fun InP, Control und LightX2V.** Die Workflows ermöglichten Generierung über das erste und letzte Frame, strukturelle Steuerungen sowie schnellere Vierschritt-Generierung mit LoRA-Beschleunigung.
- **2025-08-26 — Qwen-Image DiffSynth ControlNet.** Die native Unterstützung erweiterte die steuerbare Bildgenerierung. Optionale cachebasierte Beschleunigung von Workflows wurde dokumentiert.
- **2025-08-27 — Gehostetes Gemini und lokale Qwen-Image-Steuerung.** Zwei getrennte Wege wurden hinzugefügt. Google Gemini 2.5 Flash Image läuft über kreditpflichtige Partner Nodes. InstantX-Qwen-Image-Unified-ControlNet-Workflows laufen lokal mit Canny-, Depth-, Pose- und Soft-Edge-Steuerungen.
- **2025-08-28 — Zweite Comfy Challenge.** Das Community-Showcase- und Workflow-Lernprogramm wuchs mit der zweiten Comfy Challenge. Dies war ein Meilenstein für Ökosystem und Bildung, keine Core-Runtime-Veröffentlichung.
- **2025-09-24 — Wan 2.2 Animate und Qwen-Bildbearbeitung.** Native Workflows für Wan 2.2 Animate und Qwen-Image-Edit-2509 wurden hinzugefügt. Sie decken performancegesteuerte Charakteranimation und -ersetzung sowie Bearbeitung mit mehreren Bildern ab.
- **2025-10-07 — ComfyUI 0.3.63: veröffentlichbare Subgraphs.** Subgraphs konnten als wiederverwendbare Blueprint-Nodes veröffentlicht werden. Die Auswahlwerkzeuge für die Graphbearbeitung wurden neu gestaltet.
- **2025-10-09 — Sora 2 Partner Nodes.** Sora 2 und Sora 2 Pro wurden über kostenpflichtige Partner Nodes verfügbar. Sie unterstützen Text-to-Video und Image-to-Video mit Ton.
- **2025-10-22 — ComfyUI 0.3.66: Werkzeuge für Subgraphs und Templates.** Subgraphs erhielten ein Parameter-Panel. Die Erkennung und Filterung von Workflow-Templates wurde neu gestaltet.
- **2025-11-26 — Comfy-Cloud-Infrastruktur und Kontingente.** Comfy Cloud kündigte den Umzug auf RTX-6000-Pro-Infrastruktur und die Unterstützung persönlicher LoRAs an. Außerdem beschrieb es längere Pro-Läufe und vereinheitlichte Credits für die Cloud-GPU-Ausführung und Partner Nodes.
- **2025-12-30 — Repository wechselt zu Comfy-Org.** Das kanonische GitHub-Repository wurde von comfyanonymous/ComfyUI nach Comfy-Org/ComfyUI verschoben. GitHub-Weiterleitungen blieben erhalten, und Nutzer wurden aufgefordert, ihre Git-Remotes zu aktualisieren.
- **2026-01-27 — Z-Image am ersten Tag.** ComfyUI fügte Unterstützung für das nicht destillierte Z-Image-Modell hinzu. Es wurde mit einem offiziellen Workflow und modellspezifischen Hinweisen zum Sampling ausgeliefert.
- **2026-02-05 — Förderinitiative für offene Modelle.** Zusammen mit dem Anima-Launch kündigte das ComfyUI-Ökosystem eine Förderinitiative mit einem Programm von 1 Million US-Dollar an. Sie wurde als Finanzierung für die Entwicklung offener Modelle dargestellt.
- **2026-03-26 — Stabiles Dynamic VRAM.** ComfyUI dokumentierte Dynamic VRAM als stabil. Es verringert den Speicherdruck und Out-of-Memory-Fehler auf unterstützten Nvidia-Systemen. Die Empfehlung lautet, die gesamte Workflow-Laufzeit zu messen, nicht isolierte Iterationsgeschwindigkeiten.
- **2026-10-17 — ComfyUI-Drama3-Nodes mehr als 3x schneller.** Ein Nutzerbericht besagte, dass die aktualisierten ComfyUI-Drama3-Nodes mindestens 3x schneller laufen und mit 8 GB VRAM funktionieren. Der Bericht verlinkt auf das GitHub-Repository des Projekts.
  - Das Update optimiert das Expert-Caching zwischen Host-RAM und GPU für die 35B-Parameter-Drama-3-MoE-Architektur von Fish Audio. Die Generierung ist 3x bis 4x schneller, und Consumer-GPUs mit 8 GB VRAM funktionieren weiterhin. (2026-10-17) — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Was sich geändert hat {#what-changed}

Das Projekt begann als Adaption der Drama-3-Architektur und wurde zu einem optimierten ComfyUI-Custom-Node-Paket. Es hält Experten im RAM, damit das 35B-Mixture-of-Experts-Modell auf Consumer-Hardware läuft. Spätere Kernel-Optimierungen und Verbesserungen des Cachings senkten die Inferenzlatenz auf 8-GB-Systemen um mehr als das Dreifache.

## So wird es verwendet {#how-to-use-this}

1. Das Repository in das Verzeichnis `custom_nodes` von ComfyUI klonen.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
2. Die Drama-3-Modellgewichte in `models/diffusion_models` und die Codec-Gewichte in `models/vae` ablegen.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
3. Den Voice-Clone- oder Text-to-Speech-Beispiel-Workflow laden. Referenzaudio für das Sprecher-Cloning anhängen, Emotions-Tags hinzufügen und in die Warteschlange stellen.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Best Practices {#best-practices}

- Auf 8-GB-Karten die gerouteten Experten in den Systemspeicher auslagern und den GPU-VRAM für den Cache aktiver Experten freihalten.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
- Kurze, saubere Referenzsprache ohne Hintergrundgeräusche verwenden, damit die geklonte Stimme originalgetreu bleibt.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
- Eckige Hinweise wie `[whispers]` oder `[laughs]` hinzufügen, um die Tonlage in Mehrsprecher-Dialogskripten zu steuern.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Was Praktiker berichten {#what-practitioners-say}

- Praktiker berichten nach dem Node-Update von einer deutlichen Beschleunigung um das 3- bis 4-Fache. Dadurch wird lokale Inferenz mit einem 35B-Modell auf 8-GB-Karten praktikabel. (2026-10-17)
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8dj76/comfyuidrama3_is_34x_faster_now/>

## Hierdurch abgelöst {#superseded-by-this}

- Frühere Node-Versionen liefen auf GPUs mit 8 GB VRAM deutlich langsamer, weil die Übertragungen der Experten vom RAM in den VRAM nicht optimiert waren.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Weiterhin unbekannt {#still-unknown}

- Commit-Daten vor der Optimierungsveröffentlichung vom 2026-10-17 waren in öffentlichen Suchzusammenfassungen nicht unabhängig datiert.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/PedroMarinhoDev/ComfyUI-Drama3 | PedroMarinhoDev/ComfyUI-Drama3: ComfyUI custom nodes for Drama 3 | 2026-10-19 |
| https://www.reddit.com/r/StableDiffusion/comments/1x8dj76/comfyuidrama3_is_34x_faster_now/ | ComfyUI-Drama3 is 3-4x faster now : r/StableDiffusion | 2026-10-19 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** project:comfyui-drama3, Thread comfyui-development, 20 datierte Ereignisse 2023-11-24 → 2026-10-17.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** hoch. Datierte Ablösungen sind maßgeblich dafür, was veraltet ist.
