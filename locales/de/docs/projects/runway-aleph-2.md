---
title: "Aleph 2.0 — Runway Aleph"
category: projects
date: 2026-05-23
tags: [project, runway-aleph, runway-aleph-2]
aliases: ["Aleph 2.0"]
level: 3
source_sha256: b8bb32f71a4710812a36a5db71e0ac2de98b73252e692a68ee6ef3662c591edb
translation: machine
translated_at: '2026-10-24'
---
# Aleph 2.0 — Runway Aleph {#aleph-20-runway-aleph}

**Entwicklungslinie:** `project:runway-aleph-2` · Thread `runway-aleph`  
**Letztes Ereignis:** 2026-05-23 · 1 datiertes seit 2026-05-23 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

Aleph 2.0 ist Runways In-Context-Editor für bestehendes Filmmaterial, entwickelt für Teams, die ein Produkt, einen Hintergrund, die Beleuchtung oder den Stil ändern müssen, ohne die Einstellung neu aufzunehmen.

- Keyframe-Propagation über relevante Frames und Multi-Shot-Sequenzen hinweg.
- Videogenerierung aus Video plus Texthinweis oder optionaler Bildvorgabe.
- Export als MP4, ProRes, PNG-Sequenz oder 10-Bit-SDR; HDR erfordert einen separaten Konvertierungsschritt.

Eingaben umfassen 2–30 Sekunden, bis zu 1080p und 30 fps; die Rate der Dev API beträgt 28 Credits pro Sekunde mit einem Minimum von 56 Credits. Wir nutzen es für quellgetreues Retuschieren; testen Sie komplexe, sich bewegende Ergänzungen, bevor Sie eine Auslieferung zusagen.

## Entwicklungslinie {#development-line}

- **2026-05-23 — Runway stellte Aleph 2.0 vor.** Am 2026-05-23 kennzeichnete ein datierter Produktlink von Runway selbst Aleph 2.0 als Entwicklungsmeilenstein der Aleph-Linie. Dieser Link nennt das Produkt, belegt aber keine konkreten Funktionen, Verfügbarkeitsbedingungen, Preise oder technischen Änderungen.

## Was sich geändert hat {#what-changed}

- 2026-05-21 — Aleph 2.0 startete mit Edit Studio für kostenpflichtige Pläne in der Desktop-Webanwendung und ergänzte 30-Sekunden-Clips in 1080p, lokalisierte, frame-basierte Bearbeitungen sowie Propagation über mehrere Einstellungen hinweg.
- 2026-05-23 — Die mitgelieferte Produktseite von Aleph 2.0 dokumentiert den aktuellen Produktumfang, ist aber undatiert und belegt keine eigenständige Veröffentlichung oder Änderung an diesem Datum.
- 2026-06-02 — Aleph 2.0 wurde in der Runway Dev API als `aleph2` für Video-zu-Video-Bearbeitung mit Text und zeitgestempelten Keyframes bereitgestellt.
- 2026-06-22 — Aleph 2.0 wurde als zeitgestempelter Keyframe-Node in Figma Weave verfügbar.
- 2026-07-14 — Aleph 2.0 ließ sich über das Werkzeug Edit Video von Runway MCP aufrufen.
- 2026-07-30 — Runway Dev stellte `gen4_aleph` außer Betrieb; API-Nutzer müssen auf `aleph2` migrieren.
- 2026-08-10 — Edit Studio erhielt ProRes 4444 mit PCM-Audio und PNG-Sequenz-Export für vollständige Clip-Bearbeitungen mit Aleph 2.0.
- 2026-08-20 — Aleph 2.0 unterstützt nun 10-Bit-Rec.709-SDR-Ausgabe; weiterhin wird kein natives HDR gerendert.

## So wird es verwendet {#how-to-use-this}

1. Öffnen Sie Edit Studio in der Desktop-Webanwendung von Runway und beginnen Sie mit einem vorhandenen Videoclip.
  — <https://runway.com/news/introducing-aleph-2-and-edit-studio>
2. Laden Sie einen Clip mit 2–30 Sekunden, bis zu 1080p und maximal 30 fps hoch.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
3. Wählen Sie einen Keyframe, in dem das Ziel klar sichtbar ist: einen Totalen für eine Umgebungsänderung und eine Nahaufnahme für eine Detailänderung.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
4. Formulieren Sie eine Aktion und die gewünschte Transformation; fügen Sie nur dann ein Referenzbild hinzu, wenn es hilft, Motiv, Produkt oder Stil zu steuern.
  — <https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide>
5. Zeigen Sie die Vorschau des Keyframe-Edits an und verfeinern Sie ihn, wählen Sie die gewünschte Version aus und generieren Sie dann das Video.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
6. Wählen Sie MP4, ProRes oder PNG-Sequenz, bevor Sie eine vollständige Clip-Generierung starten; eine Bearbeitung eines Teilbereichs liefert immer MP4.
  — <https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats>

## Best Practices {#best-practices}

- Beginnen Sie mit einem kurzen, gezielten Prompt: einem Aktionsverb plus der gewünschten Transformation; ergänzen Sie Details nur bei Bedarf.
  — <https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide>
- Prüfen Sie die Vorschau des bearbeiteten Keyframes, bevor Sie die Videogenerierung bezahlen, und iterieren Sie die Bildbearbeitung, bis die Änderung stimmt.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
- Verwenden Sie Extra motion nur, wenn die neue Bewegung weder im Originalclip noch im bearbeiteten Keyframe vorhanden ist.
  — <https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide>
- Verwenden Sie für die Erweiterung des Seitenverhältnisses einen Einzeleinstellungs-Clip ohne Schnitte und prüfen Sie, ob die Vorschau die ursprüngliche Bildkomposition beibehält.
  — <https://help.runwayml.com/hc/en-us/articles/52264567609363-Expanding-a-video-s-aspect-ratio-with-Edit-Studio>
- Wählen Sie das Auslieferungsformat vor der Generierung: Es lässt sich danach nicht mehr ändern, und ProRes oder PNG-Sequenz erfordert eine Bearbeitung des gesamten Clips.
  — <https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats>
- Betrachten Sie einen unabhängigen Test mit sieben Szenarien nur als Richtungshinweis: Er ergab, dass Aleph bei konservativen Packshot-, Text- und Retusche-Arbeiten am stärksten ist, während komplex neu bewegte Motive Nacharbeit erforderten.
  — <https://journal.everypixel.com/runway-aleph-2-vs-gemini-omni>

## Dadurch abgelöst {#superseded-by-this}

- 2026-06-02 — Bevorzugen Sie `aleph2` gegenüber dem veralteten API-Alias `aleph2_alpha`.
- 2026-07-30 — `gen4_aleph` ist kein verwendbarer Modellbezeichner in Runway Dev mehr; Aufrufe schlagen fehl und müssen auf `aleph2` umgestellt werden.
- 2026-08-20 — Planen Sie kein natives HDR mit Aleph 2.0 ein: Die aktuelle API-Ausgabe ist 10-Bit-SDR, für HDR ist anschließend `/v1/video_to_hdr` erforderlich.

## Weiterhin unbekannt {#still-unknown}

- Die mitgelieferte Produktseite ist undatiert, daher lässt sich ihr genauer Inhalt am 2026-05-23 nicht rekonstruieren; der datierte Launch ist der 2026-05-21.
- Die Herkunft bleibt ungeklärt, da mehrere Subjekt-Schlüssel dieselbe Historie teilen; behaupten Sie keine Vorgängerbeziehung, bis sie geprüft wurde.
- Es wurde keine offizielle Dokumentation von Aleph 2.0 in vereinfachtem Chinesisch gefunden; die chinesischsprachigen Treffer waren Drittanbieter-Tutorials und wurden für die Kernaussagen nicht verwendet.
- Runways allgemeiner Edit-Studio-Leitfaden sagt weiterhin, dass Expand bald verfügbar sei, während der eigene Leitfaden zum Expand Ratio es als aktiv dokumentiert; das Aktivierungsdatum ist unbekannt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://runwayml.com/product/aleph-2 | Aleph 2.0 | Runway (leitet weiter auf runway.com) | 2026-09-06 |
| https://runway.com/product/aleph-2 | Aleph 2.0 | Runway | 2026-09-06 |
| https://runway.com/news/introducing-aleph-2-and-edit-studio | Introducing Aleph 2.0 and Edit Studio | 2026-09-06 |
| https://docs.dev.runwayml.com/api-details/api_changelog/ | API Changelog & Updates | Runway Dev | 2026-09-06 |
| https://runway.com/news/aleph-2-in-figma-weave | Aleph 2.0 Is Now in Figma Weave | 2026-09-06 |
| https://runway.com/changelog | Product Updates & Changelog | Runway AI | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio | Creating with Edit Studio | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide | Aleph 2.0 Prompting Guide | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats | Exporting Videos in ProRes and PNG Sequence Formats | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/52264567609363-Expanding-a-video-s-aspect-ratio-with-Edit-Studio | Expanding a video's aspect ratio with Edit Studio | 2026-09-06 |
| https://docs.dev.runwayml.com/guides/models/ | Available AI Models | Runway Dev | 2026-09-06 |
| https://docs.dev.runwayml.com/guides/pricing/ | API Pricing & Costs | Runway Dev | 2026-09-06 |
| https://journal.everypixel.com/runway-aleph-2-vs-gemini-omni | Runway Aleph 2 vs Gemini Video Omni | 2026-09-06 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:runway-aleph-2`, Thread `runway-aleph`, 1 datiertes Ereignis 2026-05-23 → 2026-05-23.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Verwendung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
