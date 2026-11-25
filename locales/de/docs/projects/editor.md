---
title: "Pascal Editor"
category: projects
date: 2026-07-27
tags: [editor, pascal-editor-development, pascal_editor, project]
aliases: ["Pascal Editor"]
level: 3
source_sha256: 3ec53c45d41bdbf4a93551c8169abe954b528cf242d8ac78659bf2bd735f4ad0
translation: machine
translated_at: '2026-10-24'
---
# Pascal Editor {#pascal-editor}

**Entwicklungslinie:** `project:editor` · Thread `pascal-editor-development`  
**Letztes Ereignis:** 2026-07-27 · 1 datiertes Ereignis seit 2026-07-27 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was ist das {#what-it-is}

Pascal Editor ist ein Open-Source-Editor für 3D-Gebäudemodelle mit einem semantischen Szenengraphen.

- Läuft als gehosteter Editor oder als persistente lokale CLI-Laufzeitumgebung.
- Stellt MCP-Tools für die Bearbeitung, Validierung und Speicherung von Projekten und Szenen bereit.
- Veröffentlicht wiederverwendbare React-Pakete zur Einbettung.

## Entwicklungslinie {#development-line}

- **2026-07-27 — GitHub-Repository von Pascal Editor verknüpft.** Am 2026-07-27 haben wir das GitHub-Repository des Projekts verknüpft. Dies bietet eine öffentliche Projektreferenz, dokumentiert jedoch weder ein Release, ein Feature, einen Eigentümerwechsel noch den Zustand des Repositorys.

## Was sich geändert hat {#what-changed}

- 2026-04-09 — Gehostetes Pascal v1.0.0 veröffentlicht, mit einem semantischen Szenengraphen für Menschen und KI-Agenten.
- 2026-04-14 — Gehostetes v1.1.0 ergänzte KI-gestützte Layout-Generierung und einen fotorealistischen Rendering-Tab.
- 2026-05-05 — Gehostetes v1.2.0 ergänzte agentengesteuerte Bearbeitung und SAM3D-Bild-zu-3D.
- 2026-06-09 — Gehostetes v1.3.0 ergänzte Voreinstellungen, Raumvorlagen und verbesserte Manipulation.
- 2026-06-10 — Open-Source-v0.9.1 veröffentlichte die Core-, Viewer- und Editor-Pakete in Version 0.9.1; die angekündigten v0.9.0-Pakete wurden nie auf npm veröffentlicht.
- 2026-06-21 — Gehostetes v1.4.0 ergänzte Materialien, Begehungen aus der Ich-Perspektive und MEP-Werkzeuge.
- 2026-07-08 — Gehostetes v1.5.0 ergänzte ein neu aufgebautes Studio, das erste Editor-Plugin und die Eingabe von Lingo-Einheiten.
- 2026-07-27 — Es wurde kein abgerufener Release oder Changelog-Eintrag des Herstellers gefunden, der an diesem Datum eine Änderung ausweist; die Repository-Referenz ist ein Identitätsverweis, keine Release-Grenze.
- 2026-07-30 — Gehostetes v1.6.0 ergänzte Workflows für Gelände und vertikales Bauen; die zugehörigen Open-Source-Pakete wurden separat als v1.0.0-beta.1 veröffentlicht.
- 2026-08-03 — Gehostetes v1.7.0 ergänzte gemeinsame Bearbeitung im Team, gemeinsam genutzte Cursor und Kameras, gemeinsamen KI-Chat und Material Studio.
- 2026-08-11 — Gehostetes v1.8.0 ergänzte die Pascal CLI und Agentenkonten.
- 2026-08-26 — Gehostetes v1.9.0 ergänzte Bones, Pascal Capture (Mesh-Scanning) und Blockmodellierung.

## Anwendung {#how-to-use-this}

Stand 2026-07-27: Verwenden Sie das verknüpfte GitHub-Repository von Pascal Editor als Referenzpunkt des Projekts, und prüfen Sie dessen Funktionen und Release-Status direkt, bevor Sie sich darauf verlassen.

1. Wählen Sie zuerst einen Projektspeicher: Verwenden Sie gehostetes MCP für Projekte von Pascal-Konten oder -Organisationen oder die lokale CLI für lokale SQLite-Projekte; beide teilen keine Daten.
  — <https://editor.pascal.app/docs/developers/mcp>
2. Für einen lokalen Editor installieren Sie Node.js 22.13+ und führen `npx @pascal-app/cli editor` aus.
  — <https://editor.pascal.app/docs/developers/local-editor>
3. Verbinden Sie einen lokalen Agenten mit `pascal mcp setup <codex|claude>` oder `pascal mcp connect`; konfigurieren Sie den gehosteten Endpunkt nur für gehostete Projekte.
  — <https://editor.pascal.app/docs/developers/mcp>
4. Für eine bestehende Szene verwenden Sie `list_scenes` und anschließend `load_scene`, nehmen semantische Änderungen vor, führen `validate_scene` und `verify_scene` aus und rufen danach `save_scene` und `get_project_status` auf.
  — <https://editor.pascal.app/docs/developers/mcp>
5. Um den Editor einzubetten, installieren Sie die veröffentlichten Pakete und laden das integrierte Plugin, bevor Sie den Viewer einbinden.
  — <https://github.com/pascalorg/editor>

## Bewährte Vorgehensweisen {#best-practices}

- Übernehmen Sie `v1.0.0-beta.1` nicht versehentlich: Es ist ein Prerelease unter dem npm-Tag `beta`, während `latest` auf der 0.x-Linie bleibt.
  — <https://github.com/pascalorg/editor/releases/tag/v1.0.0-beta.1>
- Bei einem Fehler der lokalen Laufzeitumgebung führen Sie zuerst `doctor`, dann `status` aus und prüfen die Logs, bevor Sie einen erzwungenen Stopp verwenden.
  — <https://editor.pascal.app/docs/developers/local-editor>
- Bevorzugen Sie semantische Szenen-Tools gegenüber rohen Patches, und schließen Sie jede Agentenänderung mit Validierung, Verifizierung, Speicherung und einer Prüfung des Projektstatus ab.
  — <https://editor.pascal.app/docs/developers/mcp>
- Für Beiträge zum Quellcode führen Sie `bun check` und `bun run test` aus; ein bloßes `bun test` startet das Test-Skript des Workspaces nicht.
  — <https://github.com/pascalorg/editor/blob/main/CONTRIBUTING.md>

## Abgelöst durch {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Für 2026-07-27 wurde kein Release oder Changelog-Eintrag des Herstellers gefunden; daher kann diesem Datum keine Funktion und keine Version sicher zugeordnet werden.
- Der gehostete Produkt-Changelog und die Open-Source-Paketreleases verwenden unterschiedliche Versionsnummern; die Veröffentlichung vom 30. Juli erklärt diesen Unterschied, aber es wurde keine vollständige spätere Kompatibilitätsmatrix über Versionen hinweg gefunden.
- Es wurde keine offizielle chinesischsprachige Dokumentation und kein unabhängig reproduzierbarer chinesischsprachiger Praxisbericht gefunden; daher ist keine chinesische Praxis enthalten.
- Die Dokumentation der lokalen CLI beschreibt die Unterstützung von Linux und Windows in der Erstveröffentlichung weiterhin als nicht verifiziert; eine aktuelle Plattform-Unterstützungsmatrix wurde nicht gefunden.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/pascalorg/editor | Pascal Editor — GitHub-Repository | 2026-09-06 |
| https://editor.pascal.app/changelog | Changelog | Pascal Editor | 2026-09-06 |
| https://github.com/pascalorg/editor/releases/tag/v0.9.1 | Release v0.9.1 — Preset-System, Räume & Vorlagen, Gebäudemanipulation | 2026-09-06 |
| https://editor.pascal.app/changelog/2026-07-30-terrain-and-community | Gelände formen, dann darauf bauen | Changelog | Pascal Editor | 2026-09-06 |
| https://github.com/pascalorg/editor/releases/tag/v1.0.0-beta.1 | Release Pascal Editor 1.0.0-beta.1 | 2026-09-06 |
| https://editor.pascal.app/docs/developers/local-editor | Pascal lokal ausführen - Pascal | 2026-09-06 |
| https://editor.pascal.app/docs/developers/mcp | KI-Agenten verbinden - Pascal | 2026-09-06 |
| https://github.com/pascalorg/editor/blob/main/CONTRIBUTING.md | Beitrag zu Pascal Editor leisten | 2026-09-06 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:editor`, Thread `pascal-editor-development`, 1 datiertes Ereignis vom 2026-07-27 bis 2026-07-27.
- **Praktischer Hinweis:** Stand 2026-07-27: Verwenden Sie das verknüpfte GitHub-Repository von Pascal Editor als Referenzpunkt des Projekts, und prüfen Sie dessen Funktionen und Release-Status direkt, bevor Sie sich darauf verlassen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
