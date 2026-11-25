---
title: "AutoDesign"
category: projects

tags: [autodesign, autodesign-development, project, yaxin9luo/autodesign]
aliases: ["AutoDesign"]
level: 2
source_sha256: 2f3e360e6403e9bd73a35791d92fdec022fe6ceb0717af8011095fc1fb9583df
translation: machine
translated_at: '2026-10-24'
---
# AutoDesign {#autodesign}

**Entwicklungslinie:** `project:autodesign` · Thread `autodesign-development`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

AutoDesign ist ein MIT-Projekt für Forschende und Teams, die mithilfe eines Coding-Agents und eines gewählten LLM-Anbieters bearbeitbare Materialien aus einer Paper-PDF benötigen.

- Generierung: erzeugt ein HTML-Poster, Folien, eine Landingpage und ein untertiteltes Video.
- Lokale Speicherung: speichert Manifeste, Run-Events, Kandidaten und Ausgaben lokal.
- Harness-Optimierung: optimiert das umgebende Agent-Harness und nicht die Gewichte des Basismodells.

Die formale Auswertung mit PosterBench deckt nur akademische Poster ab; Folien, Webseiten und Videos bleiben Pilotspuren.
Wir können es für einen reproduzierbaren Workflow von Paper zu Poster nutzen; andere Formate sollten anhand eigener Beispiele getestet werden.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; das bisher Bekannte steht in den folgenden Abschnitten.

## Was sich geändert hat {#what-changed}

- 2026-08-13 — Das Paper stellte AutoDesign als Meta-Harness für Paper-zu-Poster und PosterBench vor: 100 Paper im Hauptset und 10 im kontrollierten Mini-Set; die Autorinnen und Autoren berichteten 78,32 Punkte im Main Track und 253 Tool-Aufrufe über 40 Minuten autonomer Ausführung.
- 2026-08-14 — Erste öffentliche Repository-Veröffentlichung.
- 2026-08-16 — AutoDesign wurde als öffentliches Projekt mit Quellcode und Weboberfläche verfügbar; der bestätigte Umfang ist die Umwandlung multimodaler Quellen in akademische Poster, nicht ein allgemeiner UI-Generator.
- 2026-08-17 — Eigenständige Agent Skills für Poster, Präsentationen, Webseiten und Videos wurden verfügbar.
- 2026-08-18 — Der Poster Skill wechselte zu agent-first v2: direkte PDF-Verarbeitung, revisionsgebundene Versuche und schreibgeschützte DOM-QA.
- 2026-08-19 — Die Web-UI erhielt Steuerelemente für die Poster-Canvas: Vorlagen, Seitenverhältnisse, exakte Maße und akademische Voreinstellungen.

## So nutzen Sie das {#how-to-use-this}

Stand 2026-08-16 können Praktikerinnen und Praktiker die verlinkte AutoDesign-Website und das Repository als Quellen zur Prüfung behandeln. Aus diesem reinen Link-Eintrag sollte jedoch kein verifizierter Release, keine verifizierte Fähigkeit und keine verifizierte Änderung des Workflows abgeleitet werden.

1. Installieren Sie Node.js 22+ und ffmpeg/ffprobe, starten Sie den lokalen Launcher und prüfen Sie die Umgebung mit `autodesign doctor`.
  — <https://github.com/Yaxin9Luo/AutoDesign>
2. Zum Ausführen aus dem Quellcode installieren Sie die Abhängigkeiten mit `uv sync`, installieren die Playwright-Browser und konfigurieren die Laufzeitumgebung für Video sowie die Abhängigkeiten des Web-Clients.
  — <https://github.com/Yaxin9Luo/AutoDesign>
3. Laden Sie eine PDF hoch und starten Sie Paper All-in-One oder rufen Sie `python -m autodesign run` mit der PDF und der Poster-Vorlage auf.
  — <https://github.com/Yaxin9Luo/AutoDesign>
4. Prüfen Sie `final/poster.html`, die Vorschau, das finale Manifest und `run_events.jsonl`; das bloße Vorhandensein von Dateien garantiert keinen erfolgreichen Validierungsabschluss.
  — <https://github.com/Yaxin9Luo/AutoDesign>

## Bewährte Vorgehensweisen {#best-practices}

- Verwenden Sie Referenzposter nur für das visuelle System: Ihre Texte, Logos, QR-Codes, Tabellen und Links dürfen nicht zur Grundlage neuer Arbeiten werden.
  — <https://github.com/Yaxin9Luo/AutoDesign>
- Werten Sie Statusmeldungen im Terminal und das Feedback des Manifests aus, anstatt eine erzeugte Datei als Erfolgsnachweis zu behandeln.
  — <https://github.com/Yaxin9Luo/AutoDesign>
- Verwenden Sie für neue Automatisierungen `autodesign` und `AUTODESIGN_*`; die älteren Namen `design_anything` und `DESIGN_ANYTHING_*` sind veraltete Aliase.
  — <https://github.com/Yaxin9Luo/AutoDesign>

## Abgelöst durch {#superseded-by-this}

- 2026-08-17 — Die monolithische Nutzung ausschließlich als Server ist nicht mehr erforderlich: Es stehen eigenständig installierbare Agent Skills zur Verfügung.
- 2026-08-18 — Der bisherige Poster Skill wurde für PDF-orientierte Workflows und DOM-QA durch agent-first v2 ersetzt.
- Die aktuelle Dokumentation kennzeichnet `design_anything`, `design-anything`, `designanything` und `DESIGN_ANYTHING_*` als veraltete Kompatibilitätsaliase; neue Setups verwenden `autodesign` und `AUTODESIGN_*`.

## Weiterhin unbekannt {#still-unknown}

- Die von den Autorinnen und Autoren veröffentlichten Benchmark-Ergebnisse und Bewertungen durch Menschen wurden in dieser Prüfung nicht unabhängig reproduziert.
- Die Stabilität der gehosteten Demo und die Produktionsreife der mitgelieferten Integrationen sind nicht verifiziert.
- Das Ereignis vom 2026-08-16 hat keine eigene datierte Primärquelle; die Details stützen sich auf das Paper vom 2026-08-13 und die öffentliche Veröffentlichung vom 2026-08-14.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/Yaxin9Luo/AutoDesign | Yaxin9Luo/AutoDesign | 2026-09-05 |
| https://arxiv.org/abs/2608.13560 | AutoDesign: Meta-Harness Optimization for Long-Horizon Agentic Design | 2026-09-05 |

## Kurzbrief für Agents {#agent-brief}

- **Gegenstand:** `project:autodesign`, Thread `autodesign-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-08-16 können Praktikerinnen und Praktiker die verlinkte AutoDesign-Website und das Repository als Quellen zur Prüfung behandeln. Aus diesem reinen Link-Eintrag sollte jedoch kein verifizierter Release, keine verifizierte Fähigkeit und keine verifizierte Änderung des Workflows abgeleitet werden.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
