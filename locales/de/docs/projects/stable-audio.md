---
title: "Stable Audio"
category: projects
date: 2025-09-12
tags: [model_release, project, stable-audio, stable-audio-releases]
aliases: ["Stable Audio"]
level: 2
source_sha256: e6f9da3e17b141e85cb22cfe685ab1b125a24d919d1b535d5754b50ceb137206
translation: machine
translated_at: '2026-10-24'
---
# Stable Audio {#stable-audio}

**Entwicklungslinie:** `project:stable-audio` · Thread `stable-audio-releases`  
**Letztes Ereignis:** 2025-09-12 · 2 datierte Ereignisse seit 2023-09-13 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Stable Audio ist eine Webanwendung, eine API und eine Modellfamilie für Text-zu-Audio, Audio-zu-Audio, Inpainting und Audiobearbeitung.

- Musik: erzeugt Tracks und vollständige Mixe.
- SFX: erzeugt Soundeffekte und Audioclips.
- Samples und Variationen: erzeugt alternative Versionen.
- Einzelspuren: isoliert einzelne Stems.
- Lokale Ausführung: betreibt ausgewählte Open-Weight-Modelle.

Die Grenzwerte hängen vom Modell ab: Stable Audio 3.0 Medium und Large sind für mehr als sechs Minuten ausgelegt. Verwenden Sie für neue Arbeiten Stable Audio 3.0 und dessen Bereitstellungsmodi statt der älteren Grenzwerte von 1.0 oder 2.5.

## Entwicklungslinie {#development-line}

- **2023-09-13 — Stable Audio wurde vorgestellt.** Text-zu-Audio im Browser erzeugt Audio aus Textprompts und Zieldauern.
- **2025-09-12 — Stable Audio 2.5 wurde für die Enterprise-Klangproduktion vorgestellt.** Drei-Minuten-Tracks, Text-zu-Audio, Audio-zu-Audio und Audio-Inpainting.

## Was sich geändert hat {#what-changed}

- 2023-09-13 — Stable Audio startete als kommerzielles Produkt mit Text-zu-Audio im Browser auf Basis von Beschreibungen und festgelegten Dauern.
- 2025-09-12 — Stable Audio 2.5 erschien für die Audioproduktion in Unternehmen und ergänzte Drei-Minuten-Tracks, Text-zu-Audio, Audio-zu-Audio und Audio-Inpainting.
- 2026-05-20 — Stable Audio 3.0 startete mit den Open-Weight-Modellen Small SFX, Small und Medium sowie API- und selbst gehosteten Large-Modellen; die Generierungslänge reicht bei Medium und Large nun über sechs Minuten.

## Wie Sie das nutzen {#how-to-use-this}

Ab 2023-09-13 konnten Praktiker Stable Audio als eigenständiges Produkt zur Audioerzeugung betrachten; ab 2025-09-12 sollten sie Stable Audio 2.5 und dessen Verfügbarkeit in ComfyUI evaluieren, wenn ein auf Unternehmen ausgerichteter Workflow zur Klangproduktion benötigt wird.

1. Wählen Sie einen Weg: den Browser-Studio für Erstellung und Bearbeitung, die Open-Weight-Modelle Small SFX, Small oder Medium für lokale Infrastruktur oder API und selbst gehostetes Large für umfangreiche Produkte.
  — <https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models>
2. Legen Sie eine Session an und beginnen Sie mit Full Mix. Geben Sie im Prompt Genre, Instrumente, Tempo, Stimmung und Zieldauer an.
  — <https://stableaudio.com/docs>
3. Verwenden Sie Multi-Track für eine strukturierte Arrangierung und hängen Sie Referenzen nur an, um Tempo und Tonart vorzugeben.
  — <https://stableaudio.com/docs>
4. Korrigieren Sie einzelne Spuren oder Zeitbereiche mit Regenerate, Replace Section oder Extend und exportieren Sie anschließend den fertigen Mix.
  — <https://stableaudio.com/docs>

## Bewährte Praktiken {#best-practices}

- Formulieren Sie präzise Prompts: Genre, Instrumente, BPM, Stimmung und Epoche steuern die Ausgabe besser als ein allgemeiner Genre-Tag.
  — <https://stableaudio.com/docs>
- Beginnen Sie mit Full Mix, wenn die wörtliche Interpretation des Prompts wichtig ist. Multi-Track erleichtert das Mischen von Stems, doch sein Arrangement-Agent kann vom Prompt abweichen.
  — <https://stableaudio.com/docs>
- Wählen Sie Small SFX oder Open Small für kurze SFX, Foley und Produktionselemente. Für vollständige Musik wählen Sie Small, Medium oder Large je nach Länge und Hosting-Setup.
  — <https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models>
- Laden Sie kein urheberrechtlich geschütztes Audiomaterial in Audio-zu-Audio- oder Inpainting-Werkzeuge hoch. Die Nutzungsbedingungen verlangen, dass hochgeladenes Material keine Urheberrechte verletzt.
  — <https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale>

## Hiermit ersetzt {#superseded-by-this}

- 2023-09-13 — Grenzwerte des ersten Webprodukts: bis zu 45 Sekunden im kostenlosen Tarif und 90 Sekunden im Pro-Tarif beschreiben das aktuelle Angebot nicht mehr; 3.0 Medium und Large erzeugen Audio für mehr als sechs Minuten.
- 2025-09-10 — Die Positionierung von Stable Audio 2.5 als neuestes Modell wurde mit dem Start von Stable Audio 3.0 am 2026-05-20 überholt.

## Weiterhin unbekannt {#still-unknown}

- Aktuelle Preisstufen, Kontingente und Partnerintegrationen ändern sich unabhängig von Modellveröffentlichungen. Prüfen Sie die Verfügbarkeit direkt über Ihren gewählten Zugangsweg, bevor Sie einen Kauf oder einen Produktionseinsatz planen.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://stableaudio.com/ | Stable Audio — Generative AI for music & sound fx | 2026-09-05 |
| https://stableaudio.com/docs | How to use Stable Audio | 2026-09-05 |
| https://stability.ai/news-updates/stable-audio-using-ai-to-generate-music | Announcing Stable Audio, a product for music & sound generation | 2026-09-05 |
| https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale | Stability AI Introduces Stable Audio 2.5, the First Audio Model Built for Enterprise Sound Production at Scale | 2026-09-05 |
| https://stability.ai/news-updates/stable-audio-2-0 | Introducing Stable Audio 2.0 | 2026-09-05 |
| https://stability.ai/news-updates/introducing-stable-audio-open | Introducing Stable Audio Open - An Open Source Model for Audio Samples and Sound Design | 2026-09-05 |
| https://stability.ai/news-updates/stability-ai-and-arm-release-stable-audio-open-small-enabling-real-world-deployment-for-on-device-audio-control | Stability AI and Arm Collaborate to Release Stable Audio Open Small, Enabling Real-World Deployment for On-Device Audio Generation | 2026-09-05 |
| https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models | Meet Stable Audio 3.0, the model family built for artistic experimentation with open-weight models | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:stable-audio`, Thread `stable-audio-releases`, 2 datierte Ereignisse vom 2023-09-13 bis 2025-09-12.
- **Praktischer Hinweis:** Ab 2023-09-13 konnten Praktiker Stable Audio als eigenständiges Produkt zur Audioerzeugung betrachten; ab 2025-09-12 sollten sie Stable Audio 2.5 und dessen Verfügbarkeit in ComfyUI evaluieren, wenn ein auf Unternehmen ausgerichteter Workflow zur Klangproduktion benötigt wird.
- **Konfidenz:** hoch. Die datierten Einträge unter „Hiermit ersetzt“ sind maßgeblich dafür, was veraltet ist.
