---
title: "Bonsai Image 4B — Entwicklung von Bonsai Image"
category: projects
date: 2026-05-29
tags: [bonsai-image, project]
aliases: ["Bonsai Image 4B"]
level: 3
source_sha256: 4d9a8ddb8af72f50f3ec27b5230a0a1ff70bf17d15fcc3cc2e347b0387d819b5
translation: machine
translated_at: '2026-10-24'
---
# Bonsai Image 4B — Entwicklung von Bonsai Image {#bonsai-image-4b-bonsai-image-development}

**Entwicklungslinie:** `project:bonsai-image` · Thread `bonsai-image`  
**Letztes Ereignis:** 2026-05-29 · 1 datiertes seit 2026-05-29 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Bonsai Image 4B: eine Familie von Text-to-Image-Diffusionsmodellen für den lokalen Betrieb; Binary 1-bit für minimale Größe, Ternary für bessere Qualität; die WebGPU-Variante bleibt experimentell. Grenzwert: Der ternäre Transformer belegt 1,21 GB, das vollständige Apple-Silicon-Paket 3,88 GB. Fazit: Für die lokale Generierung sollte man mit dem ternären Low-Bit-Pack beginnen, nicht mit der FP16-Version.

## Entwicklungslinie {#development-line}

- **2026-05-29 — Bonsai Image 4B wurde über Hugging-Face-Ressourcen bekannt.** Am 2026-05-29 verwies ein datierter Eintrag auf eine Hugging-Face-Sammlung für Bonsai Image sowie auf einen mit dem Projekt verbundenen WebGPU-Space. Dies gilt als wesentliches Ereignis der Verbreitung und des Evaluierungszugangs, da konkrete öffentliche Projektressourcen genannt werden. Allein die Links belegen jedoch nicht, ob an diesem Datum ein Modellrelease, ein Update oder ein Benchmark stattfand.

## Was sich geändert hat {#what-changed}

2026-05-26 — PrismML veröffentlichte Bonsai Image 4B in zwei Varianten: Binary 1-bit und Ternary. 2026-05-29 — Die Links zur Gewichtssammlung und zur WebGPU-Demo spiegelten die Verfügbarkeit des Modells wider; der primäre Release präzisiert die Basis FLUX.2 Klein 4B, die Größe von 0,93 GB für Binary und 1,21 GB für den Ternary-Diffusion-Transformer sowie die lokalen Pfade für Apple Silicon und CUDA. 2026-06-01 — In der Sammlung erschienen plattformspezifische Low-Bit-Packs und entpackte FP16-Varianten; FP16 dient der Kompatibilität mit dem gewöhnlichen Diffusers und nicht der Speicherersparnis oder Beschleunigung.

## Verwendung {#how-to-use-this}

Ab 2026-05-29 können Anwender die verlinkte Hugging-Face-Sammlung und den WebGPU-Space als Ausgangspunkte nutzen, um Bonsai Image 4B zu finden und zu evaluieren. Status, Fähigkeiten oder Nutzungshinweise sollten sie allein aus diesen Links nicht ableiten.

1. Klonen Sie Bonsai Image Demo und führen Sie das Setup für Ihre Plattform aus: MLX unter macOS oder gemlite/HQQ unter Linux oder Windows.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
2. Laden Sie standardmäßig die Ternary-Variante; wählen Sie Binary, wenn minimale Größe wichtiger ist als Qualität.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
3. Starten Sie das Studio über scripts/serve oder senden Sie Anfragen über send_request an ein bereits laufendes Backend, um den Kaltstart nicht für jedes Bild erneut zu bezahlen.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
4. Für den experimentellen Start im Browser öffnen Sie die WebGPU-Demo, laden das Ternary-Modell, geben Prompt und Parameter an; die Seite fordert ein Hugging-Face-Access-Token an.
  — <https://huggingface.co/spaces/webml-community/bonsai-image-webgpu>

## Bewährte Praktiken {#best-practices}

- Verwenden Sie Ternary als Standardvariante: Die offizielle Demo empfiehlt sie wegen der besseren Qualität bei moderatem Größenzuwachs.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
- Wählen Sie entpackte FP16-Safetensors nicht um der lokalen Effizienz willen: Sie dienen als Fallback für den Standard-Diffusers und behalten nicht die Vorteile des Low-Bit-Packs.
  — <https://huggingface.co/prism-ml/bonsai-image-ternary-4B-unpacked>
- Betrachten Sie die Kompatibilität der Browser-Demo außerhalb von Apple M4 Max und M5 Max als ungeprüft; Chrome/Edge bietet das Flag für unsichere WebGPU-Nutzung nur zur Leistungssteigerung an.
  — <https://webml-community-bonsai-image-webgpu.static.hf.space/index.html>

## Dadurch überholt {#superseded-by-this}

- 2026-06-01 — Die Empfehlung, entpackte FP16-Dateien als Hauptpfad zu verwenden, ist veraltet: Die offiziellen Modellkarten empfehlen optimierte MLX- oder gemlite-Low-Bit-Packs.

## Noch unbekannt {#still-unknown}

- Der primäre Release ist auf 2026-05-26 datiert, der erfasste Schritt auf 2026-05-29; das genaue Erstellungsdatum der Sammlung und des WebGPU-Space ist in den geprüften Quellen nicht bestätigt.
- Die erforderlichen Felder event_findings und new_events fehlen im bereitgestellten Ausgabeschema; die ereignisbezogene Präzisierung und der frühere Release sind unter was_sich_geändert_hat (what_changed) abgebildet.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://prismml.com/news/bonsai-image-4b | Introducing 1-bit and Ternary Bonsai Image 4B: Image Generation for Local Devices | 2026-09-05 |
| https://huggingface.co/collections/prism-ml/bonsai-image | Bonsai Image – eine Sammlung von prism-ml | 2026-09-05 |
| https://huggingface.co/spaces/webml-community/bonsai-image-webgpu | Bonsai Image WebGPU – ein Hugging-Face-Space von webml-community | 2026-09-05 |
| https://webml-community-bonsai-image-webgpu.static.hf.space/index.html | Bonsai-Image-Generierung: WebGPU-Demo | 2026-09-05 |
| https://huggingface.co/prism-ml/bonsai-image-ternary-4B-mlx-2bit | prism-ml/bonsai-image-ternary-4B-mlx-2bit | 2026-09-05 |
| https://huggingface.co/prism-ml/bonsai-image-ternary-4B-unpacked | Bonsai Image Ternary 4B — Entpackte FP16-Safetensors | 2026-09-05 |
| https://github.com/PrismML-Eng/Bonsai-image-demo | PrismML-Eng/Bonsai-Image-Demo | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:bonsai-image`, Thread `bonsai-image`, 1 datiertes Ereignis, 2026-05-29 → 2026-05-29.
- **Praktischer Hinweis:** Ab 2026-05-29 können Anwender die verlinkte Hugging-Face-Sammlung und den WebGPU-Space als Ausgangspunkte nutzen, um Bonsai Image 4B zu finden und zu evaluieren. Status, Fähigkeiten oder Nutzungshinweise sollten sie allein aus diesen Links nicht ableiten.
- **Konfidenz:** hoch. Die datierten Überholungsvermerke oben sind maßgeblich für die Frage, was veraltet ist.
