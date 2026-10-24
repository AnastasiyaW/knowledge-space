---
title: "FLUX 3"
category: projects
date: 2026-08-05
tags: [flux-3, flux-3-development, flux_3, project]
aliases: ["FLUX 3"]
level: 2
source_sha256: bfbeac1ecf848db22f2a80bbbdaa68e416c9028bc8020e43daab24f145eee645
translation: machine
translated_at: '2026-10-24'
---
# FLUX 3 {#flux-3}

**Entwicklungslinie:** `project:flux-3` · Thread `flux-3-development`  
**Letztes Ereignis:** 2026-08-05 · 2 datierte seit 2026-07-24 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

FLUX 3 ist ein Vorschau-Videomodell von BFL für Creator und API-Teams, die kurze audiovisuelle Clips erstellen.

- Videogenerierung: Text-zu-Video, Bild- oder Keyframe-zu-Video sowie Videofortsetzung, ausgeführt über den Endpunkt flux-3-video.
- Ausgabespezifikation: Video mit 24 fps und synchronisierter Sprache, Soundeffekten und Atmosphäre.

## Entwicklungslinie {#development-line}

- **2026-07-24 — Black Forest Labs veröffentlichte ein Blog-Update zu FLUX 3.** FLUX 3 startete als einheitliches multimodales Modell in der Early Access. Black Forest Labs staffelte den Zugang zu Video, Image, Action und Dev getrennt.
- **2026-08-05 — FLUX 3 wurde über Produktoberflächen von Black Forest Labs hinweg verlinkt.** Die Seiten zu Modell und Quick Start tragen keine Datumsangaben. Die verlinkte Playground-Route liefert einen Fehler.

## Was sich geändert hat {#what-changed}

2026-07-24 — Das zitierte Launch-Material ist auf 2026-07-23 datiert: FLUX 3 startete als einheitliches multimodales Modell in der Early Access, während der Zugang zu Video, Image, Action und Dev getrennt gestaffelt wurde. 2026-08-04 — BFL machte ein erstes FLUX 3 Video über seine API und ausgewählte Partner allgemein verfügbar. 2026-08-05 — Eine separate Fähigkeitsveröffentlichung lässt sich nicht verifizieren: Die Seiten zu Modell und Quick Start sind undatiert, und die zugehörige Playground-Route liefert nun einen Fehler. 2026-08-20 — FLUX Upscale wurde als eigenständiger Endpunkt gestartet, der Videos bis zur nativen Auflösung 4K neu rendern kann.

## Anwendung {#how-to-use-this}

Konsultieren Sie vor dem Test von FLUX 3 die Modellseite zu FLUX 3, die Quick-Start-Dokumentation und den Prompt-to-Image-Playground vom 2026-08-05, damit Funktionen und Zugang anhand primärer Quellen verifiziert bleiben.

1. Legen Sie ein BFL-Konto an, laden Sie Credits auf und nutzen Sie dann den Playground oder die API.
  — <https://docs.bfl.ai/flux_3>
2. Für einen neuen Clip senden Sie mode=t2v, einen Prompt und optional die Dauer per POST an den Endpunkt /v1/flux-3-video, mit Ihrem BFL-API-Schlüssel.
  — <https://docs.bfl.ai/flux_3>
3. Für bildgeführtes Video verwenden Sie mode=i2v mit Keyframes; für eine Verlängerung verwenden Sie mode=v2v mit start_video.
  — <https://docs.bfl.ai/flux_3>
4. Fragen Sie die zurückgegebene polling_url ab, bis der Job Ready ist, und laden Sie das Ergebnis herunter, bevor seine signierte URL abläuft.
  — <https://docs.bfl.ai/flux_3>
5. Erstellen Sie Prototypen mit draft=true; senden Sie den draft_cache des ausgewählten Ergebnisses in mode=draft_enhance, um denselben Clip in voller Qualität zu rendern.
  — <https://docs.bfl.ai/flux_3>

## Best Practices {#best-practices}

- Verwenden Sie draft und draft_enhance erst nach der Freigabe einer Vorschau, da ein neuer vollständiger Render den Clip neu interpretieren kann.
  — <https://docs.bfl.ai/flux_3>
- Fixieren Sie Keyframes auf exakte Zeitstempel, wenn ein Übergang kontrolliert werden muss; i2v akzeptiert ein bis zehn Bilder, einschließlich Start- und End-Pins.
  — <https://docs.bfl.ai/flux_3>
- Laden Sie ein Ready-Ergebnis zügig herunter, da seine signierte URL nach etwa zwei Stunden abläuft.
  — <https://docs.bfl.ai/flux_3>
- Verwenden Sie den Modus Upscale Precise, wenn Identität oder Referenzdetails konsistent bleiben müssen, da Creative Identitäten verändern oder ersetzen kann.
  — <https://bfl.ai/blog/flux-video-upscale>

## Durch dies ersetzt {#superseded-by-this}

- 2026-08-04: „FLUX 3 Video ist nur über die Early Access verfügbar“ ist veraltet; BFL machte eine erste Version über seine API und ausgewählte Partner allgemein verfügbar.

## Noch unbekannt {#still-unknown}

- Die Playground-URL vom 2026-08-05 liefert derzeit einen internen Fehler, sodass sich ihr ursprüngliches Modell, ihr Prompt und ihre Ausgabe nicht verifizieren lassen.
- Das Quellpaket vom 2026-08-05 vermischt eine Prompt-to-Image-Playground-Route mit der aktuellen BFL-Dokumentation, die FLUX 3 als Video darstellt. Ohne den ursprünglichen Quelltext ist unklar, ob es sich um dasselbe Produkt FLUX 3 handelt oder um einen allgemeinen Dashboard-Link.
- Die geprüften öffentlichen Quellen erster Hand belegen weder ein Veröffentlichungsdatum noch einen öffentlichen Endpunkt für FLUX 3 Image, FLUX 3 Dev oder FLUX 3 Action nach deren gestaffelten Launch-Plänen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://bfl.ai/blog/flux-3 | FLUX 3 - Real World Models: Towards Multimodal Flow Models as the Backbone of Visual Intelligence. | 2026-09-04 |
| https://bfl.ai/blog/flux-3-video | FLUX 3 Video, Part 1: Generation | 2026-09-04 |
| https://bfl.ai/blog/flux-video-upscale | FLUX Upscale: 2K and 4K for Video | 2026-09-04 |
| https://docs.bfl.ai/flux_3 | FLUX 3 - Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/quick_start/introduction | The frontier of visual intelligence - Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/7655484417-what-flux-models-are-available | Welche FLUX-Modelle sind verfügbar? | Black Forest Labs Wissensdatenbank | 2026-09-04 |
| https://bfl.ai/models/flux-3 | FLUX 3: One Multimodal Model | Black Forest Labs | 2026-09-04 |

## Agent-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:flux-3`, Thread `flux-3-development`, 2 datierte Ereignisse vom 2026-07-24 bis 2026-08-05.
- **Praktischer Hinweis:** Konsultieren Sie vor dem Test von FLUX 3 die Modellseite zu FLUX 3, die Quick-Start-Dokumentation und den Prompt-to-Image-Playground vom 2026-08-05, damit Fähigkeiten und Berechtigung anhand primärer Quellen bestätigt bleiben.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise sind maßgeblich dafür, was veraltet ist.
