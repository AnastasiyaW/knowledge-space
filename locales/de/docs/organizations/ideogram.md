---
title: "Ideogram"
category: projects
date: 2025-07-31
tags: [ideogram, ideogram_3_0, model-and-product-releases, project]
aliases: ["Ideogram"]
level: 3
source_sha256: b5e23fb4486cb3f224942a11c8c94d19136378e6c39f6fc1ab65eeeb2a5939cb
translation: machine
translated_at: '2026-10-24'
---
# Ideogram {#ideogram}

**Entwicklungslinie:** `project:ideogram` · Thread `model-and-product-releases`  
**Letztes Ereignis:** 2025-07-31 · 3 datierte Ereignisse seit 2024-03-01 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Ideogram ist eine Plattform zur Bilderzeugung für Designer, Content-Teams und Entwickler, die gut lesbaren Text, Kompositionskontrolle und iterative Bearbeitung benötigen.

- Ideogram 4.0: 2K-Generierung, Layoutkontrolle, bearbeitbare Elemente und offene Gewichte.
- Web und API: Generierung, Remix, Inpainting, Hintergrund- und Objektbearbeitung, Upscaling und Custom Models.

Die gehostete API für 4.0 listet $0.03 / $0.06 / $0.10 pro Bild für die Stufen Turbo / Default / Quality. Sie eignet sich für Designassets, die korrigiert, skaliert und überarbeitet werden müssen, und nicht für einmalige Generierung per Einzel-Prompt.

## Entwicklungslinie {#development-line}

- **2024-03-01 — Ideogram kündigt Ideogram 1.0 an.** Öffentliches Text-zu-Bild-Modell mit Fokus auf Typografie in Bildern, Prompt-Treue und Magic Prompt; die offizielle Release-Seite ist auf 2024-02-28 datiert.
- **2025-03-26 — Ideogram kündigt Ideogram 3.0 an.** Style Reference mit bis zu drei Bildern, Style Code zur erneuten Anwendung von Stilen, Batch Generation sowie verbesserte Handhabung von grafischem Text und Layout.
- **2025-07-31 — Ideogram veröffentlicht seine Seite zum Character-Feature.** Ein Referenzbild zur Wahrung der Figurenidentität über verschiedene Szenen hinweg; Masking, Magic Fill und Remix wurden in den Character-Workflow aufgenommen.

## Was sich geändert hat {#what-changed}

- 2024-03-01 — Ideogram 1.0: öffentliches Text-zu-Bild-Modell mit Fokus auf Typografie in Bildern, Prompt-Treue und Magic Prompt; die offizielle Release-Seite ist auf 2024-02-28 datiert.
- 2024-08-21 — Ideogram 2.0: ergänzt um die Stile Realistic, Design, 3D und Anime, Palettenkontrolle, eine iOS-App, eine Beta-API und öffentliche Bildersuche.
- 2025-03-26 — Ideogram 3.0: Style Reference mit bis zu drei Bildern, Style Code zur erneuten Anwendung von Stilen, Batch Generation sowie verbesserte Handhabung von grafischem Text und Layout.
- 2025-07-31 — Ideogram Character: ein Referenzbild zur Wahrung der Figurenidentität über verschiedene Szenen hinweg; Masking, Magic Fill und Remix wurden in den Character-Workflow aufgenommen.
- 2026-06-03 — Ideogram 4.0 verlagert die aktive Linie auf ein Modell mit offenen Gewichten, JSON-Szenenbeschreibungen, Palettenkontrolle und optionalen Bounding Boxes.
- 2026-06-18 — Die offizielle Dokumentation bestätigt, dass ältere Freiform-Prompts in 4.0 sich möglicherweise anders verhalten; für exakte Farben, Texte und Layouts ist strukturiertes JSON erforderlich.

## So wird es verwendet {#how-to-use-this}

Stand 2025-07-31 sollten Praktiker bei der Bewertung der Bilderzeugungsoptionen den aktuellen Character-Workflow von Ideogram prüfen; die vorliegenden datierten Links belegen Versionsmeilensteine und einen Character-Produktbereich, aber keine Implementierungsdetails.

1. Ideogram öffnen, anmelden und in Creative mit Ideogram 4.0 starten; Studio und Hilfswerkzeuge sind dort ebenfalls verfügbar.
  — <https://ideogram.ai/>
2. Für ein erstes Konzept die Szene in ausführlichem natürlichem Text beschreiben: Der Live-Ideogram-4.0-Magic-Prompt erweitert einfachen Text automatisch zu einer strukturierten Beschreibung.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
3. Wenn Farbe, Komposition oder Typografie exakt sein müssen, JSON mit high_level_description, style_description, background und elements verwenden; wörtlichen Text und bbox für Schriftzüge angeben.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
4. Nach einem guten Ergebnis style_code und seed speichern: Ersteres fixiert den visuellen Stil, Letzteres ermöglicht kontrollierte Kompositionsvarianten.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
5. Für eine Serie mit einem konsistenten Motiv Character öffnen, ein klares Porträt hochladen, die Szene beschreiben und Maske, Magic Fill oder Remix bei Bedarf anpassen.
  — <https://ideogram.ai/features/character/>
6. Für die Produktintegration einen API-Schlüssel konfigurieren und POST /v1/ideogram-v4/generate aufrufen; die Character-Referenz im aktuellen Quickstart läuft als separater v3-Aufruf.
  — <https://developer.ideogram.ai/ideogram-api/api-overview>

## Best Practices {#best-practices}

- In 4.0 vage Stimmungsbeschreibungen durch Konkretes ersetzen: Lichtquelle, Medium, Palette, Objekte und deren Anordnung.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Den Zyklus einhalten: Klartext zum Erkunden von Ideen, style_code zum Fixieren eines erfolgreichen Stils und JSON für strikte Markenvorgaben.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Gewünschte Schriftzüge in doppelte Anführungszeichen setzen, jeden Textausschnitt auf 5–7 Wörter begrenzen und für fehlerkritische Typografie die Stufe Quality wählen.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Produktionsworkflows nicht auf Random Style aufbauen: Die Dokumentation kennzeichnet ihn als veraltet; für reproduzierbare Ergebnisse einen gespeicherten Style Code oder eine eigene Style Reference verwenden.
  — <https://docs.ideogram.ai/using-ideogram/generation-settings/styles>
- Für Character ein klares, gut ausgeleuchtetes Porträt verwenden, das frontal oder dreiviertel ausgerichtet ist, und die Maske so anpassen, dass Haare, Kleidung und Accessoires erhalten bleiben oder ersetzt werden.
  — <https://ideogram.ai/features/character/>

## Damit überholt {#superseded-by-this}

- 2024-03-01 — Ideogram 1.0 als aktives Flaggschiffmodell zu behandeln, ist veraltet: Die aktuelle Linie ist Ideogram 4.0.
- 2025-03-26 — Stile über Random oder "4.3 billion presets" zu durchsuchen, ist veraltet: Die aktuelle Dokumentation kennzeichnet den Random-Modus als veraltet.
- 2025-03-26 — Sich auf lange Freiform-Prompts für exakte Typografie und Layout zu verlassen, ist in Ideogram 4.0 veraltet: Präzise Ausgabe erfordert strukturiertes JSON, Textelemente und Bounding Boxes.

## Weiterhin unbekannt {#still-unknown}

- Der Eintrag vom 2024-08-21 enthält nur die URL der Startseite: Die offizielle Release-Seite bestätigt Datum und Inhalt von Ideogram 2.0, der ursprüngliche Wortlaut des Eintrags ist jedoch nicht verfügbar.
- Die älteren offiziellen URLs /1.0, /2.0 und /3.0 leiten inzwischen auf neue Seiten weiter; die langfristige Überprüfung historischer Aussagen erfordert separate Archivaufnahmen.
- Die aktuelle API-Dokumentation stützt die Basisgenerierung auf v4, das Beispiel für die Character-Referenz verwendet aber noch v3; die öffentliche Dokumentation bestätigt keinen eigenen v4-Character-Endpunkt.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://about.ideogram.ai/1.0 | Ideogram 1.0, Feb 2024 | 2026-09-04 |
| https://about.ideogram.ai/2.0 | Ideogram 2.0 | 2026-09-04 |
| https://about.ideogram.ai/3.0 | Ideogram 3.0 | 2026-09-04 |
| https://about.ideogram.ai/character | Ideogram Character | 2026-09-04 |
| https://ideogram.ai/ | Ideogram | KI-Apps und Modelle auf einer Plattform | 2026-09-04 |
| https://ideogram.ai/models/3.0/ | Ideogram 3.0 — Realismus, Design und konsistente Stile | 2026-09-04 |
| https://ideogram.ai/models/4.0/ | Ideogram 4.0 | Ideogram | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technische Details: Offenes Modell an der Spitze des Designs | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4-json-prompting/ | So erstellst du JSON-Prompts für Ideogram 4.0 | 2026-09-04 |
| https://ideogram.ai/features/character/ | Figurenkonsistenz aus einem Foto: Kostenloser KI-Headshot-Generator | Ideogram | 2026-09-04 |
| https://docs.ideogram.ai/using-ideogram/generation-settings/styles | Style Reference | Ideogram | 2026-09-04 |
| https://developer.ideogram.ai/ideogram-api/api-overview | API Overview | Ideogram | Dokumentation | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:ideogram`, Thread `model-and-product-releases`, 3 datierte Ereignisse 2024-03-01 → 2025-07-31.
- **Praxishinweis:** Stand 2025-07-31 sollten Praktiker bei der Bewertung der Bilderzeugungsoptionen den aktuellen Character-Workflow von Ideogram prüfen; die vorliegenden datierten Links belegen Versionsmeilensteine und einen Character-Produktbereich, aber keine Implementierungsdetails.
- **Konfidenz:** mittel. Die datierten Einträge unter „Damit überholt“ sind maßgeblich dafür, was veraltet ist.
