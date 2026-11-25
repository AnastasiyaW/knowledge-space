---
title: "ComfyUI"
category: projects
date: 2026-09-03
tags: [comfy-cloud-pricing, comfyui, comfyui-development, comfyui_core_updates, comfyui_desktop, ecosystem_grants, product_updates, project]
aliases: ["Comfy Cloud", "ComfyUI"]
level: 2
source_sha256: b489a482ac639686aadbd2921c05392c6f891742de39856722272b02691e88db
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI {#comfyui}

**Entwicklungslinie:** `project:comfyui` · Thread `comfyui-development`  
**Letztes Ereignis:** 2026-09-03 · 21 datierte Einträge seit 2023-11-24 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ComfyUI-H3VAE_TRT ist eine Drittanbieter-Erweiterung für ComfyUI von lihaoyun6. Sie kompiliert MiniMax-H3-VAE-ONNX-Modelle zu TensorRT-Engines und lädt diese als VAE. Dabei handelt es sich um eine Custom-Node-Integration, nicht um eine Veröffentlichung des MiniMax-H3-Modells oder um ein Core-Update von ComfyUI.

## Entwicklungslinie {#development-line}

- **2023-11-24 — ComfyUI veröffentlicht Stable-Video-Diffusion-Workflows.** Am 2023-11-24 veröffentlichte ComfyUI erste offizielle Beispiel-Workflows für Stable Video Diffusion zur Bild-zu-Video-Generierung. Die Beispiele dokumentierten die Platzierung der Modelle sowie Steuerungsmöglichkeiten für Frame-Anzahl, Bewegung, Framerate und Classifier-Free Guidance.
- **2024-06-12 — ComfyUI Core ergänzt SD3-Unterstützung.** Am 2024-06-12 fügte ComfyUI seiner Core-Engine per Commit 8c4a9be SD3-Unterstützung hinzu. Die Änderung schuf die native Engine-Unterstützung für den Aufbau von SD3-Workflows.
- **2024-09-16 — ComfyUI ergänzt Inpainting-ControlNet-Unterstützung für SD3 und Flux.** Am 2024-09-16 fügte ComfyUI per Commit f48e390 Unterstützung für AliMama-ControlNet-Modelle für SD3- und Flux-Inpainting hinzu. Die Änderung erweiterte strukturell konditioniertes Inpainting für diese Modellfamilien.
- **2024-10-21 — ComfyUI V1 führt eine neue Oberfläche und Desktop-Beta ein.** Am 2024-10-21 stellte ComfyUI seine V1-Oberfläche vor und öffnete die geschlossene Beta der Desktop-Paketierung. Das Release brachte einen mitgelieferten Manager, Tabs, Einstellungen, Browser für Modelle und Workflows sowie Unterstützung beim Modell-Download. Die ursprüngliche Oberfläche wurde auf einen Wartungspfad verschoben.
- **2024-12-06 — ComfyUI reagiert auf die Kompromittierung des Ultralytics-Pakets.** Am 2024-12-06 dokumentierte ComfyUI seine Reaktion auf die bösartigen Pakete Ultralytics 8.3.41 und 8.3.42, auf die über einige Abhängigkeitsketten von Custom Nodes gestoßen wurde. Das Projekt unterschied die kompromittierte Abhängigkeit vom ComfyUI-Core und ergänzte Warnungen im Manager sowie das Pinnen von Versionen.
- **2025-07-28 — ComfyUI ergänzt Day-Zero-Unterstützung für Wan 2.2.** Am 2025-07-28 fügte ComfyUI native Day-Zero-Unterstützung für Wan 2.2 hinzu. Das Release stellte offizielle Text-zu-Video- und Bild-zu-Video-Workflows mit Mixture-of-Experts-Architektur bereit und enthielt die Modelldateien.
- **2025-08-13 — ComfyUI erweitert Wan-2.2-Fun-InP- und Control-Workflows.** Am 2025-08-13 ergänzte ComfyUI Unterstützung für Wan 2.2 Fun InP, Control und LightX2V. Die Workflows ermöglichten die Generierung zwischen erstem und letztem Frame, strukturelle Steuerungen sowie schnellere Vier-Schritt-Generierung mit LoRA-Beschleunigung.
- **2025-08-26 — ComfyUI ergänzt native Qwen-Image-DiffSynth-ControlNet-Unterstützung.** Am 2025-08-26 fügte ComfyUI native Unterstützung für Qwen-Image-DiffSynth-ControlNet hinzu. Das Update erweiterte die steuerbare Bildgenerierung und dokumentierte optionale, cache-basierte Beschleunigung des Workflows.
- **2025-08-27 — ComfyUI ergänzt gehostete Gemini- und lokale Qwen-Image-Steuerungspfade.** Am 2025-08-27 fügte ComfyUI zwei unterschiedliche Ausführungspfade hinzu: Google Gemini 2.5 Flash Image über kreditpflichtige Partner Nodes und lokale InstantX-Qwen-Image-Unified-ControlNet-Workflows. Die lokalen Workflows unterstützten Canny-, Depth-, Pose- und Soft-Edge-Steuerungen.
- **2025-08-28 — Zweite Comfy Challenge erweitert das Community-Workflow-Programm.** Am 2025-08-28 erweiterte ComfyUI seine Community-Showcase- und Workflow-Lernprogramme durch die zweite Comfy Challenge. Dabei handelte es sich um einen Meilenstein für Ökosystem und Bildung, nicht um ein Core-Runtime-Release.
- **2025-09-24 — ComfyUI ergänzt Workflows für Wan 2.2 Animate und Qwen-Image-Editing.** Am 2025-09-24 fügte ComfyUI native Workflows für Wan 2.2 Animate und Qwen-Image-Edit-2509 hinzu. Sie unterstützten performance-gesteuerte Charakteranimation und -ersetzung sowie Bearbeitung mit mehreren Bildern.
- **2025-10-07 — ComfyUI 0.3.63 macht Subgraphs veröffentlichbar.** Am 2025-10-07 machte ComfyUI 0.3.63 Subgraphs als wiederverwendbare Blueprint-Nodes veröffentlichbar. Das Release überarbeitete außerdem die Auswahlwerkzeuge für die Graph-Bearbeitung.
- **2025-10-09 — ComfyUI ergänzt Sora-2-Partner-Nodes.** Am 2025-10-09 machte ComfyUI Sora 2 und Sora 2 Pro über kostenpflichtige Partner Nodes verfügbar. Die Integration unterstützte Text-zu-Video- und Bild-zu-Video-Generierung mit Ton.
- **2025-10-22 — ComfyUI 0.3.66 verbessert Subgraph- und Template-Werkzeuge.** Am 2025-10-22 ergänzte ComfyUI 0.3.66 ein Parameter-Panel für Subgraphs. Das Release überarbeitete außerdem die Suche und Filterung von Workflow-Templates.
- **2025-11-26 — Comfy Cloud erweitert Infrastruktur und Funktionskontingente.** Am 2025-11-26 kündigte Comfy Cloud den Umstieg auf RTX-6000-Pro-Infrastruktur an sowie die Unterstützung für eigene LoRAs. Außerdem beschrieb es längere Pro-Läufe und vereinheitlichte Credits für Cloud-GPU-Ausführung und Partner Nodes.
- **2025-12-30 — ComfyUI beginnt mit der Verlagerung seines kanonischen Repositorys zu Comfy-Org.** Am 2025-12-30 begann ComfyUI, sein kanonisches GitHub-Repository von comfyanonymous/ComfyUI nach Comfy-Org/ComfyUI zu verlagern. GitHub-Weiterleitungen blieben erhalten, und Nutzer wurden aufgefordert, ihre Git-Remotes zu aktualisieren.
- **2026-01-27 — ComfyUI ergänzt Day-Zero-Unterstützung für Z-Image.** Am 2026-01-27 fügte ComfyUI Day-Zero-Unterstützung für das nicht destillierte Z-Image-Modell hinzu. Das Release enthielt einen offiziellen Workflow und modellspezifische Hinweise zum Sampling.
- **2026-02-05 — Das ComfyUI-Ökosystem kündigt eine Grant-Initiative für offene Modelle an.** Am 2026-02-05 kündigte das ComfyUI-Ökosystem eine Grant-Initiative für offene Modelle an, die als Programm mit 1 Million US-Dollar zusammen mit dem Launch von Anima beschrieben wurde. Die Initiative wurde als Finanzierung für die Entwicklung offener Modelle dargestellt.
- **2026-03-26 — ComfyUI führt stabiles Dynamic VRAM Management ein.** Am 2026-03-26 dokumentierte ComfyUI Dynamic VRAM als stabilen Mechanismus, um den Speicherdruck und Out-of-Memory-Fehler auf unterstützten Nvidia-Systemen zu verringern. Die Hinweise betonten, dass die gesamte Workflow-Dauer statt isolierter Iterationsgeschwindigkeit gemessen werden sollte.
- **2026-09-02 — Start der ComfyUI-H3VAE-TensorRT-Integration.** Der Maintainer kündigte eine TensorRT-Version des MiniMax-H3-VAE für ComfyUI an, die die Geschwindigkeit um bis zu 1,7-fach steigern kann.
  - Die Erweiterung stellt getrennte Compiler- und Loader-Nodes bereit. Die geprüfte Quellrevision ist 1b72e7439e1fc306b9dfbfd3d485866553b5960e, die später am 2. September committet wurde; die ursprüngliche Ankündigung nannte kein Release-Tag. (2026-09-02) — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>
- **2026-09-03 — ComfyUI-Update.** Ein unabhängiger Tester berichtete 48,8 s gegenüber 36,6 s für dieselbe VAE-Dekodierung mit 2,0 MP und sechs Sekunden auf einer RTX 4090 mit 24 GB, ComfyUI 0.34.2 und TensorRT 10.12. Bei 768p betrug das Ergebnis 19,6 s gegenüber 18,0 s. Dies ist ein einzelner, workload-spezifischer Dekodierungstest und keine Aussage über die Generierungsgeschwindigkeit insgesamt.

## Was sich geändert hat {#what-changed}

Der Maintainer berichtet von bis zu 1,7-fach schnellerer MiniMax-H3-VAE-Verarbeitung in einer Drittanbieter-Integration für ComfyUI. Die Angabe bezieht sich auf VAE-Encoding und -Decoding, nicht auf die End-to-End-Videogenerierung. Das Datum der ursprünglichen Ankündigung wird getrennt von der späteren Recherche geführt.

## So wird es verwendet {#how-to-use-this}

1. Klonen Sie die Erweiterung in ComfyUI/custom_nodes und installieren Sie deren Anforderungen mit derselben Python-Umgebung, in der ComfyUI läuft.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>
2. Laden Sie die ONNX-Dateien für Encoder und Decoder aus dem vom Maintainer verlinkten Modell-Repository herunter, einschließlich der zugehörigen .data-Dateien, sofern vorhanden. Legen Sie sie unter ComfyUI/models/vae ab.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>
3. Erstellen Sie die Engines mit MiniMax-H3 TRT VAE Compiler und laden Sie sie anschließend mit MiniMax-H3 TRT VAE Loader.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>

## Best Practices {#best-practices}

- Unterhalb von 12 GB VRAM empfiehlt der Maintainer den Decoder w4a16_awq. Betrachten Sie dies als Empfehlung des Autors, nicht als Garantie dafür, dass der vollständige Video-Workflow auf Ihre GPU passt.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README_zh.md>
- Vergleichen Sie dieselbe Latent-Repräsentation in Ihrer Zielauflösung und messen Sie die VAE-Dekodierung getrennt von der gesamten Generierungszeit. Der unabhängige Test ergab bei 768p einen deutlich geringeren Gewinn als bei 2,0 MP.
  — <https://note.com/seal309midorin/n/nb75b14bbab4e>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die ursprüngliche Ankündigung nennt weder ein unveränderliches Release-Tag noch die installierte Version.
- Die maximale Angabe von 1,7-fach durch den Maintainer ist kein unabhängiger Benchmark der vollständigen Videogenerierung.
- Ein chinesischer Community-Leitfaden wurde gefunden, seine Seite konnte im Verifizierungsdurchlauf jedoch nicht abgerufen werden. Die chinesischsprachige Abdeckung hier stammt aus der Dokumentation des Herstellers; ein unabhängiger chinesischer Benchmark wird nicht behauptet.
- Für diesen Artikel wurde kein Workflow auf unserer GPU ausgeführt. Hardware-Messwerte werden ihren jeweiligen Autoren zugeschrieben.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md | Maintainer-README, Englisch, angeheftete Quellrevision | 2026-09-05 |
| https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README_zh.md | Maintainer-README, vereinfachtes Chinesisch, als englische Zusammenfassung übersetzt | 2026-09-05 |
| https://note.com/seal309midorin/n/nb75b14bbab4e | Unabhängiger japanischer VAE-Dekodierungstest auf RTX 4090, öffentlicher Auszug | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:comfyui`, Thread `comfyui-development`, 21 datierte Ereignisse vom 2023-11-24 bis 2026-09-03.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ablösungen sind die maßgebliche Quelle dafür, was veraltet ist.
