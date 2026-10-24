---
title: "WAN"
category: projects
date: 2026-07-31
tags: [project, wan, wan-video-generation]
aliases: ["WAN", "Wan", "Wan2.2 dyno"]
level: 2
source_sha256: 163affe162b36def00c920958f44219a2721b201bf53e3863d1cb126bc0de624
translation: machine
translated_at: '2026-10-24'
---
# WAN {#wan}

**Entwicklungslinie:** `project:wan` · Thread `wan-video-generation`  
**Letztes Ereignis:** 2026-07-31 · 3 datierte seit 2025-09-23 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

WAN ist eine Familie von Videogenerierungsmodellen für Kreative und Entwickler: Text-zu-Video, Bild-zu-Video, sprach- und referenzgesteuerte Videos, Charakteranimation und Charakterersetzung. Wan2.2 bleibt eine lokal betreibbare Modellreihe unter Apache-2.0, während aktuelle gehostete APIs neuere Modelle der Versionen 2.6 und 2.7 bereitstellen. Die lokale Inferenz des A14B-Modells benötigt im offiziellen Beispiel mindestens 80 GB VRAM. Fazit: Für die Produktionsgenerierung gehostetes, aktuelles WAN verwenden; Wan2.2 einsetzen, wenn lokale, prüfbare Gewichte und Community-Beschleunigung wichtig sind.

## Entwicklungslinie {#development-line}

- **2025-09-23 — Alibaba Wan 2.5 erschien auf WaveSpeed als Text-zu-Video-Modell.** Am 2025-09-23 wies eine WaveSpeed-Modellroute Alibaba Wan 2.5 als Text-zu-Video-Angebot aus. Dies ist ein wesentlicher Schritt bei der Verfügbarkeit im Ökosystem, da Praktiker damit einen benannten gehosteten Zugang zu dieser WAN-Version für die Videogenerierung erhielten.
- **2025-10-01 — Assets zu Wan 2.2 Lightning erschienen für Vier-Schritt-Workflows im Text-zu-Video-Bereich.** Am 2025-10-01 wiesen die verlinkten Ressourcen eine Vier-Schritt-Dyno-Variante von Wan 2.2 Lightning, ein entsprechendes FP8-ComfyUI-Artefakt und eine Workflow-Seite aus. Dies ist ein wesentlicher praktischer Schritt, da er auf einen schnelleren, sofort einsetzbaren Inferenzpfad für die Text-zu-Video-Generierung mit Wan 2.2 hinweist.
- **2026-07-31 — WAN stellte eine Realtime-Playground-Route bereit.** Am 2026-07-31 enthielt die WAN-Create-Seite eine als Realtime bezeichnete Lab-Playground-Route. Dies ist ein wesentlicher Schritt in der Schnittstellenentwicklung, da er auf einen interaktiven Realtime-Einstiegspunkt für WAN hinweist, der sich von einem Modell-Download- oder Batch-Workflow-Link unterscheidet.

## Was sich geändert hat {#what-changed}

2025-09-23 — Wan 2.5 erschien als gehostete Text-/Bild-zu-Video-API mit synchronisiertem Audio, Ausgabe von 480p bis 1080p und Jobs von 5 oder 10 Sekunden. 2025-10-01 — der Community-Pfad Wan2.2-Lightning ergänzte ein benanntes 4-Schritt-Dyno-Checkpoint-Verzeichnis für die Basis Wan2.2 T2V-A14B; das Repository führt das Verzeichnis mit 28,6 GB auf, und das zugehörige ComfyUI-FP8-Asset benennt die genaue T2V-Modellfamilie. 2026-07-31 — eine WAN-Realtime-Playground-Route war verfügbar, die zugängliche Seite nennt jedoch weder Modellnamen, Latenz, Preise noch einen öffentlichen Nutzungsvertrag. 2026-08-04 — eine Canary-Version derselben Realtime-Route war verfügbar; auch ihre zugängliche Seite enthält keine Angaben zur Veröffentlichung, weshalb sie kein Beleg für ein eigenständiges öffentliches Modell ist. 2025-07-28 — nachgetragener früherer Schritt: Wan2.2 veröffentlichte Code und Gewichte und erhielt eine Integration in ComfyUI und Diffusers. 2025-09-19 — nachgetragener früherer Schritt: Wan2.2-Animate-14B ergänzte Charakteranimation und Charakterersetzung. 2026-09-02 — die aktuelle gehostete Dokumentation führt Video-APIs von Wan 2.6 und 2.7 auf; Wan2.7 unterstützt Varianten für Text-zu-Video und Bild-zu-Video mit 720p/1080p, 2 bis 15 Sekunden und 30 fps.

## So wird es genutzt {#how-to-use-this}

Ab 2025-10-01 konnten Praktiker Wan 2.2 über den verlinkten Vier-Schritt-Workflow Lightning/ComfyUI evaluieren, wenn es auf Videoinferenz mit wenigen Schritten ankam; ab 2026-07-31 sollten sie zusätzlich den öffentlichen WAN-Realtime-Playground getrennt von Batch-Workflows prüfen. Den Canary-Endpunkt vom 2026-08-04 sollte man als nicht verifizierte Deployment-Infrastruktur behandeln, nicht als öffentliche Änderung der Fähigkeiten.

1. Für einen aktuellen gehosteten Text-zu-Video-Job einen Prompt an die WAN-API senden, eine unterstützte Größe und Dauer wählen, die zurückgegebene Task-ID aufbewahren und dann abfragen (Polling), statt doppelte Aufträge erneut einzureichen.
  — <https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference>
2. Für lokales Wan2.2 das offizielle Repository klonen, die Abhängigkeiten installieren, den passenden Checkpoint herunterladen und anschließend `generate.py` mit der gewünschten Aufgabe und Auflösung ausführen.
  — <https://github.com/Wan-Video/Wan2.2>
3. Für beschleunigte lokale Experimente mit Wan2.2 T2V die Basis-Checkpoints A14B und die LightX2V-Assets herunterladen und dann das Verzeichnis des Lightning-LoRA an den offiziellen Generierungsbefehl übergeben.
  — <https://huggingface.co/lightx2v/Wan2.2-Lightning>

## Best Practices {#best-practices}

- Für Reproduzierbarkeit einen Seed festlegen, einen fixierten Seed aber nicht als Garantie für identische Videoausgaben behandeln.
  — <https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference>
- Modellversion, Auflösung, Dauer, Audio und Region als explizite Job-Parameter behandeln; sie beeinflussen Verfügbarkeit, Kosten und Ausgabelimits.
  — <https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference>
- Einen lokalen Wan2.2-Workflow nur mit dafür dimensionierter Hardware einsetzen; das offizielle Beispiel für A14B auf einer einzelnen GPU mit 720p nennt mindestens 80 GB VRAM.
  — <https://github.com/Wan-Video/Wan2.2>
- Beschleunigung im Lightning-Stil als Community-Erweiterung des passenden Basismodells einsetzen, nicht als Ersatz für den Basis-Checkpoint.
  — <https://huggingface.co/lightx2v/Wan2.2-Lightning>

## Abgelöst durch diesen Stand {#superseded-by-this}

- 2025-09-23: Wan 2.5 weiterhin als aktuellen WAN-Endpunkt zu behandeln ist veraltet; die aktuelle Alibaba-Dokumentation führt die Videomodellfamilien Wan 2.6 und Wan 2.7 auf.
- 2025-10-01: das Dyno-Asset Wan2.2 mit 4 Schritten als Standardpfad für WAN zu behandeln ist für gehostete Produktion veraltet; es bleibt eine lokale Inferenzoption aus der Community.
- 2026-07-31 und 2026-08-04: eine der beiden Realtime-Playground-URLs als dokumentierte Produktspezifikation zu behandeln ist nicht belegt; keine der zugänglichen Routen legte einen öffentlichen Vertrag offen.

## Weiterhin unbekannt {#still-unknown}

- Die zugänglichen Seiten für Realtime und den Canary-Realtime-Zugang waren reine Hüllseiten ohne auslesbare Angaben zu Modell, Veröffentlichungsdatum, Latenz, Kontingent oder Preisen; ihre Ereignisse vom 2026-07-31 und 2026-08-04 lassen sich daher über die Verfügbarkeit der Route hinaus nicht näher beschreiben.
- Das datierte Ereignis zu WAN 2.5 stützt sich hier auf einen Drittanbieter der API und nicht auf eine zugängliche Ankündigung des Herstellers; der genaue ursprüngliche Veröffentlichungsumfang ist nicht verifiziert.
- WAN umfasst zwei betrieblich unterschiedliche Gegenstände: offene lokale Wan2.2-Gewichte und spätere gehostete APIs von Wan 2.5 bis 2.7. Sie teilen einen Namen, sollten aber nicht als austauschbare Deployment-Ziele behandelt werden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference | Wan - text-to-video API reference | 2026-09-05 |
| https://www.alibabacloud.com/help/tc/model-studio/video-generate-edit-model/ | Video generation and editing model list | 2026-09-05 |
| https://github.com/Wan-Video/Wan2.2 | Wan2.2 — official repository | 2026-09-05 |
| https://huggingface.co/lightx2v/Wan2.2-Lightning | lightx2v/Wan2.2-Lightning | 2026-09-05 |
| https://huggingface.co/lightx2v/Wan2.2-Lightning/tree/main/Wan2.2-T2V-A14B-4steps-250928-dyno | Wan2.2 Lightning Dyno 4-step directory | 2026-09-05 |
| https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/blob/main/T2V/Wan2_2-T2V-A14B-HIGH_4_steps-250928-dyno-lightx2v_fp8_e4m3fn_scaled_KJ.safetensors | Kijai Wan2.2 T2V-A14B Dyno 4-step FP8 asset | 2026-09-05 |
| https://wavespeed.ai/models/alibaba/wan-2.5/text-to-video | Wan 2.5 Text-to-Video API on WaveSpeed | 2026-09-05 |
| https://create.wan.video/lab/playground/realtime | Wan Realtime playground | 2026-09-05 |
| https://canary-create.wan.video/lab/playground/realtime | Wan Realtime playground canary route | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:wan`, Thread `wan-video-generation`, 3 datierte Ereignisse vom 2025-09-23 bis 2026-07-31.
- **Praxishinweis:** Ab 2025-10-01 konnten Praktiker Wan 2.2 über den verlinkten Vier-Schritt-Workflow Lightning/ComfyUI evaluieren, wenn es auf Videoinferenz mit wenigen Schritten ankam; ab 2026-07-31 sollten sie zusätzlich den öffentlichen WAN-Realtime-Playground getrennt von Batch-Workflows prüfen. Den Canary-Endpunkt vom 2026-08-04 sollte man als nicht verifizierte Deployment-Infrastruktur behandeln, nicht als öffentliche Änderung der Fähigkeiten.
- **Konfidenz:** mittel. Die datierten Ablösungshinweise oben sind maßgeblich für das, was veraltet ist.
