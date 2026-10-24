---
title: "Ideogram"
category: projects
tags: [ideogram, ideogram_3_0, model-and-product-releases, project]
aliases: ["Ideogram"]
level: 3
source_sha256: 4b19c1dc95877f9796f35755807757307dbf9dce9b06d99ebebcca8acbf049b1
translation: machine
translated_at: '2026-10-24'
---
# Ideogram {#ideogram}

**Entwicklungslinie:** `project:ideogram` · Thread `model-and-product-releases`  
**Ereignisse:** 3 datiert, 2024-03-01 → 2025-07-31 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Ideogram ist eine Plattform für Bildgenerierung für Designer, Content-Teams und Entwickler, die lesbaren Text, Kompositionskontrolle und iterative Bearbeitung benötigen.

- Ideogram 4.0: 2K-Generierung, Layoutkontrolle, bearbeitbare Elemente und offene Gewichte.
- Web und API: Generierung, Remix, Inpaint, Hintergrund- und Objektbearbeitung, Upscale und Custom Models.

Die gehostete API-Preisgestaltung für 4.0 liegt bei $0,03 / $0,06 / $0,10 pro Bild für die Stufen Turbo, Default und Quality. Wähle Ideogram für Designassets, die Korrektur, Reproduktion und Bearbeitung erfordern, statt einer reinen Einzel-Prompt-Generierung.

## Entwicklungslinie {#development-line}

- **2024-03-01 — Ideogram kündigte Ideogram 1.0 an.** Öffentliches Text-zu-Bild-Modell mit Fokus auf Text in Bildern, Prompt-Treue und Magic Prompt; die offizielle Release-Seite ist auf 2024-02-28 datiert.
- **2025-03-26 — Ideogram kündigte Ideogram 3.0 an.** Style Reference unterstützt bis zu drei Bilder, Style Code wendet Stile erneut an, Batch Generation kommt hinzu, mit verbesserter Handhabung von grafischem Text und Layout.
- **2025-07-31 — Ideogram veröffentlichte seine Character-Funktionsseite.** Eine Referenz bewahrt die Identität der Figur über Szenen hinweg; Masking, Magic Fill und Remix sind in den Character-Workflow integriert.

## Was sich geändert hat {#what-changed}

- **2024-03-01 — Ideogram 1.0:** Öffentliches Text-zu-Bild-Modell mit Fokus auf Text in Bildern, Prompt-Treue und Magic Prompt; die offizielle Release-Seite ist auf 2024-02-28 datiert.
- **2024-08-21 — Ideogram 2.0:** Ergänzt wurden die Modi Realistic, Design, 3D und Anime, Palettenkontrolle, eine iOS-App, eine Beta-API und öffentliche Bildsuche; bestätigt auf der offiziellen Release-Seite.
- **2025-03-26 — Ideogram 3.0:** Style Reference mit bis zu drei Bildern, Style Code zur Wiederverwendung von Stilen, Batch Generation sowie verbesserte Handhabung von grafischem Text und Layout.
- **2025-07-31 — Ideogram Character:** Ein Referenzbild bewahrt die Identität der Figur über Szenen hinweg; Masking, Magic Fill und Remix wurden Teil des Character-Workflows.
- **2026-06-03:** Ideogram 4.0 verlagerte die aktive Linie auf ein Modell mit offenen Gewichten, mit JSON-Szenenbeschreibungen, Farbpaletten und optionalen Bounding Boxes.
- **2026-06-18:** Der offizielle Leitfaden bestätigte, dass Legacy-Freitext-Prompts in 4.0 sich anders verhalten können; exakte Farbe, Text und Platzierung erfordern strukturiertes JSON.

## So verwendest du es {#how-to-use-this}

Stand 2025-07-31 sollten Praktiker bei der Bewertung der Bildgenerierungsoptionen von Ideogram den aktuellen Character-Workflow prüfen; die vorliegenden datierten Links belegen Versionsmeilensteine und einen Character-Produktbereich, aber keine Implementierungsdetails.

1. Öffne Ideogram, melde dich an und starte in Creative mit Ideogram 4.0; Studio und Hilfswerkzeuge befinden sich in derselben Oberfläche.
  — <https://ideogram.ai/>
2. Beschreibe die Szene für das erste Konzept in einfachem Text; das aktuelle Ideogram 4.0 verwendet Magic Prompt, um einfachen Text in eine strukturierte Beschreibung zu erweitern.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
3. Verwende JSON mit high_level_description, style_description, background und elements für exakte Farbe, Komposition oder Text; gib wörtlichen Text und bbox für Schriftzüge an.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
4. Speichere style_code und seed nach einem guten Ergebnis: style_code fixiert den visuellen Stil, während seed kontrollierte Kompositionsvariationen ermöglicht.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
5. Für eine Serie mit derselben Figur öffne Character, lade ein klares Porträt hoch, beschreibe die Szene und passe bei Bedarf die Maske, Magic Fill oder Remix an.
  — <https://ideogram.ai/features/character/>
6. Für die Produktintegration konfiguriere einen API-Schlüssel und rufe POST /v1/ideogram-v4/generate auf; das aktuelle Quickstart zeigt die Character-Referenz als separaten v3-Aufruf.
  — <https://developer.ideogram.ai/ideogram-api/api-overview>

## Best Practices {#best-practices}

- Ersetze in 4.0 vage Stimmungswörter durch konkrete Details: Lichtquelle, Medium, Palette, Objekte und räumliche Platzierung.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Folge dem Zyklus: einfacher Text für die Konzeptsuche, style_code zum Fixieren eines Looks, JSON für exakte Markenvorgaben.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Setze gewünschte Schriftzüge in doppelte Anführungszeichen, halte jeden Textausschnitt bei etwa 5–7 Wörtern und wähle Quality für fehleranfällige Typografie.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Baue aktuelle Workflows nicht auf Random Style auf, da Ideogram es als veraltet markiert hat; verwende stattdessen gespeicherte Style Codes oder eigene Style Reference.
  — <https://docs.ideogram.ai/using-ideogram/generation-settings/styles>
- Verwende für Character ein klares, gut ausgeleuchtetes Porträt, das frontal oder dreiviertel ausgerichtet ist, und bearbeite die Maske, um Haare, Kleidung oder Accessoires zu erhalten oder zu ersetzen.
  — <https://ideogram.ai/features/character/>

## Hierdurch abgelöst {#superseded-by-this}

- 2024-03-01 — Ideogram 1.0 als aktives Hauptmodell zu behandeln, ist veraltet; das aktuelle Release ist Ideogram 4.0.
- 2025-03-26 — Stile über den Random-Modus und seine 4,3 Milliarden Presets zu suchen, ist veraltet; die aktuelle Dokumentation markiert den Random-Modus als veraltet.
- 2025-03-26 — Auf lange Freitext-Prompts für exakten Text und exaktes Layout zu setzen, ist für Ideogram 4.0 veraltet; strikte Ausgaben erfordern strukturiertes JSON, Textelemente und bbox.

## Weiterhin unbekannt {#still-unknown}

- Der Eintrag vom 2024-08-21 enthält nur die Adresse der Hauptseite; die offizielle Release-Seite bestätigt Datum und Inhalt von Ideogram 2.0, doch der Wortlaut des ursprünglichen Beitrags ist nicht verfügbar.
- Die früheren offiziellen URLs /1.0, /2.0 und /3.0 leiten inzwischen auf neue Seiten weiter; die langfristige Erhaltung historischer Aussagen erfordert separate archivierte Snapshots.
- Die aktuelle API zeigt die Standardgenerierung auf v4, während das Character-Referenzbeispiel noch v3 verwendet; die öffentliche Dokumentation bestätigt keinen eigenen v4-Character-Endpunkt.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://about.ideogram.ai/1.0 | Ideogram 1.0, Feb 2024 | 2026-09-04 |
| https://about.ideogram.ai/2.0 | Ideogram 2.0 | 2026-09-04 |
| https://about.ideogram.ai/3.0 | Ideogram 3.0 | 2026-09-04 |
| https://about.ideogram.ai/character | Ideogram Character | 2026-09-04 |
| https://ideogram.ai/ | Ideogram | AI apps and models in one platform | 2026-09-04 |
| https://ideogram.ai/models/3.0/ | Ideogram 3.0 — Realism, design, and consistent styles | 2026-09-04 |
| https://ideogram.ai/models/4.0/ | Ideogram 4.0 | Ideogram | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technical Details: Open model at the forefront of design | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4-json-prompting/ | How to JSON prompt for Ideogram 4.0 | 2026-09-04 |
| https://ideogram.ai/features/character/ | Character Consistency from One Photo: Free AI Headshot Generator | Ideogram | 2026-09-04 |
| https://docs.ideogram.ai/using-ideogram/generation-settings/styles | Style Reference | Ideogram | 2026-09-04 |
| https://developer.ideogram.ai/ideogram-api/api-overview | API Overview | Ideogram | Documentation | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:ideogram`, Thread `model-and-product-releases`, 3 datierte Ereignisse 2024-03-01 → 2025-07-31.
- **Praxishinweis:** Stand 2025-07-31 sollten Praktiker bei der Bewertung der Bildgenerierungsoptionen von Ideogram den aktuellen Character-Workflow prüfen; die vorliegenden datierten Links belegen Versionsmeilensteine und einen Character-Produktbereich, aber keine Implementierungsdetails.
- **Konfidenz:** mittel. Die datierten Einträge unter „Hierdurch abgelöst“ sind maßgeblich dafür, was veraltet ist.
