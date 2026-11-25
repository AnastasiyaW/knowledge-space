---
title: "GalaxyAce LoRA"
category: projects
date: 2026-03-30
tags: [galaxyace-lora, project]
aliases: ["GalaxyAce LoRA"]
level: 2
source_sha256: ad1af1e87bacec8240fd3b0895e174a0897c793cbab229c9736b77fc81e36bca
translation: machine
translated_at: '2026-10-24'
---
# GalaxyAce LoRA {#galaxyace-lora}

**Entwicklungslinie:** `project:galaxyace-lora` · Thread `galaxyace-lora`  
**Letztes Ereignis:** 2026-03-30 · 1 datiertes seit 2026-03-30 · **Recherchiert:** 2026-09-04 · Konfidenz: medium

## Was es ist {#what-it-is}

GalaxyAce LoRA — das sind eigenständige Style-LoRAs für Foto- und Videoautoren, die Aufnahmen im Stil einer günstigen Android-Kamera von Anfang der 2010er-Jahre benötigen. — Farbwiedergabe, Belichtung und Weichheit des Objektivs; — für LTX-Varianten — Sensorrauschen, Kompression und Handzittern; — für H3 — derselbe visuelle Effekt bei Videos mit nativem Audio. Eine Datei ist an ihr Basismodell gebunden: LTX-2/2.3, Z-Image-Turbo, Krea 2 und MiniMax H3 verwenden keine austauschbaren Gewichte. Fazit: Es handelt sich um einen Adapter für einen konkreten Workflow, nicht um einen universellen Filter für jeden Checkpoint.

## Entwicklungslinie {#development-line}

- **2026-03-30 — Versionsspezifische Civitai-Referenz für GalaxyAce LoRA erfasst.** Am 2026-03-30 hat diese Entwicklungslinie eine versionsspezifische Civitai-URL für GalaxyAce LoRA erfasst, die Modell 2200329 und Version 2808759 identifiziert. Sie dient als datierter Identitätsanker für diese Modellversion, während Veröffentlichungskontext, Trainingsdetails und Kompatibilität unverifiziert bleiben.

## Was sich geändert hat {#what-changed}

GalaxyAce LoRA — die Linie ist von LTX-2.3 zu eigenständigen Varianten für Krea 2 und MiniMax H3 übergegangen. 2026-03-30 — der Verweis auf Version 2808759 fixiert die Variante LTXV 2.3; das öffentliche Update beschreibt Stärke 1.0, fehlendes Trigger-Wort und die Einbindung nach dem Checkpoint innerhalb des ComfyUI-T2V/I2V-Subgraphs. 2026-06-25 (heute gefunden, Update des Autors) — eine eigenständige Variante für Krea 2 Raw und Turbo wurde ergänzt; die Stärke hängt nun davon ab, wie nah der Prompt an den Alltagsszenen aus dem Training liegt. 2026-07-06 — die Root-Seite des Modells wird ohne Version-ID angegeben; ein neues Gewicht oder eine neue Einstellung zu diesem Datum lässt sich nicht feststellen. 2026-08-05 (heute gefunden, Update des Autors) — eine MiniMax-H3-Variante 3201619 für Videos mit nativem Ton und einer anderen Prompt-Form wurde ergänzt. Stand 2026-09-04 wird die verfügbare Karte als MiniMax H3 bezeichnet, ihr Inhalt erfordert jedoch eine Anmeldung.

## Anwendung {#how-to-use-this}

Stand 2026-03-30 können Anwender das Civitai-Modell 2200329, Version 2808759 als datierten Herkunftsnachweis für GalaxyAce LoRA beibehalten, sollten aber Trainingsmethode, Inhalt, Kompatibilität oder spätere Updates nicht allein aus dieser Entwicklungslinie ableiten.

1. Öffnen Sie die Modellkarte, melden Sie sich bei Civitai an und wählen Sie gezielt die MiniMax-H3-Variante; laden Sie kein LTX- oder Krea-Gewicht in einen H3-Workflow.
  — <https://civitai.red/models/2200329/galaxyace-lora>
2. Richten Sie MiniMax H3 Base gemäß der offiziellen Anleitung ein und beginnen Sie mit dem empfohlenen ComfyUI-T2V- oder R2V-Template.
  — <https://github.com/MiniMax-AI/MiniMax-H3>
3. Binden Sie das H3-kompatible GalaxyAce LoRA im LoRA-Slot des H3-Workflows ein; im Spiegel der aktuellen Version sind als Startwerte strength 1.0, guidance_scale 1, 768p/24 fps, Anzahl der Frames 17n+5 und Auflösungen, die durch 32 teilbar sind, angegeben.
  — <https://fastsdmodel.com/models/2200329?lang=zh>
4. Formulieren Sie einen zusammenhängenden Prompt in der Reihenfolge „Szene → Beats mit Zeitcodes → Kamerabewegung → Audio → ohne Text und Logos“.
  — <https://www.reddit.com/r/comfyui/comments/1vgkbej/sora_2_vibes_on_minimax_h3_galaxyace_lora_update/>

## Best Practices {#best-practices}

- Beschreiben Sie bei MiniMax H3 den gewünschten Ton explizit und verwenden Sie keine Tag-Enden oder Gewichtungsklammern wie in CLIP-Pipelines; Struktur und positive Formulierungen funktionieren zuverlässiger.
  — <https://fastsdmodel.com/models/2200329?lang=zh>
- Kombinieren Sie den Effekt der billigen Kamera nicht mit Wörtern wie cinematic, anamorphic, depth of field, iPhone oder benannten Colour Grades: Sie widersprechen dem festen, kleinen Objektiv und der Automatikbelichtung.
  — <https://www.reddit.com/r/comfyui/comments/1vgkbej/sora_2_vibes_on_minimax_h3_galaxyace_lora_update/>
- Nur für die Krea-2-Variante: Beginnen Sie bei Alltagsszenen mit 1.0, verwenden Sie 1.25–1.45 als Realism Detailer und 1.7–2.0 für den vollen Effekt oder ungewöhnliche Handlungen; dies sind keine H3-Parameter.
  — <https://www.reddit.com/r/comfyui/comments/1ufksvg/galaxyace_lora_update_now_supports_krea_2/>
- Wenn in H3 die Sprache nicht mehr synchron ist, rät die gespiegelte Anleitung, zuerst die Stärke des LoRA auf 0.7 zu senken, statt den Prompt umzuschreiben; ein Negativ-Prompt ist dort kein funktionierendes Mittel zum Ausschluss.
  — <https://fastsdmodel.com/models/2200329?lang=zh>

## Hierdurch überholt {#superseded-by-this}

- 2026-03-30 — Die Anleitung für LTX-2.3, das LoRA nach dem Checkpoint anzuschließen, ist nach dem Erscheinen der H3-Variante keine allgemeingültige Anleitung mehr; sie gilt nur noch für das Gewicht LTXV 2.3.
- 2026-06-25 — Die Stärkeskala der Krea 2 von 1.0 bis 2.0 ist als allgemeine Empfehlung für GalaxyAce LoRA überholt: Sie bezieht sich nur auf Krea-2 Raw/Turbo.
- 2026-07-06 — Ein Root-Link ohne Version-ID kann nicht als Hinweis auf das aktuelle Gewicht gelten; später wurde die H3-Variante 3201619 veröffentlicht.

## Weiterhin unbekannt {#still-unknown}

- Die direkte Civitai-Karte erfordert eine Anmeldung: Dateiliste, SHA-256, Lizenz, Autorenkonto und Verfügbarkeit früherer Versionen sind nicht bestätigt.
- Die H3-Parameter aus Fast SD Model stammen von einem Drittanbieter-Spiegel und wurden nicht mit der herunterladbaren Datei auf Civitai abgeglichen.
- Zwei datierte Verweise haben dieselbe Modell-ID 2200329; es gibt daher keine Anzeichen für zwei verschiedene Objekte. LTX, Krea und H3 wirken wie unterschiedliche basisspezifische Versionen einer Serie.
- Es existiert ein gleichnamiges Hugging-Face-Repository, dessen Herkunft jedoch nicht durch eine überprüfbare Quelle mit dem Civitai-Modell verbunden ist; es wurde aus den Anleitungen ausgeschlossen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://civitai.red/models/2200329/galaxyace-lora | GalaxyAce LoRA - MiniMax H3 GalaxyAce LoRA | Hailuo H3 by MiniMax LoRA | Civitai | 2026-09-04 |
| https://www.reddit.com/r/comfyui/comments/1vgkbej/sora_2_vibes_on_minimax_h3_galaxyace_lora_update/ | Sora 2 vibes on MiniMax H3 — GalaxyAce LoRA Update | 2026-09-04 |
| https://github.com/MiniMax-AI/MiniMax-H3 | MiniMax H3 | 2026-09-04 |
| https://fastsdmodel.com/models/2200329?lang=zh | GalaxyAce LoRA | Fast SD Model | 2026-09-04 |
| https://civitai.com/models/2200329/galaxyace-lora?modelVersionId=2808759 | GalaxyAce LoRA model URL (version 2808759) | 2026-09-04 |
| https://www.reddit.com/r/comfyui/comments/1s5g11w/galaxyace_lora_update_now_supports_ltx23/ | GalaxyAce LoRA Update — Now Supports LTX-2.3 | 2026-09-04 |
| https://www.reddit.com/r/comfyui/comments/1ufksvg/galaxyace_lora_update_now_supports_krea_2/ | GalaxyAce LoRA Update — Now Supports Krea 2 | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:galaxyace-lora`, Thread `galaxyace-lora`, 1 datiertes Ereignis 2026-03-30 → 2026-03-30.
- **Praktischer Hinweis:** Stand 2026-03-30 können Anwender das Civitai-Modell 2200329, Version 2808759 als datierten Herkunftsnachweis für GalaxyAce LoRA beibehalten, sollten aber Trainingsmethode, Inhalt, Kompatibilität oder spätere Updates nicht allein aus dieser Entwicklungslinie ableiten.
- **Konfidenz:** medium. Die datierten Einträge unter „Hierdurch überholt“ sind maßgeblich dafür, was veraltet ist.
