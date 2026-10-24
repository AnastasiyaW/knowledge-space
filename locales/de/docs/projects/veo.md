---
title: "Veo"
category: projects
date: 2024-05-14
tags: [google_io_2024, project, veo, veo-development]
aliases: ["Veo", "Veo 3"]
level: 2
source_sha256: 42109440b97fafdd3513c5c6c01950d6bbb2c8606d29b991697ef965d0a65175
translation: machine
translated_at: '2026-10-24'
---
# Veo {#veo}

**Entwicklungslinie:** `project:veo` · Thread `veo-development`  
**Letztes Ereignis:** 2024-05-14 · 1 datiertes seit 2024-05-14 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Veo ist die Videogenerierungs-Modellfamilie von Google DeepMind für Filmschaffende, Kreative und API-Nutzer.

- Videoclips: erzeugt Text-zu-Video- und Bild-zu-Video-Clips.
- Frame-Steuerung: unterstützt Referenzbilder, Generierung von erstem und letztem Frame sowie Verlängerung.
- Audiospuren: erzeugt synchronisierte Dialoge, Soundeffekte und Atmosphäre.

## Entwicklungslinie {#development-line}

- **2024-05-14 — Veo auf der Google I/O 2024 vorgestellt.** Am 2024-05-14 stellte Google Veo auf der Google I/O 2024 vor. Dies markiert den Beginn der identifizierten Veo-Entwicklungslinie und ist für ihre öffentliche Historie von Bedeutung.

## Was sich geändert hat {#what-changed}

- 2024-05-14 — Google stellte Veo als 1080p-Videomodell vor, das nur ausgewählten Kreativen über die VideoFX-Private-Preview zur Verfügung stand.
- 2025-05-20 — Veo 3 erhielt native Audiounterstützung. Google stellte Flow vor und machte Veo 3 in Gemini, Flow und Vertex AI unter angekündigten Zugangsbedingungen verfügbar.
- 2025-09-26 — Veo 3 war Gegenstand eines Zero-Shot-Forschungsberichts zu visueller Wahrnehmung, Manipulation, physikalischer Modellierung und einfachem visuellen Schlussfolgern. Dabei handelte es sich um Forschungsevidenz, nicht um einen neuen Produktendpunkt.
- 2025-10-15 — Veo 3.1 ergänzte Audio für Ingredients to Video, Frames to Video und Extend in Flow, mit verbesserter Einhaltung von Prompts bei Bild-zu-Video.
- 2026-01-13 — Veo 3.1 Ingredients to Video ergänzte native 9:16-Ausgabe sowie 1080p- und 4K-Optionen in unterstützten professionellen Workflows.

## So nutzt du das {#how-to-use-this}

Ab 2024-05-14 sollten Praktiker Veo als eigenständiges Videogenerierungsprojekt behandeln und dessen weitere Releases, Zugangsänderungen und Modellfähigkeiten getrennt von allgemeinen Ankündigungen der Google I/O verfolgen.

1. Erstelle einen Gemini-API-Client, sende eine Generierungsanfrage mit einem Veo-Modellnamen, frage die langlaufende Operation ab und lade anschließend das generierte Video herunter.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
2. Formuliere den Prompt als Motiv, Aktion, Stil, Kamera, Komposition, Fokus und Atmosphäre. Füge wörtliche Dialoge oder explizite Klanghinweise hinzu, wenn Audio relevant ist.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
3. Stelle für kontrollierte Bild-zu-Video-Arbeiten ein Ausgangsbild, bis zu drei Referenzbilder oder erstes und letztes Frame bereit. Verwende die Verlängerung nur für einen von Veo generierten Clip.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
4. Lade die Ausgabe zügig herunter: Google dokumentiert eine serverseitige Aufbewahrungsdauer von zwei Tagen.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>

## Best Practices {#best-practices}

- Gib Kameraposition oder Kamerabewegung, Bildausschnitt, Objektiv/Fokus und Atmosphäre an, statt dich allein auf Stilbezeichnungen zu verlassen.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
- Verwende Referenzbilder für die Konsistenz von Figur, Produkt oder Szene; die dokumentierte Grenze liegt bei drei Assets.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
- Plane hochauflösende Aufnahmen, Aufnahmen mit Referenzbildern und Verlängerungen als Einheiten von acht Sekunden; die Verlängerung ist auf 720p begrenzt.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
- Formuliere Anforderungen an Sprache und Klang explizit und prüfe die Ergebnisse anschließend. Google dokumentiert verbleibende Einschränkungen bei natürlicher, konsistenter gesprochener Audioausgabe.
  — <https://deepmind.google/models/veo/>

## Durch diese Angaben überholt {#superseded-by-this}

- 2024-05-14 — Veo lässt sich nicht mehr korrekt als reine VideoFX-Private-Preview beschreiben; die aktuelle Dokumentation stellt es über die Gemini API und mehrere Google-Produkte bereit.
- 2024-05-14 — Die ursprüngliche Positionierung „beyond a minute“ („über eine Minute hinaus“) beschreibt nicht die aktuell dokumentierte API-Einheit, die ein generierter Clip mit 4, 6 oder 8 Sekunden ist.

## Weiterhin offen {#still-unknown}

- Der Eintrag vom 2024-05-14 enthielt keine URL; seine Zuordnung beruht daher auf Googles gleichdatierter Veo-Ankündigung und nicht auf dem ursprünglich verlinkten Material.
- Der Eintrag vom 2025-09-26 verlinkt auf ein Veo-3-Forschungsprojekt, nicht auf eine Produktveröffentlichungsseite. Die offizielle Veröffentlichungsseite ist auf 2025-09-24 datiert; das genaue Verhältnis zwischen dem Eintrag vom 26. September und einer bestimmten Revision der Veröffentlichung ist nicht angegeben.
- Das Zero-Shot-Forschungsergebnis sollte nicht als unterstützter Produktionsworkflow behandelt werden und auch nicht als Beleg dafür, dass Veo Segmentierungs-, Bearbeitungs- oder Schlussfolgerungs-APIs bereitstellt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://blog.google/innovation-and-ai/products/google-generative-ai-veo-imagen-3/ | New generative media models and tools, built with and for creators | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/ | Fuel your creativity with new generative media models and tools | 2026-09-05 |
| https://deepmind.google/research/publications/203190/ | Video models are zero-shot learners and reasoners | 2026-09-05 |
| https://video-zero-shot.github.io/ | Video models are zero-shot learners and reasoners | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/veo-updates-flow/ | Introducing Veo 3.1 and advanced capabilities in Flow | 2026-09-05 |
| https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/ | Veo 3.1 Ingredients to Video: More consistency, creativity and control | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/veo?hl=en | Generate videos with Veo 3.1 in Gemini API | 2026-09-05 |
| https://deepmind.google/models/veo/ | Veo 3.1 | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:veo`, Thread `veo-development`, 1 datiertes Ereignis 2024-05-14 → 2024-05-14.
- **Praktischer Hinweis:** Ab 2024-05-14 sollten Praktiker Veo als eigenständiges Videogenerierungsprojekt behandeln und dessen weitere Releases, Zugangsänderungen und Modellfähigkeiten getrennt von allgemeinen Ankündigungen der Google I/O verfolgen.
- **Konfidenz:** hoch. Die datierten Einträge unter „Durch diese Angaben überholt“ sind maßgeblich dafür, was veraltet ist.
