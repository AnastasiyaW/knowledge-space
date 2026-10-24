---
title: "FLUX Video Upscale — Black Forest Labs"
category: projects
date: 2026-08-21
tags: [black-forest-labs, flux-video-upscale, project]
aliases: ["FLUX Video Upscale"]
level: 2
source_sha256: 1d7cf6ba7163e65ec8d2649189ce2027fa402c8ce9c87c197f63062ad925d17c
translation: machine
translated_at: '2026-10-24'
---
# FLUX Video Upscale — Black Forest Labs {#flux-video-upscale-black-forest-labs}

**Entwicklungslinie:** `project:flux-video-upscale` · Thread `black-forest-labs`  
**Letztes Ereignis:** 2026-08-21 · 1 datiertes seit 2026-08-21 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

FLUX Video Upscale ist ein Video-Super-Resolution-Endpunkt von FLUX 3 für API-Nutzer.

- Videoskalierung im Maßstab 1,5×–3×, bis 4K.
- Precise-Modus für identitätskritisches Material und Creative-Modus für generierte Details.
- Erhalt der Audiospur des Quellmaterials.

Eingaben sind höchstens 20 Sekunden, 50 MB und 2560×1440; die Ausgabe-Frames sind auf etwa 14,4 MP begrenzt.

Precise verwenden für Gesichter, Produkte und Markenassets; Creative verwenden für generierte Landschaften und Texturen, bei denen Detailreichtum wichtiger ist als exakte Identität.

## Entwicklungslinie {#development-line}

- **2026-08-21 — Black Forest Labs hat FLUX Video Upscale vorgestellt.** Am 2026-08-21 verlinkte Black Forest Labs eine offizielle Blog-Ankündigung, Produktdokumentation und ein Playground-Modell für FLUX Video Upscale. Die offiziellen Links belegen die öffentliche Vorstellung, zeigen aber keine detaillierten Fähigkeiten, Verfügbarkeit, Preise oder Leistungswerte.

## Was sich geändert hat {#what-changed}

2026-08-21 — FLUX Video Upscale wurde als eigenständiges Tool `POST /v1/flux-tools/video-upscale-v1` verfügbar, im Anschluss an die BFL-Veröffentlichung vom 20. August. Der Launch brachte Video-Super-Resolution im Maßstab 1,5×–3×, zwei `creativity`-Modi, erhaltenes Audio und Abrechnung nur für die Ausgabe.

2026-08-26 — Der aktuelle Tool-Katalog von BFL führte Video Upscale neben seinen anderen Bearbeitungs-Endpunkten auf, was seine Rolle als FLUX Tool mit demselben asynchronen Submit-and-Poll-Workflow bestätigt.

## So wird es verwendet {#how-to-use-this}

Ab dem 2026-08-21 evaluieren wir FLUX Video Upscale über den dokumentierten Workflow von Black Forest Labs und den verlinkten Playground, statt es als nicht angekündigte oder undokumentierte Funktion zu behandeln.

1. Eine MP4-Datei mit höchstens 20 Sekunden vorbereiten und sie entweder unter einer erreichbaren HTTPS-URL bereitstellen oder als Base64 kodieren.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
2. `input_video`, einen `upscale_factor` von 1,5 bis 3 und `creativity` an `/v1/flux-tools/video-upscale-v1` per POST senden.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
3. Die zurückgegebene `polling_url` abfragen, bis der Status `Ready` ist, und danach `result.sample` herunterladen, bevor die signierte URL abläuft.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>

## Best Practices {#best-practices}

- `creativity: 0` für Gesichter, Produkte, Logos und anderes Material verwenden, dessen Identität stabil bleiben muss.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
- `creativity: 1` für generiertes Material, Texturen, Menschenmengen und Landschaften verwenden; einen kurzen Inhaltsprompt nur hinzufügen, wenn die Steuerung erfundener Details hilfreich ist.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
- Das am wenigsten komprimierte Quellmaterial nach dem Bearbeiten und Schneiden skalieren, damit Artefakte nicht verstärkt werden und die reine Ausgabenabrechnung nur das behaltene Material umfasst.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>

## Hierdurch ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Unser Eintrag datiert das Ereignis auf 2026-08-21, während die eigene Release-Notiz und der Blog von BFL den Launch auf 2026-08-20 datieren; die Verbreitung wurde vermutlich einen Tag später erfasst.
- Während der Recherche hatten wir keine unabhängig zugängliche Playground-Antwort, daher wurden die aktuellen Bedienelemente des Browser-UI und die Verfügbarkeit nach Kontostufe nicht überprüft.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://bfl.ai/blog/flux-video-upscale | FLUX Upscale: 2K und 4K für Video | 2026-09-05 |
| https://docs.bfl.ai/flux_tools/flux_video_upscale | FLUX Video Upscale | 2026-09-05 |
| https://docs.bfl.ai/release-notes | Release Notes | 2026-09-05 |
| https://help.bfl.ai/articles/5950329591-what-are-the-flux-tools | What are the FLUX Tools? | 2026-09-05 |
| https://bfl.ai/video-upscaler | FLUX Video Upscale: KI-Videoupscaler auf 1080p, 2K und 4K | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:flux-video-upscale`, Thread `black-forest-labs`, 1 datiertes Ereignis 2026-08-21 → 2026-08-21.
- **Praxishinweis:** Ab dem 2026-08-21 FLUX Video Upscale über den dokumentierten Workflow von Black Forest Labs und den verlinkten Playground evaluieren, statt es als nicht angekündigte oder undokumentierte Funktion zu behandeln.
- **Konfidenz:** hoch. Datierte Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
