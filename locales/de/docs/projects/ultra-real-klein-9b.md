---
title: "Ultra Real - Klein 9b — Klein 9b"
category: projects
date: 2026-03-23
tags: [klein-9b, project, ultra-real-klein-9b]
aliases: ["Ultra Real - Klein 9b"]
level: 2
source_sha256: 1b404e90ad930bd14749904192cc4f94a56fb6cb0c8f6785f153d42485b99527
translation: machine
translated_at: '2026-10-24'
---
# Ultra Real - Klein 9b — Klein 9b {#ultra-real-klein-9b-klein-9b}

**Entwicklungslinie:** `project:ultra-real-klein-9b` · Thread `klein-9b`  
**Letztes Ereignis:** 2026-03-23 · 1 datiertes seit 2026-03-23 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Ultra Real - Klein 9b ist ein LoRA für Nutzer von FLUX.2 Klein 9B in ComfyUI.

- Porträterstellung: erzeugt Porträts.
- Bildbearbeitung: verändert bestehende Bilder.
- Upscaling: restauriert alte Bilder.

Die Versionen V1–V4 sind verfügbar: V3 erzeugt eine feinere Textur, während V4 für die Detailverarbeitung gedacht ist.
Das LoRA ist kein Basismodell und setzt einen kompatiblen Klein-9B-Workflow voraus.
Für natürliche Haut beginnt man mit V3 und verwendet V4 nur für einen Detail-Durchgang.

## Entwicklungslinie {#development-line}

- **2026-03-23 — Ultra Real - Klein 9b mit einer Civitai-Modellseite und ComfyUI-Workflows verknüpft.** V2 soll eine natürlichere Hauttextur mit besserer Erhaltung von Ton und Beleuchtung bieten.

## Was sich geändert hat {#what-changed}

- 2026-03-23 — Ultra Real - Klein 9b war als V1/V2-LoRA-Linie für FLUX.2 Klein 9B verfügbar; V2 versprach eine natürlichere Hauttextur mit besserer Erhaltung von Ton und Beleuchtung.
- 2026-04-10 — Der Modelleintrag wurde auf die V1–V4-Linie aktualisiert; V3 wurde als feinere Textur ohne zusätzliche Sommersprossen beschrieben, V4 als eigener Detailmodus.
- 2026-04-13 — Die aktuelle Karte führt FLUX.2 Klein 9B als Basismodell und V1–V4 als Varianten einer LoRA-Linie auf.

## Anwendung {#how-to-use-this}

Ab 2026-03-23 dient die verlinkte Civitai-Modellseite und das ComfyUI-Workflows-Repository als datierte Referenzpunkte für die Bewertung von Ultra Real - Klein 9b. Allein die Links belegen jedoch keine bestimmte Version, Workflow-Kompatibilität oder Leistungsangabe.

1. Kompatible FLUX.2-Klein-9B-Komponenten in die passenden ComfyUI-Ordner installieren: das Diffusionsmodell, den Qwen-3-8B-Text-Encoder und das flux2-VAE.
  — <https://github.com/Comfy-Org/docs/blob/main/ja/tutorials/flux/flux-2-klein.mdx>
2. Ultra Real - Klein 9b in den LoRA-Slot des Klein-9B-Workflows laden; für Bildbearbeitung mit V3 mit Gewicht 0,6 beginnen, für V4 mit 0,55.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
3. Für die Bearbeitung eine Anweisung verwenden, die Gesicht, Ausdruck, Statur, Pose und Komposition erhält; für V2 liegt das veröffentlichte Zielgewicht bei 0,5.
  — <https://tensor.art/models/981017447823890853>
4. Für Text-zu-Bild mit einem Gewicht von 0,7–0,8 beginnen und die Aufnahme als Fotografie beschreiben; das veröffentlichte Zielgewicht für V2 ist 0,7.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>

## Best Practices {#best-practices}

- V4 nicht als universelles Stil-LoRA verwenden: Die Beschreibung beschränkt es auf die Detailverarbeitung; für die Standarderzeugung einen Text-Prompt oder ein anderes LoRA verwenden.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
- Einstellungen von V1 nicht ohne Test übernehmen: V1 kann Poren und Sommersprossen übersteigern oder Beleuchtung und Hautton verschieben; V3 verspricht ein feineres Ergebnis.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
- Bei der Bildbearbeitung das Modell ausdrücklich anweisen, Merkmale, Ausdruck, Pose und Komposition beizubehalten, damit das LoRA nicht mehr als die Hauttextur verändert.
  — <https://tensor.art/models/981017447823890853>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-04-10 — V1 ist für natürliche Haut nicht mehr der bevorzugte Modus: Die aktuelle Karte beschreibt V3 als feinere Textur und V4 als eigenen Detail-Durchgang.
- 2026-04-10 — Die Empfehlung, dasselbe LoRA sowohl für die Erzeugung als auch für die Detailverarbeitung zu verwenden, ist überholt: V4 ist ausdrücklich auf die Detailverarbeitung beschränkt.

## Weiterhin unbekannt {#still-unknown}

- Die direkte Civitai-Seite und das Workflow-Repository waren während der Prüfung nicht sinnvoll herunterladbar; Einstellungen sind durch Spiegelungen und Veröffentlichungsseiten bestätigt, nicht durch die ursprünglichen Workflow-Dateien.
- Die aktuelle SeaArt-Karte nennt ein Ankündigungsdatum von 2026-03-13, ein Aktualisierungsdatum von 2026-04-10 und ein Veröffentlichungsdatum von 2026-04-13, gibt aber keine eigenen Veröffentlichungsdaten für V3 und V4 an; eine genauere Datierung ist nicht möglich.
- Die Civitai-ID 2462105 taucht auf einigen Spiegelungen später auch für UltraReal - Krea2, Klein9b auf; nichts belegt, dass es sich um eine Fortsetzung desselben Klein-9B-LoRA handelt und nicht um eine Wiederverwendung der Karte.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://civitai.com/models/2462105/ultra-real-klein-9b | Ultra Real - Klein 9b — Civitai-Modellseite | 2026-09-05 |
| https://github.com/vizsumit/comfyui-workflows | vizsumit/comfyui-workflows | 2026-09-05 |
| https://civarchive.com/seaart/models/0b4b3278ab4fd5b6471cd029ef88fc09/versions/4eaaed353d71f3ae09efa4411c954877 | Ultra Real - Klein 9b V2 — CivArchive | 2026-09-05 |
| https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09 | Ultra Real - Klein 9b — SeaArt-Modellseite | 2026-09-05 |
| https://tensor.art/models/981017447823890853 | Ultra Real - Klein 9b V1 — Tensor.Art | 2026-09-05 |
| https://github.com/Comfy-Org/docs/blob/main/ja/tutorials/flux/flux-2-klein.mdx | FLUX.2-Klein-ComfyUI-Tutorial | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:ultra-real-klein-9b`, Thread `klein-9b`, 1 datiertes Ereignis 2026-03-23 → 2026-03-23.
- **Praxishinweis:** Ab 2026-03-23 sollten Anwender die verlinkte Civitai-Modellseite und das ComfyUI-Workflows-Repository als datierte Referenzpunkte für die Bewertung von Ultra Real - Klein 9b nutzen; allein die Links belegen keine bestimmte Version, Workflow-Kompatibilität oder Leistungsangabe.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
